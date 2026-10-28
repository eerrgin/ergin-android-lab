# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

"""Ergin Lab paylaşımlı düzen: tek halkada bayt tamponu.

Sayaçlar monoton artar. Tampon adresi `konum % kapasite` ile sarılır.
Boş durum yazma sayacı ile okuma sayacının eşit olmasıdır.
Dolu durum, yeni kaydın sığmamasıdır. Ayrım için bir bayt boşluk
bırakmak gerekmez; sayaçlar modulo tutulmaz.
"""

from __future__ import annotations

import struct
import threading


class HalkaHatasi(ValueError):
    """Ergin Android Atölyesi halka hatası."""


class HalkaTampon:
    """Ergin Kaplan halka tamponu. Her üreticinin kendi halkası vardır."""

    def __init__(self, kapasite: int):
        if kapasite < 64 or kapasite & (kapasite - 1):
            raise HalkaHatasi("kapasite en az 64 ve ikinin kuvveti olmalı")
        self.kapasite = kapasite
        self._buf = bytearray(kapasite)
        self._w = 0
        self._r = 0
        self.dusen = 0
        self._kilit = threading.Lock()

    def yaz(self, paket: bytes) -> bool:
        """Uzunluk önekli paketi halkaya koyar. Sığmazsa düşürür."""
        ihtiyac = len(paket)
        if ihtiyac < 4 or ihtiyac > self.kapasite:
            with self._kilit:
                self.dusen += 1
            return False
        with self._kilit:
            if (self._w - self._r) + ihtiyac > self.kapasite:
                self.dusen += 1
                return False
            self._koy(self._w, paket)
            self._w += ihtiyac
            return True

    def cek(self, en_fazla: int | None = None) -> list[bytes]:
        """Hazır paketleri çıkarır. Her öğe uzunluk önekiyle birlikte döner."""
        cikti: list[bytes] = []
        with self._kilit:
            while self._w != self._r:
                if en_fazla is not None and len(cikti) >= en_fazla:
                    break
                if (self._w - self._r) < 4:
                    break
                (boy,) = struct.unpack("<I", self._al(self._r, 4))
                toplam = 4 + boy
                if boy > self.kapasite or (self._w - self._r) < toplam:
                    break
                cikti.append(self._al(self._r, toplam))
                self._r += toplam
        return cikti

    def kullanilan(self) -> int:
        with self._kilit:
            return self._w - self._r

    def _koy(self, konum: int, veri: bytes) -> None:
        cap = self.kapasite
        i = konum % cap
        ilk = min(len(veri), cap - i)
        self._buf[i : i + ilk] = veri[:ilk]
        if ilk < len(veri):
            kalan = len(veri) - ilk
            self._buf[:kalan] = veri[ilk:]

    def _al(self, konum: int, boy: int) -> bytes:
        cap = self.kapasite
        i = konum % cap
        ilk = min(boy, cap - i)
        if ilk == boy:
            return bytes(self._buf[i : i + boy])
        return bytes(self._buf[i : i + ilk] + self._buf[: boy - ilk])
