---
slug: osint-arastirma-kaynak-dogrulama
order_index: 8
title: OSINT Araştırma ve Kaynak Doğrulama
summary: Açık kaynaklardan bilgi toplarken kaynağın güvenilirliğini, bilginin doğruluğunu ve araştırma sürecinin izlenebilirliğini değerlendirme yöntemleri.
tags: [osint, cti, kaynak-dogrulama]
---

# OSINT Araştırma ve Kaynak Doğrulama

## Dersin Amacı

Bu dersin amacı, OSINT çalışmalarında yalnızca bilgi bulmanın yeterli olmadığını açıklamaktır. Bir CTI analisti için asıl önemli olan, bulunan bilginin kaynağını değerlendirmek, başka kaynaklarla doğrulamak ve araştırmanın nasıl yapıldığını kayıt altına almaktır.

OSINT araştırmalarında yanlış, eski veya bağlamından koparılmış bilgiler analiz sonucunu doğrudan etkileyebilir.

## Ana Kavramlar

- OSINT
- Kaynak güvenilirliği
- Bilgi doğrulama
- Cross-check
- Birincil kaynak
- İkincil kaynak
- Pivoting
- Metadata
- Araştırma izi
- Confidence Level

## OSINT Nedir?

OSINT, **Open Source Intelligence** ifadesinin kısaltmasıdır.

Herkese açık veya yasal şekilde erişilebilen kaynaklardan bilgi toplama, bu bilgiyi değerlendirme ve anlamlı sonuçlar üretme sürecidir.

OSINT kaynağı yalnızca arama motorları değildir.

Araştırmalarda şu tür kaynaklarla karşılaşılabilir:

- Haber siteleri
- Resmî kurum yayınları
- Güvenlik şirketlerinin raporları
- Sosyal medya
- Alan adı kayıtları
- Sertifika kayıtları
- GitHub gibi açık kod platformları
- Malware analiz servisleri
- İnternet arşivleri
- Forumlar
- Tehdit aktörlerinin herkese açık paylaşımları

Buradaki temel problem bilgiye ulaşmaktan çok, bulunan bilginin ne kadar güvenilir olduğunu anlamaktır.

## Araştırmaya Soruyla Başlamak

İyi bir OSINT araştırması doğrudan araç kullanarak başlamamalıdır.

Önce cevaplanması gereken soru belirlenmelidir.

Örneğin elimizde şüpheli bir domain bulunduğunu düşünelim:

`secure-example-login.com`

Doğrudan onlarca farklı serviste arama yapmak yerine önce araştırma soruları oluşturulabilir.

Domain ne zaman oluşturuldu?

Hangi IP adresleriyle ilişkili?

Daha önce zararlı faaliyetlerde görüldü mü?

Başka hangi domainlerle ortak altyapı kullanıyor?

Bilinen bir saldırı kampanyasıyla bağlantısı var mı?

Sorular belirlendiğinde hangi kaynakların kullanılması gerektiği de daha kolay anlaşılır.

## Birincil ve İkincil Kaynaklar

Kaynakları değerlendirirken bilginin nereden geldiğini anlamak önemlidir.

**Birincil kaynak**, olay veya veriyle doğrudan ilişkili kaynaktır.

Örneğin:

Bir kurumun kendi yayınladığı güvenlik duyurusu veya doğrudan incelenmiş bir malware örneğine ait teknik analiz birincil kaynağa daha yakın olabilir.

**İkincil kaynak** ise başka kaynaklardan aldığı bilgiyi yorumlayan veya tekrar yayımlayan kaynaktır.

Örneğin bir güvenlik haber sitesinin başka bir şirketin araştırmasını özetlemesi ikincil kaynak olabilir.

İkincil kaynaklar değersiz değildir ancak kritik bir bulgu mümkün olduğunda ilk kaynağa kadar takip edilmelidir.

## Kaynak Güvenilirliğini Değerlendirmek

Bir kaynağı kullanırken yalnızca profesyonel görünmesine bakmak yeterli değildir.

Şu sorular değerlendirilebilir:

Kaynağı kim yayımladı?

