---
slug: diamond-model
order_index: 12
title: Diamond Model of Intrusion Analysis
summary: Saldırgan, yetenek, altyapı ve kurban arasındaki ilişkileri Diamond Model ile incelemeyi ve CTI olaylarını kanıta dayalı biçimde ilişkilendirmeyi öğretir.
tags: [cti, diamond-model, intrusion-analysis, threat-analysis]
---

# Diamond Model of Intrusion Analysis

## Dersin Amacı

Bu dersin amacı, bir siber olayı yalnızca IP adresleri, dosya hash'leri veya saldırı tekniklerinden oluşan bir liste olarak değil, **birbirine bağlı aktör, yetenek, altyapı ve hedef ilişkileri** olarak değerlendirmeyi öğretmektir. Diamond Model, analistin elindeki bulguları düzenlemesine, eksik kanıtları fark etmesine ve birden fazla olay arasında savunulabilir bağlantılar kurmasına yardımcı olur.

Ders sonunda öğrenci modelin dört temel bileşenini tanımlayabilecek, bir olayı bir *diamond event* olarak gösterebilecek, olayları ilişkilendirebilecek ve kanıt ile varsayımı ayırabilecektir.

## Ana Kavramlar

- Diamond Model of Intrusion Analysis
- Adversary (Saldırgan)
- Capability (Yetenek)
- Infrastructure (Altyapı)
- Victim (Kurban / Hedef)
- Event (Olay)
- Pivoting (İlişkili veriler üzerinden yeni bulgulara geçiş)
- Activity Thread (Bağlantılı olay dizisi)
- Attribution (Saldırganla ilişkilendirme)
- Confidence Level (Güven düzeyi)

## Diamond Model Nedir?

Diamond Model, siber saldırı faaliyetlerini yapılandırılmış biçimde analiz etmek için kullanılan bir modeldir. Temel yaklaşım şudur: Bir saldırı olayında **bir saldırgan**, **bir yeteneği**, **belirli bir altyapı aracılığıyla**, **bir hedefe karşı** kullanır.

Dört bileşen bir elmasın köşeleri gibi düşünülebilir:

```text
                Adversary
               /         \
     Infrastructure     Capability
               \         /
                  Victim
```

Bu şema ilişkileri kavramsal olarak gösterir; gerçek analizde her köşenin mutlaka tam olarak bilinmesi gerekmez. Örneğin hedef ve kullanılan zararlı yazılım bilinirken saldırganın kimliği belirsiz olabilir.

Model, yalnızca tek bir saldırıyı sınıflandırmak için değil, farklı olaylardaki ortak noktaları bulmak için de kullanılır.

## 1. Adversary — Saldırgan

Adversary, olayı gerçekleştiren veya yönlendiren kişi, grup ya da organizasyonu ifade eder.

Araştırılabilecek sorular:

- Bu faaliyeti kim yürütüyor olabilir?
- Bir tehdit aktörü kümesiyle bağlantıyı destekleyen kanıt nedir?
- Saldırganın olası amacı nedir?
- Atıf yaparken hangi alternatif açıklamalar göz önünde bulundurulmalıdır?

**Önemli:** Aynı zararlı yazılım ailesini ya da saldırı altyapısını kullanmak, tek başına iki olayın aynı aktöre ait olduğunu kanıtlamaz. Araçlar ve altyapı farklı kişilerce kullanılabilir, kiralanabilir veya taklit edilebilir.

## 2. Capability — Yetenek

Capability, saldırganın hedef üzerinde etki oluşturmak için kullandığı teknik araçları ve yöntemleri kapsar.

Örnekler:

- Makro içeren kötü amaçlı belge
- Kimlik bilgisi çalmaya yönelik sahte giriş sayfası
- Belirli bir malware family
- PowerShell tabanlı çalıştırma tekniği
- Bir zafiyetin istismar edilmesi

Yetenek ile altyapıyı karıştırmamak gerekir. **Sahte giriş sayfasının kendisi** bir yetenek veya saldırı mekanizması olarak değerlendirilebilirken, **sayfanın barındırıldığı sunucu ve alan adı** altyapı bileşenidir.

## 3. Infrastructure — Altyapı

Infrastructure, saldırı faaliyetinin gerçekleştirilmesini veya yönetilmesini sağlayan teknik kaynaklardır.

Örnekler:

