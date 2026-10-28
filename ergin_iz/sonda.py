# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab veri kaynakları.

Dilim ölçümü görev koşucusunda çalışır.
Sayaç, zamanlama ve işaret kendi iş parçacığından halkaya yazılır.
Çekirdek sinyali olarak /proc/stat ve /proc/meminfo okunur; sarmalayıcı
Ergin İz Atölyesi kodudur.
"""

from __future__ import annotations

import threading
from pathlib import Path

from ergin_iz.cerceve import dilim_bas, dilim_bit, isaret, sayac, yeni_cerez, zamanlama
from ergin_iz.gorev import ErginGorevKosucu
from ergin_iz.uretici import Uretici


def oku_cpu_jiffy() -> tuple[int, int] | None:
    yol = Path("/proc/stat")
    if not yol.is_file():
        return None
    parca = yol.read_text(encoding="utf-8").splitlines()[0].split()
    if not parca or parca[0] != "cpu":
        return None
    sayilar = [int(x) for x in parca[1:]]
    if len(sayilar) < 4:
        return None
    return sum(sayilar), sayilar[3]


def oku_ctxt() -> int | None:
    yol = Path("/proc/stat")
    if not yol.is_file():
        return None
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if satir.startswith("ctxt "):
            return int(satir.split()[1])
    return None


def oku_bellek_kb() -> int | None:
    yol = Path("/proc/meminfo")
    if not yol.is_file():
        return None
    for satir in yol.read_text(encoding="utf-8").splitlines():
        if satir.startswith("MemAvailable:"):
            return int(satir.split()[1])
    return None


def cpu_yuzde_binde(once: tuple[int, int], sonra: tuple[int, int]) -> int:
    toplam = sonra[0] - once[0]
    bosta = sonra[1] - once[1]
    if toplam <= 0:
        return 0
    kullan = toplam - bosta
    if kullan < 0:
        kullan = 0
    return (kullan * 10000) // toplam


def calistir_dilim(
    uretici: Uretici,
    dur: threading.Event,
    ayar: dict,
    kosucu: ErginGorevKosucu,
) -> None:
    n = int(ayar["dilim.yineleme"])
    for _ in range(n):
        if dur.is_set():
            return

        def parca() -> None:
            dis = yeni_cerez()
            uretici.yayinla(dilim_bas("ergin.lab.cerceve", "Ergin Lab", dis))
            ic = yeni_cerez()
            uretici.yayinla(dilim_bas("ergin.lab.olcum", "Ergin İz", ic))
            toplam = 0
            for k in range(8000):
                toplam += k
            if toplam < 0:
                uretici.yayinla(isaret("ergin.lab.sapma", "Ergin Lab"))
            uretici.yayinla(dilim_bit("ergin.lab.olcum", "Ergin İz", ic))
            uretici.yayinla(dilim_bit("ergin.lab.cerceve", "Ergin Lab", dis))

        kosucu.ekle(parca)
        if dur.wait(0.02):
            return


def calistir_sayac(
    uretici: Uretici,
    dur: threading.Event,
    ayar: dict,
    kosucu: ErginGorevKosucu,
) -> None:
    kosucu.ekle(lambda: uretici.yayinla(isaret("ergin.lab.sayac.basladi", "Ergin İz")))
    once = oku_cpu_jiffy()
    aralik = int(ayar["sayac.aralik_ms"]) / 1000.0
    while not dur.is_set():
        if dur.wait(aralik):
            return
        sonra = oku_cpu_jiffy()
        if once is not None and sonra is not None:
            uretici.yayinla(
                sayac("cpu.oran_10000", "Ergin Lab", cpu_yuzde_binde(once, sonra))
            )
            once = sonra
        bellek = oku_bellek_kb()
        if bellek is not None:
            uretici.yayinla(sayac("bellek.musait_kb", "Ergin İz Atölyesi", bellek))


def calistir_zamanlayici(
    uretici: Uretici,
    dur: threading.Event,
    ayar: dict,
    kosucu: ErginGorevKosucu,
) -> None:
    kosucu.ekle(
        lambda: uretici.yayinla(isaret("ergin.lab.zamanlayici.basladi", "Ergin Lab"))
    )
    once = oku_ctxt()
    aralik = int(ayar["zamanlayici.aralik_ms"]) / 1000.0
    while not dur.is_set():
        if dur.wait(aralik):
            return
        sonra = oku_ctxt()
        if once is None or sonra is None:
            continue
        uretici.yayinla(
            zamanlama(
                "baglam.degisim",
                "Ergin İz",
                onceki=once,
                sonraki=sonra,
            )
        )
        once = sonra


def calistir_isaret(
    uretici: Uretici,
    dur: threading.Event,
    ayar: dict,
    kosucu: ErginGorevKosucu,
) -> None:
    del kosucu
    aralik = int(ayar["isaret.aralik_ms"]) / 1000.0
    while not dur.is_set():
        uretici.yayinla(isaret("ergin.lab.kalp", "Ergin İz Atölyesi"))
        if dur.wait(aralik):
            return


TABLO = {
    "dilim": calistir_dilim,
    "sayac": calistir_sayac,
    "zamanlayici": calistir_zamanlayici,
    "isaret": calistir_isaret,
}
