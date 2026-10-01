const okudumBtn = document.getElementById("okudum-btn");

if (okudumBtn) {
  okudumBtn.addEventListener("click", async function () {
    const { veri } = await apiPost("/api/ders/" + okudumBtn.dataset.slug + "/okudum");
    if (!veri.ok) {
      yaz("okudum-cikti", veri.hata || t("İşaretlenemedi."));
      return;
    }
    okudumBtn.disabled = true;
    okudumBtn.textContent = t("Okundu olarak işaretlendi");
    yaz("okudum-cikti", t("Toplam okunan ders: {n}", { n: veri.toplam_okunan }));
  });
}
