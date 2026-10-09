---
slug: cyber-kill-chain
order_index: 11
title: Cyber Kill Chain ve Saldırı Aşamaları
summary: Cyber Kill Chain modelinin yedi aşamasını, saldırı örneklerini ve savunma ekiplerinin her aşamada saldırıyı nasıl kesintiye uğratabileceğini açıklayan ders.
tags: [cti, attack-lifecycle, cyber-kill-chain]
---

# Cyber Kill Chain ve Saldırı Aşamaları

## Dersin Amacı

Bu dersin amacı, siber saldırıları yalnızca son aşamada ortaya çıkan zararlı faaliyetler olarak değil, birbirini takip eden eylemler bütünü olarak incelemektir. **Cyber Kill Chain** modeli ile saldırganın hedefini araştırmasından amacına ulaşmasına kadar izleyebileceği adımlar açıklanacak; CTI analistlerinin bu modeli olayları anlamlandırmak, istihbarat soruları üretmek ve savunma önceliklerini belirlemek için nasıl kullandığı gösterilecektir.

Ders sonunda öğrenci yedi aşamayı tanımlayabilecek, bir olay senaryosundaki gözlemleri ilgili aşamalarla eşleştirebilecek ve modelin sınırlılıklarını açıklayabilecektir.

## Ana Kavramlar

- Cyber Kill Chain
- Reconnaissance (Keşif)
- Weaponization (Saldırı aracının hazırlanması)
- Delivery (İletim)
- Exploitation (İstismar)
- Installation (Yerleşme)
- Command and Control / C2 (Komuta ve kontrol)
- Actions on Objectives (Hedefe yönelik eylemler)
- Indicator of Compromise (IOC)
- Tactics, Techniques and Procedures (TTP)
- Detection ve Disruption

## Cyber Kill Chain Nedir?

Cyber Kill Chain, Lockheed Martin tarafından geliştirilen ve hedefli siber saldırıların birbirini izleyen yedi aşama üzerinden incelenmesini sağlayan bir modeldir. Model, savunma ekiplerine yalnızca saldırının **ne yaptığını** değil, **hangi noktada tespit edilip durdurulabileceğini** de düşünme imkânı verir.

Klasik sıralama şöyledir:

`Reconnaissance → Weaponization → Delivery → Exploitation → Installation → Command and Control → Actions on Objectives`

Bu sıralama öğretici bir çerçevedir. Gerçek olaylarda bütün aşamaların kanıtı bulunmayabilir; saldırgan bazı adımları atlayabilir, tekrarlayabilir veya birbirine paralel yürütebilir. Bu nedenle model, değişmez bir saldırı reçetesi olarak kullanılmamalıdır.

## 1. Reconnaissance – Keşif

Saldırgan bu aşamada hedefle ilgili bilgi toplamaya çalışır. Kurumun dışarıya açık servisleri, çalışanların kamuya açık profilleri, kullanılan teknolojiler ve alan adı yapısı araştırma konusu olabilir.

Örnek gözlemler:

- Kurumun kamuya açık personel bilgilerinin araştırılması
- İnternete açık sistemlere ilişkin bilgilerin toplanması
- Hedef organizasyonun teknoloji altyapısının anlaşılmaya çalışılması

**CTI açısından:** Hedef alınan sektör, kullanılan araştırma yöntemleri ve kampanyalar arasında tekrar eden hedef seçimleri önemlidir. Kamuya açık bir bilginin varlığı, tek başına saldırının gerçekleştiğini göstermez.

**Savunma yaklaşımı:** Gereksiz bilgi ifşasını azaltmak, dış varlık envanteri tutmak ve olağan dışı tarama faaliyetlerini uygun bağlamda incelemek.

## 2. Weaponization – Saldırı Aracının Hazırlanması

Bu aşamada saldırgan, bir zararlı yükü veya hedefe uygun saldırı içeriğini hazırlayabilir. Örneğin belirli bir yazılım zafiyetinden yararlanmayı amaçlayan bir dosya ile kötü amaçlı bir bileşen bir araya getirilebilir.

Weaponization genellikle saldırganın kendi ortamında gerçekleştiğinden, hedef kurumun doğrudan gözlemlemesi zor olabilir. Analistler çoğu zaman bu aşamayı sonradan elde edilen örnekler, kampanya raporları veya malware davranışlarından çıkarır.

**CTI açısından:** Kullanılan araçlar, belge biçimleri ve zararlı yazılım aileleri arasındaki benzerlikler kampanya kümelendirmesinde yardımcı olabilir; yalnızca tek bir benzerlik kesin attribution kanıtı değildir.

