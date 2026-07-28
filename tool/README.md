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

## Bedienung

1. Links oben einen der 60 echten Kurse aus der Stichprobe wählen. Titel,
   Nummer, Programmbereich, Niveau und Text werden vorbelegt und lassen sich
   ändern. Ein eigener Text geht genauso.
2. „Text prüfen“ (oder `Cmd + Return`) startet die Prüfung.
3. Rechts erscheinen Zielgruppe, Befunde, geprüfte Regeln ohne Befund und die
   Gesamteinschätzung. Farbcode: Petrol = PFLICHT, Warnton = EMPFEHLUNG,
   Grau = HINWEIS.
4. Über „Rohtext“ oben rechts lässt sich die unveränderte Modellantwort
   ansehen. Das ist auch der Rückfall, falls die Antwort einmal nicht dem
   Format folgt.

## Dateien

| Datei | Inhalt |
|---|---|
| `server.py` | Lokaler Server auf Port 8799, baut den System-Prompt, proxyt zu OpenRouter, schreibt die Protokolle |
| `index.html` | Die Oberfläche, eine Datei, CSS und JS inline, keine externen Ressourcen |
| `start.command` | Doppelklick-Start für macOS |
| `protokoll/` | Ein JSON je Prüfung, mit Zeitstempel. Grundlage für die Dokumentation der Testszenarien |

## Was der Server mit dem Prompt macht

- `../system-prompt.md` wird geladen, der Kopfbereich bis zur ersten
  `---`-Trennlinie fällt weg.
- Der Platzhalter `{{WORTLISTE_A1}}` wird durch den Inhalt von
  `../daten/wortliste-goethe-a1.txt` ersetzt (Zeilen mit `#` sind Kommentare
  und fallen weg).
- **Fehlt die Wortliste**, läuft die Prüfung ohne Referenzwortschatz weiter.
  Die Oberfläche zeigt dann oben einen orangenen Balken „Ohne
  Referenzwortschatz“, und der Prompt sorgt dafür, dass die Niveau-Befunde als
  Schätzungen gekennzeichnet werden.
- Prompt und Wortliste werden bei jeder Prüfung frisch geprüft. Eine später
  erzeugte Wortliste wirkt also ohne Neustart des Servers.

## Modell

Erstwahl `anthropic/claude-sonnet-4.5`, Ersatz `anthropic/claude-3.7-sonnet`.
Welches geantwortet hat, steht in der Fußzeile der App, im Protokoll und im
Terminal. Temperatur 0,1, damit derselbe Text möglichst dieselben Befunde
ergibt.

## Protokolle

Jede Prüfung landet als `protokoll/JJJJMMTT-HHMMSS-<kursnummer>.json` mit
Zeitstempel, Modell, Promptfassung und Prüfsumme des Prompts, Angabe ob mit
oder ohne Wortliste geprüft wurde, der vollständigen Eingabe, der
vollständigen Modellantwort und dem Tokenverbrauch. Kein API-Key.
