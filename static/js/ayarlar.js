async function adDegistir(event) {
  event.preventDefault();
  const { veri } = await apiPost("/api/ayarlar/ad", {
    gorunen_ad: document.getElementById("ad").value,
  });
  if (!veri.ok) {
    yaz("ad-cikti", veri.hata || "Değiştirilemedi.");
    return false;
  }
  yaz("ad-cikti", "Kaydedildi. Yeni adın: " + veri.gorunen_ad);
  return false;
}

async function parolaDegistir(event) {
  event.preventDefault();
  const { veri } = await apiPost("/api/ayarlar/parola", {
    mevcut: document.getElementById("mevcut").value,
    yeni: document.getElementById("yeni").value,
  });
  if (!veri.ok) {
    yaz("parola-cikti", veri.hata || "Değiştirilemedi.");
    return false;
  }
  document.getElementById("mevcut").value = "";
  document.getElementById("yeni").value = "";
  yaz("parola-cikti", "Parola değişti. Diğer oturumların kapatıldı.");
  return false;
}

(function gorunumKur() {
  const dugmeler = document.querySelectorAll("[data-tema-secim] .tema");
  const mevcut = document.documentElement.getAttribute("data-tema") || "gece";
  dugmeler.forEach(function (dugme) {
    dugme.setAttribute("aria-pressed", dugme.dataset.tema === mevcut ? "true" : "false");
    dugme.addEventListener("click", function () {
      temaUygula(dugme.dataset.tema);
      dugmeler.forEach(function (d) { d.setAttribute("aria-pressed", d === dugme ? "true" : "false"); });
    });
  });

  const anahtar = document.querySelector("[data-efekt-anahtar]");
  if (!anahtar) return;
  const acik = document.documentElement.getAttribute("data-efekt") !== "kapali";
  anahtar.setAttribute("aria-checked", acik ? "true" : "false");
  anahtar.addEventListener("click", function () {
    const yeni = anahtar.getAttribute("aria-checked") !== "true";
    anahtar.setAttribute("aria-checked", yeni ? "true" : "false");
    efektUygula(yeni);
  });
})();