## 3. Delivery – İletim

Hazırlanan saldırı içeriğinin hedefe ulaştırıldığı aşamadır. Phishing e-postası, zararlı bağlantı, kötü amaçlı dosya veya güvenliği ihlal edilmiş bir web sitesi bu aşamada rol oynayabilir.

Örnek gözlemler:

- Şüpheli ek içeren bir e-posta
- Kullanıcıyı sahte oturum açma sayfasına yönlendiren bağlantı
- Bilinen bir saldırı kampanyasıyla ilişkili URL

**CTI açısından:** E-posta başlıkları, URL ve alan adı bilgileri, dosya hash'leri ve gönderim zamanı gibi veriler incelenebilir. IOC'lerin güvenilirliği, güncelliği ve bağlamı değerlendirilmelidir.

**Savunma yaklaşımı:** E-posta güvenliği, bağlantı ve ek analizi, kullanıcı farkındalığı ve ağ filtreleme kontrolleri.

## 4. Exploitation – İstismar

Saldırganın hedef sistemde bir zafiyetten ya da kullanıcı eyleminden yararlanarak amaçladığı çalıştırmayı veya erişimi elde etmeye çalıştığı aşamadır.

Örneğin kullanıcı kötü amaçlı bir belgeyi açtıktan sonra şüpheli bir işlemin çalışması veya bir uygulama zafiyetinin istismar edilmesi bu aşamada değerlendirilebilir. Ancak her phishing olayı mutlaka yazılım açığı içermez; çalınan kimlik bilgilerinin kullanılması gibi olaylar klasik modelin sınırlarını da gösterir.

**CTI açısından:** Hangi zafiyetin, tekniğin veya koşulun istismar edildiği araştırılır. CVE bilgisinin bulunması, o CVE'nin olayda gerçekten kullanıldığını kanıtlamaz.

**Savunma yaklaşımı:** Güncelleme yönetimi, saldırı yüzeyini daraltma, uygulama sertleştirme ve şüpheli işlem davranışlarının izlenmesi.

## 5. Installation – Yerleşme

Bu aşama, saldırganın hedef ortamda zararlı yazılım veya erişimi sürdürebilecek bir bileşen yerleştirdiği durumu ifade eder. Örneğin kötü amaçlı bir servis ya da kalıcılık mekanizması oluşturulabilir.

Her saldırıda kalıcı bir yazılım kurulması gerekmez. Dosyasız saldırılar veya geçici erişim yöntemleri bu aşamaya tam uymayabilir.

**CTI açısından:** Yeni servisler, otomatik başlatma kayıtları, beklenmeyen dosyalar ve olayla bağlantılı dosya hash'leri analiz edilebilir.

**Savunma yaklaşımı:** Endpoint Detection and Response (EDR), uygulama kontrolü, sistem değişikliklerinin izlenmesi ve asgari yetki ilkesi.

## 6. Command and Control (C2) – Komuta ve Kontrol

Saldırgan, ele geçirilen sistemle haberleşmek ve bazı eylemleri uzaktan yönlendirmek için bir iletişim kanalı kullanabilir. C2 trafiği kimi zaman normal web trafiğine benzeyebilir.

CTI analisti şu sorulara odaklanabilir:

- Şüpheli bağlantı hangi alan adı veya IP'ye yöneliyor?
- Bağlantılar hangi sıklıkta tekrarlanıyor?
- Altyapı daha önce raporlanan bir kampanyayla ilişkili mi?
- Bu ilişkinin kanıtı ne kadar güçlü?

**Savunma yaklaşımı:** DNS ve ağ günlüklerini incelemek, olağandışı dış bağlantıları analiz etmek ve doğrulanmış kötü amaçlı hedeflere erişimi sınırlandırmak.

Tek başına bir IP eşleşmesi kesin C2 kanıtı değildir; paylaşımlı servisler ve değişken altyapılar yanlış pozitiflere neden olabilir.

## 7. Actions on Objectives – Hedefe Yönelik Eylemler

Saldırganın asıl amacını gerçekleştirmeye çalıştığı aşamadır. Hedef; veri sızdırma, sistemleri şifreleme, operasyonu aksatma, bilgi toplama veya başka bir etki oluşturma olabilir.

**CTI açısından:** Eylemin kurum üzerindeki etkisi, hedeflenen veri türü ve saldırganın olası motivasyonu değerlendirilir. Bulgular desteklenmiyorsa motivasyon veya saldırgan kimliği kesin ifadelerle açıklanmamalıdır.

**Savunma yaklaşımı:** Veri erişimi ve aktarımının izlenmesi, ağ segmentasyonu, yedekleme, olay müdahalesi ve iş sürekliliği planlarının işletilmesi.

