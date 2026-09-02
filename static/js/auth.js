function ac(id) {
  const dlg = document.getElementById(id);
  if (dlg && !dlg.open) dlg.showModal();
}
function kapat(id) {
  const dlg = document.getElementById(id);
  if (dlg && dlg.open) dlg.close();
}
function kayitAc() { ac("dlg-kayit"); }
function girisAc() { ac("dlg-giris"); }

function hataGoster(id, mesaj) {
  const kutu = document.getElementById(id);
  if (!kutu) return;
  kutu.textContent = mesaj || "";
  kutu.hidden = !mesaj;
}

function nereye(varsayilan) {
  const istenen = window.SONRAKI;
  if (istenen && istenen.startsWith("/") && !istenen.startsWith("//")) return istenen;
  return varsayilan || "/panel";
}

async function kayitGonder(event) {
  event.preventDefault();
  hataGoster("k-hata", "");
  const { veri } = await apiPost("/api/kayit", {
    gorunen_ad: document.getElementById("k-ad").value,
    eposta: document.getElementById("k-eposta").value,
    parola: document.getElementById("k-parola").value,
  });
  if (!veri.ok) {
    hataGoster("k-hata", veri.hata || "Kayıt tamamlanamadı.");
    return false;
  }
  window.location.href = nereye(veri.next);
  return false;
}

async function girisGonder(event) {
  event.preventDefault();
  hataGoster("g-hata", "");
  const { veri } = await apiPost("/api/giris", {
    eposta: document.getElementById("g-eposta").value,
    parola: document.getElementById("g-parola").value,
  });
  if (!veri.ok) {
    hataGoster("g-hata", veri.hata || "Giriş yapılamadı.");
    return false;
  }
  window.location.href = nereye(veri.next);
  return false;
}

if (window.SONRAKI) girisAc();
