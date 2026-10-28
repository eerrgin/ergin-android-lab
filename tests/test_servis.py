# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

import tempfile
import threading
import unittest
from pathlib import Path

from ergin_iz.islemci import IzIslemci
from ergin_iz.kanal import denetim_sor
from ergin_iz.servis import Servis
from ergin_iz.sonda import cpu_yuzde_binde, oku_cpu_jiffy
from ergin_iz.yapilandirma import YapilandirmaHatasi, yukle, yukle_metin

KOK = Path(__file__).resolve().parents[1]


class ServisTest(unittest.TestCase):
    def test_yapilandirma(self):
        ayar = yukle(KOK / "ornekler" / "atolye.config")
        self.assertEqual(ayar["kaynaklar"], ["dilim", "sayac", "zamanlayici", "isaret"])
        self.assertEqual(ayar["tampon_kb"], 512)
        with self.assertRaises(YapilandirmaHatasi):
            yukle_metin("kaynak: yok\n")

    def test_cpu_orani(self):
        self.assertEqual(cpu_yuzde_binde((100, 40), (200, 90)), 5000)
        self.assertIsNotNone(oku_cpu_jiffy())

    def test_kayit_ve_denetim(self):
        metin = """
        # Ergin Android Lab
        tampon_kb: 64
        sure_ms: 700
        kaynak: dilim
        kaynak: isaret
        kaynak: sayac
        dilim.yineleme: 4
        sayac.aralik_ms: 100
        isaret.aralik_ms: 80
        """
        ayar = yukle_metin(metin)
        with tempfile.TemporaryDirectory() as tmp:
            yol = Path(tmp) / "atolye.eiz"
            servis = Servis(ayar)
            kutu = {}

            def calistir():
                kutu["yol"] = servis.calistir(str(yol))

            iplik = threading.Thread(target=calistir)
            iplik.start()
            for _ in range(50):
                if servis.kanal is not None:
                    break
                threading.Event().wait(0.02)
            self.assertIsNotNone(servis.kanal)
            durum = denetim_sor(servis.kanal.port, "DURUM")
            self.assertIn("Ergin Lab", durum)
            self.assertIn("Ergin Kaplan", durum)
            self.assertIn("Ergin Android Atölyesi", durum)
            yazar = denetim_sor(servis.kanal.port, "YAZAR")
            self.assertIn("Ergin Android Lab", yazar)
            bilinmeyen = denetim_sor(servis.kanal.port, "SIL")
            self.assertIn("HATA", bilinmeyen)
            iplik.join(timeout=5)
            self.assertFalse(iplik.is_alive())
            self.assertEqual(servis.hatalar, [])
            iz = IzIslemci(yol)
            try:
                dilim = iz.db.execute("SELECT COUNT(*) FROM dilimler").fetchone()[0]
                isaret = iz.db.execute("SELECT COUNT(*) FROM isaretler").fetchone()[0]
                self.assertGreaterEqual(dilim, 4)
                self.assertGreaterEqual(isaret, 1)
                marka = iz.db.execute(
                    "SELECT deger FROM ustbilgi WHERE anahtar = 'marka'"
                ).fetchone()[0]
                self.assertEqual(marka, "Ergin Android Lab")
            finally:
                iz.kapat()


if __name__ == "__main__":
    unittest.main()
