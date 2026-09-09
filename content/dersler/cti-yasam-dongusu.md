---
slug: cti-yasam-dongusu
order_index: 7
title: CTI Yaşam Döngüsü
summary: Tehdit istihbaratının ihtiyaç belirlemeden geri bildirime kadar hangi aşamalardan geçtiğini açıklayan temel süreç.
tags: [cti, cti-temelleri, intelligence-cycle]
---

# CTI Yaşam Döngüsü

## Dersin Amacı

Bu dersin amacı, siber tehdit istihbaratının yalnızca veri toplamak veya IOC listeleri oluşturmak olmadığını açıklamaktır. CTI çalışmalarının belirli bir ihtiyaçla başlayıp bilginin toplanması, işlenmesi, analiz edilmesi, ilgili kişilere aktarılması ve geri bildirim alınmasıyla devam eden sistematik bir süreç olduğu ele alınmaktadır.

## Ana Kavramlar

- Planning and Direction
- Collection
- Processing
- Analysis
- Dissemination
- Feedback
- Intelligence Requirement
- PIR (Priority Intelligence Requirement)
- İstihbarat tüketicisi

## CTI Yaşam Döngüsü Nedir?

CTI yaşam döngüsü, ham verinin karar vermede kullanılabilecek tehdit istihbaratına dönüştürülmesi için izlenen aşamaları ifade eder.

Bu süreç doğrusal görünse de uygulamada sürekli tekrar eder. Bir analiz sonucunda ortaya çıkan yeni sorular, yeni veri toplama ihtiyaçlarına yol açabilir.

Genel olarak süreç şu şekilde gösterilebilir:

`Planlama → Toplama → İşleme → Analiz → Dağıtım → Geri Bildirim`

Amaç mümkün olduğunca fazla veri toplamak değil, doğru soruya cevap verecek istihbaratı üretmektir.

## 1. Planning and Direction

İlk aşamada hangi soruların cevaplanması gerektiği belirlenir.

Bir kuruluş için örnek sorular şunlar olabilir:

- Hangi tehdit aktörleri sektörümüzü hedefliyor?
- Hangi ransomware grupları bölgemizde aktif?
- Kurumumuzun kullandığı teknolojiler hangi tehditlerle ilişkilendiriliyor?
- Belirli bir kampanyanın kurumumuz için oluşturduğu risk nedir?

Bu aşamada istihbaratı kimin kullanacağı da belirlenmelidir.

SOC ekibi teknik IOC'lerle ilgilenebilirken yöneticiler saldırının iş etkisini ve risk seviyesini bilmek isteyebilir.

## Intelligence Requirement

İstihbarat ihtiyacı, analistin hangi soruya cevap üretmesi gerektiğini tanımlar.

Öncelikli ve kritik sorular genellikle **Priority Intelligence Requirement (PIR)** olarak ifade edilir.

Örneğin:

> Finans sektörünü hedefleyen ve kimlik avı kullanan aktif tehdit grupları hangileridir?

Bu soru veri toplama ve analiz sürecinin yönünü belirler.

Belirli bir ihtiyaç olmadan toplanan büyük miktarda veri, doğrudan istihbarat anlamına gelmez.

## 2. Collection

Bu aşamada belirlenen sorulara cevap verebilmek için gerekli veriler toplanır.

Kaynaklar arasında şunlar bulunabilir:

- Açık kaynaklar
- Güvenlik üreticilerinin raporları
- IOC paylaşım platformları
- Malware analiz servisleri
- Kurum içi loglar
- SIEM kayıtları
- EDR verileri
- CERT ve kamu kurumu yayınları
- Dark web veya tehdit aktörü kaynakları

Kaynak seçimi araştırma sorusuna göre yapılmalıdır.

Bir IP adresinin geçmişini araştırmak ile belirli bir tehdit aktörünün hedef sektörlerini araştırmak aynı veri kaynaklarını gerektirmeyebilir.

## 3. Processing

Toplanan veriler çoğu zaman doğrudan analiz edilebilir durumda değildir.

Processing aşamasında ham veri düzenlenir ve analize uygun hale getirilir.

Bu işlemler arasında:

- Tekrarlanan kayıtların kaldırılması
- IOC'lerin normalize edilmesi
- Tarih ve zaman bilgilerinin düzenlenmesi
- Dosya formatlarının dönüştürülmesi
- Verilerin sınıflandırılması
- İlgisiz kayıtların elenmesi
- Farklı kaynaklardan gelen verilerin ortak yapıya getirilmesi

bulunabilir.

