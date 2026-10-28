# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin İz ikili çerçevesi. Ergin Lab veri düzlemi.

Dosya başlığı 48 bayttır. Ardından paketler gelir.
Her paket: little-endian u32 gövde boyu + gövde.
Gövde, sabit 52 baytlık alan ve iki uzunluk önekli metin taşır.
"""

from __future__ import annotations

import struct
import threading
import time
from dataclasses import dataclass
from pathlib import Path

SABIT = 52
BASLIK_BOY = 48
SABIT_BICIM = "<B3sQIIIQqIII"
BASLIK_BICIM = "<4sHHIHHQIIIQ4s"
SIHIR = b"EIZ1"
IMZA = b"ELAB"

TUR_DILIM_BAS = 1
TUR_DILIM_BIT = 2
TUR_SAYAC = 3
TUR_ZAMAN = 4
TUR_ISARET = 5

TUR_AD = {
    TUR_DILIM_BAS: "dilim_bas",
    TUR_DILIM_BIT: "dilim_bit",
    TUR_SAYAC: "sayac",
    TUR_ZAMAN: "zamanlama",
    TUR_ISARET: "isaret",
}

_cerez_kilit = threading.Lock()
_cerez = 0


class CerceveHatasi(ValueError):
    """Ergin İz çerçeve hatası."""


@dataclass
class Olay:
    tur: int
    ts: int
    pid: int
    tid: int
    izlek: int
    cerez: int
    deger: int
    cpu: int
    arg0: int
    arg1: int
    ad: str
    kat: str


def simdi() -> int:
    return time.perf_counter_ns()


def yeni_cerez() -> int:
    global _cerez
    with _cerez_kilit:
        _cerez += 1
        return _cerez


def olay_yap(
    tur: int,
    ad: str,
    kat: str,
    cerez: int = 0,
    deger: int = 0,
    cpu: int = 0,
    arg0: int = 0,
    arg1: int = 0,
    ts: int = 0,
) -> Olay:
    return Olay(
        tur=tur,
        ts=ts,
        pid=0,
        tid=0,
        izlek=0,
        cerez=cerez,
        deger=deger,
        cpu=cpu,
        arg0=arg0,
        arg1=arg1,
        ad=ad,
        kat=kat,
    )


def dilim_bas(ad: str, kat: str, cerez: int) -> Olay:
    return olay_yap(TUR_DILIM_BAS, ad, kat, cerez=cerez)


def dilim_bit(ad: str, kat: str, cerez: int) -> Olay:
    return olay_yap(TUR_DILIM_BIT, ad, kat, cerez=cerez)


def sayac(ad: str, kat: str, deger: int) -> Olay:
    return olay_yap(TUR_SAYAC, ad, kat, deger=deger)


def zamanlama(ad: str, kat: str, onceki: int, sonraki: int, cpu: int = 0) -> Olay:
    artis = sonraki - onceki
    if artis < 0:
        artis = 0
    if artis > 0xFFFFFFFF:
        artis = 0xFFFFFFFF
    return olay_yap(TUR_ZAMAN, ad, kat, deger=sonraki, cpu=cpu, arg0=artis, arg1=0)


def isaret(ad: str, kat: str) -> Olay:
    return olay_yap(TUR_ISARET, ad, kat)


def govde_yap(olay: Olay) -> bytes:
    ad = olay.ad.encode("utf-8")
    kat = olay.kat.encode("utf-8")
    if len(ad) > 65535 or len(kat) > 65535:
        raise CerceveHatasi("ad veya kat çok uzun")
    sabit = struct.pack(
        SABIT_BICIM,
        olay.tur & 0xFF,
        b"\0\0\0",
        olay.ts & 0xFFFFFFFFFFFFFFFF,
        olay.pid & 0xFFFFFFFF,
        olay.tid & 0xFFFFFFFF,
        olay.izlek & 0xFFFFFFFF,
        olay.cerez & 0xFFFFFFFFFFFFFFFF,
        int(olay.deger),
        olay.cpu & 0xFFFFFFFF,
        olay.arg0 & 0xFFFFFFFF,
        olay.arg1 & 0xFFFFFFFF,
    )
    if len(sabit) != SABIT:
        raise CerceveHatasi("sabit alan boyu şaştı")
    return sabit + struct.pack("<H", len(ad)) + ad + struct.pack("<H", len(kat)) + kat


def paket_yap(olay: Olay) -> bytes:
    govde = govde_yap(olay)
    return struct.pack("<I", len(govde)) + govde


def olay_coz(govde: bytes) -> Olay:
    if len(govde) < SABIT + 4:
        raise CerceveHatasi("gövde kısa")
    (
        tur,
        _pad,
        ts,
        pid,
        tid,
        izlek,
        cerez,
        deger,
        cpu,
        arg0,
        arg1,
    ) = struct.unpack_from(SABIT_BICIM, govde, 0)
    kon = SABIT
    if kon + 2 > len(govde):
        raise CerceveHatasi("ad boyu yok")
    (ad_boy,) = struct.unpack_from("<H", govde, kon)
    kon += 2
    if kon + ad_boy > len(govde):
        raise CerceveHatasi("ad kesik")
    ad = govde[kon : kon + ad_boy].decode("utf-8")
    kon += ad_boy
    if kon + 2 > len(govde):
        raise CerceveHatasi("kat boyu yok")
    (kat_boy,) = struct.unpack_from("<H", govde, kon)
    kon += 2
    if kon + kat_boy != len(govde):
        raise CerceveHatasi("kat sınırı tutmuyor")
    kat = govde[kon : kon + kat_boy].decode("utf-8")
    return Olay(
        tur=tur,
        ts=ts,
        pid=pid,
        tid=tid,
        izlek=izlek,
        cerez=cerez,
        deger=deger,
        cpu=cpu,
        arg0=arg0,
        arg1=arg1,
        ad=ad,
        kat=kat,
    )


def baslik_yap(
    uretici_sayisi: int,
    tampon_bayt: int,
    paket: int = 0,
    dusen: int = 0,
    olusturma: int | None = None,
) -> bytes:
    if olusturma is None:
        olusturma = time.time_ns()
    blok = struct.pack(
        BASLIK_BICIM,
        SIHIR,
        1,
        0,
        BASLIK_BOY,
        uretici_sayisi & 0xFFFF,
        0,
        olusturma & 0xFFFFFFFFFFFFFFFF,
        tampon_bayt & 0xFFFFFFFF,
        paket & 0xFFFFFFFF,
        dusen & 0xFFFFFFFF,
        0,
        IMZA,
    )
    if len(blok) != BASLIK_BOY:
        raise CerceveHatasi("başlık boyu 48 değil")
    return blok


def baslik_coz(blok: bytes) -> dict:
    if len(blok) < BASLIK_BOY:
        raise CerceveHatasi("başlık kısa")
    (
        sihir,
        surum,
        bayrak,
        baslik_boy,
        uretici,
        _pad,
        olusturma,
        tampon,
        paket,
        dusen,
        _ayrildi,
        imza,
    ) = struct.unpack_from(BASLIK_BICIM, blok, 0)
    if sihir != SIHIR or imza != IMZA:
        raise CerceveHatasi("Ergin İz başlığı değil")
    if surum != 1 or baslik_boy != BASLIK_BOY:
        raise CerceveHatasi("desteklenmeyen Ergin İz sürümü")
    return {
        "sihir": sihir,
        "surum": surum,
        "bayrak": bayrak,
        "baslik_boy": baslik_boy,
        "uretici": uretici,
        "olusturma": olusturma,
        "tampon": tampon,
        "paket": paket,
        "dusen": dusen,
        "imza": imza,
    }


def dosyayi_oku(yol: str | Path) -> tuple[dict, list[Olay]]:
    veri = Path(yol).read_bytes()
    if len(veri) < BASLIK_BOY:
        raise CerceveHatasi("dosya kısa")
    baslik = baslik_coz(veri[:BASLIK_BOY])
    olaylar: list[Olay] = []
    off = baslik["baslik_boy"]
    while off + 4 <= len(veri):
        (boy,) = struct.unpack_from("<I", veri, off)
        if boy == 0 or off + 4 + boy > len(veri):
            break
        olaylar.append(olay_coz(veri[off + 4 : off + 4 + boy]))
        off += 4 + boy
    return baslik, olaylar
