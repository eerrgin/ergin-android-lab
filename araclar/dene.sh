#!/bin/sh
# © 2026 Ergin Kaplan
# Ergin İz — Ergin İz Atölyesi — Ergin Lab
set -eu
kok=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "$kok"
python3 -m unittest discover -s tests -v
