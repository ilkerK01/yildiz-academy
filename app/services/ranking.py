from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app.models import Lab, LabProgress, LessonProgress, StepProgress, User


@dataclass
class RankRow:
    user_id: int
    display_name: str
    points: int
    rank: int


def leaderboard(db: DbSession, limit: int = 20) -> list[RankRow]:
    stmt = (
        select(
            User.id,
            User.display_name,
            func.coalesce(func.sum(LabProgress.earned_points), 0).label("puan"),
            func.max(LabProgress.completed_at).label("son_bitis"),
        )
        .join(LabProgress, LabProgress.user_id == User.id)
        .where(LabProgress.status == "tamamlandi", User.is_active.is_(True))
        .group_by(User.id)
        .having(func.coalesce(func.sum(LabProgress.earned_points), 0) > 0)
        .order_by(func.coalesce(func.sum(LabProgress.earned_points), 0).desc(),
                  func.max(LabProgress.completed_at).asc())
        .limit(limit)
    )
    rows = db.execute(stmt).all()
    return [
        RankRow(user_id=r[0], display_name=r[1], points=int(r[2]), rank=i + 1)
        for i, r in enumerate(rows)
    ]


def own_rank(db: DbSession, user_id: int) -> int | None:
    full = leaderboard(db, limit=10_000)
    for row in full:
        if row.user_id == user_id:
            return row.rank
    return None


@dataclass
class Badge:
    slug: str
    name: str
    description: str
    earned: bool


def badges(db: DbSession, user_id: int) -> list[Badge]:
    scored_labs = db.execute(
        select(LabProgress.lab_id, LabProgress.earned_points).where(
            LabProgress.user_id == user_id,
            LabProgress.status == "tamamlandi",
            LabProgress.earned_points > 0,
        )
    ).all()
    lab_count = len(scored_labs)

    lesson_count = db.scalar(
        select(func.count(LessonProgress.id)).where(LessonProgress.user_id == user_id)
    ) or 0

    hintless = False
    perfect = False
    for lab_id, earned in scored_labs:
        lab = db.get(Lab, lab_id)
        if lab is None:
            continue
        step_ids = [s.id for s in lab.steps]
        if not step_ids:
            continue
        used = db.scalar(
            select(func.coalesce(func.sum(StepProgress.hints_used), 0)).where(
                StepProgress.user_id == user_id, StepProgress.step_id.in_(step_ids)
            )
        ) or 0
        if used == 0:
            hintless = True
        if earned >= lab.total_points and lab.total_points > 0:
            perfect = True

    return [
        Badge("ilk-adim", "İlk adım", "İlk labını tamamladın", lab_count >= 1),
        Badge("beslik", "Beşlik", "5 lab tamamladın", lab_count >= 5),
        Badge("onluk", "Onluk", "10 lab tamamladın", lab_count >= 10),
        Badge("okur", "Okur", "5 ders okudun", lesson_count >= 5),
        Badge("kutuphane-faresi", "Kütüphane faresi", "15 ders okudun", lesson_count >= 15),
        Badge("yalniz-avci", "Yalnız avcı", "Bir labı hiç ipucu açmadan tamamladın", hintless),
        Badge("kusursuz", "Kusursuz", "Bir labı tam puanla tamamladın", perfect),
    ]
