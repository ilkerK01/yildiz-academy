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
