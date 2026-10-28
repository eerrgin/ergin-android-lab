# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

import struct
import unittest

from ergin_iz.halka import HalkaHatasi, HalkaTampon


def paket(govde: bytes) -> bytes:
    return struct.pack("<I", len(govde)) + govde


class HalkaTest(unittest.TestCase):
    def test_gidis_donus(self):
        halka = HalkaTampon(256)
        beklenen = [paket(f"ergin-lab-{i}".encode()) for i in range(10)]
        for p in beklenen:
            self.assertTrue(halka.yaz(p))
        self.assertEqual(halka.cek(), beklenen)
        self.assertEqual(halka.cek(), [])
        self.assertEqual(halka.dusen, 0)

    def test_sarma(self):
        halka = HalkaTampon(64)
        ilk = paket(b"A" * 28)
        self.assertEqual(len(ilk), 32)
        self.assertTrue(halka.yaz(ilk))
        self.assertEqual(halka.cek(1), [ilk])
        sarilan = paket(b"C" * 36)
        self.assertEqual(len(sarilan), 40)
        self.assertTrue(halka.yaz(sarilan))
        self.assertEqual(halka.cek(), [sarilan])

    def test_dolu_duser(self):
        halka = HalkaTampon(64)
        govde = b"K" * 20
        p = paket(govde)
        yazilan = 0
        for _ in range(20):
            if halka.yaz(p):
                yazilan += 1
        self.assertGreater(halka.dusen, 0)
        self.assertEqual(len(halka.cek()), yazilan)
        self.assertEqual(yazilan + halka.dusen, 20)

    def test_kapasite(self):
        with self.assertRaises(HalkaHatasi):
            HalkaTampon(63)
        with self.assertRaises(HalkaHatasi):
            HalkaTampon(100)


if __name__ == "__main__":
    unittest.main()
