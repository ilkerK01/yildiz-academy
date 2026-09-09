---
slug: stix-taxii-misp
order_index: 10
title: STIX, TAXII ve MISP ile Threat Intelligence Paylaşımı
summary: Tehdit istihbaratının standart biçimde paylaşılmasını sağlayan STIX, TAXII ve MISP yapılarını temel seviyede açıklayan ders.
tags: [cti, stix, taxii, misp, threat-intelligence-sharing]
---

# STIX, TAXII ve MISP ile Threat Intelligence Paylaşımı

## Dersin Amacı

Bu dersin amacı, CTI ekiplerinin tehdit bilgilerini neden standart bir yapıda paylaşması gerektiğini ve bu alanda sık kullanılan STIX, TAXII ve MISP kavramlarının ne işe yaradığını açıklamaktır.

Bir tehdit istihbaratı ekibi yalnızca kendi topladığı IOC'lerle çalışmaz. Farklı kuruluşlardan, güvenlik şirketlerinden, CERT ekiplerinden veya topluluklardan gelen tehdit verilerinin de işlenmesi gerekir.

Ancak herkes veriyi farklı biçimde paylaşırsa otomasyon ve karşılaştırma zorlaşır. Bu nedenle CTI ekosisteminde ortak veri formatları ve paylaşım yöntemleri kullanılır.

## Ana Kavramlar

- Threat Intelligence Sharing
- IOC
- STIX
- TAXII
- MISP
- Indicator
- Threat Actor
- Campaign
- Malware
- Relationship
- Feed
- Structured Intelligence

## Tehdit İstihbaratı Neden Paylaşılır?

Bir kurum bir saldırı sırasında yeni bir zararlı domain tespit edebilir. Başka bir kurum aynı domaini birkaç gün sonra kendi ağında görebilir.

Eğer ilk kurum bu bilgiyi paylaşırsa diğer kurumlar saldırıyı daha erken tespit edebilir.

Paylaşılabilecek bilgiler arasında şunlar bulunabilir:

- IP adresleri
- Domain'ler
- URL'ler
- Dosya hash'leri
- Malware aileleri
- Threat actor bilgileri
- Kampanya bilgileri
- TTP'ler
- Güven seviyeleri
- İlk ve son görülme tarihleri

Ancak yalnızca IOC listesini paylaşmak çoğu zaman yeterli değildir.

Örneğin:

`203.0.113.20`

şeklinde tek bir IP adresi çok az bağlam sağlar.

Daha değerli bir paylaşım şöyle olabilir:

> Bu IP, 8 Eylül 2026 tarihinde gözlemlenen phishing kampanyasında C2 altyapısı olarak kullanılmıştır.

Burada IOC ile birlikte bağlam da paylaşılmış olur.

## Standartlaştırma Neden Gerekli?

Farklı kurumların tehdit bilgisini farklı şekillerde sakladığını düşünelim.

Bir kurum:

```text
IP: 203.0.113.20
Threat: phishing
```

şeklinde kayıt tutarken başka bir kurum:

```text
indicator=203.0.113.20
category=c2
```

kullanabilir.

İnsanlar bu iki kaydı anlayabilir ancak otomatik sistemlerin veriyi işlemesi zorlaşabilir.

Standartlaştırılmış veri yapıları sayesinde farklı sistemler tehdit bilgisini daha kolay anlayabilir ve paylaşabilir.

## STIX Nedir?

STIX, **Structured Threat Information eXpression** ifadesinin kısaltmasıdır.

Siber tehdit istihbaratının yapılandırılmış biçimde ifade edilmesini sağlayan bir standarttır.

STIX yalnızca IOC saklamak için kullanılmaz. Bir tehdit olayındaki farklı varlıklar ve aralarındaki ilişkiler de ifade edilebilir.

Örneğin:

- Indicator
- Malware
- Threat Actor
- Campaign
- Attack Pattern
- Identity
- Vulnerability

gibi nesneler tanımlanabilir.

## STIX Nesneleri

Bir phishing kampanyasını düşünelim.

Elimizde:

- Zararlı domain
- Malware
- Threat actor
- Phishing tekniği

bulunsun.

STIX bu bilgileri birbirinden ayrı nesneler olarak ifade edebilir.

Örneğin:

- `Indicator → Domain`
- `Malware → Zararlı yazılım`
- `Threat Actor → Tehdit grubu`
- `Attack Pattern → Phishing`

Ardından bu nesneler arasındaki ilişkiler tanımlanabilir.

## Relationship

STIX'in güçlü yönlerinden biri yalnızca nesneleri değil, aralarındaki ilişkileri de tanımlayabilmesidir.

Örneğin:

`Threat Actor → uses → Malware`

veya:

`Indicator → indicates → Malware`

