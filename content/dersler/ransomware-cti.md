---
slug: ransomware-cti
order_index: 6
title: Ransomware Olaylarında CTI
summary: Fidye yazılımı vakalarında tehdit aktörü, altyapı, kampanya ve hedef profilinin ilişkilendirilmesi.
tags: [cti, ransomware, threat-actor, vaka-analizi, osint-temelleri]
---

# Ransomware Olaylarında CTI

## Dersin Amacı

Bu dersin amacı, ransomware olaylarının CTI kapsamında nasıl analiz edildiğini açıklamaktır. Ransomware ailesi, tehdit aktörü, kullanılan altyapı, hedef profili, TTP'ler ve kampanya ilişkilerinin birlikte değerlendirilmesi üzerinde durulmaktadır.

## Ana Kavramlar

- Ransomware
- Ransomware-as-a-Service (RaaS)
- Affiliate
- Leak site
- Çifte şantaj
- Threat actor
- TTP
- Kampanya ilişkilendirme

## Ransomware Ekosistemi

Ransomware olaylarında CTI analizi, yalnızca kullanılan zararlı yazılımın adının belirlenmesiyle sınırlı değildir. Saldırının arkasındaki grup, kullanılan altyapı, hedeflenen sektörler, operasyonel yöntemler ve kampanya bağlantıları birlikte değerlendirilmelidir.

Modern ransomware operasyonlarında zararlı yazılım geliştiricileri, altyapı sağlayıcıları, ilk erişim sağlayan aktörler, affiliate'ler ve müzakere altyapısını yöneten kişiler gibi farklı roller bulunabilir.

Bu yapı nedeniyle bir ransomware ailesi ile tek bir saldırgan grubunun doğrudan eşleştirilmesi her zaman doğru olmayabilir.

## Ransomware-as-a-Service

**Ransomware-as-a-Service (RaaS)** modelinde geliştiriciler veya operatörler ransomware altyapısını sağlar. Affiliate olarak adlandırılan bağlı aktörler ise hedef sistemlere erişim sağlar ve saldırıyı gerçekleştirir.

Bu model, aynı ransomware ailesinin farklı aktörler tarafından kullanılmasına neden olabilir ve tehdit aktörü atfını daha karmaşık hale getirebilir.

## Sızıntı Siteleri

Bazı ransomware grupları çalınan verileri yayımlamakla tehdit ederek çifte şantaj yöntemi uygular. Bu sitelerde kurban kuruluş, yayın tarihi, sektör, ülke ve saldırıyı üstlenen grup hakkında bilgiler bulunabilir.

Saldırganların kendi yayınları bağımsız doğrulama olmadan kesin bilgi olarak kabul edilmemelidir.

## Araştırılan Temel Bilgiler

Bir ransomware vakasında aşağıdaki unsurlar incelenebilir:

- Ransomware ailesi
- Grup veya operatör adı
- İlk görülme tarihi
- Hedef sektörler ve ülkeler
- Kullanılan TTP'ler
- İlişkili IP ve alan adları
- Fidye notları
- Leak site kayıtları
- Bilinen kampanyalar
- Resmî kurum açıklamaları

## Kaynak Doğrulama

CISA ve FBI danışmanlıkları, MITRE ATT&CK, güvenlik firmalarının araştırma raporları ve ransomware izleme servisleri birlikte değerlendirilmelidir.

Özellikle tehdit aktörü atfında tek bir kaynağa dayanılmaması önemlidir.

## Atıf Değerlendirmesi

CTI raporlarında tehdit aktörü atfı kesinlik derecesiyle birlikte ele alınmalıdır. “İlişkilendirildi”, “yüksek güvenle değerlendirildi” veya “benzer TTP'ler gözlendi” gibi ifadeler, eldeki kanıtların gücünü daha doğru biçimde yansıtır.

## Sonuç

Ransomware CTI analizi genel olarak şu ilişki zincirini ortaya çıkarmayı amaçlar:

`Olay → Malware → Grup → Altyapı → TTP → Kampanya → Hedef profili`

Bu yaklaşım, tekil bir olayın daha geniş tehdit bağlamına yerleştirilmesini sağlar.

## İlgili Laboratuvar

**Boru Hattındaki Saldırı**  
Colonial Pipeline vakası üzerinden ransomware ailesi, RaaS modeli, tehdit aktörü atfı ve kritik altyapı etkisinin araştırıldığı vaka tabanlı bir CTI laboratuvarıdır.
