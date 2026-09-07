from __future__ import annotations

from fastapi.templating import Jinja2Templates

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


def page(request, name: str, **context):
    context.setdefault("user", None)
    return templates.TemplateResponse(request, name, context)
