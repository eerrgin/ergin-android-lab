# Kullanım

Ergin İz — Ergin Android Lab
Ergin Kaplan · Ergin Android Atölyesi · Ergin Lab

Python 3.10 yeterlidir. Ek paket kurulmaz.

```bash
python3 -m ergin_iz surum
python3 -m ergin_iz kaydet -c ornekler/atolye.config -o cikti/atolye.eiz
python3 -m ergin_iz cozumle -i cikti/atolye.eiz
python3 -m ergin_iz rapor -i cikti/atolye.eiz
python3 -m ergin_iz sorgula -i cikti/atolye.eiz -s ornekler/sorgular.sql
python3 -m ergin_iz sorgula -i cikti/atolye.eiz -q "SELECT ad, COUNT(*) AS n FROM dilimler GROUP BY ad"
sh araclar/dene.sh
sh araclar/derle.sh
```

Kayıt sırasında satırda `denetim_port=` görünür. Kayıt sürerken:

```bash
python3 -m ergin_iz denetim --port PORT --komut DURUM
python3 -m ergin_iz denetim --port PORT --komut YAZAR
python3 -m ergin_iz denetim --port PORT --komut DUR
```

`DUR` kaydı süreden önce keser.

## Yapılandırma

```
tampon_kb: 512
sure_ms: 1500
cikis: cikti/atolye.eiz
kaynak: dilim
kaynak: sayac
kaynak: zamanlayici
kaynak: isaret
dilim.yineleme: 8
sayac.aralik_ms: 100
zamanlayici.aralik_ms: 100
isaret.aralik_ms: 200
```

`#` sonrası açıklamadır. Kaynak yazılmazsa `dilim` ve `isaret` açılır.

## Tablolar

- `ustbilgi`
- `olaylar`
- `dilimler`
- `sayaclar`
- `zamanlama`
- `isaretler`
- `acik_dilimler`

`dilimler.sur` nanosaniyedir.
