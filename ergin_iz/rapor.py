# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab metin raporu."""

from __future__ import annotations

from ergin_iz.islemci import IzIslemci


def _us_ms(ns: int) -> str:
    return f"{ns / 1_000_000:.3f} ms"


def metin_rapor(iz: IzIslemci) -> str:
    satirlar = [
        "Ergin İz raporu",
        "Ergin İz",
        "Ergin İz Atölyesi · Ergin Kaplan · Ergin Lab",
        "",
        "Üst bilgi",
    ]
    for row in iz.db.execute("SELECT anahtar, deger FROM ustbilgi ORDER BY anahtar"):
        satirlar.append(f"  {row['anahtar']}: {row['deger']}")
    sayilar = iz.db.execute(
        """
        SELECT
          (SELECT COUNT(*) FROM olaylar) AS olay,
          (SELECT COUNT(*) FROM dilimler) AS dilim,
          (SELECT COUNT(*) FROM sayaclar) AS sayac,
          (SELECT COUNT(*) FROM zamanlama) AS zaman,
          (SELECT COUNT(*) FROM isaretler) AS isaret,
          (SELECT COUNT(*) FROM acik_dilimler) AS acik
        """
    ).fetchone()
    satirlar.extend(
        [
            "",
            "Sayımlar",
            f"  olay: {sayilar['olay']}",
            f"  dilim: {sayilar['dilim']}",
            f"  sayaç: {sayilar['sayac']}",
            f"  zamanlama: {sayilar['zaman']}",
            f"  işaret: {sayilar['isaret']}",
            f"  açık dilim: {sayilar['acik']}",
            "",
            "En uzun dilimler",
        ]
    )
    uzun = iz.db.execute(
        """
        SELECT ad, kat, sur, derinlik
        FROM dilimler
        ORDER BY sur DESC
        LIMIT 8
        """
    ).fetchall()
    if not uzun:
        satirlar.append("  (yok)")
    for row in uzun:
        satirlar.append(
            f"  {_us_ms(row['sur'])}  d={row['derinlik']}  {row['kat']}  {row['ad']}"
        )
    satirlar.extend(["", "Dilim özeti"])
    ozet = iz.db.execute(
        """
        SELECT ad, COUNT(*) AS adet, AVG(sur) AS ortalama, MAX(sur) AS en_uzun
        FROM dilimler
        GROUP BY ad
        ORDER BY en_uzun DESC
        """
    ).fetchall()
    if not ozet:
        satirlar.append("  (yok)")
    for row in ozet:
        satirlar.append(
            f"  {row['ad']}  adet={row['adet']}  "
            f"ortalama={_us_ms(int(row['ortalama']))}  en_uzun={_us_ms(row['en_uzun'])}"
        )
    satirlar.extend(["", "Sayaçlar"])
    sayac = iz.db.execute(
        """
        SELECT ad, COUNT(*) AS adet, MIN(deger) AS en_kucuk, MAX(deger) AS en_buyuk
        FROM sayaclar
        GROUP BY ad
        ORDER BY ad
        """
    ).fetchall()
    if not sayac:
        satirlar.append("  (yok)")
    for row in sayac:
        satirlar.append(
            f"  {row['ad']}  adet={row['adet']}  "
            f"min={row['en_kucuk']}  max={row['en_buyuk']}"
        )
    satirlar.extend(["", "Zamanlama"])
    zaman = iz.db.execute(
        """
        SELECT ad, COUNT(*) AS adet, MAX(sonraki - onceki) AS en_buyuk_artis
        FROM zamanlama
        GROUP BY ad
        """
    ).fetchall()
    if not zaman:
        satirlar.append("  (yok)")
    for row in zaman:
        satirlar.append(
            f"  {row['ad']}  adet={row['adet']}  en_büyük_artış={row['en_buyuk_artis']}"
        )
    satirlar.extend(
        [
            "",
            "Ergin İz raporu bitti.",
            "Ergin Kaplan — Ergin Lab — Ergin İz Atölyesi",
        ]
    )
    return "\n".join(satirlar) + "\n"
