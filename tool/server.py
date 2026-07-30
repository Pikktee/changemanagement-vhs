#!/usr/bin/env python3
"""Lokaler Server fuer KLARTEXT, den Redaktionsassistenten der VHS Frankfurt.

Liest den OpenRouter-Key aus einer .env-Datei (dieser Ordner, der Ordner
darueber oder der Ordner darueber) und reicht die Pruefanfragen der Web-App
als Proxy an OpenRouter weiter. Der Key wird nie an den Browser ausgeliefert,
nie protokolliert und nie in eine Datei geschrieben.

Start:  python3 server.py          ->  http://localhost:8799
        python3 server.py --open   ->  oeffnet zusaetzlich den Browser
"""

import base64
import hashlib
import hmac
import json
import os
import re
import sys
import threading
import time
import webbrowser
import urllib.request
import urllib.error
from datetime import datetime
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Lokal 8799 wie gehabt. Auf einer Hosting-Plattform gibt die Umgebung den Port
# vor; dann muss der Server ausserdem auf allen Adressen lauschen statt nur auf
# 127.0.0.1, sonst erreicht ihn der vorgelagerte Proxy nicht.
PORT = int(os.environ.get("PORT", "8799"))
HOST = os.environ.get("KLARTEXT_HOST", "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

BASE_DIR = Path(__file__).resolve().parent
PROJEKT_DIR = BASE_DIR.parent
PROMPT_DATEI = PROJEKT_DIR / "system-prompt.md"
WORTLISTE_DATEI = PROJEKT_DIR / "daten" / "wortliste-goethe-a1.txt"
# Der vollstaendige Kursplan, erzeugt von daten/kursplan-holen.py. Fehlt er,
# faellt der Server auf die alte Stichprobe zurueck, damit das Tool auch ohne
# Abruf lauffaehig bleibt.
KURSE_DATEI = PROJEKT_DIR / "daten" / "vhs-kursplan.json"
KURSE_ERSATZ = PROJEKT_DIR / "daten" / "vhs-stichprobe-60.json"
# Beim Hosting liegt hier der Pfad eines dauerhaften Datentraegers. Das
# Dateisystem eines Containers ueberlebt den naechsten Start sonst nicht, und
# die Protokolle sind der Beleg der Abgabe: dokumentation.md zieht sie ueber
# {{PROTOKOLL:...}} zur Bauzeit heraus.
PROTOKOLL_DIR = Path(os.environ.get("KLARTEXT_PROTOKOLL_DIR") or (BASE_DIR / "protokoll"))
INDEX_DATEI = BASE_DIR / "index.html"
# Die Schriften liegen ausserhalb von tool/, weil Folien und Dokument sie
# ebenso brauchen. Sie werden mitgeliefert statt vom Google-CDN geladen: das
# haelt das Tool offline lauffaehig und uebermittelt keine Besucher-IP an
# Dritte, was fuer einen staedtischen Eigenbetrieb der springende Punkt ist.
SCHRIFTEN_DIR = PROJEKT_DIR / "schriften"

# Erstwahl, danach der Ersatz. Welches Modell geantwortet hat, steht im
# Protokoll und im Panel der Oberflaeche. Die Erstwahl ist die Fassung, mit der
# alle Belege der Abgabe entstanden sind; sie bleibt der Standard, auch wenn im
# Panel andere Modelle waehlbar sind.
MODELL_STANDARD = "anthropic/claude-sonnet-4.5"
MODELL_ERSATZ = "anthropic/claude-sonnet-4"

# Waehlbar im Panel. Weiter reicht die Liste bewusst nicht: Was der Browser
# schickt, geht sonst ungeprueft als Modellname an OpenRouter.
MODELLE_WAHL = [
    {"id": "anthropic/claude-sonnet-4.5", "name": "Claude Sonnet 4.5", "hinweis": "Standard der Abgabe"},
    {"id": "anthropic/claude-sonnet-5", "name": "Claude Sonnet 5", "hinweis": ""},
    {"id": "anthropic/claude-opus-5", "name": "Claude Opus 5", "hinweis": ""},
    {"id": "anthropic/claude-haiku-4.5", "name": "Claude Haiku 4.5", "hinweis": "schnell, günstig"},
    {"id": "openai/gpt-5.1", "name": "GPT-5.1", "hinweis": ""},
    {"id": "google/gemini-3.5-flash", "name": "Gemini 3.5 Flash", "hinweis": ""},
    {"id": "meta-llama/llama-3.3-70b-instruct", "name": "Llama 3.3 70B", "hinweis": "offenes Modell"},
]
MODELL_IDS = {m["id"] for m in MODELLE_WAHL} | {MODELL_ERSATZ}

# Niedrig, weil es um Reproduzierbarkeit geht: derselbe Text soll in der
# Vorfuehrung dieselben Befunde ergeben wie im Test.
TEMPERATUR = 0.0
MAX_TOKENS = 4000
TIMEOUT = 240
# Ein angepasster Prompt darf lang sein, aber nicht beliebig. Der Wert liegt
# rund fuenfmal ueber dem ausgelieferten Prompt.
PROMPT_MAX = 60000

# Zugangsschutz. Leer gelassen ist der Server offen — richtig fuer den lokalen
# Betrieb, falsch sobald er im Netz steht: /api/pruefen ruft ein Modell auf
# Rechnung des hinterlegten Schluessels auf. Ist die Variable gesetzt, verlangt
# jede Anfrage den Benutzernamen "vhs" und dieses Passwort.
PASSWORT = os.environ.get("KLARTEXT_PASSWORT", "").strip()

PLATZHALTER = "{{WORTLISTE_A1}}"
# Fehlt die Wortliste, wird der Platzhalter nicht durch nichts ersetzt, sondern
# durch diese Marke. Ein leerer Codeblock uebersieht sich zu leicht; der Test
# T7 hat genau das gezeigt. Der Prompt kennt die Marke und schaltet darauf um.
FEHLT_MARKE = "KEINE WORTLISTE GELADEN"

# Schreibweise wie im System-Prompt, Abschnitt Programmbereiche.
BEREICHE = [
    "Gesellschaft/Politik/Psychologie",
    "Frankfurt/Region/Umwelt",
    "Kunst/Kultur/Kreativität",
    "Gesundheit",
    "Deutsch als Fremdsprache",
    "Sprachen",
    "Beruf/Karriere/Computer/Internet",
    "Grundbildung/Schule",
]

NIVEAUS = ["A1", "A2", "B1", "B2", "C1", "C2"]
OHNE_NIVEAU = "kein Sprachniveau"


# --------------------------------------------------------------------------
# API-Key
# --------------------------------------------------------------------------

def load_api_key():
    env_value = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if env_value:
        return env_value
    for folder in (BASE_DIR, PROJEKT_DIR, PROJEKT_DIR.parent):
        env_file = folder / ".env"
        if not env_file.is_file():
            continue
        try:
            zeilen = env_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for line in zeilen:
            line = line.strip()
            if line.startswith("OPENROUTER_API_KEY"):
                _, _, value = line.partition("=")
                value = value.strip().strip('"').strip("'")
                if value:
                    return value
    return None


API_KEY = load_api_key()


# --------------------------------------------------------------------------
# System-Prompt und Wortliste
# --------------------------------------------------------------------------

_prompt_cache = {"stempel": None, "daten": None}
_prompt_lock = threading.Lock()


def _wortliste_lesen():
    """Gibt (text, anzahl) zurueck. Fehlt die Datei, kommt ('', 0).

    Die Datei wird parallel von einem anderen Vorgang erzeugt. Fehlt sie oder
    ist sie leer, laeuft die App ohne Referenzwortschatz weiter; der Prompt
    regelt diesen Fall selbst.
    """
    if not WORTLISTE_DATEI.is_file():
        return "", 0
    try:
        roh = WORTLISTE_DATEI.read_text(encoding="utf-8")
    except OSError:
        return "", 0
    woerter = []
    gesehen = set()
    for zeile in roh.splitlines():
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#"):
            continue
        for teil in zeile.split(","):
            wort = teil.strip()
            if wort and wort not in gesehen:
                gesehen.add(wort)
                woerter.append(wort)
    return ", ".join(woerter), len(woerter)


def _stempel():
    """Aenderungsstempel beider Quelldateien, damit der Cache nachzieht."""
    teile = []
    for pfad in (PROMPT_DATEI, WORTLISTE_DATEI):
        try:
            st = pfad.stat()
            teile.append((str(pfad), st.st_mtime, st.st_size))
        except OSError:
            teile.append((str(pfad), None, None))
    return tuple(teile)


def prompt_bauen(erzwingen=False):
    """Baut den System-Prompt aus system-prompt.md und der Wortliste.

    Der Kopfbereich bis zur ersten ---Trennlinie faellt weg, der Platzhalter
    wird ersetzt. Wird bei jeder Anfrage geprueft, damit eine spaeter
    erzeugte Wortliste ohne Neustart wirksam wird.
    """
    with _prompt_lock:
        aktuell = _stempel()
        if not erzwingen and _prompt_cache["stempel"] == aktuell and _prompt_cache["daten"]:
            return _prompt_cache["daten"]

        try:
            roh = PROMPT_DATEI.read_text(encoding="utf-8")
        except OSError as err:
            daten = {
                "prompt": None,
                "promptAnzeige": None,
                "wortlisteText": "",
                "fehler": "System-Prompt nicht lesbar (%s): %s" % (PROMPT_DATEI.name, err),
                "fassung": "unbekannt",
                "wortlisteVorhanden": False,
                "wortanzahl": 0,
                "zeichen": 0,
                "pruefsumme": "",
            }
            _prompt_cache["stempel"] = aktuell
            _prompt_cache["daten"] = daten
            return daten

        treffer = re.search(r"^\*\*Fassung:\*\*\s*(.+)$", roh, re.MULTILINE)
        fassung = treffer.group(1).strip() if treffer else "ohne Angabe"

        zeilen = roh.splitlines()
        start = 0
        for i, zeile in enumerate(zeilen):
            if re.match(r"^-{3,}\s*$", zeile.strip()):
                start = i + 1
                break
        koerper = "\n".join(zeilen[start:]).strip("\n")

        wortliste, anzahl = _wortliste_lesen()
        prompt = koerper.replace(PLATZHALTER, wortliste if anzahl else FEHLT_MARKE)

        # Zwei Fassungen desselben Prompts. `prompt` geht an das Modell und hat
        # die Liste eingesetzt; `promptAnzeige` behaelt den Platzhalter, damit
        # das Panel lesbar bleibt. Fehlt die Liste, zeigt die Anzeige die
        # Fehlt-Marke -- gerade dann ist der Zustand die wichtige Information.
        anzeige = koerper if anzahl else prompt

        daten = {
            "prompt": prompt,
            "promptAnzeige": anzeige,
            "wortlisteText": wortliste,
            "fehler": None,
            "fassung": fassung,
            "wortlisteVorhanden": anzahl > 0,
            "wortanzahl": anzahl,
            "zeichen": len(prompt),
            "pruefsumme": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16],
        }
        _prompt_cache["stempel"] = aktuell
        _prompt_cache["daten"] = daten
        return daten


