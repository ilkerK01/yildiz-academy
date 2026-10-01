from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


def _bool(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "evet"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


APP_DIR = BASE_DIR / "app"
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
CONTENT_DIR = BASE_DIR / "content"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'yildiz.db'}")

USER_COOKIE = "ya_oturum"
ADMIN_COOKIE = "ya_admin"
COOKIE_SECURE = _bool("COOKIE_SECURE", "0")
USER_SESSION_DAYS = _int("USER_SESSION_DAYS", 30)
ADMIN_SESSION_HOURS = _int("ADMIN_SESSION_HOURS", 8)

LOGIN_ATTEMPTS_PER_MINUTE = 5
ANSWER_ATTEMPTS_PER_MINUTE = 10
ANSWER_MAX_LENGTH = 200
UPLOAD_MAX_BYTES = 1 * 1024 * 1024

DISPLAY_NAME_MIN = 3
DISPLAY_NAME_MAX = 24
PASSWORD_MIN = 8
DISPLAY_NAME_COOLDOWN_DAYS = 30

SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")
RESET_TOKEN_MINUTES = _int("RESET_TOKEN_MINUTES", 30)

SMTP_HOST = os.getenv("SMTP_HOST", "").strip()
SMTP_PORT = _int("SMTP_PORT", 587)
SMTP_USER = os.getenv("SMTP_USER", "").strip()
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_FROM = os.getenv("SMTP_FROM", "").strip() or SMTP_USER
SMTP_SSL = _bool("SMTP_SSL", "0")
