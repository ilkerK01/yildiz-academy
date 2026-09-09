---
slug: mitre-attack-cti
order_index: 4
title: CTI İçin MITRE ATT&CK Kullanımı
summary: Tehdit davranışlarının MITRE ATT&CK teknikleriyle eşleştirilmesi ve CTI analizinde kullanılması.
tags: [cti, mitre-attack, threat-actor, ttp, apt]
---

# CTI İçin MITRE ATT&CK Kullanımı

## Dersin Amacı

Bu dersin amacı, MITRE ATT&CK bilgi tabanının CTI analizinde nasıl kullanıldığını açıklamaktır. Tehdit aktörlerinin davranışlarının taktik, teknik ve prosedürler üzerinden sınıflandırılması ve farklı kampanyalar arasındaki davranışsal ilişkilerin değerlendirilmesi ele alınmaktadır.

## Ana Kavramlar

- MITRE ATT&CK
- Taktik
- Teknik
- Alt teknik
- TTP
- Threat actor
- Campaign
- Davranışsal ilişkilendirme

## MITRE ATT&CK Nedir?

MITRE ATT&CK, tehdit aktörlerinin gerçek operasyonlarda kullandığı taktik, teknik ve prosedürleri sınıflandıran bir bilgi tabanıdır.

CTI analizinde ATT&CK, farklı saldırıların ve tehdit aktörlerinin davranışsal özelliklerini ortak bir terminoloji üzerinden değerlendirmek amacıyla kullanılır.

## Taktik ve Teknik Kavramları

**Taktik**, saldırganın ulaşmak istediği genel amacı; **teknik** ise bu amaca ulaşmak için kullandığı yöntemi ifade eder.

Initial Access, Execution, Persistence, Credential Access, Discovery, Command and Control ve Exfiltration yaygın taktik örnekleridir.

## TTP Kavramı

TTP, **Tactics, Techniques and Procedures** ifadesinin kısaltmasıdır.

IOC'ler kısa süre içerisinde değiştirilebilir. Buna karşılık operasyonel yöntemler ve davranış kalıpları daha uzun süre korunabilir. Bu nedenle TTP'ler tehdit aktörü ve kampanya analizinde önemli bir veri kaynağıdır.

## IOC ve TTP Arasındaki Fark

Bir IP adresi veya hash değeri belirli bir olayla ilişkili teknik gösterge niteliğindedir. TTP ise saldırganın kullandığı davranışı ifade eder.

IOC ve TTP verileri birbirinin alternatifi değil, birbirini tamamlayan veri türleridir.

## ATT&CK Teknik Kimlikleri

MITRE ATT&CK teknikleri `Txxxx`, alt teknikler ise `Txxxx.xxx` biçiminde tanımlanır.

Bu kimlikler sayesinde farklı kaynaklarda yer alan saldırı davranışları ortak bir referans sistemiyle karşılaştırılabilir.

## Tehdit Aktörü Analizinde Kullanım

Bir tehdit aktörünün farklı operasyonlarında benzer TTP'lerin görülmesi ilişkilendirme açısından değerli olabilir. Ancak tek bir tekniğin ortak olması, iki olayın aynı aktör tarafından gerçekleştirildiğini kanıtlamaz.

Bu nedenle ATT&CK eşleştirmeleri IOC'ler, altyapı ilişkileri, zararlı yazılım benzerlikleri ve diğer CTI bulgularıyla birlikte değerlendirilmelidir.

## CTI Raporlarında ATT&CK Kullanımı

Analiz sırasında genel olarak şu süreç izlenir:

1. Gözlenen davranış belirlenir.
2. İlgili taktik tespit edilir.
3. Teknik ve varsa alt teknik eşleştirilir.
4. Aynı teknikleri kullanan aktör ve kampanyalar incelenir.
5. Sonuç diğer CTI bulgularıyla birlikte değerlendirilir.

## Sonuç

MITRE ATT&CK, tehdit aktörlerinin otomatik olarak belirlenmesini sağlayan bir araç değildir. Temel değeri, saldırgan davranışlarının sistematik biçimde sınıflandırılmasına ve farklı olaylar arasında davranışsal ilişkilendirme yapılmasına katkı sağlamasıdır.

## İlgili Laboratuvar

**SolarWinds Zincirini Çöz**  
Tek bir IOC'den başlayarak SUNBURST, SolarWinds Orion, MITRE ATT&CK tekniği, NOBELIUM, APT29 ve ilgili kampanya bağlantılarının araştırıldığı ileri seviye CTI laboratuvarıdır.