# --------------------------------------------------------------------------
# Kursdaten
# --------------------------------------------------------------------------

def bereich_raten(nummer, titel):
    """Ersatz fuer Kurse, denen das Portal keinen Programmbereich mitgibt.

    Betrifft rund jeden zwoelften Kurs, vor allem die junge vhs und die
    Stadtteilangebote. Geraten wird nur fuer die Vorbelegung des Formulars;
    im Filter erscheinen diese Kurse als „ohne Angabe", damit die Luecke
    sichtbar bleibt und nicht als Portalangabe durchgeht.
    """
    nummer = (nummer or "").strip()
    titel = (titel or "").strip()
    unten = titel.lower()
    if unten.startswith("daf"):
        return "Deutsch als Fremdsprache"
    ziffer = nummer[:1]
    if ziffer == "0":
        return "Frankfurt/Region/Umwelt"
    if ziffer == "1":
        return "Gesellschaft/Politik/Psychologie"
    if ziffer == "2":
        return "Kunst/Kultur/Kreativität"
    if ziffer == "3":
        return "Gesundheit"
    if ziffer == "4":
        if nummer[:2] in ("40", "41"):
            return "Deutsch als Fremdsprache"
        return "Sprachen"
    if ziffer == "5":
        return "Beruf/Karriere/Computer/Internet"
    if ziffer == "6":
        return "Grundbildung/Schule"
    if ziffer == "7":
        for wort in ("windows", "pc", "computer", "smartphone", "excel", "word", "internet"):
            if wort in unten:
                return "Beruf/Karriere/Computer/Internet"
        return "Gesundheit"
    return "Gesellschaft/Politik/Psychologie"


