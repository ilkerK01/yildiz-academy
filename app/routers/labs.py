from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app import config, i18n
from app.db import get_db
from app.deps import require_user_api
from app.models import Lab, LabStep, User, now
from app.services import answers, progress, scoring, security, yerel

router = APIRouter(prefix="/api/lab", tags=["lab"])


class CevapIstek(BaseModel):
    cevap: str


def _lab_or_404(db: DbSession, slug: str) -> Lab:
    lab = db.scalar(select(Lab).where(Lab.slug == slug, Lab.published.is_(True)))
    if lab is None:
        raise HTTPException(404, "Laboratuvar bulunamadı.")
    return lab


def _step_or_404(lab: Lab, index: int) -> LabStep:
    for step in lab.steps:
        if step.step_index == index:
            return step
    raise HTTPException(404, "Adım bulunamadı.")


def _m(request: Request, metin: str) -> str:
    return i18n.cevir(i18n.dil(request), metin)


def _adim_kilitli(lab: Lab, step: LabStep, step_rows: dict) -> bool:
    return step.step_index > progress.current_step_index(lab, step_rows)


@router.post("/{slug}/adim/{index}/cevap")
def cevapla(
    slug: str,
    index: int,
    payload: CevapIstek,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    ip = security.client_ip(request)
    if not security.rate_limit(
        f"cevap:{user.id}:{slug}:{index}:{ip}", config.ANSWER_ATTEMPTS_PER_MINUTE
    ):
        return JSONResponse(
            {"ok": False, "hata": _m(request, "Çok hızlı deniyorsun. Bir dakika bekle.")}, 429
        )

    lab = _lab_or_404(db, slug)
    step = _step_or_404(lab, index)
    step_rows = progress.get_step_rows(db, user.id, lab)

    if _adim_kilitli(lab, step, step_rows):
        raise HTTPException(403, "Bu adım henüz açılmadı.")

    row = progress.get_or_create_step_row(db, user.id, step)
    if row.solved:
        return {"ok": True, "dogru": True, "zaten_cozulmus": True}

    dogru = answers.check(step.answer_type, step.answer_value, payload.cevap)

    if not dogru:
        row.attempts += 1
        progress.get_lab_progress(db, user.id, lab)
        db.commit()
        return {
            "ok": True,
            "dogru": False,
            "deneme": row.attempts,
            "mesaj": _m(request, "Bu değil. Tekrar dene."),
        }

    row.solved = True
    row.solved_at = now()
    row.earned_points = scoring.step_award(step, row.hints_used)
    db.commit()

    lab_progress = progress.recalculate_lab(db, user.id, lab)
    bitti = lab_progress.status == "tamamlandi"

    return {
        "ok": True,
        "dogru": True,
        "kazanilan_puan": row.earned_points,
        "sonraki_adim_acik": (not bitti),
        "lab_bitti": bitti,
        "lab_puani": lab_progress.earned_points,
        "puan_kilitli": bitti and lab_progress.earned_points == 0,
        "cozum_html": yerel.alan(lab, "solution_html", i18n.dil(request)) if bitti else None,
    }


@router.post("/{slug}/adim/{index}/ipucu")
def ipucu(
    slug: str,
    index: int,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    lab = _lab_or_404(db, slug)
    step = _step_or_404(lab, index)
    step_rows = progress.get_step_rows(db, user.id, lab)

    if _adim_kilitli(lab, step, step_rows):
        raise HTTPException(403, "Bu adım henüz açılmadı.")

    row = progress.get_or_create_step_row(db, user.id, step)
    if row.hints_used >= len(step.hints):
        return {"ok": False, "hata": _m(request, "Bu adımda başka ipucu yok.")}

    ipucu_html = yerel.adim(step, i18n.dil(request))["hints"][row.hints_used]
    row.hints_used += 1
    progress.get_lab_progress(db, user.id, lab)
    db.commit()

    return {
        "ok": True,
        "ipucu_html": ipucu_html,
        "yeni_puan": scoring.step_award(step, row.hints_used),
        "kalan_ipucu": len(step.hints) - row.hints_used,
    }


@router.post("/{slug}/pes")
def pes(
    slug: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    lab = _lab_or_404(db, slug)
    progress.give_up(db, user.id, lab)
    return {
        "ok": True,
        "cozum_html": yerel.alan(lab, "solution_html", i18n.dil(request)),
        "mesaj": _m(request, "Çözüm açıldı. Bu labdan artık puan kazanamazsın."),
    }


@router.post("/{slug}/sifirla")
def sifirla(
    slug: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user_api),
):
    lab = _lab_or_404(db, slug)
    lab_progress = progress.reset_lab(db, user.id, lab)
    return {
        "ok": True,
        "puan_kilitli": lab_progress.solution_seen,
        "mesaj": _m(
            request,
            "Lab sıfırlandı. Çözümü daha önce gördüğün için bu tekrar alıştırma "
            "modunda, puan yazılmayacak. En iyi puanın korunuyor."
            if lab_progress.solution_seen
            else "Lab sıfırlandı.",
        ),
    }
