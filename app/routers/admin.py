from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session as DbSession

from app import config
from app.db import get_db
from app.deps import is_admin, require_admin
from app.models import (
    ContentTag,
    Lab,
    LabProgress,
    Lesson,
    LessonProgress,
    Session,
    StepProgress,
    User,
)
from app.services import ingest, progress, security
from app.services.ingest import IngestError
from app.templating import page

router = APIRouter(prefix="/academy/admin", tags=["admin"])


def _geri(yol: str = "") -> RedirectResponse:
    return RedirectResponse(f"/academy/admin{yol}", status_code=303)


@router.get("")
def giris_veya_panel(
    request: Request, db: DbSession = Depends(get_db), admin: bool = Depends(is_admin)
):
    if not admin:
        return page(request, "admin/giris.html", hata=None)

    sayilar = {
        "ders": db.scalar(select(func.count(Lesson.id))) or 0,
        "lab": db.scalar(select(func.count(Lab.id))) or 0,
        "kullanici": db.scalar(select(func.count(User.id))) or 0,
        "oturum": db.scalar(select(func.count(Session.id)).where(Session.kind == "user")) or 0,
    }
    return page(request, "admin/panel.html", sayilar=sayilar)


@router.post("/giris")
def giris(
    request: Request,
    kullanici: str = Form(...),
    parola: str = Form(...),
    db: DbSession = Depends(get_db),
):
    ip = security.client_ip(request)
    if not security.rate_limit(f"admin:{ip}", config.LOGIN_ATTEMPTS_PER_MINUTE):
        return page(
            request,
            "admin/giris.html",
            hata="Çok fazla deneme. Bir dakika sonra tekrar dene.",
        )

    if not security.check_admin_credentials(kullanici, parola):
        return page(request, "admin/giris.html", hata="Kullanıcı adı veya parola hatalı.")

    session = security.create_session(db, kind="admin")
    response = _geri()
    security.set_session_cookie(response, session.token, kind="admin")
    return response


@router.post("/cikis")
def cikis(request: Request, db: DbSession = Depends(get_db)):
    security.destroy_session(db, request.cookies.get(config.ADMIN_COOKIE))
    response = _geri()
    security.clear_session_cookie(response, kind="admin")
    return response


@router.get("/icerik")
def icerik(
    request: Request, db: DbSession = Depends(get_db), _: bool = Depends(require_admin)
):
    return page(
        request,
        "admin/icerik.html",
        dersler=list(db.scalars(select(Lesson).order_by(Lesson.order_index, Lesson.title))),
        lablar=list(db.scalars(select(Lab).order_by(Lab.title))),
        onizleme=None,
        hata=None,
        dosya_adi="",
        icerik_metni="",
    )


def _icerik_sayfasi(request, db, *, onizleme=None, hata=None, dosya_adi="", metin=""):
    return page(
        request,
        "admin/icerik.html",
        dersler=list(db.scalars(select(Lesson).order_by(Lesson.order_index, Lesson.title))),
        lablar=list(db.scalars(select(Lab).order_by(Lab.title))),
        onizleme=onizleme,
        hata=hata,
        dosya_adi=dosya_adi,
        icerik_metni=metin,
    )


@router.post("/icerik/yukle")
async def icerik_yukle(
    request: Request,
    dosya: UploadFile = File(...),
    db: DbSession = Depends(get_db),
    _: bool = Depends(require_admin),
):
    ad = (dosya.filename or "").strip()
    if not ad.lower().endswith((".md", ".yaml", ".yml")):
        return _icerik_sayfasi(
            request, db, hata="Yalnızca .md ve .yaml dosyaları kabul edilir."
        )

    ham = await dosya.read()
    if len(ham) > config.UPLOAD_MAX_BYTES:
        return _icerik_sayfasi(request, db, hata="Dosya 1 MB sınırını aşıyor.")

    try:
        metin = ham.decode("utf-8")
    except UnicodeDecodeError:
        return _icerik_sayfasi(request, db, hata="Dosya UTF-8 değil.")

    try:
        _, onizleme = ingest.ingest_text(db, ad, metin, commit=False)
    except IngestError as exc:
        return _icerik_sayfasi(request, db, hata=str(exc), dosya_adi=ad, metin=metin)

    return _icerik_sayfasi(request, db, onizleme=onizleme, dosya_adi=ad, metin=metin)


