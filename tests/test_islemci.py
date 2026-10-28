# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

import tempfile
import unittest
from pathlib import Path

from ergin_iz.cerceve import (
    dilim_bas,
    dilim_bit,
    isaret,
    paket_yap,
    sayac,
    baslik_yap,
)
from ergin_iz.islemci import IzIslemci, sql_ayir


class IslemciTest(unittest.TestCase):
    def test_dilim_ve_sorgu(self):
        dis = dilim_bas("ergin.lab.cerceve", "Ergin Lab", 1)
        dis.ts = 1_000
        ic = dilim_bas("ergin.lab.olcum", "Ergin Android Lab", 2)
        ic.ts = 1_500
        ic_bit = dilim_bit("ergin.lab.olcum", "Ergin Android Lab", 2)
        ic_bit.ts = 4_000
        dis_bit = dilim_bit("ergin.lab.cerceve", "Ergin Lab", 1)
        dis_bit.ts = 5_000
        nabiz = isaret("ergin.lab.kalp", "Ergin Android Atölyesi")
        nabiz.ts = 2_000
        olcu = sayac("bellek.musait_kb", "Ergin Android Atölyesi", 4096)
        olcu.ts = 2_100
        govde = b"".join(paket_yap(o) for o in (dis, ic, nabiz, olcu, ic_bit, dis_bit))
        with tempfile.TemporaryDirectory() as tmp:
            yol = Path(tmp) / "ornek.eiz"
            yol.write_bytes(baslik_yap(1, 4096, paket=6, dusen=0, olusturma=7) + govde)
            iz = IzIslemci(yol)
            try:
                yazar = iz.db.execute(
                    "SELECT deger FROM ustbilgi WHERE anahtar = 'yazar'"
                ).fetchone()[0]
                self.assertEqual(yazar, "Ergin Kaplan")
                atolye = iz.db.execute(
                    "SELECT deger FROM ustbilgi WHERE anahtar = 'atolye'"
                ).fetchone()[0]
                self.assertEqual(atolye, "Ergin Android Atölyesi")
                satirlar = iz.db.execute(
                    "SELECT ad, sur, derinlik FROM dilimler ORDER BY derinlik"
                ).fetchall()
                self.assertEqual([tuple(s) for s in satirlar], [
                    ("ergin.lab.cerceve", 4_000, 0),
                    ("ergin.lab.olcum", 2_500, 1),
                ])
                self.assertEqual(
                    iz.db.execute("SELECT COUNT(*) FROM isaretler").fetchone()[0],
                    1,
                )
                sonuc = iz.calistir(
                    "SELECT ad, deger FROM sayaclar; -- Ergin Lab\nSELECT COUNT(*) AS n FROM dilimler"
                )
                self.assertEqual(len(sonuc), 2)
                self.assertEqual(sonuc[0]["satir"], [("bellek.musait_kb", 4096)])
                self.assertEqual(sonuc[1]["satir"], [(2,)])
            finally:
                iz.kapat()

    def test_sql_ayir(self):
        self.assertEqual(
            sql_ayir("-- Ergin Lab\nSELECT 1; SELECT 'a;b'"),
            ["SELECT 1", "SELECT 'a;b'"],
        )


if __name__ == "__main__":
    unittest.main()
