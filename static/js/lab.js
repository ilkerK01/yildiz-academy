const LAB_SLUG = document.getElementById("adimlar").dataset.slug;

function adimEl(index) {
  return document.getElementById("adim-" + index);
}

async function cevapGonder(event, index) {
  event.preventDefault();
  const form = event.target;
  const alan = form.querySelector("[name=cevap]");
  const cikti = adimEl(index).querySelector("[data-cikti]");

  const { veri } = await apiPost(
    "/api/lab/" + LAB_SLUG + "/adim/" + index + "/cevap",
    { cevap: alan.value }
  );

  if (veri.hata) {
    yaz(cikti, veri.hata);
    return false;
  }

  if (!veri.dogru) {
    yaz(cikti, veri.mesaj + " " + t("({n}. deneme)", { n: veri.deneme }));
    return false;
  }

  if (veri.lab_bitti) {
    const cozum = document.getElementById("cozum");
    document.getElementById("cozum-govde").innerHTML = veri.cozum_html || "";
    cozum.hidden = false;
    cozum.scrollIntoView({ behavior: "smooth" });
  }
  window.location.reload();
  return false;
}

async function ipucuAc(index) {
  const { veri } = await apiPost(
    "/api/lab/" + LAB_SLUG + "/adim/" + index + "/ipucu"
  );
  if (!veri.ok) {
    yaz(adimEl(index).querySelector("[data-cikti]"), veri.hata || t("İpucu açılamadı."));
    return;
  }
  const kutu = adimEl(index).querySelector("[data-ipuclari]");
  const satir = document.createElement("div");
  satir.className = "hintrow";
  satir.innerHTML = veri.ipucu_html;
  kutu.appendChild(satir);

  const puan = adimEl(index).querySelector("[data-puan]");
  if (puan) puan.textContent = t("{n} puan (ipucu düştü)", { n: veri.yeni_puan });

  const sayac = document.querySelector("[data-ipucu-sayac]");
  if (sayac) sayac.textContent = String(Number(sayac.textContent) + 1);

  if (veri.kalan_ipucu === 0) {
    const dugme = adimEl(index).querySelector("button[onclick^='ipucuAc']");
    if (dugme) dugme.remove();
  }
}

async function pesEt() {
  if (!confirm(t("Çözümü açarsan bu labdan bir daha puan kazanamazsın. Emin misin?"))) {
    return;
  }
  const { veri } = await apiPost("/api/lab/" + LAB_SLUG + "/pes");
  if (!veri.ok) return;
  document.getElementById("cozum-govde").innerHTML = veri.cozum_html || "";
  document.getElementById("cozum").hidden = false;
  window.location.reload();
}

async function labSifirla() {
  if (!confirm(t("Bu labın ilerlemesi silinecek. En iyi puanın korunur. Devam edilsin mi?"))) return;
  const { veri } = await apiPost("/api/lab/" + LAB_SLUG + "/sifirla");
  if (veri.mesaj) alert(veri.mesaj);
  window.location.reload();
}
