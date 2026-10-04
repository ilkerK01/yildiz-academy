(function () {
  if (!window.fetch || !window.DOMParser || !history.pushState) return;

  const HARIC = ["/static/", "/api/", "/dil/", "/academy/", "/admin"];

  function stilImzasi(belge) {
    return Array.from(belge.querySelectorAll('head link[rel="stylesheet"]'))
      .map(function (l) { return l.getAttribute("href"); })
      .join("|");
  }

  function uygunMu(url) {
    if (url.origin !== location.origin) return false;
    return !HARIC.some(function (on) { return url.pathname.startsWith(on); });
  }

  function betikleriCalistir(govde) {
    govde.querySelectorAll("script").forEach(function (eski) {
      const yeni = document.createElement("script");
      Array.from(eski.attributes).forEach(function (a) { yeni.setAttribute(a.name, a.value); });
      yeni.async = false;
      yeni.textContent = eski.textContent;
      eski.replaceWith(yeni);
    });
  }

  let sira = 0;

  async function git(adres, ekle, kaydirma) {
    const no = ++sira;
    let yanit, metin;
    try {
      yanit = await fetch(adres, { credentials: "same-origin", headers: { "X-Gecis": "1" } });
      metin = await yanit.text();
    } catch (_) {
      location.href = adres;
      return;
    }
    if (no !== sira) return;

    const tur = yanit.headers.get("content-type") || "";
    const belge = tur.includes("text/html") ? new DOMParser().parseFromString(metin, "text/html") : null;
    if (!belge || !belge.querySelector("script[data-gecis]") || stilImzasi(belge) !== stilImzasi(document)) {
      location.href = yanit.url || adres;
      return;
    }

    const varilan = new URL(yanit.url || adres, location.href);
    const hedef = new URL(adres, location.href);
    varilan.hash = hedef.hash;

    if (ekle) history.pushState({ gecis: true }, "", varilan.href);
    else if (varilan.href !== location.href) history.replaceState({ gecis: true }, "", varilan.href);

    document.title = belge.title;
    document.documentElement.lang = belge.documentElement.lang;
    const yeniGovde = document.adoptNode(belge.body);
    document.body.replaceWith(yeniGovde);
    betikleriCalistir(yeniGovde);

    if (typeof kaydirma === "number") {
      window.scrollTo(0, kaydirma);
    } else if (varilan.hash && document.getElementById(decodeURIComponent(varilan.hash.slice(1)))) {
      document.getElementById(decodeURIComponent(varilan.hash.slice(1))).scrollIntoView();
    } else {
      window.scrollTo(0, 0);
    }
  }

  window.sayfaYenile = function () {
    git(location.href, false, window.scrollY);
  };

  history.scrollRestoration = "manual";
  history.replaceState({ gecis: true }, "", location.href);

  document.addEventListener("click", function (olay) {
    if (olay.defaultPrevented || olay.button !== 0) return;
    if (olay.metaKey || olay.ctrlKey || olay.shiftKey || olay.altKey) return;
    const baglanti = olay.target.closest("a[href]");
    if (!baglanti || baglanti.target || baglanti.hasAttribute("download")) return;
    const ham = baglanti.getAttribute("href");
    if (!ham || ham.startsWith("#")) return;
    const url = new URL(baglanti.href, location.href);
    if (!uygunMu(url)) return;
    if (url.pathname === location.pathname && url.search === location.search && url.hash) return;
    olay.preventDefault();
    git(url.href, true);
  });

  document.addEventListener("submit", function (olay) {
    const form = olay.target;
    if (olay.defaultPrevented || (form.method || "get").toLowerCase() !== "get" || form.target) return;
    const url = new URL(form.action || location.href, location.href);
    if (!uygunMu(url)) return;
    url.search = new URLSearchParams(new FormData(form)).toString();
    olay.preventDefault();
    git(url.href, true);
  });

  window.addEventListener("popstate", function () {
    git(location.href, false);
  });
})();
