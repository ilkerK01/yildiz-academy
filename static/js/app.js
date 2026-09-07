async function apiPost(url, govde) {
  const yanit = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(govde || {}),
  });
  let veri = {};
  try {
    veri = await yanit.json();
  } catch (_) {
    veri = { ok: false, hata: "Sunucu yanıtı okunamadı." };
  }
  return { durum: yanit.status, veri: veri };
}

function yaz(hedef, metin, sinif) {
  const el = typeof hedef === "string" ? document.getElementById(hedef) : hedef;
  if (!el) return;
  el.textContent = metin || "";
  el.className = "cikti" + (sinif ? " " + sinif : "");
}

async function cikisYap(event) {
  if (event) event.preventDefault();
  await apiPost("/api/cikis");
  window.location.href = "/";
}

function temaUygula(tema) {
  document.documentElement.setAttribute("data-tema", tema);
  try { localStorage.setItem("ya-tema", tema); } catch (_) {}
}

function efektUygula(acik) {
  const deger = acik ? "acik" : "kapali";
  document.documentElement.setAttribute("data-efekt", deger);
  try { localStorage.setItem("ya-efekt", deger); } catch (_) {}
}

(function paketleriKur() {
  const kutu = document.querySelector("[data-packets]");
  if (!kutu) return;
  const renkler = ["var(--acc)", "#3ddc84", "#60a5fa", "#f472b6"];
  for (let i = 0; i < 22; i++) {
    const nokta = document.createElement("span");
    const renk = renkler[i % 4];
    nokta.style.left = ((i * 37) % 100) + "%";
    nokta.style.background = renk;
    nokta.style.boxShadow = "0 0 8px " + renk;
    nokta.style.setProperty("--dur", (14 + ((i * 7) % 12)) + "s");
    nokta.style.setProperty("--delay", -(i * 1.3) + "s");
    kutu.appendChild(nokta);
  }
})();

(function menuGenisligi() {
  const EN_AZ = 180, EN_COK = 420, VARSAYILAN = 220;

  function uygula(px, kaydet) {
    const deger = Math.min(EN_COK, Math.max(EN_AZ, Math.round(px)));
    document.documentElement.style.setProperty("--side-w", deger + "px");
    if (kaydet) {
      try { localStorage.setItem("ya-side-w", String(deger)); } catch (_) {}
    }
    return deger;
  }

  try {
    const kayitli = parseInt(localStorage.getItem("ya-side-w"), 10);
    if (kayitli) uygula(kayitli, false);
  } catch (_) {}

  const tutamac = document.querySelector("[data-side-resize]");
  const menu = document.querySelector(".side");
  if (!tutamac || !menu) return;

  let suruklerken = false;

  tutamac.addEventListener("pointerdown", function (olay) {
    if (window.matchMedia("(max-width:900px)").matches) return;
    olay.preventDefault();
    suruklerken = true;
    tutamac.setPointerCapture(olay.pointerId);
    document.body.setAttribute("data-side-suruk", "1");
  });

  tutamac.addEventListener("pointermove", function (olay) {
    if (!suruklerken) return;
    uygula(olay.clientX - menu.getBoundingClientRect().left, false);
  });

  function birak(olay) {
    if (!suruklerken) return;
    suruklerken = false;
    try { tutamac.releasePointerCapture(olay.pointerId); } catch (_) {}
    document.body.removeAttribute("data-side-suruk");
    uygula(menu.getBoundingClientRect().width, true);
  }
  tutamac.addEventListener("pointerup", birak);
  tutamac.addEventListener("pointercancel", birak);

  tutamac.addEventListener("dblclick", function () {
    uygula(VARSAYILAN, true);
  });

  tutamac.addEventListener("keydown", function (olay) {
    const adim = olay.shiftKey ? 24 : 8;
    const su_an = menu.getBoundingClientRect().width;
    if (olay.key === "ArrowLeft") { olay.preventDefault(); uygula(su_an - adim, true); }
    if (olay.key === "ArrowRight") { olay.preventDefault(); uygula(su_an + adim, true); }
  });
})();