@router.post("/icerik/onayla")
def icerik_onayla(
    request: Request,
    dosya_adi: str = Form(...),
    icerik_metni: str = Form(...),
    db: DbSession = Depends(get_db),
    _: bool = Depends(require_admin),
):
    try:
        ingest.ingest_text(db, dosya_adi, icerik_metni, commit=True)
    except IngestError as exc:
        return _icerik_sayfasi(
            request, db, hata=str(exc), dosya_adi=dosya_adi, metin=icerik_metni
        )
    return _geri("/icerik")


@router.post("/icerik/{tip}/{slug}/yayin")
def yayin_cevir(
    tip: str,
    slug: str,
    db: DbSession = Depends(get_db),
    _: bool = Depends(require_admin),
):
    model = Lesson if tip == "ders" else Lab
    row = db.scalar(select(model).where(model.slug == slug))
    if row is None:
        raise HTTPException(404, "İçerik bulunamadı.")
    row.published = not row.published
    db.commit()
    return _geri("/icerik")


@router.post("/icerik/{tip}/{slug}/sil")
def icerik_sil(
    tip: str,
    slug: str,
    db: DbSession = Depends(get_db),
    _: bool = Depends(require_admin),
):
    model = Lesson if tip == "ders" else Lab
    row = db.scalar(select(model).where(model.slug == slug))
    if row is None:
        raise HTTPException(404, "İçerik bulunamadı.")
    db.execute(
        delete(ContentTag).where(
            ContentTag.content_type == ("lesson" if tip == "ders" else "lab"),
            ContentTag.content_id == row.id,
        )
    )
    db.delete(row)
    db.commit()
    return _geri("/icerik")


@router.get("/kullanicilar")
def kullanicilar(
    request: Request, db: DbSession = Depends(get_db), _: bool = Depends(require_admin)
):
    users = list(db.scalars(select(User).order_by(User.created_at.desc())))
    satirlar = []
    for u in users:
        stats = progress.user_stats(db, u.id)
        satirlar.append({"user": u, "stats": stats})
    return page(request, "admin/kullanicilar.html", satirlar=satirlar, yeni_parola=None)


@router.post("/kullanicilar/{user_id}/parola")
def parola_sifirla(
    request: Request,
    user_id: int,
    db: DbSession = Depends(get_db),
    _: bool = Depends(require_admin),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "Kullanıcı bulunamadı.")

    yeni = secrets.token_urlsafe(9)
    user.password_hash = security.hash_password(yeni)
    db.commit()
    security.destroy_user_sessions(db, user.id)

    users = list(db.scalars(select(User).order_by(User.created_at.desc())))
    satirlar = [{"user": u, "stats": progress.user_stats(db, u.id)} for u in users]
    return page(
        request,
        "admin/kullanicilar.html",
        satirlar=satirlar,
        yeni_parola={"ad": user.display_name, "parola": yeni},
    )


@router.post("/kullanicilar/{user_id}/askiya-al")
def askiya_al(
    user_id: int, db: DbSession = Depends(get_db), _: bool = Depends(require_admin)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "Kullanıcı bulunamadı.")
    user.is_active = not user.is_active
    db.commit()
    if not user.is_active:
        security.destroy_user_sessions(db, user.id)
    return _geri("/kullanicilar")


@router.post("/kullanicilar/{user_id}/ilerleme-sifirla")
def ilerleme_sifirla(
    user_id: int, db: DbSession = Depends(get_db), _: bool = Depends(require_admin)
):
    if db.get(User, user_id) is None:
        raise HTTPException(404, "Kullanıcı bulunamadı.")
    progress.reset_all_progress(db, user_id)
    return _geri("/kullanicilar")


@router.post("/kullanicilar/{user_id}/sil")
def kullanici_sil(
    user_id: int, db: DbSession = Depends(get_db), _: bool = Depends(require_admin)
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(404, "Kullanıcı bulunamadı.")
    db.execute(delete(StepProgress).where(StepProgress.user_id == user_id))
    db.execute(delete(LabProgress).where(LabProgress.user_id == user_id))
    db.execute(delete(LessonProgress).where(LessonProgress.user_id == user_id))
    db.execute(delete(Session).where(Session.user_id == user_id))
    db.delete(user)
    db.commit()
    return _geri("/kullanicilar")
