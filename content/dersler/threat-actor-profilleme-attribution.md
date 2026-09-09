---
slug: threat-actor-profilleme-attribution
order_index: 9
title: Threat Actor Profilleme ve Attribution
summary: Tehdit aktörlerini davranış, altyapı, hedef ve kampanya özellikleri üzerinden profilleme ve attribution çalışmalarındaki belirsizlikleri değerlendirme.
tags: [cti, threat-actor, attribution, apt]
---

# Threat Actor Profilleme ve Attribution

## Dersin Amacı

Bu dersin amacı, CTI çalışmalarında tehdit aktörlerinin nasıl profillendiğini ve bir saldırının belirli bir grup veya aktörle ilişkilendirilmesinin neden zor olduğunu açıklamaktır.

Bir tehdit aktörünü yalnızca kullandığı malware veya IP adresi üzerinden tanımlamak çoğu zaman yeterli değildir.

Analistler;

- TTP'ler
- Hedef sektörler
- Kullanılan altyapı
- Malware aileleri
- Kampanyalar
- Zamanlama
- Dil ve operasyonel alışkanlıklar

gibi birçok farklı veri noktasını birlikte değerlendirir.

Bu sürece genel olarak **threat actor profiling** adı verilir.

## Ana Kavramlar

- Threat Actor
- Threat Group
- APT
- Campaign
- Attribution
- Alias
- TTP
- Infrastructure
- Malware
- Victimology
- Confidence Level
- False Flag

## Threat Actor Nedir?

Threat actor, siber saldırı veya kötü amaçlı faaliyet gerçekleştiren kişi, grup veya organizasyon için kullanılan genel bir terimdir.

Threat actor farklı motivasyonlara sahip olabilir.

Örneğin:

- Finansal kazanç
- Casusluk
- Politik amaç
- Hacktivizm
- Sabotaj
- Veri hırsızlığı
- Rekabet avantajı

Bu nedenle tüm saldırganları aynı kategori içinde değerlendirmek doğru değildir.

Bir ransomware grubu ile devlet destekli olduğu değerlendirilen bir casusluk grubu farklı amaçlara ve çalışma yöntemlerine sahip olabilir.

## Threat Group ve Campaign Arasındaki Fark

CTI çalışmalarında **threat group** ile **campaign** kavramlarının karıştırılmaması önemlidir.

Threat group, belirli davranış özellikleri ve operasyonlarla ilişkilendirilen saldırgan kümesini ifade eder.

Campaign ise belirli bir süre boyunca belirli bir hedef veya amaç için yürütülen saldırı faaliyetidir.

Örneğin aynı tehdit grubu farklı zamanlarda:

- Finans kurumlarını hedefleyen bir phishing kampanyası,
- Kamu kurumlarını hedefleyen başka bir casusluk kampanyası

yürütebilir.

Bu durumda grup aynı olabilir ancak kampanyalar farklıdır.

## APT Nedir?

APT, **Advanced Persistent Threat** ifadesinin kısaltmasıdır.

Genellikle yüksek kaynaklara sahip, uzun süreli operasyon yürüten ve belirli hedeflere odaklanan tehdit aktörlerini veya gruplarını tanımlamak için kullanılır.

Ancak APT ifadesi her zaman yalnızca teknik olarak çok gelişmiş saldırılar anlamına gelmez.

Bir grup:

- Basit phishing teknikleri,
- Bilinen açıklar,
- Hazır malware araçları

kullanarak da etkili ve uzun süreli operasyonlar gerçekleştirebilir.

Önemli olan saldırının amacı, sürekliliği ve operasyonel yapısıdır.

## Threat Actor Profili Nasıl Oluşturulur?

Bir tehdit aktörü profili oluşturulurken tek bir veri noktasına güvenilmez.

Analist farklı kategorilerdeki bilgileri bir araya getirir.

### Hedefler

Aktör hangi sektörleri hedefliyor?

Örneğin:

- Finans
- Savunma
- Enerji
- Sağlık
- Telekomünikasyon
- Kamu kurumları

Hedeflerin coğrafi dağılımı da önemli olabilir.

Bir grubun sürekli olarak belirli ülkeleri veya bölgeleri hedeflemesi operasyonun amacı hakkında ipucu sağlayabilir.

## Victimology

Bir saldırganın hedeflediği kişi, kuruluş, sektör veya ülkelerin incelenmesine **victimology** denir.

Örneğin bir grubun geçmiş operasyonlarında sürekli:

- Savunma şirketlerini,
- Diplomatik kurumları,
- Araştırma merkezlerini

hedeflediği görülüyorsa bu durum grubun motivasyonu hakkında önemli bilgi sağlayabilir.

Ancak hedef profili tek başına attribution için yeterli değildir.

Birden fazla tehdit aktörü aynı sektörü hedefleyebilir.

## TTP Analizi