Kaynak daha önce güvenilir bilgi sağladı mı?

Bilginin yayımlanma tarihi nedir?

İddianın arkasında teknik kanıt bulunuyor mu?

Başka bağımsız kaynaklar aynı bilgiyi destekliyor mu?

Kaynak kendi gözlemini mi paylaşıyor, başka bir kaynağı mı tekrar ediyor?

Örneğin bir forum kullanıcısının:

> Bu IP APT grubuna ait.

şeklindeki mesajı tek başına attribution yapmak için yeterli değildir.

Ancak aynı IP farklı teknik raporlarda, malware analizlerinde ve ağ kayıtlarında aynı kampanyayla ilişkilendiriliyorsa bulgunun güven seviyesi artabilir.

## Cross-check Nedir?

Cross-check, bir bilgiyi farklı kaynaklarla karşılaştırarak doğrulamaya çalışma sürecidir.

Örneğin bir domainin belirli bir tehdit aktörüyle ilişkili olduğu iddia ediliyorsa şu kaynaklardan destek aranabilir:

Passive DNS kayıtları,

Threat intelligence platformları,

Malware sandbox raporları,

Güvenlik üreticilerinin araştırmaları,

Sertifika kayıtları.

Ancak burada önemli bir ayrıntı vardır.

Beş farklı web sitesinin aynı bilgiyi göstermesi, mutlaka beş bağımsız kaynak olduğu anlamına gelmez.

Bu sitelerin tamamı aynı threat feed üzerinden veri alıyor olabilir.

Bu yüzden sadece kaynak sayısını değil, **kaynakların birbirinden bağımsız olup olmadığını** da değerlendirmek gerekir.

## Tarih Neden Önemlidir?

CTI verisinin önemli bir bölümü zamanla değer kaybedebilir.

Bir IP adresi geçen yıl kötü amaçlı bir C2 sunucusu olarak kullanılmış olabilir, ancak bugün aynı IP başka bir sisteme atanmış olabilir.

Benzer şekilde bir domain geçmişte phishing için kullanılmış ancak daha sonra el değiştirmiş olabilir.

Bu nedenle araştırmada:

İlk görülme tarihi,

Son görülme tarihi,

Rapor tarihi,

Kayıt tarihi,

Gözlem tarihi

birbirinden ayrılmalıdır.

Eski bir IOC'nin bugün hâlâ aktif olduğunu varsaymak yanlış sonuçlara yol açabilir.

## Pivoting

OSINT ve CTI araştırmalarında bir bulgudan başka bir bulguya geçme işlemine **pivoting** denir.

Örneğin araştırma şu şekilde ilerleyebilir:

`Domain → IP → Aynı IP'deki diğer domainler → Sertifika → Başka altyapılar`

veya:

`Malware hash → C2 domain → IP → İlişkili kampanya`

Pivoting araştırmanın kapsamını genişletir.

Ancak her bulunan ilişkinin tehdit ilişkisi olmadığı unutulmamalıdır.

Örneğin aynı IP üzerinde iki domain bulunması, iki domainin mutlaka aynı tehdit aktörüne ait olduğunu göstermez. Paylaşımlı hosting kullanılıyor olabilir.

Bu nedenle pivot sonucunda bulunan ilişkiler ayrıca doğrulanmalıdır.

## Metadata Kullanımı

Metadata, bir veri hakkında ek bilgiler sağlar.

Örneğin bir dosyanın metadata alanlarında:

- Oluşturulma zamanı
- Dosya türü
- Kullanılan yazılım
- Yazar bilgisi
- Dil
- Coğrafi bilgi

bulunabilir.

Ancak metadata kolaylıkla değiştirilebilir.

Bu nedenle metadata tek başına güçlü bir attribution kanıtı olarak değerlendirilmemelidir.

Metadata bir **araştırma başlangıç noktası** olabilir ancak başka kaynaklarla desteklenmelidir.

## Araştırma İzi Tutmak

Bir CTI analistinin yaptığı araştırmanın daha sonra tekrar edilebilir olması önemlidir.

