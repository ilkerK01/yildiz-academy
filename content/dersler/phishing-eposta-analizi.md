---
slug: phishing-eposta-analizi
order_index: 5
title: Phishing E-postalarında CTI Analizi
summary: Şüpheli e-postalardaki başlık alanlarının incelenmesi ve teknik IOC'lerin çıkarılması.
tags: [cti, phishing, email-analizi, ioc-analizi, osint-temelleri]
---

# Phishing E-postalarında CTI Analizi

## Dersin Amacı

Bu dersin amacı, phishing e-postalarının CTI bakış açısıyla incelenmesini ve e-posta başlıklarından teknik göstergelerin çıkarılmasını açıklamaktır. Gönderen altyapısı, e-posta kimlik doğrulama mekanizmaları ve mesaj içerisinde yer alan teknik izler üzerinden olayın daha geniş bir tehdit bağlamında nasıl değerlendirilebileceği ele alınmaktadır.

## Ana Kavramlar

- Phishing
- E-posta başlık analizi
- Received
- Return-Path
- Reply-To
- SPF
- DKIM
- DMARC
- E-posta kaynaklı IOC'ler

## Phishing ve CTI

Phishing e-postaları, sosyal mühendislik amacı taşımanın yanı sıra CTI analizi açısından önemli teknik göstergeler içerebilir. E-posta başlıkları, gönderen altyapısı, kimlik doğrulama sonuçları ve mesaj içerisinde yer alan bağlantılar saldırının kaynağı ve yöntemi hakkında bilgi sağlayabilir.

## Görünen Gönderici Bilgisi

Bir e-postadaki `From` alanı kullanıcıya görünen gönderici bilgisini içerir. Ancak bu alan tek başına güvenilir bir doğrulama mekanizması değildir.

Bu nedenle `Received`, `Return-Path`, `Reply-To`, `Message-ID` ve `Authentication-Results` alanları birlikte incelenmelidir.

## Received Alanı

`Received` satırları e-postanın hangi sunucular üzerinden iletildiğini gösterir. Burada yer alan IP adresleri araştırılabilir IOC'ler arasında değerlendirilir.

Bir e-postada birden fazla `Received` satırı bulunabileceğinden iletim zinciri dikkatli şekilde analiz edilmelidir.

## Return-Path ve Reply-To

`Return-Path`, teslim edilemeyen mesajların yönlendirileceği adresi; `Reply-To` ise kullanıcının yanıt vermesi durumunda mesajın gideceği adresi gösterir.

Bu alanların görünen gönderici adresinden farklı olması inceleme gerektiren bir göstergedir. Ancak tek başına kötü niyet kanıtı olarak değerlendirilmemelidir.

## SPF, DKIM ve DMARC

SPF, gönderen IP'nin ilgili alan adı adına e-posta gönderme yetkisini kontrol eder. DKIM, mesaj bütünlüğü ve yetkili gönderim hakkında kriptografik doğrulama sağlar. DMARC ise SPF ve DKIM sonuçlarını görünen gönderen alan adıyla birlikte değerlendirir.

`spf=fail`, `dkim=none` veya `dmarc=fail` gibi sonuçlar şüphe seviyesini artırabilir.

## Çıkarılabilecek IOC'ler

Bir phishing e-postasından aşağıdaki göstergeler elde edilebilir:

- Kaynak IP adresi
- Gönderen alan adı
- Return-Path alan adı
- Reply-To adresi
- Mesaj içerisindeki URL'ler
- Ek dosyalara ait hash değerleri
- Şüpheli alt alan adları

## Güvenli Analiz Yaklaşımı

Şüpheli bağlantılar doğrudan açılmamalı, bilinmeyen ekler kontrolsüz ortamlarda çalıştırılmamalı ve araştırma mümkün olduğunca pasif kaynaklar üzerinden yürütülmelidir.

## Sonuç

Phishing e-posta analizi, tek bir mesajdan saldırgan altyapısına ilişkin teknik göstergeler elde edilmesini sağlar. Bu göstergelerin ilişkilendirilmesi, olayın daha geniş bir tehdit kampanyası kapsamında değerlendirilmesine katkı sağlar.

## İlgili Laboratuvar

**Faturayı Kim Gönderdi?**  
Şüpheli bir e-postanın başlık alanlarının incelenmesi, kaynak IP ve alan adı göstergelerinin çıkarılması ve e-posta kimlik doğrulama sonuçlarının değerlendirilmesine yönelik uygulamalı bir laboratuvardır.
