from __future__ import annotations

import argparse
import sys

from sqlalchemy import select

from app.db import SessionLocal, sema_guncelle
from app.models import AdminUser, User
from app.services import security


def _admin_ac(db, kullanici: str, parola: str) -> int:
    hata = security.check_password(parola)
    if hata:
        print(f"Hata: {hata}", file=sys.stderr)
        return 1
    mevcut = db.scalar(select(AdminUser).where(AdminUser.username == kullanici))
    if mevcut is not None:
        mevcut.password_hash = security.hash_password(parola)
        mevcut.is_active = True
        db.commit()
        print(f"Yonetici parolasi guncellendi: {kullanici}")
        return 0
    security.create_admin(db, kullanici, parola)
    print(f"Yonetici acildi: {kullanici}")
    return 0


def _kullanici_ac(db, ad: str, eposta: str, parola: str) -> int:
    for kontrol, deger in (
        (security.check_display_name, ad),
        (security.check_email, eposta),
        (security.check_password, parola),
    ):
        hata = kontrol(deger)
        if hata:
            print(f"Hata: {hata}", file=sys.stderr)
            return 1

    mevcut = db.scalar(select(User).where(User.email == eposta.strip().lower()))
    if mevcut is not None:
        mevcut.password_hash = security.hash_password(parola)
        mevcut.is_active = True
        db.commit()
        print(f"Kullanici parolasi guncellendi: {mevcut.display_name} <{mevcut.email}>")
        return 0

    user = User(
        display_name=ad.strip(),
        email=eposta.strip().lower(),
        password_hash=security.hash_password(parola),
    )
    db.add(user)
    db.commit()
    print(f"Kullanici acildi: {user.display_name} <{user.email}>")
    return 0


def _listele(db) -> int:
    print("Yoneticiler:")
    for a in db.scalars(select(AdminUser).order_by(AdminUser.username)):
        durum = "aktif" if a.is_active else "askida"
        print(f"  {a.username} ({durum})")
    print("Kullanicilar:")
    for u in db.scalars(select(User).order_by(User.display_name)):
        durum = "aktif" if u.is_active else "askida"
        print(f"  {u.display_name} <{u.email}> ({durum})")
    return 0


def main() -> int:
    komut = argparse.ArgumentParser(prog="hesap.py")
    alt = komut.add_subparsers(dest="komut", required=True)

    a = alt.add_parser("admin")
    a.add_argument("kullanici")
    a.add_argument("parola")

    k = alt.add_parser("kullanici")
    k.add_argument("ad")
    k.add_argument("eposta")
    k.add_argument("parola")

    alt.add_parser("liste")

    args = komut.parse_args()

    sema_guncelle()
    with SessionLocal() as db:
        if args.komut == "admin":
            return _admin_ac(db, args.kullanici, args.parola)
        if args.komut == "kullanici":
            return _kullanici_ac(db, args.ad, args.eposta, args.parola)
        return _listele(db)


if __name__ == "__main__":
    raise SystemExit(main())
