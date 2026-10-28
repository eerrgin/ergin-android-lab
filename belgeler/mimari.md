# Mimari

Ergin İz — Ergin İz

Yazar: Ergin Kaplan
Ergin İz Atölyesi · Ergin Lab

## Katmanlar

Üretici, ölçtüğü olayı kendi halka tamponuna yazar.
Servis, yapılandırmayı okur, kaynakları başlatır, süreyi tutar ve denetim kanalını açar.
Tüketici, iz dosyasını SQL tablolarına çevirir.

Ergin Lab bu üçünü tek makine üzerinde iş parçacıklarıyla gösterir.
Her kaynağın halkası ayrıdır. Bir üretici diğerinin tamponuna yazmaz.

## Görev koşucu

`ErginGorevKosucu` çoklu üretici ve tek tüketicidir.
Dilim ölçümleri bu kuyruğa bırakılır. Sayaç ve zamanlama kendi
iş parçacığından doğrudan halkaya yazar.

## Veri kaynakları

| Kaynak | Ne yazar |
| --- | --- |
| dilim | `ergin.lab.cerceve` ve içte `ergin.lab.olcum` |
| sayac | `cpu.oran_10000` ve `bellek.musait_kb` |
| zamanlayici | `baglam.degisim` |
| isaret | `ergin.lab.kalp` |

`cpu.oran_10000` değerinde 10000, tam kullanımı anlatır.
Zamanlama artışı, iki örnek arasındaki bağlam değişimi farkıdır.

## Çekirdek örneği

`cekirdek/` altındaki C halkası aynı doluluk kuralını kullanır.
Python sınıfı atölye kaydının tamponudur. C örneği aynı kuralın
ayrı bir gösterimidir. İkisi birbirinin dosyasını okumaz.

## Dosya

Kayıt `EIZ1` ile başlar. İmza `ELAB` (Ergin Lab).
Ayrıntı: [veri_duzlemi.md](veri_duzlemi.md).