def niveau_raten(titel):
    treffer = re.search(r"\b([ABC][12])\b", titel or "")
    if treffer:
        return treffer.group(1)
    return OHNE_NIVEAU


UMLAUT_LANG = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})
UMLAUT_KURZ = str.maketrans({"ä": "a", "ö": "o", "ü": "u", "ß": "ss"})


def falten(text):
    """Kleinschreibung, Umlaute in der Ersatzschreibung: „Französisch" wird
    zu „franzoesisch"."""
    return (text or "").lower().translate(UMLAUT_LANG)


def such_text(text):
    """Beide Umlautformen nebeneinander.

    Wer eine Umlauttaste nicht trifft, tippt entweder „franzoesisch" oder
    „franzosisch". Eine einzige Normalform kann nur eines von beiden finden,
    deshalb steht im Index beides. Der Suchbegriff wird nur in der langen Form
    gefaltet; ohne Umlaut geschrieben bleibt er unveraendert und trifft dann
    die kurze Haelfte.
    """
    unten = (text or "").lower()
    return unten.translate(UMLAUT_LANG) + "\n" + unten.translate(UMLAUT_KURZ)


_kurse_cache = {"stempel": None, "liste": [], "quelle": ""}
_kurse_lock = threading.Lock()


def _kurse_aus_datei():
    """Liest den Kursplan, sonst die alte Stichprobe. Gibt (Liste, Quelle)."""
    if KURSE_DATEI.is_file():
        try:
            daten = json.loads(KURSE_DATEI.read_text(encoding="utf-8"))
            return daten.get("kurse") or [], KURSE_DATEI.name
        except (OSError, ValueError):
            pass
    try:
        return json.loads(KURSE_ERSATZ.read_text(encoding="utf-8")), KURSE_ERSATZ.name
    except (OSError, ValueError):
        return [], ""


def kurse_laden():
    """Baut die Kursliste einmal auf und haelt sie im Speicher.

    Der Suchtext wird hier vorbereitet, nicht bei jeder Anfrage: Die Suche
    laeuft ueber gut dreitausend Kurse, und der Aufbau des gefalteten
    Suchtextes kostet mehr als der Vergleich.
    """
    with _kurse_lock:
        try:
            st = KURSE_DATEI.stat() if KURSE_DATEI.is_file() else KURSE_ERSATZ.stat()
            aktuell = (st.st_mtime, st.st_size)
        except OSError:
            aktuell = None
        if _kurse_cache["stempel"] == aktuell and _kurse_cache["liste"]:
            return _kurse_cache["liste"]

        roh, quelle = _kurse_aus_datei()
        liste = []
        for eintrag in roh:
            if not isinstance(eintrag, dict):
                continue
            nummer = str(eintrag.get("nummer") or "").strip()
            titel = re.sub(r"\s+", " ", str(eintrag.get("titel") or "").strip())
            untertitel = re.sub(r"\s+", " ", str(eintrag.get("untertitel") or "").strip())
            text = str(eintrag.get("text") or "")
            # Der Kursplan bringt den Bereich mit, die alte Stichprobe nicht.
            bereich = str(eintrag.get("bereich") or "").strip()
            niveau = str(eintrag.get("niveau") or "").strip() or niveau_raten(titel)
            kurs = {
                "id": eintrag.get("id"),
                "nummer": nummer,
                "titel": titel,
                "untertitel": untertitel,
                "text": text,
                "bereich": bereich,
                "bereichVorschlag": bereich or bereich_raten(nummer, titel),
                "niveau": niveau,
                "ort": str(eintrag.get("ort") or eintrag.get("kursOrt") or "").strip(),
                "preis": eintrag.get("preis"),
                "termin": str(eintrag.get("termin") or "").strip(),
                "zeit": str(eintrag.get("zeit") or "").strip(),
                "zeichen": len(text),
            }
            kurs["_such"] = such_text(" ".join(
                (nummer, titel, untertitel, kurs["ort"], bereich, text)))
            liste.append(kurs)
        liste.sort(key=lambda k: (k["nummer"], k["id"] or 0))
        _kurse_cache["stempel"] = aktuell
        _kurse_cache["liste"] = liste
        _kurse_cache["quelle"] = quelle
        return liste


AUSZUG_LAENGE = 150
AUSZUG_VORLAUF = 55


