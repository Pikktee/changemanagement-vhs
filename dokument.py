#!/usr/bin/env python3
"""Baut die System-Prompt-Dokumentation als PDF (Abgabe 2).

Liest dokumentation.md, loest die Platzhalter auf, rendert jede Seite als
HTML im A4-Format, schiesst sie mit headless Chrome und fuegt die Bilder mit
PIL zu einem PDF zusammen. Gleiches Verfahren wie build.py fuer die Folien.

Die Abschnitte des System-Prompts und der Iterationshistorie werden nicht
kopiert, sondern zur Bauzeit aus den Quelldateien gezogen. Eine Aenderung am
Prompt schlaegt damit unmittelbar auf die Abgabe durch, und das Dokument kann
gar nicht erst veralten.

    python3 dokument.py            # alles
    python3 dokument.py --schnell  # nur HTML, ohne Chrome
"""

import html
import re
import subprocess
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).resolve().parent
QUELLE = WURZEL / "dokumentation.md"
PROMPT = WURZEL / "system-prompt.md"
ITER = WURZEL / "iterationen.md"
SERVER = WURZEL / "tool" / "server.py"
AUS = WURZEL / "ausgabe-dokument"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 8793

# A4 bei 96 dpi. Der Faktor 2 beim Rendern verdoppelt beides.
BREITE, HOEHE = 794, 1123
SKALA = 2

TITEL = "KLARTEXT · System-Prompt-Dokumentation"


# --------------------------------------------------------------------------
# Quellen einlesen
# --------------------------------------------------------------------------

def abschnitte(pfad, muster):
    """Zerlegt eine Markdown-Datei an ihren ##-Ueberschriften.

    Gibt {schluessel: rumpf} zurueck. Der Schluessel kommt aus der Gruppe 1
    des uebergebenen Musters, angewandt auf den Ueberschriftentext.
    """
    text = pfad.read_text(encoding="utf-8")
    treffer = list(re.finditer(r"^## (.+)$", text, re.M))
    raus = {}
    for i, t in enumerate(treffer):
        ende = treffer[i + 1].start() if i + 1 < len(treffer) else len(text)
        rumpf = text[t.end():ende].strip("\n")
        rumpf = re.sub(r"\n-{3,}\s*$", "", rumpf).strip("\n")
        m = re.match(muster, t.group(1).strip())
        if m:
            raus[m.group(1)] = rumpf
    return raus


def fassung_lesen():
    """Das Feld **Fassung:** aus dem Prompt, damit das Titelblatt nicht driftet.

    Die Nummer stand hier einmal abgetippt und zeigte v9, als der Prompt schon
    bei v11 war.
    """
    m = re.search(r"^\*\*Fassung:\*\*\s*(.+)$", PROMPT.read_text(encoding="utf-8"),
                  re.M)
    if not m:
        sys.exit("Kein Feld **Fassung:** in system-prompt.md")
    return m.group(1).strip()


def kurztexte_lesen():
    """{'v8': 'Stelle = Wort bei NIVEAU, ...'} aus tool/server.py.

    Dieselbe Liste zeigt das Werkzeug im Panel neben jeder Iteration. Sie hier
    zu wiederholen hiesse, zwei Fassungen derselben Angabe zu pflegen.
    """
    m = re.search(r"^ITERATION_KURZTEXTE = \{(.*?)^\}", SERVER.read_text(encoding="utf-8"),
                  re.M | re.S)
    if not m:
        sys.exit("ITERATION_KURZTEXTE nicht in tool/server.py gefunden")
    return dict(re.findall(r'"([^"]+)":\s*"([^"]+)"', m.group(1)))


