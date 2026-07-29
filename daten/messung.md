# Befundquote der 60er-Stichprobe

Erhebung und Auswertung, Stand 29. Juli 2026. Skript: `daten/messung.py`.

Anlass sind zwei Zahlen, die auf drei Folien stehen und nirgends hergeleitet
waren: „90 Prozent der Texte haben mindestens einen Befund“ und „9 von 13
Kursen für Deutschlernende enthalten C1-Vokabular“. Beide sollten
nachrechenbar sein, sonst behauptet die Arbeit eine Messung, die keine war.
Dieses Dokument hält fest, wie nachgerechnet wurde und was dabei
herausgekommen ist.

**Das Ergebnis bestätigt die beiden Zahlen nicht.** Gemessen sind 58,3 Prozent
statt 90, und bei den Deutschkursen ist die Aussage je nach Lesart 14 von 14
oder 4 von 14, aber in keiner Lesart 9 von 13. Die Herleitung steht unten,
der Abgleich im Abschnitt „Abweichung zu den bisher genannten Zahlen“.

## Methode

Datenquelle ist `vhs-stichprobe-60.json`, dieselbe Stichprobe, auf die sich
die Folien berufen: 60 Kursbeschreibungen, gezogen über die offene
Schnittstelle des Kursportals am 28.07.2026. Sie wurde für diese Messung
nicht verändert.

Referenz für den Wortschatz ist `wortliste-goethe-a1.txt`, der veröffentlichte
Prüfungswortschatz des Goethe-Zertifikats A1. Das Skript liest daraus 812
Vollformen und 15 Stämme auf Bindestrich (`all-`, `dies-`).

Gemessen werden fünf der sechs Prüfregeln aus `system-prompt.md`, und zwar
genau die, die ohne Urteil entscheidbar sind:

| Regel | Operationalisierung im Skript |
| --- | --- |
| `SATZ` | Satz über 25 Wörter, im strengen Fall über 15. Zeilenumbruch gilt als Satzgrenze, Doppelpunkt nicht. Abkürzungen wie „z. B.“ beenden keinen Satz, „etc.“ und „usw.“ schon. |
| `NIVEAU` | Nur im strengen Fall. Inhaltswort, das weder auf der A1-Liste steht noch sich nach den vier Ausnahmen des Prompts herleiten lässt: gebeugte Form, Funktionswort, Zusammensetzung oder Ableitung aus Listenwörtern, Eigenname. Je Text zählt jedes Wort einmal. |
| `LINKTEXT` | Linktext aus dem Markup gelesen, bevor die Auszeichnung entfernt wird. Befund bei nichtssagenden Texten wie „hier“, „mehr“, „klicken“, „diese Seite“, „Link“. |
| `ABK` | Die Hausabkürzungen aus dem Prompt (DaF, DTZ, GER, telc, Xpert, ECDL, IVOM sowie A1 bis C2), wenn der Text sie nicht selbst auflöst. KI, PC, EU und ISBN gelten laut Prompt als bekannt. |
| `AMTSDEUTSCH` | Abgleich gegen eine Liste von 28 Wendungen, die im Skript sichtbar steht. Die ersten vier nennt der Prompt selbst. |

Der strenge Fall gilt, wenn der Kurs selbst Deutsch vermittelt. Erkannt wird
das an der Kursnummer 40xx oder 41xx — das ist die Nummernsystematik des
Hauses für den Programmbereich Deutsch als Fremdsprache — und ersatzweise an
den Titelstichworten DaF, Integrationskurs, Alphabetisierung, Literalisierung
und Goethe-Zertifikat. In der Stichprobe ergibt das 14 Kurse.

Der Text enthält HTML, in dieser Stichprobe nur `<a>` und `<strong>`.
Ausgewertet wird der sichtbare Text; Linktext und Linkziel werden vor dem
Entfernen des Markups herausgelesen, weil sonst nur noch das Wort „hier“
übrig bliebe und nicht mehr erkennbar wäre, dass es ein Link war.

Das Skript prüft sich bei jedem Lauf an fünfzehn Beispielen, die der Prompt
selbst nennt: acht Wörter, die ein Niveaubefund sein müssen (`Niveaustufe`,
`Teilstufen`, `umfasst`, `äußern`, `Selbsteinschätzung`, `Fehleinschätzung`,
`Umbuchung`, `gegebenenfalls`), und sieben Formen, die keiner sein dürfen
(`den`, `dem`, `einer`, `Kursen`, `Sätze`, `Ausdrücke`, `Kursleitung`).
Schlägt das fehl, sind die Niveauzahlen des Laufs wertlos und die Ausgabe
sagt das. Im hier dokumentierten Lauf ist die Selbstprüfung bestanden.

## Was nicht gemessen wird

