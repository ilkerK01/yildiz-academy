---
slug: cti-automation
order_index: 19
title: Cyber Threat Intelligence Automation
summary: Python ile IOC ayıklama, doğrulama, normalizasyon, tekrarları temizleme, güvenli API zenginleştirme ve otomatik CTI raporu üretme süreci.
tags: [cti, automation, python, ioc, enrichment, api]
---

# Cyber Threat Intelligence Automation

## Dersin Amacı

Bu ders, CTI analistinin tekrarlanan veri işleme görevlerini Python kullanarak nasıl otomatikleştirebileceğini öğretir. Amaç yalnızca daha hızlı IOC toplamak değildir; doğrulanabilir, tutarlı ve bağlamı korunmuş istihbarat üretmektir.

## Ana Kavramlar

- CTI Automation
- IOC Parsing ve Validation
- Normalization ve Deduplication
- Enrichment ve Context
- API, JSON ve Rate Limiting
- False Positive ve Data Provenance
- Confidence ve Timestamp
- Intelligence Pipeline

## 1. CTI Otomasyonu Nedir?

Bir analist farklı kaynaklardan IP adresleri, domain'ler, URL'ler ve hash değerleri toplar. Bu göstergeler farklı biçimlerde yazılmış, tekrarlanmış veya güncelliğini yitirmiş olabilir. Otomasyon, bu verilerin belirli kurallarla işlenmesini ve incelenmeye hazır hale getirilmesini sağlar.

Örnek bir iş akışı:

`Kaynaklar → Toplama → Ayrıştırma → Doğrulama → Normalizasyon → Tekrarları Temizleme → Zenginleştirme → Analiz → Rapor`

**Önemli:** Bir IOC'nin bir tehdit akışında görülmesi, tek başına kötü amaçlı olduğunun kanıtı değildir.

## 2. IOC Parsing ve Validation

Parsing, ham metinden göstergeleri ayırmaktır. Validation ise çıkarılan değerin ilgili veri türüne uygun olup olmadığını denetler.

Örnekler:

- IP: `198.51.100.24`
- Domain: `sample.example`
- URL: `https://sample.example/login`
- SHA-256: 64 karakterlik hexadecimal değer

Buradaki adresler dokümantasyon ve eğitim için kullanılmıştır; gerçek saldırı altyapısını temsil etmez.

**Parsing ile doğrulama farklı işlemlerdir.** Regex ile IP benzeri dizeler yakalanabilir; `ipaddress` modülü ise IP'nin gerçekten geçerli olup olmadığını kontrol eder.

## 3. Normalization ve Deduplication

Aynı domain büyük/küçük harf farkıyla gelebilir: `EXAMPLE.ORG` ve `example.org`. Normalizasyon bunları aynı biçime getirir. Deduplication ise yinelenen kayıtları ayıklar.

Normalizasyon sırasında önemli ayrıntılar kaybedilmemelidir. Örneğin URL path'i ve query parametreleri olay bağlamını etkileyebilir. Domain normalizasyonunun tüm URL'yi değiştirmesine izin verilmemelidir.

## 4. Python ile Basit IOC İşleme

Aşağıdaki örnek **yalnızca yerel, kurgusal IP verisi** işler. Ağ isteği göndermez.

```python
import ipaddress
import json

raw_ips = [
    " 198.51.100.24 ",
    "198.51.100.24",
    "203.0.113.8",
    "999.10.10.10",
    "2001:db8::1",
]

valid_ips = set()
invalid_values = []

for raw in raw_ips:
    value = raw.strip()
    try:
        valid_ips.add(str(ipaddress.ip_address(value)))
    except ValueError:
        invalid_values.append(value)

report = {
    "indicator_type": "ip",
    "indicators": sorted(valid_ips),
    "unique_count": len(valid_ips),
    "invalid_values": invalid_values,
}

print(json.dumps(report, indent=2, ensure_ascii=False))
```

Bu program geçerli üç benzersiz IP adresi bulur ve geçersiz kaydı ayrıca raporlar. Ancak IP'nin zararlı olduğuna dair bir hüküm vermez.

## 5. Enrichment: IOC'ye Bağlam Ekleme

Enrichment, göstergeyi ek bilgilerle zenginleştirmedir. Kaynağa göre şu bilgiler alınabilir:

- İlk ve son görülme zamanı
- İlgili malware family veya kampanya
- ASN ve barındırma bilgisi
- İlgili MITRE ATT&CK teknikleri
- Kaynak sayısı ve kaynak güvenilirliği
- Gözlemin güncelliği

