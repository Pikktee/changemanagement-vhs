#!/usr/bin/env python3
"""Erzeugt die vier Bilder der Praesentation aus Palette und Schrift des Systems.

    cd abschlussprojekt-vhs && python3 bilder/zeichnen.py

Warum ueber Chrome und nicht mit PIL. Die Vorgaenger waren mit PIL gezeichnet,
und daran ist zweierlei gescheitert:

1. **Keine Schrift.** PIL braucht eine TTF, das System liefert woff2. Die
   Prozessbilder bestanden deshalb aus fuenf leeren weissen Balken. Ein
   Ablaufbild, dessen Stationen keine Woerter tragen, zeigt ein Muster und
   keine Kette mit einer Luecke — niemand konnte es ohne Bildunterschrift
   entziffern.
2. **Keine weichen Kanten.** PIL kennt kein Antialiasing fuer Flaechen. Der
   Umweg war vierfach zeichnen und herunterrechnen; gestrichelte Linien und
   Schriftkanten wurden davon trotzdem nicht gut.

Chrome loest beides: dieselbe Schrift, dieselben Farbrollen und derselbe
Renderweg wie in build.py. Die Farbwerte kommen weiterhin aus stil.css und
werden hier nicht gepflegt.

Was davor schon richtig war und bleibt:

* **Kein grauer Grund.** Das alte Bildpapier lag auf --grund, die Folie ist
  weiss; jedes Bild sass als hellgraues Kaestchen darauf. Der Grund ist --marke.
* **Rot und Gruen kommen nicht vor.** DESIGN.md belegt beide mit Bedeutung;
  als Schmuck sind sie verboten.
* **Die Luecke ist kein Fehler.** Sie ist eine Stelle, an der niemand einen
  Arbeitsschritt vorgesehen hat, und wird deshalb gestrichelt und leer
  gezeichnet, nicht rot markiert.

Vier Bilder, zwei Paare:

    01-titel-wand      Wand aus Textzeilen, ein Schlitz            Titelfolie
    15-durchgang       dieselbe Wand, der Durchgang offen          Schlussfolie
    04-prozess-luecke  Kette mit offener Stelle                    IST, Folie 4
    03-prozess-voll    dieselbe Kette, die Stelle besetzt          SOLL, Folie 3
"""
import pathlib
import re
import shutil
import subprocess
import sys
import time

WURZEL = pathlib.Path(__file__).resolve().parent.parent
ZIEL = WURZEL / "bilder"
TEMP = ZIEL / ".render"
PORT = 8795  # eigener Testport laut CLAUDE.md, beisst sich nicht mit build.py
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Die vier Stationen des Ablaufs, wie sie auf Folie 4 in der rechten Spalte
# stehen. Die offene Stelle liegt zwischen Einpflegen und Erscheinen — genau
# dort, wo der Sprechtext sagt, dass kein Pruefschritt vorgesehen ist.
STATIONEN = ["Planen", "Schreiben", "Einpflegen", None, "Erscheinen"]
OFFEN = STATIONEN.index(None)
NEUER_SCHRITT = "Prüfen"

# Zeilenlaengen der Wand als Anteil der Wandbreite. Ungleich, damit sie wie
# gesetzter Text aussieht und nicht wie ein Strichcode. Von Hand gesetzt, damit
# das Bild bei jedem Lauf gleich herauskommt — Zufall waere hier ein Fehler.
ZEILEN = [1.00, 0.86, 0.94, 0.71, 1.00, 0.90, 0.62, 0.97, 0.83, 1.00,
          0.77, 0.93, 0.88, 1.00, 0.68, 0.95, 0.81, 1.00, 0.90, 0.74,
          0.98, 0.86, 1.00, 0.79, 0.92]


