#!/usr/bin/env python3
"""Holt den vollständigen Kursplan der VHS Frankfurt und legt ihn als JSON ab.

Das Kursportal der vhs läuft auf einem Kundenportal mit offener Schnittstelle.
Der Abruf geht in zwei Schritten:

1. Ein POST auf `api/angebot` ohne Suchkriterien liefert das gesamte buchbare
   Angebot in einer einzigen Antwort, mit allen Stammdaten.
2. Ein GET auf `api/angebot/<id>` liefert je Kurs den **vollständigen**
   Beschreibungstext.

Schritt 2 ist nicht wegzulassen. Die Liste liefert den Text ohne die
vorangestellten Bausteine, also ohne den Anmeldehinweis und ohne den
eingebetteten Link. Genau diese Bausteine erzeugen einen erheblichen Teil der
Befunde, die KLARTEXT finden soll: Der Kernfall 4074-74 hat in der Liste 331,
im Detail 710 Zeichen, und nur die Detailfassung enthält das `hier` als
Linktext, an dem die Regel LINKTEXT greift. Wer nur die Liste abruft, prüft
einen Text, den so niemand zu sehen bekommt.

Schritt 2 kostet eine Anfrage je Kurs und wird deshalb auf zwei Anfragen je
Sekunde gedrosselt. Das Kursportal ist eine öffentliche kommunale Seite. Der
Lauf dauert rund eine halbe Stunde und ist wiederaufnehmbar: Bereits geholte
Texte liegen in einer Zwischendatei, ein Abbruch kostet nur den Rest.

    python3 kursplan-holen.py           ->  daten/vhs-kursplan.json
    python3 kursplan-holen.py --pruefen ->  vergleicht mit der vorhandenen
                                            Datei, ohne sie zu überschreiben

Die alten Stichproben `vhs-stichprobe-60.json` und `vhs-stichprobe-gross.json`
bleiben unangetastet. Sie sind die Messgrundlage der Abgaben und dürfen nicht
durch einen späteren Abruf verändert werden.
"""

import json
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ZIEL = BASE_DIR / "vhs-kursplan.json"
CACHE = BASE_DIR / ".kursplan-texte.json"

API = "https://vhs.frankfurt.de/KundenportalApi/api/angebot"
TIMEOUT = 180
# Zwei Anfragen je Sekunde, siehe Kopfkommentar.
PAUSE = 0.5

# Das Portal schreibt die Bereiche mit Komma, der System-Prompt mit Schrägstrich
# und Umlaut. Übersetzt wird hier, damit im Prompt genau die acht Bezeichnungen
# ankommen, die er in seiner Bereichsliste führt.
BEREICH_AUS_PORTAL = {
    "Gesellschaft, Politik, Psychologie": "Gesellschaft/Politik/Psychologie",
    "Frankfurt, Region, Umwelt": "Frankfurt/Region/Umwelt",
    "Kunst, Kultur, Kreativität": "Kunst/Kultur/Kreativität",
    "Gesundheit": "Gesundheit",
    "Deutsch als Fremdsprache": "Deutsch als Fremdsprache",
    "Sprachen": "Sprachen",
    "Beruf, Karriere, Computer, Internet": "Beruf/Karriere/Computer/Internet",
    "Grundbildung, Schule": "Grundbildung/Schule",
}


KOPFZEILEN = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "KLARTEXT Redaktionsassistenz (Abschlussprojekt VHS Frankfurt)",
}


def abrufen():
    req = urllib.request.Request(
        API, data=json.dumps({}).encode("utf-8"), headers=KOPFZEILEN, method="POST")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as antwort:
        roh = antwort.read().decode("utf-8", "replace")
    daten = json.loads(roh)
    if not daten.get("success"):
        raise RuntimeError("Portal meldet Fehler: %s" % daten.get("message"))
    return daten["data"]


def volltext_holen(angebot_id):
    """Holt den vollständigen Beschreibungstext eines Kurses.

    Gibt None zurück, wenn der Abruf scheitert. Der Aufrufer behält dann den
    Kurztext aus der Liste und vermerkt das, statt den Kurs stillschweigend
    wegzulassen.
    """
    req = urllib.request.Request(
        "%s/%d" % (API, angebot_id), headers=KOPFZEILEN, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=60) as antwort:
            daten = json.loads(antwort.read().decode("utf-8", "replace"))
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, OSError):
        return None
    if not daten.get("success") or not isinstance(daten.get("data"), dict):
        return None
    return daten["data"].get("text") or ""