VirusTotal, URLhaus, MalwareBazaar veya benzeri servisler, **kendi erişim ve kullanım koşulları** çerçevesinde değerlendirilebilir. Kaynakların sonuçlarını birbirinden bağımsız kanıtlar gibi saymamak gerekir; birkaç servis aynı ilk kaydı yeniden yayımlıyor olabilir.

## 6. API Kullanımında Güvenlik

Harici servisle entegrasyonda şu kurallara dikkat edilmelidir:

1. API anahtarını kaynak koda yazma; ortam değişkeninde veya bir secret manager içinde sakla.
2. Timeout belirle; geçici hatalarda kontrollü yeniden deneme (backoff) kullan.
3. Servisin rate limit ve kullanım koşullarına uy.
4. Kişisel veri, müşteri bilgisi veya gizli kurum içi IOC'leri yetkisiz servislere gönderme.
5. Gelen JSON'un alanlarını ve veri tiplerini doğrula.
6. Her sonucun kaynağını, sorgu zamanını ve hata durumunu kaydet.
7. Otomatik IOC engelleme kararlarını analist onayı ve kurum politikasına bağla.

**Önemli:** Veri zenginleştirme ile otomatik engelleme aynı işlem değildir. Yanlış pozitifler iş sürekliliğini etkileyebilir.

## 7. Örnek CTI Otomasyon Senaryosu

Bir SOC ekibi farklı güvenlik raporlarında geçen IP göstergelerini haftalık olarak değerlendiriyor.

**Toplama:** Raporlardan yalnızca analiz için izin verilen IOC'ler alınır.

**İşleme:** IP değerleri doğrulanır, standartlaştırılır ve tekrarlar kaldırılır.

**Zenginleştirme:** Yetkili kaynaklardan ilk görülme zamanı ve tehdit ilişkileri alınır.

**Analiz:** Kaynak güvenilirliği, IOC güncelliği ve kurumun kendi telemetrisi birleştirilir.

**Dağıtım:** SOC için teknik liste, yönetim için kısa risk değerlendirmesi hazırlanır.

**Geri bildirim:** Hatalı pozitifler ve eski göstergeler bir sonraki çalışmada filtrelenir.

## 8. Örnek JSON Raporu

```json
{
  "report_type": "ioc_processing_summary",
  "source": "training_dataset",
  "indicator_type": "ip",
  "unique_count": 3,
  "enrichment_status": "not_performed",
  "assessment": "Indicators require context and analyst review",
  "recommended_action": "Correlate with internal telemetry before taking action"
}
```

Bu örnekte işlem sonuçlarıyla analistin güvenlik değerlendirmesi ayrı tutulmuştur.

## 9. Sınırlamalar ve Kalite Kontrolü

Otomasyonun yanlış veya eskimiş kaynaklardan gelen veriyi hızlı şekilde çoğaltma riski vardır. Bu yüzden pipeline sonuçları düzenli olarak kontrol edilmelidir:

- Yanlış pozitif oranı
- Eksik veya hatalı alanlar
- Güncelliğini kaybetmiş IOC'ler
- Kaynaklar arasında yinelenen iddialar
- API hata oranları ve veri işleme süreleri
- İnsan incelemesi gerektiren bulgular

Bir istihbarat üretim hattı **hızlı** olduğu kadar **izlenebilir ve denetlenebilir** olmalıdır.

## Mini Alıştırma

Bir veri kümesinde 500 IOC kaydı var; normalizasyondan sonra 320 benzersiz gösterge kalıyor. Zenginleştirme servisi 40 istek için hata döndürüyor ve 60 IOC'nin son görülme tarihi çok eski.

1. Kaç yinelenen kayıt kaldırılmıştır?
2. API hatalarını nasıl raporlarsın?
3. Eski IOC'leri doğrudan engelleme listesine eklemek neden risklidir?
4. Analiste hangi üç bilgiyi öncelikli gösterirsin?

**Kontrol:** 180 yinelenen kayıt kaldırılmıştır. Başarısız enrichment sorguları 'temiz' sonucuyla karıştırılmamalı, ayrı hata durumu olarak saklanmalıdır.

## Sonuç

CTI otomasyonu ham göstergelerin doğrulanmasına, temizlenmesine ve bağlamla ilişkilendirilmesine yardımcı olur. Güvenilir bir çözüm; veri kökenini, zamanı, hata durumlarını ve analist kararını görünür tutar. Son kararı yalnızca otomasyon sistemine bırakmak yerine kanıt temelli değerlendirme yapmak gerekir.