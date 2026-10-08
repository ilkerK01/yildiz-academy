from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app import config
from app.config import STATIC_DIR
from app.db import sema_guncelle
from app.deps import LoginRedirect, login_redirect_response
from app.routers import admin, auth, labs, lessons, medya, pages
from app.templating import page


@asynccontextmanager
async def lifespan(_: FastAPI):
    sema_guncelle()
    yield

app = FastAPI(title="Yıldız Academy", docs_url=None, redoc_url=None, lifespan=lifespan)

GUVENLIK_BASLIKLARI = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "same-origin",
    "Content-Security-Policy": "frame-ancestors 'none'; object-src 'none'; base-uri 'self'; form-action 'self'",
}
GOVDE_SINIRI = 2 * 1024 * 1024


@app.middleware("http")
async def guvenlik_katmani(request: Request, call_next):
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        site = request.headers.get("sec-fetch-site")
        kaynak = request.headers.get("origin")
        beklenen = f"{request.url.scheme}://{request.url.netloc}"
        if site == "cross-site" or (kaynak and kaynak != "null" and kaynak != beklenen):
            return JSONResponse({"ok": False, "hata": "İstek reddedildi."}, status_code=403)
        uzunluk = request.headers.get("content-length")
        sinir = GOVDE_SINIRI
        if request.url.path.startswith("/academy/admin/icerik/"):
            # Word belgeleri ve videolar: asıl sınır ilgili uç noktada denetlenir.
            sinir = config.VIDEO_MAX_MB * 1024 * 1024 + GOVDE_SINIRI
        elif request.url.path == "/api/ayarlar/avatar":
            sinir = config.AVATAR_MAX_MB * 1024 * 1024 + GOVDE_SINIRI
        if uzunluk and uzunluk.isdigit() and int(uzunluk) > sinir:
            return JSONResponse({"ok": False, "hata": "İstek çok büyük."}, status_code=413)
    yanit = await call_next(request)
    for ad, deger in GUVENLIK_BASLIKLARI.items():
        yanit.headers.setdefault(ad, deger)
    return yanit

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(labs.router)
app.include_router(admin.router)
app.include_router(medya.router)


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
    yanit = page(request, "404.html", user=None)
    yanit.status_code = 404
    return yanit
