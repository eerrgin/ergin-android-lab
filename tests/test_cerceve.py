# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

import struct
import tempfile
import unittest
from pathlib import Path

from ergin_iz.cerceve import (
    BASLIK_BOY,
    SABIT,
    baslik_coz,
    baslik_yap,
    dilim_bas,
    dosyayi_oku,
    govde_yap,
    isaret,
    olay_coz,
    paket_yap,
    sayac,
    zamanlama,
)


class CerceveTest(unittest.TestCase):
    def test_sabit_boy(self):
        self.assertEqual(len(govde_yap(isaret("ergin.lab", "Ergin Lab"))), SABIT + 2 + len("ergin.lab") + 2 + len("Ergin Lab"))
        self.assertEqual(len(baslik_yap(1, 4096)), BASLIK_BOY)
        self.assertEqual(struct.calcsize("<4sHHIHHQIIIQ4s"), 48)

    def test_olay_turleri(self):
        ornekler = [
            dilim_bas("ergin.lab.cerceve", "Ergin Lab", 7),
            sayac("bellek.musait_kb", "Ergin İz Atölyesi", 123456),
            zamanlama("baglam.degisim", "Ergin İz", 10, 40),
            isaret("ergin.lab.kalp", "Ergin İz Atölyesi"),
        ]
        ornekler[0].ts = 99
        ornekler[0].pid = 5
        for olay in ornekler:
            geri = olay_coz(govde_yap(olay))
            self.assertEqual(geri.tur, olay.tur)
            self.assertEqual(geri.ad, olay.ad)
            self.assertEqual(geri.kat, olay.kat)
            self.assertEqual(geri.deger, olay.deger)
            self.assertEqual(geri.cerez, olay.cerez)
        zaman = olay_coz(govde_yap(zamanlama("baglam.degisim", "Ergin Lab", 10, 40)))
        self.assertEqual(zaman.deger, 40)
        self.assertEqual(zaman.arg0, 30)

    def test_dosya(self):
        bas = baslik_yap(2, 8192, paket=1, dusen=0, olusturma=42)
        self.assertEqual(baslik_coz(bas)["uretici"], 2)
        self.assertEqual(baslik_coz(bas)["olusturma"], 42)
        olay = isaret("ergin.lab.kalp", "Ergin Kaplan")
        olay.ts = 1000
        with tempfile.TemporaryDirectory() as tmp:
            yol = Path(tmp) / "atolye.eiz"
            yol.write_bytes(bas + paket_yap(olay))
            okunan_baslik, olaylar = dosyayi_oku(yol)
            self.assertEqual(okunan_baslik["imza"], b"ELAB")
            self.assertEqual(len(olaylar), 1)
            self.assertEqual(olaylar[0].ad, "ergin.lab.kalp")
            self.assertIn("Ergin", olaylar[0].kat)


if __name__ == "__main__":
    unittest.main()
