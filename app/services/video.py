from __future__ import annotations

import asyncio
import json
import secrets
import shutil
import struct
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app import config
from app.models import Lesson, LessonVideo

# Tarayıcıların hepsinde sorunsuz oynayan biçimler.
UZANTILAR = {".mp4": "video/mp4", ".m4v": "video/mp4", ".webm": "video/webm"}
UYUMLU_VIDEO = {"h264", "vp8", "vp9", "av1"}
UYUMLU_SES = {"aac", "mp3", "opus", "vorbis"}
PARCA = 1024 * 1024


class VideoHatasi(Exception):
    pass


@dataclass
class Sonuc:
    video: LessonVideo
    uyarilar: list[str] = field(default_factory=list)


def klasor() -> Path:
    yol = config.MEDIA_DIR / "videolar"
    yol.mkdir(parents=True, exist_ok=True)
    return yol


def dosya_yolu(video: LessonVideo) -> Path:
    return klasor() / video.file_name


def ders_videosu(db: DbSession, lesson: Lesson, kod: str) -> LessonVideo | None:
    """Seçilen dildeki video, yoksa Türkçe video."""
    videolar = {
        v.lang: v
        for v in db.scalars(select(LessonVideo).where(LessonVideo.lesson_id == lesson.id))
    }
    video = videolar.get(kod) or videolar.get("tr")
    if video is not None and not dosya_yolu(video).is_file():
        return None
    return video


def ders_videolari(db: DbSession) -> dict[int, list[LessonVideo]]:
    sonuc: dict[int, list[LessonVideo]] = {}
    for v in db.scalars(select(LessonVideo).order_by(LessonVideo.lang.desc())):
        sonuc.setdefault(v.lesson_id, []).append(v)
    return sonuc


def _bas_kontrol(yol: Path, uzanti: str) -> None:
    with yol.open("rb") as f:
        bas = f.read(16)
    if uzanti == ".webm":
        if not bas.startswith(b"\x1a\x45\xdf\xa3"):
            raise VideoHatasi("Dosya geçerli bir WebM videosu değil.")
    elif bas[4:8] != b"ftyp":
        raise VideoHatasi("Dosya geçerli bir MP4 videosu değil.")


def _moov_basta_mi(yol: Path) -> bool | None:
    """MP4'te oynatma bilgisi (moov) verinin (mdat) önündeyse video
    tamamı inmeden oynamaya başlar. None: belirlenemedi."""
    try:
        with yol.open("rb") as f:
            boyut_toplam = yol.stat().st_size
            konum = 0
            while konum < boyut_toplam:
                f.seek(konum)
                baslik = f.read(16)
                if len(baslik) < 8:
                    return None
                boyut, tur = struct.unpack(">I4s", baslik[:8])
                if boyut == 1:
                    boyut = struct.unpack(">Q", baslik[8:16])[0]
                elif boyut == 0:
                    boyut = boyut_toplam - konum
                if tur == b"moov":
                    return True
                if tur == b"mdat":
                    return False
                if boyut < 8:
                    return None
                konum += boyut
    except OSError:
        return None
    return None


def _ffmpeg_var() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def _kodekler(yol: Path) -> tuple[str | None, str | None]:
    try:
        cikti = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name",
             "-of", "json", str(yol)],
            capture_output=True, text=True, timeout=60, check=True,
        ).stdout
        akislar = json.loads(cikti).get("streams", [])
    except (OSError, subprocess.SubprocessError, ValueError):
        return None, None
    video = next((s.get("codec_name") for s in akislar if s.get("codec_type") == "video"), None)
    ses = next((s.get("codec_name") for s in akislar if s.get("codec_type") == "audio"), None)
    return video, ses


def _faststart(yol: Path) -> bool:
    gecici = yol.with_name(yol.stem + ".fs" + yol.suffix)
    try:
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(yol), "-map", "0", "-c", "copy",
             "-movflags", "+faststart", str(gecici)],
            capture_output=True, timeout=1800, check=True,
        )
        gecici.replace(yol)
        return True
    except (OSError, subprocess.SubprocessError):
        gecici.unlink(missing_ok=True)
        return False