TTP, **Tactics, Techniques and Procedures** ifadesinin kısaltmasıdır.

Bir saldırganın operasyon sırasında nasıl hareket ettiğini anlamak için kullanılır.

Örneğin bir aktör sürekli olarak:

- Spear phishing kullanıyor,
- Belirli dosya türleri gönderiyor,
- PowerShell ile payload çalıştırıyor,
- Credential dumping yapıyor,
- Benzer persistence yöntemleri kullanıyorsa

bu davranışlar aktörün operasyonel profilinin bir parçası olabilir.

TTP'ler genellikle IP veya domain gibi IOC'lerden daha uzun ömürlüdür.

Ancak saldırganlar zaman içerisinde kullandıkları teknikleri değiştirebilir.

Bu nedenle TTP eşleşmesi de tek başına kesin attribution sağlamaz.

## Malware Kullanımı

Bir threat actor belirli malware aileleriyle ilişkilendirilebilir.

Örneğin analist şu ilişkiyi gözlemleyebilir:

`Threat Actor → Malware → C2 Infrastructure`

Ancak bir malware'in belirli bir saldırıda kullanılması, saldırıyı otomatik olarak malware ile daha önce ilişkilendirilen gruba bağlamaz.

Bazı malware aileleri:

- Birden fazla grup tarafından kullanılabilir,
- Dark web üzerinden satılabilir,
- Açık kaynak olabilir,
- Başka gruplar tarafından kopyalanabilir.

Bu nedenle malware ilişkisi başka kanıtlarla desteklenmelidir.

## Altyapı Analizi

Saldırganların kullandığı altyapı da profil oluşturmada önemli bir veri kaynağıdır.

Örneğin:

- Domain kayıtları
- IP adresleri
- Hosting sağlayıcıları
- DNS kayıtları
- TLS sertifikaları
- C2 sunucuları
- Redirect altyapıları

incelenebilir.

Birden fazla kampanyada tekrar eden altyapı özellikleri tehdit aktörleri arasında ilişki kurulmasına yardımcı olabilir.

Ancak burada da dikkatli olunmalıdır.

Aynı hosting servisinin kullanılması, iki saldırının aynı grup tarafından gerçekleştirildiğini kanıtlamaz.

## Zamanlama Analizi

Saldırgan faaliyetlerinin hangi saatlerde ve hangi günlerde gerçekleştiği de yardımcı veri olarak kullanılabilir.

Örneğin operasyonların belirli bir zaman dilimindeki çalışma saatleriyle yoğun şekilde örtüşmesi bazı değerlendirmelere katkıda bulunabilir.

Ancak bu tür bilgiler doğrudan kanıt değildir.

Saldırganlar:

- Farklı saatlerde çalışabilir,
- Otomasyon kullanabilir,
- Bilerek yanıltıcı zamanlama oluşturabilir.

Bu nedenle zamanlama analizi yalnızca destekleyici veri olarak kullanılmalıdır.

## Neden Aynı Grubun Birden Fazla İsmi Var?

CTI dünyasında aynı veya benzer tehdit kümeleri farklı güvenlik şirketleri tarafından farklı isimlerle takip edilebilir.

Örneğin bir şirket kendi gözlemlediği faaliyetlere ayrı bir isim verirken başka bir şirket aynı faaliyet kümesini farklı bir isimle tanımlayabilir.

Bu isimlere **alias** adı verilir.

Bir tehdit aktörünün farklı kaynaklarda:

`Group A`

`APT-X`

`Fancy Animal`

gibi farklı isimlerle geçmesi mümkündür.

Ancak farklı isimlerin kullanılması her zaman şirketlerin aynı gruptan bahsettiği anlamına gelmez.

Bazen iki şirketin takip ettiği faaliyet kümeleri yalnızca kısmen örtüşebilir.

Bu nedenle alias ilişkileri dikkatli değerlendirilmelidir.

## Attribution Nedir?

Attribution, bir saldırının veya kampanyanın arkasındaki kişi, grup veya organizasyonun belirlenmeye çalışılmasıdır.

CTI açısından en zor analiz alanlarından biridir.

Attribution yapılırken farklı veri noktaları bir araya getirilebilir:

- TTP benzerlikleri
- Malware kullanımı
- Altyapı ilişkileri
- Hedef profili
- Kampanya geçmişi
- Operasyonel zamanlama
- Dil özellikleri
- Teknik hatalar
- Önceki güvenilir raporlar

Ancak bu kanıtların hiçbiri tek başına kesin sonuç vermeyebilir.

## Teknik Attribution ve Politik Attribution

Teknik analiz sonucunda:

> Bu saldırı daha önce X grubu ile ilişkilendirilen faaliyetlerle güçlü benzerlik göstermektedir.

şeklinde bir değerlendirme yapılabilir.

Bu, saldırının arkasındaki gerçek kişi veya devletin kesin olarak belirlendiği anlamına gelmez.

