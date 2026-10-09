---
slug: structured-analytic-techniques
order_index: 17
title: Structured Analytic Techniques (SATs) ile CTI Analizi
summary: ACH, Key Assumptions Check ve Timeline Analysis teknikleriyle siber tehdit istihbaratında hipotezleri, kanıtları ve belirsizlikleri sistematik olarak değerlendirmeyi öğretir.
tags: [cti, structured-analytic-techniques, ach, timeline-analysis, analytic-bias]
---

# Structured Analytic Techniques (SATs) ile CTI Analizi

## Dersin Amacı

Bu derste **Structured Analytic Techniques (SATs)** yaklaşımının siber tehdit istihbaratı (CTI) analizini nasıl daha sistematik, denetlenebilir ve kanıta dayalı hale getirdiği ele alınır. Öğrenci, farklı açıklamaları karşılaştırmayı, varsayımlarını sorgulamayı ve olayları zaman sırasına dizmeyi öğrenir.

SATs, tek başına bir saldırıyı kesin olarak kimin gerçekleştirdiğini söylemez. Amaç, analistin düşünme sürecini görünür kılmak ve belirsizliği dürüstçe ifade etmektir.

## Ana Kavramlar

- Structured Analytic Techniques (SATs)
- Analysis of Competing Hypotheses (ACH)
- Key Assumptions Check
- Timeline Analysis
- Hypothesis (Hipotez)
- Evidence (Kanıt / bulgu)
- Confirmation Bias (Doğrulama yanlılığı)
- Alternative Explanation (Alternatif açıklama)
- Confidence Level (Analitik güven düzeyi)

## SATs Nedir ve CTI'da Neden Kullanılır?

CTI analistleri çoğu zaman eksik veya çelişkili verilerle çalışır. Aynı IP adresi birden fazla aktör tarafından kullanılabilir; benzer phishing e-postaları birbirinden bağımsız kampanyalarda görülebilir. İlk göze çarpan açıklamayı doğru kabul etmek, **attribution** ve risk değerlendirmelerinde hataya neden olabilir.

SATs, analiz sürecine kontrollü bir yapı kazandırır:

1. Analiz sorusunu açıkça tanımlar.
2. Birden fazla olası açıklamayı dikkate alır.
3. Kanıt ile yorumu birbirinden ayırır.
4. Alternatif açıklamalara ters düşen bulguları araştırır.
5. Sonucun belirsizliklerini ve değişmesini sağlayabilecek yeni kanıtları belirtir.

**Önemli:** SATs, analistin uzmanlığının yerini tutmaz; onu destekler.

## 1. Analysis of Competing Hypotheses (ACH)

**ACH**, bir olayın birbirine rakip açıklamalarını mevcut kanıtlar üzerinden karşılaştırmak için kullanılan bir yöntemdir. Yalnızca favori hipotezi destekleyen bulgulara bakmak yerine, her bulgunun diğer hipotezlerle ne derece uyuştuğu incelenir.

### ACH Süreci

1. Açık ve karşılaştırılabilir hipotezler üret.
2. Kanıtları, kaynaklarını ve güvenilirliklerini listele.
3. Her kanıtın her hipotez için **uyumlu**, **uyumsuz** veya **ayırt edici değil** olduğunu değerlendir.
4. Özellikle hipotezle çelişen güvenilir kanıtlara odaklan.
5. En az çelişen açıklamayı geçici değerlendirme olarak sun.
6. Hangi yeni bulgunun değerlendirmeyi değiştireceğini açıkla.

### Örnek ACH Matrisi

Bir kurum, çalışanlarını hedefleyen şüpheli e-postalar görüyor. Analist üç açıklama oluşturuyor:

- **H1:** Organize bir phishing kampanyası var.
- **H2:** Kuruma özel olmayan toplu spam gönderimi söz konusu.
- **H3:** Meşru bir hizmetin yanlış yapılandırılmış bildirimleri gönderiliyor.

