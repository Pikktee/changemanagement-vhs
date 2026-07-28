#!/usr/bin/env python3
"""
Beobachtet folien.md und stil.css und baut bei jeder Aenderung neu.

    python3 watch.py

Laufen lassen und daneben folien.md bearbeiten. Nach jedem Speichern
entsteht die PowerPoint neu. Beenden mit Strg+C.
"""

import subprocess
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).parent
BEOBACHTET = [WURZEL / "folien.md", WURZEL / "stil.css"]


def stand():
    return tuple(p.stat().st_mtime if p.exists() else 0 for p in BEOBACHTET)


def baue():
    print("\n" + "─" * 62)
    subprocess.run([sys.executable, str(WURZEL / "build.py")], cwd=WURZEL)


def main():
    print("Beobachte folien.md und stil.css. Beenden mit Strg+C.")
    baue()
    letzter = stand()
    try:
        while True:
            time.sleep(1)
            jetzt = stand()
            if jetzt != letzter:
                letzter = jetzt
                time.sleep(0.4)      # Editor fertig schreiben lassen
                baue()
    except KeyboardInterrupt:
        print("\nBeendet.")


if __name__ == "__main__":
    main()
