# Veri düzlemi

Ergin İz · Ergin Kaplan · Ergin İz Atölyesi · Ergin Lab

## Dosya başlığı (48 bayt, little-endian)

| Alan | Boy | Anlam |
| --- | --- | --- |
| sihir | 4 | `EIZ1` |
| surum | 2 | 1 |
| bayrak | 2 | 0 |
| baslik_boy | 4 | 48 |
| uretici | 2 | kaynak sayısı |
| pad | 2 | 0 |
| olusturma | 8 | duvar saati, nanosaniye |
| tampon | 4 | halka kapasitesi, bayt |
| paket | 4 | yazılan paket |
| dusen | 4 | sığmadığı için düşen |
| ayrildi | 8 | 0 |
| imza | 4 | `ELAB` |

## Paket

`u32` gövde boyu, ardından gövde.

Gövde sabit alanı 52 bayttır:

| Alan | Boy |
| --- | --- |
| tur | 1 |
| pad | 3 |
| ts | 8 |
| pid | 4 |
| tid | 4 |
| izlek | 4 |
| cerez | 8 |
| deger | 8, işaretli |
| cpu | 4 |
| arg0 | 4 |
| arg1 | 4 |

Ardından `u16` ad boyu, ad baytları, `u16` kat boyu, kat baytları.
Metin UTF-8'dir.

## Türler

| tur | Ad |
| --- | --- |
| 1 | dilim başlangıcı |
| 2 | dilim bitişi |
| 3 | sayaç |
| 4 | zamanlama |
| 5 | işaret |

Dilim çifti `cerez` ile eşleşir. Derinlik, aynı izlekte açık olan dilim sayısıdır.
Zamanlamada `deger` sonraki sayaç, `arg0` artıştır.

## Halka

Kapasite ikinin kuvvetidir ve en az 64 bayttır.
Yazma ve okuma sayaçları monoton artar.
Paket sığmazsa düşer; eski paketin üzerine yazılmaz.
