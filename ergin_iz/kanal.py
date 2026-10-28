# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab denetim kanalı.

Yalnızca 127.0.0.1 dinlenir. Çerçeve: big-endian u32 boy + UTF-8 metin.
En fazla 4096 bayt. Kabuk çağrısı yoktur.
"""

from __future__ import annotations

import socket
import struct
import threading

AZAMI = 4096


class KanalHatasi(RuntimeError):
    """Ergin İz denetim hatası."""


def tam_oku(sock: socket.socket, boy: int) -> bytes | None:
    parca: list[bytes] = []
    kalan = boy
    while kalan:
        try:
            blok = sock.recv(kalan)
        except socket.timeout:
            return None
        if not blok:
            return None
        parca.append(blok)
        kalan -= len(blok)
    return b"".join(parca)


def yanit_yaz(sock: socket.socket, metin: str) -> None:
    veri = metin.encode("utf-8")
    sock.sendall(struct.pack(">I", len(veri)) + veri)


def denetim_sor(port: int, komut: str, zaman: float = 2.0) -> str:
    with socket.create_connection(("127.0.0.1", port), timeout=zaman) as sock:
        sock.settimeout(zaman)
        veri = komut.encode("utf-8")
        if len(veri) > AZAMI:
            raise KanalHatasi("komut çok uzun")
        sock.sendall(struct.pack(">I", len(veri)) + veri)
        bas = tam_oku(sock, 4)
        if bas is None:
            raise KanalHatasi("yanıt başlığı gelmedi")
        (boy,) = struct.unpack(">I", bas)
        if boy > 65536:
            raise KanalHatasi("yanıt çok büyük")
        govde = tam_oku(sock, boy)
        if govde is None:
            raise KanalHatasi("yanıt gövdesi gelmedi")
        return govde.decode("utf-8")


class DenetimKanali:
    """Ergin Kaplan yerel denetim soketi."""

    def __init__(self, servis) -> None:
        self.servis = servis
        self._sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sunucu.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sunucu.bind(("127.0.0.1", 0))
        self._sunucu.listen(8)
        self._sunucu.settimeout(0.2)
        self.port = self._sunucu.getsockname()[1]
        self._dur = threading.Event()
        self._thread: threading.Thread | None = None

    def baslat(self) -> None:
        self._thread = threading.Thread(
            target=self._dongu,
            name="ergin-lab-denetim",
            daemon=True,
        )
        self._thread.start()

    def durdur(self) -> None:
        self._dur.set()
        try:
            self._sunucu.close()
        except OSError:
            pass
        if self._thread is not None:
            self._thread.join(timeout=1.0)

    def _dongu(self) -> None:
        while not self._dur.is_set():
            try:
                bag, _adres = self._sunucu.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=self._ele_al,
                args=(bag,),
                name="ergin-lab-istemci",
                daemon=True,
            ).start()

    def _ele_al(self, bag: socket.socket) -> None:
        with bag:
            bag.settimeout(1.0)
            try:
                bas = tam_oku(bag, 4)
                if bas is None:
                    return
                (boy,) = struct.unpack(">I", bas)
                if boy == 0 or boy > AZAMI:
                    yanit_yaz(bag, "HATA cerceve\n")
                    return
                govde = tam_oku(bag, boy)
                if govde is None:
                    return
                komut = govde.decode("utf-8", "replace").strip()
                yanit_yaz(bag, self._cevap(komut))
            except OSError:
                return

    def _cevap(self, komut: str) -> str:
        soz = komut.split()[0].upper() if komut.split() else ""
        if soz == "DURUM":
            kaynak = ",".join(self.servis.ayar["kaynaklar"])
            return (
                "ERGIN_LAB TAMAM\n"
                "atolye=Ergin İz Atölyesi\n"
                "lab=Ergin Lab\n"
                "marka=Ergin İz\n"
                "yazar=Ergin Kaplan\n"
                f"paket={self.servis.paket}\n"
                f"kaynak={kaynak}\n"
            )
        if soz == "KAYNAKLAR":
            satir = "\n".join(self.servis.ayar["kaynaklar"])
            return f"ERGIN_LAB TAMAM\n{satir}\n"
        if soz == "YAZAR":
            return (
                "Ergin Kaplan\n"
                "Ergin İz\n"
                "Ergin İz Atölyesi\n"
                "Ergin Lab\n"
            )
        if soz == "DUR":
            self.servis.istek_dur.set()
            return "ERGIN_LAB TAMAM\ndur=1\n"
        return "HATA bilinmeyen\n"
