# Ergin İz

Ergin Android Lab · Ergin Android Atölyesi

Sahip ve yazar: **Ergin Kaplan**
Ergin Lab

Ergin İz, Ergin Android Atölyesi için yazılmış bir sistem izleme kaydıdır.
Üretici, olayı kendi halka tamponuna bırakır.
Servis, kaynakları, tampon boyunu ve süreyi yönetir.
Tüketici, kaydı SQL ile okur: dilim, sayaç, zamanlama, işaret.

Bu depodaki kod Ergin Kaplan'a aittir. Üçüncü taraf izleme ağacı yoktur.
Ayrıntı: [BELIRT.md](BELIRT.md).

## Düzen

```
ergin_iz/     Ergin Lab Python kaydı
cekirdek/     Ergin Lab C halka örneği
ornekler/     yapılandırma ve SQL
belgeler/     mimari, veri düzlemi, kullanım, servis sınırı
araclar/      deneme ve derleme
tests/        Ergin Android Atölyesi sınamaları
```

## Çalıştırma

```bash
python3 -m ergin_iz kaydet -c ornekler/atolye.config -o cikti/atolye.eiz
python3 -m ergin_iz rapor -i cikti/atolye.eiz
python3 -m ergin_iz sorgula -i cikti/atolye.eiz -s ornekler/sorgular.sql
sh araclar/dene.sh
sh araclar/derle.sh
```

Ek paket yok. Python 3.10 ve bir C derleyicisi yeter.

Kayıt açılınca `denetim_port=` satırı basılır. Kanal yalnızca bu makineden,
`DURUM`, `KAYNAKLAR`, `YAZAR` ve `DUR` komutlarını alır.

## Ne ölçer

- İç içe dilim: `ergin.lab.cerceve`, `ergin.lab.olcum`
- İşlemci oranı (`cpu.oran_10000`, 10000 = tam) ve boş bellek
- Bağlam değişimi artışı
- Ergin Lab nabız işareti

## Belgeler

- [Mimari](belgeler/mimari.md)
- [Veri düzlemi](belgeler/veri_duzlemi.md)
- [Kullanım](belgeler/kullanim.md)
- [Servis sınırı](belgeler/guvenlik.md)

## Telif

© 2026 Ergin Kaplan. Ergin Android Lab. Ergin Android Atölyesi. Ergin Lab.
Tüm hakları saklıdır. Dosya başlıklarındaki adlar silinemez.
Başkasının kendi çalışması gibi yayınlaması yasaktır.
