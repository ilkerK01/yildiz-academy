from __future__ import annotations

import secrets
from collections.abc import Iterator

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL


class Base(DeclarativeBase):
    pass

_connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=_connect_args, future=True)


if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(engine, "connect")
    def _sqlite_pragmas(dbapi_connection, _record):
        cur = dbapi_connection.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()


_EK_KOLONLAR = (
    ("lab", "order_index", "INTEGER NOT NULL DEFAULT 0"),
    ("lab_progress", "best_points", "INTEGER NOT NULL DEFAULT 0"),
    ("lab_progress", "best_at", "DATETIME"),
    ("user", "public_id", "VARCHAR(16)"),
    ("user", "avatar_file", "VARCHAR(40)"),
    ("lesson", "en_json", "TEXT"),
    ("lab", "en_json", "TEXT"),
)


def sema_guncelle() -> None:
    Base.metadata.create_all(bind=engine)
    mevcut = inspect(engine)
    eklenen = set()
    with engine.begin() as conn:
        for tablo, kolon, tanim in _EK_KOLONLAR:
            kolonlar = {k["name"] for k in mevcut.get_columns(tablo)}
            if kolon not in kolonlar:
                conn.execute(text(f'ALTER TABLE "{tablo}" ADD COLUMN {kolon} {tanim}'))
                eklenen.add(kolon)
        if "best_points" in eklenen:
            conn.execute(
                text(
                    "UPDATE lab_progress SET best_points = earned_points, "
                    "best_at = completed_at "
                    "WHERE status = 'tamamlandi' AND earned_points > 0"
                )
            )
        bos = conn.execute(text('SELECT id FROM "user" WHERE public_id IS NULL')).all()
        for (kimlik,) in bos:
            conn.execute(
                text('UPDATE "user" SET public_id = :p WHERE id = :i'),
                {"p": secrets.token_urlsafe(9), "i": kimlik},
            )
        conn.execute(
            text('CREATE UNIQUE INDEX IF NOT EXISTS ix_user_public_id ON "user" (public_id)')
        )


SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
