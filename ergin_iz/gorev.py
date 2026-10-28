# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab

"""Ergin Lab görev koşucusu.

Çoklu üretici tek tüketici. Üretici iş parçalarını kuyruğa bırakır.
Tek tüketici işi sırayla çalıştırır. Ergin İz Atölyesi içinde
dilim ölçümü bu koşucu üzerinden halkaya yazılır.
"""

from __future__ import annotations

import threading
import time
from collections import deque
from typing import Callable


class ErginGorevKosucu:
    """Ergin Kaplan çoklu üretici — tek tüketici görev yürütücüsü."""

    def __init__(self) -> None:
        self._kuyruk: deque[Callable[[], None]] = deque()
        self._kosul = threading.Condition()
        self._dur = False
        self._thread: threading.Thread | None = None
        self.bitti = 0
        self.hatalar: list[BaseException] = []

    def baslat(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(
            target=self._dongu,
            name="ergin-lab-gorev",
            daemon=True,
        )
        self._thread.start()

    def ekle(self, fn: Callable[[], None]) -> None:
        with self._kosul:
            if self._dur:
                raise RuntimeError("Ergin Lab görev koşucusu durdu")
            self._kuyruk.append(fn)
            self._kosul.notify()

    def bekle_adet(self, adet: int, zaman: float = 3.0) -> bool:
        son = time.monotonic() + zaman
        with self._kosul:
            while self.bitti < adet or self._kuyruk:
                kalan = son - time.monotonic()
                if kalan <= 0:
                    return False
                self._kosul.wait(kalan)
            return True

    def durdur(self, zaman: float = 2.0) -> None:
        with self._kosul:
            self._dur = True
            self._kosul.notify_all()
        if self._thread is not None:
            self._thread.join(timeout=zaman)

    def _dongu(self) -> None:
        while True:
            with self._kosul:
                while not self._kuyruk and not self._dur:
                    self._kosul.wait(0.1)
                if not self._kuyruk and self._dur:
                    return
                fn = self._kuyruk.popleft()
            try:
                fn()
            except BaseException as exc:  # görev düşmesin, kayıt sürsün
                self.hatalar.append(exc)
            with self._kosul:
                self.bitti += 1
                self._kosul.notify_all()