`STRUKTUR` ist die sechste Regel und nicht deterministisch prüfbar. Sie
verlangt die Entscheidung, ob eine Zeile als Überschrift oder Aufzählung
gemeint war, und genau diese Entscheidung kann ein Skript nur raten. Sie
bleibt deshalb ungemessen, und die Ausgabe weist sie ausdrücklich als
ungemessen aus. **Die gemessene Befundquote ist damit eine Untergrenze**, und
zwar vermutlich eine deutliche: `STRUKTUR` ist unter den sechs Regeln
diejenige, die in den Portaltexten am häufigsten greifen dürfte, weil dort
regelmäßig freistehende Zeilen wie „Information und Beratung“ oder
„Technische Hinweise“ als Fließtext gesetzt sind.

`NIVEAU` im normalen Fall bleibt aus demselben Grund ungemessen. Der Prompt
lässt die Regel dort ausschließlich bei Fachwörtern wie „Kontraindikation“
oder „Lasurtechnik“ gelten. Ob ein Wort ein Fachwort ist, ist ein Urteil und
keine Nachschlagetabelle.

## Ergebnis des Laufs vom 29.07.2026

| Kennzahl | Wert |
| --- | --- |
| Ausgewertete Texte | 60 |
| Texte mit mindestens einem Befund | 35 (**58,3 Prozent**) |
| Texte ohne Befund | 25 |
| Befunde insgesamt | 438 |

### Verteilung nach Regel

| Regel | Befunde | betroffene Texte |
| --- | --- | --- |
| `SATZ` | 57 | 30 |
| `NIVEAU` | 339 | 14 |
| `LINKTEXT` | 9 | 9 |
| `ABK` | 21 | 15 |
| `AMTSDEUTSCH` | 12 | 9 |
| `STRUKTUR` | nicht gemessen | nicht gemessen |

Alle neun Linktextbefunde lauten „hier“. Fünf der zwölf
Amtsdeutschbefunde sind „gegebenenfalls“, vier „Erstattung“, drei „ggf.“.

### Strenger und normaler Fall

| Kennzahl | Strenger Fall | Normaler Fall |
| --- | --- | --- |
| Texte | 14 | 46 |
| Satzgrenze | 15 Wörter | 25 Wörter |
| Texte mit Befund | 14 (100 Prozent) | 21 (45,7 Prozent) |
| Befunde | 396 | 42 |
| davon `SATZ` | 35 | 22 |
| davon `NIVEAU` | 339 | nicht geprüft |
| davon `LINKTEXT` | 4 | 5 |
| davon `ABK` | 18 | 3 |
| davon `AMTSDEUTSCH` | 0 | 12 |

Die Null bei `AMTSDEUTSCH` im strengen Fall ist kein Ausfall, sondern die
Regel des Prompts: Trifft dort `NIVEAU` und `AMTSDEUTSCH` auf dasselbe Wort
zu, zählt `NIVEAU`. „Umbuchung“ steht deshalb im DaF-Kurs als Niveaubefund
und im Computerkurs als Amtsdeutschbefund.

### Kurse für Deutschlernende

| Lesart | Wert |
| --- | --- |
| Kurse, die Deutsch vermitteln | 14 |
| davon mit mindestens einem `NIVEAU`-Befund | 14 |
| davon auf Stufe A1 oder A2 | 6, alle sechs mit `NIVEAU`-Befund |
| Kurse mit den drei auf der Folie genannten Wörtern | 4 |

Die drei genannten Wörter sind `Selbsteinschätzung`, `Fehleinschätzung` und
`Umbuchung`. Sie stehen alle drei im selben Textbaustein „Hinweis zur
Anmeldung“, der in vier der vierzehn Kurse vorkommt.

### Satzlänge

| Kennzahl | Wert |
| --- | --- |
| Längster gemessener Satz | 36 Wörter, Kurs 5604-02 „Debattieren“ |
| Längster Satz im strengen Fall | 34 Wörter, Kurs 4143-74 |
| Vergleichswert ohne Zeilenumbruch als Satzgrenze | 79 Wörter, Kurs 5353-02 |
| Kernfall 4074-74, DaF A2.2 | Ø 10,8 Wörter, längster Satz 23 |
| Kernfall 4213-40, Englisch A1.1 | Ø 9,1 Wörter, längster Satz 23 |

Der Vergleichswert von 79 Wörtern gehört nicht zur Regel `SATZ`. Er entsteht,
wenn Zeilenumbrüche nicht als Satzgrenze gelten und eine Aufzählung ohne
Satzzeichen dadurch als ein einziger Satz zählt. Er steht hier nur, weil sich
die zuvor veröffentlichte Zahl anders nicht erklären lässt.

## Abweichung zu den bisher genannten Zahlen

