#!/usr/bin/env python3
"""Rechnet nach, ob das Farbsystem haelt, was DESIGN.md behauptet.

Die Arbeit argumentiert damit, dass die entscheidenden WCAG-Kriterien Stufe
AAA und deshalb nicht verbindlich sind. Wer so argumentiert, sollte die Stufe
im eigenen Foliensatz einhalten koennen — und zwar nachweisbar, nicht nach
Augenmass. Das Skript liest die Farbwerte aus stil.css, prueft jedes Paar,
das im Entwurf tatsaechlich vorkommt, und meldet jeden Verstoss.

    python3 pruefe-design.py

Zusaetzlich prueft es, dass stil.css, dokument.css und tool/index.html
dieselben Werte verwenden. Driften die auseinander, sieht man das sonst erst
im fertigen PDF.
"""
import pathlib
import re
import sys

WURZEL = pathlib.Path(__file__).resolve().parent
QUELLE = WURZEL / "stil.css"
WEITERE = [WURZEL / "dokument.css", WURZEL / "tool" / "index.html"]

# Jedes Paar, das im Entwurf vorkommt, mit seinem Mindestwert.
#   7.0  AAA fuer Fliesstext
#   4.5  AAA fuer grossen Text (ab 24px, oder ab 18.66px fett)
#   3.0  Rahmen und Bedienelemente, WCAG 1.4.11
#
# Drei Gruende dienen als Grund: --papier (weiss, Folie und Karte), --grund
# (Seitengrund des Werkzeugs) und --flaeche (ruhige Fuellung). Auf --flaeche
# steht nur noch --tinte und die Marke: seit --papier weiss ist, haelt
# --leise dort 6.80:1 und damit kein AAA mehr. Das ist eine Regel in
# DESIGN.md, kein weggelassenes Paar.
PAARE = [
    ("tinte", "papier", 7.0, "Fliesstext auf Folie und Karte"),
    ("leise", "papier", 7.0, "Nebentext, Beschriftungen, Quellenzeile"),
    ("marke", "papier", 7.0, "Auszeichnung im Text, Kennzahlen"),
    ("pflicht", "papier", 7.0, "Befund der Stufe PFLICHT, Fehlertext"),
    ("empfehlung", "papier", 7.0, "Befund der Stufe EMPFEHLUNG"),
    ("hinweis", "papier", 7.0, "Befund der Stufe HINWEIS"),
    ("geprueft", "papier", 7.0, "Bestaetigung im Text"),
    ("tinte", "grund", 7.0, "Fliesstext auf dem Seitengrund"),
    ("leise", "grund", 7.0, "Beschriftung auf dem Seitengrund"),
    ("marke", "grund", 7.0, "Aktion auf dem Seitengrund"),
    ("pflicht", "grund", 7.0, "Abweichungsknopf, Warnton auf Seitengrund"),
    ("empfehlung", "grund", 7.0, "Stufe EMPFEHLUNG auf Seitengrund"),
    ("hinweis", "grund", 7.0, "Stufe HINWEIS auf Seitengrund"),
    ("geprueft", "grund", 7.0, "Bestaetigung auf Seitengrund"),
    ("tinte", "flaeche", 7.0, "Text auf ruhiger Fuellflaeche"),
    # ("leise", "flaeche", ...) fehlt hier absichtlich: Die Kombination haelt
    # nur 6,80:1 und wird deshalb nirgends verwendet. Auf --flaeche steht
    # --tinte, so steht es auch im Prototyp.
    ("marke", "flaeche", 7.0, "Quadrantenkopf der Stakeholder-Matrix"),
    ("marke-dunkel", "flaeche", 7.0, "leiser Knopf, gedrueckt"),
    ("weiss", "marke", 7.0, "Text auf Markenflaeche, Callout, Knopf"),
    ("weiss", "marke-dunkel", 7.0, "Text auf gedruecktem Knopf"),
    ("weiss", "pflicht", 7.0, "Stufenmarke PFLICHT, Warnbalken"),
    ("weiss", "empfehlung", 7.0, "Stufenmarke EMPFEHLUNG"),
    ("weiss", "hinweis", 7.0, "Stufenmarke HINWEIS"),
    ("weiss", "geprueft", 7.0, "Stufenmarke ohne Beanstandung"),
    ("auf-marke", "marke", 4.5, "Titelakzent auf Markenflaeche, nur gross"),
    ("marke-dunkel", "auf-marke", 7.0, "Text auf hellblauer Flaeche"),
    ("tinte", "auf-marke", 7.0, "Suchtreffer, hellblau unterlegt"),
    ("rahmen", "papier", 3.0, "Rahmen von Bedienelementen, WCAG 1.4.11"),
    ("rahmen", "grund", 3.0, "Rahmen auf dem Seitengrund, WCAG 1.4.11"),
    ("rahmen", "flaeche", 3.0, "Rahmen auf Fuellflaeche, WCAG 1.4.11"),
]

