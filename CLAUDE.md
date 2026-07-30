# KLARTEXT — Betriebsanleitung

Die Rahmung des Projekts steht in der `CLAUDE.md` im übergeordneten Ordner und
wird von dort mitgeladen. Hier steht, wie man damit arbeitet, ohne etwas
kaputtzumachen.

Alle Pfade in dieser Datei sind relativ zu `abschlussprojekt-vhs/`. Shell-Befehle
gehen vom übergeordneten Ordner als Arbeitsverzeichnis aus.

---

## Woraus die Arbeit besteht

Die Aufgabenstellung schreibt Struktur, Folienzahl und Pflichtinhalte ungefähr vor. Vier Phasen:

### 1. Executive Summary (1-2 Slides)
- Kurze, prägnante Zusammenfassung des Gesamtkonzepts
- Enthält: Ausgangssituation, Kernziele, erwartete Ergebnisse und wichtigste Maßnahmen
- Ziel: Entscheider sollen in 2-3 Minuten die wichtigsten Punkte erfassen können

### 2. Unternehmensanalyse & Potentiale (2-3 Slides)
- Vorstellung des ausgewählten Unternehmens
- Analyse des IST-Zustands
- Identifizierte Optimierungspotenziale
- Quantifizierung der erwarteten Verbesserungen

### 3. System Prompt & technische Implementation (3-4 Slides)
- Vorstellung des ausgewählten Prozesses
- Detaillierte Darstellung des entwickelten System Prompts
- Technische Voraussetzungen
- Implementierungsschritte

### 4. Change Management Konzept (3-4 Slides)
- Stakeholder-Matrix (Einfluss-Betroffenheit)
- integrierte Timeline (Monat 1-3, Technische Implementation: Setup, Pilot, Rollout / Kommunikation: Ankündigung, Training, Support / Change: Vorbereitung, Einbindung, Begleitung)

### 5. Zeitplan & nächste Schritte (1-2 Slides)
- Konkrete erste Schritte für die nächsten 30 Tage
- Ressourcenplanung
- Erfolgsmessung und K

---

## Die inhaltliche Kernthese

Ein Text ist nie an sich verständlich, sondern nur für bestimmte Leser. Lesbarkeitsindizes übersehen das: Sie beanstanden den Englischkurs und winken den Deutschkurs auf A2 durch. Der Prompt klärt erst die Zielgruppe, dann den Maßstab. Belegt an zwei Kursen über je vier Läufe: beim Deutschkurs jedes Mal mehrere Niveau-Befunde, beim Englischkurs jedes Mal keiner.

**Keine feste Zahl behaupten.** Die Zahl schwankt (aktuell 11 bis 12), die Asymmetrie nicht. Wer „sieben gegen null“ schreibt, behauptet eine Messung, die ein einzelner Lauf war — genau daran ist die Abgabe schon einmal fast gescheitert, siehe `iterationen.md`, v8.

Verpflichtet ist die vhs dazu nicht — die maßgeblichen WCAG-Kriterien sind AAA. Das Argument liefert die Betriebssatzung: Angebote „für alle, ohne Rücksicht auf Vorbildung“.

## Welcher Maßstab gilt

Das ist eine **Kursabgabe, keine Verteidigung.** Es gibt kein Kolloquium, in dem
einzelne Zahlen angegriffen werden. Maßstab ist deshalb **innere Konsistenz**,
nicht die Beweisbarkeit jeder einzelnen Angabe.

Eine Zahl darf auf einer begründeten Annahme beruhen. Zu melden ist, wenn zwei
Folien einander widersprechen — oder wenn eine Folie etwas als „gemessen"
ausweist, das nirgends hergeleitet ist. Nicht zu melden ist die bloße
Abwesenheit eines Belegs.

## Der wichtigste Grundsatz der Umsetzung

**Was feststeht, gehört in den Code. Was die Zielgruppe kennen muss, bleibt
beim Modell.**

