# Wirtschaftlichkeit des KI-Pruefschritts fuer Kursbeschreibungen

Erhebung und Auswertung, Stand 28. Juli 2026.

Anlass ist der Einwand, ein Pruefschritt fuer Kursbeschreibungen koste bei 5.800 Veranstaltungen im Jahr und drei Minuten Pruefzeit rund 290 Stunden. Der Einwand unterstellt, dass jede Veranstaltung einen eigenen, einzeln zu pruefenden Text besitzt. Genau diese Annahme wird hier geprueft.

## Methode

Datenquelle ist die offene Schnittstelle des VHS-Kundenportals:

```
GET https://vhs.frankfurt.de/KundenportalApi/api/angebot/{id}
```

Sie liefert je Angebot ein JSON-Objekt. Das Feld `text` enthaelt die veroeffentlichte Beschreibung. Nicht belegte IDs liefern `data: null` und wurden uebersprungen.

Die Abfrage war auf hoechstens zwei Anfragen je Sekunde gedrosselt, tatsaechlich lag die Pause bei 0,55 Sekunden je Anfrage. Die Erhebung lief rund sieben Minuten und verursachte keinen einzigen Fehler und keine Sperre.

Die Stichprobe besteht bewusst aus zwei Teilen, weil eine reine Zufallsstichprobe Doppelungen systematisch unterschaetzt. Wenn ein Text in der Grundgesamtheit nur zweimal vorkommt, gelangen bei einer Stichprobe von wenigen Prozent so gut wie nie beide Exemplare in die Auswahl. Die gemessene Eindeutigkeitsquote einer Zufallsstichprobe ist deshalb immer zu hoch.

* **Teilstichprobe A, Zufall.** Zufaellig gezogene IDs ueber den gesamten belegten Bereich von rund 175.200 bis 185.800. Sie bildet die Programmmischung, die Textlaengen und die Verbreitung von Textbausteinen unverzerrt ab.
* **Teilstichprobe B, dichte Bloecke.** Drei zusammenhaengende ID-Bloecke (176.300 bis 176.460, 179.560 bis 179.720, 183.800 bis 183.960), in denen jede einzelne ID abgefragt wurde. Innerhalb eines Blocks ist das eine Vollerhebung. Da parallele Kurse einer Reihe gemeinsam angelegt werden und dadurch benachbarte IDs tragen, werden Doppelungen hier weitgehend sichtbar. Teilstichprobe B ist der belastbarere Schaetzer fuer die Wiederholungsquote, die drei Bloecke liegen in unterschiedlichen Programmbereichen.

Zwei Texte gelten als identisch, wenn sie nach Normalisierung zeichengleich sind. Normalisiert wurde nur der Leerraum: alle Folgen von Leerzeichen, Tabulatoren und Zeilenumbruechen wurden zu einem Leerzeichen zusammengezogen, fuehrender und abschliessender Leerraum entfernt. HTML blieb erhalten, Gross- und Kleinschreibung blieb unveraendert. Fuer die Bausteinanalyse wurden die Texte an Leerzeilen in Absaetze zerlegt und diese ebenso normalisiert.

## Stichprobenumfang

| Groesse | Wert |
| --- | --- |
| Angefragte IDs | 688 |
| Zurueckgelieferte Angebote | 489 (Trefferquote 71,1 Prozent) |
| Davon mit Beschreibungstext | 483 |
| Angebote ohne Beschreibungstext | 6 |
| Teilstichprobe A, Zufall | 141 Kurse mit Text |
| Teilstichprobe B, Bloecke | 342 Kurse mit Text |
| Anteil an rund 5.800 Veranstaltungen im Jahr | 8,3 Prozent |
| Fehlerhafte Anfragen | 0 |

Die Rohdaten liegen in `vhs-stichprobe-gross.json`, das Feld `stichprobe` kennzeichnet die Zugehoerigkeit zu A oder B.

## Messergebnisse

### Identische Gesamttexte

| Kennzahl | Gesamt | A (Zufall) | B (Bloecke) |
| --- | --- | --- | --- |
| Kurse mit Text | 483 | 141 | 342 |
| Verschiedene Texte | 380 | 128 | 259 |
| **Anteil eindeutiger Texte** | **78,7 Prozent** | **90,8 Prozent** | **75,7 Prozent** |
| Kurse, deren Text mindestens einmal identisch wiederkehrt | 161 (33,3 Prozent) | 21 (14,9 Prozent) | 129 (37,7 Prozent) |
| Texte, die nur einmal vorkommen | 322 | 120 | 213 |
| Groesste Gruppen identischer Texte | 15, 11, 6, 4, 4, 4, 4, 4 | 4, 4, 3, 2, 2 | 15, 11, 5, 4, 4, 3 |

