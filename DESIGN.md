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
| Alles, was gelesen oder geschrieben wird | Atkinson Hyperlegible Next | 400, 600, 700, dazu 400 und 700 kursiv |
| Angezeigte Messwerte, Prüfsummen, Zähler und wörtlich wiedergegebener Maschinentext | IBM Plex Mono | 400, 600 |

**Warum Atkinson Hyperlegible Next.** Entworfen im Auftrag des Braille
Institute mit dem erklärten Ziel, Buchstaben auch dann unterscheidbar zu
halten, wenn das Sehvermögen nachlässt: offene Punzen, deutlich verschiedene
Formen für Zeichen, die sich sonst ähneln, und eine geschlitzte Null. Für ein
Projekt über Verständlichkeit ist das keine Dekoration, sondern dasselbe
Argument eine Ebene tiefer.

**Die geschlitzte Null ist Absicht.** `0` und `O` sind dadurch nicht zu
verwechseln — bei Kursnummern wie `4074-74` der eigentliche Zweck. Sie fällt
im Fließtext auf. Das ist der Preis und er ist bewusst bezahlt.

**Warum IBM Plex Mono daneben.** Prüfsummen, Messwerte und Zähler sind keine
Wörter. Sie stehen untereinander und werden verglichen, nicht gelesen. Eine
Schreibmaschinenschrift markiert diesen Unterschied und hält die Ziffern auf
gleicher Breite.

**Mono ist eine Anzeigeschrift und keine Eingabeschrift.** Eingabefelder
laufen immer in Atkinson — auch das Feld, in dem der System-Prompt steht. Der
Prompt ist deutscher Fließtext, kein Quelltext; er wird geschrieben, nicht
verglichen.

**Kennungen sind keine Messwerte.** Die Kursnummer stand einmal in Mono neben
dem Niveau in Atkinson. Beides sind Kennungen; der Schriftwechsel markierte
einen Unterschied, den es nicht gibt. Er fiel auf, ohne zu helfen. Kursnummern
laufen deshalb im Fließtext, in Listen und in Feldern in Atkinson mit — die
geschlitzte Null hält `4074-74` ohnehin eindeutig.

Mono bleibt damit an drei Stellen: gemessene Zahlen (`.parwert`, Zeichen- und
Trefferzähler), Prüfsummen — und wörtlich wiedergegebener Maschinentext, also
die Rohantwort des Modells im Werkzeug und die Prompt-Auszüge im Dokument.

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

### Versalien nur auf der Folie, nicht im Werkzeug

Auf den Folien tragen `th` und `.foot` Versalien mit gesperrtem Zeichenabstand.
Das sind kurze Etiketten, die aus zwei Metern Entfernung erkannt und nicht
gelesen werden.

Im Werkzeug ist **`text-transform:uppercase` ersatzlos entfallen.** Es stand
dort auf jeder Beschriftung, jedem Knopf, jeder Plakette und jeder Stufe. Ein
Text, der neben einem Prüfbericht über Verständlichkeit steht, sollte nicht
selbst die Wortbilder zerstören: Versalien nehmen der Schrift die Ober- und
Unterlängen, an denen das Auge Wörter erkennt — genau die Eigenschaft, wegen
der Atkinson gewählt wurde. Bei einer Oberfläche, die auch fachfremde
Kursleitungen bedienen sollen, wiegt das schwerer als die Anmutung.

**Der Projektname bleibt KLARTEXT.** Er ist als Name in Versalien geschrieben
und nicht per `text-transform` erzeugt. Die Sperrung von 4px ist auf 0,5px
zurückgenommen; weites Tracking arbeitet gegen Atkinson.

**Regelkürzel und Stufen erscheinen als Wörter.** Das Modell antwortet mit
`NIVEAU`, `AMTSDEUTSCH`, `PFLICHT` — die Oberfläche zeigt „Niveau",
„Amtsdeutsch", „Pflicht". Die Übersetzung steht als Tabelle in
`tool/index.html`. Wörtlich wiedergegebene Modellantwort bleibt davon
unberührt: Was im Einschätzungssatz des Modells steht, wird nicht umgeschrieben.

### Drei Stricharten für drei Stufen

Die Fundstellen im geprüften Text sind unterstrichen: PFLICHT durchgezogen,
EMPFEHLUNG gestrichelt, HINWEIS gepunktet. Die Farbe kommt hinzu, sie trägt
nicht allein — WCAG 1.4.1 ist Stufe A und damit verbindlich. Zusätzlich hängt
an jeder Markierung die Befundnummer, und im Befund daneben steht die Stufe
als Wort.

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

