#!/usr/bin/env python3
"""
KLARTEXT — Vortragswerkzeug.

Erzeugt zwei eigenstaendige Seiten fuer den Vortrag:

    ausgabe/notizen.html   Referentennotizen, eine Folie je Bildschirm,
                           entworfen fuer einen zweiten Monitor im Hochformat
    ausgabe/vortrag.html   nur die Folie als Bild, formatfuellend, schwarz

    python3 notizen.py

Beide Seiten sind an keiner Abgabe beteiligt. Sie gehen weder in die
Praesentation noch in die Dokumentation ein und werden von build.py nicht
angefasst. folien.md wird ausschliesslich gelesen.

Bedienung (auf beiden Seiten gleich):
    vor      Pfeil rechts, Pfeil runter, Leertaste, Bild ab
    zurueck  Pfeil links, Pfeil hoch, Bild auf
    Anfang   Pos1        Ende   Ende
    Schrift  + und -  (nur Notizen, in Schritten von 5 Prozent,
                       gemerkt in localStorage)
    Ein Klick blaettert ebenfalls vor.
    Bearbeiten  Taste E oder der Stift rechts in der Fusszeile
                Esc speichert und schliesst, Cmd+S speichert zwischendurch

Bearbeitet wird der rohe Markdown-Text in einem Textfeld, nicht die gesetzte
Anzeige. Was im Feld steht, geht Zeichen fuer Zeichen in die Datei — es gibt
keinen Ruecklese-Schritt, der etwas anders verstehen koennte, als es aussieht.

Erkannt wird: **fett**, *kursiv*, "# " und "### " als Ueberschrift, "- " und
"1. " als Liste, "> " als Zitat, "---" als Trennlinie. Zwei Muster sind
verboten, weil sie folien.md zerlegen wuerden, und werden vor dem Schreiben
abgewiesen (notiz_pruefen):

    "## " am Zeilenanfang   beginnt dort eine neue Folie
    "### NOTIZ"             ist die Marke, die den Notizblock einleitet

Deshalb fehlt die zweite Ueberschriftenebene. Alles andere ist gegen
build.parse() nachgemessen und ueberlebt unveraendert.

Das braucht den mitgelieferten Server:

    python3 notizen.py --server

Er baut die beiden Seiten, liefert sie auf 8795 aus und nimmt unter
POST /notiz die geaenderte Notiz entgegen. Geschrieben wird ausschliesslich
der Notizblock der einen Folie in folien.md; der Rest der Datei bleibt Byte
fuer Byte stehen (siehe notiz_schreiben). Ein Build laeuft dabei NICHT — die
Folienbilder aendern sich durch eine Notiz nicht, und build.py committet
selbst. Wer die PowerPoint mit den neuen Notizen will, baut danach von Hand
oder laesst watch.py nebenher laufen.

Mit "python3 -m http.server" laufen die Seiten weiter, nur ohne Editor: der
Stift bleibt verborgen, und die Taste E meldet den Grund.

Direkt anspringen laesst sich eine Folie mit ?folie=5 in der Adresse. Das
zaehlt nicht als Blaettern, der Hinweis in der Fusszeile bleibt stehen.

Praesentations-Fernbedienungen senden PageUp und PageDown; beide sind
belegt.

WICHTIG — die Kopplung braucht denselben Ursprung:
    Die beiden Seiten reden ueber einen BroadcastChannel miteinander.
    BroadcastChannel verlangt gleiche Herkunft (Protokoll, Host, Port).
    Ueber file:// ist die Herkunft "null", und Chrome laesst den Kanal dort
    nicht zu — die Seiten blaettern dann jede fuer sich. Beide Fenster
    muessen deshalb ueber denselben lokalen Server geoeffnet werden:

        cd abschlussprojekt-vhs && python3 -m http.server 8795
        http://localhost:8795/ausgabe/notizen.html
        http://localhost:8795/ausgabe/vortrag.html

    Der Hinweis steht zusaetzlich sichtbar in der Fusszeile der Notizseite
    und verschwindet, sobald zum ersten Mal geblaettert wird.

Aufbau der Notizseite:
    Kopf   Foliennummer und Folientitel
    Text   die Notiz, Absaetze durch Leerzeilen getrennt; beim Bearbeiten
           liegt an derselben Stelle das Textfeld mit dem Markdown
    Fuss   Hinweis oder Statuszeile, rechts der Stift

Die Notizen stecken als JSON in der Datei selbst, es wird zur Laufzeit
nichts nachgeladen. Nur die Folienbilder der Vortragsseite kommen als
Datei dazu (ausgabe/folie-NN.png), die liegen daneben.

Die Schriftgroesse der Notiz wird im Browser gesucht, nicht hier
geschaetzt: Der Text wird so lange verkleinert, bis er in das Fenster
passt (Halbierungssuche zwischen MIN und MAX). Reicht MIN nicht, darf
diese eine Folie scrollen — abschneiden waere der schlimmere Fehler.

Gemessen bei 1080x1920: alle 15 Folien passen ohne Scrollen, die Groessen
liegen zwischen 22px (Folie 5, 612 Woerter) und 57px (Folie 15), der Rest
zum unteren Rand zwischen 2 und 121 Pixeln. Am knappsten ist Folie 12 mit
2 Pixeln — wer dort einen Satz ergaenzt, schickt die ganze Notiz eine
Groessenstufe hinunter.

Das Textfeld des Editors uebernimmt die gefundene Groesse (--gr haengt an
.seite und wird von beiden geerbt), damit der Text beim Umschalten nicht
springt. Es rollt dabei oefter als die Anzeige: derselbe Inhalt braucht als
Markdown mehr Zeilen als gesetzt.
"""

import contextlib
import html
import http.server
import importlib.util
import io
import json
import os
import re
import sys
import textwrap
import threading
from pathlib import Path

WURZEL = Path(__file__).parent
QUELLE = WURZEL / "folien.md"
AUS = WURZEL / "ausgabe"

PORT = 8795

# Zeilenbreite beim Zurueckschreiben. folien.md ist von Hand auf diese Breite
# umbrochen (gemessen: Median 73, Maximum 78). Der Umbruch ist nicht nur
# Kosmetik — notiz_setzen() in build.py macht aus jeder Quellzeile einen
# eigenen Absatz der PowerPoint-Notiz. Wer hier eine Notiz als eine einzige
# 2000-Zeichen-Zeile ablegt, bekommt sie in der Referentenansicht als einen
# Block ohne Umbruch zurueck.
UMBRUCH = 78


