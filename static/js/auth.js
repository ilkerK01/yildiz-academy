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

if (window.SONRAKI) girisAc();
if (window.location.hash === "#kayit") kayitAc();