Die Namen bezeichnen **Rollen, keine Farben**. `--pflicht` ist rot, weil
Beanstandungen rot sind — nicht umgekehrt. Wer eine Rolle braucht, die es
nicht gibt, legt sie hier an, statt einen Wert danebenzuschreiben.

| Rolle | Wert | Verwendung |
|---|---|---|
| `--papier` | `#FFFFFF` | Folienfläche, Karten und Felder im Werkzeug |
| `--grund` | `#F5F6F8` | Seitengrund hinter den Karten, **nur im Werkzeug** |
| `--flaeche` | `#EEF0F3` | ruhige Füllung: Quadranten, Zeitleiste, Bildkasten |
| `--linie` | `#E4E6EB` | dekorative Trennstriche, **nie Text, nie Bedienelement** |
| `--rahmen` | `#848B96` | Rahmen von Eingabefeldern und Knöpfen |
| `--tinte` | `#14171C` | Fließtext |
| `--leise` | `#4C535E` | Nebentext, Beschriftungen, Quellenzeile |
| `--marke` | `#14459E` | Markenflächen, Auszeichnung, Aktion |
| `--marke-dunkel` | `#0E3378` | gedrückter Knopf, Text auf `--auf-marke` |
| `--auf-marke` | `#B9DFFA` | einzige Akzentfarbe **auf** Markenfläche |
| `--pflicht` | `#A4162B` | Befund der Stufe PFLICHT |
| `--empfehlung` | `#6E4600` | Befund der Stufe EMPFEHLUNG |
| `--hinweis` | `#4C535E` | Befund der Stufe HINWEIS |
| `--geprueft` | `#155739` | ohne Beanstandung |

### Warum der Grund neutral ist und nicht creme

Der warme Grund `#F7F5F0` sah auf Papier gut aus und im Werkzeug nach Papier,
das keines ist. Ein Prüfwerkzeug, das neben dem Kursportal im Browser steht,
soll nicht so tun, als läge dort ein Bogen. Entscheidend war aber, dass die
Entscheidung **für alle drei Ausgaben zugleich** fällt: Im Vortrag folgt der
Vorführung des Werkzeugs unmittelbar die nächste Folie. Zwei Grundtöne in
derselben Viertelstunde fallen auf und wirken wie ein Versehen.

Die Folie ist damit weiß. Das Werkzeug setzt seine Karten und Felder in Weiß
auf `--grund` — die einzige Stelle, an der zwei helle Töne gebraucht werden,
weil dort Flächen übereinanderliegen. Eine Folie hat nichts, worauf sie liegen
könnte, und braucht den zweiten Ton nicht.

### Drei Stufen statt einer Befundfarbe

Der Prompt stuft jeden Befund als PFLICHT, EMPFEHLUNG oder HINWEIS ein; die
Zuordnung trifft die Regeltabelle in `tool/server.py`, nicht das Modell. Eine
einzige Befundfarbe warf alle drei in denselben Topf und zwang die Oberfläche,
die Stufe allein über das Wort zu tragen.

`--hinweis` trägt **absichtlich denselben Wert wie `--leise`**. Die schwächste
Stufe ist kein Signal, sondern eine Randbemerkung; sie bekommt die Farbe des
Nebentexts, nicht eine dritte Warnfarbe. Doppelt gepflegt wird der Wert
trotzdem nicht — es sind zwei Rollen, die derselbe Ton bedient, und das Skript
rechnet beide nach.

