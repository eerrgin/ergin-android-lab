# Lisans, marka ve bağımsızlık notu

Bu belge hukuki görüş değildir; projenin mevcut kapsamını ve kaynak ekleme politikasını açıklamak için yazılmıştır.

## Mevcut içerik
- Mevcut ağaç Python ve C kaynaklarından oluşan yerel izleme/kayıt prototipidir.
- Mevcut ağaçta Android Gradle projesi, AndroidManifest.xml, Kotlin/Java uygulama katmanı veya Android SDK bağımlılığı bulunmaz.
- Bu depo Google LLC, Open Handset Alliance veya Android ekibi tarafından desteklenmez ve onlarla bağlantılı değildir.
- Depoya Google/AOSP kaynak kodu, Google Play Services bileşeni, Android logosu veya Google'a ait marka görseli eklenmiş olduğu iddia edilmez.

## Android ve AOSP arasındaki ayrım
Android açık kaynak platformunda kullanılan lisansların çoğu Apache License 2.0 olsa da tüm bileşenlerin aynı lisansa sahip olduğu varsayılamaz. Android adı, logoları ve Google Play markası ayrıca marka kurallarına tabidir. Bir SDK'yı indirmek, her marka varlığını veya her üçüncü taraf bileşeni sınırsız kullanma izni vermez.

Resmî belgeler:
- [AOSP sık sorulan sorular](https://source.android.com/docs/setup/about/faqs)
- [Android Developers Legal Notice](https://developer.android.com/legal)
- [Android Brand Guidelines](https://developer.android.com/distribute/marketing-tools/brand-guidelines)

## Gelecekte Android uygulaması eklenirse
1. Mevcut yerel prototipten ayrı bir uygulama/alt proje tanımla; bugünkü kodu Android uygulaması diye sunma.
2. Yalnızca gerektiği kadar resmî SDK/API kullan; sürümleri sabitle ve her bağımlılığın lisansını kaydet.
3. Dosya erişimi için mümkün olduğunda sistem dosya seçicisini kullan; gereksiz izin, telemetri veya arka plan toplaması ekleme.
4. Google Play'e yayımlama hedeflenirse Play şartlarını ayrıca doğrula; bu depo için yayımlama veya onay iddiasında bulunma.
5. Android/Google logolarını, ikonlarını, özel yazı tiplerini ya da marka tasarımlarını izinsiz kullanma.
6. İlgili platformdan yalnızca tanımlayıcı bağlamda söz et; resmî ortaklık/sertifikasyon izlenimi yaratma.

## Bu depodaki haklar
Bu depodaki özgün Python, C, HTML ve belgeler için `BELIRT.md` geçerlidir. Açık bir yeniden kullanım lisansı tanımlanmadığı için başkalarının kodu yeniden dağıtması veya değiştirilmiş bir sürümü yayımlaması otomatik olarak yetkilendirilmiş değildir.
