from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import STATIC_DIR
from app.db import Base, engine
from app.deps import LoginRedirect, login_redirect_response
from app.routers import admin, auth, labs, lessons, pages
from app.templating import page


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Yıldız Academy", docs_url=None, redoc_url=None, lifespan=lifespan)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(labs.router)
app.include_router(admin.router)


@app.exception_handler(LoginRedirect)
async def giris_yonlendir(request: Request, exc: LoginRedirect):
    return login_redirect_response(exc.next_url)


@app.get("/admin", include_in_schema=False)
def admin_kisayolu():
    return RedirectResponse("/academy/admin", status_code=301)


@app.exception_handler(404)
async def bulunamadi(request: Request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"ok": False, "hata": "Bulunamadı."}, status_code=404)
    return page(request, "404.html", user=None)
