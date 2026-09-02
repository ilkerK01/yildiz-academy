const okudumBtn = document.getElementById("okudum-btn");

if (okudumBtn) {
  okudumBtn.addEventListener("click", async function () {
    const { veri } = await apiPost("/api/ders/" + okudumBtn.dataset.slug + "/okudum");
    if (!veri.ok) {
      yaz("okudum-cikti", veri.hata || "İşaretlenemedi.");
      return;
    }
    okudumBtn.disabled = true;
    okudumBtn.textContent = "Okundu olarak işaretlendi";
    yaz("okudum-cikti", "Toplam okunan ders: " + veri.toplam_okunan);
  });
}