def iterationen_tabelle():
    """Die Fassungshistorie als Tabelle: Nummer, Datum, Kurztext.

    Reihenfolge und Datum kommen aus den Ueberschriften von iterationen.md,
    der Kurztext aus server.py. Eine neue Fassung erscheint damit beim
    naechsten Bau von selbst.
    """
    kurz = kurztexte_lesen()
    zeilen = ["| Fassung | Datum | Was sich geändert hat |", "|---|---|---|"]
    for t in re.finditer(r"^##\s+(v[\d.]+)\s*·\s*([^·\n]+?)\s*·\s*(.+?)\s*$",
                         ITER.read_text(encoding="utf-8"), re.M):
        nummer, datum, titel = t.groups()
        zeilen.append("| %s | %s | %s |"
                      % (nummer, datum.split(",")[0].strip(),
                         kurz.get(nummer) or titel.replace("`", "")))
    if len(zeilen) < 3:
        sys.exit("Keine Fassungen in iterationen.md gefunden")
    return "\n".join(zeilen)


def teilstueck(rumpf, von=None, bis=None):
    """Schneidet einen Abschnitt an seinen ###-Unterueberschriften zu."""
    if von is None and bis is None:
        return rumpf
    stellen = list(re.finditer(r"^### (.+)$", rumpf, re.M))
    start = 0
    ende = len(rumpf)
    for s in stellen:
        name = s.group(1).strip()
        if von and name.startswith(von):
            start = s.start()
        if bis and name.startswith(bis):
            ende = s.start()
            break
    return rumpf[start:ende].strip("\n")


# --------------------------------------------------------------------------
# Markdown, nur so viel wie gebraucht wird
# --------------------------------------------------------------------------

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    return s


LISTENZEILE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.+)$")


def liste_bauen(eintraege, pos, einzug):
    """Baut aus (Einzug, geordnet, Text) verschachtelte Listen.

    Gibt (HTML, naechste Position) zurueck. Eine Zeile mit groesserem Einzug
    beginnt eine Unterliste, eine mit kleinerem beendet die laufende. Ohne
    diese Unterscheidung liefen die zwei Unterpunkte in AUFGABE als Schritt 3
    und 4 mit, und die fuenf Arbeitsschritte des Prompts wurden zu sieben.
    """
    geordnet = eintraege[pos][1]
    stuecke = []
    while pos < len(eintraege):
        e_einzug, e_geordnet, e_text = eintraege[pos]
        if e_einzug < einzug or (e_einzug == einzug and e_geordnet != geordnet):
            break
        if e_einzug > einzug and stuecke:
            unter, pos = liste_bauen(eintraege, pos, e_einzug)
            stuecke[-1] += unter
            continue
        stuecke.append(inline(e_text))
        pos += 1
    tag = "ol" if geordnet else "ul"
    return ("<%s>%s</%s>"
            % (tag, "".join("<li>%s</li>" % s for s in stuecke), tag), pos)


