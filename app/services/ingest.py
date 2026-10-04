from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from sqlalchemy import delete, select
from sqlalchemy.orm import Session as DbSession

from app.models import ContentTag, Lab, LabHint, LabStep, Lesson, Tag
from app.services import answers
from app.services.markdown import render


class IngestError(Exception):
    pass


@dataclass
class Preview:

    kind: str
    slug: str
    title: str
    lines: list[str] = field(default_factory=list)


_FRONTMATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def slugify(value: str) -> str:
    table = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")
    value = value.translate(table).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_lesson(text: str, *, filename: str = "") -> dict:
    match = _FRONTMATTER.match(text.lstrip("﻿"))
    if not match:
        raise IngestError(
            f"{filename}: dosya `---` ile başlayan YAML frontmatter içermiyor."
        )
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise IngestError(f"{filename}: frontmatter okunamadı. {exc}") from exc
    if not isinstance(meta, dict):
        raise IngestError(f"{filename}: frontmatter bir sözlük olmalı.")

    title = str(meta.get("title") or "").strip()
    if not title:
        raise IngestError(f"{filename}: `title` zorunlu.")

    slug = str(meta.get("slug") or slugify(title)).strip()
    body = match.group(2).strip()

    return {
        "slug": slug,
        "title": title,
        "summary": str(meta.get("summary") or "").strip(),
        "body_md": body,
        "reading_minutes": int(meta.get("reading_minutes") or _estimate_minutes(body)),
        "order_index": int(meta.get("order_index") or 0),
        "published": bool(meta.get("published", True)),
        "tags": [str(t) for t in (meta.get("tags") or [])],
    }


def _estimate_minutes(body: str) -> int:
    words = len(body.split())
    return max(1, round(words / 180))


def parse_lab(text: str, *, filename: str = "") -> dict:
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        yer = f" (satır {mark.line + 1})" if mark else ""
        raise IngestError(f"{filename}: YAML okunamadı{yer}. {exc}") from exc

    if not isinstance(data, dict):
        raise IngestError(f"{filename}: dosyanın kökü bir sözlük olmalı.")

    title = str(data.get("title") or "").strip()
    if not title:
        raise IngestError(f"{filename}: `title` zorunlu.")

    slug = str(data.get("slug") or slugify(title)).strip()
    difficulty = str(data.get("difficulty") or "kolay").strip()
    if difficulty not in {"kolay", "orta", "zor"}:
        raise IngestError(
            f"{filename}: `difficulty` kolay/orta/zor olmalı, '{difficulty}' geldi."
        )

    raw_steps = data.get("steps") or []
    if not raw_steps:
        raise IngestError(f"{filename}: en az bir adım gerekli.")

    steps = []
    total = 0
    for i, raw in enumerate(raw_steps, start=1):
        if not isinstance(raw, dict):
            raise IngestError(f"{filename}: {i}. adım bir sözlük değil.")

        prompt = str(raw.get("prompt_md") or "").strip()
        if not prompt:
            raise IngestError(f"{filename}: {i}. adımda `prompt_md` boş.")

        answer_type = str(raw.get("answer_type") or "exact").strip()
        answer_value = str(raw.get("answer_value", "")).strip()
        if not answer_value:
            raise IngestError(f"{filename}: {i}. adımda `answer_value` boş.")

        choices = raw.get("choices")
        problem = answers.validate_definition(answer_type, answer_value, choices)
        if problem:
            raise IngestError(f"{filename}: {i}. adım. {problem}")

        points = int(raw.get("points") or 0)
        if points <= 0:
            raise IngestError(f"{filename}: {i}. adımın puanı pozitif olmalı.")

        hints = []
        for j, hint in enumerate(raw.get("hints") or [], start=1):
            if not isinstance(hint, dict):
                raise IngestError(f"{filename}: {i}. adımın {j}. ipucusu sözlük değil.")
            hint_text = str(hint.get("text_md") or "").strip()
            if not hint_text:
                raise IngestError(f"{filename}: {i}. adımın {j}. ipucusu boş.")
            hints.append(
                {
                    "hint_index": j,
                    "text_md": hint_text,
                    "penalty": max(0, int(hint.get("penalty") or 0)),
                }
            )

        total += points
        steps.append(
            {
                "step_index": i,
                "prompt_md": prompt,
                "artifact": (str(raw["artifact"]).strip() if raw.get("artifact") else None),
                "answer_type": answer_type,
                "answer_value": answer_value,
                "choices": [str(c) for c in choices] if choices else None,
                "points": points,
                "hints": hints,
            }
        )

    return {
        "slug": slug,
        "title": title,
        "summary": str(data.get("summary") or "").strip(),
        "briefing_md": str(data.get("briefing_md") or "").strip(),
        "solution_md": str(data.get("solution_md") or "").strip(),
        "difficulty": difficulty,
        "order_index": int(data.get("order_index") or 0),
        "published": bool(data.get("published", True)),
        "total_points": total,
        "tags": [str(t) for t in (data.get("tags") or [])],
        "steps": steps,
    }


def preview_lesson(parsed: dict) -> Preview:
    return Preview(
        kind="lesson",
        slug=parsed["slug"],
        title=parsed["title"],
        lines=[
            f"Okuma süresi: {parsed['reading_minutes']} dk",
            f"Etiketler: {', '.join(parsed['tags']) or 'yok'}",
            f"Yayında: {'evet' if parsed['published'] else 'hayır'}",
        ],
    )


