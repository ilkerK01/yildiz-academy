from __future__ import annotations

import io
import re
import secrets
from pathlib import Path

from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
from PIL import Image, ImageOps, UnidentifiedImageError
from sqlalchemy.orm import Session as DbSession

from app import config
from app.models import User

# Kaynak olarak kabul edilen biçimler; Pillow dosyanın içeriğine bakarak belirler,
# uzantıya ya da tarayıcının bildirdiği türe güvenilmez.
BICIMLER = {"JPEG", "PNG", "WEBP", "GIF"}
KABUL = "image/png,image/jpeg,image/webp,image/gif"
DOSYA_ADI = re.compile(r"^[0-9a-f]{24}\.webp$")
PARCA = 64 * 1024


class AvatarHatasi(Exception):
    def __init__(self, mesaj: str, **degerler) -> None:
        super().__init__(mesaj)
        self.mesaj = mesaj
        self.degerler = degerler


def klasor() -> Path:
    config.AVATAR_DIR.mkdir(parents=True, exist_ok=True)
    return config.AVATAR_DIR


def dosya_yolu(ad: str) -> Path:
    return klasor() / ad


def url(user) -> str | None:
    ad = getattr(user, "avatar_file", None)
    return f"/medya/avatar/{ad}" if ad else None


async def _oku(dosya: UploadFile) -> bytes:
    sinir = config.AVATAR_MAX_MB * 1024 * 1024
    tampon = bytearray()
    while parca := await dosya.read(PARCA):
        tampon.extend(parca)
        if len(tampon) > sinir:
            raise AvatarHatasi("Dosya en fazla {mb} MB olabilir.", mb=config.AVATAR_MAX_MB)
    if not tampon:
        raise AvatarHatasi("Bir görsel seç.")
    return bytes(tampon)


def _isle(ham: bytes) -> bytes:
    boyut = config.AVATAR_BOYUT
    try:
        with Image.open(io.BytesIO(ham)) as gorsel:
            if gorsel.format not in BICIMLER:
                raise AvatarHatasi("Yalnızca PNG, JPG, WebP ya da GIF yükleyebilirsin.")
            genislik, yukseklik = gorsel.size
            if max(genislik, yukseklik) > config.AVATAR_MAX_PX:
                raise AvatarHatasi("Görsel en fazla {px} piksel olabilir.", px=config.AVATAR_MAX_PX)
            if min(genislik, yukseklik) < config.AVATAR_MIN_PX:
                raise AvatarHatasi("Görsel en az {px} piksel olmalı.", px=config.AVATAR_MIN_PX)
            # Hareketli GIF'te ilk kare; telefon fotoğraflarında EXIF yönü uygulanır.
            gorsel.seek(0)
            gorsel = ImageOps.exif_transpose(gorsel)
            saydam = gorsel.mode in ("RGBA", "LA", "PA") or "transparency" in gorsel.info
            gorsel = gorsel.convert("RGBA" if saydam else "RGB")
            kare = ImageOps.fit(gorsel, (boyut, boyut), Image.Resampling.LANCZOS)
            cikti = io.BytesIO()
            kare.save(cikti, "WEBP", quality=config.AVATAR_KALITE, method=6)
            return cikti.getvalue()
    except AvatarHatasi:
        raise
    except (UnidentifiedImageError, Image.DecompressionBombError, OSError, ValueError):
        raise AvatarHatasi("Görsel okunamadı.") from None


def _eskiyi_sil(ad: str | None) -> None:
    if ad and DOSYA_ADI.match(ad):
        dosya_yolu(ad).unlink(missing_ok=True)


async def kaydet(db: DbSession, user: User, dosya: UploadFile) -> str:
    ham = await _oku(dosya)
    veri = await run_in_threadpool(_isle, ham)
    # Her yüklemede yeni ad: tarayıcı önbelleği eski fotoğrafı göstermez.
    ad = f"{secrets.token_hex(12)}.webp"
    dosya_yolu(ad).write_bytes(veri)
    eski = user.avatar_file
    user.avatar_file = ad
    db.commit()
    _eskiyi_sil(eski)
    return ad


def sil(db: DbSession, user: User) -> None:
    eski = user.avatar_file
    user.avatar_file = None
    db.commit()
    _eskiyi_sil(eski)
