# Yıldız Academy

Siber tehdit istihbaratı öğrenmek isteyenler için kapalı bir akademi. İki yarısı
var. Kütüphanede kısa dersler duruyor; laboratuvarda ise gerçek bir iz veriliyor
(bir hash, bir onion gönderisi, bir takma ad), araştırmayı kullanıcı kendi
makinesinde yapıyor, bulduğu cevabı siteye yazıyor.

Kayıt olmadan görülebilen tek yer açılış sayfasıdır. Geri kalan her şey giriş
arkasında.

![Açılış sayfası](ekran/hero.jpg)

Panel kişiseldir: sayaçlar, sıralamadaki yerin ve kazanılmış mühürler. Ders ve
lab listeleri buraya değil, kendi sayfalarına ait. Aşağıdaki görüntüdeki isimler
ve puanlar örnek veridir.

![Panel](ekran/panel.jpg)

## Yığın

FastAPI · Jinja2 · SQLAlchemy 2 · SQLite · Argon2id · Vanilla JS

Node çalışma zamanı bağımlılığı yoktur. `static/css/tokens.css` dosyası
`design/tokens.json` içinden üretilmiştir ama üreteç depoda değil; token
değişirse şu an CSS'i elle güncellemek gerekiyor.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
python seed.py
```

`.env` içinde parola yoktur. Yönetici hesabı ayrı bir araçla açılır:

```bash
python hesap.py admin yildiz "parolan"
python hesap.py kullanici "Görünen Ad" ad@ornek.com "parolan"
python hesap.py liste
```

Parola komut satırından alınır ve hiçbir dosyaya yazılmaz, Argon2 ile hashlenip
veritabanına gider. Tek pürüz şu: komut satırına yazdığın parola kabuk
geçmişine düşer (PowerShell'de PSReadLine'ın `ConsoleHost_history.txt`
dosyası), gerekiyorsa oradan sil. Var olan bir hesabı verirsen parolası
güncellenir.

```bash
uvicorn app.main:app --reload
```

Yönetici hesabı açılmadan `/academy/admin` kapısı çalışmaz.

## Yapı

| Yol | Ne |
|---|---|
| `app/models.py` | 12 tablo: içerik, kimlik, ilerleme |
| `app/routers/` | Sayfalar, kimlik, ders, lab, yönetim |
| `app/services/` | Cevap doğrulama, puanlama, ilerleme, sıralama, içe aktarma |
| `app/templates/` | Jinja şablonları |
| `hesap.py` | Yönetici ve kullanıcı hesabı açma aracı |
| `seed.py` | `content/` klasörünü veritabanına basar |
| `content/dersler/*.md` | Ders kaynakları, frontmatter + Markdown |
| `content/lablar/*.yaml` | Lab tanımları: adımlar, ipuçları, çözüm |
| `design/tokens.json` | Tasarım token kaynağı, tek gerçek kaynak |
| `static/css/tokens.css` | Üretilmiş CSS değişkenleri, elle düzenlenmez |
| `static/css/base.css` | Temel katman, yalnızca `var()` kullanır |
| `static/css/app.css` | Giriş sonrası arayüz |
| `static/css/landing.css` | Açılış sayfası, kendi token seti üzerinde |
| `static/img/muhur/` | Yedi başarım rozeti; dosya adı rozetin `slug` alanıyla eşleşir |
| `tasarim/landing/` | Tasarım prototipleri: açılış, panel, kütüphane, laboratuvar |
| `scrollcraft/builds/` | Kaydırma anlatısı |
| `ekran/` | README görüntüleri |

Açılış sayfası ile uygulama iki ayrı CSS zinciri kullanır ve bu bilerek böyledir.
Açılış eski tasarımda kaldı, giriş sonrası sayfalar sonradan yenilendi; ikisini
tek zincire bağlamak açılışın yıldızlı görünümünü bozuyordu.

## Laboratuvar mekaniği

Bir lab 2-6 adımdır. Her adımın kendi sorusu, cevabı, ipuçları ve puanı vardır.
Adımlar sıralıdır, atlanamaz.

Cevap tipleri `exact`, `regex` ve `choice`. Doğrulama yalnızca sunucuda yapılır;
doğru cevap hiçbir şablona, hiçbir JSON yanıtına girmez.

Adımın kazanılan puanı `max(0, puan - açılan ipuçların cezası)` ve adım ilk kez
doğru çözüldüğünde donar.

Cevap karşılaştırılırken `I`, `İ`, `ı` ve `i` tek bir harfe katlanır. Türkçe
küçültme kuralı "EICAR" yazan kullanıcıyı "eıcar" üretip yanlış cevap vermiş
duruma düşürüyordu.

## Puan kilidi

Lab her zaman sıfırlanıp baştan çözülebilir. Ama `lab_progress.solution_seen`
bayrağı sıfırlamada silinmez: çözüm metnini bir kez gören kullanıcı o labdan
bir daha puan kazanamaz. Lab tekrar çözülebilir, sıralamaya 0 yazar.

## Kimlik

Görünen ad tek kamusal kimliktir ve 30 günde bir değiştirilebilir. E-posta bir
kimlik değil, bir giriş anahtarıdır: sıralamada, panelde ve kullanıcıya dönük
hiçbir yanıtta geçmez, yalnızca sahibinin ayarlar sayfasında görünür.

Giriş hatası hangi alanın yanlış olduğunu söylemez.

## Yönetim

`/academy/admin` ayrı bir kapıdır. Yöneticiler `admin_user` tablosunda durur,
kullanıcılarla aynı tabloyu paylaşmazlar; çerezleri de oturum süreleri de
farklıdır (yönetici 8 saat, kullanıcı 30 gün). Kodda çalışan bir varsayılan
parola yoktur.

İçerik panelden `.md` ve `.yaml` olarak yüklenir; `seed.py` ile aynı ayrıştırma
mantığından geçer. Parolasını unutan kullanıcıya geçici parolayı yönetici atar,
e-posta gönderimi henüz yok.

## Fontlar

`static/fonts/` altındaki Stokeda demo sürümü ve Hemmet kişisel kullanım
lisanslıdır. Ticari yayın kararı verilirse lisans alınacak veya font
değiştirilecek. Stokeda'nın demo sürümünde rakamlar yoktur, her rakamın yerine
üreticinin filigranı basılır; sayı gösteren yerlerde bu yüzden mono font
kullanılıyor.