Die groessten Gruppen im Einzelnen:

| Groesse | Beispieltitel | Textanfang |
| --- | --- | --- |
| 15 Kurse | Freies Zeichnen und Malen im Atelier | `Im Atelier „Libelle“ in Goldstein koennen Sie in einer kleinen Gruppe ...` |
| 11 Kurse | Regelmaessiges Gedaechtnistraining | `Jedes Gehirn braucht geistige Anregungen und kontinuierliches Training ...` |
| 6 Kurse | Excel 2024 I | `Anhand zahlreicher Uebungen erhalten Sie den effektiven Einstieg in die ...` |
| 4 Kurse | DaF Integrationskurs A2.2 | `Sie lernen in den Kursen der Niveaustufe A2 oft gebrauchte Ausdruecke ...` |
| 4 Kurse | Hatha Yoga | `Sie lernen grundlegende Asanas kennen und vertiefen Ihre Yogakenntnisse ...` |

Der Unterschied zwischen 90,8 und 75,7 Prozent ist kein Widerspruch, sondern der erwartete Verduennungseffekt der Zufallsstichprobe. Der niedrigere Wert aus den Blockdaten ist der realistischere.

### Textbausteine, also identische Absaetze in sonst verschiedenen Kursen

33 Absaetze kommen in mindestens fuenf verschiedenen Kursen vor, alle 33 sind laenger als 40 Zeichen. Die fuenf haeufigsten:

| Vorkommen | Anteil der Kurse | Laenge | Erste 80 Zeichen |
| --- | --- | --- | --- |
| 36 | 7,5 Prozent | 728 Zeichen | `– – – Gemaess Punkt 12 unserer AGBs gelten fuer <strong>Bildungsurlaube besondere S` |
| 24 | 5,0 Prozent | 149 Zeichen | `Aus dem VHS-Angebot: AKTIV IM ALTER Hier orientieren sich Inhalte, Lerntempo und` |
| 20 | 4,1 Prozent | 850 Zeichen | `<strong>Technische Hinweise</strong> Die Veranstaltung wird auf der Videokonfere` |
| 19 | 3,9 Prozent | 120 Zeichen | `Der Kurs ersetzt keine krankengymnastische Behandlung. Bei akuten Beschwerden em` |
| 19 | 3,9 Prozent | 119 Zeichen | `Bitte besorgen Sie sich die angegebenen Lehrbuecher im Buchhandel erst dann, wenn` |

Die Zeichenfolge am Anfang des haeufigsten Bausteins stammt aus den Quelldaten und dient dort als Trennlinie. Umlaute sind in dieser Tabelle transkribiert, in den Rohdaten stehen sie im Original.

Weitere Bausteine derselben Art sind der Hinweis auf die Anerkennung von Bildungsurlauben durch das Land Hessen (16 Kurse), der Link auf die Bildungsurlaubsseite (16 Kurse) und die Schritt-fuer-Schritt-Anleitung zur Beantragung von Bildungsurlaub (16 Kurse).

| Kennzahl | Wert |
| --- | --- |
| Absatzinstanzen insgesamt | 1.050 |
| Verschiedene Absaetze | 537 (51,1 Prozent) |
| Absaetze in mindestens 5 Kursen | 33 |
| Kurse mit mindestens einem solchen Baustein | 196 (40,6 Prozent) |
| Zeichenvolumen insgesamt | 430.486 |
| Davon in Bausteinen mit mindestens 5 Vorkommen | 147.108 (34,2 Prozent) |
| Zeichenvolumen ohne Absatzdubletten | 240.482 (55,9 Prozent) |
| Absaetze je Kurs | Median 2,0, Mittel 2,2 |

Auf Absatzebene ist die Wiederverwendung also deutlich hoeher als auf Ebene ganzer Texte. Rund die Haelfte des ausgelieferten Textvolumens besteht aus Absaetzen, die anderswo woertlich noch einmal stehen.

### Textlaenge

| Kennzahl | Mittelwert | Median | Minimum | Maximum |
| --- | --- | --- | --- | --- |
| Zeichen | 892 | 736 | 18 | 3.666 |
| Woerter | 115 | 98 | 1 | 426 |

### Verteilung ueber die Programmbereiche

Die erste Ziffer der Kursnummer trennt die Bereiche. Die Zuordnung der Inhalte wurde aus den Kurstiteln abgeleitet, ein eigenes Bereichsfeld liefert die Schnittstelle nicht.