Das ist zugleich die Change-Argumentation, und die Trennlinie verläuft nicht
zwischen Technik und Sprache, sondern zwischen der Seite und dem einzelnen
Text: Das Seitengerüst — Kontraste, Tastaturbedienung, Navigation — ist
prüfbar, ohne einen einzigen Kurs zu kennen, und bleibt bei den Prüfwerkzeugen
der städtischen IT. Die KI übernimmt allein den Schritt, für den man wissen
muss, wer den Text liest, und der liegt bei den Programmbereichen.

Nicht nach der Methode trennen: Auch etablierte Prüfwerkzeuge setzen inzwischen
KI ein (Deque axe: Axe Assistant, Guided Tests). „Deterministisch gegen KI"
trägt als Abgrenzung deshalb nicht mehr, „ohne Kenntnis des Kurses entscheidbar
oder nicht" schon.

Das ist dreimal beim Bauen passiert (siehe `iterationen.md`, v4, v5 und v9):
Zusagen im Prompt hielt das Modell nicht zuverlässig ein, heute stehen sie in
`tool/server.py` — Ehrlichkeitsvorbehalt, Einstufung, Namensschutz.
Regel daraus: Ist eine neue Anforderung im Kern eine Nachschlagetabelle oder
ein prüfbarer Zustand, schreib sie nicht in den Prompt.

Sechs Prüfregeln, zwei Stufen: `STRUKTUR` und `LINKTEXT` sind PFLICHT,
`NIVEAU`, `AMTSDEUTSCH`, `SATZ` und `ABK` sind EMPFEHLUNG. Fünf weitere
Befundarten wurden in v7 gestrichen; die Begründung je Regel steht dort.

---

## Was man hier leicht falsch macht

**`folien.md` ist die einzige Quelle der Präsentation.** PPTX und PDF werden
von `build.py` erzeugt. Änderungen direkt in der PowerPoint sind beim nächsten
Build weg. Dasselbe gilt für `dokumentation.md` und `dokument.py`.

**`build.py` committet selbst.** Nach einem Build meldet git „nothing to
commit" — das ist normal, nicht ein Zeichen dafür, dass nichts passiert ist.
Für eine erklärende Commit-Notiz `git commit --allow-empty` verwenden.

**Feste Seitenhöhen schneiden stillschweigend ab.** Folien sind 1280×720,
Dokumentseiten A4. Läuft Inhalt über, sieht man das im HTML nicht, sondern erst
auf dem Beamer. Deshalb nach jeder inhaltlichen Änderung messen, nicht
schätzen:

```bash
cd abschlussprojekt-vhs && python3 -m http.server 8795
```

Dann `ausgabe/pruefung.html` (Folien) beziehungsweise
`ausgabe-dokument/pruefung.html` (Dokument) im Browser öffnen. Beide messen je
Seite die Unterkante des Inhalts gegen den verfügbaren Platz. So wurde
gefunden, dass Folie 5 einmal 185 Pixel überlief und ihr Callout unsichtbar
war.

**Die Prüfseite im Browser zeigt altes CSS.** `ausgabe/pruefung.html` lädt die
Folien in iframes, und die laden `../stil.css` ohne Cache-Buster. Nach einer
Änderung an `stil.css` meldet die Seite deshalb weiter die alten Werte — auch
nach einem Reload der Prüfseite selbst. Das kostet sonst eine Stunde Suche nach
einem Überlauf, den es nicht gibt. Zuverlässig misst nur ein frischer Chrome:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --disable-gpu --virtual-time-budget=15000 --window-size=900,900 \
  --screenshot=/tmp/pruef.png http://localhost:8795/ausgabe/pruefung.html