- Phishing domain'leri ve web sunucuları
- Command and Control (C2) sunucuları
- E-posta gönderim sistemleri
- Proxy veya yönlendirme servisleri
- Barındırma hesapları ve ilgili ağ bileşenleri

Bir domain ya da IP adresi incelenirken zaman bilgisi önemlidir. Bir IP farklı dönemlerde farklı kullanıcılar tarafından kullanılabilir. Bu nedenle yalnızca aynı IP'nin görülmesi güçlü bir ilişkilendirme kanıtı olmayabilir.

## 4. Victim — Kurban / Hedef

Victim, saldırı faaliyetinin yöneltildiği kişi, sistem, kurum veya varlığı ifade eder.

Hedefe ilişkin veriler şunları içerebilir:

- Kurumun faaliyet gösterdiği sektör
- Hedef kullanıcının rolü
- Etkilenen cihaz veya hesap
- Coğrafi konum veya kullanılan teknoloji
- Hedefin saldırgan açısından muhtemel değeri

Birden fazla olayın aynı sektördeki kuruluşları hedeflemesi anlamlı olabilir; ancak bunun tek başına ortak saldırganı göstermediği unutulmamalıdır.

## 5. Diamond Event Nasıl Oluşturulur?

Modelin temel analiz birimi, belirli bir zamanda gözlenen faaliyetle ilişkili **event**tir. Bir olay kaydı oluştururken yalnızca dört köşeyi değil, olayın zamanını, kaynaklarını ve belirsizliklerini de belirtmek yararlıdır.

Örnek olay kaydı:

| Alan | Örnek bulgu |
| --- | --- |
| Event ID | EVT-001 |
| Zaman | 12 Eylül, 09.15 UTC |
| Adversary | Bilinmiyor |
| Capability | Parola toplamayı amaçlayan sahte oturum açma sayfası |
| Infrastructure | `login-update.example` (kurgusal) |
| Victim | Finans kurumu çalışanı |
| Evidence | E-posta üstbilgisi ve doğrulanmış URL kaydı |
| Confidence | Altyapı/yöntem için yüksek; aktör atfı için yetersiz |

Bu kayıt tek başına saldırganın kim olduğunu söylemez; ancak hangi bilginin bilindiğini ve hangi soruların açık kaldığını görünür kılar.

## 6. Pivoting ve Activity Thread

**Pivoting**, mevcut bir bulgudan hareketle yeni ve ilgili bulguların araştırılmasıdır. Örneğin şüpheli bir domain'den geçmiş DNS kayıtlarına, oradan başka alan adlarına geçilebilir. Her yeni bağlantının bağımsız kanıtlarla doğrulanması gerekir.

**Activity Thread** ise zaman ve ilişki bakımından birbirine bağlanan olayların dizisidir:

`Phishing e-postası → Sahte giriş sayfası ziyareti → Hesap oturumu denemesi`

Bu zincir, olayların aynı kampanyaya ait olabileceğine ilişkin bir hipotez oluşturur. Ancak zaman yakınlığı ve teknik benzerlik tek başına kesin kanıt değildir.

Diamond Model'de olaylar arasında ilişki kurarken şu soruları sorun:

1. Aynı altyapı mı kullanılmış? Kullanım zamanları örtüşüyor mu?
2. Aynı capability veya TTP gözleniyor mu?
3. Hedef profilleri arasında anlamlı bir ortaklık var mı?
4. Alternatif açıklamalar, örneğin paylaşılan hosting, mümkün mü?
5. Bu bağı hangi somut kayıt veya kaynak destekliyor?

## 7. Örnek CTI Analizi: Phishing Kampanyası

Aşağıdaki olay tamamen kurgusaldır; alan adları örnek amaçlıdır.

Bir SOC ekibi üç ayrı şüpheli e-posta bildirimi alır. İlk iki e-postanın aynı sahte giriş sayfasına yönlendirdiği ve farklı çalışanları hedeflediği görülür. Üçüncü e-postada ise farklı bir domain vardır; ancak sayfa düzeni ve istek akışı benzerdir.

**Event A:**

- Adversary: Bilinmiyor
- Capability: Kurumsal kimlik bilgilerini hedefleyen phishing sayfası
- Infrastructure: `secure-login.example`
- Victim: Finans ekibi çalışanı
- Evidence: E-posta bağlantısı ve güvenli ortamda alınmış sayfa kaydı

**Event B:**

