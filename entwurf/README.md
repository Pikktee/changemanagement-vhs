# Entwurf der Werkzeugoberfläche

> **Umgesetzt am 29.07.2026.** `tool/index.html` folgt diesem Entwurf. Wo
> abgewichen wurde und warum, steht in `OFFEN.md` unter Punkt 4. Diese Datei
> bleibt als Begründung der Bedienung stehen; geändert wird ab jetzt das
> Werkzeug, nicht der Entwurf.

`werkzeug.html` ist ein **klickbarer Entwurf**, kein lauffähiges Werkzeug. Er
enthält einen festen Beispielfall (Kurs 4074-74) und ruft kein Modell auf.
Zweck: die Bedienung ausprobieren, bevor sie in `tool/index.html` eingebaut
wird.

Öffnen über einen lokalen Server, damit die Schriften aus `../schriften/`
geladen werden:

```bash
cd abschlussprojekt-vhs && python3 -m http.server 8795
```

Dann `http://localhost:8795/entwurf/werkzeug.html`.

## Was hier entschieden ist

**Zwei Ansichten statt einer.** Vor der Prüfung nur die Eingabe, danach nur
das Ergebnis. Ein Layout mit leerer Ergebnisfläche verspricht eine Anordnung,
die nach dem Prüfen nicht kommt.

**Text links, Befunde rechts, Text bleibt stehen.** Geprüft gegen vier
Alternativen (Befunde links, einspaltig untereinander, Befund als Popover an
der Stelle). Ausschlaggebend war nicht Ergonomie, sondern die Aussage: Dass
ein Text als Ganzes an seiner Zielgruppe vorbeigeht, sieht man nur, wenn der
durchgehend markierte Absatz und die Liste gleichzeitig im Bild sind. Popover
und Einspalter zeigen immer nur einen Befund.

**Es scrollt die Liste, nicht der Text.** Kursbeschreibungen sind kurz — der
Kernfall hat 331 Zeichen, mit Bausteinen 710. Die Befundliste wächst dagegen
mit jedem Fund. Deshalb `position:sticky` auf dem Textbereich: Beim Sprung zu
Befund 9 bleibt der Text vollständig sichtbar.

**Unter 980 px** erscheint der Befund als Kopie direkt unter dem Text, statt
ans Seitenende zu springen. Die Liste darunter bleibt vollständig.

**Bedienung ohne Maus.** Fundstellen und Befunde sind fokussierbar, Enter und
Leertaste wählen, Escape löst die Auswahl. Ein zweiter Klick auf dieselbe
Stelle hebt sie ebenfalls auf.

## Was diesem Entwurf fehlte

Alles davon ist im Werkzeug erledigt, hier nicht — `werkzeug.html` bleibt der
Entwurf, der er war.

- Anbindung an `server.py`; die Befunde sind hier fest eingetragen
- Ableitung der Fundstellen aus dem Zitat des Modells (der Prompt liefert
  jede Stelle wörtlich, die Markierung muss daraus erzeugt werden)
- Lade- und Fehlerzustand

## Was weiterhin offen ist

- **Prüfung auf einem echten Touchgerät.** Ob die Markierungen groß genug zu
  treffen sind, lässt sich am Simulator nicht abschließend beurteilen. Die
  Fundstellen sind so hoch wie die Zeile und liegen bei `line-height:2` weit
  auseinander, aber ein einzelnes markiertes Wort wie „hier" ist schmal.
- **Personennamen auf der Leinwand.** Der Prompt ersetzt Namen in seiner
  Ausgabe durch `[Name]`. Der geprüfte Text ist jetzt aber die Hauptfläche der
  Ergebnisansicht, und viele Kursbeschreibungen führen die Kursleitung samt
  Telefonnummer und Dienstadresse — bei `4213-40` etwa. Bei der Vorführung
  steht das dann groß im Raum. Die Daten stehen so im öffentlichen Kursportal,
  und den Text zu schwärzen hieße, die Fundstellen zu verlieren; für den
  Vortrag ist trotzdem zu entscheiden, welcher Kurs vorgeführt wird.
