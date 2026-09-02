# Yıldız Academy

Siber tehdit istihbaratı öğrenme platformu. Kısa dersler ve gerçek izlerle
kurulmuş CTF tarzı araştırma laboratuvarları.

Akademinin tamamı giriş arkasındadır. Kullanıcı görünen ad, e-posta ve parola
ile hesap açar, sonra içeri girer. Herkese açık olan tek sayfa açılıştır.

## Yığın

FastAPI · Jinja2 · SQLAlchemy 2 · SQLite · Argon2id · Vanilla JS

Node çalışma zamanı bağımlılığı yoktur.

## Kurulum

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
```

`.env` içinde `ADMIN_PASS` değerini kendin belirle. Boş bırakılırsa yönetim
paneli hiç açılmaz.

```bash
python seed.py
uvicorn app.main:app --reload
```

## Yapı

| Yol | Ne |
|---|---|
| `app/models.py` | 11 tablo: içerik, kimlik, ilerleme |
| `app/routers/` | Sayfalar, kimlik, ders, lab, yönetim |
| `app/services/` | Cevap doğrulama, puanlama, ilerleme, sıralama, içe aktarma |
| `app/templates/` | Jinja şablonları |
| `content/dersler/*.md` | Ders kaynakları, frontmatter + Markdown |
| `content/lablar/*.yaml` | Lab tanımları: adımlar, ipuçları, çözüm |
| `design/tokens.json` | Tasarım token kaynağı, tek gerçek kaynak |
| `static/css/tokens.css` | Üretilmiş CSS değişkenleri, elle düzenlenmez |
| `static/css/base.css` | Temel katman, yalnızca `var()` kullanır |
| `tasarim/landing/` | Tasarım prototipleri: açılış, panel, kütüphane, laboratuvar |
| `scrollcraft/builds/` | Kaydırma anlatısı |
| `seed.py` | `content/` klasörünü veritabanına basar |

## Laboratuvar mekaniği

Bir lab 2-6 adımdır. Her adımın kendi sorusu, cevabı, ipuçları ve puanı vardır.
Adımlar sıralıdır, atlanamaz.

Cevap tipleri `exact`, `regex` ve `choice`. Doğrulama yalnızca sunucuda yapılır;
doğru cevap hiçbir şablona, hiçbir JSON yanıtına girmez.

Adımın kazanılan puanı `max(0, puan - açılan ipuçların cezası)` ve adım ilk kez
doğru çözüldüğünde donar.

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

`/academy/admin` ayrı bir kapıdır, kullanıcı tablosuyla ilişkisi yoktur. Kimlik
`.env` dosyasından okunur, kodda çalışan bir varsayılan yoktur.

İçerik panelden `.md` ve `.yaml` olarak yüklenir; `seed.py` ile aynı ayrıştırma
mantığından geçer.

## Fontlar

`static/fonts/` altındaki Stokeda demo sürümü ve Hemmet kişisel kullanım
lisanslıdır. Ticari yayın kararı verilirse lisans alınacak veya font
değiştirilecek.
