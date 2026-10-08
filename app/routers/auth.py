from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, File, Request, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app import config, i18n
from app.db import get_db
from app.deps import require_user_api
from app.models import User, now
from app.services import avatar, eposta, security

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


class UnuttumIstek(BaseModel):
    eposta: str


class SifirlaIstek(BaseModel):
    token: str
    yeni: str


RESET_SENT = "Bu adrese kayıtlı bir hesap varsa sıfırlama bağlantısı gönderildi. Gelen kutunu ve spam klasörünü kontrol et."


def _hata(request: Request, mesaj: str, kod: int = 400) -> JSONResponse:
    return JSONResponse(
        {"ok": False, "hata": i18n.cevir(i18n.dil(request), mesaj)}, status_code=kod
    )


def _limit_asildi(request: Request, etiket: str) -> bool:
    ip = security.client_ip(request)
    return not security.rate_limit(f"{etiket}:{ip}", config.LOGIN_ATTEMPTS_PER_MINUTE)


@router.post("/kayit")
def kayit(payload: KayitIstek, request: Request, db: DbSession = Depends(get_db)):
    if _limit_asildi(request, "kayit"):
        return _hata(request, "Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    ad = payload.gorunen_ad.strip()
    eposta = security.normalize_email(payload.eposta)

    for kontrol in (
        security.check_display_name(ad),
        security.check_email(eposta),
        security.check_password(payload.parola),
    ):
        if kontrol:
            return _hata(request, kontrol)

    if db.scalar(select(User).where(func.lower(User.display_name) == ad.lower())):
        return _hata(request, "Bu görünen ad alınmış.")
    if db.scalar(select(User).where(User.email == eposta)):
        return _hata(request, "Kayıt tamamlanamadı. Hesabın varsa giriş yap ya da şifreni sıfırla.")

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
        return _hata(request, "Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    eposta = security.normalize_email(payload.eposta)
    user = db.scalar(select(User).where(User.email == eposta))

    if user is None or not user.is_active:
        security.hash_password(payload.parola)
        return _hata(request, GENERIC_LOGIN_ERROR, 401)
    if not security.verify_password(user.password_hash, payload.parola):
        return _hata(request, GENERIC_LOGIN_ERROR, 401)

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
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    yeni = payload.gorunen_ad.strip()
    hata = security.check_display_name(yeni)
    if hata:
        return _hata(request, hata)

    if yeni.lower() == user.display_name.lower():
        return _hata(request, "Bu zaten mevcut adın.")

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
                    "hata": i18n.cevir(
                        i18n.dil(request),
                        "Görünen adını {kalan} gün sonra değiştirebilirsin.",
                        kalan=kalan,
                    ),
                    "kalan_gun": kalan,
                },
                status_code=400,
            )

    if db.scalar(select(User).where(func.lower(User.display_name) == yeni.lower())):
        return _hata(request, "Bu görünen ad alınmış.")

    user.display_name = yeni
    user.display_name_changed_at = now()
    db.commit()
    return {"ok": True, "gorunen_ad": user.display_name}


@router.post("/ayarlar/avatar")
async def avatar_yukle(
    request: Request,
    dosya: UploadFile = File(...),
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    if _limit_asildi(request, "avatar"):
        return _hata(request, "Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)
    try:
        await avatar.kaydet(db, user, dosya)
    except avatar.AvatarHatasi as hata:
        return JSONResponse(
            {"ok": False, "hata": i18n.cevir(i18n.dil(request), hata.mesaj, **hata.degerler)},
            status_code=400,
        )
    return {"ok": True, "url": avatar.url(user)}


@router.post("/ayarlar/avatar/sil")
def avatar_kaldir(
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    avatar.sil(db, user)
    return {"ok": True}


@router.post("/ayarlar/parola")
def parola_degistir(
    payload: ParolaIstek,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    if not security.verify_password(user.password_hash, payload.mevcut):
        return _hata(request, "Mevcut parola hatalı.")
    hata = security.check_password(payload.yeni)
    if hata:
        return _hata(request, hata)

    user.password_hash = security.hash_password(payload.yeni)
    db.commit()

    security.destroy_user_sessions(db, user.id)
    session = security.create_session(db, kind="user", user_id=user.id)
    response = JSONResponse({"ok": True})
    security.set_session_cookie(response, session.token, kind="user")
    return response


def _sifirlama_postasi(kod: str, ad: str, baglanti: str) -> tuple[str, str]:
    dakika = config.RESET_TOKEN_MINUTES
    if kod == "en":
        return (
            "Yıldız Academy password reset",
            f"Hello {ad},\n\n"
            "A password reset was requested for your Yıldız Academy account. "
            "Use the link below to set a new password:\n\n"
            f"{baglanti}\n\n"
            f"The link is valid for {dakika} minutes and can be used once. "
            "If you did not request this, ignore this email; your password stays the same.\n",
        )
    return (
        "Yıldız Academy parola sıfırlama",
        f"Merhaba {ad},\n\n"
        "Yıldız Academy hesabın için parola sıfırlama istendi. "
        "Yeni parolanı belirlemek için aşağıdaki bağlantıyı kullan:\n\n"
        f"{baglanti}\n\n"
        f"Bağlantı {dakika} dakika geçerli ve tek kullanımlık. "
        "Bu isteği sen yapmadıysan e-postayı yok say, parolan değişmez.\n",
    )


@router.post("/sifremi-unuttum")
def sifremi_unuttum(
    payload: UnuttumIstek,
    request: Request,
    arka_plan: BackgroundTasks,
    db: DbSession = Depends(get_db),
):
    if _limit_asildi(request, "unuttum"):
        return _hata(request, "Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    adres = security.normalize_email(payload.eposta)
    if security.check_email(adres):
        return _hata(request, "E-posta adresi geçerli görünmüyor.")

    user = db.scalar(select(User).where(User.email == adres))
    if user is not None and user.is_active:
        token = security.create_reset_token(db, user.id)
        baglanti = f"{config.SITE_URL}/sifre-sifirla?token={token}"
        konu, govde = _sifirlama_postasi(i18n.dil(request), user.display_name, baglanti)
        arka_plan.add_task(eposta.gonder, user.email, konu, govde)

    return {"ok": True, "mesaj": i18n.cevir(i18n.dil(request), RESET_SENT)}


@router.post("/sifre-sifirla")
def sifre_sifirla(payload: SifirlaIstek, request: Request, db: DbSession = Depends(get_db)):
    if _limit_asildi(request, "sifirla"):
        return _hata(request, "Çok fazla deneme. Bir dakika sonra tekrar dene.", 429)

    kayit = security.resolve_reset_token(db, payload.token)
    user = db.get(User, kayit.user_id) if kayit is not None else None
    if kayit is None or user is None or not user.is_active:
        return _hata(request, "Bağlantı geçersiz ya da süresi dolmuş. Yeni bir bağlantı iste.")

    hata = security.check_password(payload.yeni)
    if hata:
        return _hata(request, hata)

    user.password_hash = security.hash_password(payload.yeni)
    kayit.used_at = now()
    db.commit()
    security.destroy_user_sessions(db, user.id)
    return {"ok": True}
