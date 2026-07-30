#!/usr/bin/env python3
"""
KLARTEXT — dieselbe Messung, angewandt auf den ganzen Kursbestand.

`messung.py` rechnet die Befundquote über die 60er-Stichprobe nach. Dieses
Skript ändert an der Methode nichts: Es importiert `messung.py` unverändert
und wechselt allein die Eingabemenge — von 60 gezogenen Texten auf alle
Kurstexte, die der Portalabruf vom 28.07.2026 geliefert hat.

    python3 daten/messung-bestand.py
    python3 daten/messung-bestand.py --json

Der Grund für die Umstellung ist nicht Genauigkeit, sondern Einfachheit. Eine
Stichprobe muss man rechtfertigen: wie gezogen, aus welchen Bereichen, warum
tragfähig. Eine Vollerhebung braucht diese Begründung nicht — und Folie 4 der
Präsentation stützt sich ohnehin schon auf den ganzen Bestand. Bis hierher
standen zwei Grundlagen nebeneinander, jetzt ist es eine.

Dass die Umstellung die Aussage nicht verschiebt, ist selbst ein Ergebnis: die
Stichprobe lag 1,6 Prozentpunkte neben der Vollerhebung.

ZWEI ABWEICHUNGEN GEGENÜBER `messung.py`, BEIDE HIER UND NICHT DORT

`messung.py` bleibt eingefroren; seine eigene Kopfzeile verlangt, dass eine
unvermeidliche Änderung in eine zweite Datei mit eigenem Namen gehört. Das ist
diese Datei. Sie ändert zwei Dinge, beide erst nach der Messung:

1. STRENGER FALL NACH PROGRAMMBEREICH. `messung.py` erkennt Deutschkurse an
   der Kursnummer 40xx oder 41xx. In der Stichprobe trifft das zu. Im ganzen
   Bestand fallen darunter auch Arabisch (4154-xx) und Bulgarisch (4155-xx) —
   23 der 129 streng geprüften Texte sind keine Deutschkurse. Für die
   Teilzahlen zu den Deutschkursen wird deshalb zusätzlich das Feld `bereich`
   verlangt. Auf die Gesamtquote wirkt sich das nicht aus: Kein einziger Kurs
   verdankt seinen Befund allein dieser Fehlzuordnung, geprüft wird das unten.

2. ZÄHLEINHEIT TEXT. 54 Prozent der Kurse teilen ihren Text wörtlich mit
   mindestens einem anderen. Beide Zählweisen stehen deshalb nebeneinander:
   je Kurs, wie die Stichprobenmessung, und je eigenständigem Text. Sie liegen
   weniger als einen Prozentpunkt auseinander.

Alles andere — Wortliste, Satzgrenzen, Ausnahmeregeln, Selbstprüfung — kommt
unverändert aus `messung.py`. Die Grenzen jener Messung gelten hier
unverändert weiter, insbesondere: STRUKTUR wird nicht gemessen, NIVEAU nur im
strengen Fall. Die Quote ist eine Untergrenze.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent
sys.path.insert(0, str(WURZEL))

import messung  # noqa: E402  — dieselbe Methode, unverändert

BESTAND = WURZEL / "vhs-kursplan.json"

# Programmbereiche, in denen ein Kurs tatsächlich Deutsch vermittelt. Die
# Nummernsystematik allein trägt im ganzen Bestand nicht, siehe Kopfzeile.
DEUTSCH_BEREICHE = ("Deutsch als Fremdsprache", "Grundbildung/Schule")


def signatur(kurs):
    return hashlib.md5((kurs.get("text") or "").strip().encode()).hexdigest()


def lernt_deutsch(kurs, ergebnis):
    """Strenger Fall, abgesichert über den Programmbereich."""
    if not ergebnis["streng"]:
        return False
    bereich = kurs.get("bereich") or ""
    # Ohne Bereichsangabe bleibt es bei der Einstufung von `messung.py`.
    return not bereich or bereich in DEUTSCH_BEREICHE


def auswerten():
    daten = json.load(open(BESTAND, encoding="utf-8"))
    kurse = [k for k in daten["kurse"] if (k.get("text") or "").strip()]
    ohne_text = len(daten["kurse"]) - len(kurse)

    ergebnisse = [messung.messen(k) for k in kurse]

    mit_befund = sum(1 for e in ergebnisse if e["befunde"])

    # Gegenprobe zur Fehlzuordnung: Verlöre ein Kurs seinen Befund, wenn die
    # Niveauprüfung bei den fälschlich streng geprüften Texten entfiele?
    nur_fehlzuordnung = 0
    for k, e in zip(kurse, ergebnisse):
        if e["befunde"] and e["streng"] and not lernt_deutsch(k, e):
            if not [b for b in e["befunde"] if b["regel"] != "NIVEAU"]:
                nur_fehlzuordnung += 1

    # Je eigenständigem Text
    nach_text = {}
    for k, e in zip(kurse, ergebnisse):
        nach_text.setdefault(signatur(k), []).append((k, e))
    texte = [gruppe[0] for gruppe in nach_text.values()]
    texte_mit_befund = sum(1 for _, e in texte if e["befunde"])
    geteilt = sum(len(g) for g in nach_text.values() if len(g) > 1)

    # Deutschkurse auf A1 und A2 — der Fall, für den die Arbeit gemacht ist
    daf = []
    for k, e in texte:
        if lernt_deutsch(k, e) and (k.get("niveau") or e["niveau"]) in ("A1", "A2"):
            daf.append((k, e, len(nach_text[signatur(k)])))
    daf_mit_niveau = [d for d in daf if d[1]["je_regel"]["NIVEAU"]]
    daf_kurse = sum(n for _, _, n in daf)

    # Hebel: die häufigsten dieser Texte decken wie viele Kurse ab?
    nach_haeufigkeit = sorted(daf_mit_niveau, key=lambda d: -d[2])
    hebel = {}
    lauf = 0
    for i, (_, _, n) in enumerate(nach_haeufigkeit, 1):
        lauf += n
        if i in (5, 10):
            hebel[i] = lauf

    return {
        "abgerufen": daten.get("abgerufen"),
        "kurse_gesamt": len(daten["kurse"]),
        "ohne_text": ohne_text,
        "kurse": len(kurse),
        "kurse_mit_befund": mit_befund,
        "quote_kurse": round(100.0 * mit_befund / len(kurse), 1),
        "nur_fehlzuordnung": nur_fehlzuordnung,
        "texte": len(texte),
        "texte_mit_befund": texte_mit_befund,
        "quote_texte": round(100.0 * texte_mit_befund / len(texte), 1),
        "kurse_mit_geteiltem_text": geteilt,
        "quote_geteilt": round(100.0 * geteilt / len(kurse), 1),
        "daf_a1a2_texte": len(daf),
        "daf_a1a2_texte_mit_niveau": len(daf_mit_niveau),
        "daf_a1a2_kurse": daf_kurse,
        "hebel_5_texte": hebel.get(5),
        "hebel_10_texte": hebel.get(10),
        "selbstpruefung": messung.selbstpruefung() or "bestanden",
    }


def bericht(d):
    print()
    print("KLARTEXT — Befundquote über den ganzen Kursbestand")
    print("Portalabruf %s · Methode unverändert aus messung.py" % d["abgerufen"])
    print("Selbstprüfung der Wortzerlegung: %s" % d["selbstpruefung"])
    print()
    print("  Kurse im Bestand           %5d  (%d ohne Text, nicht gewertet)"
          % (d["kurse_gesamt"], d["ohne_text"]))
    print("  ausgewertet                %5d" % d["kurse"])
    print("  mit mindestens einem Befund%5d  = %.1f %%"
          % (d["kurse_mit_befund"], d["quote_kurse"]))
    print()
    print("  eigenständige Texte        %5d" % d["texte"])
    print("  davon mit Befund           %5d  = %.1f %%"
          % (d["texte_mit_befund"], d["quote_texte"]))
    print("  Kurse mit geteiltem Text   %5d  = %.0f %%"
          % (d["kurse_mit_geteiltem_text"], d["quote_geteilt"]))
    print()
    print("  Deutschkurse auf A1 und A2")
    print("    eigenständige Texte      %5d" % d["daf_a1a2_texte"])
    print("    davon mit Wörtern über dem Niveau ihrer Leser  %d"
          % d["daf_a1a2_texte_mit_niveau"])
    print("    diese Texte stecken in   %5d Kursen" % d["daf_a1a2_kurse"])
    print("    die 5 häufigsten decken  %5d Kurse ab" % (d["hebel_5_texte"] or 0))
    print("    die 10 häufigsten decken %5d Kurse ab" % (d["hebel_10_texte"] or 0))
    print()
    print("  Kurse, die ihren Befund allein der Nummernheuristik verdanken: %d"
          % d["nur_fehlzuordnung"])
    print()
    print("  STRUKTUR ist nicht gemessen, NIVEAU nur bei Deutschkursen.")
    print("  Die Quote ist eine Untergrenze.")
    print()


def main():
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    p.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    a = p.parse_args()
    d = auswerten()
    if a.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
    else:
        bericht(d)


if __name__ == "__main__":
    main()
