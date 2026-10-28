# Ergin İz — gelecek yol haritası

Bu bir geliştirme önerisidir, mevcut özellik listesi değildir.

## Aşama 1 — mevcut prototipi sağlamlaştır
- [ ] halka tamponu dolduğunda sayaç ve davranış için testler
- [ ] kayıt formatı için sürüm ve bozuk/truncated dosya sınamaları
- [ ] örnek yapılandırmaların sınır doğrulaması
- [ ] süreç/sayaç ölçümünde platforma özgü varsayımları belgele
- [ ] Python ve C parçaları için ayrı test/derleme komutları

## Aşama 2 — kayıt inceleyici
- [ ] `.eiz` dosyasını kullanıcının açıkça seçtiği yerel dosyadan oku
- [ ] kronolojik zaman çizelgesi ve kayıp kayıt göstergesi
- [ ] yerel SQL sorgularının izin verilen örnekleri
- [ ] hiçbir dosyayı kendiliğinden sunucuya göndermeme
- [ ] hatalı dosyalarda kontrollü hata mesajı

## Aşama 3 — gerçek Android™ uygulaması ayrı çalışma
- [ ] ayrı Kotlin/Gradle uygulama iskeleti oluştur
- [ ] başlangıçta ağ izni ve arka plan servisi ekleme
- [ ] SAF ile kullanıcı tarafından seçilen kayıt dosyasını içeri al
- [ ] küçük ekran, büyük metin ve erişilebilirlik testleri
- [ ] emülatör ve fiziksel cihazda uyum testi
- [ ] bütün bağımlılıklar için lisans/envanter kaydı
- [ ] marka, gizlilik ve mağaza şartlarını yayımdan önce tekrar kontrol et

Bugünkü depo birinci aşamadaki yerel sistem prototipidir. Aşama 3 henüz uygulanmış değildir.