Örneğin farklı kaynaklardan elde edilen IP adresleri ve domain kayıtları tek bir çalışma tablosunda birleştirilebilir.

## 4. Analysis

Analysis aşaması CTI sürecinin en önemli bölümlerinden biridir.

Bu aşamada işlenmiş veriler değerlendirilerek anlamlı sonuçlar üretilir.

Analist şu tür sorulara cevap arayabilir:

- Farklı IOC'ler aynı altyapıya mı ait?
- İki kampanya arasında ortak TTP'ler var mı?
- Belirli bir tehdit aktörü kurum için gerçekten ilgili mi?
- Gözlenen faaliyet daha önce bilinen bir kampanyayla ilişkili olabilir mi?
- Kaynakların güvenilirliği ne seviyede?

Analiz yalnızca verileri yan yana koymak değildir. Veriler arasındaki ilişkilerin ve bağlamın değerlendirilmesi gerekir.

## Veri ile İstihbarat Arasındaki Fark

Bir IP adresinin tek başına bulunması veridir.

Bu IP'nin son dönemde belirli bir zararlı yazılım ailesinin C2 altyapısıyla ilişkili olduğunun belirlenmesi bilgidir.

Aynı altyapının kurumun faaliyet gösterdiği sektörü hedefleyen aktif bir kampanyada kullanıldığının değerlendirilmesi ise karar vermeye yardımcı olan istihbarata dönüşebilir.

Bu nedenle analiz aşamasında bağlam kritik öneme sahiptir.

## 5. Dissemination

Üretilen istihbarat doğru kişiye, doğru formatta ve doğru zamanda ulaştırılmalıdır.

Aynı analiz farklı kullanıcılara farklı biçimde sunulabilir.

Örneğin SOC ekibi için:

- IP adresleri
- Domain'ler
- Hash değerleri
- YARA veya Sigma kuralları
- MITRE ATT&CK teknikleri

önemli olabilir.

Yönetim için ise:

- Tehdidin kurum açısından önemi
- Hedeflenen sektör
- Olası iş etkisi
- Risk seviyesi
- Önerilen aksiyonlar

daha anlamlıdır.

İyi bir istihbarat raporu, hedef kitlenin ihtiyaçlarına göre hazırlanmalıdır.

## 6. Feedback

Yaşam döngüsünün son aşaması geri bildirimdir.

İstihbaratı kullanan kişilerden şu tür soruların cevapları alınabilir:

- Üretilen bilgi ihtiyacı karşıladı mı?
- Daha fazla teknik detay gerekiyor mu?
- Analiz zamanında ulaştı mı?
- Yeni bir araştırma sorusu ortaya çıktı mı?
- Hangi konuların düzenli takip edilmesi gerekiyor?

Bu geri bildirim bir sonraki CTI döngüsünün planlama aşamasını şekillendirir.

Bu nedenle CTI yaşam döngüsü sona eren değil, sürekli gelişen bir süreçtir.

## Örnek CTI Döngüsü

Bir finans kuruluşunun phishing kampanyalarıyla ilgili tehdit istihbaratı üretmek istediğini düşünelim.

**Planlama:** Finans sektörünü hedefleyen aktif phishing grupları araştırılacak.

**Toplama:** Güvenlik raporları, phishing IOC'leri, e-posta örnekleri ve tehdit aktörü kayıtları toplanacak.

**İşleme:** Domain, IP, URL ve tarih bilgileri düzenlenecek ve tekrar eden kayıtlar kaldırılacak.

**Analiz:** Ortak altyapılar, kullanılan TTP'ler ve tehdit aktörü ilişkileri incelenecek.

**Dağıtım:** SOC ekibine teknik IOC'ler, yönetime ise risk ve hedef profili aktarılacak.

**Geri Bildirim:** SOC ekibinin yeni bulguları ve ihtiyaçları doğrultusunda araştırma yeniden yönlendirilecek.

## Sonuç

CTI yaşam döngüsü, tehdit verisinin sistematik şekilde karar verilebilir istihbarata dönüştürülmesini sağlar.

Başarılı bir CTI çalışmasının başlangıç noktası araç veya veri kaynağı değil, cevaplanması gereken doğru sorudur.

Süreç genel olarak şu ilişki üzerinden ilerler:

`İhtiyaç → Veri → Analiz → İstihbarat → Karar → Geri Bildirim`

Bu yaklaşım CTI çalışmalarının yalnızca IOC toplamaktan çıkıp kurumun gerçek güvenlik ihtiyaçlarına hizmet etmesini sağlar.