def palette():
    """Liest die :root-Rollen aus stil.css. Einzige Quelle der Farbwerte."""
    text = (WURZEL / "stil.css").read_text(encoding="utf-8")
    block = re.search(r":root\s*\{(.*?)\n\}", text, re.S)
    if not block:
        sys.exit("Kein :root-Block in stil.css gefunden.")
    p = {n: w.upper() for n, w in
         re.findall(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})\s*;", block.group(1))}
    for rolle in ("marke", "marke-dunkel", "auf-marke"):
        if rolle not in p:
            sys.exit(f"Rolle --{rolle} fehlt in stil.css.")
    return p


# --------------------------------------------------------------------------
# Die Kette der Arbeitsschritte — Folie 3 und Folie 4
# --------------------------------------------------------------------------

def prozess_html(p, besetzt):
    """Fuenf Stationen untereinander, eine davon offen oder besetzt.

    Der Rahmen der Bildspalte ist 322x334 und schneidet mit 'cover'. Gezeichnet
    wird deshalb genau in diesem Verhaeltnis, dann wird nichts beschnitten.

    Die beiden Verbindungen, die an die offene Stelle grenzen, fehlen im
    IST-Bild ganz: Ohne den Schritt haengt die Kette dort nicht zusammen. Im
    SOLL-Bild tragen dieselben zwei Verbindungen die Akzentfarbe — man sieht,
    was neu ist, ohne es beschriften zu muessen.
    """
    teile = []
    for i, name in enumerate(STATIONEN):
        if i:
            grenzt = i in (OFFEN, OFFEN + 1)
            if grenzt and not besetzt:
                teile.append('<span class="verb leer"></span>')
            else:
                teile.append(
                    f'<span class="verb{" neu" if grenzt else ""}"></span>')
        if name is not None:
            teile.append(f'<span class="stat">{name}</span>')
        elif besetzt:
            teile.append(f'<span class="stat neu">{NEUER_SCHRITT}</span>')
        else:
            teile.append('<span class="stat offen"></span>')

    return f"""<meta charset="utf-8">
<style>
  @import url('../schriften/schriften.css');
  *{{ margin:0; padding:0; box-sizing:border-box; }}
  body{{ width:322px; height:334px; background:{p['marke']};
         font-family:'Atkinson Hyperlegible Next',sans-serif;
         display:flex; flex-direction:column; align-items:center;
         justify-content:center; }}
  /* Station: weisse Flaeche mit Beschriftung. Die Versalien folgen der
     Plakette .spkopf aus stil.css, damit das Bild zur Folie gehoert. */
  .stat{{ width:206px; height:38px; background:#fff; color:{p['marke-dunkel']};
          display:flex; align-items:center; justify-content:center;
          font-size:12.5px; font-weight:700; letter-spacing:1.5px;
          text-transform:uppercase; }}
  /* Der neue Schritt in der Akzentfarbe. Text darauf ist --marke-dunkel,
     so schreibt es DESIGN.md vor. */
  .stat.neu{{ background:{p['auf-marke']}; }}
  /* Die offene Stelle: gestrichelt und leer. Kein Rot — es ist kein Fehler,
     sondern ein Schritt, den niemand vorgesehen hat. */
  .stat.offen{{ background:transparent;
                border:2px dashed {p['auf-marke']}; }}
  .verb{{ width:7px; height:26px; background:#fff; }}
  .verb.neu{{ background:{p['auf-marke']}; }}
  .verb.leer{{ background:transparent; }}
</style>
{"".join(teile)}"""


# --------------------------------------------------------------------------
# Die Wand aus Textzeilen — Titel- und Schlussfolie
# --------------------------------------------------------------------------

