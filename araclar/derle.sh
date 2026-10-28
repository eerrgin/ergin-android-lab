#!/bin/sh
# © 2026 Ergin Kaplan
# Ergin Android Lab — Ergin Android Atölyesi — Ergin Lab
set -eu
kok=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cc -std=c11 -Wall -Wextra -O2 -o "$kok/cekirdek/ergin_halka_demo" \
  "$kok/cekirdek/halka.c" "$kok/cekirdek/demo.c"
"$kok/cekirdek/ergin_halka_demo"
