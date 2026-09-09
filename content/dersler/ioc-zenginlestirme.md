---
slug: ioc-zenginlestirme
order_index: 3
title: IOC Zenginleştirme ve Pivoting
summary: IOC'lerin bağlamsal bilgilerle zenginleştirilmesi ve ilişkili göstergelere geçiş yöntemleri.
tags: [cti, ioc-analizi, osint-temelleri]
---

# IOC Zenginleştirme ve Pivoting

## Dersin Amacı

Bu dersin amacı, tehdit istihbaratı çalışmalarında kullanılan IOC'lerin yalnızca tekil göstergeler olarak değil, daha geniş bir tehdit bağlamı içerisinde değerlendirilmesini açıklamaktır. IOC zenginleştirme ve pivoting süreçleri üzerinden bir göstergeden ilişkili altyapı, zararlı yazılım, kampanya ve tehdit aktörü bilgilerine nasıl geçiş yapılabileceği ele alınmaktadır.

## Ana Kavramlar

- IOC (Indicator of Compromise)
- IOC zenginleştirme
- Pivoting
- ASN
- Domain ve IP ilişkileri
- Dosya hash değerleri
- C2 altyapısı
- Pasif CTI ve OSINT kaynakları

## IOC Nedir?

Bir **IOC (Indicator of Compromise)**, kötü amaçlı veya şüpheli bir faaliyete ilişkin teknik göstergeyi ifade eder. IP adresleri, alan adları, URL'ler, dosya hash değerleri ve e-posta adresleri yaygın IOC türleri arasında yer alır.

CTI çalışmalarında yalnızca bir IOC'nin tespit edilmesi yeterli değildir. İlgili göstergenin hangi tehdit, altyapı, zararlı yazılım, kampanya veya tehdit aktörüyle ilişkili olduğunun belirlenmesi gerekir.

## IOC Zenginleştirme

IOC zenginleştirme, mevcut bir göstergenin farklı açık kaynaklardan elde edilen ek bilgilerle desteklenmesi sürecidir.

Örneğin bir IP adresi için aşağıdaki bilgiler araştırılabilir:

- Ait olduğu ASN
- Coğrafi konum
- Barındırma sağlayıcısı
- İlk ve son görülme tarihleri
- Kötü amaçlı faaliyet kayıtları
- İlişkili alan adları
- Bağlantılı zararlı yazılım aileleri
- C2 altyapısı ile ilişkisi

Bu bilgiler, tek başına sınırlı anlam taşıyan bir IOC'nin daha geniş bir tehdit bağlamı içerisinde değerlendirilmesini sağlar.

## Pivoting

**Pivoting**, bir göstergeden ilişkili başka göstergelere geçiş yapılmasıdır.

Örnek araştırma zinciri:

`IP → ASN → Domain → URL → Hash → Malware`

Bu yaklaşım sayesinde bir başlangıç göstergesinden hareketle saldırgan altyapısı, zararlı yazılım ailesi ve kampanya ilişkileri ortaya çıkarılabilir.

## Kullanılabilecek Kaynaklar

IOC analizi sırasında VirusTotal, ThreatFox, MalwareBazaar, URLhaus, AbuseIPDB, WHOIS/RDAP servisleri, ASN sorgu servisleri, MITRE ATT&CK ve güvenlik üreticilerinin tehdit araştırma raporlarından yararlanılabilir.

Mümkün olduğunda bilgiler birden fazla bağımsız kaynaktan doğrulanmalıdır.

## Pasif Araştırma Yaklaşımı

Şüpheli bir IP adresine veya alan adına doğrudan bağlantı kurulması gereksiz güvenlik riski oluşturabilir. Bu nedenle araştırma, mümkün olduğunca pasif CTI ve OSINT kaynakları üzerinden yürütülmelidir.

## IOC'lerin Bağlam İçinde Değerlendirilmesi

Bir IOC'nin tehdit veri tabanında yer alması, tek başına kesin kötü niyet göstergesi değildir. Paylaşımlı barındırma altyapıları, eski kayıtlar veya yanlış pozitifler dikkate alınmalıdır.

Bu nedenle IOC'ler zaman bilgisi, kaynak güvenilirliği, ilişkili göstergeler ve tehdit bağlamı ile birlikte değerlendirilmelidir.

## Sonuç

IOC zenginleştirme ve pivoting, CTI analizinin temel süreçlerinden biridir. Amaç yalnızca bir göstergenin zararlı olup olmadığını belirlemek değil, göstergenin ait olduğu daha geniş tehdit yapısını ortaya çıkarmaktır.

## İlgili Laboratuvarlar

**Bir hash'in izini sürmek**  
Dosya hash değerinden hareketle zararlı yazılım ailesi ve ilişkili tehdit bilgilerini araştırmaya yönelik uygulamalı bir laboratuvardır.

**Şüpheli IP'nin İzinde**  
Bir IP adresinden başlayarak ASN, tehdit türü, zararlı yazılım ve ilişkili örneklere pivot edilmesini sağlayan uygulamalı bir CTI senaryosudur.
