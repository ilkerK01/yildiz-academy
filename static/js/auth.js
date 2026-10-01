function ac(id) {
  const hedef = typeof id === "string" ? document.getElementById(id) : id;
  if (!hedef) return;
  document.querySelectorAll("dialog.modal[open]").forEach(function (acik) {
    if (acik !== hedef) acik.close();
  });
  if (!hedef.open) hedef.showModal();
  const ilk = hedef.querySelector("input");
  if (ilk) setTimeout(function () { ilk.focus(); }, 60);
}
function kayitAc() { ac("modal-kayit"); }
function girisAc() { ac("modal-giris"); }

function hataGoster(id, mesaj) {
  const kutu = document.getElementById(id);
  if (!kutu) return;
  kutu.textContent = mesaj || "";
  kutu.hidden = !mesaj;
}

function nereye(varsayilan) {
  const istenen = window.SONRAKI;
  if (istenen && istenen.startsWith("/") && !istenen.startsWith("//") && !/[\\\x00-\x1f\x7f]/.test(istenen)) {
    try {
      const hedef = new URL(istenen, window.location.origin);
      if (hedef.origin === window.location.origin) return hedef.pathname + hedef.search + hedef.hash;
    } catch (_) {}
  }
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
    hataGoster("k-hata", veri.hata || t("Kayıt tamamlanamadı."));
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
    hataGoster("g-hata", veri.hata || t("Giriş yapılamadı."));
    return false;
  }
  window.location.href = nereye(veri.next);
  return false;
}

async function unuttumGonder(event) {
  event.preventDefault();
  hataGoster("u-hata", "");
  const tamam = document.getElementById("u-tamam");
  tamam.hidden = true;
  const dugme = document.getElementById("u-gonder");
  dugme.disabled = true;
  const { veri } = await apiPost("/api/sifremi-unuttum", {
    eposta: document.getElementById("u-eposta").value,
  });
  dugme.disabled = false;
  if (!veri.ok) {
    hataGoster("u-hata", veri.hata || t("Bağlantı gönderilemedi."));
    return false;
  }
  tamam.textContent = veri.mesaj;
  tamam.hidden = false;
  return false;
}

async function sifirlaGonder(event) {
  event.preventDefault();
  hataGoster("s-hata", "");
  const parola = document.getElementById("s-parola").value;
  if (parola !== document.getElementById("s-tekrar").value) {
    hataGoster("s-hata", t("Parolalar eşleşmiyor."));
    return false;
  }
  const { veri } = await apiPost("/api/sifre-sifirla", { token: window.SIFIRLA, yeni: parola });
  if (!veri.ok) {
    hataGoster("s-hata", veri.hata || t("Parola kaydedilemedi."));
    return false;
  }
  window.SIFIRLA = "";
  history.replaceState(null, "", "/");
  girisAc();
  const not = document.getElementById("g-tamam");
  not.textContent = t("Parolan değişti. Yeni parolanla giriş yapabilirsin.");
  not.hidden = false;
  return false;
}

document.querySelectorAll('a[href="#kayit"]').forEach(function (baglanti) {
  baglanti.addEventListener("click", function (event) { event.preventDefault(); kayitAc(); });
});
document.querySelectorAll('a[href="#giris"]').forEach(function (baglanti) {
  baglanti.addEventListener("click", function (event) { event.preventDefault(); girisAc(); });
});
document.querySelectorAll("[data-kapat]").forEach(function (dugme) {
  dugme.addEventListener("click", function () { dugme.closest("dialog").close(); });
});
document.querySelectorAll("[data-gec]").forEach(function (dugme) {
  dugme.addEventListener("click", function () { ac(dugme.dataset.gec); });
});
document.querySelectorAll("dialog.modal").forEach(function (kutu) {
  kutu.addEventListener("click", function (event) {
    if (event.target === kutu) kutu.close();
  });
});

(function reveal() {
  const ogeler = document.querySelectorAll(".reveal");
  if (!("IntersectionObserver" in window) ||
      window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    ogeler.forEach(function (el) { el.classList.add("is-in"); });
    return;
  }
  const io = new IntersectionObserver(function (girisler) {
    girisler.forEach(function (e) {
      if (!e.isIntersecting) return;
      const grup = e.target.parentElement;
      const kardesler = grup ? Array.prototype.filter.call(grup.children, function (c) {
        return c.classList.contains("reveal");
      }) : [];
      const i = kardesler.indexOf(e.target);
      e.target.style.setProperty("--d", (i > 0 ? i * 280 : 0) + "ms");
      e.target.classList.add("is-in");
      io.unobserve(e.target);
    });
  }, { threshold: 0.16, rootMargin: "0px 0px -8% 0px" });
  ogeler.forEach(function (el) { io.observe(el); });
})();

if (window.SIFIRLA) ac("modal-sifirla");
else if (window.SONRAKI) girisAc();
if (window.location.hash === "#kayit") kayitAc();