| Ziffer | Inhalt laut Titeln | Kurse | Anteil | Eindeutige Texte |
| --- | --- | --- | --- | --- |
| 0 | Stadt, Region, Politik, Fuehrungen | 31 | 6,4 Prozent | 100 Prozent |
| 1 | Persoenlichkeit, Kommunikation, Psychologie | 27 | 5,6 Prozent | 89 Prozent |
| 2 | Kunst, Kultur, Kreativitaet | 66 | 13,7 Prozent | 70 Prozent |
| 3 | Gesundheit, Bewegung | 86 | 17,8 Prozent | 74 Prozent |
| 4 | Sprachen und Deutsch als Fremdsprache | 67 | 13,9 Prozent | 76 Prozent |
| 5 | Beruf, Karriere, Computer, Internet | 93 | 19,3 Prozent | 73 Prozent |
| 6 | Grundbildung | 8 | 1,7 Prozent | 75 Prozent |
| 7 | Junge VHS, Kinder und Jugendliche | 104 | 21,5 Prozent | 86 Prozent |
| 9 | Pruefungen und Zertifikate | 1 | 0,2 Prozent | 100 Prozent |

Die Wiederholungsquote ist also kein Randphaenomen einzelner Bereiche, sie zieht sich mit 70 bis 89 Prozent Eindeutigkeit durch fast alle Bereiche. Die Verteilung stuetzt zugleich die Annahme, ein Programmbereich entspreche grob einem Achtel des Angebots, auch wenn die Bereiche real zwischen etwa 2 und 21 Prozent schwanken.

### Unabhaengige Kennzahl der VHS selbst

Die VHS veroeffentlicht die Zahl neuer Angebote je Semester. Fuer das Programm Fruehjahr und Sommer 2026 nennt sie 2.835 Kurse und Veranstaltungen, davon 293 neu und 309 online. Fuer Herbst und Winter 2025/26 nennt sie rund 2.800 Kurse. Beide Semester zusammen ergeben rund 5.600 bis 5.700 Veranstaltungen im Jahr, was die im Einwand genannten 5.800 bestaetigt.

Aus 293 neuen von 2.835 Angeboten folgt ein Neuanteil von 10,3 Prozent je Semester, hochgerechnet rund 586 neue Angebote im Jahr. Diese Zahl misst genau das, worum es beim Pruefschritt geht: Texte, die tatsaechlich neu entstehen.

Quellen: Programmmeldung der VHS Frankfurt unter `https://vhs.frankfurt.de/de/news/tag/vhs-programm` und die Uebersicht der Programmbereiche unter `https://vhs.frankfurt.de/de/about/featured/fachbereiche-an-der-vhs`.

## Hochrechnung

Basis sind 5.800 Veranstaltungen im Jahr und drei Minuten Pruefzeit je zu pruefendem Text.

| Szenario | Zu pruefende Texte im Jahr | Aufwand | Grundlage |
| --- | --- | --- | --- |
| 1. Einwand, jede Veranstaltung einzeln | 5.800 | 290 Stunden | Annahme des Einwands |
| 2. Nur eindeutige Gesamttexte im laufenden Programm | rund 4.390 | rund 220 Stunden | gemessen, Teilstichprobe B |
| 3. Wie 2, aber Textbausteine nur einmal geprueft | entspricht 55,9 Prozent des Textvolumens | rund 162 Stunden | gemessen, Absatzebene |
| 4. Nur tatsaechlich neue Angebote im Jahr | rund 586 | rund 29 Stunden | Kennzahl der VHS |
| 5. Pilot in einem Programmbereich, nur neue Texte | rund 73 | rund 4 Stunden | Kennzahl der VHS, geteilt durch 8 |

Szenario 4 ist das fuer die Einfuehrung entscheidende. Der Pruefschritt greift bei der Neuanlage eines Textes, nicht bei jeder Wiederholung eines seit Jahren laufenden Kurses. Der Aufwand liegt dann bei rund 29 Stunden im Jahr, also etwa einer halben Stunde je Woche verteilt ueber acht Programmbereiche. Das entspricht rund vier Minuten je Bereich und Woche.

Szenario 5 beziffert den Pilotbetrieb: rund 73 neue Texte im Jahr, rund vier Stunden Pruefzeit insgesamt, also weniger als eine Stunde je Quartal.

Selbst das konservativste realistische Szenario 2, in dem jedes Semester saemtliche eindeutigen Texte erneut geprueft wuerden, liegt mit rund 220 Stunden um ein Viertel unter dem Einwand. Der Einwand von 290 Stunden ist damit rechnerisch die obere Grenze eines Falls, der praktisch nicht eintritt.

## Offengelegte Annahmen

**Gemessen an der Stichprobe von 483 Kursen:**

