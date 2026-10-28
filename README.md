# Ergin İz — Sistem İzleme Atölyesi

Sahip ve yazar: **Ergin Kaplan**

Ergin İz, olay üretimi, sınırlı halka tamponu, servis, yerel kayıt dosyası ve SQL tüketicisini gösteren bağımsız bir eğitim prototipidir.

> **Teknik durum:** Depo adında `android` geçse de mevcut kod Android cihazda çalışan bir uygulama değildir. Kod tabanı Python 3.10 ve C örneklerinden oluşur; mevcut ağaçta Android Gradle projesi, `AndroidManifest.xml`, Kotlin/Java uygulama ekranları veya Android SDK entegrasyonu bulunmaz. Prototip yerel ana makinede çalışır.

## Bileşenler

```
ergin_iz/     Python tabanlı kayıt ve rapor katmanı
cekirdek/     C halka tamponu örneği
ornekler/     yapılandırma, örnek rapor ve SQL
belgeler/     mimari, veri akışı, güvenlik ve lisans notları
araclar/      yerel deneme ve derleme komutları
tests/        birim testleri
```

## Çalıştırma

```sh
python3 -m ergin_iz kaydet -c ornekler/atolye.config -o cikti/atolye.eiz
python3 -m ergin_iz rapor -i cikti/atolye.eiz
python3 -m ergin_iz sorgula -i cikti/atolye.eiz -s ornekler/sorgular.sql
sh araclar/dene.sh
sh araclar/derle.sh
```

Python 3.10 ve bir C derleyicisi yeterlidir. Önce [kullanım rehberini](belgeler/kullanim.md) okuyun.

## Güvenlik sınırı

Denetim kanalı tasarım gereği yerel döngü adresinde çalışır ve sınırlı bir komut kümesini kabul eder. Dosya yolları/sorgular kabuğa aktarılmamalı, kayıt içeriği kullanıcı seçimi dışında ağ üzerinden paylaşılmamalıdır. Bu notlar tasarımın niyetini açıklar; kodu ayrıca incelemek gerekir.

## Lisans ve marka

Bu bağımsız depoda Google LLC veya Open Handset Alliance kaynak kodu bulunduğu iddia edilmez. Mevcut ağaç bir Android SDK uygulaması değildir. “Android” yalnızca ilgili teknik platformu betimleyen bağlamda kullanılır; Android adı/logosu/Google Play varlıkları bu projeye ait değildir. Ayrıntı: [lisans ve marka notları](belgeler/lisans-ve-marka.md).

Bu depodaki özgün kaynaklar için [BELIRT.md](BELIRT.md) geçerlidir. Açık kaynak yeniden kullanım lisansı verilmemiştir; GitHub'da herkese açık olmak kodu yeniden dağıtma izni anlamına gelmez.
