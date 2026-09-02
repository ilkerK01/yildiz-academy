from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app import config
from app.db import get_db
from app.deps import require_user_api
from app.models import User, now
from app.services import security

router = APIRouter(prefix="/api", tags=["kimlik"])

GENERIC_LOGIN_ERROR = "E-posta veya parola hatalı."


class KayitIstek(BaseModel):
    gorunen_ad: str
    eposta: str
    parola: str


class GirisIstek(BaseModel):
    eposta: str
    parola: str


class AdIstek(BaseModel):
    gorunen_ad: str


class ParolaIstek(BaseModel):
    mevcut: str
    yeni: str


def _hata(mesaj: str, kod: int = 400) -> JSONResponse:
    return JSONResponse({"ok": False, "hata": mesaj}, status_code=kod)


def _limit_asildi(request: Request, etiket: str) -> bool:
    ip = security.client_ip(request)
    return not security.rate_limit(f"{etiket}:{ip}", config.LOGIN_ATTEMPTS_PER_MINUTE)


@router.post("/kayit")
def kayit(payload: KayitIstek, request: Request, db: DbSession = Depends(get_db)):
    if _limit_asildi(request, "kayit"):
        return _hata("Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    ad = payload.gorunen_ad.strip()
    eposta = security.normalize_email(payload.eposta)

    for kontrol in (
        security.check_display_name(ad),
        security.check_email(eposta),
        security.check_password(payload.parola),
    ):
        if kontrol:
            return _hata(kontrol)

    if db.scalar(select(User).where(func.lower(User.display_name) == ad.lower())):
        return _hata("Bu görünen ad alınmış.")
    if db.scalar(select(User).where(User.email == eposta)):
        return _hata("Bu e-posta ile bir hesap zaten var.")

    user = User(
        display_name=ad,
        email=eposta,
        password_hash=security.hash_password(payload.parola),
        last_login_at=now(),
    )
    db.add(user)
    db.commit()

    session = security.create_session(db, kind="user", user_id=user.id)
    response = JSONResponse({"ok": True, "gorunen_ad": user.display_name, "next": "/panel"})
    security.set_session_cookie(response, session.token, kind="user")
    return response


@router.post("/giris")
def giris(payload: GirisIstek, request: Request, db: DbSession = Depends(get_db)):
    if _limit_asildi(request, "giris"):
        return _hata("Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    eposta = security.normalize_email(payload.eposta)
    user = db.scalar(select(User).where(User.email == eposta))

    if user is None or not user.is_active:
        security.hash_password(payload.parola)
        return _hata(GENERIC_LOGIN_ERROR, 401)
    if not security.verify_password(user.password_hash, payload.parola):
        return _hata(GENERIC_LOGIN_ERROR, 401)

    user.last_login_at = now()
    db.commit()

    session = security.create_session(db, kind="user", user_id=user.id)
    response = JSONResponse({"ok": True, "gorunen_ad": user.display_name, "next": "/panel"})
    security.set_session_cookie(response, session.token, kind="user")
    return response


@router.post("/cikis")
def cikis(request: Request, db: DbSession = Depends(get_db)):
    security.destroy_session(db, request.cookies.get(config.USER_COOKIE))
    response = JSONResponse({"ok": True})
    security.clear_session_cookie(response, kind="user")
    return response


@router.post("/ayarlar/ad")
def ad_degistir(
    payload: AdIstek,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    yeni = payload.gorunen_ad.strip()
    hata = security.check_display_name(yeni)
    if hata:
        return _hata(hata)

    if yeni.lower() == user.display_name.lower():
        return _hata("Bu zaten mevcut adın.")

    son = user.display_name_changed_at
    if son is not None:
        from datetime import timezone

        if son.tzinfo is None:
            son = son.replace(tzinfo=timezone.utc)
        gecen = now() - son
        kilit = timedelta(days=config.DISPLAY_NAME_COOLDOWN_DAYS)
        if gecen < kilit:
            kalan = (kilit - gecen).days + 1
            return JSONResponse(
                {
                    "ok": False,
                    "hata": f"Görünen adını {kalan} gün sonra değiştirebilirsin.",
                    "kalan_gun": kalan,
                },
                status_code=400,
            )

    if db.scalar(select(User).where(func.lower(User.display_name) == yeni.lower())):
        return _hata("Bu görünen ad alınmış.")

    user.display_name = yeni
    user.display_name_changed_at = now()
    db.commit()
    return {"ok": True, "gorunen_ad": user.display_name}


@router.post("/ayarlar/parola")
def parola_degistir(
    payload: ParolaIstek,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    if not security.verify_password(user.password_hash, payload.mevcut):
        return _hata("Mevcut parola hatalı.")
    hata = security.check_password(payload.yeni)
    if hata:
        return _hata(hata)

    user.password_hash = security.hash_password(payload.yeni)
    db.commit()

    security.destroy_user_sessions(db, user.id)
    session = security.create_session(db, kind="user", user_id=user.id)
    response = JSONResponse({"ok": True})
    security.set_session_cookie(response, session.token, kind="user")
    return response