def preview_lab(parsed: dict) -> Preview:
    hint_count = sum(len(s["hints"]) for s in parsed["steps"])
    return Preview(
        kind="lab",
        slug=parsed["slug"],
        title=parsed["title"],
        lines=[
            f"Zorluk: {parsed['difficulty']}",
            f"Adım sayısı: {len(parsed['steps'])}",
            f"İpucu sayısı: {hint_count}",
            f"Toplam puan: {parsed['total_points']}",
            f"Etiketler: {', '.join(parsed['tags']) or 'yok'}",
            f"Çözüm metni: {'var' if parsed['solution_md'] else 'YOK'}",
        ],
    )


def _sync_tags(db: DbSession, content_type: str, content_id: int, names: list[str]) -> None:
    db.execute(
        delete(ContentTag).where(
            ContentTag.content_type == content_type, ContentTag.content_id == content_id
        )
    )
    for name in names:
        slug = slugify(name)
        if not slug:
            continue
        tag = db.scalar(select(Tag).where(Tag.slug == slug))
        if tag is None:
            tag = Tag(slug=slug, name=name)
            db.add(tag)
            db.flush()
        db.add(ContentTag(tag_id=tag.id, content_type=content_type, content_id=content_id))


def save_lesson(db: DbSession, parsed: dict) -> Lesson:
    lesson = db.scalar(select(Lesson).where(Lesson.slug == parsed["slug"]))
    if lesson is None:
        lesson = Lesson(slug=parsed["slug"])
        db.add(lesson)

    lesson.title = parsed["title"]
    lesson.summary = parsed["summary"]
    lesson.body_md = parsed["body_md"]
    lesson.body_html = render(parsed["body_md"])
    lesson.reading_minutes = parsed["reading_minutes"]
    lesson.order_index = parsed["order_index"]
    lesson.published = parsed["published"]
    db.flush()

    _sync_tags(db, "lesson", lesson.id, parsed["tags"])
    db.commit()
    return lesson


def save_lab(db: DbSession, parsed: dict) -> Lab:
    lab = db.scalar(select(Lab).where(Lab.slug == parsed["slug"]))
    if lab is None:
        lab = Lab(slug=parsed["slug"])
        db.add(lab)

    lab.title = parsed["title"]
    lab.summary = parsed["summary"]
    lab.briefing_md = parsed["briefing_md"]
    lab.briefing_html = render(parsed["briefing_md"])
    lab.solution_md = parsed["solution_md"]
    lab.solution_html = render(parsed["solution_md"])
    lab.difficulty = parsed["difficulty"]
    lab.order_index = parsed["order_index"]
    lab.published = parsed["published"]
    lab.total_points = parsed["total_points"]
    db.flush()

    mevcut = {
        step.step_index: step
        for step in db.scalars(select(LabStep).where(LabStep.lab_id == lab.id))
    }
    yeni_siralar = {raw["step_index"] for raw in parsed["steps"]}
    for sira, step in mevcut.items():
        if sira not in yeni_siralar:
            db.delete(step)
    db.flush()

    for raw in parsed["steps"]:
        step = mevcut.get(raw["step_index"])
        if step is None:
            step = LabStep(lab_id=lab.id, step_index=raw["step_index"])
            db.add(step)
        step.prompt_md = raw["prompt_md"]
        step.prompt_html = render(raw["prompt_md"])
        step.artifact = raw["artifact"]
        step.answer_type = raw["answer_type"]
        step.answer_value = raw["answer_value"]
        step.choices_json = (
            json.dumps(raw["choices"], ensure_ascii=False) if raw["choices"] else None
        )
        step.points = raw["points"]
        step.hints.clear()
        db.flush()
        for hint in raw["hints"]:
            step.hints.append(
                LabHint(
                    hint_index=hint["hint_index"],
                    text_md=hint["text_md"],
                    text_html=render(hint["text_md"]),
                    penalty=hint["penalty"],
                )
            )
        db.flush()

    _sync_tags(db, "lab", lab.id, parsed["tags"])
    db.commit()
    return lab


def ingest_text(db: DbSession, filename: str, text: str, *, commit: bool = True):
    lower = filename.lower()
    if lower.endswith(".md"):
        parsed = parse_lesson(text, filename=filename)
        preview = preview_lesson(parsed)
    elif lower.endswith((".yaml", ".yml")):
        parsed = parse_lab(text, filename=filename)
        preview = preview_lab(parsed)
    else:
        raise IngestError(f"{filename}: yalnızca .md ve .yaml kabul edilir.")

    if commit:
        if preview.kind == "lesson":
            save_lesson(db, parsed)
        else:
            save_lab(db, parsed)
    return parsed, preview


def ingest_directory(db: DbSession, root: Path) -> list[str]:
    log: list[str] = []
    for path in sorted((root / "dersler").glob("*.md")):
        _, preview = ingest_text(db, path.name, path.read_text(encoding="utf-8"))
        log.append(f"ders  {preview.slug}  {preview.title}")
    for path in sorted((root / "lablar").glob("*.y*ml")):
        _, preview = ingest_text(db, path.name, path.read_text(encoding="utf-8"))
        log.append(f"lab   {preview.slug}  {preview.title}")
    return log
