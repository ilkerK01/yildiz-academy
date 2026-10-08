from __future__ import annotations

import hashlib
import io
import re
import zipfile
from html import unescape
from pathlib import Path
from xml.etree import ElementTree

import mammoth
import yaml
from sqlalchemy import func, select
from sqlalchemy.orm import Session as DbSession

from app import config
from app.models import Lesson
from app.services.ingest import IngestError, slugify

# Word belgesini ders kaynağına (frontmatter + HTML gövde) çevirir.
# Gövde HTML olarak kalır; markdown işleyicisi HTML bloğunu olduğu gibi
# geçirir, ardından bleach ile temizlenir.
#
# Bilgiler belgenin özelliklerinden okunur (Word: Dosya > Bilgi > Özellikler):
#   Başlık   -> title (yoksa ilk "Başlık 1", o da yoksa dosya adı)
#   Konu     -> summary (yoksa Açıklama)
#   Etiketler-> tags (virgülle ayrılmış)
# Dosya adı slug olur. `slug.en.docx` ya da `en/` klasöründeki dosya
# mevcut dersin İngilizce çevirisi sayılır.

_STIL = """
p[style-name='Title'] => h1:fresh
p[style-name='Subtitle'] => p:fresh
p[style-name='Quote'] => blockquote > p:fresh
p[style-name='Intense Quote'] => blockquote > p:fresh
p[style-name='Code'] => pre:separator('\\n')
r[style-name='Code Char'] => code
"""

_GORSEL_TURLERI = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/gif": ".gif",
    "image/webp": ".webp",
}

_NS = {
    "dc": "http://purl.org/dc/elements/1.1/",
    "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
}


def gorsel_klasoru() -> Path:
    yol = config.MEDIA_DIR / "gorsel"
    yol.mkdir(parents=True, exist_ok=True)
    return yol


def _ozellikler(veri: bytes) -> dict[str, str]:
    try:
        with zipfile.ZipFile(io.BytesIO(veri)) as z:
            if "docProps/core.xml" not in z.namelist():
                return {}
            kok = ElementTree.fromstring(z.read("docProps/core.xml"))
    except (zipfile.BadZipFile, ElementTree.ParseError, KeyError):
        return {}

    def oku(etiket: str) -> str:
        dugum = kok.find(etiket, _NS)
        return (dugum.text or "").strip() if dugum is not None else ""

    return {
        "title": oku("dc:title"),
        "subject": oku("dc:subject"),
        "description": oku("dc:description"),
        "keywords": oku("cp:keywords"),
    }


def _metin(html: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def donustur(db: DbSession, dosya_adi: str, veri: bytes, *, ingilizce: bool = False):
    """(ders dosya adı, ders metni, bilgi satırları) döner."""
    if not zipfile.is_zipfile(io.BytesIO(veri)):
        raise IngestError(f"{dosya_adi}: geçerli bir Word (.docx) belgesi değil.")

    gok = Path(dosya_adi).name
    gok = gok[: -len(".docx")] if gok.lower().endswith(".docx") else gok
    if gok.lower().endswith(".en"):
        gok, ingilizce = gok[:-3], True
    slug = slugify(gok)
    if not slug:
        raise IngestError(f"{dosya_adi}: dosya adından slug çıkarılamadı.")

    atlanan: list[str] = []
    kaydedilen = 0

    def gorsel(resim):
        nonlocal kaydedilen
        uzanti = _GORSEL_TURLERI.get(resim.content_type)
        if uzanti is None:
            atlanan.append(resim.content_type or "bilinmiyor")
            return {}
        with resim.open() as akis:
            icerik = akis.read()
        ad = hashlib.sha256(icerik).hexdigest()[:20] + uzanti
        hedef = gorsel_klasoru() / ad
        if not hedef.exists():
            hedef.write_bytes(icerik)
        kaydedilen += 1
        return {"src": f"/medya/gorsel/{ad}", "alt": resim.alt_text or ""}

    try:
        sonuc = mammoth.convert_to_html(
            io.BytesIO(veri),
            style_map=_STIL,
            convert_image=mammoth.images.img_element(gorsel),
        )
    except Exception as exc:  # bozuk ya da desteklenmeyen belge
        raise IngestError(f"{dosya_adi}: belge okunamadı. {exc}") from exc

    html = sonuc.value.strip()
    if not _metin(html):
        raise IngestError(f"{dosya_adi}: belgede metin yok.")

    ozellik = _ozellikler(veri)
    baslik = ozellik.get("title", "")
    ilk_h1 = re.match(r"\s*<h1[^>]*>(.*?)</h1>", html, re.DOTALL)
    if ilk_h1 and (not baslik or _metin(ilk_h1.group(1)) == baslik):
        # Başlık sayfanın üstünde zaten gösteriliyor, gövdede tekrar etmesin.
        baslik = baslik or _metin(ilk_h1.group(1))
        html = html[ilk_h1.end():].lstrip()
    baslik = baslik or gok.replace("-", " ").strip()

    meta: dict = {"title": baslik, "slug": slug}
    ozet = ozellik.get("subject") or ozellik.get("description")
    if ozet:
        meta["summary"] = ozet
    if ingilizce:
        meta = {"lang": "en", **meta}
    else:
        etiketler = [e.strip() for e in re.split(r"[,;]", ozellik.get("keywords", "")) if e.strip()]
        if etiketler:
            meta["tags"] = etiketler
        mevcut = db.scalar(select(Lesson).where(Lesson.slug == slug))
        if mevcut is not None:
            meta["order_index"] = mevcut.order_index
            meta["published"] = mevcut.published
        else:
            son = db.scalar(select(func.max(Lesson.order_index))) or 0
            meta["order_index"] = son + 1

    # Gövdeyi tek bir HTML bloğu olarak tut: içinde boş satır olmamalı.
    govde = re.sub(r"\n\s*\n", "\n", html)
    metin = "---\n" + yaml.safe_dump(meta, allow_unicode=True, sort_keys=False) + "---\n\n" + govde + "\n"

    bilgi = ["Kaynak: Word belgesi"]
    if kaydedilen:
        bilgi.append(f"Görsel: {kaydedilen}")
    if atlanan:
        bilgi.append(
            "Atlanan görsel (desteklenmeyen biçim, PNG/JPG kullan): " + ", ".join(sorted(set(atlanan)))
        )
    if not ozellik.get("title") and not ilk_h1:
        bilgi.append("Uyarı: belgede başlık bulunamadı, dosya adı kullanıldı.")
    ad = f"{slug}.en.md" if ingilizce else f"{slug}.md"
    return ad, metin, bilgi
