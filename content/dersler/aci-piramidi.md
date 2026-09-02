---
title: Acı piramidi
slug: aci-piramidi
summary: Saldırgana hangi göstergeyi engelleyerek ne kadar acı verdiğini gösteren model.
tags: [cti-temelleri, hash-analizi]
order_index: 2
reading_minutes: 4
published: true
---

David Bianco'nun 2013'te önerdiği model, bir göstergeyi (indicator) engellemenin
saldırgana ne kadar maliyet yüklediğini sıralar. Aşağıdan yukarı doğru
saldırganın işi zorlaşır.

## Basamaklar

1. **Hash değerleri.** Engellemesi en kolay, saldırganın atlatması en ucuz.
   Dosyada tek bir bayt değişince hash değişir.
2. **IP adresleri.** Biraz daha zahmetli ama bulut sağlayıcıda yeni adres almak
   dakikalar sürer.
3. **Alan adları.** Kayıt ve yapılandırma gerektirir, biraz daha pahalı.
4. **Ağ ve host artefaktları.** Kullanıcı ajanı dizgileri, kayıt defteri
   anahtarları, dosya yolları. Saldırganın araçlarını değiştirmesi gerekir.
5. **Araçlar.** Kullandığı yazılımı bırakmak zorunda kalır.
6. **TTP'ler.** Taktik, teknik ve prosedürler. Burayı tespit edersen saldırgan
   çalışma biçimini değiştirmek zorunda kalır ki bu gerçekten pahalıdır.

## Pratikte ne anlama geliyor

Bir hash listesi engellemek kötü bir şey değildir, ucuzdur ve otomatiktir. Ama
savunma programının **tamamı** piramidin dibindeyse, saldırgan hiçbir zaman acı
çekmez.

Tespit yatırımı yukarı doğru kaydıkça pahalılaşır ve yavaşlar, ama kalıcı olur.
Bir TTP tespiti yıllarca çalışabilir; bir hash imzası bir hafta çalışır.

## Bunu labda görmek

`hash-avi` laboratuvarı tam olarak piramidin en alt basamağıyla çalışır: eline
bir hash verilir ve o hashten yukarı doğru çıkman beklenir.
