# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab

"""Ergin Lab servisi. Yapılandırmayı uygular, halkaları ve süreyi yönetir."""

from __future__ import annotations

import threading
import time
from pathlib import Path

from ergin_iz.cerceve import BASLIK_BOY, baslik_yap
from ergin_iz.gorev import ErginGorevKosucu
from ergin_iz.halka import HalkaTampon
from ergin_iz.kanal import DenetimKanali
from ergin_iz.sonda import TABLO
from ergin_iz.uretici import Uretici

IZLEK = {
    "dilim": 1,
    "sayac": 2,
    "zamanlayici": 3,
    "isaret": 4,
}


def kuvvet_iki(bayt: int) -> int:
    n = 4096
    while n < bayt:
        n *= 2
    return n


class Servis:
    """Ergin Android Atölyesi koordinasyon katmanı. Ergin Kaplan."""

    def __init__(self, ayar: dict):
        bilinmeyen = [ad for ad in ayar["kaynaklar"] if ad not in TABLO]
        if bilinmeyen:
            raise ValueError("bilinmeyen kaynak: " + ",".join(bilinmeyen))
        self.ayar = ayar
        self.paket = 0
        self.dusen = 0
        self.hatalar: list[str] = []
        self.istek_dur = threading.Event()
        self.kanal: DenetimKanali | None = None
        self._kilit = threading.Lock()

    def calistir(self, cikis: str | None = None) -> Path:
        yol = Path(cikis or self.ayar["cikis"])
        yol.parent.mkdir(parents=True, exist_ok=True)
        cap = kuvvet_iki(int(self.ayar["tampon_kb"]) * 1024)
        kosucu = ErginGorevKosucu()
        kosucu.baslat()
        dur = threading.Event()
        self.kanal = DenetimKanali(self)
        self.kanal.baslat()

        halkalar: dict[str, HalkaTampon] = {}
        ureticiler: dict[str, Uretici] = {}
        for ad in self.ayar["kaynaklar"]:
            halka = HalkaTampon(cap)
            halkalar[ad] = halka
            ureticiler[ad] = Uretici(ad, halka, IZLEK[ad])

        iplikler: list[threading.Thread] = []
        for ad in self.ayar["kaynaklar"]:
            iplik = threading.Thread(
                target=self._sonda_sar,
                args=(ad, ureticiler[ad], dur, kosucu),
                name=f"ergin-lab-{ad}",
                daemon=True,
            )
            iplik.start()
            iplikler.append(iplik)

        print(f"denetim_port={self.kanal.port}", flush=True)
        print("Ergin Android Lab servisi dinliyor.", flush=True)
        print("Ergin Kaplan · Ergin Lab · Ergin Android Atölyesi", flush=True)

        sure = int(self.ayar["sure_ms"]) / 1000.0
        bas = time.monotonic()
        with yol.open("wb") as dosya:
            dosya.write(
                baslik_yap(
                    uretici_sayisi=len(self.ayar["kaynaklar"]),
                    tampon_bayt=cap,
                )
            )
            dosya.flush()
            while time.monotonic() - bas < sure and not self.istek_dur.is_set():
                self._aktar(dosya, halkalar)
                time.sleep(0.01)
            dur.set()
            for iplik in iplikler:
                iplik.join(timeout=2.0)
            kosucu.bekle_adet(kosucu.bitti + len(kosucu._kuyruk), zaman=2.0)
            kosucu.durdur()
            self._aktar(dosya, halkalar)
            self.dusen = sum(h.dusen for h in halkalar.values())
            dosya.seek(0)
            dosya.write(
                baslik_yap(
                    uretici_sayisi=len(self.ayar["kaynaklar"]),
                    tampon_bayt=cap,
                    paket=self.paket,
                    dusen=self.dusen,
                )
            )
            if dosya.tell() != BASLIK_BOY:
                raise RuntimeError("Ergin İz başlığı yerinden oynadı")
        self.kanal.durdur()
        for hata in kosucu.hatalar:
            self.hatalar.append(str(hata))
        return yol

    def _sonda_sar(self, ad: str, uretici: Uretici, dur: threading.Event, kosucu) -> None:
        try:
            TABLO[ad](uretici, dur, self.ayar, kosucu)
        except Exception as exc:  # sonda tek başına servisi düşürmesin
            self.hatalar.append(f"{ad}: {exc}")

    def _aktar(self, dosya, halkalar: dict[str, HalkaTampon]) -> None:
        for halka in halkalar.values():
            for paket in halka.cek():
                dosya.write(paket)
                with self._kilit:
                    self.paket += 1
