# Entwurf der Werkzeugoberfläche

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

## Was noch fehlt

- Anbindung an `server.py`; die Befunde sind hier fest eingetragen
- Ableitung der Fundstellen aus dem Zitat des Modells (der Prompt liefert
  jede Stelle wörtlich, die Markierung muss daraus erzeugt werden)
- Lade- und Fehlerzustand
- Prüfung auf einem echten Touchgerät: ob die Markierungen groß genug zu
  treffen sind, lässt sich am Simulator nicht abschließend beurteilen
