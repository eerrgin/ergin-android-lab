# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin İz komut satırı. Ergin İz."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ergin_iz.bayrak import ACIKLAMA, BANNER, SURUM, YAZAR
from ergin_iz.cerceve import dosyayi_oku
from ergin_iz.islemci import IzIslemci, SorguHatasi
from ergin_iz.kanal import KanalHatasi, denetim_sor
from ergin_iz.rapor import metin_rapor
from ergin_iz.servis import Servis
from ergin_iz.yapilandirma import YapilandirmaHatasi, yukle


def _tablo(sonuc: dict) -> str:
    kolon = sonuc["kolon"]
    satirlar = sonuc["satir"]
    if not kolon:
        return "(satır dönmedi)\n"
    gen = [len(ad) for ad in kolon]
    metinler = []
    for satir in satirlar:
        hucre = [str(h) for h in satir]
        metinler.append(hucre)
        for i, h in enumerate(hucre):
            gen[i] = max(gen[i], len(h))
    cizgi = "  ".join(ad.ljust(gen[i]) for i, ad in enumerate(kolon))
    ayir = "  ".join("-" * gen[i] for i in range(len(kolon)))
    govde = [
        "  ".join(h.ljust(gen[i]) for i, h in enumerate(satir)) for satir in metinler
    ]
    return "\n".join([cizgi, ayir, *govde]) + "\n"


def _kaydet(args) -> int:
    try:
        ayar = yukle(args.yapilandirma)
    except YapilandirmaHatasi as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 2
    if args.cikis:
        ayar["cikis"] = args.cikis
    print(BANNER)
    servis = Servis(ayar)
    yol = servis.calistir()
    print(f"kayit={yol}")
    print(f"paket={servis.paket} dusen={servis.dusen}")
    for hata in servis.hatalar:
        print(f"uyari: {hata}", file=sys.stderr)
    print("Ergin İz kaydı tamam.")
    print("Ergin Kaplan · Ergin Lab · Ergin İz Atölyesi")
    return 0


def _sorgula(args) -> int:
    if not Path(args.iz).is_file():
        print("hata: iz dosyası yok", file=sys.stderr)
        return 2
    if args.sorgu_dosyasi:
        sql = Path(args.sorgu_dosyasi).read_text(encoding="utf-8")
    else:
        sql = args.sorgu
    iz = IzIslemci(args.iz)
    try:
        sonuclar = iz.calistir(sql)
    except SorguHatasi as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
    finally:
        iz.kapat()
    print(BANNER)
    for sonuc in sonuclar:
        print(sonuc["sql"])
        print(_tablo(sonuc), end="")
        print()
    return 0


def _rapor(args) -> int:
    if not Path(args.iz).is_file():
        print("hata: iz dosyası yok", file=sys.stderr)
        return 2
    iz = IzIslemci(args.iz)
    try:
        print(metin_rapor(iz), end="")
    finally:
        iz.kapat()
    return 0


def _cozumle(args) -> int:
    if not Path(args.iz).is_file():
        print("hata: iz dosyası yok", file=sys.stderr)
        return 2
    baslik, olaylar = dosyayi_oku(args.iz)
    print(BANNER)
    print(f"yazar={YAZAR}")
    print("marka=Ergin İz")
    print("atolye=Ergin İz Atölyesi")
    print("lab=Ergin Lab")
    for anahtar in ("surum", "uretici", "tampon", "paket", "dusen", "olusturma"):
        print(f"{anahtar}={baslik[anahtar]}")
    print(f"okunan={len(olaylar)}")
    return 0


def _denetim(args) -> int:
    try:
        print(denetim_sor(args.port, args.komut), end="")
    except (OSError, KanalHatasi) as exc:
        print(f"hata: {exc}", file=sys.stderr)
        return 1
    return 0


def _surum(_args) -> int:
    print(BANNER)
    print(f"surum={SURUM}")
    print(f"yazar={YAZAR}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ayr = argparse.ArgumentParser(prog="ergin-iz", description=ACIKLAMA)
    alt = ayr.add_subparsers(dest="komut", required=True)

    kaydet = alt.add_parser("kaydet", help="Ergin Lab iz kaydı al")
    kaydet.add_argument("-c", "--yapilandirma", required=True)
    kaydet.add_argument("-o", "--cikis")
    kaydet.set_defaults(fn=_kaydet)

    sorgula = alt.add_parser("sorgula", help="SQL çalıştır")
    sorgula.add_argument("-i", "--iz", required=True)
    grup = sorgula.add_mutually_exclusive_group(required=True)
    grup.add_argument("-q", "--sorgu")
    grup.add_argument("-s", "--sorgu-dosyasi")
    sorgula.set_defaults(fn=_sorgula)

    rapor = alt.add_parser("rapor", help="Ergin İz metin raporu")
    rapor.add_argument("-i", "--iz", required=True)
    rapor.set_defaults(fn=_rapor)

    cozumle = alt.add_parser("cozumle", help="başlık ve paket sayısı")
    cozumle.add_argument("-i", "--iz", required=True)
    cozumle.set_defaults(fn=_cozumle)

    denetim = alt.add_parser("denetim", help="yerel servise komut gönder")
    denetim.add_argument("--port", type=int, required=True)
    denetim.add_argument("--komut", required=True)
    denetim.set_defaults(fn=_denetim)

    surum = alt.add_parser("surum", help="Ergin Kaplan sürüm satırı")
    surum.set_defaults(fn=_surum)

    args = ayr.parse_args(argv)
    return args.fn(args)
