# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab iz yapılandırması. Kaynak listesi ve tampon boyu burada durur."""

from __future__ import annotations

import re
from pathlib import Path

GECERLI_KAYNAK = ("dilim", "sayac", "zamanlayici", "isaret")


class YapilandirmaHatasi(ValueError):
    """Ergin İz Atölyesi yapılandırma hatası."""


def yukle(yol: str | Path) -> dict:
    p = Path(yol)
    if not p.is_file():
        raise YapilandirmaHatasi(f"yapılandırma yok: {p}")
    return yukle_metin(p.read_text(encoding="utf-8"))


def yukle_metin(metin: str) -> dict:
    ayar: dict = {
        "tampon_kb": 256,
        "sure_ms": 1000,
        "cikis": "cikti/atolye.eiz",
        "dilim.yineleme": 6,
        "sayac.aralik_ms": 100,
        "zamanlayici.aralik_ms": 100,
        "isaret.aralik_ms": 150,
    }
    kaynaklar: list[str] = []
    for ham in metin.splitlines():
        satir = ham.split("#", 1)[0].strip()
        if not satir:
            continue
        if ":" not in satir:
            raise YapilandirmaHatasi(f"satır anlaşılamadı: {satir}")
        anahtar, deger = satir.split(":", 1)
        anahtar = anahtar.strip()
        deger = deger.strip()
        if anahtar == "kaynak":
            if deger not in GECERLI_KAYNAK:
                raise YapilandirmaHatasi(f"bilinmeyen kaynak: {deger}")
            if deger not in kaynaklar:
                kaynaklar.append(deger)
            continue
        if anahtar not in ayar and anahtar != "cikis":
            raise YapilandirmaHatasi(f"bilinmeyen ayar: {anahtar}")
        ayar[anahtar] = _cevir(deger) if anahtar != "cikis" else deger
    if not kaynaklar:
        kaynaklar = ["dilim", "isaret"]
    _denetle(ayar)
    ayar["kaynaklar"] = kaynaklar
    return ayar


def _cevir(deger: str):
    if re.fullmatch(r"-?\d+", deger):
        return int(deger)
    return deger


def _denetle(ayar: dict) -> None:
    tampon = ayar["tampon_kb"]
    sure = ayar["sure_ms"]
    if not isinstance(tampon, int) or not 4 <= tampon <= 65536:
        raise YapilandirmaHatasi("tampon_kb 4 ile 65536 arasında olmalı")
    if not isinstance(sure, int) or not 50 <= sure <= 600_000:
        raise YapilandirmaHatasi("sure_ms 50 ile 600000 arasında olmalı")
    for anahtar in (
        "dilim.yineleme",
        "sayac.aralik_ms",
        "zamanlayici.aralik_ms",
        "isaret.aralik_ms",
    ):
        deger = ayar[anahtar]
        if not isinstance(deger, int) or deger < 1:
            raise YapilandirmaHatasi(f"{anahtar} pozitif tam sayı olmalı")