| Bulgu | H1: Phishing | H2: Spam | H3: Meşru bildirim |
|---|---|---|---|
| E-postalar sahte giriş sayfasına yönlendiriyor | Uyumlu | Kısmen uyumlu | Uyumsuz |
| Gönderici alan adı kurum markasını taklit ediyor | Uyumlu | Kısmen uyumlu | Uyumsuz |
| Aynı içerik birçok kuruma gönderilmiş | Uyumlu | Uyumlu | Ayırt edici değil |
| Hizmet sağlayıcı bu bildirimleri gönderdiğini doğruluyor | Uyumsuz | Uyumsuz | Uyumlu |

Bu tablo **puanlama sonucu değildir**. Son satır yalnızca doğrulanmışsa yüksek önem taşır; güvenilir olmayan bir iddia aynı ağırlıkta değerlendirilmemelidir. ACH mekanik bir sayma işlemi değil, çelişkilerin niteliğini inceleme yöntemidir.

## 2. Key Assumptions Check

**Key Assumptions Check**, analiz sonucunu önemli ölçüde etkileyen ve her zaman açıkça belirtilmeyen varsayımları sorgular.

Bir CTI raporunda şu varsayımlar bulunabilir:

- “Aynı malware ailesi kullanıldıysa aynı tehdit aktörüdür.”
- “Bir sızıntı forumunda kurum adı geçiyorsa veriler kesinlikle çalınmıştır.”
- “Bir IP adresi bir kez zararlı faaliyetle ilişkilendirildiyse hâlâ kötücül amaçla kullanılmaktadır.”

Bunların hiçbiri tek başına güvenilir sonuç değildir.

### Uygulama Adımları

1. Analizin dayandığı temel varsayımları yaz.
2. Her varsayımın hangi kaynağa veya bulguya dayandığını belirt.
3. Varsayımın yanlış olabileceği durumları araştır.
4. Yanlış çıkarsa sonuç ne kadar değişir, değerlendir.
5. Yüksek etkili ama zayıf destekli varsayımları yeniden test et.

**CTI örneği:** Bir C2 alan adının iki olayda görülmesi, otomatik olarak aynı aktörün sorumlu olduğunu göstermez. Ortak barındırma, altyapının el değiştirmesi veya yanlış pozitif olasılıkları kontrol edilmelidir.

## 3. Timeline Analysis

**Timeline Analysis**, farklı kaynaklardan gelen olayların ortak zaman çizelgesinde gösterilmesidir. Saldırının sırasını, olası neden-sonuç ilişkilerini ve veri boşluklarını bulmaya yardımcı olur.

### Örnek Olay Zaman Çizelgesi

*Aşağıdaki saatler, aynı zaman dilimine (UTC) dönüştürülmüş kurgusal kayıtlardır.*

| Zaman (UTC) | Olay | Kaynak |
|---|---|---|
| 09:05 | Şüpheli e-posta teslim edildi | Mail gateway |
| 09:12 | E-postadaki bağlantı açıldı | Proxy log |
| 09:14 | Yeni bir oturum açma denemesi görüldü | Identity log |
| 09:20 | Bilinmeyen cihazdan başarılı oturum açıldı | Identity log |
| 09:35 | Toplu dosya erişimi tespit edildi | Audit log |

Bu kayıtlar olası bir hesap ele geçirme senaryosunu destekleyebilir. Ancak **zaman sıralaması tek başına nedensellik kanıtı değildir**. Kullanıcı doğrulaması, cihaz telemetrisi ve diğer kayıtlarla desteklenmelidir.

### Zaman Çizelgesinde Dikkat Edilecekler

- UTC veya açıkça belirtilmiş tek bir zaman dilimi kullan.
- Sistemler arası saat kaymalarını kontrol et.
- Gerçekleşme zamanı ile loga yazılma zamanını ayır.
- Eksik kayıtları “olay olmadı” şeklinde yorumlama.
- Her satırın veri kaynağını koru.

## 4. Analitik Önyargılar

**Confirmation Bias:** Analistin, inandığı hipotezi destekleyen kanıtlara gereğinden fazla önem vermesi.