def volltexte_holen(kurse):
    """Ergänzt die Kurse um ihren vollständigen Text, gedrosselt und wiederaufnehmbar."""
    cache = {}
    if CACHE.is_file():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except ValueError:
            cache = {}
        print("  Zwischenstand gefunden: %d Texte" % len(cache))

    offen = [k for k in kurse if str(k["id"]) not in cache]
    print("  Volltexte zu holen: %d von %d (rund %d Minuten)"
          % (len(offen), len(kurse), round(len(offen) * PAUSE / 60) + 1))

    fehler = 0
    for i, kurs in enumerate(offen, 1):
        text = volltext_holen(kurs["id"])
        if text is None:
            fehler += 1
        else:
            cache[str(kurs["id"])] = text
        if i % 100 == 0 or i == len(offen):
            CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            print("    %d/%d, davon nicht abrufbar: %d" % (i, len(offen), fehler),
                  flush=True)
        time.sleep(PAUSE)

    if offen:
        CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    ohne_volltext = 0
    for kurs in kurse:
        roh = cache.get(str(kurs["id"]))
        if roh is None:
            ohne_volltext += 1
            kurs["textQuelle"] = "liste"
            continue
        voll = aufraeumen(roh)
        kurs["textQuelle"] = "detail"
        if voll:
            kurs["text"] = voll
    return ohne_volltext


def niveau_aus_titel(titel):
    treffer = re.search(r"\b([ABC][12])\b", titel or "")
    return treffer.group(1) if treffer else ""


def aufraeumen(wert):
    """Vereinheitlicht Zeilenenden und schneidet Rand-Leerraum ab."""
    if not wert:
        return ""
    return str(wert).replace("\r\n", "\n").replace("\r", "\n").strip()


def umformen(rohliste):
    kurse = []
    for eintrag in rohliste:
        titel = aufraeumen(eintrag.get("titel"))
        text = aufraeumen(eintrag.get("text"))
        thema = eintrag.get("themenMerkmal")
        kurse.append({
            "id": eintrag.get("angebotId"),
            "nummer": aufraeumen(eintrag.get("nummer")),
            "titel": re.sub(r"\s+", " ", titel),
            "untertitel": re.sub(r"\s+", " ", aufraeumen(eintrag.get("untertitel"))),
            # Leer, wo das Portal keinen Bereich führt. Geraten wird nicht: das
            # Tool zeigt diese Kurse als „ohne Angabe" und belegt das Feld erst
            # beim Übernehmen aus der Kursnummer vor, sichtbar und änderbar.
            "bereich": BEREICH_AUS_PORTAL.get(thema, "") if thema else "",
            "niveau": niveau_aus_titel(titel),
            "ort": aufraeumen(eintrag.get("kursOrt")),
            "preis": eintrag.get("preis"),
            "termin": re.sub(r"\s+", " ", aufraeumen(eintrag.get("terminStruktur"))),
            "zeit": re.sub(r"\s+", " ", aufraeumen(eintrag.get("datumStruktur"))),
            "beginn": (eintrag.get("von") or "")[:10],
            "text": text,
        })
    kurse.sort(key=lambda k: (k["nummer"], k["id"] or 0))
    return kurse


def main():
    nur_pruefen = "--pruefen" in sys.argv
    print("Rufe den Kursplan ab: %s" % API)
    try:
        data = abrufen()
    except (urllib.error.URLError, urllib.error.HTTPError) as err:
        print("Abruf fehlgeschlagen: %s" % err)
        return 1
    except (ValueError, RuntimeError) as err:
        print("Antwort unbrauchbar: %s" % err)
        return 1

    kurse = umformen(data.get("results") or [])
    print("  %d Angebote gemeldet, %d übernommen" % (data.get("total", 0), len(kurse)))

    if not nur_pruefen:
        ohne_volltext = volltexte_holen(kurse)
        if ohne_volltext:
            print("  ACHTUNG: %d Kurse ohne Volltext, dort steht der Kurztext der Liste."
                  % ohne_volltext)

    ohne_text = sum(1 for k in kurse if not k["text"])
    ohne_bereich = sum(1 for k in kurse if not k["bereich"])
    print("  davon ohne Beschreibungstext: %d" % ohne_text)
    print("  davon ohne Bereichsangabe des Portals: %d" % ohne_bereich)

    if nur_pruefen:
        if not ZIEL.is_file():
            print("Vergleich nicht möglich, %s fehlt." % ZIEL.name)
            return 1
        alt = json.loads(ZIEL.read_text(encoding="utf-8"))
        alte_ids = {k["id"] for k in alt["kurse"]}
        neue_ids = {k["id"] for k in kurse}
        print("  neu hinzugekommen: %d, entfallen: %d"
              % (len(neue_ids - alte_ids), len(alte_ids - neue_ids)))
        print("Datei wurde nicht verändert.")
        return 0

    inhalt = {
        "abgerufen": datetime.now().isoformat(timespec="seconds"),
        "quelle": API,
        "anzahl": len(kurse),
        "ohneText": ohne_text,
        "kurse": kurse,
    }
    ZIEL.write_text(
        json.dumps(inhalt, ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    print("Geschrieben: %s (%.1f MB)" % (ZIEL.name, ZIEL.stat().st_size / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