* Anteil eindeutiger Gesamttexte 75,7 Prozent (Blockdaten) bis 78,7 Prozent (Gesamtstichprobe)
* Anteil verschiedener Absaetze an allen Absatzinstanzen 51,1 Prozent
* Anteil des Textvolumens ohne Absatzdubletten 55,9 Prozent
* Mittlere Textlaenge 892 Zeichen und 115 Woerter
* Verteilung ueber die Programmbereiche

**Aus veroeffentlichten Angaben der VHS uebernommen, nicht selbst gemessen:**

* 2.835 Kurse und Veranstaltungen im Semester Fruehjahr und Sommer 2026, davon 293 neu
* rund 2.800 Kurse im Semester Herbst und Winter 2025/26
* acht Programmbereiche

**Gesetzte Annahmen, weder gemessen noch belegt:**

* 5.800 Veranstaltungen im Jahr als Rechenbasis, aus der Aufgabenstellung uebernommen und durch die Semesterzahlen ungefaehr bestaetigt
* drei Minuten Pruefzeit je Text, aus der Aufgabenstellung uebernommen
* ein Programmbereich entspricht einem Achtel des Angebots, aus der Aufgabenstellung uebernommen und durch die gemessene Verteilung nur grob gestuetzt
* der Neuanteil von 10,3 Prozent aus dem Fruehjahrssemester gilt auch fuer das Herbstsemester

## Einschraenkungen

1. **Momentaufnahme statt Jahresverlauf.** Die Schnittstelle zeigt das aktuell buchbare Programm. Wiederholungen ueber Semester hinweg, also der eigentliche Kern der Frage, lassen sich daraus nicht direkt messen. Deshalb stuetzt sich Szenario 4 auf die von der VHS selbst veroeffentlichte Zahl neuer Angebote.

2. **Definition von "neu" nicht dokumentiert.** Die 293 neuen Angebote stammen aus einer Programmankuendigung. Ob damit neue Kursthemen, neue Kursnummern oder auch ueberarbeitete Beschreibungen gemeint sind, geht aus der Quelle nicht hervor. Wenn zusaetzlich bestehende Texte redaktionell ueberarbeitet werden, steigt die Zahl der zu pruefenden Texte entsprechend. Das ist die groesste Unsicherheit der Rechnung, sie bewegt das Ergebnis zwischen rund 29 und rund 220 Stunden.

3. **Nur exakte Gleichheit gemessen.** Texte, die sich nur in einer Jahreszahl, einem Ort oder einem Namen unterscheiden, zaehlen hier als verschieden. Die tatsaechliche Wiederverwendung ist damit hoeher als gemessen. Alle Angaben zur Eindeutigkeit sind Obergrenzen.

4. **Blockannahme.** Teilstichprobe B unterstellt, dass parallele Kurse einer Reihe benachbarte IDs tragen. Das ist plausibel, weil die IDs in Anlagereihenfolge vergeben werden, aber nicht bewiesen. Gruppenmitglieder ausserhalb eines Blocks bleiben unsichtbar, auch B unterschaetzt die Wiederholung also eher.

5. **Nur das Portal.** Erfasst ist, was ueber die Portalschnittstelle ausgeliefert wird. Programmhefttexte, Vorworte und Bereichseinleitungen, die ebenfalls geprueft werden muessten, sind nicht enthalten. Sechs von 489 Angeboten hatten gar keinen Beschreibungstext.

6. **Bereichszuordnung abgeleitet.** Die Programmbereiche wurden aus der ersten Ziffer der Kursnummer und den Kurstiteln erschlossen, da die Schnittstelle kein gefuelltes Bereichsfeld liefert. Die Zuordnung ist fuer die Groessenordnung ausreichend, nicht fuer eine amtliche Statistik.

7. **Pruefzeit ungeprueft.** Die drei Minuten sind gesetzt. Ob ein KI-gestuetzter Pruefschritt in drei Minuten zu erledigen ist oder ob Nachbearbeitung und Klaerfaelle die Zeit verdoppeln, ist offen und sollte im Pilot gemessen werden. Eine Verdopplung auf sechs Minuten ergaebe in Szenario 4 rund 59 Stunden und in Szenario 5 rund 7 Stunden.

## Fazit

Der Einwand rechnet mit 5.800 einzeln zu pruefenden Texten. Gemessen sind auf 483 Kursen 24 Prozent exakte Volltextdubletten und 49 Prozent Absatzdubletten, dazu kommt laut Angaben der VHS ein Neuanteil von rund 10 Prozent je Semester. Der Pruefschritt trifft damit nicht 5.800 Texte im Jahr, sondern in der Groessenordnung 600. Der Jahresaufwand liegt bei rund 29 Stunden statt 290, im Pilotbetrieb eines Programmbereichs bei rund 4 Stunden. Offen bleibt, wie viele bestehende Texte zusaetzlich ueberarbeitet werden, das sollte im Pilot erhoben werden.
