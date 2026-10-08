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

// Sayfadaki tüm avatarları (menü, önizleme) aynı görsele çevirir; url boşsa baş harfe döner.
function avatarlariGuncelle(url) {
  document.querySelectorAll("[data-avatar]").forEach(function (el) {
    el.textContent = "";
    if (url) {
      const img = document.createElement("img");
      img.src = url;
      img.alt = "";
      el.appendChild(img);
      el.classList.add("avatar--foto");
    } else {
      el.textContent = el.dataset.harf;
      el.classList.remove("avatar--foto");
    }
  });
}

async function avatarYukle(event) {
  event.preventDefault();
  const girdi = document.getElementById("avatar-dosya");
  if (!girdi.files.length) {
    yaz("avatar-cikti", t("Bir görsel seç."));
    return false;
  }
  const govde = new FormData();
  govde.append("dosya", girdi.files[0]);
  const dugme = event.target.querySelector("button[type=submit]");
  dugme.disabled = true;
  yaz("avatar-cikti", t("Yükleniyor..."));
  let veri = {};
  try {
    const yanit = await fetch("/api/ayarlar/avatar", { method: "POST", body: govde });
    veri = await yanit.json();
  } catch (_) {
    veri = { ok: false, hata: t("Sunucu yanıtı okunamadı.") };
  }
  dugme.disabled = false;
  if (!veri.ok) {
    yaz("avatar-cikti", veri.hata || t("Yüklenemedi."));
    return false;
  }
  avatarlariGuncelle(veri.url);
  girdi.value = "";
  document.querySelector("[data-avatar-ad]").textContent = t("Görsel seç ya da buraya sürükle");
  document.querySelector("[data-avatar-kaldir]").hidden = false;
  yaz("avatar-cikti", t("Profil fotoğrafın güncellendi."));
  return false;
}

async function avatarKaldir() {
  const { veri } = await apiPost("/api/ayarlar/avatar/sil");
  if (!veri.ok) {
    yaz("avatar-cikti", veri.hata || t("Değiştirilemedi."));
    return;
  }
  avatarlariGuncelle(null);
  document.querySelector("[data-avatar-kaldir]").hidden = true;
  yaz("avatar-cikti", t("Profil fotoğrafı kaldırıldı."));
}

(function avatarSeciciKur() {
  const girdi = document.getElementById("avatar-dosya");
  const secici = document.querySelector(".avatar-yukle__secici");
  if (!girdi || !secici) return;
  const onizleme = document.querySelector(".avatar-yukle__onizleme [data-avatar]");

  function goster() {
    const dosya = girdi.files[0];
    if (!dosya) return;
    document.querySelector("[data-avatar-ad]").textContent = dosya.name;
    // Yüklemeden önce yalnızca önizleme kutusunda yerel görsel gösterilir.
    if (onizleme) {
      onizleme.textContent = "";
      const img = document.createElement("img");
      img.src = URL.createObjectURL(dosya);
      img.alt = "";
      onizleme.appendChild(img);
      onizleme.classList.add("avatar--foto");
    }
  }

  girdi.addEventListener("change", goster);
  ["dragenter", "dragover"].forEach(function (tur) {
    secici.addEventListener(tur, function (olay) {
      olay.preventDefault();
      secici.setAttribute("data-surukle", "1");
    });
  });
  ["dragleave", "drop"].forEach(function (tur) {
    secici.addEventListener(tur, function () { secici.removeAttribute("data-surukle"); });
  });
  secici.addEventListener("drop", function (olay) {
    olay.preventDefault();
    if (!olay.dataTransfer.files.length) return;
    girdi.files = olay.dataTransfer.files;
    goster();
  });
})();

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
