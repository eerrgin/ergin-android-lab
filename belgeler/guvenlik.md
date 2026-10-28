# Servis sınırı

Ergin Android Lab · Ergin Kaplan · Ergin Lab · Ergin Android Atölyesi

Denetim kanalı yalnızca `127.0.0.1` üzerinde, işletim sisteminin seçtiği
bir kapıda dinler. Dış arayüze bağlanmaz.

Çerçeve boyu en fazla 4096 bayttır. Daha büyüğü `HATA cerceve` ile kapanır.
Bilinen komutlar: `DURUM`, `KAYNAKLAR`, `YAZAR`, `DUR`.
Bunun dışı `HATA bilinmeyen` döner.

Komut metni kabuğa verilmez. Dosya yolu, ortam değişkeni veya başka bir
program çağrısı üretilmez.

İz dosyası yalnızca kaydı başlatan kullanıcının yazdığı yere konur.
SQL tüketici tarafında, eldeki dosyanın üzerinde çalışır. Sorguyu ağa açmaz.

Halka dolunca eski olay ezilmez. Sığmayan paket düşer ve `dusen` sayılır.
Bu, sessiz veri kaybını başlıkta görünür kılar.