gibi ilişkiler kurulabilir.

Bu yaklaşım CTI bilgisinin basit bir IOC listesinden daha anlamlı hale gelmesini sağlar.

## Basit STIX Mantığı

Bir örnek düşünelim.

Bir tehdit grubunun belirli bir malware kullandığını ve malware'in belirli bir domain ile iletişim kurduğunu biliyoruz.

Bu ilişki kavramsal olarak şöyle gösterilebilir:

`Threat Actor → Malware → Domain`

Bu yapı sayesinde analist yalnızca domaini değil, domainin hangi tehdit bağlamı içinde bulunduğunu da görebilir.

## TAXII Nedir?

TAXII, **Trusted Automated eXchange of Intelligence Information** ifadesinin kısaltmasıdır.

STIX tehdit bilgisinin **nasıl ifade edildiğini** tanımlarken TAXII bu bilginin sistemler arasında **nasıl taşınabileceğine** odaklanır.

Basit şekilde:

**STIX = Veri formatı**

**TAXII = Verinin taşınma yöntemi**

Bu iki teknoloji genellikle birlikte kullanılır.

## STIX ve TAXII Arasındaki Fark

Bu farkı bir belge ve posta sistemi gibi düşünebiliriz.

STIX belgenin hangi formatta yazılacağını belirler. TAXII ise bu belgenin karşı tarafa nasıl gönderileceğini belirler.

Örneğin bir kurum STIX formatında oluşturduğu threat intelligence verisini TAXII üzerinden başka bir sisteme aktarabilir.

Bu işlem otomatik şekilde gerçekleştirilebilir.

## Collections

TAXII sistemlerinde tehdit verileri genellikle belirli koleksiyonlarda sunulabilir.

Örneğin farklı koleksiyonlar oluşturulabilir:

- Phishing IOC'leri
- Ransomware IOC'leri
- Finans sektörünü hedefleyen tehditler
- Belirli bir bölgedeki kampanyalar

Bir CTI sistemi ihtiyacı olan koleksiyondan verileri çekebilir.

Bu sayede bütün veriyi almak yerine yalnızca ilgili tehdit bilgileri kullanılabilir.

## MISP Nedir?

MISP, **Malware Information Sharing Platform** olarak ortaya çıkmış ve zamanla tehdit istihbaratı paylaşımı için yaygın kullanılan bir platform haline gelmiştir.

MISP üzerinde tehdit olayları oluşturulabilir ve bu olaylara farklı göstergeler eklenebilir.

Örneğin bir phishing olayına:

- Domain
- IP
- URL
- Dosya hash'i
- E-posta adresi
- Malware bilgisi

eklenebilir.

Bu veriler başka MISP kullanıcıları veya sistemleriyle paylaşılabilir.

## MISP Event Mantığı

MISP içerisinde bilgiler genellikle **event** yapısı altında organize edilir.

Örneğin:

`Event: Finans sektörünü hedefleyen phishing kampanyası`

Bu event içinde:

```text
Domain: fake-bank-login.example
IP: 203.0.113.20
SHA-256: ...
Malware: ExampleRAT
```

gibi bilgiler bulunabilir.

Bu yapı aynı olayla ilişkili farklı IOC'lerin birlikte tutulmasını sağlar.

## Attribute

MISP içinde event altında bulunan veri parçaları attribute olarak tutulabilir.

Örneğin:

- IP
- Domain
- Hash
- URL
- E-posta

birer attribute olabilir.

Attribute'lara ek bilgiler de eklenebilir.

Örneğin bir IOC'nin:

- IDS sisteminde kullanılabilir olup olmadığı
- İlk görülme zamanı
- Yorumu
- Kategorisi

belirtilebilir.

## MISP ve IOC Paylaşımı

Bir SOC ekibi şüpheli bir domain tespit ettiğinde bunu MISP üzerinde paylaşabilir.

Başka bir kurum aynı MISP ağına bağlıysa bu IOC'yi kendi güvenlik sistemlerine aktarabilir.

Bu yaklaşım tehdit bilgisinin manuel olarak e-posta veya Excel dosyalarıyla paylaşılmasına göre daha hızlı ve düzenlidir.

## STIX ile MISP Aynı Şey mi?

Hayır.

STIX bir tehdit istihbaratı **veri standardıdır**.

MISP ise tehdit bilgisinin oluşturulması, organize edilmesi ve paylaşılması için kullanılabilen bir **platformdur**.

MISP farklı formatlarla çalışabilir ve STIX verilerini de içe veya dışa aktarabilir.

Bu nedenle iki teknoloji birbirinin doğrudan alternatifi değildir.

## TAXII ile MISP Aynı Şey mi?

Hayır.

TAXII sistemler arasında tehdit bilgisinin taşınması için kullanılan bir protokoldür.

