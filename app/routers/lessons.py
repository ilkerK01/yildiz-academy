from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.db import get_db
from app.deps import require_user_api
from app.models import Lesson, User
from app.services import progress

router = APIRouter(prefix="/api/ders", tags=["ders"])


@router.post("/{slug}/okudum")
def okudum(
    slug: str,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    lesson = db.scalar(select(Lesson).where(Lesson.slug == slug, Lesson.published.is_(True)))
    if lesson is None:
        raise HTTPException(404, "Ders bulunamadı.")

    yeni = progress.mark_lesson_read(db, user.id, lesson)
    stats = progress.user_stats(db, user.id)
    return {"ok": True, "yeni": yeni, "toplam_okunan": stats["okunan_ders"]}
