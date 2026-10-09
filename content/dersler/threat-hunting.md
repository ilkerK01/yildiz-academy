---
slug: threat-hunting
order_index: 18
title: Threat Hunting Fundamentals
summary: Hipotez odaklı tehdit avcılığını, Windows olay kayıtlarını, Sysmon ve SIEM verilerini kullanarak şüpheli davranışları araştırmayı öğretir.
tags: [cti, threat-hunting, detection-engineering, mitre-attack, sigma]
---

# Threat Hunting Fundamentals

## Dersin Amacı

Bu derste **Threat Hunting (Tehdit Avcılığı)** yaklaşımının ne olduğu, geleneksel alarm incelemesinden nasıl ayrıldığı ve Cyber Threat Intelligence (CTI) verilerinin avcılık hipotezlerine nasıl dönüştürüldüğü ele alınır. Örnekler, gerçek sistemlerde çalıştırılması gerekmeyen **kurgusal ve zararsız log kayıtları** üzerinden ilerler.

## Ana Kavramlar

- Threat Hunting
- Hypothesis-Driven Hunting
- IOC (Indicator of Compromise)
- TTP (Tactics, Techniques and Procedures)
- SIEM (Security Information and Event Management)
- EDR (Endpoint Detection and Response)
- Windows Event Logs ve Sysmon
- Sigma Rule
- False Positive / False Negative
- Baseline ve Evidence

## Threat Hunting Nedir?

Threat Hunting, yalnızca otomatik güvenlik alarmlarını beklemek yerine, mevcut veriler içinde saldırgan davranışlarına ait izleri **proaktif ve hipotez temelli** biçimde arama sürecidir.

Örneğin EDR bir zararlı dosyayı engellediğinde alarm incelemesi yapılabilir. Threat Hunting ise henüz alarm üretmemiş, fakat belirli bir TTP ile uyumlu olabilecek davranışların kurum genelinde araştırılmasıdır.

Avcılık süreci, bütün anormal olayların mutlaka saldırı olduğu varsayımına dayanmaz. Şüpheli bulguların bağlamla doğrulanması gerekir.

## CTI ile Threat Hunting İlişkisi

CTI raporları tehdit aktörlerinin hedeflerini, kullandıkları araçları ve **TTP'lerini** açıklayabilir. Avcı bu bilgiyi ölçülebilir bir soruya dönüştürür.

Örnek:

- **İstihbarat bulgusu:** Bazı saldırılar, ilk erişim sonrasında olağan dışı komut kabuğu süreçleri oluşturuyor.
- **Hipotez:** Kurumumuzda ofis uygulamalarından başlatılmış şüpheli komut yorumlayıcı süreçleri olabilir.
- **Veri gereksinimi:** Parent/child process ilişkileri, komut satırı, kullanıcı ve zaman bilgileri.
- **Kontrol:** Yetkili otomasyon, yönetim araçları ve test faaliyetleriyle açıklanamayan örneklerin bulunması.

Tek bir IOC hızla geçersizleşebilir; davranışa dayalı TTP araştırması daha geniş bir görünürlük sağlayabilir.

## 1. Avcılık Sürecinin Aşamaları

1. **Kapsam belirleme:** Hangi sistemlerin ve zaman aralığının araştırılacağı seçilir.
2. **Hipotez kurma:** Gözlenebilir ve yanlışlanabilir bir tehdit davranışı tanımlanır.
3. **Veri hazırlama:** İlgili logların mevcut, zaman damgalarının tutarlı ve kayıt kapsamının yeterli olduğu kontrol edilir.
4. **Sorgulama:** SIEM, EDR veya log arama sistemi üzerinden aday olaylar bulunur.
5. **Doğrulama:** Normal iş akışları, geçmiş kayıtlar ve diğer veri kaynakları ile karşılaştırılır.
6. **Sonuçlandırma:** Bulgular belgelenir, gerekli durumlarda olay müdahale ekibine aktarılır ve tespit içeriği geliştirilir.

Bir avcılık çalışmasının sonuç vermemesi, tehdidin kesinlikle bulunmadığı anlamına gelmez. Veri eksikliği, görünürlük sorunları veya hipotezin kapsamı da sonucu etkiler.

## 2. Veri Kaynakları

| Kaynak | Sağladığı örnek bilgiler |
|---|---|
| Windows Security Log | Oturum açma ve süreç oluşturma (yapılandırmaya bağlı) |
| Sysmon | Süreç oluşturma, ağ bağlantıları ve seçili diğer olaylar |
| EDR | Süreç ağacı, davranış alarmı, uç nokta bağlamı |
| DNS kayıtları | Alan adı sorguları ve zaman ilişkileri |
| Proxy / Firewall | Bağlantı ve web erişim gözlemleri |
| SIEM | Farklı kaynakları birleştiren arama ve korelasyon |

Önemli örnekler: Windows Security **Event ID 4688** süreç oluşturmayı gösterir (denetim etkinse); Sysmon **Event ID 1** süreç oluşturma, **Event ID 3** ise yapılandırma etkinse ağ bağlantısı bilgisini kaydedebilir. Event ID tek başına kötü niyet kanıtı değildir.

## 3. Örnek Avcılık Senaryosu

