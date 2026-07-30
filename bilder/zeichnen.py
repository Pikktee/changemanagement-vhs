#!/usr/bin/env python3
"""Zeichnet die vier Bilder der Praesentation aus der Palette von stil.css.

    cd abschlussprojekt-vhs && python3 bilder/zeichnen.py

Warum gezeichnet und nicht erzeugt. Die Vorgaenger waren flach-geometrische
Bilder aus einem Bildmodell, nachtraeglich umgefaerbt. Drei Dinge gingen dabei
schief, und alle drei sind hier konstruktiv ausgeschlossen:

1. **Der graue Grund.** Das alte Bildpapier lag auf --grund (#F5F6F8), die
   Folie ist aber weiss. Jedes Bild sass damit als hellgraues Kaestchen auf
   weisser Flaeche. Hier ist der Grund --marke, also eine Entscheidung und
   kein Rest.
2. **Rot als Schmuck.** Alle drei alten Bilder trugen --pflicht als Zierde.
   DESIGN.md verbietet das ausdruecklich: Rot und Gruen sind mit Bedeutung
   belegt. In diesem Skript kommen die beiden Rollen nicht vor.
3. **Aussage.** Ein Bildmodell trifft die Aussage ungefaehr. Das alte
   Prozessbild setzte an die Stelle der fehlenden Verbindung einen roten
   Punkt — die Luecke sah dadurch wie ein Fehler aus und nicht wie das, was sie
   ist: ein Arbeitsschritt, den niemand vorgesehen hat.

Die Farbwerte kommen aus stil.css und werden nicht hier gepflegt. Wer dort eine
Rolle aendert, laesst dieses Skript neu laufen und die Bilder passen wieder.

Zwei Bildpaare, die dieselbe Aussage auf zwei Ebenen tragen:

    01-titel-wand      Wand aus Textzeilen, ein Schlitz            Titelfolie
    15-durchgang       dieselbe Wand, der Durchgang offen          Schlussfolie
    04-prozess-luecke  Kette mit leerer Stelle                     IST, Folie 4
    03-prozess-voll    dieselbe Kette, die Stelle besetzt          SOLL, Folie 3

Gezeichnet wird vierfach und dann heruntergerechnet; PIL kennt kein
Antialiasing fuer Flaechen.
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "bilder"
UEBER = 4  # vierfach zeichnen, dann herunterrechnen


def palette():
    """Liest die :root-Rollen aus stil.css. Einzige Quelle der Farbwerte."""
    text = (WURZEL / "stil.css").read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\}", text, re.S)
    if not block:
        sys.exit("Kein :root-Block in stil.css gefunden.")
    p = {n: w.upper() for n, w in
         re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", block.group(1))}
    for rolle in ("marke", "marke-dunkel", "auf-marke"):
        if rolle not in p:
            sys.exit(f"Rolle --{rolle} fehlt in stil.css.")
    # Rot und Gruen holen wir absichtlich nicht: siehe Kopf dieser Datei.
    return p


def leinwand(breite, hoehe, grund):
    bild = Image.new("RGB", (breite * UEBER, hoehe * UEBER), grund)
    return bild, ImageDraw.Draw(bild)


def fertig(bild, breite, hoehe, name):
    bild = bild.resize((breite, hoehe), Image.LANCZOS)
    pfad = ZIEL / name
    bild.save(pfad, "PNG", optimize=True)
    print(f"    {name}  {breite}x{hoehe}  {pfad.stat().st_size // 1024} kB")


def kasten(d, x, y, b, h, farbe):
    d.rectangle([x * UEBER, y * UEBER,
                 (x + b) * UEBER - 1, (y + h) * UEBER - 1], fill=farbe)


def rahmen(d, x, y, b, h, farbe, dicke):
    d.rectangle([x * UEBER, y * UEBER, (x + b) * UEBER - 1, (y + h) * UEBER - 1],
                outline=farbe, width=dicke * UEBER)


# --------------------------------------------------------------------------
# Die Wand aus Textzeilen — Titel- und Schlussfolie
# --------------------------------------------------------------------------

# Zeilenlaengen als Anteil der Wandbreite. Ungleich, damit die Wand wie
# gesetzter Text aussieht und nicht wie ein Strichcode. Von Hand gesetzt, damit
# das Bild bei jedem Lauf gleich herauskommt — Zufall waere hier ein Fehler.
ZEILEN = [1.00, 0.86, 0.94, 0.71, 1.00, 0.90, 0.62, 0.97, 0.83, 1.00,
          0.77, 0.93, 0.88, 1.00, 0.68, 0.95, 0.81, 1.00, 0.90, 0.74,
          0.98, 0.86, 1.00, 0.79, 0.92]


def wand(p, name, offen):
    """Wand aus waagerechten Zeilen mit einem senkrechten Durchgang.

    Die Panel-Folien legen einen Verlauf darueber: --marke deckend bis 46
    Prozent der Breite, dann bis --marke-62 nach rechts. Sichtbar ist also nur
    die rechte Haelfte, und die durch einen Blauschleier. Deshalb steht die
    Wand rechts, der Grund ist --marke-dunkel und die Zeilen sind --auf-marke:
    Ein feiner Kontrast waere unter dem Schleier verschwunden.
    """
    B, H = 1280, 720
    bild, d = leinwand(B, H, p["marke-dunkel"])

    links = 470          # links davon deckt der Verlauf ohnehin alles ab
    rechts = B - 78
    wandbreite = rechts - links
    zh, luecke = 15, 11  # Zeilenhoehe und Abstand
    oben = 62

    # Der Durchgang. Auf der Titelfolie ein Schlitz, auf der Schlussfolie
    # begehbar. Dieselbe Wand, ein anderer Wert — das ist die ganze Aussage
    # der beiden Bilder.
    spalt = 128 if offen else 15
    spalt_x = links + int(wandbreite * 0.58)

    for i, anteil in enumerate(ZEILEN):
        y = oben + i * (zh + luecke)
        if y + zh > H - oben:
            break
        ende = links + int(wandbreite * anteil)
        # Zeile links des Durchgangs
        if spalt_x > links:
            kasten(d, links, y, min(ende, spalt_x) - links, zh, p["auf-marke"])
        # Zeile rechts des Durchgangs, nur wo die Zeile ueberhaupt hinreicht
        nach = spalt_x + spalt
        if ende > nach:
            kasten(d, nach, y, ende - nach, zh, p["auf-marke"])

    if offen:
        # Hinter dem Durchgang wird es hell. Weiss, weil auf Markenflaeche
        # laut DESIGN.md Weiss oder --auf-marke gilt und sonst nichts.
        kasten(d, spalt_x, 0, spalt, H, "#FFFFFF")

    # build.py rendert die Folie in doppelter Aufloesung. Ein Bild in 1280x720
    # wuerde dort hochskaliert.
    fertig(bild, B * 2, H * 2, name)


# --------------------------------------------------------------------------
# Die Kette der Arbeitsschritte — Folie 3 und Folie 4
# --------------------------------------------------------------------------

def prozess(p, name, besetzt):
    """Vier Arbeitsschritte untereinander, dazwischen eine offene Stelle.

    Folie 4 sagt: zwischen Einpflegen und Erscheinen ist kein Pruefschritt
    vorgesehen. Deshalb sind vier Schritte gefuellt und die fuenfte Stelle ist
    ein leerer Rahmen ohne Verbindung nach oben und unten — nicht ein Fehler,
    sondern eine Stelle, an der nichts steht. Auf Folie 3 ist dieselbe Stelle
    besetzt, in --auf-marke, damit man den neuen Schritt von den vier
    vorhandenen unterscheidet.

    Der Rahmen der Bildspalte ist 322x334 und schneidet mit 'cover'. Gezeichnet
    wird deshalb annaehernd quadratisch und die Kette sitzt mittig.
    """
    B, H = 322, 334
    bild, d = leinwand(B, H, p["marke"])

    # Zwei Anlaeufe kosteten das: 152x44 mit 18px Abstand las sich als weisser
    # Block mit Schlitzen; 204 breit fuellte die Bildspalte so weit, dass die
    # Verbindungen wie Kerben im Rand wirkten. Entscheidend ist, dass links und
    # rechts der Kaesten genug Grund sichtbar bleibt.
    kb, kh = 138, 32         # Kasten
    mitte_x = (B - kb) // 2
    verb_b = 8               # Verbindungsstueck
    verb_h = 30
    OFFEN = 3                # Position der offenen Stelle, nullbasiert
    schritte = 5             # vier vorhandene Schritte, dazu die offene Stelle

    ganz = schritte * kh + (schritte - 1) * verb_h
    y = (H - ganz) // 2

    for i in range(schritte):
        oy = y + i * (kh + verb_h)
        if i != OFFEN:
            kasten(d, mitte_x, oy, kb, kh, "#FFFFFF")
        elif besetzt:
            kasten(d, mitte_x, oy, kb, kh, p["auf-marke"])
        else:
            rahmen(d, mitte_x, oy, kb, kh, p["auf-marke"], 2)

        # Verbindung zum naechsten Schritt. Die beiden, die an die offene
        # Stelle grenzen, fehlen ganz, solange sie leer ist: Ohne den Schritt
        # haengt die Kette dort nicht zusammen. Ist die Stelle besetzt, tragen
        # dieselben zwei Verbindungen die Akzentfarbe — man sieht, was neu ist.
        if i == schritte - 1:
            continue
        grenzt = i in (OFFEN - 1, OFFEN)
        if grenzt and not besetzt:
            continue
        kasten(d, mitte_x + (kb - verb_b) // 2, oy + kh, verb_b, verb_h,
               p["auf-marke"] if grenzt else "#FFFFFF")

    fertig(bild, B * 3, H * 3, name)


def main():
    p = palette()
    print(f"Palette aus stil.css: --marke {p['marke']}, "
          f"--marke-dunkel {p['marke-dunkel']}, --auf-marke {p['auf-marke']}\n")
    print("  Panel-Folien, 1280x720 unter dem Blauverlauf:")
    wand(p, "01-titel-wand.png", offen=False)
    wand(p, "15-durchgang.png", offen=True)
    print("\n  Bildspalte, 322x334 in dreifacher Aufloesung:")
    prozess(p, "04-prozess-luecke.png", besetzt=False)
    prozess(p, "03-prozess-voll.png", besetzt=True)
    print("\nFertig. Kein Rot, kein Gruen, kein grauer Grund.")


if __name__ == "__main__":
    main()
