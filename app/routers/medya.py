from __future__ import annotations

import re

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session as DbSession

from app.db import get_db
from app.deps import current_user, is_admin
from app.models import LessonVideo, User
from app.services import avatar, docx_ders, video

router = APIRouter(prefix="/medya", tags=["medya"])

_GORSEL_ADI = re.compile(r"^[0-9a-f]{20}\.(png|jpg|gif|webp)$")


@router.get("/video/{video_id}/{dosya}")
def video_akisi(
    video_id: int,
    dosya: str,
    db: DbSession = Depends(get_db),
    user: User | None = Depends(current_user),
    admin: bool = Depends(is_admin),
):
    # Videolar yalnızca giriş yapmış kullanıcılara (ve yöneticiye) açık.
    if user is None and not admin:
        raise HTTPException(401, "Giriş gerekli.")
    kayit = db.get(LessonVideo, video_id)
    if kayit is None or kayit.file_name != dosya:
        raise HTTPException(404, "Video bulunamadı.")
    yol = video.dosya_yolu(kayit)
    if not yol.is_file():
        raise HTTPException(404, "Video bulunamadı.")
    # FileResponse Range isteklerini destekler (206 Partial Content):
    # tarayıcı videoyu parça parça indirir, ileri sarma anında çalışır.
    return FileResponse(
        yol,
        media_type=kayit.mime,
        headers={"Cache-Control": "private, max-age=604800", "Accept-Ranges": "bytes"},
    )


@router.get("/avatar/{ad}")
def avatar_gorseli(ad: str, user: User | None = Depends(current_user), admin: bool = Depends(is_admin)):
    # Profiller yalnızca giriş yapmış kullanıcılara açık; fotoğraflar da öyle.
    if user is None and not admin:
        raise HTTPException(401, "Giriş gerekli.")
    if not avatar.DOSYA_ADI.match(ad):
        raise HTTPException(404, "Bulunamadı.")
    yol = avatar.dosya_yolu(ad)
    if not yol.is_file():
        raise HTTPException(404, "Bulunamadı.")
    # Ad her yüklemede değiştiği için dosya hiç değişmez; uzun süre önbellekte kalabilir.
    return FileResponse(
        yol, media_type="image/webp", headers={"Cache-Control": "private, max-age=31536000, immutable"}
    )


@router.get("/gorsel/{ad}")
def gorsel(ad: str):
    if not _GORSEL_ADI.match(ad):
        raise HTTPException(404, "Bulunamadı.")
    yol = docx_ders.gorsel_klasoru() / ad
    if not yol.is_file():
        raise HTTPException(404, "Bulunamadı.")
    return FileResponse(yol, headers={"Cache-Control": "public, max-age=31536000, immutable"})
