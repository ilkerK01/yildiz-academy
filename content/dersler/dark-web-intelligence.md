---
slug: dark-web-intelligence
order_index: 16
title: Dark Web Intelligence (DARKINT)
summary: Dark web kaynaklarından elde edilen iddiaların güvenli, etik ve kanıta dayalı biçimde değerlendirilmesini anlatan CTI dersi.
tags: [cti, darkint, dark-web, source-validation, opsec]
---

# Dark Web Intelligence (DARKINT)

## Dersin Amacı

Bu ders, dark web üzerinde yer alan bilgilerin Cyber Threat Intelligence (CTI) açısından nasıl değerlendirileceğini öğretir. Amaç, gizli servisleri ziyaret etmeyi veya suç faaliyetlerine katılmayı öğretmek değil; bir iddiayı doğrulamak, kaynağın güvenilirliğini ölçmek ve kuruma yönelik tehdidi raporlamaktır.

## Ana Kavramlar

- Surface Web, Deep Web ve Dark Web
- DARKINT (Dark Web Intelligence)
- Threat Actor, Initial Access Broker (IAB)
- Leak Site, Data Breach, Credential Exposure
- Source Reliability, Information Credibility
- Corroboration (Bağımsız Doğrulama)
- OPSEC (Operational Security)
- TLP (Traffic Light Protocol)
- Collection Requirement ve PIR

## 1. Surface Web, Deep Web ve Dark Web

**Surface Web**, genel arama motorlarının indeksleyebildiği içerikleri ifade eder.

**Deep Web**, arama motorlarınca indekslenmeyen içerikleri kapsar. Bir şirketin dahili portalı veya oturum açılması gereken bir hesap sayfası deep web kapsamına girebilir. Deep web, kendi başına yasa dışı değildir.

**Dark Web**, genellikle özel ağ yazılımlarıyla erişilen, herkese açık arama motorlarında listelenmeyebilen servisleri ifade eder. Tor üzerindeki `.onion` servisleri bunun bilinen örneklerindendir. Dark web yalnızca suç amacıyla kullanılmaz; gizlilik ve sansürü aşma amaçlarıyla da kullanılabilir.

Bu üç kavram birbirinin eş anlamlısı değildir.

## 2. DARKINT CTI Sürecinde Neden Önemlidir?

Bazı fidye yazılımı grupları, çalındığını iddia ettikleri verileri sızıntı sayfalarında duyurabilir. Initial Access Broker (IAB) olarak bilinen aracılar, kurum sistemlerine erişim sattıklarını iddia edebilir. Forumlarda kimlik bilgisi veya veritabanı satış ilanları görülebilir.

Ancak bir paylaşımın mevcut olması **ihlalin gerçekten gerçekleştiğini kanıtlamaz**. İçerik sahte, eski, tekrar yayımlanmış, yanlış kuruma atfedilmiş veya abartılmış olabilir.

CTI analistinin sorusu şudur:

> Bu iddiayı hangi bağımsız kanıtlar destekliyor ve kurum açısından nasıl bir risk oluşturuyor?

## 3. İstihbarat İhtiyacını Belirleme

Araştırmadan önce bir **Priority Intelligence Requirement (PIR)** oluşturulur.

Örnek PIR:

> Kurumumuzla ilişkili erişim satışı veya veri sızıntısı iddiaları var mı ve bunların güncelliği ile güvenilirliği nedir?

Bu soru araştırmanın kapsamını sınırlar. Rastgele içerik toplamak yerine belirli kurum adları, doğrulanmış alan adları, tarih aralıkları ve olay türleri değerlendirilir. Yetkisiz erişim, hesap satın alma veya çalıntı veri indirme araştırmanın zorunlu parçası değildir.

## 4. Başlıca Bilgi Türleri

### Veri sızıntısı iddiaları

Bir saldırgan, kuruma ait verileri elde ettiğini ileri sürebilir. İddia edilen veri türü, yayın tarihi ve bağımsız doğrulama imkanları değerlendirilir. Hassas veriyi indirmek veya yaymak yerine kamuya açık ihlal bildirimleri ve kurumla yetkili koordinasyon tercih edilir.

### Initial Access Broker ilanları

İlanda erişim türü (örneğin VPN veya RDP), hedef sektör ve coğrafya belirtilmiş olabilir. Bunlar doğrulanmamış iddialardır; ilan üzerinden satın alma veya erişim testi yapılmaz.

### Kimlik bilgisi ifşası

E-posta adresleri ya da kurumsal alan adlarıyla ilgili ifşa iddiaları görülebilir. Analist, çalıntı parolaları toplamadan kurumun yetkili güvenlik ekibini bilgilendirir; parola sıfırlama ve MFA kontrolleri önerebilir.

### Ransomware leak site duyuruları

Bir grubun mağdur listesine şirket eklemesi operasyonel açıdan önemli olabilir ancak olayın ölçeği veya belirtilen veri miktarı ayrıca doğrulanmalıdır.

## 5. Kaynak Güvenilirliği ve Bilgi Doğruluğu

İki farklı unsur değerlendirilmelidir:

- **Source Reliability:** Kaynağın geçmiş paylaşımları ne kadar tutarlı ve güvenilirdi?
- **Information Credibility:** Bu belirli iddia hangi kanıtlarla doğrulanıyor?