Araştırma sırasında aşağıdaki bilgilerin kaydedilmesi yararlıdır:

- Kullanılan kaynak
- Erişim tarihi
- Aranan değer
- Elde edilen sonuç
- Sonucun güvenilirlik değerlendirmesi
- Yapılan pivotlar
- Analistin çıkardığı sonuç

Örneğin:

`09.09.2026 — example.com — Passive DNS sorgusu — 203.0.113.10 IP adresiyle ilişki bulundu.`

şeklinde bir kayıt tutulabilir.

Bu yöntem daha sonra analizin nasıl üretildiğinin anlaşılmasını sağlar.

## Gerçek ile Değerlendirmeyi Ayırmak

CTI raporlamasında gözlemlenen gerçek ile analistin değerlendirmesi birbirinden ayrılmalıdır.

Örneğin:

**Gerçek:**

Domain, 8 Eylül tarihinde `203.0.113.10` IP adresine çözülmüştür.

**Değerlendirme:**

Bu IP'nin daha önce aynı phishing kampanyasında kullanıldığı göz önüne alındığında domainin kampanyayla ilişkili olma ihtimali yüksektir.

İkinci ifade bir analiz sonucudur.

Bu ayrım özellikle attribution çalışmalarında önemlidir.

## Confidence Level

Her CTI sonucu aynı kesinlik seviyesinde değildir.

Bu nedenle analistler değerlendirmelerini belirli güven seviyeleriyle ifade edebilir.

Örneğin:

**Düşük güven:** Sınırlı veya doğrulanmamış kanıt mevcut.

**Orta güven:** Birden fazla veri noktası değerlendirmeyi destekliyor ancak önemli belirsizlikler bulunuyor.

**Yüksek güven:** Birden fazla güvenilir ve bağımsız kaynak değerlendirmeyi güçlü şekilde destekliyor.

Confidence level kullanmak analistin "kesin biliyoruz" ile "eldeki veriler bunu gösteriyor" arasındaki farkı ifade etmesini sağlar.

## Yaygın OSINT Hataları

OSINT araştırmalarında sık yapılan hatalardan biri ilk bulunan sonucu doğru kabul etmektir.

Aynı şekilde eski IOC'leri güncelmiş gibi değerlendirmek, bir sosyal medya paylaşımını bağımsız doğrulama olmadan kullanmak veya aynı kaynaktan veri alan farklı servisleri bağımsız kanıt olarak görmek analiz kalitesini düşürebilir.

Bir başka hata ise korelasyonu doğrudan attribution olarak değerlendirmektir.

İki sistem arasında teknik ilişki bulunması, otomatik olarak aynı tehdit aktörü tarafından yönetildiklerini kanıtlamaz.

## Örnek Araştırma

Bir analistin elinde şüpheli bir domain olduğunu düşünelim:

`invoice-example.com`

İlk araştırmada domainin kısa süre önce kaydedildiği görülüyor.

Passive DNS sorgusunda belirli bir IP adresi bulunuyor.

Aynı IP üzerinde benzer isimlere sahip başka domainler tespit ediliyor.

Malware analiz servisinde bu domainlerden birinin zararlı bir dosya tarafından C2 olarak kullanıldığı görülüyor.

Bir güvenlik şirketinin raporunda da aynı altyapının yakın zamanda gerçekleştirilen bir phishing kampanyasında kullanıldığı belirtiliyor.

Bu noktada analist tek bir kaynağa değil, birden fazla bulguya dayanarak değerlendirme yapabilir.

Ancak yine de:

> Bu domain kesin olarak X grubuna aittir.

demek yerine eldeki kanıt seviyesine uygun bir değerlendirme yapılmalıdır.

## Sonuç

OSINT araştırmasının amacı yalnızca internette bilgi bulmak değildir.

İyi bir CTI analisti şu üç soruyu sürekli sorar:

**Bu bilgiyi nereden aldım?**

**Bu bilgi ne kadar güvenilir?**

**Başka bir kaynakla doğrulayabilir miyim?**

OSINT verisi ancak doğrulama, bağlam ve analiz eklendiğinde tehdit istihbaratına dönüşür.