def md(text):
    """Wandelt den benutzten Markdown-Umfang in HTML."""
    zeilen = text.split("\n")
    raus, i = [], 0
    while i < len(zeilen):
        z = zeilen[i]

        if z.startswith("```"):
            block = []
            i += 1
            while i < len(zeilen) and not zeilen[i].startswith("```"):
                block.append(zeilen[i])
                i += 1
            i += 1
            raus.append("<pre>%s</pre>" % html.escape("\n".join(block)))
            continue

        if re.match(r"^\s*$", z):
            i += 1
            continue

        if re.match(r"^-{3,}\s*$", z):
            raus.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.+)$", z)
        if m:
            stufe = len(m.group(1))
            raus.append("<h%d>%s</h%d>" % (stufe, inline(m.group(2)), stufe))
            i += 1
            continue

        # Tabelle
        if z.lstrip().startswith("|") and i + 1 < len(zeilen) \
                and re.match(r"^\s*\|[\s:|-]+\|\s*$", zeilen[i + 1]):
            kopf = [c.strip() for c in z.strip().strip("|").split("|")]
            i += 2
            reihen = []
            while i < len(zeilen) and zeilen[i].lstrip().startswith("|"):
                reihen.append([c.strip() for c in
                               zeilen[i].strip().strip("|").split("|")])
                i += 1
            t = ["<table><thead><tr>"]
            t += ["<th>%s</th>" % inline(c) for c in kopf]
            t.append("</tr></thead><tbody>")
            for r in reihen:
                t.append("<tr>" + "".join(
                    "<td>%s</td>" % inline(c) for c in r) + "</tr>")
            t.append("</tbody></table>")
            raus.append("".join(t))
            continue

        # Listen
        if LISTENZEILE.match(z):
            eintraege = []
            while i < len(zeilen):
                mm = LISTENZEILE.match(zeilen[i])
                if not mm:
                    # Fortsetzungszeile eines Eintrags. Die Quellen ruecken
                    # mal zwei, mal drei Zeichen ein, je nach Listenart.
                    if eintraege and zeilen[i][:1].isspace() and zeilen[i].strip():
                        eintraege[-1][2] += " " + zeilen[i].strip()
                        i += 1
                        continue
                    break
                eintraege.append([len(mm.group(1)),
                                  bool(re.match(r"^\d+\.$", mm.group(2))),
                                  mm.group(3)])
                i += 1
            raus.append(liste_bauen(eintraege, 0, eintraege[0][0])[0])
            continue

        if z.startswith("> "):
            block = []
            while i < len(zeilen) and zeilen[i].startswith(">"):
                block.append(zeilen[i].lstrip("> ").rstrip())
                i += 1
            raus.append("<blockquote>%s</blockquote>" % inline(" ".join(block)))
            continue

        # Absatz
        block = []
        while i < len(zeilen) and zeilen[i].strip() \
                and not re.match(r"^\s*([-*]|\d+\.)\s|^#|^\||^```|^>", zeilen[i]):
            block.append(zeilen[i].strip())
            i += 1
        if block:
            raus.append("<p>%s</p>" % inline(" ".join(block)))
        else:
            i += 1
    return "\n".join(raus)


# --------------------------------------------------------------------------
# Seiten
# --------------------------------------------------------------------------

def platzhalter_aufloesen(text, prompt_teile, iter_teile):
    """Ersetzt {{PROMPT:X}} und {{ITER:X}}, optional mit Zuschnitt."""
    def prompt(m):
        name = m.group(1)
        von, bis = m.group(2), m.group(3)
        rumpf = prompt_teile.get(name)
        if rumpf is None:
            sys.exit("Unbekannter Prompt-Abschnitt: %s" % name)
        return teilstueck(rumpf, von, bis)

    def iteration(m):
        name = m.group(1)
        rumpf = iter_teile.get(name)
        if rumpf is None:
            sys.exit("Unbekannte Fassung: %s" % name)
        return rumpf

    text = re.sub(r"\{\{PROMPT:([A-ZÄÖÜ]+)(?::([^:}]*))?(?::([^}]*))?\}\}",
                  prompt, text)
    text = re.sub(r"\{\{ITER:([^}]+)\}\}", iteration, text)
    text = re.sub(r"\{\{PROTOKOLL:([\d-]+):(\w+)\}\}", protokoll, text)
    # Zuletzt, damit die eingesetzten Texte nicht selbst noch durchsucht
    # werden: In einem Kurztext steht {{WORTLISTE_A1}} als Wort.
    text = text.replace("{{ITER_TABELLE}}", iterationen_tabelle())
    text = text.replace("{{FASSUNG}}", fassung_lesen())
    return text


def protokoll(m):
    """Holt Ein- oder Ausgabe aus dem juengsten Protokoll eines Kurses.

    Damit stehen im Dokument keine abgetippten Beispiele, sondern die Daten
    des letzten tatsaechlichen Laufs.
    """
    import json
    nummer, teil = m.group(1), m.group(2)
    treffer = sorted((WURZEL / "tool" / "protokoll").glob("*-%s.json" % nummer))
    if not treffer:
        sys.exit("Kein Protokoll fuer Kurs %s" % nummer)
    d = json.loads(treffer[-1].read_text(encoding="utf-8"))
    if teil == "eingabe":
        return d["benutzernachricht"].strip()
    if teil == "antwort":
        return d["antwort"].strip()
    if teil == "kopf":
        return ("Kurs %s · %s · Prompt %s · %s · Temperatur %s · %.0f s"
                % (d["eingabe"]["nummer"], d["eingabe"]["titel"].strip(),
                   d["promptFassung"], d["modell"], d["temperatur"],
                   d["dauerSekunden"]))
    sys.exit("Unbekannter Protokollteil: %s" % teil)


