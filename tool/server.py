#!/usr/bin/env python3
"""Lokaler Server fuer KLARTEXT, den Redaktionsassistenten der VHS Frankfurt.

Liest den OpenRouter-Key aus einer .env-Datei (dieser Ordner, der Ordner
darueber oder der Ordner darueber) und reicht die Pruefanfragen der Web-App
als Proxy an OpenRouter weiter. Der Key wird nie an den Browser ausgeliefert,
nie protokolliert und nie in eine Datei geschrieben.

Start:  python3 server.py          ->  http://localhost:8799
        python3 server.py --open   ->  oeffnet zusaetzlich den Browser
"""

import hashlib
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

PORT = 8799
API_URL = "https://openrouter.ai/api/v1/chat/completions"

BASE_DIR = Path(__file__).resolve().parent
PROJEKT_DIR = BASE_DIR.parent
PROMPT_DATEI = PROJEKT_DIR / "system-prompt.md"
WORTLISTE_DATEI = PROJEKT_DIR / "daten" / "wortliste-goethe-a1.txt"
KURSE_DATEI = PROJEKT_DIR / "daten" / "vhs-stichprobe-60.json"
PROTOKOLL_DIR = BASE_DIR / "protokoll"
INDEX_DATEI = BASE_DIR / "index.html"

# Erstwahl, danach der Ersatz. Welches Modell geantwortet hat, steht im
# Protokoll und in der Fusszeile der Oberflaeche.
MODELLE = ["anthropic/claude-sonnet-4.5", "anthropic/claude-3.7-sonnet"]
# Niedrig, weil es um Reproduzierbarkeit geht: derselbe Text soll in der
# Vorfuehrung dieselben Befunde ergeben wie im Test.
TEMPERATUR = 0.1
MAX_TOKENS = 4000
TIMEOUT = 240

PLATZHALTER = "{{WORTLISTE_A1}}"
# Fehlt die Wortliste, wird der Platzhalter nicht durch nichts ersetzt, sondern
# durch diese Marke. Ein leerer Codeblock uebersieht sich zu leicht; der Test
# T7 hat genau das gezeigt. Der Prompt kennt die Marke und schaltet darauf um.
FEHLT_MARKE = "KEINE WORTLISTE GELADEN"