ZUSATZ = {"weiss": "#FFFFFF"}


def _lin(kanal):
    c = kanal / 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def leuchtdichte(farbe):
    h = farbe.lstrip("#")
    if len(h) == 3:
        h = "".join(z * 2 for z in h)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def kontrast(vorne, hinten):
    a, b = leuchtdichte(vorne), leuchtdichte(hinten)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


def farben_lesen(datei):
    """Zieht die --name:#wert-Paare aus dem ersten :root-Block."""
    text = datei.read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\}", text, re.S)
    if not block:
        return {}
    return {n: w.upper() for n, w in
            re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\s*;", block.group(1))}


def main():
    farben = farben_lesen(QUELLE)
    if not farben:
        sys.exit(f"Kein :root-Block in {QUELLE.name} gefunden.")
    farben.update(ZUSATZ)

    fehler = 0

    print(f"Farbwerte aus {QUELLE.name}\n")
    print(f"  {'Vordergrund':14s} {'Grund':14s} {'Ist':>8s} {'Soll':>6s}  Verwendung")
    print("  " + "-" * 76)
    for vorne, hinten, soll, zweck in PAARE:
        if vorne not in farben or hinten not in farben:
            print(f"  ! Unbekannte Rolle: {vorne} auf {hinten}")
            fehler += 1
            continue
        ist = kontrast(farben[vorne], farben[hinten])
        haelt = ist >= soll
        if not haelt:
            fehler += 1
        marke = " " if haelt else "!"
        print(f"{marke} {vorne:14s} {hinten:14s} {ist:6.2f}:1 {soll:5.1f}:1  {zweck}")

    print("\nGleichstand der Dateien\n")
    gepruefte = [r for r, _, _, _ in PAARE] + [h for _, h, _, _ in PAARE]
    for datei in WEITERE:
        if not datei.exists():
            print(f"  ! {datei.name} fehlt")
            fehler += 1
            continue
        andere = farben_lesen(datei)
        abweichend = [
            f"{n}: {farben[n]} gegen {andere[n]}"
            for n in sorted(set(farben) & set(andere) & set(gepruefte))
            if farben[n] != andere[n]
        ]
        fehlend = sorted(set(gepruefte) - set(andere) - set(ZUSATZ))
        if abweichend:
            fehler += len(abweichend)
            print(f"  ! {datei.name}: " + "; ".join(abweichend))
        elif fehlend:
            print(f"    {datei.name}: gleich, ohne {', '.join(fehlend)}")
        else:
            print(f"    {datei.name}: gleich")

    if fehler:
        print(f"\n{fehler} Verstoss(e). DESIGN.md und die Dateien passen nicht "
              f"zusammen.")
        return 1
    print(f"\nAlle {len(PAARE)} Paare halten ihren Mindestwert, "
          f"die Dateien stimmen ueberein.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
