// Açılış sayfası hareketleri. Hepsi "hareketi azalt" tercihine uyar ve
// görünmeyen bölümde çalışmayı bırakır.
(function () {
  const AZ_HAREKET = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ALTIN = "224,188,106";

  // --- Gökyüzü: parıldayan yıldızlar, imlece yakın olanlar birbirine bağlanır ---
  function gokyuzu(tuval) {
    const ctx = tuval.getContext("2d");
    if (!ctx) return;
    let gen = 0, yuk = 0, oran = 1, yildizlar = [], kayan = null, sonrakiKayan = 0;
    const fare = { x: -9999, y: -9999, aktif: false };
    let calisiyor = false, kare = 0;

    function kur() {
      const kutu = tuval.getBoundingClientRect();
      oran = Math.min(window.devicePixelRatio || 1, 2);
      gen = kutu.width;
      yuk = kutu.height;
      tuval.width = Math.round(gen * oran);
      tuval.height = Math.round(yuk * oran);
      ctx.setTransform(oran, 0, 0, oran, 0, 0);
      const adet = Math.min(220, Math.round((gen * yuk) / 7000));
      yildizlar = [];
      for (let i = 0; i < adet; i++) {
        const derinlik = Math.random();
        yildizlar.push({
          x: Math.random() * gen,
          y: Math.random() * yuk,
          r: 0.4 + derinlik * 1.3,
          a: 0.25 + Math.random() * 0.55,
          faz: Math.random() * Math.PI * 2,
          hiz: 0.6 + Math.random() * 1.6,
          d: derinlik,
          kx: 0, ky: 0,
        });
      }
    }

    function ciz(zaman) {
      const t = zaman / 1000;
      ctx.clearRect(0, 0, gen, yuk);

      // Fare hafif paralaks verir: yakın (büyük) yıldızlar daha çok kayar.
      const px = fare.aktif ? (fare.x / gen - 0.5) : 0;
      const py = fare.aktif ? (fare.y / yuk - 0.5) : 0;
      const yakinlar = [];

      for (const y of yildizlar) {
        y.kx += ((-px * 18 * y.d) - y.kx) * 0.06;
        y.ky += ((-py * 12 * y.d) - y.ky) * 0.06;
        const x = y.x + y.kx, yy = y.y + y.ky;
        const parilti = AZ_HAREKET ? 1 : 0.65 + 0.35 * Math.sin(t * y.hiz + y.faz);
        ctx.beginPath();
        ctx.arc(x, yy, y.r, 0, Math.PI * 2);
        ctx.fillStyle = "rgba(255,255,255," + (y.a * parilti).toFixed(3) + ")";
        ctx.fill();
        if (fare.aktif) {
          const dx = x - fare.x, dy = yy - fare.y;
          const uzak = dx * dx + dy * dy;
          if (uzak < 170 * 170) yakinlar.push({ x: x, y: yy, u: Math.sqrt(uzak) });
        }
      }

      // Takımyıldız: imlece yakın yıldızlar arasında altın çizgiler.
      if (yakinlar.length > 1) {
        ctx.lineWidth = 0.8;
        for (let i = 0; i < yakinlar.length; i++) {
          const a = yakinlar[i];
          for (let j = i + 1; j < yakinlar.length; j++) {
            const b = yakinlar[j];
            const dx = a.x - b.x, dy = a.y - b.y;
            const m = Math.sqrt(dx * dx + dy * dy);
            if (m > 95) continue;
            const g = (1 - m / 95) * (1 - Math.max(a.u, b.u) / 170);
            ctx.strokeStyle = "rgba(" + ALTIN + "," + (g * 0.75).toFixed(3) + ")";
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
          ctx.beginPath();
          ctx.arc(a.x, a.y, 1.6, 0, Math.PI * 2);
          ctx.fillStyle = "rgba(" + ALTIN + "," + (0.9 * (1 - a.u / 170)).toFixed(3) + ")";
          ctx.fill();
        }
      }

      // Arada bir kayan yıldız; seyrek tutulur.
      if (!AZ_HAREKET) {
        if (!kayan && t > sonrakiKayan) {
          kayan = { x: Math.random() * gen * 0.7, y: Math.random() * yuk * 0.35, bas: t };
          sonrakiKayan = t + 7 + Math.random() * 9;
        }
        if (kayan) {
          const s = (t - kayan.bas) / 1.1;
          if (s >= 1) {
            kayan = null;
          } else {
            const x = kayan.x + s * 260, y = kayan.y + s * 120;
            const iz = ctx.createLinearGradient(x - 90, y - 42, x, y);
            iz.addColorStop(0, "rgba(255,255,255,0)");
            iz.addColorStop(1, "rgba(255,255,255," + (0.8 * Math.sin(s * Math.PI)).toFixed(3) + ")");
            ctx.strokeStyle = iz;
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(x - 90, y - 42);
            ctx.lineTo(x, y);
            ctx.stroke();
          }
        }
      }
    }

    function dongu(zaman) {
      if (!calisiyor) return;
      ciz(zaman);
      kare = requestAnimationFrame(dongu);
    }
    function baslat() {
      if (calisiyor || AZ_HAREKET) return;
      calisiyor = true;
      kare = requestAnimationFrame(dongu);
    }
    function durdur() {
      calisiyor = false;
      cancelAnimationFrame(kare);
    }

    kur();
    sonrakiKayan = 3;
    if (AZ_HAREKET) ciz(0);

    const kapsayan = tuval.parentElement;
    kapsayan.addEventListener("pointermove", function (olay) {
      if (olay.pointerType === "touch") return;
      const kutu = tuval.getBoundingClientRect();
      fare.x = olay.clientX - kutu.left;
      fare.y = olay.clientY - kutu.top;
      fare.aktif = true;
      if (AZ_HAREKET) ciz(0);
    });
    kapsayan.addEventListener("pointerleave", function () {
      fare.aktif = false;
      if (AZ_HAREKET) ciz(0);
    });

    let zamanlayici = 0;
    window.addEventListener("resize", function () {
      clearTimeout(zamanlayici);
      zamanlayici = setTimeout(function () { kur(); if (AZ_HAREKET) ciz(0); }, 150);
    });

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (girisler) {
        girisler.forEach(function (g) { g.isIntersecting ? baslat() : durdur(); });
      }).observe(tuval);
    } else {
      baslat();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) durdur();
      else if (tuval.getBoundingClientRect().bottom > 0) baslat();
    });
  }

  document.querySelectorAll("[data-gokyuzu]").forEach(gokyuzu);

  // --- Başlık harf harf belirir ---
  document.querySelectorAll("[data-harfler]").forEach(function (baslik) {
    const metin = baslik.textContent.trim();
    baslik.setAttribute("aria-label", metin);
    baslik.textContent = "";
    Array.from(metin).forEach(function (harf, i) {
      const s = document.createElement("span");
      s.className = "harf";
      s.setAttribute("aria-hidden", "true");
      s.style.setProperty("--i", i);
      s.textContent = harf === " " ? " " : harf;
      baslik.appendChild(s);
    });
    baslik.classList.add("is-hazir");
  });

  // --- Terminal satırı: örnek pivotlar yazılıp silinir ---
  document.querySelectorAll("[data-yaz]").forEach(function (el) {
    let satirlar;
    try { satirlar = JSON.parse(el.getAttribute("data-yaz")); } catch (_) { return; }
    if (!satirlar.length) return;
    if (AZ_HAREKET) { el.textContent = satirlar[satirlar.length - 1]; return; }
    let i = 0, n = 0, siliyor = false;
    function adim() {
      const satir = satirlar[i];
      if (!siliyor) {
        n++;
        el.textContent = satir.slice(0, n);
        if (n >= satir.length) { siliyor = true; return setTimeout(adim, 2200); }
        return setTimeout(adim, 38 + Math.random() * 50);
      }
      n -= 2;
      el.textContent = satir.slice(0, Math.max(n, 0));
      if (n <= 0) { siliyor = false; n = 0; i = (i + 1) % satirlar.length; return setTimeout(adim, 420); }
      return setTimeout(adim, 18);
    }
    setTimeout(adim, 1500);
  });

  // --- Sayaçlar ekrana girince sıfırdan sayar ---
  const sayaclar = document.querySelectorAll("[data-say]");
  function say(el) {
    const hedef = parseInt(el.getAttribute("data-say"), 10) || 0;
    if (AZ_HAREKET || hedef === 0) { el.textContent = hedef; return; }
    const sure = 1400, bas = performance.now();
    function kare(simdi) {
      const s = Math.min(1, (simdi - bas) / sure);
      el.textContent = Math.round(hedef * (1 - Math.pow(1 - s, 3)));
      if (s < 1) requestAnimationFrame(kare);
    }
    requestAnimationFrame(kare);
  }
  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(function (girisler) {
      girisler.forEach(function (g) {
        if (!g.isIntersecting) return;
        say(g.target);
        io.unobserve(g.target);
      });
    }, { threshold: 0.6 });
    sayaclar.forEach(function (el) { el.textContent = "0"; io.observe(el); });
  }

  // --- "Bir iz, üç adım": aşağı kaydırdıkça adımları bağlayan çizgi dolar ---
  const yol = document.querySelector("[data-yol]");
  if (yol) {
    const adimlar = yol.querySelectorAll(".yol__adim");
    let bekliyor = false;
    function guncelle() {
      bekliyor = false;
      const kutu = yol.getBoundingClientRect();
      const ekran = window.innerHeight;
      // Bölümün üstü ekranın %85'ine geldiğinde başlar, %35'ine geldiğinde biter.
      const ilerleme = Math.min(1, Math.max(0, (ekran * 0.85 - kutu.top) / (ekran * 0.5)));
      yol.style.setProperty("--ilerleme", AZ_HAREKET ? 1 : ilerleme.toFixed(3));
      adimlar.forEach(function (adim, i) {
        adim.classList.toggle("is-yandi", AZ_HAREKET || ilerleme >= i / Math.max(1, adimlar.length - 1) - 0.02);
      });
    }
    window.addEventListener("scroll", function () {
      if (!bekliyor) { bekliyor = true; requestAnimationFrame(guncelle); }
    }, { passive: true });
    guncelle();
  }

  // --- Kartlarda imleci izleyen yumuşak ışık ---
  document.querySelectorAll("[data-isik]").forEach(function (kart) {
    kart.addEventListener("pointermove", function (olay) {
      const kutu = kart.getBoundingClientRect();
      kart.style.setProperty("--mx", (olay.clientX - kutu.left) + "px");
      kart.style.setProperty("--my", (olay.clientY - kutu.top) + "px");
    });
  });
})();