```

**Die Abgabe-2-Doku zieht ihre Inhalte zur Bauzeit.** `dokumentation.md`
enthält Platzhalter: `{{PROMPT:GRENZEN}}` holt einen Prompt-Abschnitt
(`{{PROMPT:KONTEXT:von:bis}}` schneidet an den `###`-Überschriften zu),
`{{FASSUNG}}` das Feld `**Fassung:**`, `{{ITER_TABELLE}}` die Fassungshistorie
als Tabelle — Datum aus den Überschriften von `iterationen.md`, Kurztext aus
`ITERATION_KURZTEXTE` in `tool/server.py`, derselben Liste, die auch das Panel
zeigt. Prompt-Abschnitte, Fassungsnummer und Historie niemals hineinkopieren,
sonst driftet das PDF vom Prompt weg; genau das war passiert, als das
Titelblatt v9 nannte und der Prompt bei v11 stand.

**Beispielläufe stehen nicht im PDF, sondern im Werkzeug.** Das Dokument
verweist dafür auf `klartext-vhs.henrikheil.net`. `{{ITER:v4}}` und
`{{PROTOKOLL:4074-74:antwort}}` beherrscht `dokument.py` weiterhin, benutzt
werden sie nicht mehr. Wer `{{PROTOKOLL:...}}` wieder einbaut, holt sich das
alte Problem zurück: Der Platzhalter nimmt das **jüngste** Protokoll dieser
Kursnummer, ein Probelauf ersetzt also den Beispiellauf der Abgabe. Läufe, die
nichts in der Abgabe zu suchen haben, gehören ohnehin nach
`tool/protokoll/pruefung-kursplan/`; der Unterordner wird nicht durchsucht.

**Farben und Schriften stehen in `DESIGN.md`, nicht im Ermessen.** Die Werte
liegen deckungsgleich in `stil.css`, `dokument.css` und `tool/index.html`.
Nach jeder Änderung daran `python3 pruefe-design.py` — das Skript rechnet alle
Kontrastpaare nach und meldet, wenn die drei Dateien auseinanderdriften. Das
System hält WCAG AAA freiwillig ein.

**Das Panel zeigt alle Iterationen des Prompts — im Hosting aus einer Datei.**
Die Auswahlliste zieht die Prompt-Stände aus `git show`. Auf Railway liegt
kein `.git` (846 MB, in `.railwayignore`), dort liest `server.py` stattdessen
`tool/iterationen-staende.json`. Diese Datei wird nicht automatisch
mitgeschrieben. Nach jedem Commit an `system-prompt.md` und vor jedem Deploy:

```bash
cd abschlussprojekt-vhs && python3 tool/iterationen-export.py
```

Bleibt das aus, ist im Hosting die neue Iteration nicht wählbar — lokal fällt
es nicht auf, weil dort Git greift.

**Das Dokumente-Modal liefert die echten Abgaben aus,** nicht Kopien:
`ausgabe/Praesentation-KLARTEXT.pdf`, `ausgabe-dokument/KLARTEXT-System-Prompt-Dokumentation.pdf`
und `system-prompt.md`. Ein neuer Build erneuert damit auch den Download. In
`.railwayignore` stehen die beiden PDFs deshalb als ausdrückliche Ausnahme vom
Ausschluss ihrer Ordner (`ausgabe/*` mit `!`-Zeile, nicht `ausgabe/`). Wer die
Ausnahme entfernt, bekommt im Hosting „liegt noch nicht vor".

**Server beenden mit `pkill -f "server.py"`.** Das Muster `python3 server.py`
greift nicht, weil der Prozess als `Python server.py` läuft. Ein übersehener
alter Server nimmt den Port und man testet unbemerkt gegen alten Code.

**Notizen im Vortragswerkzeug bearbeiten, aber nicht gleichzeitig in einem
Texteditor.** `notizen.py --server` schreibt die bearbeitete Sprechnotiz sofort
nach `folien.md` — es ersetzt dabei nur den Zeilenbereich dieser einen Notiz
und rechnet vorher nach, dass keine andere Folie mitgeht; schlägt die Probe
fehl, bleibt die Datei unangetastet. Wogegen das nicht schützt: eine offene
`folien.md` in einem Editor, der beim nächsten Speichern seinen eigenen Stand
darüberschreibt. Dasselbe gilt für eine Notizseite, die schon offen war, bevor
die Datei von außen geändert wurde — sie hält ihre eigene Kopie und schreibt
beim Speichern den alten Stand zurück. Nach jeder Änderung an `folien.md` von
außen die Seite neu laden. Ein Build läuft beim Speichern nicht — Folienbilder
ändern sich durch eine Notiz nicht, und `build.py` würde committen. Für die
PowerPoint mit den neuen Notizen danach `python3 build.py`.

