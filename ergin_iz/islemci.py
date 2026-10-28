# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab SQL iz işlemcisi. Dilim, sayaç ve zamanlama tabloları."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from ergin_iz.bayrak import ATOLYE, LAB, MARKA, SURUM, URUN, YAZAR
from ergin_iz.cerceve import (
    TUR_DILIM_BAS,
    TUR_DILIM_BIT,
    TUR_ISARET,
    TUR_SAYAC,
    TUR_ZAMAN,
    TUR_AD,
    dosyayi_oku,
)


class SorguHatasi(ValueError):
    """Ergin İz Atölyesi sorgu hatası."""


def sql_ayir(metin: str) -> list[str]:
    parcalar: list[str] = []
    buf: list[str] = []
    tirnak = None
    i = 0
    while i < len(metin):
        c = metin[i]
        if tirnak:
            buf.append(c)
            if c == tirnak:
                tirnak = None
            i += 1
            continue
        if c in ("'", '"'):
            tirnak = c
            buf.append(c)
            i += 1
            continue
        if c == "-" and i + 1 < len(metin) and metin[i + 1] == "-":
            while i < len(metin) and metin[i] != "\n":
                i += 1
            continue
        if c == ";":
            parca = "".join(buf).strip()
            if parca:
                parcalar.append(parca)
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    son = "".join(buf).strip()
    if son:
        parcalar.append(son)
    return parcalar


class IzIslemci:
    """Ergin Kaplan tüketici katmanı."""

    def __init__(self, yol: str | Path):
        self.yol = Path(yol)
        self.baslik, self.olaylar = dosyayi_oku(self.yol)
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self._sema()
        self._yukle()

    def kapat(self) -> None:
        self.db.close()

    def calistir(self, sql: str) -> list[dict]:
        sonuclar = []
        try:
            for parca in sql_ayir(sql):
                cur = self.db.execute(parca)
                if cur.description is None:
                    sonuclar.append({"sql": parca, "kolon": [], "satir": []})
                    continue
                kolon = [c[0] for c in cur.description]
                satir = [tuple(r) for r in cur.fetchall()]
                sonuclar.append({"sql": parca, "kolon": kolon, "satir": satir})
        except sqlite3.Error as exc:
            raise SorguHatasi(str(exc)) from exc
        return sonuclar

    def _sema(self) -> None:
        self.db.executescript(
            """
            CREATE TABLE ustbilgi (
                anahtar TEXT PRIMARY KEY,
                deger TEXT
            );
            CREATE TABLE olaylar (
                id INTEGER PRIMARY KEY,
                ts INTEGER,
                tur INTEGER,
                tur_ad TEXT,
                pid INTEGER,
                tid INTEGER,
                izlek INTEGER,
                cerez INTEGER,
                deger INTEGER,
                cpu INTEGER,
                arg0 INTEGER,
                arg1 INTEGER,
                ad TEXT,
                kat TEXT
            );
            CREATE TABLE dilimler (
                id INTEGER PRIMARY KEY,
                ts INTEGER,
                sur INTEGER,
                ad TEXT,
                kat TEXT,
                izlek INTEGER,
                tid INTEGER,
                derinlik INTEGER,
                cerez INTEGER
            );
            CREATE TABLE sayaclar (
                ts INTEGER,
                ad TEXT,
                deger INTEGER,
                izlek INTEGER
            );
            CREATE TABLE zamanlama (
                ts INTEGER,
                cpu INTEGER,
                onceki INTEGER,
                sonraki INTEGER,
                ad TEXT,
                kat TEXT
            );
            CREATE TABLE isaretler (
                ts INTEGER,
                ad TEXT,
                kat TEXT,
                izlek INTEGER
            );
            CREATE TABLE acik_dilimler (
                ts INTEGER,
                ad TEXT,
                kat TEXT,
                izlek INTEGER,
                cerez INTEGER,
                derinlik INTEGER
            );
            """
        )

    def _yukle(self) -> None:
        meta = [
            ("urun", URUN),
            ("yazar", YAZAR),
            ("atolye", ATOLYE),
            ("lab", LAB),
            ("marka", MARKA),
            ("surum", SURUM),
            ("dosya", str(self.yol)),
            ("paket", str(self.baslik["paket"])),
            ("dusen", str(self.baslik["dusen"])),
            ("tampon", str(self.baslik["tampon"])),
            ("uretici", str(self.baslik["uretici"])),
            ("olusturma_ns", str(self.baslik["olusturma"])),
        ]
        self.db.executemany("INSERT INTO ustbilgi(anahtar, deger) VALUES (?, ?)", meta)
        yigin: dict[int, list[tuple]] = {}
        for sira, olay in enumerate(self.olaylar, start=1):
            self.db.execute(
                """
                INSERT INTO olaylar (
                    id, ts, tur, tur_ad, pid, tid, izlek, cerez, deger, cpu,
                    arg0, arg1, ad, kat
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    sira,
                    olay.ts,
                    olay.tur,
                    TUR_AD.get(olay.tur, "bilinmeyen"),
                    olay.pid,
                    olay.tid,
                    olay.izlek,
                    olay.cerez,
                    olay.deger,
                    olay.cpu,
                    olay.arg0,
                    olay.arg1,
                    olay.ad,
                    olay.kat,
                ),
            )
            if olay.tur == TUR_DILIM_BAS:
                st = yigin.setdefault(olay.izlek, [])
                st.append((olay, len(st)))
            elif olay.tur == TUR_DILIM_BIT:
                st = yigin.get(olay.izlek, [])
                bulunan = None
                for i in range(len(st) - 1, -1, -1):
                    if st[i][0].cerez == olay.cerez:
                        bulunan = i
                        break
                if bulunan is None:
                    continue
                bas, der = st.pop(bulunan)
                sur = olay.ts - bas.ts
                if sur < 0:
                    sur = 0
                self.db.execute(
                    """
                    INSERT INTO dilimler (ts, sur, ad, kat, izlek, tid, derinlik, cerez)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (bas.ts, sur, bas.ad, bas.kat, bas.izlek, bas.tid, der, bas.cerez),
                )
            elif olay.tur == TUR_SAYAC:
                self.db.execute(
                    "INSERT INTO sayaclar (ts, ad, deger, izlek) VALUES (?, ?, ?, ?)",
                    (olay.ts, olay.ad, olay.deger, olay.izlek),
                )
            elif olay.tur == TUR_ZAMAN:
                sonraki = olay.deger
                artis = olay.arg0
                onceki = sonraki - artis
                self.db.execute(
                    """
                    INSERT INTO zamanlama (ts, cpu, onceki, sonraki, ad, kat)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (olay.ts, olay.cpu, onceki, sonraki, olay.ad, olay.kat),
                )
            elif olay.tur == TUR_ISARET:
                self.db.execute(
                    "INSERT INTO isaretler (ts, ad, kat, izlek) VALUES (?, ?, ?, ?)",
                    (olay.ts, olay.ad, olay.kat, olay.izlek),
                )
        for st in yigin.values():
            for olay, der in st:
                self.db.execute(
                    """
                    INSERT INTO acik_dilimler (ts, ad, kat, izlek, cerez, derinlik)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (olay.ts, olay.ad, olay.kat, olay.izlek, olay.cerez, der),
                )
        self.db.commit()
