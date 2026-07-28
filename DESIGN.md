# KLARTEXT — Gestaltungssystem

Verbindlich für alle drei Ausgaben des Projekts: die Präsentation
(`stil.css`), die System-Prompt-Dokumentation (`dokument.css`) und den
Prototyp (`tool/index.html`). Wer eine Farbe, eine Schriftgröße oder einen
Abstand ändert, ändert ihn hier mit — und lässt `pruefe-design.py` laufen.

---

## Der Gedanke dahinter

Die Arbeit behauptet, dass ein Text nicht an sich verständlich ist, sondern
nur für eine bestimmte Zielgruppe. Sie argumentiert außerdem, dass die
entscheidenden WCAG-Kriterien — 3.1.4 Abkürzungen und 3.1.5 Leseniveau —
Stufe AAA und damit **nicht verbindlich** sind, und stützt den Auftrag
stattdessen auf die Betriebssatzung.

Wer so argumentiert, steht unter Beobachtung: Ein Foliensatz, der die
freiwillige Stufe selbst reißt, entwertet das Argument. Deshalb hält dieses
System **AAA freiwillig ein** und weist es nach, statt es zu behaupten. Die
Gestaltung führt vor, was der Vortrag fordert.

Das ist zugleich die Antwort auf die Frage, warum hier nicht Helvetica steht.
Eine Schrift, die überall vorhanden ist, ist deshalb noch keine gute Wahl —
und Verfügbarkeit ist ohnehin kein Argument mehr, seit die Schriftdateien
mitgeliefert werden.

---

## Schrift

| Rolle | Familie | Schnitte |
|---|---|---|
| Alles außer Kennungen | Atkinson Hyperlegible Next | 400, 600, 700, dazu 400 und 700 kursiv |
| Kursnummern, Prüfsummen, Messwerte, Code | IBM Plex Mono | 400, 600 |

**Warum Atkinson Hyperlegible Next.** Entworfen im Auftrag des Braille
Institute mit dem erklärten Ziel, Buchstaben auch dann unterscheidbar zu
halten, wenn das Sehvermögen nachlässt: offene Punzen, deutlich verschiedene
Formen für Zeichen, die sich sonst ähneln, und eine geschlitzte Null. Für ein
Projekt über Verständlichkeit ist das keine Dekoration, sondern dasselbe
Argument eine Ebene tiefer.

**Die geschlitzte Null ist Absicht.** `0` und `O` sind dadurch nicht zu
verwechseln — bei Kursnummern wie `4074-74` der eigentliche Zweck. Sie fällt
im Fließtext auf. Das ist der Preis und er ist bewusst bezahlt.

**Warum IBM Plex Mono daneben.** Kursnummern, Prüfsummen und Messwerte sind
keine Wörter. Sie stehen untereinander und werden verglichen, nicht gelesen.
Eine Schreibmaschinenschrift markiert diesen Unterschied und hält die Ziffern
auf gleicher Breite.

### Einbindung

Beide Familien liegen als `.woff2` in `schriften/` und werden über
`schriften/schriften.css` eingebunden — **nicht** über das Google-CDN. Drei
Gründe, in dieser Reihenfolge:

1. Ein CDN-Abruf übermittelt die IP-Adresse jeder lesenden Person an einen
   Dritten. Für einen städtischen Eigenbetrieb ist das der springende Punkt,
   nicht eine Formalie.
2. Die Ausgaben müssen ohne Netz bauen und laufen.
3. Damit ist die Frage nach Windows und Mac erledigt: Es wird nichts
   vorausgesetzt, was auf dem Zielrechner installiert sein müsste.

Drei Festlegungen in `schriften/schriften.css`, die nicht geändert werden
sollten:

- **`font-display:block`**, nicht `swap`. `build.py` schießt die Folie als
  PNG, sobald die Seite steht. Bei `swap` könnte der Schuss den Fallback
  erwischen und eine einzelne Folie in Helvetica ins PDF wandern.
- **Kein `local()` im `src`.** Sonst zöge eine auf dem Rechner installierte
  Fassung die mitgelieferte Datei vor, und das Ergebnis hinge davon ab, wer
  baut.
- **`unicode-range` bleibt stehen.** Der Browser lädt dadurch nur die
  Zeichensätze, die eine Seite wirklich braucht — im Prototyp vier Dateien
  statt vierzehn.

### Zur Präsentation im Besonderen

`build.py` rendert jede Folie als PNG und legt die Bilder in PPTX und PDF ab.
**In der abgegebenen Präsentation steckt kein Buchstabe als Text.** Sie sieht
auf jedem fremden Rechner pixelgenau gleich aus, unabhängig von installierten
Schriften. Die Schriftwahl ist damit eine reine Gestaltungsfrage und keine
Kompatibilitätsfrage — der Grund, warum hier überhaupt frei gewählt werden
konnte.

