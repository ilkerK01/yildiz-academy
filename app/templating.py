from __future__ import annotations

from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from app import i18n
from app.config import STATIC_DIR, TEMPLATES_DIR

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

ZORLUK_SINIF = {"kolay": "easy", "orta": "medium", "zor": "hard"}

templates.env.globals["zorluk_sinif"] = lambda d: ZORLUK_SINIF.get(d, "easy")


def _statik_surum(yol: str) -> str:
    try:
        return str(int((STATIC_DIR / yol).stat().st_mtime))
    except OSError:
        return "0"


templates.env.globals["statik_surum"] = _statik_surum


def _baglam_dili(ctx) -> str:
    request = ctx.get("request")
    return i18n.dil(request) if request is not None else i18n.VARSAYILAN


@pass_context
def _cevir(ctx, metin: str, **degerler) -> str:
    return i18n.cevir(_baglam_dili(ctx), metin, **degerler)


@pass_context
def _aktif_dil(ctx) -> str:
    return _baglam_dili(ctx)


@pass_context
def _js_metinleri(ctx) -> dict[str, str]:
    return i18n.js_metinleri(_baglam_dili(ctx))


templates.env.globals["_"] = _cevir
templates.env.globals["aktif_dil"] = _aktif_dil
templates.env.globals["js_metinleri"] = _js_metinleri


def page(request, name: str, **context):
    context.setdefault("user", None)
    return templates.TemplateResponse(request, name, context)