MISP ise kullanıcıların ve organizasyonların threat intelligence verilerini yönetebildiği bir platformdur.

Bir CTI ortamında bu teknolojiler farklı görevler üstlenebilir.

## Feed Nedir?

Threat intelligence platformlarında sık kullanılan kavramlardan biri de **feed**'dir.

Feed, düzenli olarak güncellenen tehdit verisi kaynağıdır.

Örneğin bir feed:

- Zararlı IP adresleri
- Phishing domainleri
- Malware hash'leri
- Botnet C2 sunucuları

sağlayabilir.

Ancak bir feed'den gelen her IOC'nin doğrudan güvenilir olduğu varsayılmamalıdır.

IOC'nin:

- Kaynağı
- Tarihi
- Güven seviyesi
- Kurum açısından ilgisi

değerlendirilmelidir.

## Paylaşımda Bağlamın Önemi

Threat intelligence paylaşımında en büyük hatalardan biri bağlamsız IOC paylaşmaktır.

Örneğin yalnızca:

`198.51.100.15`

IP adresini paylaşmak yerine şu bilgiler de eklenebilir:

- Neden zararlı olarak değerlendirildi?
- Ne zaman gözlemlendi?
- Hangi malware ile ilişkili?
- Hangi kampanyada kullanıldı?
- Confidence level nedir?
- Hâlâ aktif mi?

Bu bilgiler IOC'nin başka analistler tarafından doğru şekilde değerlendirilmesini sağlar.

## False Positive Riski

Paylaşılan IOC'ler her zaman doğru olmayabilir.

Örneğin bir IP adresi geçmişte saldırgan tarafından kullanılmış ancak daha sonra başka bir kullanıcıya atanmış olabilir.

Bir cloud sağlayıcısına ait IP çok sayıda yasal sistem tarafından da kullanılabilir.

Bu nedenle alınan tehdit verisi doğrudan engelleme listesine eklenmeden önce değerlendirilmelidir.

Aksi halde false positive oluşabilir.

## TLP

Tehdit istihbaratı paylaşımında bilginin kimlerle paylaşılabileceğini belirtmek de önemlidir.

Bu amaçla **Traffic Light Protocol (TLP)** kullanılabilir.

TLP, bilginin paylaşım sınırlarını ifade eden bir sınıflandırma yaklaşımıdır.

Bir CTI analisti bir bilgiyi paylaşmadan önce yalnızca içeriğin teknik değerini değil, paylaşım izinlerini de değerlendirmelidir.

Her tehdit bilgisi herkese açık olarak yayımlanamaz.

## Otomasyon

STIX, TAXII ve MISP gibi yapıların önemli avantajlarından biri otomasyona uygun olmalarıdır.

Örneğin süreç şu şekilde olabilir:

`Threat Feed → CTI Platform → IOC Enrichment → SIEM / EDR → Detection`

Bu sayede yeni bir IOC geldiğinde güvenlik sistemlerinin otomatik olarak güncellenmesi mümkün olabilir.

Ancak otomasyon insan analizinin tamamen ortadan kalktığı anlamına gelmez.

Yanlış veya düşük kaliteli veri otomatik sisteme aktarılırsa yanlış alarmlar üretilebilir.

## Örnek Senaryo

Bir CTI ekibinin yeni bir phishing kampanyası keşfettiğini düşünelim.

Araştırma sırasında:

- 3 zararlı domain
- 2 IP adresi
- 1 malware hash'i
- Kullanılan phishing tekniği

tespit edildi.

Analist bu bilgileri MISP üzerinde bir event altında organize edebilir.

Tehdit aktörü, malware ve IOC ilişkileri STIX formatında ifade edilebilir.

Başka sistemler bu veriyi TAXII üzerinden otomatik olarak alabilir.

SOC ekibi ise gelen IOC'leri SIEM veya diğer güvenlik sistemlerinde kullanabilir.

Bu şekilde bir analistin bulduğu tehdit bilgisi farklı güvenlik ekipleri tarafından hızlı şekilde kullanılabilir.

## Sonuç

Threat intelligence paylaşımının amacı yalnızca IOC göndermek değildir.

İyi bir paylaşım şu üç özelliğe sahip olmalıdır:

- **Yapılandırılmış olmalı**
- **Bağlam içermeli**
- **Makine tarafından işlenebilir olmalı**

Temel ilişki şöyle özetlenebilir:

`STIX → Tehdit bilgisini ifade eder`

`TAXII → Tehdit bilgisini taşır`

`MISP → Tehdit bilgisini yönetir ve paylaşır`

Bu yapıların birlikte kullanılması, CTI ekiplerinin tehdit bilgisini daha hızlı, tutarlı ve otomatik şekilde paylaşmasına yardımcı olur.