`--pflicht` ist das **einzige Rot im System**. Fehlermeldungen, der Warnbalken
bei abweichendem Prompt und der Vorbehalt bei fehlender Wortliste laufen
deshalb ebenfalls darauf. Das ist bewusst so entschieden: Ein zweites Rot
daneben wäre nicht unterscheidbar, aber es behauptete einen Unterschied.

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
| `--tinte` | `--papier` | 17,96:1 | 7,0 |
| `--leise` | `--papier` | 7,76:1 | 7,0 |
| `--marke` | `--papier` | 8,84:1 | 7,0 |
| `--pflicht` | `--papier` | 7,70:1 | 7,0 |
| `--empfehlung` | `--papier` | 8,27:1 | 7,0 |
| `--hinweis` | `--papier` | 7,76:1 | 7,0 |
| `--geprueft` | `--papier` | 8,56:1 | 7,0 |
| `--tinte` | `--grund` | 16,61:1 | 7,0 |
| `--leise` | `--grund` | 7,18:1 | 7,0 |
| `--marke` | `--grund` | 8,18:1 | 7,0 |
| `--pflicht` | `--grund` | 7,12:1 | 7,0 |
| `--empfehlung` | `--grund` | 7,65:1 | 7,0 |
| `--hinweis` | `--grund` | 7,18:1 | 7,0 |
| `--geprueft` | `--grund` | 7,91:1 | 7,0 |
| `--tinte` | `--flaeche` | 15,73:1 | 7,0 |
| `--marke` | `--flaeche` | 7,75:1 | 7,0 |
| `--marke-dunkel` | `--flaeche` | 10,43:1 | 7,0 |
| Weiß | `--marke` | 8,84:1 | 7,0 |
| Weiß | `--marke-dunkel` | 11,91:1 | 7,0 |
| Weiß | `--pflicht` | 7,70:1 | 7,0 |
| Weiß | `--empfehlung` | 8,27:1 | 7,0 |
| Weiß | `--hinweis` | 7,76:1 | 7,0 |
| Weiß | `--geprueft` | 8,56:1 | 7,0 |
| `--auf-marke` | `--marke` | 6,32:1 | 4,5 |
| `--marke-dunkel` | `--auf-marke` | 8,51:1 | 7,0 |
| `--tinte` | `--auf-marke` | 12,83:1 | 7,0 |
| `--rahmen` | `--papier` | 3,43:1 | 3,0 |
| `--rahmen` | `--grund` | 3,18:1 | 3,0 |
| `--rahmen` | `--flaeche` | 3,01:1 | 3,0 |

7,0 ist AAA für Fließtext, 4,5 ist AAA für großen Text (ab 24px, fett ab
18,66px), 3,0 ist die Anforderung an Bedienelemente aus WCAG 1.4.11.

**`--rahmen` auf `--flaeche` hält 3,01:1.** Das ist kein Spielraum, sondern
der Rand. Wer an `--rahmen` oder `--flaeche` auch nur eine Stufe dreht, reißt
dieses Paar — deshalb steht es in der Liste, obwohl derzeit kein
Bedienelement auf einer Füllfläche sitzt.

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

**`--linie` ist nie ein Bedienelement und nie Text.** Der Wert hält 1,25:1 und
ist für Striche gedacht, die keine Information tragen. Alles, was man
anklicken oder beschreiben kann, bekommt `--rahmen`; alles, was man lesen
soll, mindestens `--leise`.

**Auf `--flaeche` steht `--tinte`.** Solange das Papier creme war, hielt
`--leise` dort 7,55:1. Auf dem neutralen System sind es 6,80:1, und damit ist
die Füllfläche für Nebentext verbraucht. Sie trägt weiterhin `--tinte`,
`--marke` und `--marke-dunkel` — Beschriftungen in `--leise` gehören auf
`--papier` oder `--grund`. Das betraf drei Stellen im Werkzeug: den Hinweis
unter der Kurswahl, die Merkmalsplaketten in der Trefferliste und die
Schwebefläche des kleinen Knopfes.

**Auf Markenfläche gilt Weiß oder `--auf-marke`, sonst nichts.** Keine
Signalfarbe auf Blau.

**Keine neuen Grautöne.** Es gibt `--linie`, `--rahmen`, `--leise`,
`--flaeche` und `--grund`. Der fünfte kam mit dem weißen Papier hinzu und ist
begründet: Karten brauchen etwas, worauf sie liegen. Wer einen sechsten
braucht, braucht in Wirklichkeit einen der fünf.

**Die Bilder gehören zur Palette.** `bilder/*.jpg` sind flach-geometrisch und
auf genau diese Farben abgebildet. Ein neues Bild in anderen Farben bricht
den Foliensatz sichtbar. `bilder/umfaerben.py` bildet von der alten
Petrol-Palette ab und legt die Originale in `bilder/original-petrol/`; das
Skript färbt immer aus dem Original, nie aus dem Ergebnis. Ein zweiter Lauf
ist deshalb gefahrlos, und genau den brauchte der Wechsel auf die neutrale
Palette.

Das alte Bildpapier `#F4F1EA` geht dabei auf `--grund` und **nicht** auf
`--papier`. Weiß ist bereits der letzte Anker der Tabelle; beide Anker auf
denselben Wert zu legen presst die hellen Verläufe gegen die Obergrenze und
erzeugt sichtbare Stufen — dieselben, die das Skript mit seiner
Helligkeitsverschiebung gerade vermeidet.

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