Das gilt nicht für den Prototyp: Der läuft live im Browser und braucht die
mitgelieferten Dateien.

---

## Größen

Atkinson läuft breiter als Helvetica Neue und hat eine größere x-Höhe.
Derselbe Text braucht deshalb mehr Platz. Beim Wechsel wurde alles ab 14px um
sieben Prozent zurückgenommen; Beschriftungen darunter blieben, die sind
ohnehin knapp.

### Folien (`stil.css`, Bühne 1280 × 720)

| Element | Größe | Verwendung |
|---|---|---|
| `.panel h1` | 69px / 700 | Titel- und Schlussfolie |
| `.kapnum` | 182,5px / 700 | Kapitelziffer |
| `h1` | 50px / 700 | Folienüberschrift |
| `h1.klein` | 41px / 700 | Überschrift bei viel Inhalt |
| `.znum` | 82px / 700 | Kennzahl |
| `.zitat .q` | 29px / 700 | Zitat |
| `.pkt .ptxt` | 18,5px / 400 | Aufzählungspunkt |
| `.callout` | 17,5px / 700 | Merksatzbalken |
| `.lede` | 16px / 400 | Vorspann |
| `td`, `.sp li` | 15,5px / 400 | Tabelle, Spaltenliste |
| `th` | 11px / 700 | Tabellenkopf, Versalien, 2px gesperrt |
| `.foot` | 10,5px / 400 | Fußzeile, Versalien |

**Zeichenabstand.** Die negativen Werte wurden gelockert (Folienüberschrift
von −1,4px auf −0,8px, Titelfolie von −2,2px auf −1,4px). Atkinson ist auf
offene Abstände hin entworfen; enges Tracking arbeitet gegen genau die
Eigenschaft, wegen der die Schrift gewählt wurde.

**Ziffern in Tabellen und Kennzahlen stehen auf `tabular-nums`**, damit
Messwerte untereinander bündig sind.

### Dokument (`dokument.css`, A4 als 794 × 1123)

Unverändert gegenüber der Vorfassung: Fließtext 11,5px, `.eng` 10,6px für
volle Seiten. Nach dem Schriftwechsel gemessen — alle 23 Seiten passen ohne
Eingriff.

### Feste Höhen messen, nicht schätzen

Folien sind 1280 × 720, Dokumentseiten A4. Läuft Inhalt über, sieht man das
im HTML nicht, sondern erst auf dem Beamer. Nach jeder Änderung an Größen
oder Abständen:

```bash
cd abschlussprojekt-vhs && python3 -m http.server 8795
```

Dann `ausgabe/pruefung.html` und `ausgabe-dokument/pruefung.html` öffnen.

---

## Farbe

Die Namen bezeichnen **Rollen, keine Farben**. `--befund` ist rot, weil
Beanstandungen rot sind — nicht umgekehrt. Wer eine Rolle braucht, die es
nicht gibt, legt sie hier an, statt einen Wert danebenzuschreiben.

| Rolle | Wert | Verwendung |
|---|---|---|
| `--papier` | `#F7F5F0` | Grundfläche |
| `--flaeche` | `#E8E5DE` | ruhige Füllung: Quadranten, Befundkarte, Bildkasten |
| `--linie` | `#D2CEC6` | dekorative Trennstriche, **nie Text, nie Bedienelement** |
| `--rahmen` | `#8C867E` | Rahmen von Eingabefeldern und Knöpfen |
| `--tinte` | `#15181C` | Fließtext |
| `--leise` | `#42464C` | Nebentext, Beschriftungen, Quellenzeile |
| `--marke` | `#14459E` | Markenflächen, Auszeichnung, Aktion |
| `--marke-dunkel` | `#0E3378` | gedrückter Knopf, Text auf `--auf-marke` |
| `--auf-marke` | `#B9DFFA` | einzige Akzentfarbe **auf** Markenfläche |
| `--befund` | `#8F1829` | Beanstandung |
| `--geprueft` | `#155739` | ohne Beanstandung |

### Warum `--auf-marke` getrennt geführt wird

Eine Farbe, die auf Papier AAA hält, kann auf der dunklen Titelfläche
unlesbar sein. Beim Entwurf stand dort zuerst das Grün von `--geprueft` auf
dem Markenblau: **1,03:1**, praktisch unsichtbar. Deshalb hat die dunkle
Fläche eine eigene Akzentfarbe, und sie ist bewusst **kein Signalton** —
Rot und Grün sind mit Bedeutung belegt und dürfen nicht als Schmuck auf einer
Titelfolie auftauchen.

`--auf-marke` gilt für die Titelüberschrift bei 69px/700 und für Zierlinien.
Für Fließtext auf Markenfläche gilt Weiß.

### Was das Skript nachrechnet

`pruefe-design.py` liest die Werte aus `stil.css` und prüft jedes Paar, das im
Entwurf tatsächlich vorkommt:

