# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

import threading
import unittest

from ergin_iz.gorev import ErginGorevKosucu


class GorevTest(unittest.TestCase):
    def test_coklu_uretici(self):
        kosucu = ErginGorevKosucu()
        kosucu.baslat()
        kilit = threading.Lock()
        gelen = []

        def uret(no):
            def is_parcasi(no=no):
                with kilit:
                    gelen.append(no)

            for _ in range(25):
                kosucu.ekle(is_parcasi)

        iplikler = [threading.Thread(target=uret, args=(i,)) for i in range(4)]
        for iplik in iplikler:
            iplik.start()
        for iplik in iplikler:
            iplik.join()
        self.assertTrue(kosucu.bekle_adet(100, zaman=3))
        kosucu.durdur()
        self.assertEqual(sorted(gelen), sorted(list(range(4)) * 25))
        self.assertEqual(kosucu.hatalar, [])


if __name__ == "__main__":
    unittest.main()
