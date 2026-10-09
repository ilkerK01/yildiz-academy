---
slug: cti-raporlama
order_index: 13
title: CTI Raporlama ve Intelligence Products
summary: Tehdit istihbaratı bulgularını hedef kitleye uygun, kanıt temelli ve aksiyona dönüştürülebilir raporlara aktarma yöntemleri.
tags: [cti, reporting, intelligence-products, tlp, analysis]
---

# CTI Raporlama ve Intelligence Products

## Dersin Amacı

Bu derste CTI analizinden elde edilen bulguların nasıl kullanılabilir bir istihbarat ürününe dönüştürüldüğünü öğreneceğiz. İyi bir rapor yalnızca IOC veya olay kronolojisi sıralamaz; **hangi tehdidin önemli olduğunu, değerlendirmeyi hangi kanıtların desteklediğini, hangi noktaların belirsiz kaldığını ve alıcının hangi adımı atması gerektiğini** açıklar.

## Ana Kavramlar

- Intelligence Product
- Intelligence Requirement / PIR
- Tactical, Operational, Strategic Intelligence
- Executive Summary
- Key Judgment
- Confidence Level
- Source Reliability
- Indicator of Compromise (IOC)
- MITRE ATT&CK TTP
- Traffic Light Protocol (TLP)
- Dissemination ve Feedback

## 1. Intelligence Product Nedir?

**Intelligence Product**, belirli bir istihbarat ihtiyacını yanıtlamak üzere analiz edilip hedef kitleye sunulan çıktıdır. Bir veri dökümü ile istihbarat ürünü arasındaki fark **yorum, bağlam ve karar desteği** sunmasıdır.

Örneğin `203.0.113.42` IP adresini içeren ham bir liste kendi başına sınırlı değer taşır. Bu adresin bir kampanyayla bağlantısına ilişkin kanıtlar, gözlemin zamanı, güven düzeyi ve kontrol edilmesi gereken sistemler belirtilirse analistin bulgusu kullanılabilir hale gelir. Buradaki IP, dokümantasyon için ayrılmış örnek bir adrestir; gerçek tehdit göstergesi değildir.

İlk soru şu olmalıdır: **Bu ürünü kim, hangi kararı vermek için okuyacak?**

## 2. Hedef Kitleye Göre Ürün Türleri

| Ürün türü | Hedef kitle | İçerik ve amaç |
| --- | --- | --- |
| Tactical Intelligence | SOC, Detection Engineering | IOC, TTP, tespit önerileri, sorgular ve kısa vadeli aksiyonlar |
| Operational Intelligence | Incident Response, güvenlik yöneticileri | Kampanya akışı, saldırgan faaliyetleri, hedefler ve müdahale planı |
| Strategic Intelligence | Üst yönetim, risk ekipleri | Eğilimler, kurumsal iş etkisi, tehdit öncelikleri ve yatırım kararları |

Aynı olay farklı kitlelere farklı ayrıntı düzeyinde sunulmalıdır. Bir SOC analisti log sorgusuna ihtiyaç duyarken yönetici olası hizmet kesintisini ve önerilen önlemi bilmek ister.

## 3. Raporun Temel Yapısı

Kısa ve etkili bir CTI raporu şu bölümlerden oluşabilir:

1. **Başlık, tarih ve kapsam:** Hangi dönem, sektör veya olay incelendi?
2. **TLP ve dağıtım bilgisi:** İçeriği kimlerle paylaşabiliriz?
3. **Executive Summary:** En kritik bulgu ve anlamı 3–5 cümlede.
4. **Key Judgments:** Kanıtlarla desteklenen ana değerlendirmeler.
5. **Evidence & Analysis:** Kaynaklar, zaman çizelgesi, IOC ve TTP bağlamı.
6. **Impact & Relevance:** Bulguların ilgili kurumu nasıl etkileyebileceği.
7. **Recommended Actions:** Sahibi ve önceliği belirlenmiş uygulanabilir adımlar.
8. **Limitations & Confidence:** Bilinmeyenler, çelişkiler ve güven düzeyi.
9. **References / Appendix:** Kaynaklar, IOC tablosu ve ayrıntılı teknik ekler.