## Örnek Olay: Kurgusal Phishing ve Ransomware Kampanyası

Bir kurumun çalışanına fatura konulu şüpheli bir e-posta geldiğini, ardından uç noktada zararlı bir işlemin görüldüğünü ve bir sunucuda şifreleme etkinliği tespit edildiğini varsayalım.

| Cyber Kill Chain aşaması | Kurgusal bulgu | Analistin sorusu |
| --- | --- | --- |
| Reconnaissance | E-postada çalışanın görevine uygun ayrıntılar var | Bu bilgiler kamuya açık kaynaklardan mı edinildi? |
| Weaponization | Ek dosyanın bilinen bir zararlı aileyle benzerliği raporlandı | Benzerlik hangi teknik kanıtlara dayanıyor? |
| Delivery | Çalışana ekli phishing e-postası ulaştı | Aynı içerik başka çalışanlara da gönderildi mi? |
| Exploitation | Ek açıldıktan sonra şüpheli işlem oluştu | İşlemi hangi olay tetikledi? |
| Installation | Beklenmeyen kalıcılık kaydı tespit edildi | Bu kayıt saldırıyla ilişkili mi? |
| Command and Control | Uç noktadan tekrarlayan dış bağlantılar görüldü | Bağlantılar doğrulanmış C2 etkinliği mi? |
| Actions on Objectives | Bazı dosyaların şifrelendiği gözlendi | Kapsam ve iş etkisi nedir? |

**Önemli:** Bu tablo örnek bir analizdir. Bir olayda belirli aşamaya ait kanıt bulunmaması, o aşamanın kesinlikle gerçekleşmediği anlamına gelmez.

## Cyber Kill Chain ile MITRE ATT&CK Arasındaki Fark

Cyber Kill Chain, hedefli saldırının genel akışını yedi aşama üzerinden düşünmeyi sağlar. **MITRE ATT&CK** ise gerçek dünyada gözlenen saldırgan davranışlarını taktik ve teknik düzeyinde sınıflandıran daha ayrıntılı bir bilgi tabanıdır.

Örneğin Cyber Kill Chain'de **Delivery** olarak yorumlanan bir olay, ATT&CK'te belirli bir initial access tekniğiyle açıklanabilir. Ancak bu iki çerçeve birebir karşılık gelen, aynı ayrıntı düzeyinde modeller değildir.

CTI çalışmalarında Kill Chain büyük resmi; ATT&CK ise davranışların teknik ayrıntılarını anlatmak için birlikte kullanılabilir.

## Modelin Sınırlılıkları

- Yedi aşama tüm saldırılarda aynı sırada gerçekleşmeyebilir.
- Bulut, kimlik bilgisi kötüye kullanımı ve living-off-the-land gibi faaliyetler klasik aşamalara zor sığabilir.
- Saldırgan bazı aşamaları tekrarlayabilir veya birden fazla hedefe paralel ilerleyebilir.
- Bir IOC'nin belirli aşamayla ilişkilendirilmesi, tek başına saldırı zincirinin tamamını kanıtlamaz.
- Model, saldırganın kimliğini veya niyetini kendi başına ortaya koymaz.

Bu nedenle model, loglar, olay zaman çizelgesi, teknik davranışlar ve diğer istihbarat kaynaklarıyla birlikte kullanılmalıdır.

## Mini Alıştırma

Aşağıdaki gözlemleri uygun Cyber Kill Chain aşamalarıyla eşleştirmeye çalışın:

1. Çalışana şüpheli bağlantı içeren e-posta gönderilmesi
2. Ele geçirilen uç noktadan düzenli aralıklarla dış bağlantı kurulması
3. Hassas dosyaların kurum dışına aktarılmaya çalışılması
4. Uç noktada şüpheli bir kalıcılık mekanizmasının görülmesi

**Yanıtlar:** 1. Delivery, 2. Command and Control, 3. Actions on Objectives, 4. Installation.

## Sonuç

Cyber Kill Chain, CTI analistinin saldırı hakkında şu üç soruyu sistematik biçimde sormasına yardımcı olur:

- Saldırgan hangi aşamada ve bunu hangi kanıtlar destekliyor?
- Hangi davranışlar daha erken tespit edilebilirdi?
- Kurumun hangi savunma kontrolleri saldırıyı kesintiye uğratabilir?

Amaç yalnızca aşamaları ezberlemek değil, bir saldırı vakasının bulgularını anlamlı bir çerçeveye oturtmak ve kanıt temelli savunma kararlarını desteklemektir.