**Anchoring Bias:** İlk görülen bilgiye aşırı bağlı kalması.

**Availability Bias:** Çok konuşulan bir tehdit aktörünü yeni olayların varsayılan açıklaması sayması.

Bu riskleri azaltmak için alternatif hipotezler oluşturmak, tersini gösteren kanıtları aramak ve başka bir analistin değerlendirmesini almak yararlıdır.

## 5. Teknikleri Birlikte Kullanmak: Örnek CTI Vakası

Bir şirket, çalışan hesaplarında şüpheli oturum açma girişimleri ve marka taklitli e-postalar tespit ediyor.

**Araştırma sorusu:** “Bu etkinlik tek bir koordineli phishing kampanyasının parçası mı?”

**Timeline Analysis:** E-posta teslimi, bağlantı tıklamaları ve oturum açma olayları aynı zaman diliminde sıralanır.

**Key Assumptions Check:** “Tüm olaylar tek bir saldırgana ait” varsayımı sorgulanır; farklı kampanyalar veya bağımsız olaylar olabileceği değerlendirilir.

**ACH:** Koordineli phishing, bağımsız spam ve meşru bildirim hatası hipotezleri mevcut kanıtlarla karşılaştırılır.

**Değerlendirme:** “Gözlemlenen sahte giriş sayfası ve hesap erişimi bulguları phishing olasılığını destekliyor; ancak tüm mesajların aynı operatör tarafından gönderildiğini doğrulamak için yeterli altyapı kanıtı bulunmuyor.”

Bu ifade, doğrulanmış gözlemlerle çıkarımlar arasındaki farkı korur.

## 6. Analitik Güven Düzeyi ve Raporlama

Bir değerlendirme yapılırken **güven düzeyi (confidence)** ve **olayın gerçekleşme olasılığı (likelihood)** birbirine karıştırılmamalıdır.

- **Güven düzeyi:** Analizin dayandığı kanıtların kalitesi, tutarlılığı ve kapsamı ile ilgilidir.
- **Olasılık değerlendirmesi:** İncelenen açıklamanın ne ölçüde olası görüldüğünü ifade eder.

Örnek rapor cümlesi:

> “Şüpheli e-posta ve oturum açma kayıtları, bir phishing girişimini desteklemektedir. Mevcut telemetriye dayanarak bu sonuca orta düzeyde güven duyuyoruz. Aktör kimliği henüz belirlenememiştir.”

## Mini Alıştırma

Bir SOC ekibi, aynı saat içinde üç farklı çalışanın şüpheli alan adına eriştiğini ve bir hesabın daha sonra kilitlendiğini tespit etti.

1. Bu olay için en az **üç rakip hipotez** oluştur.
2. ACH matrisinde hangi ek kanıtların ayırt edici olacağını belirle.
3. Sorgulanması gereken iki temel varsayım yaz.
4. Zaman çizelgesi için ihtiyaç duyacağın en az dört veri alanını sırala.
5. Sonucunu kesinlik iddiasında bulunmadan iki cümleyle raporla.

**Örnek yaklaşım:** Olasılıklar arasında phishing, zararsız test trafiği veya birbirinden bağımsız olaylar bulunabilir. URL içeriği, DNS/proxy kayıtları, oturum açma telemetrisi ve kullanıcı doğrulaması ayırt edici kanıtlardır.

## Sonuç

Structured Analytic Techniques, CTI analizlerinde “ilk akla gelen açıklamayı seçmek” yerine **alternatifleri test etme, varsayımları sorgulama ve olayları kanıtlarla ilişkilendirme** yaklaşımını güçlendirir.

- **ACH:** Rakip açıklamaları karşılaştırır.
- **Key Assumptions Check:** Kırılgan varsayımları görünür kılar.
- **Timeline Analysis:** Olay sırasını ve araştırılması gereken boşlukları ortaya çıkarır.

İyi bir CTI analizi yalnızca ne düşünüldüğünü değil, **neden düşünüldüğünü, neyin bilinmediğini ve hangi kanıtın sonucu değiştirebileceğini** de ifade eder.