- Adversary: Bilinmiyor
- Capability: Aynı phishing sayfası örüntüsü
- Infrastructure: `secure-login.example`
- Victim: İnsan kaynakları çalışanı
- Evidence: İkinci e-posta bildirimi ve bağlantı kaydı

**Event C:**

- Adversary: Bilinmiyor
- Capability: Benzer fakat aynı olduğu doğrulanmamış sayfa
- Infrastructure: `employee-auth.example`
- Victim: Başka bir kurumun çalışanı
- Evidence: Ekran görüntüsü ve sınırlı URL bilgisi

**Analiz:** Event A ve B aynı altyapıyı paylaştığı için ilişkili olma olasılığı yüksektir. Event C'nin aynı kampanyaya ait olması ise yalnızca benzer tasarıma dayanarak söylenemez. DNS geçmişi, kayıt zamanları veya daha ayırt edici teknik bulgular gereklidir.

**CTI çıktısı:** Doğrulanmış domain göstergeleri, hedef kullanıcı grupları, gözlenen phishing tekniği, kanıt kaynakları ve henüz doğrulanmamış ilişkiler ayrı ayrı raporlanır.

## 8. Diamond Model ve MITRE ATT&CK Arasındaki Fark

İki yaklaşım birbirini tamamlar:

| Diamond Model | MITRE ATT&CK |
| --- | --- |
| Saldırgan, yetenek, altyapı ve kurban arasındaki ilişkilere odaklanır. | Saldırgan davranışlarını tactic ve technique düzeyinde sınıflandırır. |
| Olaylar ve kampanyalar arasındaki bağları araştırmaya yardımcı olur. | Gözlenen davranışları ortak bir teknik dille ifade eder. |
| “Kim, neyi, hangi araç ve altyapıyla hedefledi?” sorusuna yaklaşır. | “Hangi davranış veya teknik uygulandı?” sorusuna yaklaşır. |

Örneğin kimlik avı etkinliği ATT&CK altında ilgili teknikle etiketlenebilir; Diamond Model ise bu etkinlikte kullanılan domain'i, hedefi ve olası saldırgan ilişkisini bir arada değerlendirir.

## 9. Analizde Sık Yapılan Hatalar

- Tek bir IOC eşleşmesine dayanarak kesin attribution yapmak.
- Ortak hosting veya meşru servisleri doğrudan suçlu kabul etmek.
- Olayların gerçekleştiği zaman aralığını göz ardı etmek.
- Bilinmeyen alanları tahminlerle doldurup gerçekmiş gibi sunmak.
- Veri kaynağının kalitesini ve kanıtın güven düzeyini belirtmemek.
- Benzer TTP kullanımını otomatik olarak aynı kampanya saymak.

İyi bir CTI değerlendirmesi, **doğrulanan bulguları**, **analitik çıkarımları** ve **henüz cevaplanmamış soruları** açık biçimde ayırır.

## Mini Alıştırma

Bir kurumun iki çalışanına `notice.example` bağlantılı e-postalar gönderilmiştir. Aynı hafta başka bir şirkete `alert.example` bağlantısı gönderilmiştir. Her iki domain de benzer bir giriş sayfası sunmaktadır.

1. Her iki olayın Diamond Model bileşenlerini listeleyin.
2. Hangi bilgiler doğrudan gözlem, hangileri çıkarımdır?
3. İki domain'in aynı saldırgan tarafından kullanıldığını değerlendirmek için hangi ek kanıtlara ihtiyaç vardır?
4. Sonucu “kesin aynı saldırgan” demeden nasıl raporlarsınız?

**Beklenen yaklaşım:** Domain'ler altyapı, sahte sayfa kimlik bilgisi toplama yeteneği, çalışanlar kurban olarak yazılabilir. Saldırgan bilinmiyor olarak kalır. Teknik benzerlik bir araştırma hipotezidir; tek başına atıf değildir.

## Sonuç

Diamond Model, CTI analistinin birbirinden kopuk görünen bulguları **Adversary – Capability – Infrastructure – Victim** ilişkileri üzerinden düzenlemesini sağlar. Modelin gücü, yalnızca bağlantı bulmasında değil, kanıtın desteklemediği iddiaları ayıklamasındadır.

`Gözlem → Diamond Event → Olaylar arası bağlantı → Alternatif açıklamaların testi → Kanıta dayalı değerlendirme`
