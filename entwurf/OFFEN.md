# Offener Arbeitsstand — Gestaltung

Stand 29.07.2026. Diese Datei ist die Übergabe: Sie enthält, was entschieden,
aber noch nicht umgesetzt ist. Nach der Umsetzung kann sie gelöscht werden.

Punkt 1, 2, 3 und 5 sind am 29.07.2026 umgesetzt und stehen unten nur noch
als Protokoll. **Offen ist Punkt 4** — der Umbau der Werkzeugoberfläche — und
der inhaltliche Punkt am Ende.

---

## Was bereits im Code steht

- Schriften Atkinson Hyperlegible Next und IBM Plex Mono, selbst gehostet in
  `schriften/`, eingebunden in `stil.css`, `dokument.css`, `tool/index.html`
- Farbrollen statt Farbnamen, `pruefe-design.py` rechnet **29** Paare nach
- `DESIGN.md` mit Begründung, Skala, Regeln
- `entwurf/werkzeug.html` als klickbarer Entwurf der neuen Oberfläche
- die neutrale Palette samt Einstufungsfarben, überall (Punkt 1 und 2)
- die geschärfte Mono-Regel (Punkt 3)
- die auf die neue Palette umgefärbten Illustrationen (Punkt 5)

## Umgesetzt am 29.07.2026

### 1. Neutraler Grund statt Creme — überall ✓

Der warme Grund `#F7F5F0` wird durch ein kühles Neutral ersetzt. Gilt für
Folien, Dokument **und** Werkzeug; ausdrücklich so entschieden, damit Vortrag
und Vorführung nicht auseinanderfallen.

| Rolle | alt | neu |
|---|---|---|
| `--papier` | `#F7F5F0` | `#FFFFFF` (Karten, Folienfläche) |
| `--grund` (Seitengrund im Werkzeug) | — | `#F5F6F8` |
| `--flaeche` | `#E8E5DE` | `#EEF0F3` |
| `--linie` | `#D2CEC6` | `#E4E6EB` |
| `--rahmen` | `#8C867E` | `#848B96` |
| `--tinte` | `#15181C` | `#14171C` |
| `--leise` | `#42464C` | `#4C535E` |
| `--marke` | `#14459E` | bleibt |
| `--auf-marke` | `#B9DFFA` | bleibt |

Nachtrag aus der Umsetzung: Der Seitengrund heißt `--grund` und ist damit der
fünfte Neutralton — die Regel „keine neuen Grautöne" in `DESIGN.md` wurde
entsprechend nachgezogen. Weißes Papier braucht etwas, worauf es liegt.

Zweiter Nachtrag: **`--flaeche` trägt keinen Nebentext mehr.** `--leise` hielt
auf der creme Füllfläche 7,55:1, auf der neutralen nur noch 6,80:1. Drei
Stellen im Werkzeug wurden auf `--tinte` beziehungsweise `--grund` umgestellt
(Hinweis unter der Kurswahl, Merkmalsplaketten der Trefferliste, Schwebefläche
des kleinen Knopfes). Die Regel steht in `DESIGN.md`, das Paar wurde nicht
stillschweigend aus der Prüfung genommen.

### 2. Drei Einstufungsfarben statt einer Befundfarbe ✓

Der Prompt stuft in PFLICHT, EMPFEHLUNG, HINWEIS ein. Bisher gibt es nur
`--befund`. Neu:

| Rolle | Wert | Kontrast auf Weiß |
|---|---|---|
| `--pflicht` | `#A4162B` | 7,70:1 |
| `--empfehlung` | `#6E4600` | 8,27:1 |
| `--hinweis` | `#4C535E` | 7,76:1 |
| `--geprueft` | `#155739` | 8,56:1 |

Alle Werte gegen Weiß **und** gegen den Seitengrund `#F5F6F8` auf AAA geprüft;
`--empfehlung` musste dafür von `#7A4E00` nachgedunkelt werden. Die Paare
gehören in `pruefe-design.py` ergänzt, die Tabelle in `DESIGN.md` ersetzt.

Nachtrag: Die hier notierten 7,20:1 für `--empfehlung` sind der Wert der
verworfenen Fassung `#7A4E00`. `#6E4600` hält 8,27:1; die Tabelle oben ist
korrigiert. `--befund` ist ersatzlos entfallen — `--pflicht` ist jetzt das
einzige Rot und trägt deshalb auch Fehler- und Warnzustände der Oberfläche.

### 3. Mono-Regel schärfen ✓

Bisher in `DESIGN.md`: „Kursnummern, Prüfsummen, Messwerte, Code" in IBM Plex
Mono. Das war zu weit. Neu: **Mono nur in der Anzeige von Messwerten,
Prüfsummen und Zählern — nie in Eingabefeldern.** Im Formular stand die
Kursnummer in Mono neben dem Niveau in Atkinson; beides sind Kennungen, der
Wechsel fiel nur auf, ohne zu helfen.