def auszug_bauen(text, begriffe):
    """Schneidet den Auszug um die erste Fundstelle statt am Textanfang.

    Wer nach einem Wort sucht, das im Beschreibungstext weit hinten steht,
    sieht sonst einen Anfang, in dem der Suchbegriff nicht vorkommt, und kann
    nicht erkennen, warum der Kurs ein Treffer ist. Die Faltung verschiebt die
    Position um ein Zeichen je Umlaut; bei diesem Vorlauf faellt das nicht ins
    Gewicht, die Fundstelle liegt in jedem Fall im Fenster.
    """
    flach = re.sub(r"\s+", " ", text)
    if not begriffe:
        return flach[:AUSZUG_LAENGE]

    unten = flach.lower()
    treffer = []
    for gefaltet in (unten.translate(UMLAUT_LANG), unten.translate(UMLAUT_KURZ)):
        for b in begriffe:
            pos = gefaltet.find(b)
            if pos >= 0:
                treffer.append(pos)
    if not treffer:
        return flach[:AUSZUG_LAENGE]

    start = max(0, min(treffer) - AUSZUG_VORLAUF)
    if start:
        # Nicht mitten im Wort anfangen.
        leer = flach.find(" ", start)
        start = leer + 1 if 0 <= leer < start + 20 else start
    stueck = flach[start:start + AUSZUG_LAENGE]
    return ("… " + stueck) if start else stueck


def kurs_knapp(kurs, begriffe=()):
    """Fassung fuer die Trefferliste: alles ausser dem vollen Text."""
    knapp = {s: kurs[s] for s in (
        "id", "nummer", "titel", "untertitel", "bereich", "bereichVorschlag",
        "niveau", "ort", "preis", "termin", "zeit", "zeichen")}
    knapp["auszug"] = auszug_bauen(kurs["text"], begriffe)
    return knapp


def kurse_suchen(q, bereich, niveau, ort, seite, pro_seite):
    """Sucht und filtert. Die Zaehler je Filterwert beruecksichtigen jeweils
    die uebrigen Filter, damit im Modal keine Auswahl angeboten wird, die
    null Treffer ergibt."""
    alle = kurse_laden()

    begriffe = [t for t in falten(q).split() if t]

    def passt_text(k):
        return all(t in k["_such"] for t in begriffe)

    def passt_bereich(k):
        if not bereich:
            return True
        if bereich == "ohne":
            return not k["bereich"]
        return k["bereich"] == bereich

    def passt_niveau(k):
        if not niveau:
            return True
        if niveau == OHNE_NIVEAU:
            return k["niveau"] == OHNE_NIVEAU
        return k["niveau"] == niveau

    def passt_ort(k):
        if not ort:
            return True
        if ort == "ohne":
            return not k["ort"]
        return k["ort"] == ort

    vor_text = [k for k in alle if passt_text(k)]

    def zaehlen(schluessel, ohne_filter):
        zaehler = {}
        for k in vor_text:
            if ohne_filter != "bereich" and not passt_bereich(k):
                continue
            if ohne_filter != "niveau" and not passt_niveau(k):
                continue
            if ohne_filter != "ort" and not passt_ort(k):
                continue
            # Leere Angaben bekommen einen eigenen Eintrag, damit sie im Modal
            # waehlbar bleiben statt unsichtbar zu verschwinden.
            wert = k[schluessel] or "ohne"
            zaehler[wert] = zaehler.get(wert, 0) + 1
        return zaehler

    treffer = [k for k in vor_text
               if passt_bereich(k) and passt_niveau(k) and passt_ort(k)]

    von = max(0, (seite - 1) * pro_seite)
    ausschnitt = treffer[von:von + pro_seite]

    return {
        "gesamt": len(alle),
        "treffer": len(treffer),
        "seite": seite,
        "proSeite": pro_seite,
        "kurse": [kurs_knapp(k, begriffe) for k in ausschnitt],
        "facetten": {
            "bereich": zaehlen("bereich", "bereich"),
            "niveau": zaehlen("niveau", "niveau"),
            "ort": zaehlen("ort", "ort"),
        },
    }


# --------------------------------------------------------------------------
# Protokoll
# --------------------------------------------------------------------------

