# Servis sınırı ve güvenlik modeli

Ergin İz — yerel sistem izleme prototipi

## Teknik kapsam
Bu depo mevcut hâliyle Android cihaz uygulaması değildir. Python/C katmanları yerel bir ana makinede çalışan eğitim prototipidir. Android SDK, Android arka plan servisi veya Google SDK entegrasyonu bulunduğu varsayılmamalıdır.

## Denetim kanalı
Denetim kanalı yalnızca `127.0.0.1` üzerinde, işletim sisteminin seçtiği bir kapıda dinler. Dış arayüze bağlanmaz. Çerçeve boyu en fazla 4096 bayttır. Bilinen komutlar: `DURUM`, `KAYNAKLAR`, `YAZAR`, `DUR`; diğer komutlar reddedilir.

Komut metni kabuğa verilmez. Dosya yolu, ortam değişkeni veya başka bir program çağrısı komut metninden üretilmez. İz dosyası yalnızca kaydı başlatan kullanıcının yazdığı yere konur. SQL tüketici tarafında eldeki dosya üzerinde çalışır; sorguyu ağa açmaz.

Halka dolunca eski olay sessizce ezilmez. Sığmayan paket düşer ve `dusen` sayılır.

## Güvenlik notları
Bu belge tasarımın hedefini açıklar; güvenlik garantisi veya bağımsız denetim raporu değildir. Kod değiştiğinde yerel sınırlar, hata yolları ve testler yeniden kontrol edilmelidir.