Özellikle devlet destekli aktörlerde attribution yalnızca teknik veri değil;

- İnsan istihbaratı,
- Hukuki bilgiler,
- Diplomatik kaynaklar,
- Gizli istihbarat

gibi CTI analistinin erişemeyebileceği bilgiler de gerektirebilir.

Bu nedenle teknik CTI raporlarında kesinlik dili dikkatli kullanılmalıdır.

## False Flag

Saldırganlar attribution sürecini zorlaştırmak için yanıltıcı izler bırakabilir.

Bu tür davranışlara **false flag** denilebilir.

Örneğin bir saldırgan:

- Başka bir grubun malware'ini kullanabilir,
- Farklı bir dilde dosya isimleri bırakabilir,
- Başka bir ülkeye ait altyapıyı kullanabilir,
- Bilinen bir grubun tekniklerini taklit edebilir.

Amaç analistin yanlış sonuca ulaşmasını sağlamak olabilir.

Bu nedenle özellikle tek bir kanıt üzerinden attribution yapılmamalıdır.

## Analitik Tuzak: Benzerlik Eşit Değildir

İki saldırıda aynı tekniğin kullanılması, saldırıların aynı grup tarafından gerçekleştirildiğini göstermez.

Örneğin phishing çok sayıda tehdit aktörü tarafından kullanılmaktadır.

Benzer şekilde:

`Aynı technique ≠ Aynı grup`

`Aynı malware ≠ Aynı grup`

`Aynı hosting sağlayıcısı ≠ Aynı grup`

`Aynı ülke hedefi ≠ Aynı grup`

Attribution için önemli olan farklı kanıtların birlikte değerlendirilmesidir.

## Confidence Level Kullanımı

Attribution sonuçları çoğu zaman kesin değildir.

Bu nedenle analiz sonucunun güven seviyesi belirtilmelidir.

Örneğin:

**Düşük güven**

Sınırlı kanıt vardır ve alternatif açıklamalar güçlüdür.

**Orta güven**

Birden fazla veri noktası değerlendirmeyi desteklemektedir ancak önemli belirsizlikler devam etmektedir.

**Yüksek güven**

Birbirinden bağımsız ve güvenilir çok sayıda veri noktası aynı değerlendirmeyi desteklemektedir.

Örneğin:

> Mevcut TTP, altyapı ve hedef profili benzerlikleri nedeniyle kampanyanın X aktörüyle ilişkili olduğunu orta güven seviyesinde değerlendiriyoruz.

Bu ifade:

> Saldırıyı kesin olarak X yaptı.

ifadesinden çok daha doğru bir CTI yaklaşımıdır.

## Örnek Threat Actor Profili

Bir analistin birkaç farklı saldırı kampanyasını incelediğini düşünelim.

Aşağıdaki ortak özellikler tespit ediliyor:

- Finans sektörüne yönelik hedefleme
- Spear phishing ile ilk erişim
- Benzer PowerShell komutları
- Aynı malware ailesi
- Benzer domain isimlendirme yöntemi
- Aynı hosting sağlayıcıları
- Ortak çalışma saatleri

Bu veriler kampanyalar arasında ilişki olabileceğini gösterebilir.

Ancak analist doğrudan:

> Bunların tamamını aynı grup gerçekleştirdi.

sonucuna varmamalıdır.

Bunun yerine alternatif açıklamalar da değerlendirilmelidir.

Örneğin kullanılan malware başka gruplar tarafından da kullanılabilir veya hosting sağlayıcısı birçok farklı müşteri tarafından tercih ediliyor olabilir.

## Threat Actor Profili Neden Önemlidir?

Threat actor profilleme yalnızca saldırının arkasındaki kişiyi bulmak için yapılmaz.

Bir grubun geçmiş davranışlarını anlamak gelecekteki faaliyetlerine karşı hazırlanmayı kolaylaştırabilir.

Örneğin bir tehdit aktörünün sürekli:

- Belirli sektörleri hedeflediği,
- Phishing kullandığı,
- Belirli TTP'lere ağırlık verdiği

biliniyorsa savunma ekipleri bu davranışlara karşı öncelikli kontroller oluşturabilir.

Bu nedenle threat actor profili savunma stratejisinin şekillendirilmesine de yardımcı olur.

## Sonuç

Threat actor attribution bir isim eşleştirme işlemi değildir.

Analist;

`Hedef + TTP + Malware + Altyapı + Kampanya geçmişi + Zaman`

gibi farklı veri noktalarını birlikte değerlendirir.

En önemli kural ise şudur:

**Bir ilişki görmek, kesin attribution yapmak anlamına gelmez.**

İyi bir CTI analisti yalnızca hangi sonuca ulaştığını değil, bu sonuca ne kadar güvendiğini ve hangi alternatif açıklamaların bulunduğunu da belirtir.