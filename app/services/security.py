from __future__ import annotations

import hashlib
import re
import secrets
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session as DbSession

from app import config
from app.models import AdminUser, PasswordReset, Session, User, now

_hasher = PasswordHasher()


def hash_password(raw: str) -> str:
    return _hasher.hash(raw)


def verify_password(hashed: str, raw: str) -> bool:
    try:
        return _hasher.verify(hashed, raw)
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_NAME_RE = re.compile(r"^[\wçğıöşüÇĞİÖŞÜ][\wçğıöşüÇĞİÖŞÜ ._-]*$", re.UNICODE)


def check_display_name(value: str) -> str | None:
    value = value.strip()
    if not (config.DISPLAY_NAME_MIN <= len(value) <= config.DISPLAY_NAME_MAX):
        return (
            f"Görünen ad {config.DISPLAY_NAME_MIN}-{config.DISPLAY_NAME_MAX} "
            "karakter olmalı."
        )
    if not _NAME_RE.match(value):
        return "Görünen ad harf, rakam, boşluk, nokta, alt çizgi ve tire içerebilir."
    return None


def check_email(value: str) -> str | None:
    if not _EMAIL_RE.match(value.strip()):
        return "E-posta adresi geçerli görünmüyor."
    return None


def check_password(value: str) -> str | None:
    if len(value) < config.PASSWORD_MIN:
        return f"Parola en az {config.PASSWORD_MIN} karakter olmalı."
    return None


def normalize_email(value: str) -> str:
    return value.strip().lower()


def _expiry(kind: str) -> datetime:
    if kind == "admin":
        return now() + timedelta(hours=config.ADMIN_SESSION_HOURS)
    return now() + timedelta(days=config.USER_SESSION_DAYS)


def create_session(db: DbSession, *, kind: str, user_id: int | None = None) -> Session:
    row = Session(
        token=secrets.token_urlsafe(32),
        kind=kind,
        user_id=user_id,
        expires_at=_expiry(kind),
    )
    db.add(row)
    db.commit()
    return row


def resolve_session(db: DbSession, token: str | None, *, kind: str) -> Session | None:
    if not token:
        return None
    row = db.scalar(select(Session).where(Session.token == token, Session.kind == kind))
    if row is None:
        return None
    expires = row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < now():
        db.delete(row)
        db.commit()
        return None
    return row


def destroy_session(db: DbSession, token: str | None) -> None:
    if not token:
        return
    db.execute(delete(Session).where(Session.token == token))
    db.commit()


def destroy_user_sessions(db: DbSession, user_id: int) -> None:
    db.execute(delete(Session).where(Session.user_id == user_id))
    db.commit()


def set_session_cookie(response, token: str, *, kind: str) -> None:
    if kind == "admin":
        name = config.ADMIN_COOKIE
        max_age = config.ADMIN_SESSION_HOURS * 3600
    else:
        name = config.USER_COOKIE
        max_age = config.USER_SESSION_DAYS * 86400
    response.set_cookie(
        name,
        token,
        max_age=max_age,
        httponly=True,
        samesite="lax",
        secure=config.COOKIE_SECURE,
        path="/",
    )


def clear_session_cookie(response, *, kind: str) -> None:
    name = config.ADMIN_COOKIE if kind == "admin" else config.USER_COOKIE
    response.delete_cookie(name, path="/")


def verify_admin(db: DbSession, username: str, password: str) -> AdminUser | None:
    admin = db.scalar(
        select(AdminUser).where(
            AdminUser.username == username.strip(), AdminUser.is_active.is_(True)
        )
    )
    if admin is None:
        _hasher.hash(password)
        return None
    if not verify_password(admin.password_hash, password):
        return None
    admin.last_login_at = now()
    db.commit()
    return admin


def create_admin(db: DbSession, username: str, password: str) -> AdminUser:
    admin = AdminUser(username=username.strip(), password_hash=hash_password(password))
    db.add(admin)
    db.commit()
    return admin


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_reset_token(db: DbSession, user_id: int) -> str:
    db.execute(
        update(PasswordReset)
        .where(PasswordReset.user_id == user_id, PasswordReset.used_at.is_(None))
        .values(used_at=now())
    )
    token = secrets.token_urlsafe(32)
    db.add(
        PasswordReset(
            user_id=user_id,
            token_hash=_token_hash(token),
            expires_at=now() + timedelta(minutes=config.RESET_TOKEN_MINUTES),
        )
    )
    db.commit()
    return token


def resolve_reset_token(db: DbSession, token: str | None) -> PasswordReset | None:
    if not token:
        return None
    row = db.scalar(select(PasswordReset).where(PasswordReset.token_hash == _token_hash(token)))
    if row is None or row.used_at is not None:
        return None
    expires = row.expires_at
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)
    if expires < now():
        return None
    return row


_hits: dict[str, deque[float]] = defaultdict(deque)
_son_temizlik = 0.0


def _temizle(cutoff: float) -> None:
    global _son_temizlik
    if time.monotonic() - _son_temizlik < 60:
        return
    _son_temizlik = time.monotonic()
    for anahtar in [k for k, v in _hits.items() if not v or v[-1] < cutoff]:
        del _hits[anahtar]


def rate_limit(key: str, limit: int, window: float = 60.0) -> bool:
    cutoff = time.monotonic() - window
    _temizle(cutoff)
    bucket = _hits[key]
    while bucket and bucket[0] < cutoff:
        bucket.popleft()
    if len(bucket) >= limit:
        return False
    bucket.append(time.monotonic())
    return True


def client_ip(request) -> str:
    return request.client.host if request.client else "bilinmiyor"
