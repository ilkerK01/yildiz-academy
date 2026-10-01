async function adDegistir(event) {
  event.preventDefault();
  const { veri } = await apiPost("/api/ayarlar/ad", {
    gorunen_ad: document.getElementById("ad").value,
  });
  if (!veri.ok) {
    yaz("ad-cikti", veri.hata || t("Değiştirilemedi."));
    return false;
  }
  yaz("ad-cikti", t("Kaydedildi. Yeni adın: {ad}", { ad: veri.gorunen_ad }));
  return false;
}

async function parolaDegistir(event) {
  event.preventDefault();
  const { veri } = await apiPost("/api/ayarlar/parola", {
    mevcut: document.getElementById("mevcut").value,
    yeni: document.getElementById("yeni").value,
  });
  if (!veri.ok) {
    yaz("parola-cikti", veri.hata || t("Değiştirilemedi."));
    return false;
  }
  document.getElementById("mevcut").value = "";
  document.getElementById("yeni").value = "";
  yaz("parola-cikti", t("Parola değişti. Diğer oturumların kapatıldı."));
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
})();