def lade_build():
    """parse() aus build.py holen, statt den Parser ein zweites Mal zu
    schreiben. Sonst driften die beiden Leser auseinander."""
    spec = importlib.util.spec_from_file_location("klartext_build", WURZEL / "build.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


# --------------------------------------------------------------------------
# Notiztext aufbereiten
# --------------------------------------------------------------------------

# Zeilen, die als eigener Block gelten und niemals mit der Nachbarzeile
# verschmolzen werden. Alles andere ist Fliesstext, dessen harte Umbrueche
# aus folien.md stammen und aufgeloest gehoeren.
#
# Gegen den Bestand geprueft: keine der 391 Notizzeilen faellt heute
# faelschlich darunter. Die 16 Zeilen, die mit einem Stern beginnen, sind
# **fett** — ohne Leerzeichen nach dem Stern und damit kein Listenpunkt.
MARKER = re.compile(r"^(#{1,6} |[-*+] |\d+\. |> |-{3,}$|\*{3,}$)")

# Was folien.md zerlegen wuerde. Nur diese beiden Muster sind gefaehrlich —
# gegen build.parse() nachgemessen, siehe die Meldungen in notiz_pruefen:
#   "## " am Zeilenanfang beginnt dort eine neue Folie
#   "### NOTIZ" / "### NOTIZEN" setzt die Notizmarke ein zweites Mal
# "# ", "### Beliebig", "#### ", Listen, Zitate und Trennlinien sind harmlos.
FOLIENMARKE = re.compile(r"^## ")
NOTIZMARKE = ("### NOTIZ", "### NOTIZEN")


def zeilen_gruppen(notiz):
    """Notiz in Gruppen zerlegen: (art, text, quellzeilen).

    art ist "text" fuer einen Fliessabsatz — dessen harte Umbrueche werden
    zusammengezogen, der Browser bricht selbst um —, "marker" fuer eine
    Ueberschrift, einen Listenpunkt, ein Zitat oder eine Trennlinie, die je
    fuer sich stehen bleibt, und "leer" fuer eine Absatzgrenze.

    quellzeilen sind die Zeilen, aus denen die Gruppe kam. notiz_zeilen()
    braucht sie, um beim Zurueckschreiben einen unveraenderten Absatz mit
    seinem originalen Umbruch wiederherzustellen.

    (build.py macht das anders herum: dort wird jede Quellzeile ein eigener
    Absatz der PowerPoint-Notiz. Fuer die ist das richtig, hier nicht.)
    """
    gruppen, puffer = [], []

    def spuele():
        if puffer:
            gruppen.append(("text", " ".join(z.strip() for z in puffer), list(puffer)))
            puffer.clear()

    for roh in notiz.split("\n"):
        z = roh.strip()
        if not z:
            spuele()
            gruppen.append(("leer", "", []))
        elif MARKER.match(z):
            spuele()
            gruppen.append(("marker", z, [roh.rstrip()]))
        else:
            puffer.append(roh)
    spuele()

    while gruppen and gruppen[-1][0] == "leer":
        gruppen.pop()
    while gruppen and gruppen[0][0] == "leer":
        gruppen.pop(0)
    return gruppen


def roh_text(notiz):
    """Die Notiz fuer das Textfeld des Editors.

    Wie in der Datei, nur ohne die harten Umbrueche im Fliesstext: die sind
    ein Artefakt der Quelle, und beim Speichern setzt notiz_zeilen() sie neu.
    Ueberschriften und Listenpunkte bleiben Zeile fuer Zeile stehen.
    """
    aus = []
    for art, text, _ in zeilen_gruppen(notiz):
        if art == "leer":
            if aus and aus[-1] != "":
                aus.append("")
        else:
            aus.append(text)
    return "\n".join(aus)


def inline(text):
    """HTML-escapen, **fett**, *kursiv* und ((nebenbei)) uebersetzen.

    Auf Folie 10 stehen die Stakeholder-Namen fett am Zeilenanfang; ohne die
    Auszeichnung verliert die Notiz dort ihre Gliederung.

    Kursiv ist eng gefasst: kein Leerzeichen hinter dem oeffnenden und keines
    vor dem schliessenden Stern, und kein Wortzeichen aussen herum. Ein
    einzelner Stern im Text soll nicht stillschweigend verschwinden — das war
    der Grund, aus dem kursiv hier lange gar nicht uebersetzt wurde.

    ((...)) ist die Nebenbemerkung: kleiner und leicht gedaempft, fuer Saetze,
    die nur bei genug Zeit vorgelesen werden. Doppelte Klammern, weil einfache
    im Vortragstext vorkommen. Ein einzelnes Paar bleibt deshalb unangetastet,
    und ein unvollstaendiges (( steht sichtbar da, statt zu verschwinden.
    HTML geht nicht: html.escape() laeuft zuerst, ein <small> im Notiztext
    erscheint woertlich auf der Seite.
    """
    s = html.escape(text)
    s = re.sub(r"\(\((.+?)\)\)", r'<span class="neben">\1</span>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    return s


def anzeige(notiz):
    """Die Notiz als HTML fuer den Kasten."""
    aus, liste = [], None

    def liste_zu():
        nonlocal liste
        if liste:
            aus.append("</%s>" % liste)
            liste = None

    for art, text, _ in zeilen_gruppen(notiz):
        if art == "leer":
            liste_zu()
            continue
        if art == "text":
            liste_zu()
            aus.append("<p>%s</p>" % inline(text))
            continue

        # Marker
        if re.match(r"^(-{3,}|\*{3,})$", text):
            liste_zu()
            aus.append("<hr>")
        elif text.startswith("#"):
            liste_zu()
            raute, rest = re.match(r"^(#{1,6}) (.*)$", text).groups()
            # "## " kann in der Datei nicht vorkommen, die Ebene fehlt also.
            # h2 fuer eine Raute, h3 fuer drei, h4 fuer alles darunter — der
            # Folientitel der Seite ist das h1.
            stufe = {1: 2, 3: 3}.get(len(raute), 4)
            aus.append("<h%d>%s</h%d>" % (stufe, inline(rest), stufe))
        elif text.startswith(">"):
            liste_zu()
            aus.append("<blockquote>%s</blockquote>" % inline(text[1:].strip()))
        else:
            art_liste = "ol" if re.match(r"^\d+\. ", text) else "ul"
            if liste != art_liste:
                liste_zu()
                aus.append("<%s>" % art_liste)
                liste = art_liste
            rest = re.sub(r"^([-*+] |\d+\. )", "", text)
            aus.append("<li>%s</li>" % inline(rest))

    liste_zu()
    return "".join(aus)


def folientitel(f):
    """Titel und Akzent zu einer Zeile verbinden. In folien.md ist der Titel
    zweiteilig ('Was zaehlt als Befund,' + 'und fuer wen.')."""
    teile = [str(f.get("titel", "")).strip(), str(f.get("akzent", "")).strip()]
    return " ".join(t for t in teile if t)


def daten(folien):
    """Die Liste, die in beide Seiten eingebettet wird.

    'html' ist die fertige Anzeige, 'roh' derselbe Inhalt als Markdown fuer
    das Textfeld des Editors. Der harte Umbruch aus folien.md steckt bewusst
    nicht im rohen Text — er ist ein Artefakt der Quelldatei, und beim
    Speichern setzt notiz_zeilen() ihn neu.
    """
    liste = []
    for nr, f in enumerate(folien, 1):
        notiz = f.get("notiz", "")
        liste.append({
            "nr": nr,
            "titel": folientitel(f),
            "bild": f"folie-{nr:02d}.png",
            "html": anzeige(notiz),
            "roh": roh_text(notiz),
        })
    return liste


# --------------------------------------------------------------------------
# Notiz zurueck in folien.md
# --------------------------------------------------------------------------
#
# Warum nicht ueber parse() und einen Serialisierer:
#
# parse() aus build.py ist verlustbehaftet. Es wirft den Kopfkommentar der
# Datei weg, die Merkzettel hinter "## 3 — ", die Leerzeilen und die
# optionalen Anfuehrungszeichen um Listenwerte. Wer die Datei aus dem Ergebnis
# neu schreibt, verliert all das bei der ersten Notizaenderung.
#
# Hier wird deshalb nur der Zeilenbereich EINER Notiz ersetzt. Alles andere —
# auch die Notizen der uebrigen 14 Folien — bleibt unberuehrt, und genau das
# wird vor dem Schreiben nachgerechnet.


def notiz_bereich(zeilen, nr):
    """(start, ende, letzte) des Notiztextes von Folie nr, 1-basiert.

    start ist die erste Zeile nach '### NOTIZ', ende die erste Zeile, die
    nicht mehr dazugehoert (die naechste '## '-Zeile oder das Dateiende).
    """
    marken = [i for i, z in enumerate(zeilen) if z.startswith("## ")]
    if not marken:
        raise ValueError("folien.md enthaelt keine Folie.")
    if not 1 <= nr <= len(marken):
        raise ValueError(f"Folie {nr} gibt es nicht, die Datei hat {len(marken)}.")

    von = marken[nr - 1]
    letzte = nr == len(marken)
    bis = len(zeilen) if letzte else marken[nr]

    for i in range(von, bis):
        if zeilen[i].strip().upper() in ("### NOTIZ", "### NOTIZEN"):
            return i + 1, bis, letzte
    raise ValueError(f"Folie {nr} hat keinen '### NOTIZ'-Block.")


def notiz_zeilen(text, alt=""):
    """Notiztext in Quellzeilen fuer folien.md umbrechen.

    Fliessabsaetze werden auf UMBRUCH Zeichen gebrochen. Ueberschriften,
    Listenpunkte, Zitate und Trennlinien bleiben je eine Zeile, auch wenn sie
    laenger werden — ein Umbruch mittendrin machte aus der Fortsetzung beim
    naechsten Lesen einen eigenen Fliessabsatz.

    Absaetze, die im alten Stand wortgleich vorkamen, behalten dessen
    Zeilenumbruch. Das ist der Kern: folien.md ist von Hand umbrochen und
    weicht an vielen Stellen von der gierigen Aufteilung durch textwrap ab.
    Ohne diese Schonung faerbt das Speichern einer einzigen geaenderten Stelle
    den kompletten Notizblock im Diff ein — bei einer Abgabe, deren Historie
    Teil der Arbeit ist, waere das teuer.

    break_on_hyphens=False, weil textwrap sonst an jedem Bindestrich trennen
    darf und aus 'KI-gestuetzt' zwei Zeilen macht. break_long_words=False
    haelt lange URLs zusammen — die eine 84 Zeichen lange Zeile im Bestand ist
    genau so eine.
    """
    bestand = {t_: q for art, t_, q in zeilen_gruppen(alt) if art == "text"}

    aus = []
    for art, t_, _ in zeilen_gruppen(text):
        if art == "leer":
            if aus and aus[-1] != "":
                aus.append("")
        elif art == "marker":
            aus.append(t_)
        elif t_ in bestand:
            aus.extend(bestand[t_])
        else:
            aus.extend(textwrap.fill(t_, width=UMBRUCH,
                                     break_long_words=False,
                                     break_on_hyphens=False).splitlines())
    while aus and aus[-1] == "":
        aus.pop()
    return aus


def notiz_pruefen(text):
    """Wirft ValueError, wenn der Text folien.md zerlegen wuerde.

    Es sind genau zwei Muster, gegen build.parse() nachgemessen. Alles andere
    an Markdown — "# ", "### Beliebig", "#### ", Listen, Zitate,
    Trennlinien — ueberlebt den Parser unveraendert und ist erlaubt.
    """
    if not text.strip():
        raise ValueError("Leere Notiz wird nicht geschrieben.")

    for nr, z in enumerate(text.splitlines(), 1):
        if FOLIENMARKE.match(z):
            raise ValueError(
                f"Zeile {nr} beginnt mit „## “. Das beginnt in folien.md eine "
                f"neue Folie. Für eine Überschrift „# “ oder „### “ nehmen.")
        if z.strip().upper() in NOTIZMARKE:
            raise ValueError(
                f"Zeile {nr} ist „{z.strip()}“. Das ist in folien.md die "
                f"Marke, die den Notizblock einleitet, und kann nicht im "
                f"Notiztext stehen.")


def notiz_schreiben(nr, text, build):
    """Notiz der Folie nr ersetzen. Gibt die neue Darstellung zurueck.

    Wirft ValueError, wenn etwas nicht stimmt — dann bleibt die Datei
    unangetastet. Geschrieben wird ueber eine Nebendatei und os.replace, damit
    ein Abbruch mitten im Schreiben keine halbe folien.md hinterlaesst.
    """
    notiz_pruefen(text)

    alt_text = QUELLE.read_text(encoding="utf-8")
    alt = build.parse(alt_text)

    # split statt splitlines: der Abschluss der Datei soll beim join
    # unveraendert zurueckkommen.
    zeilen = alt_text.split("\n")
    start, ende, letzte = notiz_bereich(zeilen, nr)

    # Leerzeile nach '### NOTIZ', dann der Text. Danach die zwei Leerzeilen,
    # die im Bestand vor jeder '## '-Zeile stehen. Bei der letzten Folie endet
    # die Datei stattdessen mit genau einem Zeilenumbruch.
    ersatz = ([""] + notiz_zeilen(text, alt[nr - 1].get("notiz", ""))
              + ([""] if letzte else ["", ""]))
    neu_text = "\n".join(zeilen[:start] + ersatz + zeilen[ende:])

    # Gegenprobe: Die Datei muss weiter lesbar sein, gleich viele Folien
    # haben, und ausser der einen Notiz darf sich nichts geaendert haben.
    neu = build.parse(neu_text)
    if len(neu) != len(alt):
        raise ValueError(
            f"Der Schnitt haette die Folienzahl von {len(alt)} auf "
            f"{len(neu)} geaendert.")
    for i, (a, b) in enumerate(zip(alt, neu), 1):
        abweichung = [k for k in set(a) | set(b)
                      if k != "_zeile" and a.get(k) != b.get(k)]
        if i == nr:
            # Leer ist erlaubt: Speichern ohne Aenderung ist kein Fehler.
            if abweichung not in ([], ["notiz"]):
                raise ValueError(
                    f"Folie {nr}: unerwartet geaendert: {sorted(abweichung)}")
        elif abweichung:
            raise ValueError(
                f"Der Schnitt haette Folie {i} mitgeaendert: {sorted(abweichung)}")

    tmp = QUELLE.with_name(QUELLE.name + ".neu")
    tmp.write_text(neu_text, encoding="utf-8")
    os.replace(tmp, QUELLE)

    # So zurueckgeben, wie es beim naechsten Start aus der Datei gelesen
    # wuerde — nicht so, wie es hereinkam. Was die Seite danach zeigt, ist
    # damit garantiert der Inhalt von folien.md.
    fertig = neu[nr - 1]["notiz"]
    return {"html": anzeige(fertig), "roh": roh_text(fertig)}


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------

# Warum dunkelblaue Flaeche und weisse Schrift:
#
# Die Notizseite steht im abgedunkelten Raum unmittelbar neben dem Beamer.
# Eine weisse Flaeche von 1080x1920 leuchtet dort den Referenten an und
# stoert im Blickfeld des Publikums. Eine dunkle Flaeche ist die
# naheliegende Wahl.
#
# DESIGN.md kennt genau eine dunkle Flaeche: --marke. Ein eigenes Grau oder
# Schwarz waere ein neuer Farbwert und damit ein Regelbruch ("Keine neuen
# Grautoene"). Auf --marke gilt: "Auf Markenflaeche gilt Weiss oder
# --auf-marke, sonst nichts." Also Weiss fuer den Text (8,84:1, AAA) und
# --auf-marke fuer die Nebenrollen — Foliennummer, Rahmen des Textfelds,
# Stift (6,32:1). Das ist AAA fuer grossen Text (ab 24px); die Foliennummer
# ist deshalb nach unten auf 26px begrenzt und wird von der automatischen
# Verkleinerung des Textkoerpers nicht erfasst. Der Stift ist ein Symbol und
# faellt unter die 3:1-Grenze fuer grafische Elemente, die er deutlich haelt.
#
# Keine Signalfarbe. Rot und Gruen sind im System mit Bedeutung belegt und
# haben auf einer Notizseite nichts zu suchen.
#
# Die Farbwerte stehen hier ein zweites Mal, weil die Seite ohne stil.css
# auskommen muss: stil.css legt html,body hart auf 1280x720 fest und wuerde
# die Notizseite zerlegen. Diese Datei ist an keiner Abgabe beteiligt;
# pruefe-design.py liest sie deshalb nicht. Wer die Palette aendert, aendert
# sie in stil.css und traegt sie hier von Hand nach.

FARBEN = """
:root{
  --marke:#14459E;
  --auf-marke:#B9DFFA;
  --papier:#FFFFFF;
  --schrift:"Atkinson Hyperlegible Next","Helvetica Neue",Arial,sans-serif;
}
"""

CSS_NOTIZEN = FARBEN + """
*{ box-sizing:border-box; margin:0; padding:0; }

html,body{ height:100%; }

body{
  font-family:var(--schrift);
  background:var(--marke);
  color:var(--papier);
  -webkit-font-smoothing:antialiased;
  overflow:hidden;
}

/* Drei Zeilen: Kopf, Text (nimmt den Rest), Fuss. Der Textbereich ist der
   einzige, der wachsen und schrumpfen darf — min-height:0 ist noetig,
   sonst laesst Grid ihn ueber das Fenster hinauswachsen und die Messung
   im Skript findet nie einen Ueberlauf. */
.seite{
  height:100%;
  display:grid;
  grid-template-rows:auto minmax(0,1fr) auto;
  padding:3.2vmin 3.6vmin 2.4vmin;
  gap:2.2vmin;
}

/* Alle vier ausdruecklich platzieren. Anzeige und Textfeld teilen sich die
   mittlere Zelle — sichtbar ist immer nur eines von beiden. Ohne die
   ausdrueckliche Zuweisung schoebe das automatische Platzieren die Fusszeile
   in eine vierte Zeile, sobald das Textfeld dazukommt. */
.seite > header{ grid-row:1; }
#notiz, #quelle{ grid-row:2; grid-column:1; }
.seite > .fuss{ grid-row:3; }

/* ---------- Kopf ---------- */
.kopf{ display:flex; align-items:baseline; gap:.55em; }

.nr{
  font-size:clamp(26px, 3.4vmin, 46px);
  font-weight:700;
  color:var(--auf-marke);
  font-variant-numeric:tabular-nums;
  flex:none;
}

h1{
  font-size:clamp(26px, 3.4vmin, 46px);
  font-weight:700;
  line-height:1.15;
  letter-spacing:-0.01em;
}

/* ---------- Notiz ---------- */
/* --gr wird von der Halbierungssuche gesetzt. overflow bleibt hidden,
   solange der Text passt; erst wenn selbst die Untergrenze nicht reicht,
   schaltet das Skript .rollt und damit Scrollen frei. */
#notiz{
  font-size:var(--gr, 30px);
  line-height:1.42;
  overflow:hidden;
  /* Keine Silbentrennung. Sie spart Platz, aber dieser Text wird unter Druck
     vorgelesen — ein am Zeilenende zerschnittenes Wort muss das Auge erst
     wieder zusammensetzen. Der rechte Rand wird dafuer unruhiger, das ist
     der guenstigere Tausch. */
  -webkit-hyphens:none; hyphens:none;
}
#notiz.rollt{ overflow-y:auto; }
#notiz p + p{ margin-top:.62em; }
#notiz strong{ font-weight:700; }
#notiz em{ font-style:italic; }

/* Markdown in der Notiz. Alle Masse in em, damit die Halbierungssuche mit
   einer einzigen Schriftgroesse den ganzen Block skaliert — ein fester
   px-Wert an einer Ueberschrift liesse sie beim Verkleinern stehen und die
   Suche faende nie eine passende Groesse.

   Die Ueberschriften stehen in --auf-marke. Das haelt auf --marke 6,32:1 und
   ist damit AAA fuer grossen Text; klein werden sie nicht, sie sind stets
   groesser als der Fliesstext. */
#notiz h2, #notiz h3, #notiz h4{
  color:var(--auf-marke);
  font-weight:700;
  line-height:1.2;
  margin:1.1em 0 .35em;
}
#notiz > :first-child{ margin-top:0; }
#notiz h2{ font-size:1.5em; }
#notiz h3{ font-size:1.25em; }
#notiz h4{ font-size:1.08em; }

#notiz ul, #notiz ol{ margin:.5em 0 .5em 1.4em; }
#notiz li{ margin-top:.3em; }
#notiz li::marker{ color:var(--auf-marke); }

/* Zitat: was wortwoertlich vorgelesen wird. Der Balken links zeigt beim
   Ueberfliegen sofort, wo der eigene Text aufhoert. */
#notiz blockquote{
  margin:.7em 0;
  padding-left:.8em;
  border-left:.2em solid var(--auf-marke);
}

#notiz hr{
  border:none;
  border-top:1px solid var(--auf-marke);
  margin:1em 0;
}

/* Nebenbemerkung: was nur bei genug Zeit vorgelesen wird.

   Gedaempft wird ueber die Deckkraft, nicht ueber eine zweite Textfarbe — die
   Palette kennt auf --marke nur Weiss und --auf-marke, und ein eigenes Grau
   waere ein neuer Farbwert. Weiss auf --marke haelt 8,84:1, bei 75 Prozent
   mischt sich #C4D0E7 und haelt 5,69:1.

   Das ist AA und nicht mehr AAA — die Schwelle fuer kleinen Text liegt bei
   7:1 und waere erst ab 90 Prozent gehalten. Bewusst in Kauf genommen: Diese
   Seite geht in keine Abgabe ein, pruefe-design.py liest sie nicht, und der
   Text soll sich beim Ueberfliegen deutlich vom Vorlesetext abheben. Wer die
   Werte anhebt, holt sich AAA zurueck und verliert die Wirkung; unter 62
   Prozent faellt auch AA. */
#notiz .neben{
  font-size:.78em;
  opacity:.75;
}

/* ---------- Bearbeiten ---------- */
/* Ein Textfeld mit dem rohen Markdown, kein contenteditable. Es liegt an
   derselben Stelle wie die Anzeige und ersetzt sie, solange bearbeitet wird.
   Die Anzeige bleibt dabei im Baum stehen (display:none), damit die
   Halbierungssuche beim Schliessen wieder gegen denselben Kasten misst.

   Warum Textfeld statt WYSIWYG: contenteditable liefert HTML zurueck, und
   dieses HTML muss jemand nach Markdown ruecklesen — mit geschachtelten <b>,
   eingefuegten <span style>, Absaetzen, die mal <p> und mal <div> sind. Was
   im Textfeld steht, geht dagegen unveraendert in die Datei. */
#quelle{
  display:none;
  width:100%; height:100%;
  box-sizing:border-box;
  padding:.7em .8em;
  border:none;
  outline:2px solid var(--auf-marke);
  outline-offset:6px;
  border-radius:2px;
  background:rgba(0,0,0,.22);        /* etwas tiefer als die Flaeche, damit
                                        das Feld als Feld lesbar ist */
  color:var(--papier);
  caret-color:var(--papier);
  font-family:var(--schrift);
  /* Dieselbe Groesse und Zeilenhoehe wie die Anzeige: --gr haengt an .seite
     und wird von beiden geerbt. Beim Umschalten springt der Text so nicht in
     der Groesse — man bearbeitet den Text, den man eben gelesen hat.
     Die Markdown-Marker machen den Text laenger als die Anzeige; passt er
     dann nicht mehr, rollt das Feld. */
  font-size:var(--gr, 30px);
  line-height:1.42;
  resize:none;
  -webkit-hyphens:none; hyphens:none;
}
.bearbeitet #quelle{ display:block; }
.bearbeitet #notiz{ display:none; }

/* ---------- Stift ---------- */
/* Sitzt rechts in der Fusszeile und bleibt stehen, auch wenn der Hinweistext
   nach dem ersten Blaettern verschwindet. Erscheint nur, wenn der Server
   schreiben kann — sonst waere er eine Falle. */
.fuss{ display:flex; align-items:center; gap:1em; }
.fusstext{ flex:1; min-width:0; }
.fusstext[hidden]{ display:block; visibility:hidden; }

.stift{
  flex:none;
  display:flex; align-items:center; justify-content:center;
  width:2.4em; height:2.4em;
  padding:0; border:none; border-radius:50%;
  background:transparent;
  color:var(--auf-marke);
  cursor:pointer;
}
.stift svg{ width:1.5em; height:1.5em; display:block; }
.stift:hover{ background:rgba(255,255,255,.14); color:var(--papier); }
/* Der Fokusrahmen muss sichtbar bleiben: die Seite laesst sich vollstaendig
   mit der Tastatur bedienen, und das ist bei diesem Projekt keine Nebensache. */
.stift:focus-visible{ outline:2px solid var(--papier); outline-offset:2px; }
.stift[hidden]{ display:none; }

/* ---------- Fuss ---------- */
/* Der Hinweis auf den Server steht nur, bis zum ersten Mal geblaettert
   wurde. Danach ist die Seite leer bis zum Rand. */
/* Weiss, nicht --auf-marke: die Zeile ist klein, und --auf-marke haelt auf
   --marke 6,32:1 — AAA fuer grossen Text, nicht fuer kleinen. */
.fuss{
  font-size:clamp(15px, 1.5vmin, 21px);
  color:var(--papier);
  min-height:1.4em;
}

/* Querformat: derselbe Aufbau, nur schmalere Raender. Zerbrechen kann
   nichts, weil die Groesse ohnehin gemessen und nicht gesetzt wird. */
@media (orientation:landscape){
  .seite{ padding:2.6vmin 3vmin 2vmin; gap:1.8vmin; }
}
"""

CSS_VORTRAG = """
*{ box-sizing:border-box; margin:0; padding:0; }
html,body{ height:100%; background:#000; overflow:hidden; }
img{
  width:100%; height:100%;
  object-fit:contain;           /* nie verzerren, lieber Rand lassen */
  display:block;
}
"""


# --------------------------------------------------------------------------
# JavaScript
# --------------------------------------------------------------------------

# Gemeinsamer Teil: Kanal, Tastatur, Adresszeile.
JS_GEMEINSAM = """
const KANAL = 'klartext-vortrag';
const kanal = (() => { try { return new BroadcastChannel(KANAL); }
                       catch (e) { return null; } })();

let folie = 0;                 // 0-basiert
let geblaettert = false;

// Solange die Notiz bearbeitet wird, darf nichts blaettern: Leertaste und
// Pfeile sind dann Schreibtasten, und ein Folienwechsel wuerde den Text im
// Kasten stillschweigend gegen den der naechsten Folie tauschen.
// imEditor() steht nur auf der Notizseite; vortrag.html kennt es nicht.
function editorAktiv(){
  return typeof imEditor === 'function' && imEditor();
}

function ausAdresse(){
  const m = /[?&#]folie=(\\d+)/.exec(location.search + location.hash);
  if (m) return Math.min(FOLIEN.length, Math.max(1, parseInt(m[1], 10))) - 1;
  return 0;
}

// senden=false, wenn der Sprung selbst aus dem Kanal kam. Sonst schickt die
// Gegenseite ihn zurueck und beide springen im Kreis.
function gehe(i, senden){
  folie = Math.min(FOLIEN.length - 1, Math.max(0, i));
  zeige(folie);
  if (senden !== false && kanal) kanal.postMessage({folie: folie});
}

// Blaettern von Hand. Nur das laesst den Hinweis in der Fusszeile
// verschwinden — der erste Aufbau der Seite (auch mit ?folie=N) nicht.
function blaettern(i){
  geblaettert = true;
  gehe(i);
}

if (kanal) kanal.onmessage = e => {
  if (editorAktiv()) return;
  if (e.data && typeof e.data.folie === 'number') {
    geblaettert = true;
    gehe(e.data.folie, false);
  }
};

const VOR    = ['ArrowRight','ArrowDown',' ','Spacebar','PageDown'];
const ZURUCK = ['ArrowLeft','ArrowUp','PageUp','Backspace'];

// Vollbild auf Taste F. Der Browser verlangt dafuer eine Nutzeraktion, ein
// Tastendruck ist eine. F11 des Browsers tut dasselbe, ist aber auf jedem
// System anders belegt.
function vollbild(){
  const d = document;
  if (d.fullscreenElement) { d.exitFullscreen && d.exitFullscreen(); }
  else { d.documentElement.requestFullscreen && d.documentElement.requestFullscreen(); }
}

document.addEventListener('keydown', ev => {
  // Im Editor gehoert die Tastatur dem Text. Escape, Cmd+S und Cmd+B fasst
  // der eigene Handler der Notizseite ab, bevor dieser hier laeuft.
  if (editorAktiv()) return;
  const k = ev.key;
  if (VOR.includes(k))          { blaettern(folie + 1); }
  else if (ZURUCK.includes(k))  { blaettern(folie - 1); }
  else if (k === 'Home')        { blaettern(0); }
  else if (k === 'End')         { blaettern(FOLIEN.length - 1); }
  else if (typeof groesser === 'function' &&
           (k === '+' || k === '=' || k === 'Add'))      { groesser(+1); }
  else if (typeof groesser === 'function' &&
           (k === '-' || k === '_' || k === 'Subtract')) { groesser(-1); }
  else if (k === 'f' || k === 'F')  { vollbild(); }
  else if (typeof editorOeffnen === 'function' &&
           (k === 'e' || k === 'E')) { editorOeffnen(); }
  else return;
  ev.preventDefault();
});

// Maus- und Fingerbedienung: ein Klick blaettert vor. Praktisch, wenn die
// Fernbedienung streikt. Nicht in einem Bereich, den man rollen kann —
// dort will man scrollen und nicht weiterblaettern.
document.addEventListener('click', ev => {
  if (editorAktiv()) return;
  if (ev.target.closest && ev.target.closest('.rollt')) return;
  blaettern(folie + 1);
});
"""

JS_NOTIZEN = """
// Untergrenze der Halbierungssuche, in px. Auf dem Zielgeraet (1080x1920)
// kommt keine Folie ihr nahe — die laengste Notiz, Folie 5 mit 612 Woertern,
// passt bei 21px. Die Grenze greift erst in kleinen Fenstern; dort rollt die
// Folie dann lieber, statt unleserlich zu werden.
const MIN = 18;
const MAX = 64;          // Obergrenze
const SPEICHER = 'klartext-notizen-nachstellung';

// Nachstellung des Referenten, in Prozent. + und - verschieben sie, der
// Wert ueberlebt einen Neustart des Browsers.
let nachstellung = 100;
try { nachstellung = parseInt(localStorage.getItem(SPEICHER), 10) || 100; }
catch (e) {}

const eSeite  = document.querySelector('.seite');
const eNr     = document.getElementById('nr');
const eTitel  = document.getElementById('titel');
const eNotiz  = document.getElementById('notiz');
const eQuelle = document.getElementById('quelle');
const eFuss   = document.getElementById('fusstext');
const eStift  = document.getElementById('stift');

let letzteGroesse = 0;   // fuer die Messseite

// Groesste Schriftgroesse suchen, bei der der Text noch in den Kasten
// passt. Halbierungssuche in ganzen Pixeln: rund sieben Durchlaeufe, das
// merkt niemand. Gemessen wird scrollHeight gegen clientHeight — genau der
// Wert, der auch entscheidet, ob abgeschnitten wuerde.
// --gr sitzt auf .seite, nicht auf #notiz: Anzeige und Textfeld erben
// dieselbe Groesse, damit der Text beim Umschalten nicht springt.
function passtBei(px){
  eSeite.style.setProperty('--gr', px + 'px');
  return eNotiz.scrollHeight <= eNotiz.clientHeight;
}

function sucheGroesse(){
  if (passtBei(MAX)) return MAX;
  let lo = MIN, hi = MAX, best = 0;
  while (lo <= hi) {
    const mitte = (lo + hi) >> 1;
    if (passtBei(mitte)) { best = mitte; lo = mitte + 1; }
    else { hi = mitte - 1; }
  }
  return best || MIN;      // 0 heisst: passt selbst bei MIN nicht
}

function einpassen(){
  // Beim Bearbeiten bleibt die Groesse stehen, die beim Oeffnen gefunden
  // wurde. Sonst springt der ganze Text bei jedem getippten Wort um eine
  // Stufe, sobald er die Kastenhoehe kreuzt.
  if (editorAktiv()) return;
  eNotiz.classList.remove('rollt');
  const basis = sucheGroesse();

  // Die Nachstellung wirkt auf das gefundene Mass. Ohne sie fuellt der Text
  // den Kasten genau aus, und + und - haetten fast nie eine Wirkung — die
  // Groesse haengt ja am Platz, nicht am Geschmack. Stellt der Referent
  // groesser, als es passt, rollt die Folie. Das ist gewollt: lieber rollen
  // als abschneiden, denn ein abgeschnittener Satz faellt auf der Buehne
  // nicht auf.
  const px = Math.min(128, Math.max(10, Math.round(basis * nachstellung / 100)));
  if (!passtBei(px)) eNotiz.classList.add('rollt');
  letzteGroesse = px;
}

function zeige(i){
  const f = FOLIEN[i];
  eNr.textContent = String(f.nr).padStart(2, '0');
  eTitel.textContent = f.titel;
  eNotiz.innerHTML = f.html;
  eNotiz.scrollTop = 0;
  fussSetzen();
  einpassen();
  document.title = 'Notizen ' + String(f.nr).padStart(2, '0');
}

function groesser(richtung){
  nachstellung = Math.min(200, Math.max(50, nachstellung + richtung * 5));
  try { localStorage.setItem(SPEICHER, String(nachstellung)); } catch (e) {}
  einpassen();
}

// Nach einer Groessenaenderung erst messen, wenn der Umbruch steht.
//
// einpassen() sucht die Groesse ueber eine Halbierungssuche und misst dabei
// mehrfach die Hoehe des Textes. Wer ein Fenster am Rand zieht, loest
// Dutzende resize-Ereignisse aus; ohne Zusammenfassung liefe die Suche
// jedes Mal komplett durch. Ein Takt Verzoegerung plus Bildrahmen fasst sie
// zusammen und stellt zugleich sicher, dass gegen den neuen und nicht gegen
// den alten Kasten gemessen wird.
let nachlauf = 0;
function einpassenSpaeter(){
  clearTimeout(nachlauf);
  nachlauf = setTimeout(() => requestAnimationFrame(einpassen), 60);
}
addEventListener('resize', einpassenSpaeter);
// Beim Wechsel ins Vollbild aendert sich die Fensterhoehe; das Ereignis kommt
// je nach Browser vor oder nach dem Neuaufbau. Der Beobachter greift in
// beiden Faellen, auch wenn resize einmal ausbleibt.
addEventListener('fullscreenchange', einpassenSpaeter);
if (window.ResizeObserver) new ResizeObserver(einpassenSpaeter).observe(document.documentElement);
document.fonts.ready.then(einpassen);

// Haken fuer die Ueberlaufmessung. Die Messseite laedt diese Datei in einen
// iframe, springt jede Folie an und liest hier ab.
// Unterkante des Textes im Kasten. scrollHeight taugt dafuer nicht: er ist
// nie kleiner als clientHeight und meldet deshalb immer 0 Rest.
function unterkante(){
  const oben = eNotiz.getBoundingClientRect().top;
  let tief = 0;
  for (const p of eNotiz.children) {
    const u = p.getBoundingClientRect().bottom - oben + eNotiz.scrollTop;
    if (u > tief) tief = u;
  }
  return Math.round(tief);
}

window.klartext = {
  gehe: i => gehe(i, false),
  anzahl: () => FOLIEN.length,
  messung: () => ({
    folie: folie + 1,
    groesse: letzteGroesse,
    inhalt: unterkante(),
    kasten: eNotiz.clientHeight,
    rest: eNotiz.clientHeight - unterkante(),
    rollt: eNotiz.classList.contains('rollt'),
    fett: eNotiz.querySelectorAll('strong').length,
    absaetze: eNotiz.querySelectorAll('p').length
  })
};
"""

JS_VORTRAG = """
const eBild = document.getElementById('bild');

function zeige(i){
  const f = FOLIEN[i];
  eBild.src = f.bild;
  eBild.alt = 'Folie ' + f.nr + ': ' + f.titel;
  document.title = 'Folie ' + String(f.nr).padStart(2, '0');
}

// Alle Folienbilder einmal vorladen, damit beim Blaettern kein schwarzer
// Zwischenzustand entsteht.
FOLIEN.forEach(f => { const v = new Image(); v.src = f.bild; });

window.klartext = { gehe: i => gehe(i, false), anzahl: () => FOLIEN.length };
"""

# Der erste Aufbau steht bewusst am Ende und nicht in den Bausteinen darueber:
# zeige() ruft fussSetzen() und einpassen(), und die greifen auf die mit let
# angelegten Zustaende des Editors zu. Liefe der Aufruf vor JS_EDIT, waeren
# die noch in ihrer temporalen Totzone.
JS_START = """
gehe(ausAdresse(), false);
"""

# Roher String: der Umwandler enthaelt Regulaerausdruecke und \\n als Zeichen
# im JavaScript. In einem gewoehnlichen Python-String wuerde daraus schon beim
# Erzeugen der Datei ein echter Zeilenumbruch.
JS_EDIT = """
// ---------- Notiz bearbeiten ----------
//
// Bearbeitet wird der rohe Markdown-Text in einem Textfeld, nicht die
// gesetzte Anzeige. Das ist die kuerzere und die ehrlichere Loesung: Was im
// Feld steht, geht Zeichen fuer Zeichen in folien.md — es gibt keinen
// Ruecklese-Schritt, der etwas anders verstehen koennte, als es aussieht.
// **fett** tippt man selbst, ohne Tastengriff und ohne execCommand.
//
// Geschrieben wird ueber POST /notiz, dafuer braucht es einen Server, der das
// annimmt. python3 -m http.server kann es nicht; ob dieser es kann, wird
// einmal beim Aufbau gefragt.

let bearbeitet = false;   // Editiermodus an
let schmutzig  = false;   // ungespeicherte Aenderung im Feld
let schreibbar = false;   // Server nimmt POST /notiz an
let meldung    = '';      // Statuszeile, verdraengt den Fusstext
let meldeUhr   = 0;

const FUSS_RUHE = eFuss.textContent;

function imEditor(){ return bearbeitet; }

function fussSetzen(){
  if (meldung) { eFuss.textContent = meldung; eFuss.hidden = false; return; }
  if (bearbeitet) {
    eFuss.textContent = schmutzig
      ? 'Bearbeiten — noch nicht gespeichert. Markdown: **fett**, *kursiv*, ### Überschrift, - Liste, > Zitat. \\u2318S speichert, Esc speichert und schließt.'
      : 'Bearbeiten — gespeichert. Markdown: **fett**, *kursiv*, ### Überschrift, - Liste, > Zitat. Esc schließt.';
    eFuss.hidden = false;
    return;
  }
  eFuss.textContent = FUSS_RUHE;
  eFuss.hidden = geblaettert;
}

function melde(text, dauer){
  clearTimeout(meldeUhr);
  meldung = text || '';
  fussSetzen();
  if (meldung && dauer) {
    meldeUhr = setTimeout(() => { meldung = ''; fussSetzen(); }, dauer);
  }
}

// ---------- Oeffnen, speichern, schliessen ----------

function editorOeffnen(){
  if (bearbeitet) return;
  if (!schreibbar) {
    melde('Bearbeiten braucht den schreibenden Server: python3 notizen.py --server', 8000);
    return;
  }
  bearbeitet = true;
  schmutzig = false;
  eQuelle.value = FOLIEN[folie].roh;
  eSeite.classList.add('bearbeitet');
  eQuelle.focus();
  eQuelle.setSelectionRange(0, 0);
  eQuelle.scrollTop = 0;
  melde('');
}

async function speichern(){
  const text = eQuelle.value;
  if (!text.trim()) { melde('Die Notiz ist leer — nicht gespeichert.', 8000); return false; }
  melde('Speichere …');
  let d;
  try {
    const a = await fetch('/notiz', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({nr: FOLIEN[folie].nr, text: text})
    });
    d = await a.json();
  } catch (e) {
    melde('Server nicht erreichbar. Es wurde nichts gespeichert.', 10000);
    return false;
  }
  if (!d.ok) { melde('Nicht gespeichert: ' + d.fehler, 10000); return false; }
  // Der Server antwortet mit dem, was beim naechsten Start aus der Datei
  // gelesen wuerde. Das Feld uebernimmt es — steht dort etwas anderes als
  // getippt, sieht man es sofort statt erst nach einem Neustart.
  FOLIEN[folie].html = d.html;
  FOLIEN[folie].roh  = d.roh;
  const p = eQuelle.selectionStart;
  eQuelle.value = d.roh;
  eQuelle.setSelectionRange(Math.min(p, d.roh.length), Math.min(p, d.roh.length));
  schmutzig = false;
  melde('In folien.md gespeichert.', 4000);
  return true;
}

async function editorSchliessen(){
  if (!bearbeitet) return;
  if (schmutzig && !(await speichern())) return;   // Fehler: offen lassen
  bearbeitet = false;
  eSeite.classList.remove('bearbeitet');
  const f = FOLIEN[folie];
  eNotiz.innerHTML = f.html;
  eNotiz.scrollTop = 0;
  einpassen();
  fussSetzen();
}

// ---------- Bedienung ----------

// Laeuft nach dem Handler in JS_GEMEINSAM, der bei offenem Editor sofort
// aussteigt. Diese beiden Griffe sind die einzigen, die dann noch gelten;
// alles uebrige gehoert dem Textfeld.
document.addEventListener('keydown', ev => {
  if (!bearbeitet) return;
  const cmd = ev.metaKey || ev.ctrlKey;
  if (ev.key === 'Escape') { ev.preventDefault(); editorSchliessen(); }
  else if (cmd && (ev.key === 's' || ev.key === 'S')) { ev.preventDefault(); speichern(); }
});

eQuelle.addEventListener('input', () => {
  if (!bearbeitet || schmutzig) return;
  schmutzig = true;
  fussSetzen();
});

// stopPropagation, sonst blaettert der Klick auf den Stift die Seite weiter —
// der Handler in JS_GEMEINSAM sieht jeden Klick auf dem Dokument.
eStift.addEventListener('click', ev => {
  ev.stopPropagation();
  if (bearbeitet) editorSchliessen(); else editorOeffnen();
});

addEventListener('beforeunload', ev => {
  if (!schmutzig) return;
  ev.preventDefault();
  ev.returnValue = '';
});

// Einmal fragen, ob der Server schreiben kann. Bei python3 -m http.server
// gibt es /notiz nicht; dann bleibt der Stift verborgen und die Taste E
// meldet den Grund beim Druecken.
fetch('/notiz')
  .then(a => a.ok ? a.json() : null)
  .then(d => { schreibbar = !!(d && d.schreibbar); eStift.hidden = !schreibbar; })
  .catch(() => {});
"""


# --------------------------------------------------------------------------
# Seiten zusammensetzen
# --------------------------------------------------------------------------

# Das ist der einzige Text, der auf dem Bildschirm erscheint und deshalb in
# vollstaendiger Rechtschreibung stehen muss.
HINWEIS_ANZEIGE = ("Kopplung nur über den lokalen Server: Beide Fenster unter "
                   "„http://localhost/…“ öffnen, nicht als Datei. Weiter mit "
                   "Pfeiltaste, Leertaste oder Bild ab.")

# Stift, gezeichnet statt getippt. Ein Unicode-Bleistift (U+270F) faellt je
# nach System in eine Emoji-Schrift und kommt dann bunt und in fremder Groesse
# — das SVG sieht ueberall gleich aus und erbt die Textfarbe.
STIFT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" '
         'aria-hidden="true">'
         '<path d="M4 20h4L19.5 8.5a2.1 2.1 0 0 0-3-3L5 17v3z"/>'
         '<path d="M14.5 6.5l3 3"/></svg>')


def seite(titel, css, js, koerper, liste):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titel}</title>
<link rel="stylesheet" href="../schriften/schriften.css">
<style>{css}</style>
</head>
<body>
{koerper}
<script>
const FOLIEN = {json.dumps(liste, ensure_ascii=False)};
</script>
<script>{JS_GEMEINSAM}</script>
<script>{js}{JS_START}</script>
</body>
</html>
"""


def baue():
    build = lade_build()
    folien = build.parse(QUELLE.read_text(encoding="utf-8"))
    liste = daten(folien)

    koerper_notizen = f"""<div class="seite">
  <header>
    <div class="kopf"><span class="nr" id="nr"></span><h1 id="titel"></h1></div>
  </header>
  <div id="notiz"></div>
  <textarea id="quelle" spellcheck="true" aria-label="Notiz als Markdown"></textarea>
  <p class="fuss">
    <span class="fusstext" id="fusstext">{html.escape(HINWEIS_ANZEIGE)}</span>
    <button type="button" class="stift" id="stift" hidden
            title="Notiz bearbeiten (Taste E)" aria-label="Notiz bearbeiten">{STIFT}</button>
  </p>
