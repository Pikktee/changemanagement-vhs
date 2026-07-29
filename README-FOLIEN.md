# So bearbeitest du die Präsentation

Du änderst **nur `folien.md`**. Nichts anderes.

```bash
python3 watch.py
```

Laufen lassen, `folien.md` bearbeiten, speichern. Nach jedem Speichern entsteht
`ausgabe/Praesentation-KLARTEXT.pptx` neu, samt Referentennotizen und
Zeitschätzung. Beenden mit Strg+C.

Einmalig bauen ohne Watcher:

```bash
python3 build.py
```

Nur bestimmte Folien neu schießen, wenn es schnell gehen soll:

```bash
python3 build.py --nur 3,7
```

Nur das HTML prüfen, ohne Chrome zu starten:

```bash
python3 build.py --schnell
```

**Wichtig:** Änderungen in der PowerPoint-Datei selbst gehen beim nächsten Build
verloren. Die Folien liegen dort als Bilder, damit das Layout exakt stimmt.

---

## Aufbau einer Folie

```
## 5 — Die Messung          ← nur ein Merkzettel für dich, erscheint nirgends

typ: zahlen
kapitel: 01 · POTENZIAL
titel: Neun von zehn Texten
akzent: haben einen Befund.

### NOTIZ

Der Sprechtext. Alles bis zur nächsten Folie landet in der
Referentenansicht.
```

Regeln:

- `## ` beginnt eine neue Folie.
- `schlüssel: wert` setzt ein Feld.
- `schlüssel:` allein, gefolgt von `- ` Zeilen, ergibt eine Liste.
- `### NOTIZ` leitet den Sprechtext ein.
- `**fett**` funktioniert in allen Texten.
- Anführungszeichen um einen Wert sind erlaubt und werden entfernt. Nötig
  sind sie nur, wenn der Wert selbst einen Doppelpunkt enthält.

**Folien umsortieren:** Den ganzen Block von `## ` bis zur nächsten `## `
ausschneiden und woanders einfügen. Die Nummern im Merkzettel sind egal, die
Reihenfolge in der Datei zählt.

---

## Felder, die überall gehen

| Feld | Wirkung |
|---|---|
| `typ` | Folientyp, siehe unten. Ohne Angabe: `punkte` |
| `kapitel` | Kopfzeile rechts, z. B. `01 · UNTERNEHMEN` |
| `titel` | Überschrift, schwarz |
| `akzent` | Fortsetzung der Überschrift in Petrol |
| `lede` | Ein grauer Satz unter der Überschrift |
| `klein: ja` | kleinere Überschrift, wenn sie sonst zu viel Platz frisst |
| `callout` | Petrolfarbener Balken unten |
| `calloutsub` | Zweite Zeile im Balken, kleiner |
| `quellen` | Kleine Quellenzeile über der Fußzeile, siehe unten |
| `meta` | Nur auf `titel` und `schluss`: Angaben in Versalien, mit `\|` getrennt |
| `fussl`, `fussr` | Fußzeile links und rechts überschreiben |
| `bild` | Pfad zu einem Bild, z. B. `bilder/05-raster.jpg` |
| `bu` | Bildunterschrift unter dem Bild |
| `bildprompt` | Dokumentation, wie das Bild entstanden ist. Erscheint nicht auf der Folie |

---

## Quellen verlinken

Schreib die Quellen als Liste. Ein Eintrag der Form `Text | URL` wird zum
anklickbaren Link, alles ohne `|` bleibt einfacher Text.

```
quellen:
  - "eigene Erhebung an 60 Kursen, 28.07.2026"
  - "Betriebssatzung der vhs | https://vhs.frankfurt.de/de/special-pages/important/betriebssatzung"
```

Auf der Folie steht die URL nicht, nur der Text — anklickbar ist sie im PDF.
Das funktioniert, weil das PDF direkt aus dem HTML gedruckt wird und nicht aus
den Bildern besteht. Deshalb ist der Text darin auch durchsuchbar und für
Vorleseprogramme lesbar.

---

## Bilder ändern

Jede Folie kann ein Bild bekommen. Auf normalen Folien erscheint es als
quadratische Spalte rechts, der Text rückt automatisch nach links und wird
kompakter gesetzt. Auf `titel` und `schluss` liegt es vollflächig hinter dem
Petrol-Verlauf.

Du hast drei Möglichkeiten:

