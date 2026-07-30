# Was `messung.py` macht

Kurzfassung in einfachen Worten. Die ausführliche Fassung mit allen
Einschränkungen steht in `messung.md`.

## Wozu es da ist

Das Skript zählt nach, wie viele Kursbeschreibungen ein Problem haben. Es
liefert die Zahlen, die in der Präsentation stehen — damit sie jeder
nachrechnen kann.

Es ist **kein** Ersatz für den KI-Prüfassistenten. Es ist ein Zählwerk.

## Wie man es benutzt

```bash
cd abschlussprojekt-vhs && python3 daten/messung.py
```

Ergebnis ist eine Übersicht auf dem Bildschirm. Mit `--json` kommt dasselbe in
Maschinenform.

## Was es prüft

Es liest die 60 Kursbeschreibungen aus `vhs-stichprobe-60.json` und sucht nach
fünf Arten von Problemen:

| Was gesucht wird | Wie es erkannt wird |
|---|---|
| Zu lange Sätze | Wörter zählen. Über 25, bei Deutschkursen über 15 |
| Zu schwere Wörter | Abgleich mit der Wortliste des Goethe-Zertifikats A1 |
| Nichtssagende Links | Sucht Linktexte wie „hier“ oder „mehr“ |
| Unerklärte Abkürzungen | Sucht Hausabkürzungen wie DaF oder DTZ im Text |
| Amtsdeutsch | Abgleich mit einer Liste von Verwaltungswörtern |

Bei Deutschkursen gilt ein strengerer Maßstab als bei allen anderen, weil die
Leserschaft dort Deutsch erst lernt. Ob ein Kurs Deutsch vermittelt, erkennt
das Skript am Titel und am Programmbereich.

## Was es nicht prüft

Eine Regel fehlt: **fett gesetzte Zeilen, die eigentlich Überschriften sein
sollten.** Um das zu erkennen, müsste man verstehen, was die Zeile bedeutet.
Ein Skript kann das nur raten, also lässt es die Regel weg und schreibt das in
die Ausgabe.

Deshalb ist das Ergebnis eine **Untergrenze**. Die tatsächliche Zahl der
Probleme liegt höher.

## Warum es sich nicht mehr ändern darf

Der Sinn des Skripts ist der Vergleich: Wie sieht es heute aus, wie in drei
Monaten? Dieser Vergleich funktioniert nur, wenn beide Male gleich gemessen
wird.

Wenn das Skript zwischendurch verbessert würde, wüsste man hinterher nicht, ob
die Texte besser geworden sind oder nur die Messung anders. Deshalb ist es
eingefroren.

Der System-Prompt darf sich dagegen weiterentwickeln, und er tut es auch — er
ist das Arbeitsgerät, nicht das Messgerät.

## Das Ergebnis vom 29.07.2026

- **35 von 60 Texten** haben mindestens einen Befund, das sind **58 Prozent**
- Deutschkurse: alle 14 betroffen, davon 6 auf den Stufen A1 und A2
- Häufigste Probleme: zu schwere Wörter (339), zu lange Sätze (57)
- Längster Satz: 36 Wörter

## Seit dem 30.07.2026 zählt der ganze Bestand

Die Folien nennen nicht mehr die Zahlen dieser Stichprobe, sondern die aller
3.111 Kurstexte des Portals. Gerechnet wird das von `messung-bestand.py`:

```bash
cd abschlussprojekt-vhs && python3 daten/messung-bestand.py
```

Es benutzt `messung.py` unverändert und wechselt nur die Eingabemenge. Das
Ergebnis: **1.765 von 3.111 Texten** haben einen Befund, das sind **57
Prozent**. Für Deutschkurse auf A1 und A2 gibt es **31 verschiedene Texte**,
alle mit Wörtern über dem Niveau ihrer Leser; sie stecken in **196 Kursen**.

Die Stichprobe lag also 1,6 Prozentpunkte daneben. Sie bleibt als Beleg dafür
liegen, wird aber nicht mehr fortgeschrieben.

## Wo die Zahlen in der Arbeit stehen

Folie 2 (Befundquote), Folie 5 (Messung und Befund), Folie 14 (Erfolgsmessung).
Wer eine dieser Zahlen ändert, lässt vorher `messung-bestand.py` laufen.
