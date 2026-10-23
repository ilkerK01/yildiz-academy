"""Yildiz Academy - bundled Turkish CTI video installer.

Run after `python seed.py`. Idempotent: keeps already configured videos whose
media file exists; restores missing bundled videos without deleting user uploads.
"""
from __future__ import annotations

import shutil
from pathlib import Path
from sqlalchemy import select

from app.config import CONTENT_DIR, MEDIA_DIR
from app.db import SessionLocal, sema_guncelle
from app.models import Lesson, LessonVideo

# Lesson slug -> exact filename committed in content/videolar
VIDEOS = {
    'aci-piramidi': 'aci-piramidi-tr-bc148c3b.mp4',
    'cti-nedir': 'cti-nedir-tr-6dde23da.mp4',
    'cti-yasam-dongusu': 'cti-yasam-dongusu-tr-189f4549.mp4',
    'ioc-zenginlestirme': 'ioc-zenginlestirme-tr-0000f415.mp4',
    'mitre-attack-cti': 'mitre-attack-cti-tr-1a622017.mp4',
    'osint-arastirma-kaynak-dogrulama': 'osint-arastirma-kaynak-dogrulama-tr-2aa9ec59.mp4',
    'phishing-eposta-analizi': 'phishing-eposta-analizi-tr-4bf6bb91.mp4',
    'ransomware-cti': 'ransomware-cti-tr-634a24ca.mp4',
    'stix-taxii-misp': 'stix-taxii-misp-tr-d43c7592.mp4',
    'threat-actor-profilleme-attribution': 'threat-actor-profilleme-attribution-tr-ffe609e6.mp4',
    'malware-analysis': 'CTI_için_Zararlı_Yazılım_Analizi_(Malware_Analysis).mp4',
    'cti-raporlama': 'CTI_Raporlama_ve_Intelligence_Products.mp4',
    'cyber-kill-chain': 'Cyber_Kill_Chain.mp4',
    'cti-automation': 'Cyber_Threat_Intelligence_Automation.mp4',
    'dark-web-intelligence': 'Dark_Web_Intelligence_(DARKINT).mp4',
    'structured-analytic-techniques': 'Structured_Analytic_Techniques_(SATs)_ile_CTI_Analizi.mp4',
    'diamond-model': 'Sızma_Analizi_Elmas_Modeli.mp4',
    'threat-hunting': 'Threat_Hunting_Fundamentals.mp4',
    'vulnerability-intelligence': 'Vulnerability_Intelligence_ve_CVE_Analizi.mp4',
}


def sync_videos() -> None:
    source_dir = CONTENT_DIR / 'videolar'
    dest_dir = MEDIA_DIR / 'videolar'
    # Check all sources (including actual MP4 data, not LFS pointer files) first.
    missing = [name for name in VIDEOS.values() if not (source_dir / name).is_file()]
    if missing:
        raise RuntimeError('Eksik kaynak video dosyalari: ' + ', '.join(missing))
    for name in VIDEOS.values():
        path = source_dir / name
        with path.open('rb') as f:
            header = f.read(12)
        if header[4:8] != b'ftyp':
            raise RuntimeError(f'Gecerli MP4 degil (LFS dosyasi indirilmemis olabilir): {name}')
    sema_guncelle()
    dest_dir.mkdir(parents=True, exist_ok=True)
    created = skipped = repaired = 0
    with SessionLocal() as db:
        for slug, name in VIDEOS.items():
            lesson = db.scalar(select(Lesson).where(Lesson.slug == slug))
            if lesson is None:
                raise RuntimeError(f'Ders bulunamadi: {slug} (once python seed.py calistirin)')
            existing = db.scalar(select(LessonVideo).where(
                LessonVideo.lesson_id == lesson.id, LessonVideo.lang == 'tr'
            ))
            if existing and (dest_dir / existing.file_name).is_file():
                skipped += 1
                continue
            dest = dest_dir / name
            if not dest.exists() or dest.stat().st_size != (source_dir / name).stat().st_size:
                shutil.copy2(source_dir / name, dest)
            if existing is None:
                existing = LessonVideo(lesson_id=lesson.id, lang='tr')
                db.add(existing)
                created += 1
            else:
                repaired += 1
            existing.file_name = name
            existing.original_name = name[:255]
            existing.size_bytes = dest.stat().st_size
            existing.mime = 'video/mp4'
        db.commit()
    print(f'Tamam: {created} video baglandi, {repaired} kayit onarildi, {skipped} mevcut kayit korundu.')


if __name__ == '__main__':
    sync_videos()
