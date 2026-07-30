#!/usr/bin/env python3
"""Schreibt die Prompt-Staende aus der Git-Historie nach iterationen-staende.json.

Warum es diese Datei gibt: Das Panel bietet jede committete Iteration des
System-Prompts zur Auswahl an. Die Texte holt server.py aus `git show`. Auf
der Hosting-Plattform liegt aber kein .git — die Historie ist 846 MB gross und
steht in .railwayignore. Ohne diesen Export bliebe dort nur die laufende
Iteration waehlbar.

Vor jedem Deploy laufen lassen, und nach jedem Commit, der system-prompt.md
aendert:

    cd abschlussprojekt-vhs && python3 tool/iterationen-export.py
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# server.py bringt das Auslesen schon mit. Zweimal pflegen hiesse, dass die
# Ausgabe eines Tages nicht mehr zu dem passt, was der Server erwartet.
import server  # noqa: E402


def main():
    staende = server.staende_aus_git()
    if not staende:
        print("FEHLER: Keine Staende aus der Git-Historie gelesen.")
        print("  Laeuft das hier in einem Git-Arbeitsverzeichnis?")
        return 1

    jetzt = server.prompt_bauen()
    laufend = (jetzt["fassung"] or "").split("·")[0].strip()

    daten = {
        "hinweis": ("Erzeugt von tool/iterationen-export.py aus der "
                    "Git-Historie von system-prompt.md. Nicht von Hand "
                    "aendern; der Server liest sie nur, wenn kein .git "
                    "vorhanden ist."),
        "staende": staende,
    }
    server.STAENDE_DATEI.write_text(
        json.dumps(daten, ensure_ascii=False, indent=1),
        encoding="utf-8")

    groesse = server.STAENDE_DATEI.stat().st_size
    print("%s geschrieben, %d Iterationen, %.0f kB"
          % (server.STAENDE_DATEI.name, len(staende), groesse / 1000))
    for nummer in sorted(staende, key=server._fassung_sortwert, reverse=True):
        marke = "  <- laeuft" if nummer == laufend else ""
        print("  %-5s %s  %6d Zeichen%s"
              % (nummer, staende[nummer]["datum"],
                 len(staende[nummer]["prompt"]), marke))

    if laufend not in staende:
        print("\nHinweis: Die laufende Iteration %s ist noch nicht committet."
              % laufend)
        print("  Der Server nimmt dafuer die Arbeitskopie, das Hosting nicht.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