def seiten_lesen():
    roh = QUELLE.read_text(encoding="utf-8")
    prompt_teile = abschnitte(PROMPT, r"^([A-ZÄÖÜ]+)$")
    iter_teile = abschnitte(ITER, r"^(v[\d.]+|Offen)")
    roh = platzhalter_aufloesen(roh, prompt_teile, iter_teile)

    seiten = []
    for stueck in re.split(r"^=== SEITE ===\s*$", roh, flags=re.M):
        stueck = stueck.strip("\n")
        if not stueck.strip():
            continue
        kopf = {}
        m = re.match(r"^((?:[a-z]+:.*\n)+)", stueck)
        if m:
            for zeile in m.group(1).strip().split("\n"):
                k, _, v = zeile.partition(":")
                kopf[k.strip()] = v.strip()
            stueck = stueck[m.end():]
        kopf["inhalt"] = stueck.strip("\n")
        seiten.append(kopf)
    return seiten


def seite_html(s, nr, gesamt):
    if s.get("typ") == "titel":
        koerper = '<div class="titelblatt">%s</div>' % md(s["inhalt"])
        fuss = ""
    else:
        koerper = md(s["inhalt"])
        fuss = ('<footer><span>%s</span><span>%s</span>'
                '<span>%02d / %02d</span></footer>'
                % (html.escape(TITEL), html.escape(s.get("kapitel", "")),
                   nr, gesamt))
    kopf = ""
    if s.get("typ") != "titel":
        kopf = ('<header><span class="marke">KLARTEXT</span>'
                '<span>%s</span></header>' % html.escape(s.get("kapitel", "")))
    klasse = "seite" + (" titel" if s.get("typ") == "titel" else "")
    if s.get("eng") == "ja":
        klasse += " eng"
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<title>{html.escape(TITEL)} — {nr}</title>
<link rel="stylesheet" href="../dokument.css"></head>
<body><div class="{klasse}">{kopf}<main>{koerper}</main>{fuss}</div></body></html>"""


def rendern(anzahl):
    if not Path(CHROME).exists():
        sys.exit("Chrome nicht gefunden: %s" % CHROME)
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=WURZEL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    try:
        for i in range(1, anzahl + 1):
            ziel = AUS / ("seite-%02d.png" % i)
            subprocess.run([
                CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=%d" % SKALA,
                "--window-size=%d,%d" % (BREITE, HOEHE),
                "--screenshot=%s" % ziel,
                "http://localhost:%d/ausgabe-dokument/seite-%02d.html" % (PORT, i),
            ], check=True, capture_output=True)
            print("  Seite %02d gerendert" % i)
    finally:
        server.terminate()


def pdf_bauen(anzahl):
    from PIL import Image
    bilder = []
    for i in range(1, anzahl + 1):
        b = Image.open(AUS / ("seite-%02d.png" % i)).convert("RGB")
        bilder.append(b)
    ziel = AUS / "KLARTEXT-System-Prompt-Dokumentation.pdf"
    bilder[0].save(ziel, save_all=True, append_images=bilder[1:],
                   resolution=96 * SKALA)
    print("  PDF: %s (%d Seiten, %.1f MB)"
          % (ziel.name, anzahl, ziel.stat().st_size / 1e6))


def main():
    schnell = "--schnell" in sys.argv
    AUS.mkdir(exist_ok=True)
    seiten = seiten_lesen()
    for i, s in enumerate(seiten, 1):
        (AUS / ("seite-%02d.html" % i)).write_text(
            seite_html(s, i, len(seiten)), encoding="utf-8")
    print("  %d Seiten aufgebaut" % len(seiten))
    if schnell:
        return
    rendern(len(seiten))
    pdf_bauen(len(seiten))


if __name__ == "__main__":
    main()
