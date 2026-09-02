from __future__ import annotations

from urllib.parse import quote

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session as DbSession

from app import config
from app.db import get_db
from app.models import User
from app.services import security


class LoginRedirect(Exception):

    def __init__(self, next_url: str) -> None:
        self.next_url = next_url


def current_user(request: Request, db: DbSession = Depends(get_db)) -> User | None:
    token = request.cookies.get(config.USER_COOKIE)
    session = security.resolve_session(db, token, kind="user")
    if session is None or session.user_id is None:
        return None
    user = db.get(User, session.user_id)
    if user is None or not user.is_active:
        return None
    return user


def require_user(
    request: Request, user: User | None = Depends(current_user)
) -> User:
    if user is None:
        raise LoginRedirect(request.url.path + ("?" + request.url.query if request.url.query else ""))
    return user


def require_user_api(user: User | None = Depends(current_user)) -> User:
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Giriş gerekli.")
    return user


def is_admin(request: Request, db: DbSession = Depends(get_db)) -> bool:
    token = request.cookies.get(config.ADMIN_COOKIE)
    return security.resolve_session(db, token, kind="admin") is not None


def require_admin(admin: bool = Depends(is_admin)):
    if not admin:
        raise HTTPException(
            status.HTTP_303_SEE_OTHER,
            "Admin girişi gerekli.",
            headers={"Location": "/academy/admin"},
        )
    return True


def login_redirect_response(next_url: str) -> RedirectResponse:
    target = "/"
    if next_url and next_url != "/":
        target = f"/?next={quote(next_url, safe='')}"
    return RedirectResponse(target, status_code=status.HTTP_303_SEE_OTHER)