**In Sprechnotizen ist fast alles Markdown erlaubt — außer `## `.** Der Parser
in `build.py` erkennt `## ` am Zeilenanfang als neue Folie und `### NOTIZ` als
Notizmarke; beides würde `folien.md` zerlegen und wird von `notiz_pruefen` in
`notizen.py` abgewiesen. Alles andere ist gegen `build.parse()` nachgemessen
und überlebt unverändert: `# `, `### `, `#### `, `- `, `1. `, `> `, `---`,
`**fett**`, `*kursiv*`. Deshalb gibt es keine zweite Überschriftenebene — für
eine Überschrift `# ` oder `### ` nehmen.

**HTML in Sprechnotizen wirkt nicht.** `inline()` in `notizen.py` ruft
zuerst `html.escape()` auf; ein `<small>` steht danach wörtlich auf der
Notizseite. Für Nebensächliches gibt es stattdessen `((doppelte Klammern))`:
auf der Notizseite kleiner und auf 90 % Deckkraft, in der PowerPoint kursiv.
Die 90 % sind keine Geschmacksfrage — Weiß auf `--marke` hält 8,84:1, bei
90 % noch 7,47:1 und damit AAA, bei 85 % nur noch 6,86:1. Anders als `**`
darf die Auszeichnung über Zeilen gehen, aber nicht über eine Leerzeile;
ein unvollständiges `((` meldet `build.py` beim Bauen.

**Der Kursplan braucht den Detailabruf.** `daten/kursplan-holen.py` holt erst
die Liste aller Angebote und dann je Kurs den vollständigen Text. Wer den
zweiten Schritt spart, bekommt die Texte ohne die vorangestellten Bausteine,
also ohne Anmeldehinweis und ohne den eingebetteten Link — und damit ohne die
Stelle, an der `LINKTEXT` greift. Beim Kernfall `4074-74`
sind das 331 statt 710 Zeichen. Die alten Stichproben in `daten/` sind
Messgrundlage der Abgaben und werden nicht überschrieben.

---

## Aufbau

```
folien.md          Quelle der Präsentation, 13 Folien
build.py           Folien → HTML → PNG → PPTX + PDF, rechnet Sprechzeit
stil.css           Foliendesign, Farbwerte nach DESIGN.md
watch.py           baut neu, sobald folien.md oder stil.css sich ändern
notizen.py         Vortragswerkzeug, geht in keine Abgabe ein: erzeugt
                   ausgabe/notizen.html (Sprechnotizen, eine Folie je
                   Bildschirm, für einen Monitor im Hochformat) und
                   ausgabe/vortrag.html (nur das Folienbild). Beide über
                   denselben lokalen Server öffnen — die Kopplung läuft
                   über einen BroadcastChannel und braucht gleiche Herkunft.
                   `--server` liefert sie auf 8795 selbst aus und nimmt
                   bearbeitete Sprechnotizen zurück nach folien.md
dokumentation.md   Quelle der Abgabe 2, mit Platzhaltern
dokument.py        Dokument → HTML → PNG → PDF
dokument.css       Dokumentsatz
system-prompt.md   der Prompt, 6 Komponenten, Platzhalter {{WORTLISTE_A1}}
iterationen.md     Fassungshistorie mit Anlass und Begründung
DESIGN.md          Schrift, Farbe, Größen — verbindlich für alle drei Ausgaben
pruefe-design.py   rechnet die Kontraste nach und prüft die Dateien auf Gleichstand
schriften/         mitgelieferte Schriften samt Lizenztexten, kein CDN-Abruf
daten/             Kursplan, Stichproben, Wortliste, Wirtschaftlichkeit
                   recherche-redaktionsablauf.md: was am Ablauf des Hauses
                   belegt ist und was Annahme bleibt, mit Quellen
tool/              Prototyp: server.py, index.html, protokoll/
                   iterationen-export.py schreibt iterationen-staende.json,
                   die Prompt-Historie für den Betrieb ohne Git
bilder/            zeichnen.py erzeugt die vier Bilder aus der Palette von
                   stil.css; original-petrol/ ist Archiv und wird nicht gelesen
```

