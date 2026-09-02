from __future__ import annotations

import sys

from app.config import CONTENT_DIR
from app.db import Base, SessionLocal, engine
from app.services.ingest import IngestError, ingest_directory


def main() -> int:
    Base.metadata.create_all(bind=engine)

    if not CONTENT_DIR.exists():
        print(f"content/ klasörü yok: {CONTENT_DIR}")
        return 1

    db = SessionLocal()
    try:
        satirlar = ingest_directory(db, CONTENT_DIR)
    except IngestError as exc:
        print(f"HATA  {exc}")
        return 1
    finally:
        db.close()

    if not satirlar:
        print("İçerik bulunamadı. content/dersler/*.md ve content/lablar/*.yaml bekleniyor.")
        return 0

    for satir in satirlar:
        print(satir)
    print(f"\n{len(satirlar)} içerik basıldı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