def _hazirla(yol: Path, uzanti: str) -> list[str]:
    """Videoyu kontrol eder, gerekirse hızlı başlatma için düzenler.
    Bloklayan iş; thread içinde çalıştırılır."""
    _bas_kontrol(yol, uzanti)
    uyarilar: list[str] = []
    ffmpeg = _ffmpeg_var()

    if ffmpeg:
        vkod, skod = _kodekler(yol)
        if vkod is None:
            raise VideoHatasi("Dosyada görüntü akışı bulunamadı.")
        if vkod not in UYUMLU_VIDEO:
            uyarilar.append(
                f"Video kodeki {vkod}. Bazı tarayıcılar (özellikle Chrome ve Firefox) "
                "bunu oynatamayabilir. H.264 ile dışa aktarman önerilir."
            )
        if skod is not None and skod not in UYUMLU_SES:
            uyarilar.append(f"Ses kodeki {skod}. AAC ile dışa aktarman önerilir.")

    if uzanti != ".webm" and _moov_basta_mi(yol) is False:
        if ffmpeg and _faststart(yol):
            uyarilar.append("Video hızlı başlatma için düzenlendi (faststart).")
        else:
            uyarilar.append(
                "Videonun oynatma bilgisi dosyanın sonunda. Oynar ama başlaması "
                "gecikebilir. Dışa aktarırken 'web için optimize et / fast start' "
                "seçeneğini aç ya da: ffmpeg -i girdi.mp4 -c copy -movflags +faststart cikti.mp4"
            )
    return uyarilar


async def kaydet(db: DbSession, lesson: Lesson, lang: str, dosya: UploadFile) -> Sonuc:
    if lang not in {"tr", "en"}:
        raise VideoHatasi("Dil tr ya da en olmalı.")
    ad = (dosya.filename or "").strip()
    uzanti = Path(ad).suffix.lower()
    if uzanti not in UZANTILAR:
        raise VideoHatasi(
            "Yalnızca .mp4 ve .webm kabul edilir. .mov, .mkv ya da .avi dosyalarını "
            "önce MP4 (H.264 + AAC) olarak dışa aktar."
        )

    sinir = config.VIDEO_MAX_MB * 1024 * 1024
    hedef_ad = f"{lesson.slug}-{lang}-{secrets.token_hex(4)}{uzanti}"
    gecici = klasor() / f".yukleniyor-{hedef_ad}"
    boyut = 0
    try:
        with gecici.open("wb") as cikis:
            while parca := await dosya.read(PARCA):
                boyut += len(parca)
                if boyut > sinir:
                    raise VideoHatasi(f"Video {config.VIDEO_MAX_MB} MB sınırını aşıyor.")
                cikis.write(parca)
        if boyut == 0:
            raise VideoHatasi("Dosya boş.")
        uyarilar = await asyncio.to_thread(_hazirla, gecici, uzanti)
        hedef = klasor() / hedef_ad
        gecici.replace(hedef)
    except BaseException:
        gecici.unlink(missing_ok=True)
        raise

    eski = db.scalar(
        select(LessonVideo).where(LessonVideo.lesson_id == lesson.id, LessonVideo.lang == lang)
    )
    if eski is not None:
        dosya_yolu(eski).unlink(missing_ok=True)
        video = eski
    else:
        video = LessonVideo(lesson_id=lesson.id, lang=lang)
        db.add(video)
    video.file_name = hedef_ad
    video.original_name = ad[:255]
    video.size_bytes = hedef.stat().st_size
    video.mime = UZANTILAR[uzanti]
    db.commit()
    return Sonuc(video=video, uyarilar=uyarilar)


def sil(db: DbSession, video: LessonVideo, *, commit: bool = True) -> None:
    dosya_yolu(video).unlink(missing_ok=True)
    db.delete(video)
    if commit:
        db.commit()