Belegte Ports: **8791** build.py, **8793** dokument.py, **8795** die
Vortragsseiten (`python3 -m http.server 8795` oder `notizen.py --server`),
**8799** Prototyp. 8765 und 8787 sind anderweitig belegt. build.py und
dokument.py starten ihren Server nur kurz zum Rendern, würden sich aber sonst
mit einem dauerhaft laufenden beißen. Wer beim Arbeiten schon einen Server auf
8795 hat, sieht `notizen.py --server` mit „Address already in use" scheitern —
erst den alten beenden.

---

## Arbeitsregeln

**Der API-Key darf nirgends hin.** Er steht in `.env` im übergeordneten Ordner,
also außerhalb dieses Repos. Nicht in eine Datei, nicht ins Protokoll, nicht
ins Frontend. `server.py` liest ihn und reicht Anfragen als Proxy weiter.

**Portalabrufe drosseln**, etwa zwei Anfragen pro Sekunde. Das Kursportal der
vhs ist eine öffentliche kommunale Seite.

**Keine Personennamen in Prompt-Ausgaben.** Kursbeschreibungen enthalten die
Namen der Kursleitungen; der Prompt ersetzt sie durch `[Name]`.

**Rechtschreibung vollständig.** Keine ASCII-Ersatzschreibungen wie „Faelle"
oder „Massstab" in Texten, die in einer Abgabe landen. Deutsche
Anführungszeichen. Das musste in `iterationen.md` schon einmal nachträglich
repariert werden.

---

## Prompt ändern

Jede Fassung braucht einen echten Anlass. Der Ablauf:

1. `system-prompt.md` ändern, Feld `**Fassung:**` hochzählen.
2. Gegen echte Texte laufen lassen, mindestens die beiden Kernfälle:
   `4074-74` (DaF A2.2, strenger Fall) und `4213-40` (Englisch A1.1, normaler
   Fall). **Je vier Läufe, nicht einen** — ein einzelner Lauf ist keine
   Messung, das hat v8 auf die harte Tour gezeigt. Erwartung: dort mehrere
   Niveau-Befunde mit einer Streuung von höchstens eins, hier konstant null.
   Zusätzlich prüfen, dass kein Personenname in der Ausgabe steht.
3. In `iterationen.md` einen Abschnitt mit **Anlass, Befund, Änderung,
   Begründung** ergänzen. Auch dann, wenn die Fassung fehlerhaft war — die
   Historie ist Teil der Abgabe und lebt von der Ehrlichkeit.
4. Eigener Commit, damit `git log --follow system-prompt.md` die Historie zeigt.

Läufe protokollieren sich selbst nach `tool/protokoll/`, mit Prüfsumme des
Prompts, Modell und Temperatur.

---

## Vortrag

Fenster **22 Minuten**: rund 18 für die Folien, 4 für die Vorführung des
Werkzeugs. `build.py` rechnet die Sprechzeit bei jedem Build mit 125 Wörtern
pro Minute aus und meldet die Abweichung zum Ziel (`ZIEL_SEK` in `build.py`).

**Diese Meldung ist während der Arbeit kein Kriterium.** Sprechnotizen dürfen
ausführlich sein. Gekürzt wird erst zum Schluss in einem eigenen Durchgang,
und zwar dort, wo es am wenigsten kostet. Die Zeit nicht bei jeder inhaltlichen
Änderung erwähnen.

Sprechnotizen sind **reiner Vorlesetext in Absätzen**, ohne Regieanweisungen.

Die Aufgabe erlaubt höchstens 15 Folien, aktuell sind es 15.
