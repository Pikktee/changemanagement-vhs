# KLARTEXT

Redaktionsassistent für Kursbeschreibungen der Volkshochschule Frankfurt am Main.
Man gibt eine Kursbeschreibung ein, die App schickt sie zusammen mit dem
System-Prompt aus `../system-prompt.md` an ein Sprachmodell und stellt die
Prüfbefunde strukturiert dar.

## Starten

Doppelklick auf `start.command`, oder im Terminal:

```bash
python3 server.py --open
```

Die App läuft danach unter [http://localhost:8799](http://localhost:8799).
Beenden mit `Ctrl+C` im Terminal.

## Voraussetzungen

- macOS mit Python 3 (vorinstalliert), keine weiteren Pakete
- Eine `.env` mit `OPENROUTER_API_KEY=...` in diesem Ordner, im Ordner darüber
  oder zwei Ordner darüber. Der Key bleibt auf dem Rechner: Der lokale Server
  reicht die Anfragen an OpenRouter weiter, liefert den Key nie an den Browser
  aus und schreibt ihn nicht ins Protokoll.
- `../daten/vhs-kursplan.json`. Fehlt die Datei, fällt der Server auf die alte
  Stichprobe `vhs-stichprobe-60.json` zurück und sagt das beim Start. Neu holen
  mit `python3 ../daten/kursplan-holen.py`.

## Bedienung

1. „Kurs aus dem Kursplan wählen“ öffnet die Kursauswahl mit dem vollständigen
   Programm der vhs. Gesucht wird über Kursnummer, Titel, Untertitel, Ort und
   den ganzen Beschreibungstext; gefiltert nach Programmbereich, Sprachniveau
   und Kursort. Titel, Nummer, Programmbereich, Niveau und Text werden
   vorbelegt und lassen sich ändern. Ein eigener Text geht genauso.
2. „Text prüfen“ startet die Prüfung.
3. Rechts erscheinen Zielgruppe, Befunde, geprüfte Regeln ohne Befund und die
   Gesamteinschätzung. Farbcode: Petrol = PFLICHT, Warnton = EMPFEHLUNG,
   Grau = HINWEIS. Darüber steht, womit geprüft wurde: Modell, Temperatur,
   Promptfassung, Referenzwortschatz und der Name der Protokolldatei.
4. Über „Rohtext“ oben rechts lässt sich die unveränderte Modellantwort
   ansehen. Das ist auch der Rückfall, falls die Antwort einmal nicht dem
   Format folgt.

## Prompt und Parameter

Der Knopf „System-Prompt“ oben rechts öffnet ein Panel mit dem Prompt, so wie
er an das Modell geht, also mit bereits eingesetztem Referenzwortschatz.
Modell und Temperatur sind dort wählbar, der Prompt lässt sich bearbeiten.

Angepasste Werte gelten **nur im geöffneten Browsertab** und ändern
`system-prompt.md` nicht. Weicht etwas vom Standard ab, sagen das drei Stellen
zugleich: ein Balken oben auf der Seite, die Marke „Angepasst“ im Panel und das
Feld `abweichungVomStandard` im Protokoll. Ein Lauf mit verändertem Prompt darf
nicht aussehen wie ein Lauf nach dem dokumentierten Stand; der angepasste
Prompt wird deshalb vollständig mitprotokolliert.

## Dateien

| Datei | Inhalt |
|---|---|
| `server.py` | Lokaler Server auf Port 8799, baut den System-Prompt, sucht und filtert im Kursplan, proxyt zu OpenRouter, schreibt die Protokolle |
| `index.html` | Die Oberfläche, eine Datei, CSS und JS inline, keine externen Ressourcen |
| `start.command` | Doppelklick-Start für macOS |
| `protokoll/` | Ein JSON je Prüfung, mit Zeitstempel. Grundlage für die Dokumentation der Testszenarien |
| `../daten/kursplan-holen.py` | Holt den Kursplan aus dem Portal |
| `../daten/vhs-kursplan.json` | Der Kursplan, rund 3.100 Kurse mit vollständigem Text |

## Was der Server mit dem Prompt macht

- `../system-prompt.md` wird geladen, der Kopfbereich bis zur ersten
  `---`-Trennlinie fällt weg.
- Der Platzhalter `{{WORTLISTE_A1}}` wird durch den Inhalt von
  `../daten/wortliste-goethe-a1.txt` ersetzt (Zeilen mit `#` sind Kommentare
  und fallen weg).
- **Fehlt die Wortliste**, läuft die Prüfung ohne Referenzwortschatz weiter.
  Die Oberfläche zeigt dann oben einen orangenen Balken „Ohne
  Referenzwortschatz“, und der Server stellt den Ehrlichkeitsvorbehalt selbst
  vor die Antwort.
- Prompt und Wortliste werden bei jeder Prüfung frisch geprüft. Eine später
  erzeugte Wortliste wirkt also ohne Neustart des Servers.

## Modell

Erstwahl `anthropic/claude-sonnet-4.5`, Ersatz `anthropic/claude-sonnet-4`.
Die Erstwahl ist die Fassung, mit der die Belege der Abgabe entstanden sind;
sie bleibt der Standard, auch wenn im Panel andere Modelle wählbar sind.
Welches Modell geantwortet hat, steht über den Befunden, im Protokoll und im
Terminal. Temperatur 0,1, damit derselbe Text möglichst dieselben Befunde
ergibt.

Wählbar sind nur Modelle aus der Liste in `server.py`. Was der Browser schickt,
ginge sonst ungeprüft als Modellname an OpenRouter.

## Kursdaten

`../daten/kursplan-holen.py` holt den Kursplan aus der offenen Schnittstelle
des Kursportals. Der Abruf geht in zwei Schritten: eine Anfrage für die Liste
aller Angebote, danach eine Anfrage je Kurs für den **vollständigen** Text.
Der zweite Schritt ist nicht wegzulassen, denn die Liste liefert die Texte ohne
die vorangestellten Bausteine, also ohne Anmeldehinweis und ohne den
eingebetteten Link. Genau daran greifen Regeln wie `LINKTEXT`. Er ist auf zwei
Anfragen je Sekunde gedrosselt, dauert rund eine halbe Stunde und lässt sich
nach einem Abbruch fortsetzen.

Die alten Stichproben `vhs-stichprobe-60.json` und `vhs-stichprobe-gross.json`
bleiben unverändert. Sie sind die Messgrundlage der Abgaben.

## Protokolle

Jede Prüfung landet als `protokoll/JJJJMMTT-HHMMSS-<kursnummer>.json` mit
Zeitstempel, Modell, Temperatur, Promptfassung und Prüfsumme des Prompts,
Angabe ob mit oder ohne Wortliste geprüft wurde, ob und wie vom Standard
abgewichen wurde, der vollständigen Eingabe, der vollständigen Modellantwort
und dem Tokenverbrauch. Kein API-Key.