**Bild austauschen.** Leg eine eigene Datei in `bilder/` ab und ändere den Pfad
im Feld `bild`. Jedes gängige Format geht, quadratisch sieht am besten aus.
Beim nächsten Speichern ist es drin.

**Bild weglassen.** Zeile `bild:` löschen. Die Folie nutzt dann die volle
Breite und setzt den Text wieder größer.

**Neues Bild generieren lassen.** Ändere den Text in `bildprompt` und sag mir
Bescheid. Das Feld ist die Dokumentation dessen, was generiert wurde, damit
später nachvollziehbar bleibt, wie ein Bild zustande kam.

Fehlt eine Bilddatei, meldet der Build das als `! Bild fehlt: …` und baut die
Folie trotzdem, nur ohne Bild. Nichts geht kaputt.

Alle Bilder sind flach-geometrisch im Bauhaus-Stil gehalten und enthalten
bewusst **keine Schrift**. In einer Präsentation über Textqualität wären
erfundene Buchstaben im Bild ein Eigentor.

Erzeugt wurden sie in den vier Farben Petrol, Papier, Mint und Orange. Die
Originale liegen in `bilder/original-petrol/`; was in `bilder/` liegt, hat
`bilder/umfaerben.py` daraus auf die Palette aus `DESIGN.md` abgebildet. Wer
die Palette ändert, ändert die Zieltabelle im Skript mit und lässt es erneut
laufen — es färbt immer aus dem Original.

---

## Folientypen

### `titel` und `schluss`
Vollflächiges Petrol-Panel. Nutzt `titel`, `akzent`, `untertitel`, `fussl`, `fussr`.

### `punkte`
Aufzählung mit Balken. Ein Punkt kann zweiteilig sein:

```
punkte:
  - "**Befund** || Erklärender Satz darunter in grau."
  - Einfacher Punkt ohne Untertext.
```

### `zahlen`
Zwei bis vier große Kennzahlen nebeneinander.

```
zahlen:
  - "90 % || der Texte mit Befund || warn"
  - "5.800 || Veranstaltungen im Jahr"
```

Das dritte Feld `warn` färbt die Zahl orange. Weglassen für Petrol.

### `zweispalt`
Zwei Spalten mit Kopfzeile, gut für Gegenüberstellungen.

```
spalte1: DETERMINISTISCH
punkte1:
  - Erster Punkt
spalte2: URTEILEND
punkte2:
  - Erster Punkt
```

### `tabelle`

```
spalten: Kriterium | Stufe | verbindlich
zeilen:
  - "1.3.1 Struktur | A | + ja"
  - "3.1.4 Abkürzungen | AAA | ! nein"
```

`+` am Zellenanfang färbt petrol, `!` färbt orange. Reine Zahlen werden
automatisch hervorgehoben.

### `tabelle2`
Wie `tabelle`, aber mit einem zweiten Block darunter, gruppiert nach
Einstufung. Die Gruppe wechselt, sobald die erste Zelle gefüllt ist.

```
regelntitel: Die sechs Befundarten
regeln:
  - "PFLICHT | STRUKTUR | Überschrift, die keine ist"
  - "| LINKTEXT | sagt nicht, wohin der Link führt"
  - "EMPFEHLUNG | NIVEAU | Wort zu schwer für diese Zielgruppe"
```

Enthält die Stufe das Wort `PFLICHT`, wird die Gruppe rot markiert, sonst
gelbbraun. Die Stufe steht als Wort da und nicht nur als Farbe. Zwei Blöcke
plus Callout passen nicht auf eine Folie — im Zweifel den Callout weglassen.

### `zitat`
Großes Zitat mit Balken links. Felder `zitat` und `quelle`.

### `text`
Fließtext in Absätzen.

```
absaetze:
  - Erster Absatz.
  - Zweiter Absatz.
```

### `kapitel`
Trennfolie mit großer Nummer. Feld `nummer`.

---

## Wenn etwas schiefgeht

Das Build-Skript sagt dir die Zeilennummer und was es erwartet hat. Häufigste
Ursachen: ein Doppelpunkt im Wert ohne Anführungszeichen, oder eine Listenzeile
ohne vorangehenden `schlüssel:`.

Die Zeitschätzung rechnet mit 125 Wörtern pro Minute. Folien über 90 Sekunden
werden mit `!` markiert.
