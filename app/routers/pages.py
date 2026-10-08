from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session as DbSession

from app import i18n
from app.config import STATIC_DIR
from app.db import get_db
from app.deps import current_user, guvenli_yol, require_user
from app.models import ContentTag, Lab, Lesson, Tag, User
from app.services import progress, ranking, scoring, video, yerel
from app.templating import page

router = APIRouter(tags=["sayfa"])


def _tags_for(db: DbSession, content_type: str, content_id: int) -> list[Tag]:
    return list(
        db.scalars(
            select(Tag)
            .join(ContentTag, ContentTag.tag_id == Tag.id)
            .where(
                ContentTag.content_type == content_type,
                ContentTag.content_id == content_id,
            )
            .order_by(Tag.name)
        )
    )


def _tag_map(db: DbSession, content_type: str, ids: list[int]) -> dict[int, list[Tag]]:
    if not ids:
        return {}
    rows = db.execute(
        select(ContentTag.content_id, Tag)
        .join(Tag, Tag.id == ContentTag.tag_id)
        .where(ContentTag.content_type == content_type, ContentTag.content_id.in_(ids))
        .order_by(Tag.name)
    ).all()
    out: dict[int, list[Tag]] = {}
    for content_id, tag in rows:
        out.setdefault(content_id, []).append(tag)
    return out


def _related_labs(db: DbSession, lesson: Lesson) -> list[Lab]:
    tag_ids = [t.id for t in _tags_for(db, "lesson", lesson.id)]
    if not tag_ids:
        return []
    lab_ids = db.scalars(
        select(ContentTag.content_id).where(
            ContentTag.content_type == "lab", ContentTag.tag_id.in_(tag_ids)
        )
    ).all()
    if not lab_ids:
        return []
    return list(
        db.scalars(
            select(Lab).where(Lab.id.in_(set(lab_ids)), Lab.published.is_(True))
        )
    )


def _vitrin_sayilari(db: DbSession) -> dict[str, int]:
    # Açılış sayfasındaki sayaçlar: yalnızca yayımlanmış içerik sayılır.
    return {
        "ders": db.scalar(select(func.count()).select_from(Lesson).where(Lesson.published.is_(True))) or 0,
        "lab": db.scalar(select(func.count()).select_from(Lab).where(Lab.published.is_(True))) or 0,
        "puan": db.scalar(select(func.coalesce(func.sum(Lab.total_points), 0)).where(Lab.published.is_(True))) or 0,
        "etiket": db.scalar(select(func.count()).select_from(Tag)) or 0,
    }


@router.get("/")
def acilis(
    request: Request,
    user: User | None = Depends(current_user),
    db: DbSession = Depends(get_db),
):
    if user is not None:
        return RedirectResponse("/panel", status_code=303)
    return page(
        request,
        "index.html",
        next=guvenli_yol(request.query_params.get("next", ""), ""),
        sayilar=_vitrin_sayilari(db),
    )


@router.get("/sifre-sifirla")
def sifre_sifirla_sayfasi(request: Request, token: str = "", db: DbSession = Depends(get_db)):
    return page(request, "index.html", next="", sifirla_token=token, sayilar=_vitrin_sayilari(db))


@router.get("/hakkinda")
def hakkinda(request: Request, user: User | None = Depends(current_user)):
    return page(request, "hakkinda.html", user=user)


@router.get("/stil")
def stil():
    path = STATIC_DIR / "styleguide.html"
    if not path.exists():
        raise HTTPException(404, "Stil rehberi bulunamadı.")
    return FileResponse(path)


@router.get("/panel")
def panel(request: Request, db: DbSession = Depends(get_db), user: User = Depends(require_user)):
    stats = progress.user_stats(db, user.id)
    return page(
        request,
        "panel.html",
        user=user,
        stats=stats,
        siralama=ranking.leaderboard(db, limit=10),
        kendi_sira=ranking.own_rank(db, user.id),
        rozetler=ranking.badges(db, user.id),
        devam=progress.active_lab(db, user.id),
    )


@router.get("/dil/{kod}")
def dil_degistir(kod: str, next: str = "/"):
    hedef = guvenli_yol(next, "/")
    response = RedirectResponse(hedef, status_code=303)
    if kod in i18n.DILLER:
        response.set_cookie(
            i18n.CEREZ, kod, max_age=60 * 60 * 24 * 365, httponly=True, samesite="lax"
        )
    return response


@router.get("/profil")
def profilim(user: User = Depends(require_user)):
    return RedirectResponse(f"/profil/{user.public_id}", status_code=303)


@router.get("/profil/{public_id}")
def profil(
    public_id: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user),
):
    kisi = db.scalar(select(User).where(User.public_id == public_id))
    if kisi is None or not kisi.is_active:
        raise HTTPException(404, "Kullanıcı bulunamadı.")
    return page(
        request,
        "profil.html",
        user=user,
        kisi=kisi,
        kendi=kisi.id == user.id,
        profil_stats=progress.user_stats(db, kisi.id),
        sira=ranking.own_rank(db, kisi.id),
        rozetler=ranking.badges(db, kisi.id),
        tamamlananlar=progress.completed_labs(db, kisi.id),
    )


@router.get("/ayarlar")
def ayarlar(request: Request, user: User = Depends(require_user)):
    return page(request, "ayarlar.html", user=user)


@router.get("/kutuphane")
def kutuphane(
    request: Request, db: DbSession = Depends(get_db), user: User = Depends(require_user)
):
    dersler = list(
        db.scalars(
            select(Lesson)
            .where(Lesson.published.is_(True))
            .order_by(Lesson.order_index, Lesson.title)
        )
    )
    return page(
        request,
        "kutuphane.html",
        user=user,
        dersler=dersler,
        etiketler=_tag_map(db, "lesson", [d.id for d in dersler]),
        okunanlar=progress.read_lesson_ids(db, user.id),
    )


