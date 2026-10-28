# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab üreticisi. Olayı kendi halka tamponuna yazar."""

from __future__ import annotations

import os
import threading

from ergin_iz.cerceve import Olay, paket_yap, simdi
from ergin_iz.halka import HalkaTampon


class Uretici:
    """Ergin İz Atölyesi üretici süreci (bu çalışmada iş parçacığı)."""

    def __init__(self, ad: str, halka: HalkaTampon, izlek: int):
        self.ad = ad
        self.halka = halka
        self.izlek = izlek
        self.pid = os.getpid()

    def yayinla(self, olay: Olay) -> bool:
        olay.pid = self.pid & 0xFFFFFFFF
        olay.tid = threading.get_ident() & 0xFFFFFFFF
        olay.izlek = self.izlek
        if olay.ts == 0:
            olay.ts = simdi()
        return self.halka.yaz(paket_yap(olay))
