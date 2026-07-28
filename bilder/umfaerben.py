#!/usr/bin/env python3
"""Bildet die Illustrationen von der alten auf die neue Palette ab.

Die JPGs entstanden in der Petrol-Creme-Palette. Nach dem Wechsel auf das in
DESIGN.md festgelegte System passten sie nicht mehr zu den Folien. Neu
erzeugen waere Zufall — dieselben Formen kaemen nicht wieder heraus. Also
wird umgefaerbt.

Verfahren: Jedes Pixel wird dem naechstgelegenen Anker der alten Palette
zugeordnet und durch dessen neuen Wert ersetzt. Der Helligkeitsunterschied
zum Anker bleibt erhalten. Ein reines Ersetzen wuerde Verlaeufe und
Kantenglaettung platt machen und sichtbare Stufen erzeugen; so bleiben die
Balken auf der Titelfolie weich.

    python3 bilder/umfaerben.py            # faerbt und schreibt
    python3 bilder/umfaerben.py --probe    # zeigt nur, was passieren wuerde

Die Originale wandern nach bilder/original-petrol/ und bleiben dort. Ein
zweiter Lauf faerbt immer aus dem Original, nie aus dem Ergebnis — sonst
verschoebe sich die Farbe mit jedem Aufruf weiter.
"""
import pathlib
import shutil
import sys

from PIL import Image

HIER = pathlib.Path(__file__).resolve().parent
ORIGINAL = HIER / "original-petrol"

# alter Anker -> neuer Wert. Die Anker sind die Farben, aus denen die Bilder
# erzeugt wurden, die Ziele die Rollen aus stil.css.
ABBILDUNG = [
    ("#F4F1EA", "#F5F6F8"),  # Papier      -> hellster Neutralton
    ("#E7E2D5", "#EEF0F3"),  # ruhige Flaeche
    ("#124A53", "#14459E"),  # Petrol      -> Marke
    ("#0E3B42", "#0E3378"),  # dunkles Petrol -> Marke dunkel
    ("#6FD0C0", "#B9DFFA"),  # Mint        -> Akzent auf Marke
    ("#C4622D", "#A4162B"),  # Orange      -> Pflicht, das einzige Rot
    ("#191917", "#14171C"),  # Tinte
    ("#FFFFFF", "#FFFFFF"),  # Weiss bleibt
]

# Warum das alte Papier auf --grund geht und nicht auf --papier: --papier ist
# jetzt reines Weiss, und Weiss ist bereits der letzte Anker. Beide Anker auf
# denselben Wert zu legen presst die hellen Verlaeufe gegen die Obergrenze und
# erzeugt genau die Stufen, die dieses Skript vermeiden soll. --grund liegt
# eine Spur darunter, laesst den Lichtern Luft und gehoert zur Palette.


def rgb(wert):
    h = wert.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def helligkeit(farbe):
    r, g, b = farbe
    return 0.299 * r + 0.587 * g + 0.114 * b


def umfaerben(bild):
    anker = [(rgb(a), rgb(n)) for a, n in ABBILDUNG]
    hell_anker = [helligkeit(a) for a, _ in anker]
    breite, hoehe = bild.size
    px = list(bild.getdata())
    neu = []
    zwischen = {}
    for p in px:
        if p in zwischen:
            neu.append(zwischen[p])
            continue
        # naechster Anker im RGB-Raum
        i = min(range(len(anker)),
                key=lambda k: sum((p[j] - anker[k][0][j]) ** 2 for j in range(3)))
        # Helligkeitsabstand zum Anker uebernehmen, damit Verlaeufe und
        # weiche Kanten erhalten bleiben
        d = helligkeit(p) - hell_anker[i]
        ziel = anker[i][1]
        wert = tuple(max(0, min(255, round(ziel[j] + d))) for j in range(3))
        zwischen[p] = wert
        neu.append(wert)
    aus = Image.new("RGB", (breite, hoehe))
    aus.putdata(neu)
    return aus


def main():
    probe = "--probe" in sys.argv
    ORIGINAL.mkdir(exist_ok=True)
    bilder = sorted(p for p in HIER.glob("*.jpg") if p.parent == HIER)
    if not bilder:
        sys.exit("Keine JPGs in bilder/ gefunden.")
    for bild in bilder:
        quelle = ORIGINAL / bild.name
        if not quelle.exists():
            if probe:
                print(f"  {bild.name}: wuerde nach original-petrol/ gesichert")
                quelle = bild
            else:
                shutil.copy2(bild, quelle)
        if probe:
            print(f"  {bild.name}: wuerde aus {quelle.parent.name}/ umgefaerbt")
            continue
        ergebnis = umfaerben(Image.open(quelle).convert("RGB"))
        ergebnis.save(bild, quality=92, optimize=True)
        print(f"  {bild.name}  {bild.stat().st_size // 1024} kB")
    if not probe:
        print(f"\n{len(bilder)} Bilder umgefaerbt, Originale in "
              f"{ORIGINAL.name}/")


if __name__ == "__main__":
    main()