def wand_html(p, offen):
    """Wand aus waagerechten Zeilen mit einem senkrechten Durchgang.

    Die Panel-Folien legen einen Verlauf darueber: --marke deckend bis 46
    Prozent der Breite, dann bis --marke-62 nach rechts. Sichtbar ist also nur
    die rechte Haelfte, und die durch einen Blauschleier. Deshalb steht die
    Wand rechts, der Grund ist --marke-dunkel und die Zeilen sind --auf-marke:
    Ein feiner Kontrast waere unter dem Schleier verschwunden.

    Die untere Grenze ist keine Schaetzung: Die Fusszeile der Panel-Folie
    beginnt bei y=631 mit ihrer Trennlinie, der Text darunter bei 646 (im
    Browser gemessen). Die Wand lief einmal bis 658 und damit mitten hinein.

    Der Durchgang reicht als einziges Element von oben nach unten durch, denn
    einer, der vor dem Rand aufhoert, ist ein Schlitz. Er sitzt bei 46 Prozent
    der Wandbreite und damit links der rechten Fusszeile, die bei x=959
    beginnt.
    """
    B, H = 1280, 720
    links, rechts = 470, B - 78
    breite = rechts - links
    zh, luecke = 15, 11
    oben, unten = 60, 631 - 18
    spalt = 128 if offen else 15
    spalt_x = links + int(breite * 0.46)

    passen = (unten - oben + luecke) // (zh + luecke)
    hoch = passen * zh + (passen - 1) * luecke
    start = oben + (unten - oben - hoch) // 2

    balken = []
    for i, anteil in enumerate(ZEILEN[:passen]):
        y = start + i * (zh + luecke)
        ende = links + int(breite * anteil)
        if spalt_x > links:
            b = min(ende, spalt_x) - links
            balken.append(f'<i style="left:{links}px;top:{y}px;width:{b}px"></i>')
        nach = spalt_x + spalt
        if ende > nach:
            balken.append(
                f'<i style="left:{nach}px;top:{y}px;width:{ende - nach}px"></i>')

    # Hinter dem Durchgang wird es hell. Weiss, weil auf Markenflaeche laut
    # DESIGN.md Weiss oder --auf-marke gilt und sonst nichts.
    durchgang = (f'<u style="left:{spalt_x}px;width:{spalt}px"></u>'
                 if offen else "")

    return f"""<meta charset="utf-8">
<style>
  *{{ margin:0; padding:0; }}
  body{{ width:{B}px; height:{H}px; background:{p['marke-dunkel']};
         position:relative; overflow:hidden; }}
  i{{ position:absolute; height:{zh}px; background:{p['auf-marke']};
      display:block; }}
  u{{ position:absolute; top:0; height:{H}px; background:#fff; display:block; }}
</style>
{"".join(balken)}{durchgang}"""


# --------------------------------------------------------------------------

def schiessen(name, html, breite, hoehe, skala):
    (TEMP / f"{name}.html").write_text(html, encoding="utf-8")
    ziel = ZIEL / f"{name}.png"
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
         f"--force-device-scale-factor={skala}",
         f"--window-size={breite},{hoehe}",
         f"--screenshot={ziel}",
         f"http://localhost:{PORT}/bilder/.render/{name}.html"],
        check=True, capture_output=True)
    print(f"    {name}.png  {breite * skala}x{hoehe * skala}  "
          f"{ziel.stat().st_size // 1024} kB")


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome nicht gefunden: {CHROME}")
    p = palette()
    print(f"Palette aus stil.css: --marke {p['marke']}, "
          f"--marke-dunkel {p['marke-dunkel']}, --auf-marke {p['auf-marke']}\n")

    TEMP.mkdir(exist_ok=True)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=WURZEL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(1.2)
        print("  Panel-Folien, 1280x720 unter dem Blauverlauf:")
        schiessen("01-titel-wand", wand_html(p, False), 1280, 720, 2)
        schiessen("15-durchgang", wand_html(p, True), 1280, 720, 2)
        print("\n  Bildspalte, 322x334 in dreifacher Aufloesung:")
        schiessen("04-prozess-luecke", prozess_html(p, False), 322, 334, 3)
        schiessen("03-prozess-voll", prozess_html(p, True), 322, 334, 3)
    finally:
        server.terminate()
        server.wait()
        shutil.rmtree(TEMP, ignore_errors=True)

    print("\nFertig. Beschriftete Stationen, kein Rot, kein Gruen, "
          "kein grauer Grund.")


if __name__ == "__main__":
    main()
