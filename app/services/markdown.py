from __future__ import annotations

import bleach
from markdown_it import MarkdownIt

_md = MarkdownIt("commonmark", {"linkify": True, "typographer": False}).enable(
    ["table", "strikethrough"]
)

ALLOWED_TAGS = {
    "p", "br", "hr",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "strong", "em", "del", "code", "pre", "blockquote", "sup", "sub", "u",
    "ul", "ol", "li",
    "a", "img",
    "table", "thead", "tbody", "tr", "th", "td",
}

ALLOWED_ATTRS = {
    "a": ["href", "title", "rel", "target"],
    "img": ["src", "alt", "title"],
    "code": ["class"],
    "th": ["align"],
    "td": ["align"],
}


def render(md_text: str | None) -> str:
    if not md_text:
        return ""
    raw = _md.render(md_text)
    clean = bleach.clean(
        raw,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=["http", "https", "mailto"],
        strip=True,
    )
    return bleach.linkify(clean, callbacks=[_external_link])


def _external_link(attrs, new=False):
    href = attrs.get((None, "href"), "")
    if href.startswith("http"):
        attrs[(None, "rel")] = "noopener noreferrer"
        attrs[(None, "target")] = "_blank"
    return attrs