| Vordergrund | Grund | Ist | Soll |
|---|---|---:|---:|
| `--tinte` | `--papier` | 16,34:1 | 7,0 |
| `--leise` | `--papier` | 8,71:1 | 7,0 |
| `--marke` | `--papier` | 8,12:1 | 7,0 |
| `--befund` | `--papier` | 8,27:1 | 7,0 |
| `--geprueft` | `--papier` | 7,85:1 | 7,0 |
| `--tinte` | `--flaeche` | 14,16:1 | 7,0 |
| `--leise` | `--flaeche` | 7,55:1 | 7,0 |
| `--befund` | `--flaeche` | 7,16:1 | 7,0 |
| Weiß | `--marke` | 8,84:1 | 7,0 |
| Weiß | `--marke-dunkel` | 11,91:1 | 7,0 |
| Weiß | `--befund` | 9,01:1 | 7,0 |
| Weiß | `--geprueft` | 8,56:1 | 7,0 |
| `--auf-marke` | `--marke` | 6,32:1 | 4,5 |
| `--marke-dunkel` | `--auf-marke` | 8,51:1 | 7,0 |
| `--rahmen` | `--papier` | 3,31:1 | 3,0 |

7,0 ist AAA für Fließtext, 4,5 ist AAA für großen Text (ab 24px, fett ab
18,66px), 3,0 ist die Anforderung an Bedienelemente aus WCAG 1.4.11.

Das Skript prüft zusätzlich, ob `dokument.css` und `tool/index.html`
dieselben Werte führen. Driften sie auseinander, sieht man das sonst erst im
fertigen PDF.

```bash
cd abschlussprojekt-vhs && python3 pruefe-design.py
```

---

## Regeln

**Bedeutung hängt nie allein an der Farbe.** WCAG 1.4.1 ist Stufe A und damit
verbindlich — anders als die Kriterien, um die es im Vortrag geht. In
Tabellen bleibt deshalb das führende `+` beziehungsweise `!` vor dem Text
stehen; die Einfärbung kommt hinzu, sie ersetzt nichts. Wer eine neue
Auszeichnung einführt, gibt ihr ein Zeichen, ein Wort oder eine Form.

**`--linie` ist nie ein Bedienelement.** Der Wert hält 1,44:1 und ist für
Tabellenstriche gedacht, die keine Information tragen. Alles, was man
anklicken oder beschreiben kann, bekommt `--rahmen`.

**Auf Markenfläche gilt Weiß oder `--auf-marke`, sonst nichts.** Keine
Signalfarbe auf Blau.

**Keine neuen Grautöne.** Es gibt `--linie`, `--rahmen`, `--leise`,
`--flaeche`. Wer einen fünften braucht, braucht in Wirklichkeit einen der
vier.

**Die Bilder gehören zur Palette.** `bilder/*.jpg` sind flach-geometrisch und
auf genau diese Farben abgebildet. Ein neues Bild in anderen Farben bricht
den Foliensatz sichtbar. `bilder/umfaerben.py` bildet von der alten
Petrol-Palette ab und legt die Originale in `bilder/original-petrol/`; das
Skript färbt immer aus dem Original, nie aus dem Ergebnis.

**Farbwerte stehen an einer Stelle.** `stil.css` ist die Quelle,
`pruefe-design.py` liest von dort. Deckkraftvarianten bekommen eine eigene
Variable (`--marke-90`, `--marke-62`, `--auf-marke-50`), damit kein Farbwert
zweimal gepflegt werden muss.

---

## Herkunft und Lizenz

Beide Familien stehen unter der **SIL Open Font License 1.1**. Die Lizenz
erlaubt Weitergabe und Einbettung ausdrücklich und verlangt, dass Copyright
und Lizenztext mitgeliefert werden. Beide liegen in `schriften/`:

| Familie | Urheber | Lizenztext |
|---|---|---|
| Atkinson Hyperlegible Next | Braille Institute of America | `schriften/OFL-Atkinson-Hyperlegible-Next.txt` |
| IBM Plex Mono | IBM Corp. | `schriften/OFL-IBM-Plex-Mono.txt` |

Die Schriftdateien wurden aus dem Google-Fonts-Bestand bezogen und auf die
Zeichensätze `latin` und `latin-ext` beschränkt: 14 Schnitte, 306 kB.

---

## Was hier nicht steht

Dieses Dokument regelt Schrift, Farbe und Größen. Es regelt **nicht**, was
auf einer Folie steht, wie viele Folien es gibt oder wie lange gesprochen
wird — das steht in `CLAUDE.md` und ergibt sich aus der Aufgabenstellung.

Es enthält auch keine Komponentenbibliothek. Die Folientypen sind in
`README-FOLIEN.md` beschrieben und in `build.py` umgesetzt; dieses Dokument
sagt nur, wie sie aussehen.
