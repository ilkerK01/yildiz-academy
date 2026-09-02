from __future__ import annotations

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session as DbSession

from app.models import (
    Lab,
    LabProgress,
    LabStep,
    Lesson,
    LessonProgress,
    StepProgress,
    now,
)
from app.services import scoring


def mark_lesson_read(db: DbSession, user_id: int, lesson: Lesson) -> bool:
    existing = db.scalar(
        select(LessonProgress).where(
            LessonProgress.user_id == user_id, LessonProgress.lesson_id == lesson.id
        )
    )
    if existing:
        return False
    db.add(LessonProgress(user_id=user_id, lesson_id=lesson.id))
    db.commit()
    return True


def read_lesson_ids(db: DbSession, user_id: int) -> set[int]:
    rows = db.scalars(
        select(LessonProgress.lesson_id).where(LessonProgress.user_id == user_id)
    )
    return set(rows)


def get_lab_progress(db: DbSession, user_id: int, lab: Lab) -> LabProgress:
    row = db.scalar(
        select(LabProgress).where(
            LabProgress.user_id == user_id, LabProgress.lab_id == lab.id
        )
    )
    if row is None:
        row = LabProgress(user_id=user_id, lab_id=lab.id, status="basladi")
        db.add(row)
        db.commit()
    return row


def get_step_rows(db: DbSession, user_id: int, lab: Lab) -> dict[int, StepProgress]:
    step_ids = [s.id for s in lab.steps]
    if not step_ids:
        return {}
    rows = db.scalars(
        select(StepProgress).where(
            StepProgress.user_id == user_id, StepProgress.step_id.in_(step_ids)
        )
    ).all()
    return {row.step_id: row for row in rows}


def get_or_create_step_row(db: DbSession, user_id: int, step: LabStep) -> StepProgress:
    row = db.scalar(
        select(StepProgress).where(
            StepProgress.user_id == user_id, StepProgress.step_id == step.id
        )
    )
    if row is None:
        row = StepProgress(user_id=user_id, step_id=step.id)
        db.add(row)
        db.commit()
    return row


def current_step_index(lab: Lab, step_rows: dict[int, StepProgress]) -> int:
    for step in lab.steps:
        row = step_rows.get(step.id)
        if row is None or not row.solved:
            return step.step_index
    return len(lab.steps) + 1


def recalculate_lab(db: DbSession, user_id: int, lab: Lab) -> LabProgress:
    progress = get_lab_progress(db, user_id, lab)
    step_rows = get_step_rows(db, user_id, lab)
    rows = list(step_rows.values())

    solved_count = sum(1 for r in rows if r.solved)

    progress.earned_points = scoring.lab_award(progress, rows)

    if lab.steps and solved_count == len(lab.steps):
        if progress.status != "tamamlandi":
            progress.status = "tamamlandi"
            progress.completed_at = now()
        progress.solution_seen = True
    elif progress.status == "tamamlandi":
        progress.status = "basladi"
        progress.completed_at = None

    db.commit()
    return progress


def give_up(db: DbSession, user_id: int, lab: Lab) -> LabProgress:
    progress = get_lab_progress(db, user_id, lab)
    progress.status = "pes_etti"
    progress.solution_seen = True
    progress.earned_points = 0
    db.commit()
    return progress


def reset_lab(db: DbSession, user_id: int, lab: Lab) -> LabProgress:
    step_ids = [s.id for s in lab.steps]
    if step_ids:
        db.execute(
            delete(StepProgress).where(
                StepProgress.user_id == user_id, StepProgress.step_id.in_(step_ids)
            )
        )
    progress = get_lab_progress(db, user_id, lab)
    progress.status = "basladi"
    progress.earned_points = 0
    progress.completed_at = None
    progress.started_at = now()
    db.commit()
    return progress


def reset_all_progress(db: DbSession, user_id: int) -> None:
    db.execute(delete(StepProgress).where(StepProgress.user_id == user_id))
    db.execute(delete(LabProgress).where(LabProgress.user_id == user_id))
    db.execute(delete(LessonProgress).where(LessonProgress.user_id == user_id))
    db.commit()


def user_stats(db: DbSession, user_id: int) -> dict:
    total_points = db.scalar(
        select(func.coalesce(func.sum(LabProgress.earned_points), 0)).where(
            LabProgress.user_id == user_id
        )
    )
    solved_labs = db.scalar(
        select(func.count(LabProgress.id)).where(
            LabProgress.user_id == user_id, LabProgress.status == "tamamlandi"
        )
    )
    read_lessons = db.scalar(
        select(func.count(LessonProgress.id)).where(LessonProgress.user_id == user_id)
    )
    hints_used = db.scalar(
        select(func.coalesce(func.sum(StepProgress.hints_used), 0)).where(
            StepProgress.user_id == user_id
        )
    )
    return {
        "puan": int(total_points or 0),
        "cozulen_lab": int(solved_labs or 0),
        "okunan_ders": int(read_lessons or 0),
        "kullanilan_ipucu": int(hints_used or 0),
    }