Başlıklar ürüne göre uyarlanabilir; önemli olan soruyu açıkça yanıtlamaktır.

## 4. Executive Summary ve Key Judgments

**Executive Summary**, raporun tamamını okumayacak birinin anlaması gereken sonucu aktarır. Aşırı teknik ayrıntılardan kaçınılmalı, tehdidin kurumsal açıdan önemi vurgulanmalıdır.

**Key Judgment**, gözlemden üretilen analitik değerlendirmedir. Örneğin:

> Son iki haftada incelenen üç oltalama iletisinde benzer gönderim altyapısı ve kimlik bilgisi toplama sayfası tasarımı görülmüştür. Bu bulgular, iletilerin bağlantılı bir faaliyet kümesine ait olabileceğini düşündürmektedir; ancak tek bir tehdit aktörüne atıf yapmak için yeterli kanıt bulunmamaktadır.

Burada **gözlenen kanıt** ile **analistin çıkarımı** ayrı tutulur. “Kesinlikle aynı grup” gibi desteklenmeyen ifadelerden kaçınılır.

## 5. Confidence Level ve Kaynak Değerlendirme

Güven düzeyi (confidence), analizin dayandığı kanıtın kalitesi ve tutarlılığına ilişkin değerlendirmedir; tehdidin gerçekleşme olasılığıyla aynı şey değildir.

- **High confidence:** Birbiriyle uyumlu, güvenilir ve bağımsız kanıtlar mevcut.
- **Moderate confidence:** Makul kanıt mevcut, ancak önemli boşluklar bulunuyor.
- **Low confidence:** Kanıt az, dolaylı ya da doğrulanmamış.

Bu ifadeler kuruma özgü bir analitik standarda bağlanmalıdır. **Kaynak güvenilirliği** ile **bilginin doğruluğu** da birbirinden ayrılmalıdır: Güvenilir bir kaynak bile hatalı bir iddia paylaşabilir.

Değerlendirmede hangi veri eksikliğinin sonucu değiştirebileceği yazılmalıdır.

## 6. TLP ile Paylaşım Sınırları

FIRST tarafından geliştirilen **TLP 2.0**, paylaşılan bilginin hangi alıcılara aktarılabileceğini belirtmeye yarar:

- **TLP:RED:** Yalnızca belirli alıcılar; ek paylaşım yok.
- **TLP:AMBER:** Alıcının kuruluşu ve bilgiyi korumak için bilmesi gereken müşterilerle sınırlı paylaşım. **TLP:AMBER+STRICT** yalnızca alıcının kuruluşu içinde paylaşılır.
- **TLP:GREEN:** Topluluk içinde paylaşım; kamuya açık paylaşım değil.
- **TLP:CLEAR:** Paylaşım sınırlaması bulunmaz.

TLP bir gizlilik derecelendirme sistemi veya şifreleme yöntemi değildir. Paylaşım kuralları için güncel FIRST tanımı esas alınmalıdır.

## 7. Teknik IOC ve TTP Sunumu

IOC'ler açık bir tabloyla verilmelidir:

| Indicator | Tür | İlk/son görülme | Bağlam | Önerilen işlem |
| --- | --- | --- | --- | --- |
| `login-check.example` | Domain | Örnek olay tarihi | Kurgusal phishing sayfası | Proxy/DNS loglarında inceleme |
| `203.0.113.42` | IPv4 | Örnek olay tarihi | Kurgusal bağlantı | Varlık kayıtlarıyla karşılaştırma |

**Not:** Bu tablo eğitim için kurgusaldır; gerçek engelleme listesine eklenmemelidir.

IOC'nin yanında davranışı açıklayan **TTP** de belirtilmelidir. Örneğin kimlik avı, sahte giriş sayfası ve hesap ele geçirme adımlarının MITRE ATT&CK ile ilişkilendirilmesi tekil göstergeler değişse de değer taşır. Teknik eşleştirmeler mevcut kanıtlarla doğrulanmalıdır.

