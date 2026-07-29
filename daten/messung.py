#!/usr/bin/env python3
"""
KLARTEXT — Befundquote der 60er-Stichprobe, deterministisch nachgerechnet.

Zwei Zahlen der Abgabe stammen aus dieser Messung: der Anteil der Texte mit
mindestens einem Befund und die Zahl der Kurse für Deutschlernende mit
Niveau-Befunden. Beide waren bisher nur behauptet. Dieses Skript rechnet sie
aus der Stichprobe und dem Referenzwortschatz nach, ohne Modell und ohne Netz.

    python3 daten/messung.py
    python3 daten/messung.py --json

DIESES SKRIPT IST EIN MESSINSTRUMENT UND WIRD EINGEFROREN.

Die Folien nennen als Erfolgskriterium eine Nachmessung „mit demselben Skript
wie die Ausgangsmessung". Eine Nachmessung ist aber nur dann eine Nachmessung,
wenn zwischen den beiden Läufen die Methode unverändert geblieben ist. Wer
später die Satzgrenze verschiebt, die Amtsdeutsch-Liste ergänzt oder die
Wortzerlegung großzügiger macht, misst nicht mehr denselben Gegenstand und
vergleicht zwei Zahlen, die nichts miteinander zu tun haben. Ab hier gilt
deshalb: Fehler dokumentieren, nicht stillschweigend beheben. Wird eine
Änderung unvermeidlich, gehört sie in eine zweite Datei mit eigenem Namen und
eigener Messung, damit beide Stände nebeneinander stehen bleiben.

Gemessen werden nur die fünf Regeln, die ohne Urteil entscheidbar sind:
SATZ, NIVEAU, LINKTEXT, ABK und AMTSDEUTSCH. Die sechste Regel STRUKTUR ist
nicht deterministisch prüfbar — sie verlangt die Entscheidung, ob eine Zeile
als Überschrift gemeint war, und genau diese Entscheidung kann ein Skript nur
raten. Sie wird deshalb nicht gemessen und in der Ausgabe ausdrücklich als
nicht gemessen ausgewiesen. Die hier ermittelte Befundquote ist damit eine
Untergrenze.

Die Regeldefinitionen stehen in `system-prompt.md`, Abschnitt KONTEXT. Wo das
Skript sie enger oder weiter auslegt als der Prompt, steht der Grund im
Kommentar an der betreffenden Stelle; zusammengefasst stehen die Grenzen der
Messung in `messung.md`.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent
STICHPROBE = WURZEL / "vhs-stichprobe-60.json"
WORTLISTE = WURZEL / "wortliste-goethe-a1.txt"

# Satzlängen nach der Regeltabelle des Prompts: 25 Wörter im Normalfall,
# 15 im strengen Fall.
GRENZE_NORMAL = 25
GRENZE_STRENG = 15

REGELN = ["SATZ", "NIVEAU", "LINKTEXT", "ABK", "AMTSDEUTSCH"]
NICHT_GEMESSEN = ["STRUKTUR"]


# --------------------------------------------------------------------------
# Strenger Fall
# --------------------------------------------------------------------------

# Der strenge Fall gilt, wenn der Kurs selbst Deutsch vermittelt: dann liest
# die Zielgruppe den Ankündigungstext in der Sprache, die sie erst lernen
# will. Woran das Skript ihn festmacht, in dieser Reihenfolge:
#
#   1. Kursnummer 40xx oder 41xx. Das ist die Nummernsystematik des Hauses
#      für den Programmbereich Deutsch als Fremdsprache; 42xx bis 45xx sind
#      die übrigen Sprachen. Dieselbe Zuordnung steht in `tool/server.py`,
#      Funktion `bereich_raten`, und wird dort für die Vorbelegung des
#      Formulars verwendet.
#   2. Ersatzweise ein Titelstichwort, falls die Nummer fehlt oder abweicht.
#
# Die Stichprobe führt kein Feld `programmbereich`; die Nummer ist der
# nächstbeste Träger derselben Information. Beide Wege werden geprüft und
# der Weg, über den die Zuordnung zustande kam, wird mitgeführt, damit
# Grenzfälle sichtbar bleiben.
STRENGE_NUMMERN = ("40", "41")
STRENGE_STICHWORTE = (
    "daf",
    "deutsch als fremdsprache",
    "integrationskurs",
    "alphabetisierung",
    "literalisierung",
    "goethe-zertifikat",
)
# „Deutsch“ allein reicht als Stichwort nicht: „Deutsch“ steht auch in
# „Deutsch-Englisch“ oder in Kursen über deutsche Geschichte. Es zählt nur
# in Verbindung mit einer Niveauangabe, siehe `ist_streng`.
NIVEAU_MUSTER = re.compile(r"\b([ABC][12])\b")


def ist_streng(kurs):
    """Vermittelt dieser Kurs Deutsch? Gibt (bool, Begründung) zurück."""
    nummer = (kurs.get("nummer") or "").strip()
    titel = (kurs.get("titel") or "").strip()
    unten = titel.lower()

    if nummer[:2] in STRENGE_NUMMERN:
        return True, "Kursnummer %s (Programmbereich Deutsch als Fremdsprache)" % nummer[:2]
    for wort in STRENGE_STICHWORTE:
        if wort in unten:
            return True, "Titelstichwort „%s“" % wort
    if "deutsch" in unten and NIVEAU_MUSTER.search(titel):
        return True, "Titel nennt Deutsch mit Niveauangabe"
    return False, "kein Hinweis auf einen Deutschkurs"


def niveau_aus_titel(titel):
    treffer = NIVEAU_MUSTER.search(titel or "")
    return treffer.group(1) if treffer else "ohne Angabe"


# --------------------------------------------------------------------------
# HTML
# --------------------------------------------------------------------------

# Die Texte des Portals enthalten nur zwei Auszeichnungen, <a> und <strong>.
# Die Linktexte müssen vor dem Entfernen des Markups herausgelesen werden,
# sonst ist der Befund LINKTEXT nicht mehr prüfbar: sichtbar bleibt nur noch
# das Wort „hier“, nicht aber, dass es ein Link war.
LINK = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.IGNORECASE | re.DOTALL)
ZIEL = re.compile(r"""href\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)""", re.IGNORECASE)
TAG = re.compile(r"<[^>]+>")


def links_lesen(roh):
    """Linktext und Linkziel aus dem Markup, vor dem Entfernen der Tags."""
    gefunden = []
    for treffer in LINK.finditer(roh):
        ziel = ZIEL.search(treffer.group(1))
        gefunden.append({
            "text": html.unescape(TAG.sub("", treffer.group(2))).strip(),
            "ziel": ziel.group(1).strip("\"'") if ziel else "",
        })
    return gefunden


def sichtbar(roh):
    """Nur das, was eine Leserin sieht. Markup raus, Entities aufgelöst."""
    return html.unescape(TAG.sub("", roh or ""))


# --------------------------------------------------------------------------
# Sätze und Wörter
# --------------------------------------------------------------------------

# Punkte, die keinen Satz beenden. Ohne diese Liste zerfällt „z. B.“ in zwei
# Sätze und die gemessene Satzlänge wird systematisch zu klein.
#
# Nicht in dieser Liste stehen „etc.“ und „usw.“: sie stehen fast immer am
# Satzende, ihr Schutz würde zwei Sätze zu einem verschmelzen. Genau daran
# scheiterte der erste Entwurf dieser Messung, siehe messung.md.
SATZSCHUTZ = (
    "z. B.", "z.B.", "u. a.", "u.a.", "d. h.", "d.h.", "u. Ä.", "ggf.",
    "bzw.", "ca.", "inkl.", "evtl.", "vgl.", "max.", "min.",
    "Nr.", "Dr.", "Prof.", "Tel.", "Str.", "Abs.", "Art.", "Mo.", "Di.",
    "Mi.", "Do.", "Fr.", "Sa.", "So.", "Jan.", "Feb.", "Sept.", "Okt.",
    "Nov.", "Dez.",
)
MARKE = "\x00"
ZAHLPUNKT = re.compile(r"(?<=\d)\.")
SATZENDE = re.compile(r"(?<=[.!?])\s+")
AUFZAEHLUNG = re.compile(r"^[\s*•\-–—]+")


def saetze(text):
    """Zerlegt den sichtbaren Text in Sätze.

    Zeilenumbrüche gelten als Satzgrenze. Die Portaltexte setzen Aufzählungen
    und freistehende Überschriften als eigene Zeilen ohne Satzzeichen; würden
    diese Zeilen zusammengezogen, entstünden Riesensätze, die niemand liest.
    Innerhalb einer Zeile wird an Punkt, Ausrufe- und Fragezeichen getrennt,
    Doppelpunkte trennen nicht.
    """
    ergebnis = []
    for zeile in (text or "").splitlines():
        zeile = AUFZAEHLUNG.sub("", zeile).strip()
        if not zeile:
            continue
        ergebnis.extend(_trennen(zeile))
    return ergebnis


def bloecke(text):
    """Dieselbe Trennung, aber ohne die Zeilenumbrüche als Satzgrenze.

    Wird nicht für die Regel SATZ verwendet, sondern nur als Vergleichswert.
    Die zuvor veröffentlichte Zahl „längster Satz 74 Wörter“ entsteht nur so:
    Eine Aufzählung ohne Satzzeichen wird dann als ein einziger Satz gezählt.
    Der Wert steht in der Ausgabe, damit der Unterschied zur neuen Messung
    nachvollziehbar bleibt und nicht als Rechenfehler erscheint.
    """
    zeilen = [AUFZAEHLUNG.sub("", z).strip() for z in (text or "").splitlines()]
    return _trennen(" ".join(z for z in zeilen if z))


def _trennen(zeile):
    geschuetzt = zeile
    for abk in SATZSCHUTZ:
        geschuetzt = geschuetzt.replace(abk, abk.replace(".", MARKE))
    geschuetzt = ZAHLPUNKT.sub(MARKE, geschuetzt)
    ergebnis = []
    for stueck in SATZENDE.split(geschuetzt):
        satz = stueck.replace(MARKE, ".").strip()
        if woerter(satz):
            ergebnis.append(satz)
    return ergebnis


HAT_ZEICHEN = re.compile(r"[0-9A-Za-zÄÖÜäöüß]")


def woerter(satz):
    """Wörter eines Satzes, gezählt wie beim Auszählen von Hand: alles, was
    zwischen Leerzeichen steht und wenigstens einen Buchstaben oder eine
    Ziffer enthält. „z. B.“ zählt danach als zwei Wörter."""
    return [w for w in (satz or "").split() if HAT_ZEICHEN.search(w)]


TOKEN = re.compile(r"[A-Za-zÄÖÜäöüß]+(?:-[A-Za-zÄÖÜäöüß]+)*")


def tokens(text):
    """Wortformen für den Wortschatzabgleich, Bindestrichwörter zusammen."""
    return TOKEN.findall(text or "")


# --------------------------------------------------------------------------
# Referenzwortschatz und die vier Ausnahmen
# --------------------------------------------------------------------------

def wortliste_lesen():
    """Liest die Goethe-A1-Liste in zwei Mengen.

    Einträge auf `-` sind Stämme flektierender Wörter (`all-`, `dies-`) und
    werden gesondert geführt. Mehrwortige Einträge (`zum Beispiel`, `Rad
    fahren`) zählen zusätzlich mit ihren Teilen, weil im Fließtext nur die
    Teile auftauchen.
    """
    if not WORTLISTE.is_file():
        sys.exit("Referenzwortschatz fehlt: %s" % WORTLISTE)
    eintraege, staemme = set(), set()
    for zeile in WORTLISTE.read_text(encoding="utf-8").splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#"):
            continue
        wort = zeile.lower()
        if wort.endswith("-"):
            staemme.add(wort[:-1])
            continue
        eintraege.add(wort)
        if " " in wort:
            eintraege.update(teil for teil in wort.split() if len(teil) > 1)
    return eintraege, staemme


EINTRAEGE, STAEMME = wortliste_lesen()

# Ausnahme 2 des Prompts: Funktionswörter sind nie ein Niveaubefund. Die
# meisten stehen ohnehin auf der A1-Liste; diese Liste fängt die Formen ab,
# die dort fehlen oder sich nicht regelmäßig herleiten lassen.
FUNKTIONSWOERTER = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem",
    "einer", "eines", "kein", "keine", "keinen", "keinem", "keiner", "keines",
    "ich", "du", "er", "sie", "es", "wir", "ihr", "mich", "dich", "sich",
    "uns", "euch", "mir", "dir", "ihm", "ihn", "ihnen", "man", "mein",
    "meine", "meinen", "meinem", "meiner", "meines", "dein", "deine", "sein",
    "seine", "seinen", "seinem", "seiner", "seines", "ihre", "ihren",
    "ihrem", "ihrer", "ihres", "unser", "unsere", "unseren", "unserem",
    "unserer", "unseres", "euer", "eure", "euren", "eurem", "eurer",
    "dieser", "diese", "dieses", "diesen", "diesem", "jene", "jener",
    "welche", "welcher", "welches", "welchen", "welchem", "wer", "wen",
    "wem", "wessen", "was", "wo", "wohin", "woher", "wann", "wie", "warum",
    "weshalb", "wieso", "an", "auf", "aus", "bei", "bis", "durch", "für",
    "gegen", "hinter", "in", "mit", "nach", "neben", "ohne", "über", "um",
    "unter", "vor", "von", "zu", "zum", "zur", "zwischen", "am", "ans",
    "beim", "im", "ins", "vom", "aufs", "übers", "und", "oder", "aber",
    "denn", "sondern", "dass", "weil", "wenn", "als", "ob", "damit",
    "obwohl", "während", "bevor", "nachdem", "sobald", "solange", "falls",
    "sowie", "sowohl", "beziehungsweise", "bin", "bist", "ist", "sind",
    "seid", "war", "waren", "warst", "wart", "gewesen", "sei", "seien",
    "wäre", "wären", "habe", "hast", "hat", "haben", "habt", "hatte",
    "hatten", "hattest", "hattet", "gehabt", "werde", "wirst", "wird",
    "werden", "werdet", "wurde", "wurden", "worden", "würde", "würden",
    "nicht", "auch", "noch", "schon", "nur", "sehr", "so", "dann", "hier",
    "da", "dort", "jetzt", "immer", "nie", "etwa", "etwas", "alle", "allen",
    "aller", "allem", "alles", "andere", "anderen", "anderem", "anderer",
    "anderes", "viele", "vielen", "mehr", "wenig", "wenige", "wenigen",
    "jede", "jeden", "jedem", "jeder", "jedes", "manche", "manchen",
    "einige", "einigen", "einiger", "mehrere", "mehreren",
}

# Zwei Wörter, die der Prompt ausdrücklich als zulässig nennt, die aber auf
# der veröffentlichten Goethe-Liste nicht stehen: `Ausdruck` (im Prompt als
# Grundform von `Ausdrücke` genannt) und `leiten` (im Prompt als Bestandteil
# des erlaubten `Kursleitung` genannt). Ohne diese Ergänzung meldete das
# Skript genau das, was der Prompt ausdrücklich nicht gemeldet haben will.
# Die Ergänzung steht hier sichtbar und nicht in der Wortlistendatei, weil
# die Datei die Quelle wiedergibt und nicht verändert werden soll.
PROMPT_ERGAENZUNG = {"ausdruck", "leiten"}

# Ausnahme 4: Eigennamen. Deterministisch nicht allgemein erkennbar. Erfasst
# werden drei Quellen, die in den Daten selbst stehen oder abzählbar sind:
# die Namen der Kursleitungen aus dem Feld `kursleiter`, die Wörter des
# Kurstitels (Kurs- und Produktbezeichnungen) und diese Liste der Orts-,
# Marken- und Produktnamen, die in der Stichprobe tatsächlich vorkommen.
EIGENNAMEN = {
    "frankfurt", "main", "hessen", "deutschland", "mainz", "fulda",
    "bonifatius", "goldstein", "sonnemannstraße", "bockenheim", "höchst",
    "nied", "sachsenhausen", "gallus", "bornheim", "vhs", "goethe", "telc",
    "zoom", "youtube", "microsoft", "windows", "excel", "word", "powerpoint",
    "outlook", "access", "adobe", "android", "chatgpt", "sql", "pivot",
    "powerpivot", "faq", "libelle", "bras", "port", "terre", "zumba",
    "pilates", "hatha", "yoga", "asana", "asanas", "dancehall", "vamos",
    "hablar", "ripetere", "praticare", "eurotest", "klett", "isbn", "agb",
    "agbs", "email", "mail", "internet", "app", "apps", "web", "online",
    "pdf", "usb", "wlan", "ki", "pc", "eu", "dvd", "cd",
}


def _entumlauten(wort):
    return (wort.replace("äu", "au").replace("ä", "a")
                .replace("ö", "o").replace("ü", "u"))


def _steht_in_liste(wort):
    if wort in EINTRAEGE or wort in PROMPT_ERGAENZUNG:
        return True
    # Stammeinträge wie `all-` decken `alle`, `allen`, `allem` ab, aber nicht
    # beliebig lange Fortsetzungen: höchstens drei Zeichen Endung.
    for stamm in STAEMME:
        if wort.startswith(stamm) and 0 <= len(wort) - len(stamm) <= 3:
            return True
    return False


# Flexionsendungen, längste zuerst. Bewusst knapp gehalten: jede weitere
# Endung lässt mehr Wörter durch und senkt die gemessene Befundzahl.
ENDUNGEN = (
    "innen", "enden", "ender", "endes", "esten", "erem", "eres", "erer",
    "eren", "sten", "ten", "tet", "end", "ens", "est", "ste", "ere", "en",
    "em", "er", "es", "et", "st", "te", "n", "e", "s", "t",
)


def _formen(wort):
    """Alle Grundformen, die aus dieser Wortform regelmäßig entstehen können."""
    kandidaten = {wort}
    for endung in ENDUNGEN:
        if wort.endswith(endung) and len(wort) - len(endung) >= 3:
            stamm = wort[: len(wort) - len(endung)]
            kandidaten.update({stamm, stamm + "e", stamm + "en"})
    if wort.startswith("ge") and len(wort) > 6:
        # Partizip II: `gebraucht`, `gesprochen`
        for endung in ("et", "en", "t"):
            if wort.endswith(endung):
                stamm = wort[2: len(wort) - len(endung)]
                if len(stamm) >= 3:
                    kandidaten.update({stamm, stamm + "en"})
    kandidaten.update(_entumlauten(k) for k in list(kandidaten))
    return kandidaten


def _ist_gebeugt(wort):
    """Ausnahme 1: gebeugte Form eines Listeneintrags."""
    return any(_steht_in_liste(form) for form in _formen(wort))


# Ableitungssuffixe für Ausnahme 3. Der zweite Wert sagt, was an den Stamm
# gehängt werden muss, damit die Grundform entsteht. Bei `-ung` ist das `en`
# und nicht die leere Zeichenkette: `Buchung` kommt von `buchen`, nicht von
# `Buch`. Ohne diese Unterscheidung ginge `Umbuchung` als ableitbar durch,
# obwohl der Prompt sie ausdrücklich als Befund führt.
ABLEITUNGEN = (
    ("ungen", "en"), ("ung", "en"),
    ("igkeit", ""), ("keit", ""), ("heit", ""),
    ("lich", ""), ("isch", ""), ("bar", ""), ("los", ""), ("ig", ""),
    ("innen", ""), ("in", ""), ("chen", ""), ("lein", ""),
)


def _ist_abgeleitet(wort):
    for suffix, anhang in ABLEITUNGEN:
        if not wort.endswith(suffix) or len(wort) - len(suffix) < 3:
            continue
        stamm = wort[: len(wort) - len(suffix)]
        for form in (stamm + anhang, _entumlauten(stamm) + anhang):
            if _steht_in_liste(form):
                return True
    return False


def _bekannt(wort):
    return _steht_in_liste(wort) or _ist_gebeugt(wort) or _ist_abgeleitet(wort)


FUGEN = ("", "s", "n", "es", "en")


def _ist_zusammengesetzt(wort, tiefe=0):
    """Ausnahme 3: Zusammensetzung aus Wörtern, die alle herleitbar sind.

    Der Prompt macht die Ausnahme davon abhängig, ob sich die Bedeutung
    erschließt — eine Entscheidung, die ein Skript nicht treffen kann. Hier
    gilt deshalb der engere, prüfbare Teil der Regel: jeder Bestandteil muss
    selbst auf der Liste stehen oder sich aus ihr herleiten lassen. Das ist
    strenger als der Prompt und wird in `messung.md` als Grenze vermerkt.
    """
    if tiefe > 1:
        return False
    if "-" in wort:
        teile = [t for t in wort.split("-") if t]
        return len(teile) > 1 and all(
            _bekannt(t) or _ist_zusammengesetzt(t, tiefe + 1) for t in teile
        )
    for schnitt in range(3, len(wort) - 2):
        links = wort[:schnitt]
        if not _bekannt(links):
            continue
        for fuge in FUGEN:
            rest = wort[schnitt:]
            if fuge and not rest.startswith(fuge):
                continue
            rechts = rest[len(fuge):]
            if len(rechts) < 3:
                continue
            if _bekannt(rechts) or _ist_zusammengesetzt(rechts, tiefe + 1):
                return True
    return False


# Abkürzungen im Fließtext sind kein Wortschatzproblem, sondern gehören zu
# ABK. Ohne diese Ausnahme stünde „etc.“ einmal als Niveaubefund und einmal
# als Abkürzungsbefund in derselben Liste.
ABKUERZUNGSTOKEN = {"etc", "usw", "bzw", "ggf", "ggfs", "ca", "vgl", "inkl",
                    "evtl", "max", "min", "zzgl", "abs", "art", "nr"}


def niveaubefund(wort, ausnahmen):
    """True, wenn dieses Wort ein Niveaubefund ist.

    `ausnahmen` enthält die Eigennamen dieses Kurses: Kursleitung und
    Kurstitel. Reihenfolge der Prüfung wie im Prompt: erst die vier
    Ausnahmen, dann melden.
    """
    klein = wort.lower()
    if len(klein) < 3:
        return False
    if klein in FUNKTIONSWOERTER:
        return False
    if klein in ABKUERZUNGSTOKEN or wort in ABKUERZUNGEN:
        return False
    if klein in EIGENNAMEN or klein in ausnahmen:
        return False
    if _bekannt(klein):
        return False
    if _ist_zusammengesetzt(klein):
        return False
    return True


# --------------------------------------------------------------------------
# LINKTEXT
# --------------------------------------------------------------------------

# Linktexte, die den Zweck des Links nicht nennen. Die ersten fünf verlangt
# die Aufgabenstellung, die übrigen sind Schreibvarianten derselben Sache.
NICHTSSAGEND = {
    "hier", "mehr", "klicken", "diese seite", "link",
    "hier klicken", "mehr erfahren", "weiterlesen", "weiter", "mehr dazu",
    "hier entlang", "zur seite", "diese webseite", "dieser link", "hier geht es",
}
RAND = re.compile(r"^[\s.,;:!?»«„“”\"'()\[\]]+|[\s.,;:!?»«„“”\"'()\[\]]+$")


def linktext_befund(linktext):
    """Nichtssagender Linktext? Vergleich ohne Rand- und Satzzeichen."""
    norm = RAND.sub("", (linktext or "").lower()).strip()
    norm = re.sub(r"\s+", " ", norm)
    return bool(norm) and norm in NICHTSSAGEND


# --------------------------------------------------------------------------
# ABK
# --------------------------------------------------------------------------

# Die Hausabkürzungen aus dem Prompt, Abschnitt KONTEXT, mit den Zeichenfolgen,
# die als Auflösung im selben Text gelten. Groß- und Kleinschreibung zählt,
# sonst trifft `GER` jedes „ger“ im Fließtext. KI, PC, EU und ISBN gelten
# laut Prompt als bekannt und stehen deshalb nicht hier.
ABKUERZUNGEN = {
    "DaF": ("Deutsch als Fremdsprache",),
    "DTZ": ("Deutsch-Test für Zuwanderer", "Deutsch Test für Zuwanderer"),
    "GER": ("Gemeinsamer Europäischer Referenzrahmen",
            "Gemeinsamen Europäischen Referenzrahmen"),
    "telc": ("The European Language Certificates", "European Language"),
    "Xpert": ("Xpert Business", "Europäischer ComputerPass"),
    "ECDL": ("European Computer Driving Licence",),
    "IVOM": ("Integrationskurs mit Alphabetisierung",),
}
# A1 bis C2 führt der Prompt als eigene Hausabkürzung. Als Auflösung gilt,
# dass der Referenzrahmen im Text genannt wird — die bloße Wiederholung der
# Stufe („Niveaustufe A2“) erklärt sie nicht.
NIVEAUKUERZEL = re.compile(r"\b[ABC][12]\b")
NIVEAU_AUFLOESUNG = ("Referenzrahmen", "GER", "Gemeinsamer Europäischer")


def abk_befunde(text):
    """Abkürzungen, die im Text vorkommen und dort nicht aufgelöst werden."""
    gefunden = []
    for kuerzel, aufloesungen in ABKUERZUNGEN.items():
        if not re.search(r"\b%s\b" % re.escape(kuerzel), text):
            continue
        if any(a in text for a in aufloesungen):
            continue
        gefunden.append(kuerzel)
    treffer = NIVEAUKUERZEL.search(text)
    if treffer and not any(a in text for a in NIVEAU_AUFLOESUNG):
        gefunden.append(treffer.group(0))
    return gefunden


# --------------------------------------------------------------------------
# AMTSDEUTSCH
# --------------------------------------------------------------------------

# Kleine, absichtlich sichtbare Liste. Aufgenommen ist nur, was aus der
# Verwaltungssprache stammt und wofür es ein alltägliches Wort gibt. Nicht
# aufgenommen ist gehobenes Standarddeutsch wie „entscheidend“, „umfassend“
# oder „zudem“ — der Prompt schließt das ausdrücklich aus. Die ersten vier
# Einträge nennt der Prompt selbst als Beispiele.
#
# Diese Liste ist der Teil der Messung mit dem größten Ermessensanteil. Sie
# steht deshalb vollständig hier und wird nicht erweitert.
AMTSWOERTER = (
    "gegebenenfalls", "ggf.", "idealerweise", "Umbuchung", "umbuchen",
    "Selbsteinschätzung", "Fehleinschätzung", "Antragstellung",
    "Inanspruchnahme", "diesbezüglich", "vorbehaltlich", "Kenntnisnahme",
    "Erstattung", "Rückerstattung", "Ermäßigung", "Anrechnung",
    "Voraussetzung hierfür", "im Vorfeld", "in Kenntnis setzen",
    "unbeschadet", "zwecks", "seitens", "hinsichtlich", "sofern",
    "sonstige", "obliegt", "zeitnah", "diesbezügliche",
)


def amtsdeutsch_befunde(text):
    gefunden = []
    unten = text.lower()
    for wendung in AMTSWOERTER:
        if wendung.lower() in unten:
            gefunden.append(wendung)
    return gefunden


# --------------------------------------------------------------------------
# Ein Text
# --------------------------------------------------------------------------

# Die Folie behauptet nicht irgendeinen Niveaubefund, sondern „C1-Vokabular“
# und nennt drei Wörter. Diese drei werden deshalb zusätzlich einzeln
# gezählt, damit die Aussage der Folie an ihrem eigenen Wortlaut prüfbar ist
# und nicht nur an der weiter gefassten Regel NIVEAU.
C1_WOERTER = ("Selbsteinschätzung", "Fehleinschätzung", "Umbuchung")


def maskieren(stelle, kursleiter):
    """Ersetzt die Namensbestandteile der Kursleitung durch `[Name]`."""
    for teil in (kursleiter or "").split():
        if len(teil) > 2:
            stelle = stelle.replace(teil, "[Name]")
    return stelle


def messen(kurs):
    roh = kurs.get("text") or ""
    streng, begruendung = ist_streng(kurs)
    text = sichtbar(roh)
    grenze = GRENZE_STRENG if streng else GRENZE_NORMAL

    # Eigennamen dieses Kurses: Kursleitung und Titel. Die Namen der
    # Kursleitungen werden nur zum Ausschließen gelesen und nirgends
    # ausgegeben — Arbeitsregel des Projekts.
    ausnahmen = set()
    for feld in ("kursleiter", "titel"):
        ausnahmen.update(t.lower() for t in tokens(kurs.get(feld) or ""))

    befunde = []

    alle_saetze = saetze(text)
    laengen = [len(woerter(s)) for s in alle_saetze]
    for satz, laenge in zip(alle_saetze, laengen):
        if laenge > grenze:
            # Der zitierte Satz kann den Namen der Kursleitung enthalten. Die
            # Arbeitsregel des Projekts verlangt `[Name]` in jeder Ausgabe;
            # in der aktuellen Stichprobe greift das nirgends, es hält die
            # Zusage aber auch bei einem Lauf auf anderen Daten ein.
            befunde.append({"regel": "SATZ",
                            "stelle": maskieren(satz[:80], kurs.get("kursleiter")),
                            "wert": laenge})

    if streng:
        # Ein Wort wird je Text einmal gezählt, auch wenn es mehrfach
        # vorkommt. Der Prompt zählt je Fundstelle; für eine Quote über
        # 60 Texte ist die Wortart die stabilere Einheit, und sie zählt
        # niemals zu hoch.
        gesehen = set()
        for wort in tokens(text):
            klein = wort.lower()
            if klein in gesehen:
                continue
            if niveaubefund(wort, ausnahmen):
                gesehen.add(klein)
                befunde.append({"regel": "NIVEAU", "stelle": wort, "wert": None})
    niveauwoerter = {b["stelle"].lower() for b in befunde if b["regel"] == "NIVEAU"}

    for link in links_lesen(roh):
        if linktext_befund(link["text"]):
            befunde.append({"regel": "LINKTEXT", "stelle": link["text"], "wert": None})

    for kuerzel in abk_befunde(text):
        befunde.append({"regel": "ABK", "stelle": kuerzel, "wert": None})

    for wendung in amtsdeutsch_befunde(text):
        # Regel des Prompts: Trifft im strengen Fall NIVEAU und AMTSDEUTSCH
        # auf dasselbe Wort zu, zählt NIVEAU. Sonst stünde „Umbuchung“
        # doppelt in der Liste.
        if streng and wendung.lower() in niveauwoerter:
            continue
        befunde.append({"regel": "AMTSDEUTSCH", "stelle": wendung, "wert": None})

    block_laengen = [len(woerter(s)) for s in bloecke(text)]

    return {
        "nummer": kurs.get("nummer") or "",
        "titel": kurs.get("titel") or "",
        "niveau": niveau_aus_titel(kurs.get("titel")),
        "streng": streng,
        "zuordnung": begruendung,
        "zeichen": len(text),
        "saetze": len(alle_saetze),
        "woerter": sum(laengen),
        "satz_max": max(laengen) if laengen else 0,
        "satz_schnitt": round(sum(laengen) / len(laengen), 1) if laengen else 0.0,
        "block_max": max(block_laengen) if block_laengen else 0,
        "grenze": grenze,
        "c1_wortschatz": [w for w in C1_WOERTER if w.lower() in text.lower()],
        "befunde": befunde,
        "je_regel": {r: sum(1 for b in befunde if b["regel"] == r) for r in REGELN},
    }


# --------------------------------------------------------------------------
# Selbstprüfung
# --------------------------------------------------------------------------

# Der Prompt nennt acht Wörter aus echten vhs-Texten, die zu Recht ein
# Niveaubefund sind, und sechs Formen, die trotz fehlenden Listeneintrags
# keiner sein dürfen. Beides prüft das Skript bei jedem Lauf an sich selbst.
# Schlägt das fehl, ist die Wortzerlegung defekt und alle Niveauzahlen dieses
# Laufs sind wertlos.
SOLL_BEFUND = ("Niveaustufe", "Teilstufen", "umfasst", "äußern",
               "Selbsteinschätzung", "Fehleinschätzung", "Umbuchung",
               "gegebenenfalls")
SOLL_KEIN_BEFUND = ("den", "dem", "einer", "Kursen", "Sätze", "Ausdrücke",
                    "Kursleitung")


def selbstpruefung():
    falsch = []
    for wort in SOLL_BEFUND:
        if not niveaubefund(wort, set()):
            falsch.append("%s müsste ein Befund sein" % wort)
    for wort in SOLL_KEIN_BEFUND:
        if niveaubefund(wort, set()):
            falsch.append("%s dürfte kein Befund sein" % wort)
    return falsch


# --------------------------------------------------------------------------
# Auswertung
# --------------------------------------------------------------------------

def auswerten(kurse):
    ergebnisse = [messen(k) for k in kurse]
    streng = [e for e in ergebnisse if e["streng"]]
    normal = [e for e in ergebnisse if not e["streng"]]

    def quote(menge):
        mit = [e for e in menge if e["befunde"]]
        return {
            "texte": len(menge),
            "mit_befund": len(mit),
            "ohne_befund": len(menge) - len(mit),
            "anteil": round(100 * len(mit) / len(menge), 1) if menge else 0.0,
            "befunde": sum(len(e["befunde"]) for e in menge),
            "je_regel": {r: sum(e["je_regel"][r] for e in menge) for r in REGELN},
            "texte_je_regel": {
                r: sum(1 for e in menge if e["je_regel"][r]) for r in REGELN
            },
        }

    laengster = max(ergebnisse, key=lambda e: e["satz_max"])
    laengster_block = max(ergebnisse, key=lambda e: e["block_max"])
    niveau_kurse = [e for e in streng if e["je_regel"]["NIVEAU"]]
    # Die A1-Liste ist nur für Kurse auf A1 und A2 ein sauberer Maßstab.
    # Darüber gibt der Prompt an das Urteil ab, siehe messung.md.
    a1a2 = [e for e in streng if e["niveau"] in ("A1", "A2")]

    return {
        "quelle": STICHPROBE.name,
        "wortliste": WORTLISTE.name,
        "wortliste_eintraege": len(EINTRAEGE),
        "gemessene_regeln": REGELN,
        "nicht_gemessen": NICHT_GEMESSEN,
        "selbstpruefung": selbstpruefung(),
        "gesamt": quote(ergebnisse),
        "streng": quote(streng),
        "normal": quote(normal),
        "streng_mit_niveau": len(niveau_kurse),
        "streng_gesamt": len(streng),
        "streng_a1a2": len(a1a2),
        "streng_a1a2_mit_niveau": sum(1 for e in a1a2 if e["je_regel"]["NIVEAU"]),
        "streng_mit_c1_wortschatz": sum(1 for e in streng if e["c1_wortschatz"]),
        "c1_woerter": list(C1_WOERTER),
        "laengster_satz": {
            "woerter": laengster["satz_max"],
            "kurs": laengster["nummer"],
            "titel": laengster["titel"],
        },
        "laengster_block": {
            "woerter": laengster_block["block_max"],
            "kurs": laengster_block["nummer"],
        },
        "kurse": ergebnisse,
    }


# --------------------------------------------------------------------------
# Ausgabe
# --------------------------------------------------------------------------

def zeile(text=""):
    print(text)


def bericht(d):
    g = d["gesamt"]
    zeile()
    zeile("KLARTEXT — Befundmessung an %d Kursbeschreibungen" % g["texte"])
    zeile("Quelle %s, Referenzwortschatz %s mit %d Einträgen"
          % (d["quelle"], d["wortliste"], d["wortliste_eintraege"]))
    zeile()

    if d["selbstpruefung"]:
        zeile("  ! Selbstprüfung fehlgeschlagen, die Niveauzahlen sind wertlos:")
        for fehler in d["selbstpruefung"]:
            zeile("    - %s" % fehler)
        zeile()
    else:
        zeile("  Selbstprüfung an den %d Beispielen des Prompts bestanden"
              % (len(SOLL_BEFUND) + len(SOLL_KEIN_BEFUND)))
        zeile()

    zeile("  Befundquote")
    zeile("    Texte insgesamt                %4d" % g["texte"])
    zeile("    davon mit mindestens einem Befund %d  (%.1f Prozent)"
          % (g["mit_befund"], g["anteil"]))
    zeile("    davon ohne Befund              %4d" % g["ohne_befund"])
    zeile("    Befunde insgesamt              %4d" % g["befunde"])
    zeile()

    zeile("  Befunde je Regel")
    zeile("    Regel          Befunde   betroffene Texte")
    for regel in REGELN:
        zeile("    %-12s %6d %12d"
              % (regel, g["je_regel"][regel], g["texte_je_regel"][regel]))
    for regel in NICHT_GEMESSEN:
        zeile("    %-12s %6s %12s" % (regel, "n. g.", "n. g."))
    zeile()
    zeile("  n. g. = nicht gemessen. STRUKTUR verlangt die Entscheidung, ob eine")
    zeile("  Zeile als Überschrift gemeint war. Ein Skript kann das nur raten,")
    zeile("  deshalb bleibt die Regel hier ungeprüft und die Befundquote ist")
    zeile("  eine Untergrenze.")
    zeile()

    for name, schluessel, hinweis in (
        ("Strenger Fall (Kurs vermittelt Deutsch)", "streng", "Satzgrenze 15 Wörter, NIVEAU geprüft"),
        ("Normaler Fall", "normal", "Satzgrenze 25 Wörter, NIVEAU nicht geprüft"),
    ):
        t = d[schluessel]
        zeile("  %s" % name)
        zeile("    %s" % hinweis)
        zeile("    Texte %d, davon mit Befund %d (%.1f Prozent), Befunde %d"
              % (t["texte"], t["mit_befund"], t["anteil"], t["befunde"]))
        zeile("    %s" % ", ".join(
            "%s %d" % (r, t["je_regel"][r]) for r in REGELN if t["je_regel"][r]
        ))
        zeile()

    zeile("  Kurse für Deutschlernende mit mindestens einem Niveau-Befund")
    zeile("    %d von %d" % (d["streng_mit_niveau"], d["streng_gesamt"]))
    zeile("    davon auf Stufe A1 oder A2, wo die A1-Liste der zutreffende")
    zeile("    Maßstab ist: %d von %d"
          % (d["streng_a1a2_mit_niveau"], d["streng_a1a2"]))
    zeile("    Kurse mit den drei Wörtern %s: %d von %d"
          % (", ".join(d["c1_woerter"]), d["streng_mit_c1_wortschatz"],
             d["streng_gesamt"]))
    zeile()

    l = d["laengster_satz"]
    b = d["laengster_block"]
    zeile("  Längster gemessener Satz: %d Wörter, Kurs %s"
          % (l["woerter"], l["kurs"]))
    zeile("  Zum Vergleich, ohne Zeilenumbruch als Satzgrenze: %d Wörter,"
          % b["woerter"])
    zeile("  Kurs %s. Dieser Wert zählt eine Aufzählung als einen Satz und"
          % b["kurs"])
    zeile("  ist nicht der Maßstab der Regel SATZ.")
    zeile()

    zeile("  Die zehn längsten Sätze der Stichprobe")
    for e in sorted(d["kurse"], key=lambda e: -e["satz_max"])[:10]:
        zeile("    %-9s %3d Wörter   Ø %4.1f   %s"
              % (e["nummer"], e["satz_max"], e["satz_schnitt"], e["titel"].strip()[:38]))
    zeile()

    zeile("  Kurse ohne jeden Befund")
    ohne = [e for e in d["kurse"] if not e["befunde"]]
    if not ohne:
        zeile("    keine")
    for e in ohne:
        zeile("    %-9s %s" % (e["nummer"], e["titel"].strip()[:52]))
    zeile()


def main():
    p = argparse.ArgumentParser(description="Befundquote der 60er-Stichprobe")
    p.add_argument("--json", action="store_true",
                   help="maschinenlesbare Ausgabe statt der Zusammenfassung")
    args = p.parse_args()

    if not STICHPROBE.is_file():
        sys.exit("Stichprobe fehlt: %s" % STICHPROBE)
    kurse = json.loads(STICHPROBE.read_text(encoding="utf-8"))

    d = auswerten(kurse)
    if args.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        bericht(d)
    return 0


if __name__ == "__main__":
    sys.exit(main())