@router.get("/kutuphane/{slug}")
def ders(
    slug: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user),
):
    lesson = db.scalar(select(Lesson).where(Lesson.slug == slug, Lesson.published.is_(True)))
    if lesson is None:
        raise HTTPException(404, "Ders bulunamadı.")
    return page(
        request,
        "ders.html",
        user=user,
        ders=lesson,
        video=video.ders_videosu(db, lesson, i18n.dil(request)),
        etiketler=_tags_for(db, "lesson", lesson.id),
        ilgili_lablar=_related_labs(db, lesson),
        okundu=lesson.id in progress.read_lesson_ids(db, user.id),
    )


@router.get("/lab")
def lablar(
    request: Request, db: DbSession = Depends(get_db), user: User = Depends(require_user)
):
    labs = list(
        db.scalars(
            select(Lab)
            .where(Lab.published.is_(True))
            .order_by(Lab.order_index, Lab.title)
        )
    )
    durumlar = {}
    for lab in labs:
        row = progress.view_lab_progress(db, user.id, lab)
        durumlar[lab.id] = row
    return page(
        request,
        "lablar.html",
        user=user,
        lablar=labs,
        durumlar=durumlar,
        etiketler=_tag_map(db, "lab", [l.id for l in labs]),
    )


@router.get("/lab/{slug}")
def lab_detay(
    slug: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user),
):
    lab = db.scalar(select(Lab).where(Lab.slug == slug, Lab.published.is_(True)))
    if lab is None:
        raise HTTPException(404, "Laboratuvar bulunamadı.")

    lab_progress = progress.view_lab_progress(db, user.id, lab)
    step_rows = progress.get_step_rows(db, user.id, lab)
    aktif = progress.current_step_index(lab, step_rows)

    kod = i18n.dil(request)
    adimlar = []
    for step in lab.steps:
        row = step_rows.get(step.id)
        metin = yerel.adim(step, kod)
        acilan_ipuclari = metin["hints"][: (row.hints_used if row else 0)]
        adimlar.append(
            {
                "index": step.step_index,
                "soru_html": metin["prompt_html"],
                "iz": metin["artifact"],
                "tip": step.answer_type,
                "siklar": metin["choices"],
                "puan": step.points,
                "guncel_puan": scoring.step_award(step, row.hints_used if row else 0),
                "cozuldu": bool(row and row.solved),
                "deneme": row.attempts if row else 0,
                "acilan_ipuclari": acilan_ipuclari,
                "kalan_ipucu": len(step.hints) - (row.hints_used if row else 0),
                "kilitli": step.step_index > aktif,
            }
        )

    return page(
        request,
        "lab.html",
        user=user,
        lab=lab,
        adimlar=adimlar,
        durum=lab_progress,
        aktif_adim=aktif,
        etiketler=_tags_for(db, "lab", lab.id),
        cozum_acik=lab_progress.solution_seen,
    )


@router.get("/etiket/{slug}")
def etiket(
    slug: str,
    request: Request,
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user),
):
    tag = db.scalar(select(Tag).where(Tag.slug == slug))
    if tag is None:
        raise HTTPException(404, "Etiket bulunamadı.")

    lesson_ids = db.scalars(
        select(ContentTag.content_id).where(
            ContentTag.tag_id == tag.id, ContentTag.content_type == "lesson"
        )
    ).all()
    lab_ids = db.scalars(
        select(ContentTag.content_id).where(
            ContentTag.tag_id == tag.id, ContentTag.content_type == "lab"
        )
    ).all()

    dersler = (
        list(db.scalars(select(Lesson).where(Lesson.id.in_(lesson_ids), Lesson.published.is_(True))))
        if lesson_ids
        else []
    )
    labs = (
        list(db.scalars(select(Lab).where(Lab.id.in_(lab_ids), Lab.published.is_(True))))
        if lab_ids
        else []
    )
    return page(request, "etiket.html", user=user, etiket=tag, dersler=dersler, lablar=labs)


@router.get("/ara")
def ara(
    request: Request,
    q: str = "",
    db: DbSession = Depends(get_db),
    user: User = Depends(require_user),
):
    q = q.strip()
    dersler: list[Lesson] = []
    labs: list[Lab] = []
    if len(q) >= 2:
        kalip = f"%{q}%"

        def etiketli(tur: str):
            return (
                select(ContentTag.content_id)
                .join(Tag, Tag.id == ContentTag.tag_id)
                .where(
                    ContentTag.content_type == tur,
                    or_(Tag.name.ilike(kalip), Tag.slug.ilike(kalip)),
                )
            )

        dersler = list(
            db.scalars(
                select(Lesson).where(
                    Lesson.published.is_(True),
                    or_(
                        Lesson.title.ilike(kalip),
                        Lesson.summary.ilike(kalip),
                        Lesson.en_json.ilike(kalip),
                        Lesson.id.in_(etiketli("lesson")),
                    ),
                ).order_by(Lesson.order_index, Lesson.title)
            )
        )
        labs = list(
            db.scalars(
                select(Lab).where(
                    Lab.published.is_(True),
                    or_(
                        Lab.title.ilike(kalip),
                        Lab.summary.ilike(kalip),
                        Lab.briefing_md.ilike(kalip),
                        Lab.en_json.ilike(kalip),
                        Lab.id.in_(etiketli("lab")),
                    ),
                ).order_by(Lab.order_index, Lab.title)
            )
        )
    return page(request, "ara.html", user=user, q=q, dersler=dersler, lablar=labs)