## 8. Uygulanabilir Öneriler Yazma

Zayıf öneri: “Kurum güvenliğini artırmalıdır.”

Daha iyi öneri: “SOC ekibi son 14 güne ait proxy ve DNS kayıtlarında ilgili domain ile bağlantılı istekleri araştırmalı; bulunan cihazlarda kimlik bilgisi kullanımını ve oturum açma anormalliklerini kontrol etmelidir.”

İyi aksiyonun **sorumlusu, önceliği, kapsamı ve doğrulama yolu** belirgin olmalıdır. Bir IOC'nin tek başına saldırı kanıtı olmadığını unutmayın; yanlış pozitif olasılığı değerlendirilmelidir.

## 9. Örnek CTI Raporu — Kurgusal Phishing Kampanyası

**Başlık:** Finans Kuruluşlarını Hedefleyen Kurgusal Kimlik Avı Faaliyeti

**Tarih:** 9 Ekim 2026

**Sınıflandırma:** TLP:CLEAR — eğitim amaçlı kurgusal içerik

### Executive Summary

Örnek bir finans kuruluşunda iki hafta içinde üç benzer phishing e-postası bildirilmiştir. İletiler, kullanıcıları sahte bir oturum açma sayfasına yönlendirmektedir. Bağımsız inceleme tamamlanmadığı için tek bir tehdit aktörüne atıf yapılmamıştır. Kurumun önceliği, etkilenen kullanıcıları ve olası kimlik bilgisi kullanımını kontrol etmektir.

### Key Judgments

- Üç iletide benzer tema ve sayfa tasarımı bulunması, koordineli bir faaliyet olasılığını destekler (**moderate confidence**).
- Kimlik bilgilerinin gerçekten ele geçirilip geçirilmediği henüz doğrulanmamıştır (**low confidence**).
- Mevcut bulgular tek başına belirli bir tehdit aktörünü tanımlamaya yeterli değildir.

### Kanıtlar

- Üç örnek phishing iletisi ve başlık bilgileri.
- Aynı görsel şablona sahip kurgusal web sayfaları.
- Eğitim amaçlı domain: `login-check.example`.

### Önerilen Aksiyonlar

1. **SOC:** İlgili URL/domain erişimlerini araştırmalı.
2. **Identity ekibi:** Etkileşime giren hesaplarda şüpheli oturumları ve MFA olaylarını incelemeli.
3. **Farkındalık ekibi:** Benzer oltalama temaları için kısa bir uyarı yayımlamalı.
4. **CTI:** Yeni kanıtlarla kampanya değerlendirmesini ve güven düzeyini güncellemeli.

### Limitations

Örnek olay verileri kurgusaldır. Gerçek ele geçirilme, saldırgan kimliği ve toplam etki hakkında sonuç çıkarılamaz.

## 10. Mini Alıştırma

Bir analist yönetime 50 satırlık hash ve IP listesi göndermiştir. Ancak olayın işletmeye etkisi ve alınması gereken önlemler raporda bulunmamaktadır.

**Sorular:**

1. Bu rapor neden yönetici kitlesi için yetersizdir?
2. Executive Summary'ye hangi üç bilgi eklenmelidir?
3. Bir bulgunun düşük güvenle değerlendirildiği nasıl belirtilir?
4. Bir raporun TLP:GREEN olması, sosyal medyada yayımlanabileceği anlamına gelir mi?

**Kısa cevap:** Yönetim, teknik liste yerine tehdit bağlamına, iş etkisine ve karar seçeneklerine ihtiyaç duyar. Düşük güvenin nedeni açıklanmalı; TLP:GREEN kamuya açık yayıma izin vermez.

## Sonuç

CTI raporlamanın hedefi çok sayıda gösterge sunmak değil, **doğru kişiye doğru zamanda karar aldıran, izlenebilir ve belirsizliklerini açıkça belirten istihbarat** üretmektir. Önce istihbarat sorusunu belirleyin, sonra bulgularınızı kanıtla destekleyin ve somut aksiyonlarla tamamlayın.