| Bisher behauptet | Gemessen | Ursache |
| --- | --- | --- |
| 90 Prozent mit mindestens einem Befund | 58,3 Prozent | Die Messung erfasst nur fünf der sechs Regeln und `NIVEAU` nur im strengen Fall. Die beiden fehlenden Urteilsanteile sind genau die, die in unauffälligen Texten am ehesten greifen. |
| Nur 6 von 60 blieben ohne Befund | 25 von 60 ohne Befund | dieselbe Ursache |
| Längster Satz 74 Wörter | 36 Wörter | Der alte Wert zählt eine Aufzählung als einen Satz. Ohne Zeilenumbruch als Satzgrenze kommt diese Messung auf 79. |
| 9 von 13 Kursen für Deutschlernende | 14 von 14 mit Niveaubefund, 4 von 14 mit den drei genannten Wörtern | Der Nenner 13 entspricht den dreizehn Kursen, deren Titel mit „DaF“ beginnt; der vierzehnte, die Prüfungsvorbereitung auf das Goethe-Zertifikat C2, vermittelt ebenfalls Deutsch. Der Zähler 9 lässt sich in keiner Lesart reproduzieren. |
| Folientabelle: Englisch A1.1 Ø 21,3 Wörter, längster 41 | Ø 9,1, längster 23 | wie beim längsten Satz: Aufzählungen als Sätze gezählt |
| Folientabelle: DaF A2.2 Ø 10,6 Wörter, längster 16 | Ø 10,8, längster 23 | Der Mittelwert stimmt fast; der längste Satz weicht ab, weil der alte Wert an „z. B.“ getrennt hat. |

Zur inhaltlichen Kernthese sagt diese Messung wenig, und sie kann auch wenig
dazu sagen: Sie prüft `NIVEAU` nur im strengen Fall, der Vergleich zwischen
Deutsch- und Englischkurs ist also von der Anlage her einseitig. Was sie
zeigt, ist der Ausgangsbefund: Der Englischkurs 4213-40 hat mit Ø 9,1 Wörtern
die kürzeren Sätze und genau einen deterministischen Befund, der DaF-Kurs
4074-74 bei niedrigerem Leseniveau die längeren Sätze und 24 Niveaubefunde.
Belegt wird die These weiterhin durch die Läufe des Prompts, nicht durch
dieses Skript. Was nicht hält, sind die Einzelzahlen, mit denen sie bisher
bebildert wurde.

## Grenzen der Messung

**Die Quote ist eine Untergrenze.** `STRUKTUR` fehlt ganz, `NIVEAU` fehlt im
normalen Fall. Beides ist nicht Nachlässigkeit, sondern der Punkt der
Arbeit: Was Urteil verlangt, bleibt beim Modell.

**Die Zerlegung von Zusammensetzungen ist strenger als der Prompt.** Der
Prompt erlaubt Zusammensetzungen aus Listenwörtern, „wenn die Bedeutung sich
erschließt“. Das Skript verlangt statt dessen, dass jeder Bestandteil selbst
auf der Liste steht oder sich regelmäßig aus ihr herleiten lässt. Es meldet
deshalb Wörter, die ein Mensch durchgehen ließe. Zwei Wörter, die der Prompt
ausdrücklich als zulässig nennt, fehlen auf der veröffentlichten Goethe-Liste
tatsächlich — `Ausdruck` und `leiten`; sie stehen im Skript als sichtbare
Ergänzung, sonst meldete es genau das, was der Prompt ausdrücklich nicht
gemeldet haben will.

**Die A1-Liste ist nur für A1- und A2-Kurse der zutreffende Maßstab.**
Darüber gibt der Prompt an das Urteil ab. Der C2-Vorbereitungskurs kommt in
dieser Messung auf 98 Niveaubefunde; das misst nicht die Verständlichkeit des
Textes, sondern den Abstand zwischen A1 und C2. Deshalb ist die Zahl der
Deutschkurse auf A1 und A2 getrennt ausgewiesen.

**Eigennamen sind deterministisch nicht sicher erkennbar.** Ausgeschlossen
werden die Namen der Kursleitungen aus dem Feld `kursleiter`, die Wörter des
Kurstitels und eine Liste von 69 Orts-, Marken- und Produktnamen, die in
dieser Stichprobe vorkommen. Auf anderen Daten wäre diese Liste unvollständig.

**Die Amtsdeutschliste ist der Teil mit dem größten Ermessensanteil.** Sie
umfasst 28 Wendungen und steht vollständig im Skript. Eine längere Liste
ergäbe eine höhere Quote; genau deshalb wird sie nicht verlängert.

**Ein Wort zählt je Text einmal.** Der Prompt zählt je Fundstelle. Für eine
Quote über 60 Texte ist die Wortart die stabilere Einheit, und sie zählt
niemals zu hoch.

## Nachmessen

```bash
cd abschlussprojekt-vhs && python3 daten/messung.py
python3 daten/messung.py --json   # maschinenlesbar
```

Das Skript ist ein Messinstrument und wird eingefroren. Eine Nachmessung ist
nur dann eine Nachmessung, wenn die Methode zwischen beiden Läufen unverändert
geblieben ist. Wer später die Satzgrenze verschiebt, die Amtsdeutschliste
ergänzt oder die Wortzerlegung großzügiger macht, vergleicht zwei Zahlen, die
nichts miteinander zu tun haben. Wird eine Änderung unvermeidlich, gehört sie
in eine zweite Datei mit eigenem Namen und eigener Messung, damit beide Stände
nebeneinander stehen bleiben.