BEREICHE = [
    "Gesellschaft/Politik/Psychologie",
    "Frankfurt/Region/Umwelt",
    "Kunst/Kultur/Kreativitaet",
    "Gesundheit",
    "Deutsch als Fremdsprache",
    "Sprachen",
    "Beruf/Karriere/Computer/Internet",
    "Grundbildung/Schule",
]


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

        daten = {
            "prompt": prompt,
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
        return "Kunst/Kultur/Kreativitaet"
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
    return "kein Sprachniveau"


def kurse_laden():
    try:
        daten = json.loads(KURSE_DATEI.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    liste = []
    for eintrag in daten:
        if not isinstance(eintrag, dict):
            continue
        nummer = str(eintrag.get("nummer") or "").strip()
        titel = str(eintrag.get("titel") or "").strip()
        liste.append({
            "id": eintrag.get("id"),
            "nummer": nummer,
            "titel": titel,
            "text": eintrag.get("text") or "",
            "kursleiter": eintrag.get("kursleiter") or "",
            "preis": eintrag.get("preis"),
            "programmbereich": bereich_raten(nummer, titel),
            "niveau": niveau_raten(titel),
        })
    liste.sort(key=lambda k: k["nummer"])
    return liste


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


def modell_aufrufen(modell, system_prompt, benutzer_text):
    body = json.dumps({
        "model": modell,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": benutzer_text},
        ],
        "temperature": TEMPERATUR,
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
        raise ApiFehler(502, "OpenRouter hat keine gueltige Antwort geliefert.", True)

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
# Ermessen. BAUSTEIN und FREMDANWEISUNG sind Kennzeichnungen, keine Regeln;
# sie stehen hier mit ihrer Einstufung, damit die Zeile vollstaendig bleibt.
EINSTUFUNGEN = {
    "STRUKTUR": "PFLICHT",
    "LINKTEXT": "PFLICHT",
    "SPRACHE": "PFLICHT",
    "ABK": "EMPFEHLUNG",
    "NIVEAU": "EMPFEHLUNG",
    "SATZ": "EMPFEHLUNG",
    "AMTSDEUTSCH": "EMPFEHLUNG",
    "ANREDE": "HINWEIS",
    "LEER": "HINWEIS",
    "FREMDANWEISUNG": "HINWEIS",
    "BAUSTEIN": "HINWEIS",
}
RANG = {"PFLICHT": 3, "EMPFEHLUNG": 2, "HINWEIS": 1}

# [1] EMPFEHLUNG · NIVEAU, AMTSDEUTSCH
BEFUNDZEILE = re.compile(
    r"^(\s*\[\d+\]\s+)(PFLICHT|EMPFEHLUNG|HINWEIS)(\s*[·.]\s*)(.+)$")


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

    # -- GET ---------------------------------------------------------------
    def do_GET(self):
        pfad = self.path.split("?", 1)[0]
        if pfad in ("/", "/index.html"):
            self.seite_ausliefern()
            return
        if pfad == "/api/status":
            self.status_ausliefern()
            return
        if pfad == "/api/kurse":
            self.send_json(200, {"kurse": kurse_laden()})
            return
        self.send_json(404, {"error": "Unbekannter Pfad."})

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
        self.send_json(200, {
            "ok": True,
            "hatKey": bool(API_KEY),
            "promptFehler": p["fehler"],
            "fassung": p["fassung"],
            "promptZeichen": p["zeichen"],
            "wortlisteVorhanden": p["wortlisteVorhanden"],
            "wortanzahl": p["wortanzahl"],
            "modell": MODELLE[0],
            "modellErsatz": MODELLE[1],
            "temperatur": TEMPERATUR,
            "bereiche": BEREICHE,
        })

    # -- POST --------------------------------------------------------------
    def do_POST(self):
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
                "Kein OPENROUTER_API_KEY gefunden. Bitte die .env im Projektordner pruefen."})
            return

        try:
            laenge = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(laenge).decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError
        except Exception:
            self.send_json(400, {"error": "Ungueltige Anfrage."})
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
            self.send_json(400, {"error": "Der Text ist zu lang (hoechstens 20.000 Zeichen)."})
            return

        p = prompt_bauen()
        if not p["prompt"]:
            self.send_json(500, {"error": p["fehler"] or "System-Prompt konnte nicht geladen werden."})
            return

        benutzer_text = eingabe_bauen(feld)
        beginn = time.time()
        letzter = None
        for i, modell in enumerate(MODELLE):
            try:
                inhalt, usage = modell_aufrufen(modell, p["prompt"], benutzer_text)
            except ApiFehler as err:
                letzter = err
                log("Modell %s fehlgeschlagen: %s" % (modell, err.meldung))
                if err.wiederholbar and i + 1 < len(MODELLE):
                    log("Versuche Ersatzmodell %s" % MODELLE[i + 1])
                    continue
                break
            dauer = round(time.time() - beginn, 2)
            log("Antwort von %s nach %.1fs (Kurs %s)" % (modell, dauer, feld["nummer"] or "ohne Nummer"))
            inhalt, korrekturen = einstufung_normieren(inhalt)
            if korrekturen:
                log("Einstufung korrigiert: %d Zeile(n)" % korrekturen)
            inhalt = ehrlichkeitshinweis(inhalt, p["wortlisteVorhanden"])

            eintrag = {
                "zeitpunkt": datetime.now().isoformat(timespec="seconds"),
                "modell": modell,
                "modellErstwahl": MODELLE[0],
                "ersatzmodellGenutzt": modell != MODELLE[0],
                "temperatur": TEMPERATUR,
                "promptFassung": p["fassung"],
                "promptPruefsumme": p["pruefsumme"],
                "promptZeichen": p["zeichen"],
                "wortlisteVorhanden": p["wortlisteVorhanden"],
                "wortanzahl": p["wortanzahl"],
                "einstufungKorrigiert": korrekturen,
                "dauerSekunden": dauer,
                "eingabe": feld,
                "benutzernachricht": benutzer_text,
                "antwort": inhalt,
                "verbrauch": usage,
            }
            name = protokoll_schreiben(eintrag, feld["nummer"])

            self.send_json(200, {
                "ok": True,
                "inhalt": inhalt,
                "modell": modell,
                "ersatzmodellGenutzt": modell != MODELLE[0],
                "temperatur": TEMPERATUR,
                "fassung": p["fassung"],
                "wortlisteVorhanden": p["wortlisteVorhanden"],
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
    print("  Kursdaten: %d Kurse" % len(kurse_laden()))
    if not API_KEY:
        print("  ACHTUNG: kein OPENROUTER_API_KEY gefunden.")
        print("  Gesucht in: Umgebungsvariable, %s/.env, %s/.env, %s/.env"
              % (BASE_DIR, PROJEKT_DIR, PROJEKT_DIR.parent))
    print("  Protokolle: %s" % PROTOKOLL_DIR)

    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
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