Geçmişte doğru bilgi paylaşmış bir kaynak bile bu kez yanlış iddiada bulunabilir.

Doğrulamada şu sorular yardımcı olur:

1. İddia ne zaman ortaya çıktı? Aynı içerik daha önce yayımlanmış mı?
2. Hedef kurum açıkça ve doğru biçimde tanımlanmış mı?
3. Birbirinden bağımsız güvenilir kaynaklar aynı olayı doğruluyor mu?
4. CERT duyurusu, kurum açıklaması veya doğrulanmış olay kaydı var mı?
5. Ekran görüntüsünün veya metnin bağlamı değişmiş olabilir mi?

**Önemli:** Bir iddiayı farklı sitelerin aynen kopyalaması bağımsız doğrulama değildir.

## 6. OPSEC, Hukuk ve Etik Sınırlar

DARKINT araştırmalarında kişisel ve kurumsal güvenlik önceliklidir:

- Kurumun onaylı araştırma ortamını ve yazılı prosedürlerini kullanın.
- Şüpheli dosyaları indirmeyin ve çalıştırmayın.
- Çalıntı verileri, parolaları veya yetkisiz erişimleri satın almayın.
- Aktörlerle izinsiz iletişim kurmayın; gerçek kurumsal kimlik bilgilerini paylaşmayın.
- Hukuka aykırı kişisel veri işlemeden kaçının; erişim ve saklama yetkilerini denetleyin.
- Bulgular için erişim kontrolü, redaksiyon ve uygun TLP etiketlerini uygulayın.

Teknik bir ağ aracının kullanılması tek başına anonimlik veya yasal uygunluk garantisi vermez.

## 7. Kurgusal Vaka: Veri Sızıntısı İddiası

Tamamen kurgusal bir senaryo düşünelim:

Bir izleme raporu, `example-corp.test` şirketine ait müşteri kayıtlarının sızdırıldığını iddia eden bir forum gönderisinden söz ediyor. Gönderi, 20.000 kayıttan bahsediyor ancak doğrulanmış bir örnek veya bağımsız kaynak sunmuyor.

**Adım 1 — İddiayı kaydet:** Kaynağın sınıfını, ilk görülme tarihini, iddia edilen veri türünü ve paylaşımın referansını kaydet. Gereksiz kişisel veri kopyalama.

**Adım 2 — Bağımsız doğrulama ara:** Şirketin yayımladığı güvenlik bildirimi, CERT açıklaması veya güvenilir olay raporunu araştır.

**Adım 3 — Alternatif açıklamaları değerlendir:** Eski sızıntının yeniden pazarlanması, yanlış hedef eşleştirmesi veya tamamen sahte bir ilan olabilir.

**Adım 4 — Güven düzeyi belirt:** Doğrulayıcı kaynak yoksa 'ihlâl doğrulandı' deme. Örneğin: *Düşük güven — doğrulanmamış veri sızıntısı iddiası.*

**Adım 5 — Savunma önerisi hazırla:** Yetkili ekibe ilgili sistemlerin izlenmesi, hesap güvenliği kontrolleri ve olay müdahale hazırlığının gözden geçirilmesini öner.

Bu olayın analitik sonucu **bir iddianın raporlanmasıdır**, gerçek bir veri ihlalinin kesinleşmesi değildir.

## 8. Örnek CTI Bilgi Notu

**Konu:** Example Corp hakkında doğrulanmamış veri sızıntısı iddiası
**Kaynak:** İkinci el izleme raporu
**Gözlem:** Kurgusal bir forum gönderisinde müşteri kayıtlarının elde edildiği ileri sürülmektedir.
**Doğrulama:** Bağımsız doğrulama bulunmamıştır.
**Güven düzeyi:** Düşük
**Olası etki:** İddia doğruysa veri gizliliği ve kimlik avı riski
**Öneri:** İlgili güvenlik ekibine iletme, doğrulama çalışması, izleme ve önleyici hesap kontrolleri
**Paylaşım:** Kurum politikasına göre uygun TLP etiketiyle

## 9. Mini Alıştırma

Bir gönderide şu ifade yer alıyor:

> “Büyük bir finans kurumunun VPN erişimi satılık. Kanıt isteyen özel mesaj atsın.”

**Sorular:**

1. Bu ifade tek başına bir kurumun ihlal edildiğini kanıtlar mı?
2. Hangi bilgiler eksik ve hangi alternatif açıklamalar mümkündür?
3. Analist hangi güvenli doğrulama adımlarını önermelidir?
4. Bulguyu yönetime iletirken güven düzeyi nasıl açıklanmalıdır?

**Kısa cevap:** Hayır. Kurum kimliği, tarih, kanıtın güvenilirliği ve bağımsız teyit yoktur. Erişimi satın almak veya test etmek yerine kurumsal yetkililerle koordineli doğrulama gerekir; raporda belirsizlik açıkça belirtilmelidir.

## Sonuç

DARKINT, dark web üzerinde görülen her iddiayı doğru kabul etmek değil, **doğrulanmamış veriyi bağlamlandırarak karar destekleyici istihbarata dönüştürmektir**. Başarılı bir çalışma; doğru PIR, kaynak değerlendirmesi, bağımsız doğrulama, OPSEC ve ölçülü raporlamaya dayanır.
