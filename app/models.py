from __future__ import annotations

import secrets
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def now() -> datetime:
    return datetime.now(timezone.utc)


def yeni_public_id() -> str:
    return secrets.token_urlsafe(9)


class Lesson(Base):
    __tablename__ = "lesson"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(String(400), default="")
    body_md: Mapped[str] = mapped_column(Text, default="")
    body_html: Mapped[str] = mapped_column(Text, default="")
    reading_minutes: Mapped[int] = mapped_column(Integer, default=5)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    published: Mapped[bool] = mapped_column(Boolean, default=True)


class Lab(Base):
    __tablename__ = "lab"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(String(400), default="")
    briefing_md: Mapped[str] = mapped_column(Text, default="")
    briefing_html: Mapped[str] = mapped_column(Text, default="")
    difficulty: Mapped[str] = mapped_column(String(10), default="kolay")
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    solution_md: Mapped[str] = mapped_column(Text, default="")
    solution_html: Mapped[str] = mapped_column(Text, default="")
    published: Mapped[bool] = mapped_column(Boolean, default=True)

    steps: Mapped[list["LabStep"]] = relationship(
        back_populates="lab",
        cascade="all, delete-orphan",
        order_by="LabStep.step_index",
    )


class LabStep(Base):
    __tablename__ = "lab_step"
    __table_args__ = (UniqueConstraint("lab_id", "step_index", name="uq_step_sira"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    lab_id: Mapped[int] = mapped_column(ForeignKey("lab.id", ondelete="CASCADE"))
    step_index: Mapped[int] = mapped_column(Integer)
    prompt_md: Mapped[str] = mapped_column(Text, default="")
    prompt_html: Mapped[str] = mapped_column(Text, default="")
    artifact: Mapped[str | None] = mapped_column(Text, nullable=True)
    answer_type: Mapped[str] = mapped_column(String(10))

    answer_value: Mapped[str] = mapped_column(Text)

    choices_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    points: Mapped[int] = mapped_column(Integer, default=10)

    lab: Mapped[Lab] = relationship(back_populates="steps")
    hints: Mapped[list["LabHint"]] = relationship(
        back_populates="step",
        cascade="all, delete-orphan",
        order_by="LabHint.hint_index",
    )


class LabHint(Base):
    __tablename__ = "lab_hint"
    __table_args__ = (UniqueConstraint("step_id", "hint_index", name="uq_ipucu_sira"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    step_id: Mapped[int] = mapped_column(ForeignKey("lab_step.id", ondelete="CASCADE"))
    hint_index: Mapped[int] = mapped_column(Integer)
    text_md: Mapped[str] = mapped_column(Text)
    text_html: Mapped[str] = mapped_column(Text, default="")
    penalty: Mapped[int] = mapped_column(Integer, default=0)

    step: Mapped[LabStep] = relationship(back_populates="hints")


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))


class ContentTag(Base):

    __tablename__ = "content_tag"
    __table_args__ = (
        UniqueConstraint("tag_id", "content_type", "content_id", name="uq_icerik_etiket"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"), index=True)
    content_type: Mapped[str] = mapped_column(String(10))
    content_id: Mapped[int] = mapped_column(Integer, index=True)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(
        String(16), unique=True, index=True, default=yeni_public_id
    )

    display_name: Mapped[str] = mapped_column(String(24), unique=True, index=True)
    display_name_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class PasswordReset(Base):
    __tablename__ = "password_reset"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AdminUser(Base):
    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class Session(Base):

    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    kind: Mapped[str] = mapped_column(String(10), default="user")
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class LessonProgress(Base):

    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id", name="uq_ders_ilerleme"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    lesson_id: Mapped[int] = mapped_column(
        ForeignKey("lesson.id", ondelete="CASCADE"), index=True
    )
    read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class LabProgress(Base):
    __tablename__ = "lab_progress"
    __table_args__ = (UniqueConstraint("user_id", "lab_id", name="uq_lab_ilerleme"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    lab_id: Mapped[int] = mapped_column(ForeignKey("lab.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(15), default="basladi")
    earned_points: Mapped[int] = mapped_column(Integer, default=0)
    best_points: Mapped[int] = mapped_column(Integer, default=0)
    best_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    solution_seen: Mapped[bool] = mapped_column(Boolean, default=False)

    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class StepProgress(Base):
    __tablename__ = "step_progress"
    __table_args__ = (UniqueConstraint("user_id", "step_id", name="uq_adim_ilerleme"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), index=True
    )
    step_id: Mapped[int] = mapped_column(
        ForeignKey("lab_step.id", ondelete="CASCADE"), index=True
    )
    solved: Mapped[bool] = mapped_column(Boolean, default=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    earned_points: Mapped[int] = mapped_column(Integer, default=0)
    solved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
