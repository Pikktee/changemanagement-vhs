# KLARTEXT — Betriebsanleitung

Die Rahmung des Projekts steht in der `CLAUDE.md` im übergeordneten Ordner und
wird von dort mitgeladen. Hier steht, wie man damit arbeitet, ohne etwas
kaputtzumachen.

Alle Pfade in dieser Datei sind relativ zu `abschlussprojekt-vhs/`. Shell-Befehle
gehen vom übergeordneten Ordner als Arbeitsverzeichnis aus.

---

## Woraus die Arbeit besteht

Die Aufgabenstellung schreibt Struktur, Folienzahl und Pflichtinhalte ziemlich
genau vor. Vier Phasen:

| Phase | Inhalt laut Aufgabe | Wo im Projekt |
|---|---|---|
| 1 | Unternehmensanalyse, Ist-Analyse, Potentialermittlung | Folien 3–5 |
| 2 | Prozessauswahl, Soll-Zustand, System-Prompt nach 6 Komponenten, Implementierungsplanung | Folien 3, 6–8, `system-prompt.md` |
| 3 | Change Management: Stakeholder, Kommunikation, Widerstand, Quick Wins, KPIs, Schulung | Folien 9–12 |
| 4 | Präsentationsvorbereitung | `folien.md`, `build.py` |

Die Arbeit entsteht in **Einzelarbeit**. Die Aufgabenstellung geht von Teams
aus; das ist auf Folie 1 und in Abgabe 2 offengelegt.

---

## Die inhaltliche Kernthese

**Ein Text ist nicht an sich verständlich, sondern nur für eine bestimmte
Zielgruppe.** Ein Lesbarkeitsindex beanstandet deshalb den Englischkurs, dessen
Leser fließend Deutsch lesen, und winkt den Deutschkurs auf A2 durch. Der
Prompt bestimmt zuerst, wer liest, und legt danach zwei verschiedene Maßstäbe
an. Belegt an zwei echten Kursen: sieben Niveau-Befunde gegen null.

Der Rechtsanspruch trägt das Projekt **nicht** — die entscheidenden
WCAG-Kriterien sind Stufe AAA und damit nicht verbindlich. Argumentiert wird
mit der Betriebssatzung: Die Angebote stehen „grundsätzlich allen offen, ohne
Rücksicht auf Vorbildung". Diese Unterscheidung ist heikel und darf nicht
verwischt werden.

## Der wichtigste Grundsatz der Umsetzung

**Was feststeht, gehört in den Code. Was Urteil verlangt, bleibt beim Modell.**

Das ist zugleich die Change-Argumentation: Technische Barrierefreiheit bleibt
beim deterministischen Prüfwerkzeug und bei der städtischen IT, die KI
übernimmt nur den urteilenden Teil bei den Programmbereichen. Zwei
Zuständigkeiten, zwei Adressaten.

Beim Bauen hat sich das zweimal selbst bestätigt: Zwei Zusagen standen zuerst
im System-Prompt und wurden nicht zuverlässig eingehalten. Beide liegen heute
in `tool/server.py` — der Ehrlichkeitsvorbehalt bei fehlender Wortliste und die
Einstufung der Befunde aus der Regeltabelle.

Wenn eine neue Anforderung eine Nachschlagetabelle ist, schreibe sie nicht in
den Prompt.

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

**Die Abgabe-2-Doku zieht ihre Inhalte zur Bauzeit.** `dokumentation.md`
enthält Platzhalter wie `{{PROMPT:GRENZEN}}`, `{{ITER:v4}}` und
`{{PROTOKOLL:4074-74:antwort}}`. Prompt-Abschnitte, Iterationshistorie und
Beispielläufe niemals hineinkopieren, sonst driftet das PDF vom Prompt weg.

**Jeder neue Lauf eines Kernfalls landet im PDF.** `{{PROTOKOLL:...}}` nimmt
das **jüngste** Protokoll dieser Kursnummer. Wer 4074-74 zum Ausprobieren durch
das Tool schickt, ersetzt damit den Beispiellauf der Abgabe — und der Fließtext
daneben behauptet weiter sieben Niveaubefunde, während das Modell beim nächsten
Mal fünf meldet. Läufe, die nicht in die Abgabe sollen, gehören nach
`tool/protokoll/pruefung-kursplan/`; der Unterordner wird nicht durchsucht.

**Farben und Schriften stehen in `DESIGN.md`, nicht im Ermessen.** Die Werte
liegen deckungsgleich in `stil.css`, `dokument.css` und `tool/index.html`.
Nach jeder Änderung daran `python3 pruefe-design.py` — das Skript rechnet alle
Kontrastpaare nach und meldet, wenn die drei Dateien auseinanderdriften. Das
System hält WCAG AAA freiwillig ein; genau das ist das Argument, und es
zerfällt, sobald eine Folie es reißt.

**Server beenden mit `pkill -f "server.py"`.** Das Muster `python3 server.py`
greift nicht, weil der Prozess als `Python server.py` läuft. Ein übersehener
alter Server nimmt den Port und man testet unbemerkt gegen alten Code.

**Der Kursplan braucht den Detailabruf.** `daten/kursplan-holen.py` holt erst
die Liste aller Angebote und dann je Kurs den vollständigen Text. Wer den
zweiten Schritt spart, bekommt die Texte ohne die vorangestellten Bausteine,
also ohne Anmeldehinweis und ohne den eingebetteten Link — und damit ohne die
Stellen, an denen `LINKTEXT` und `BAUSTEIN` greifen. Beim Kernfall `4074-74`
sind das 331 statt 710 Zeichen. Die alten Stichproben in `daten/` sind
Messgrundlage der Abgaben und werden nicht überschrieben.

---

## Aufbau

```
folien.md          Quelle der Präsentation, 13 Folien
build.py           Folien → HTML → PNG → PPTX + PDF, rechnet Sprechzeit
stil.css           Foliendesign, Farbwerte nach DESIGN.md
watch.py           baut neu, sobald folien.md oder stil.css sich ändern
dokumentation.md   Quelle der Abgabe 2, mit Platzhaltern
dokument.py        Dokument → HTML → PNG → PDF
dokument.css       Dokumentsatz
system-prompt.md   der Prompt, 6 Komponenten, Platzhalter {{WORTLISTE_A1}}
iterationen.md     Fassungshistorie mit Anlass und Begründung
DESIGN.md          Schrift, Farbe, Größen — verbindlich für alle drei Ausgaben
pruefe-design.py   rechnet die Kontraste nach und prüft die Dateien auf Gleichstand
schriften/         mitgelieferte Schriften samt Lizenztexten, kein CDN-Abruf
daten/             Kursplan, Stichproben, Wortliste, Wirtschaftlichkeit
tool/              Prototyp: server.py, index.html, protokoll/
bilder/            flach-geometrische JPGs; umfaerben.py, Originale in original-petrol/
```

Belegte Ports: **8791** build.py, **8793** dokument.py, **8799** Prototyp.
8765 und 8787 sind anderweitig belegt. Für eigene Testserver 8795 nehmen —
build.py und dokument.py starten ihren Server nur kurz zum Rendern, würden
sich aber sonst mit einem dauerhaft laufenden beißen.

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
   Fall). Erwartung: dort sieben Niveau-Befunde, hier null.
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

Sprechnotizen sind **reiner Vorlesetext in Absätzen**, ohne Regieanweisungen.

Die Aufgabe erlaubt höchstens 15 Folien, aktuell sind es 13.
