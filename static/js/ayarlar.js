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