</div>"""

    (AUS / "notizen.html").write_text(
        seite("KLARTEXT — Referentennotizen", CSS_NOTIZEN, JS_NOTIZEN + JS_EDIT,
              koerper_notizen, liste), encoding="utf-8")

    (AUS / "vortrag.html").write_text(
        seite("KLARTEXT — Folien", CSS_VORTRAG, JS_VORTRAG,
              '<img id="bild" src="" alt="">', liste), encoding="utf-8")

    laengste = max(liste, key=lambda f: len(f["roh"]))
    print(f"notizen.py: {len(liste)} Folien geschrieben")
    print(f"  ausgabe/notizen.html   laengste Notiz: Folie {laengste['nr']}, "
          f"{len(laengste['roh'].split())} Woerter")
    print("  ausgabe/vortrag.html")
    return build


# --------------------------------------------------------------------------
# Server
# --------------------------------------------------------------------------
#
# Reicht python3 -m http.server nicht? Zum Blaettern schon. Aber der Editor
# schreibt zurueck, und dafuer braucht es jemanden, der POST annimmt.
#
# Gebunden wird auf 127.0.0.1, nicht auf 0.0.0.0. Der Server nimmt Schreib-
# zugriffe entgegen; im WLAN eines Schulungsraums hat er nichts zu suchen.

# Ausgeliefert wird der ganze Projektordner, damit ../schriften und
# ../stil.css erreichbar sind. Diese Namen liegen darin und gehen niemanden
# etwas an — .env enthaelt den API-Schluessel.
VERBOTEN = (".env", ".git", ".railwayignore", ".gitignore", ".DS_Store")

# Die beiden erzeugten Seiten. bediene() ruft baue() beim Start, danach nie
# wieder — do_GET faellt fuer alles ausser /notiz auf den Dateiserver zurueck.
# Ein Reload holte deshalb die HTML-Datei so, wie sie beim Start geschrieben
# wurde, auch wenn der Editor folien.md seither zwanzigmal geaendert hatte.
# Die offene Seite merkte davon nichts: Sie bekommt ihre neue Fassung aus der
# POST-Antwort. Erst der naechste Reload fiel auf den alten Stand zurueck —
# und das sah aus wie verlorene Arbeit, obwohl in folien.md alles stand.
SEITEN = ("/ausgabe/notizen.html", "/ausgabe/vortrag.html")

_bau_sperre = threading.Lock()


def seiten_nachziehen():
    """baue() nachholen, wenn folien.md juenger ist als die erzeugten Seiten.

    Der mtime-Vergleich ist nicht Sparsamkeit um ihrer selbst willen:
    lade_build() liest build.py bei jedem Aufruf neu ein, und beim Blaettern
    laedt der Browser die Seite nicht neu — aber ein versehentliches Reload
    beim Vortrag soll auch nicht spuerbar haengen.

    Faellt der Bau aus, wird die alte Seite ausgeliefert statt gar keiner.
    Das ist der bessere Fehler: Wer vortraegt, braucht etwas auf dem Schirm.
    """
    ziel = AUS / "notizen.html"

    def aktuell():
        try:
            return ziel.exists() and ziel.stat().st_mtime >= QUELLE.stat().st_mtime
        except OSError:
            return True          # Quelle weg: nichts anfassen

    if aktuell():
        return
    with _bau_sperre:
        if aktuell():            # ein anderer Thread war schneller
            return
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                baue()
        except Exception as f:
            print(f"  ! Seiten nicht neu gebaut: {f}")


class Bediener(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(WURZEL), **k)

    # ---------- Hilfen ----------

    def antworte(self, code, nutzlast):
        roh = json.dumps(nutzlast, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(roh)))
        self.end_headers()
        self.wfile.write(roh)

    def gesperrt(self):
        teile = self.path.split("?")[0].split("/")
        return any(t in VERBOTEN for t in teile)

    def end_headers(self):
        # Eine Stelle, alle Antworten. Ohne das liefert der Browser nach einem
        # neuen Lauf von notizen.py weiter die alte notizen.html aus dem Cache
        # — derselbe Fallstrick, den CLAUDE.md fuer die Pruefseite beschreibt.
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *a):
        pass          # das Blaettern soll die Konsole nicht zumuellen

    # ---------- Anfragen ----------

    def do_GET(self):
        if self.gesperrt():
            return self.antworte(403, {"ok": False, "fehler": "gesperrt"})
        pfad = self.path.split("?")[0]
        if pfad == "/notiz":
            return self.antworte(200, {"schreibbar": True})
        if pfad in SEITEN:
            seiten_nachziehen()
        return super().do_GET()

    def do_HEAD(self):
        if self.gesperrt():
            return self.antworte(403, {"ok": False, "fehler": "gesperrt"})
        # Auch hier, sonst meldet HEAD die Laenge der veralteten Datei.
        if self.path.split("?")[0] in SEITEN:
            seiten_nachziehen()
        return super().do_HEAD()

    def do_POST(self):
        if self.path.split("?")[0] != "/notiz":
            return self.antworte(404, {"ok": False, "fehler": "unbekannter Weg"})
        try:
            laenge = int(self.headers.get("Content-Length") or 0)
            if laenge <= 0 or laenge > 200_000:
                raise ValueError("unglaubwuerdige Laenge")
            daten_ = json.loads(self.rfile.read(laenge).decode("utf-8"))
            nr = int(daten_["nr"])
            text = str(daten_["text"])
        except Exception as ex:
            return self.antworte(400, {"ok": False, "fehler": f"Anfrage: {ex}"})

        try:
            # notiz_schreiben liest, rechnet nach und schreibt. Zwei Anfragen
            # gleichzeitig wuerden gegen denselben alten Stand rechnen und die
            # erste Aenderung stillschweigend ueberschreiben.
            with self.server.schloss:
                neu = notiz_schreiben(nr, text, self.server.build)
        except Exception as ex:
            # Bewusst breit: was hier auch schiefgeht, folien.md ist dann
            # unveraendert, und der Grund gehoert auf den Bildschirm des
            # Referenten statt in ein Serverprotokoll, das niemand liest.
            print(f"  ! Folie {nr} nicht gespeichert: {ex}")
            return self.antworte(400, {"ok": False, "fehler": str(ex)})

        # Erst antworten, dann protokollieren. Andersherum kann ein Fehler in
        # der Meldung die Antwort verhindern, obwohl die Datei laengst
        # geschrieben ist — der Browser meldet dann "Server nicht erreichbar"
        # zu einer Aenderung, die in Wahrheit drin steht. Genau das ist beim
        # Bauen passiert, als hier noch ein Feldname der alten Fassung stand.
        self.antworte(200, {"ok": True, **neu})
        print(f"  Folie {nr:02d}: Notiz gespeichert "
              f"({len(neu['roh'].split())} Wörter)")


def bediene():
    build = baue()
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Bediener)
    server.build = build
    server.schloss = threading.Lock()
    print(f"\n  Server auf http://localhost:{PORT}  (Strg+C beendet ihn)")
    print(f"    http://localhost:{PORT}/ausgabe/notizen.html   Taste E bearbeitet")
    print(f"    http://localhost:{PORT}/ausgabe/vortrag.html")
    print("\n  Gespeicherte Notizen gehen sofort nach folien.md. Die PowerPoint")
    print("  entsteht davon nicht neu — dafuer danach python3 build.py.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBeendet.")
    finally:
        server.server_close()


if __name__ == "__main__":
    if "--server" in sys.argv:
        bediene()
    else:
        baue()
        print("  Beide ueber den lokalen Server oeffnen, sonst koppeln sie nicht:")
        print(f"    cd abschlussprojekt-vhs && python3 -m http.server {PORT}")
        print(f"    http://localhost:{PORT}/ausgabe/notizen.html")
        print(f"    http://localhost:{PORT}/ausgabe/vortrag.html")
        print("  Zum Bearbeiten der Notizen: python3 notizen.py --server")