def protokoll_schreiben(eintrag, nummer):
    """Legt Anfrage und Antwort als JSON mit Zeitstempel ab.

    Enthaelt bewusst keinen Key und keine Kopfzeilen der Anfrage, sondern nur
    das, was die Testszenarien spaeter belegen muss.
    """
    try:
        PROTOKOLL_DIR.mkdir(parents=True, exist_ok=True)
        sicher = re.sub(r"[^A-Za-z0-9._-]", "_", nummer or "ohne-nummer")[:40]
        name = "%s-%s.json" % (datetime.now().strftime("%Y%m%d-%H%M%S"), sicher)
        pfad = PROTOKOLL_DIR / name
        pfad.write_text(
            json.dumps(eintrag, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return name
    except OSError as err:
        log("Protokoll konnte nicht geschrieben werden: %s" % err)
        return None


def log(text):
    sys.stderr.write("[klartext] %s\n" % text)
    sys.stderr.flush()


# --------------------------------------------------------------------------
# OpenRouter
# --------------------------------------------------------------------------

class ApiFehler(Exception):
    def __init__(self, status, meldung, wiederholbar):
        Exception.__init__(self, meldung)
        self.status = status
        self.meldung = meldung
        self.wiederholbar = wiederholbar


def modell_aufrufen(modell, system_prompt, benutzer_text, temperatur):
    body = json.dumps({
        "model": modell,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": benutzer_text},
        ],
        "temperature": temperatur,
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:%d" % PORT,
            "X-Title": "KLARTEXT VHS Frankfurt",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as antwort:
            roh = antwort.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except Exception:
            pass
        detail = str(detail)[:400]
        raise ApiFehler(err.code, "OpenRouter meldet %s: %s" % (err.code, detail), True)
    except urllib.error.URLError as err:
        raise ApiFehler(502, "Keine Verbindung zu OpenRouter: %s" % err.reason, False)
    except Exception as err:
        raise ApiFehler(502, "Anfrage an OpenRouter fehlgeschlagen: %s" % err, False)

    try:
        daten = json.loads(roh)
    except ValueError:
        raise ApiFehler(502, "OpenRouter hat keine gültige Antwort geliefert.", True)

    if isinstance(daten.get("error"), dict):
        meldung = str(daten["error"].get("message", "unbekannter Fehler"))[:400]
        raise ApiFehler(502, "OpenRouter meldet: %s" % meldung, True)

    auswahl = daten.get("choices") or []
    if not auswahl:
        raise ApiFehler(502, "OpenRouter hat eine leere Antwort geliefert.", True)
    inhalt = (auswahl[0].get("message") or {}).get("content") or ""
    if not inhalt.strip():
        raise ApiFehler(502, "Das Modell hat einen leeren Text geliefert.", True)

    return inhalt, daten.get("usage") or {}


EHRLICHKEITSSATZ = (
    "Ohne Referenzwortschatz geprüft, die Niveau-Befunde sind "
    "Schätzungen. Begründungen, die auf eine Wortliste verweisen, "
    "sind in diesem Lauf unbelegt.")


def ehrlichkeitshinweis(inhalt, wortliste_vorhanden):
    """Setzt den Vorbehalt vor die Ausgabe, wenn die Wortliste fehlt.

    Der Prompt fordert diesen Satz zwar selbst ein, aber Test T7 hat gezeigt,
    dass das Modell ihn zuverlaessig vergisst: Es behauptet dann sogar, ein
    Wort stehe nicht auf einer Liste, die es gar nicht hatte. Ob eine Liste
    geladen ist, weiss der Server sicher. Eine Aussage ueber die Belastbarkeit
    der eigenen Befunde darf deshalb nicht davon abhaengen, ob ein
    Sprachmodell an sie denkt. Sie wird hier gesetzt, nicht erbeten.
    """
    if wortliste_vorhanden:
        return inhalt
    kopf = "HINWEIS DES SYSTEMS\n" + EHRLICHKEITSSATZ + "\n\n"
    return kopf + inhalt


# Die Zuordnung Regelkuerzel zu Einstufung ist eine Tabelle, kein Urteil.
# Sie steht auch im Prompt, aber das Modell hielt sich nicht zuverlaessig
# daran: derselbe Text ergab einmal PFLICHT, einmal HINWEIS. Woran haengt, ob
# ein Befund rechtlich gefordert oder eine Stilfrage ist, gehoert nicht in ein
# Ermessen.
# Seit v7 gibt es nur noch sechs Regeln und zwei Stufen; HINWEIS ist entfallen.
# Der Rang bleibt dreistufig, damit aeltere Protokolle lesbar bleiben.
EINSTUFUNGEN = {
    "STRUKTUR": "PFLICHT",
    "LINKTEXT": "PFLICHT",
    "ABK": "EMPFEHLUNG",
    "NIVEAU": "EMPFEHLUNG",
    "SATZ": "EMPFEHLUNG",
    "AMTSDEUTSCH": "EMPFEHLUNG",
}
RANG = {"PFLICHT": 3, "EMPFEHLUNG": 2, "HINWEIS": 1}

# [1] EMPFEHLUNG · NIVEAU, AMTSDEUTSCH
BEFUNDZEILE = re.compile(
    r"^(\s*\[\d+\]\s+)(PFLICHT|EMPFEHLUNG|HINWEIS)(\s*[·.]\s*)(.+)$")


# Regel 1 des Prompts verbietet Personennamen in der Ausgabe. Bei Namen im
# Fliesstext haelt das Modell sich daran; bei einem Titel davor nicht: Es
# beanstandet das "Dr." als unaufgeloeste Abkuerzung und zitiert dabei den
# ganzen Namen. In vier von vier Laeufen, auch nachdem der Prompt die Ausnahme
# ausdruecklich nannte -- das Modell schrieb die Regel sogar in den Vorschlag
# und meldete den Befund trotzdem. Ob an einer Stelle ein Titel mit Namen
# steht, ist eine Mustererkennung und kein Urteil, also steht sie hier.
#
# Das faengt den beobachteten Fall, nicht die Fehlerklasse: Ein Name ohne
# Titel wird hiervon nicht erfasst, dafuer bleibt Regel 1 zustaendig.
# Mehrere Titel hintereinander muessen mitgehen: "Prof. Dr. Anna Müller" darf
# nicht nach dem ersten Titel abbrechen, sonst bleibt der Name stehen.
# Auch die ausgeschriebene Form muss mit: Das Modell schlaegt von sich aus
# "Doktorin Liliya Karpynska" als Aufloesung vor und bringt den Namen so
# wieder herein, nachdem die abgekuerzte Form entfernt wurde.
TITEL = (r"(?:(?:Dr|Prof|Dipl|Mag|PD|Dres)\.(?:[\s-]*(?:med|phil|rer|nat|jur|paed|Ing)\.)*"
         r"|Doktor(?:in)?|Professor(?:in)?|Herr|Frau)")
NAME_MIT_TITEL = re.compile(
    r"(?:" + TITEL + r"\s*)+"
    r"(?:(?:von|van|de|di|zu)\s+)?"
    r"(?:[A-ZÄÖÜ][\wÄÖÜäöüß'’-]+)(?:\s+[A-ZÄÖÜ][\wÄÖÜäöüß'’-]+){0,2}")


def namensschutz(inhalt):
    """Ersetzt Titel samt folgendem Namen durch [Name].

    Gibt (Text, Zahl der Ersetzungen) zurueck.
    """
    neu, anzahl = NAME_MIT_TITEL.subn("[Name]", inhalt)
    return neu, anzahl


def einstufung_normieren(inhalt):
    """Setzt die Einstufung jeder Befundzeile aus der Tabelle.

    Nach Regel 3 des Prompts gilt bei mehreren Kuerzeln in einer Zeile die
    strengste Einstufung. Kuerzel, die die Tabelle nicht kennt, bleiben ohne
    Wirkung; steht in einer Zeile kein bekanntes Kuerzel, bleibt die Zeile
    unveraendert. Gibt (Text, Zahl der Korrekturen) zurueck.
    """
    korrekturen = 0
    zeilen = []
    for zeile in inhalt.split("\n"):
        treffer = BEFUNDZEILE.match(zeile)
        if not treffer:
            zeilen.append(zeile)
            continue
        vorne, gesetzt, trenner, rest = treffer.groups()
        kuerzel = [k.strip().upper() for k in re.split(r"[,\s]+", rest) if k.strip()]
        bekannt = [EINSTUFUNGEN[k] for k in kuerzel if k in EINSTUFUNGEN]
        if not bekannt:
            zeilen.append(zeile)
            continue
        soll = max(bekannt, key=lambda e: RANG[e])
        if soll != gesetzt:
            korrekturen += 1
            zeile = "%s%s%s%s" % (vorne, soll, trenner, rest)
        zeilen.append(zeile)
    return "\n".join(zeilen), korrekturen


def eingabe_bauen(feld):
    return (
        "KURSTITEL:        %s\n"
        "KURSNUMMER:       %s\n"
        "PROGRAMMBEREICH:  %s\n"
        "NIVEAU:           %s\n"
        "TEXT:\n%s"
    ) % (
        feld["titel"] or "nicht angegeben",
        feld["nummer"] or "nicht angegeben",
        feld["programmbereich"] or "nicht angegeben",
        feld["niveau"] or "kein Sprachniveau",
        feld["text"],
    )


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "KLARTEXT/1.0"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        log(fmt % args)

    def zugang_ok(self):
        """Prueft Basic Auth, sofern KLARTEXT_PASSWORT gesetzt ist. Ohne die
        Variable bleibt der Server offen wie bisher. Der Vergleich laeuft ueber
        compare_digest, damit die Antwortzeit das Passwort nicht verraet."""
        if not PASSWORT:
            return True
        kopf = self.headers.get("Authorization", "")
        if kopf.startswith("Basic "):
            try:
                klar = base64.b64decode(kopf[6:]).decode("utf-8", "replace")
            except Exception:
                klar = ""
            _, _, gesendet = klar.partition(":")
            if hmac.compare_digest(gesendet, PASSWORT):
                return True
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="KLARTEXT", charset="UTF-8"')
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.end_headers()
        return False

    # -- GET ---------------------------------------------------------------
    def do_GET(self):
        if not self.zugang_ok():
            return
        zerlegt = urlparse(self.path)
        pfad = zerlegt.path
        if pfad in ("/", "/index.html"):
            self.seite_ausliefern()
            return
        if pfad == "/api/status":
            self.status_ausliefern()
            return
        if pfad == "/api/prompt":
            self.prompt_ausliefern()
            return
        if pfad == "/api/kurse":
            self.kurse_ausliefern(parse_qs(zerlegt.query))
            return
        if pfad.startswith("/api/kurs/"):
            self.kurs_ausliefern(pfad[len("/api/kurs/"):])
            return
        if pfad.startswith("/schriften/"):
            self.schrift_ausliefern(pfad[len("/schriften/"):])
            return
        self.send_json(404, {"error": "Unbekannter Pfad."})

    def schrift_ausliefern(self, name):
        """Liefert eine Datei aus schriften/. Nur die beiden gebrauchten
        Endungen, und der aufgeloeste Pfad muss im Ordner liegen — sonst
        koennte ein Aufruf mit ../ jede Datei des Rechners abholen."""
        if not name.endswith((".woff2", ".css")):
            self.send_json(404, {"error": "Unbekannter Pfad."})
            return
        ziel = (SCHRIFTEN_DIR / name).resolve()
        if not ziel.is_file() or SCHRIFTEN_DIR.resolve() not in ziel.parents:
            self.send_json(404, {"error": "Unbekannter Pfad."})
            return
        typ = ("font/woff2" if name.endswith(".woff2")
               else "text/css; charset=utf-8")
        inhalt = ziel.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", typ)
        self.send_header("Content-Length", str(len(inhalt)))
        self.send_header("Cache-Control", "max-age=86400")
        self.end_headers()
        self.wfile.write(inhalt)

    def kurse_ausliefern(self, felder):
        def wert(name, ersatz=""):
            return (felder.get(name) or [ersatz])[0].strip()

        def zahl(name, ersatz, klein, gross):
            try:
                n = int(wert(name) or ersatz)
            except ValueError:
                n = ersatz
            return min(gross, max(klein, n))

        self.send_json(200, kurse_suchen(
            q=wert("q"),
            bereich=wert("bereich"),
            niveau=wert("niveau"),
            ort=wert("ort"),
            seite=zahl("seite", 1, 1, 500),
            pro_seite=zahl("proSeite", 40, 5, 200),
        ))

    def kurs_ausliefern(self, roh_id):
        try:
            gesucht = int(roh_id)
        except ValueError:
            self.send_json(400, {"error": "Ungültige Kurskennung."})
            return
        for kurs in kurse_laden():
            if kurs["id"] == gesucht:
                voll = dict(kurs)
                voll.pop("_such", None)
                self.send_json(200, {"kurs": voll})
                return
        self.send_json(404, {"error": "Kurs nicht gefunden."})

    def prompt_ausliefern(self):
        """Liefert den Prompt fuer das Panel, mit Platzhalter statt Wortliste.

        Die 820 Eintraege wuerden das Textfeld unlesbar machen. Der Server
        setzt den Platzhalter beim Pruefen wieder ein, das Panel zeigt daneben
        an, wie viele Woerter dort einruecken. `zeichen` und `pruefsumme`
        bleiben die Werte des vollstaendigen Prompts, denn geprueft wird mit
        diesem; `zeichenAnzeige` gehoert zum Text im Feld.
        """
        p = prompt_bauen()
        anzeige = p["promptAnzeige"] or ""
        self.send_json(200, {
            "prompt": anzeige,
            "platzhalter": PLATZHALTER,
            "zeichenAnzeige": len(anzeige),
            "fehler": p["fehler"],
            "fassung": p["fassung"],
            "zeichen": p["zeichen"],
            "pruefsumme": p["pruefsumme"],
            "wortlisteVorhanden": p["wortlisteVorhanden"],
            "wortanzahl": p["wortanzahl"],
            "wortlisteDatei": WORTLISTE_DATEI.name,
            "promptDatei": PROMPT_DATEI.name,
        })

    def seite_ausliefern(self):
        try:
            inhalt = INDEX_DATEI.read_bytes()
        except OSError:
            self.send_json(500, {"error": "index.html fehlt."})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(inhalt)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(inhalt)

    def status_ausliefern(self):
        p = prompt_bauen()
        kurse = kurse_laden()
        self.send_json(200, {
            "ok": True,
            "hatKey": bool(API_KEY),
            "promptFehler": p["fehler"],
            "fassung": p["fassung"],
            "promptZeichen": p["zeichen"],
            "promptPruefsumme": p["pruefsumme"],
            "wortlisteVorhanden": p["wortlisteVorhanden"],
            "wortanzahl": p["wortanzahl"],
            "wortlisteDatei": WORTLISTE_DATEI.name,
            "modell": MODELL_STANDARD,
            "modellErsatz": MODELL_ERSATZ,
            "modelle": MODELLE_WAHL,
            "temperatur": TEMPERATUR,
            "bereiche": BEREICHE,
            "niveaus": NIVEAUS,
            "ohneNiveau": OHNE_NIVEAU,
            "kursanzahl": len(kurse),
            "kursquelle": _kurse_cache.get("quelle") or "",
        })

    # -- POST --------------------------------------------------------------
    def do_POST(self):
        if not self.zugang_ok():
            return
        pfad = self.path.split("?", 1)[0]
        if pfad != "/api/pruefen":
            self.send_json(404, {"error": "Unbekannter Pfad."})
            return
        try:
            self.pruefen()
        except Exception as err:  # nichts darf als Stacktrace im Browser landen
            log("Unerwarteter Fehler: %r" % (err,))
            self.send_json(500, {"error": "Unerwarteter Fehler im Server. Details siehe Terminal."})

    def pruefen(self):
        if not API_KEY:
            self.send_json(500, {"error":
                "Kein OPENROUTER_API_KEY gefunden. Bitte die .env im Projektordner prüfen."})
            return

        try:
            laenge = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(laenge).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError
        except Exception:
            self.send_json(400, {"error": "Ungültige Anfrage."})
            return

        feld = {
            "titel": str(payload.get("titel") or "").strip(),
            "nummer": str(payload.get("nummer") or "").strip(),
            "programmbereich": str(payload.get("programmbereich") or "").strip(),
            "niveau": str(payload.get("niveau") or "").strip(),
            "text": str(payload.get("text") or "").strip(),
        }
        if not feld["text"]:
            self.send_json(400, {"error": "Kein Kurstext eingegeben. Bitte links einen Text einsetzen."})
            return
        if len(feld["text"]) > 20000:
            self.send_json(400, {"error": "Der Text ist zu lang (höchstens 20.000 Zeichen)."})
            return

        p = prompt_bauen()
        if not p["prompt"]:
            self.send_json(500, {"error": p["fehler"] or "System-Prompt konnte nicht geladen werden."})
            return

        # Prompt, Modell und Temperatur duerfen aus dem Panel kommen. Was davon
        # vom Standard abweicht, steht in der Antwort und im Protokoll: ein
        # Lauf mit veraendertem Prompt darf nicht aussehen wie ein Standardlauf.
        # Das Panel bekommt den Prompt mit Platzhalter; er wird hier wieder
        # ersetzt, bevor verglichen wird. Sonst gaelte jeder Lauf als angepasst.
        prompt_text = p["prompt"]
        prompt_angepasst = False
        roh_prompt = payload.get("prompt")
        if isinstance(roh_prompt, str) and roh_prompt.strip():
            if p["wortanzahl"]:
                roh_prompt = roh_prompt.replace(PLATZHALTER, p["wortlisteText"])
            if len(roh_prompt) > PROMPT_MAX:
                self.send_json(400, {"error":
                    "Der angepasste Prompt ist zu lang (höchstens %s Zeichen)."
                    % format(PROMPT_MAX, ",d").replace(",", ".")})
                return
            if roh_prompt.strip() != prompt_text.strip():
                prompt_text = roh_prompt
                prompt_angepasst = True

        # Der Ehrlichkeitsvorbehalt haengt daran, ob die Liste in dem Prompt
        # steht, der wirklich abgeschickt wird -- nicht daran, ob die Datei auf
        # der Platte liegt. Wer den Platzhalter aus dem Panel loescht, prueft
        # ohne Referenz; das muss in der Ausgabe stehen.
        wortliste_wirksam = bool(p["wortanzahl"]) and p["wortlisteText"] in prompt_text

        pruefsumme = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()[:16]

        gewaehlt = str(payload.get("modell") or "").strip()
        if gewaehlt and gewaehlt not in MODELL_IDS:
            self.send_json(400, {"error": "Unbekanntes Modell: %s" % gewaehlt[:80]})
            return
        erstwahl = gewaehlt or MODELL_STANDARD
        kette = [erstwahl] + ([MODELL_ERSATZ] if erstwahl != MODELL_ERSATZ else [])

        temperatur = TEMPERATUR
        if payload.get("temperatur") is not None:
            try:
                temperatur = min(1.0, max(0.0, float(payload["temperatur"])))
            except (TypeError, ValueError):
                temperatur = TEMPERATUR

        abweichung = (prompt_angepasst
                      or erstwahl != MODELL_STANDARD
                      or abs(temperatur - TEMPERATUR) > 1e-9)

        benutzer_text = eingabe_bauen(feld)
        beginn = time.time()
        letzter = None
        for i, modell in enumerate(kette):
            try:
                inhalt, usage = modell_aufrufen(modell, prompt_text, benutzer_text, temperatur)
            except ApiFehler as err:
                letzter = err
                log("Modell %s fehlgeschlagen: %s" % (modell, err.meldung))
                if err.wiederholbar and i + 1 < len(kette):
                    log("Versuche Ersatzmodell %s" % kette[i + 1])
                    continue
                break
            dauer = round(time.time() - beginn, 2)
            log("Antwort von %s nach %.1fs (Kurs %s)" % (modell, dauer, feld["nummer"] or "ohne Nummer"))
            inhalt, korrekturen = einstufung_normieren(inhalt)
            if korrekturen:
                log("Einstufung korrigiert: %d Zeile(n)" % korrekturen)
            inhalt, namen = namensschutz(inhalt)
            if namen:
                log("Personenname entfernt: %d Stelle(n)" % namen)
            inhalt = ehrlichkeitshinweis(inhalt, wortliste_wirksam)

            eintrag = {
                "zeitpunkt": datetime.now().isoformat(timespec="seconds"),
                "modell": modell,
                "modellErstwahl": erstwahl,
                "modellStandard": MODELL_STANDARD,
                "ersatzmodellGenutzt": modell != erstwahl,
                "temperatur": temperatur,
                "temperaturStandard": TEMPERATUR,
                "promptFassung": p["fassung"],
                "promptPruefsumme": pruefsumme,
                "promptPruefsummeStandard": p["pruefsumme"],
                "promptAngepasst": prompt_angepasst,
                "promptZeichen": len(prompt_text),
                "abweichungVomStandard": abweichung,
                "wortlisteVorhanden": wortliste_wirksam,
                "wortanzahl": p["wortanzahl"],
                "einstufungKorrigiert": korrekturen,
                "namenEntfernt": namen,
                "dauerSekunden": dauer,
                "eingabe": feld,
                "benutzernachricht": benutzer_text,
                "antwort": inhalt,
                "verbrauch": usage,
            }
            # Ein angepasster Prompt wird mitgeschrieben. Ohne ihn liesse sich
            # der Lauf spaeter nicht nachvollziehen, und die Protokolle sind
            # der Beleg der Abgabe.
            if prompt_angepasst:
                eintrag["promptText"] = prompt_text
            name = protokoll_schreiben(eintrag, feld["nummer"])

            self.send_json(200, {
                "ok": True,
                "inhalt": inhalt,
                "modell": modell,
                "ersatzmodellGenutzt": modell != erstwahl,
                "temperatur": temperatur,
                "fassung": p["fassung"],
                "promptAngepasst": prompt_angepasst,
                "promptPruefsumme": pruefsumme,
                "abweichungVomStandard": abweichung,
                "wortlisteVorhanden": wortliste_wirksam,
                "wortanzahl": p["wortanzahl"],
                "einstufungKorrigiert": korrekturen,
                "dauerSekunden": dauer,
                "protokoll": name,
            })
            return

        meldung = letzter.meldung if letzter else "Die Anfrage ist fehlgeschlagen."
        status = letzter.status if letzter else 502
        if status < 400 or status > 599:
            status = 502
        self.send_json(status, {"error": meldung})

    # -- Hilfen ------------------------------------------------------------
    def send_json(self, status, obj):
        try:
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass


def main():
    p = prompt_bauen(erzwingen=True)
    print("KLARTEXT, Redaktionsassistent VHS Frankfurt")
    print("  System-Prompt: %s (Fassung %s, %d Zeichen)" % (
        PROMPT_DATEI.name, p["fassung"], p["zeichen"]))
    if p["fehler"]:
        print("  ACHTUNG: %s" % p["fehler"])
    if p["wortlisteVorhanden"]:
        print("  Referenzwortschatz: %d Eintraege aus %s" % (p["wortanzahl"], WORTLISTE_DATEI.name))
    else:
        print("  Referenzwortschatz: NICHT vorhanden (%s). Die Pruefung laeuft ohne Referenz."
              % WORTLISTE_DATEI.name)
    anzahl = len(kurse_laden())
    quelle = _kurse_cache.get("quelle") or "keine Datei"
    print("  Kursdaten: %d Kurse aus %s" % (anzahl, quelle))
    if quelle == KURSE_ERSATZ.name:
        print("  Hinweis: %s fehlt. Vollstaendigen Kursplan holen mit"
              % KURSE_DATEI.name)
        print("           python3 ../daten/kursplan-holen.py")
    print("  Modell: %s (Ersatz %s), Temperatur %s"
          % (MODELL_STANDARD, MODELL_ERSATZ, TEMPERATUR))
    if not API_KEY:
        print("  ACHTUNG: kein OPENROUTER_API_KEY gefunden.")
        print("  Gesucht in: Umgebungsvariable, %s/.env, %s/.env, %s/.env"
              % (BASE_DIR, PROJEKT_DIR, PROJEKT_DIR.parent))
    print("  Protokolle: %s" % PROTOKOLL_DIR)
    print("  Zugang: %s" % ("Passwort gesetzt" if PASSWORT else "offen, kein Passwort"))
    if not PASSWORT and HOST != "127.0.0.1":
        print("  ACHTUNG: erreichbar auf %s ohne Passwort. Jeder Aufruf von" % HOST)
        print("           /api/pruefen geht auf Rechnung des API-Schluessels.")
        print("           Abhilfe: Umgebungsvariable KLARTEXT_PASSWORT setzen.")

    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = "http://localhost:%d" % PORT
    print("\nLaeuft: %s   (Beenden mit Ctrl+C)\n" % url)
    if "--open" in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")


if __name__ == "__main__":
    main()