Nachtrag: Umgestellt wurden das Prompt-Feld im Werkzeug und die Kursnummer in
der Trefferliste. Wörtlich wiedergegebener Maschinentext bleibt in Mono — die
Rohantwort des Modells und die Prompt-Auszüge im Dokument. Das ist in
`DESIGN.md` ausdrücklich festgehalten und geht insofern über den Wortlaut der
Entscheidung hinaus, die „Code" aus der Aufzählung gestrichen hatte.

### 4. Werkzeug umbauen — **offen**

Vorlage ist `entwurf/werkzeug.html`, Begründungen in `entwurf/README.md`.

- Zwei getrennte Ansichten statt eines Layouts mit leerer Ergebnisfläche
- Ergebniskopf: Urteil, dann Zielgruppe, dann Messwerte. Der Einschätzungssatz
  aus dem `GESAMT`-Block stand bisher **ganz unten**, nach Befundliste und
  Regelkürzeln
- Text mit markierten Fundstellen als Hauptfläche, gekoppelt an die Befunde
- `position:sticky` auf dem Textbereich, damit er beim Sprung zu einem späten
  Befund im Bild bleibt
- Unter 980 px erscheint der Befund unter dem Text statt am Seitenende
- Keine Versalien mehr; Regelkürzel als „Niveau", nicht „NIVEAU"
- Kein „Vorschlag übernehmen" — das Werkzeug zeigt nur an

Noch zu lösen: Ableitung der Markierungen aus den wörtlichen Zitaten des
Modells, Lade- und Fehlerzustand, eigener Scrollbereich für die Befundspalte
(derzeit ist der letzte Befund beim Sprung nicht vollständig im Bild).

### 5. Illustrationen erneut umfärben ✓

`bilder/umfaerben.py` bildet von der alten Petrol-Palette ab. Die Zieltabelle
`ABBILDUNG` muss auf die neuen Werte gehen. Das Skript färbt immer aus
`bilder/original-petrol/`, ein zweiter Lauf ist also gefahrlos.

Nachtrag: Das alte Bildpapier `#F4F1EA` geht auf `--grund` und nicht auf
`--papier`. Weiß ist bereits der letzte Anker der Tabelle; zwei Anker auf
demselben Ziel pressen die hellen Verläufe gegen die Obergrenze und erzeugen
genau die Stufen, die die Helligkeitsverschiebung im Skript vermeiden soll.
Alle 16 Bilder sind neu gefärbt.

### 6. Nach jeder Änderung messen ✓

```bash
python3 pruefe-design.py
python3 build.py && python3 dokument.py
cd abschlussprojekt-vhs && python3 -m http.server 8795
```

Dann `ausgabe/pruefung.html` und `ausgabe-dokument/pruefung.html` öffnen.
Der Schriftwechsel hat schon einmal alle Größen verschoben; der neue Grund
tut das nicht, aber geprüft werden muss es trotzdem.

Ergebnis vom 29.07.2026: 29 von 29 Paaren halten ihren Mindestwert, die drei
Dateien stimmen überein. Keine der 13 Folien läuft über, keine der 23
Dokumentseiten. Die knappste Seite ist 10 mit 17 px Rest, danach 23 mit 80 px.
Der neue Grund hat keine Größe verschoben.

---

## Inhaltlicher Punkt, der über die Gestaltung hinausgeht

**Die Kursleitungen sind eine zweite Nutzergruppe.** Der System-Prompt sagt
unter GRENZEN, die Entscheidung treffe die Programmbereichsleitung — das
regelt aber die Freigabe, nicht die Nutzung. Folie 9 führt die Kursleitungen
auf Honorarbasis unter „hoch betroffen, kein formaler Einfluss" und hält im
Callout fest, Beteiligung sei dort „das einzige verfügbare Instrument".

Ein Werkzeug, das die Kursleitungen **vor** dem Einreichen selbst benutzen
können, ist genau diese Beteiligung. Prüft nur die Programmbereichsleitung,
ist es eine Kontrollinstanz und erzeugt den Widerstand, den Folie 10
behandelt. Dasselbe Werkzeug, umgekehrtes Vorzeichen.

Zu entscheiden:

- ob die Kursleitungen in der Implementierungsplanung ausdrücklich als
  Nutzergruppe genannt werden (Folie 8 oder 9)
- ob `system-prompt.md` unter ROLLE erwähnen soll, dass die Prüfung auch vor
  dem Einreichen stattfinden kann. Das wäre eine neue Fassung mit Eintrag in
  `iterationen.md`
- Folge für die Oberfläche: Sie muss für Fachleute **und** für fachfremde
  Kursleitungen tragen. Regel dafür: Fachbegriff nennen und im selben Satz
  erklären — „Kompositum aus zwei Wörtern, die auf A2.2 beide noch nicht
  eingeführt sind"

---

## Was nicht angefasst werden soll

- `daten/` — Messgrundlage der Abgaben
- Protokolle der Kernfälle in `tool/protokoll/`. Ein neuer Lauf von `4074-74`
  oder `4213-40` ersetzt den Beispiellauf im Abgabe-PDF. Zum Ausprobieren
  gehören Läufe nach `tool/protokoll/pruefung-kursplan/`
- Die inhaltliche Aussage der Folien. Hier geht es um Schrift und Farbe