Bir kurum, ofis uygulamalarından başlatılan komut yorumlayıcılarının izlenmesine yönelik bir hipotez kurmuştur. Aşağıdaki tablo tamamen **kurgusal** bir veri kümesidir:

| Saat | Cihaz | Parent Image | Image | Kullanıcı |
|---|---|---|---|---|
| 09:10 | PC-01 | explorer.exe | WINWORD.EXE | ayse |
| 09:11 | PC-01 | WINWORD.EXE | powershell.exe | ayse |
| 09:14 | PC-02 | explorer.exe | powershell.exe | admin |
| 09:17 | PC-03 | scheduler.exe | powershell.exe | svc-backup |

İlk dikkat çeken olay, `WINWORD.EXE → powershell.exe` süreç ilişkisidir. Ancak bu ilişki tek başına ihlal kanıtı değildir. Analist şu soruları araştırmalıdır:

- Belge kurum içi güvenilir bir kaynaktan mı geldi?
- Komut satırı, süreç imzası ve dosya yolu ne gösteriyor?
- Aynı zaman aralığında ağ bağlantısı, yeni dosya veya kalıcılık davranışı var mı?
- Kullanıcı için beklenen bir iş akışı veya kurumsal eklenti söz konusu mu?

Diğer satırlardaki PowerShell kullanımı yönetim ve yedekleme işlemleriyle ilişkili olabilir. Bunlar da doğrulama gerektirir, ancak farklı öncelikte ele alınabilir.

## 4. Sigma ile Tespit Mantığı

**Sigma**, log olayları için taşınabilir tespit kuralları tanımlamayı sağlayan açık bir kural formatıdır. Aşağıdaki örnek, veri alanları uygun şekilde eşlenmiş **Sysmon Event ID 1** kayıtlarında Office süreçlerinden başlatılan PowerShell olaylarını aramak için basitleştirilmiştir:

```yaml
# Eğitim amaçlı basitleştirilmiş örnek; üretimde test edilmelidir.
title: Office Application Spawning PowerShell
id: 7925fb1f-a449-44f0-ae56-6a6b99b5089f
status: experimental
description: Finds PowerShell launched by a common Office application.
logsource:
  product: windows
  category: process_creation
detection:
  selection_parent:
    ParentImage|endswith:
      - '\\WINWORD.EXE'
      - '\\EXCEL.EXE'
  selection_child:
    Image|endswith:
      - '\\powershell.exe'
      - '\\pwsh.exe'
  condition: selection_parent and selection_child
falsepositives:
  - Legitimate macros or enterprise automation
level: medium
```

Bu kural bir **araştırma sinyali** üretir; otomatik olarak "saldırı tespit edildi" sonucu vermez. Ortama uygun alan isimleri, istisnalar ve testler gerekir.

## 5. MITRE ATT&CK ile Eşleştirme

Şüpheli PowerShell kullanımı için **T1059.001 – PowerShell** tekniği araştırılabilir. Ancak bu tekniği bir olaya atamak için yalnızca süreç adını görmekten fazlası gerekebilir: komut satırı, çalıştırılma amacı ve çevresel kanıtlar birlikte değerlendirilmelidir.

ATT&CK bir davranış sınıflandırma çerçevesidir; tek başına olayın gerçekleştiğini veya saldırganın kimliğini doğrulamaz.

## 6. Bulguların Raporlanması

Kısa bir threat hunting raporu aşağıdakileri içerebilir:

- **Hipotez:** Office uygulamalarından olağan dışı PowerShell başlatılması.
- **Kapsam:** Son 7 gün, Windows kullanıcı uç noktaları.
- **Veri kaynakları:** Sysmon Process Creation, EDR süreç ağacı.
- **Bulgular:** İncelenmesi gereken bir aday süreç zinciri.
- **Sınırlamalar:** Bazı cihazlarda Sysmon kapsamı eksik olabilir.
- **Sonraki adım:** İşletim bağlamı ve ağ etkinliğiyle doğrulama, gerektiğinde olay müdahale sürecine yönlendirme.

Sonucu **confirmed malicious**, **benign**, **inconclusive** gibi uygun durumlarla ifade etmek, belirsizliği gizlememek açısından yararlıdır.

## Mini Alıştırma

Aşağıdaki soruları cevaplamaya çalışın:

1. Threat Hunting ile yalnızca alarm inceleme arasındaki fark nedir?
2. `WINWORD.EXE → powershell.exe` ilişkisi neden tek başına saldırı kanıtı değildir?
3. Aynı olayı doğrulamak için hangi iki ek veri kaynağına bakarsınız?
4. Çalışmada bazı cihazların loglarının eksik olması raporda neden belirtilmelidir?

**Değerlendirme:** İyi bir cevap, hipotez ile kanıtı ayırır; meşru açıklamaları dışlamadan ek doğrulama adımları önerir.

## Sonuç

Threat Hunting, CTI verilerini somut araştırma hipotezlerine dönüştürür. Başarılı bir süreç yalnızca şüpheli olay bulmaya değil, **bulguların doğrulanmasına, belirsizliklerin belirtilmesine ve savunma görünürlüğünün geliştirilmesine** dayanır.
