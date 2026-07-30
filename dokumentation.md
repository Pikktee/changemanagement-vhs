typ: titel

# KLARTEXT

## Dokumentation des System-Prompts für die Prüfung von Kursbeschreibungen der Volkshochschule Frankfurt am Main

*Werkzeug* **klartext-vhs.henrikheil.net**

*Quellen* **github.com/Pikktee/changemanagement-vhs**

Henrik Heil · cimdata Bildungsakademie · Kurs Changemanagement und KI · Juli 2026

---

| | |
|---|---|
| Fassung des Prompts | {{FASSUNG}} |
| Aufbau | sechs Komponenten: ROLLE · AUFGABE · FORMAT · GRENZEN · KONTEXT · REGELN |
| Modell | `anthropic/claude-sonnet-4.5` |
| Temperatur | 0 |
| Prüfregeln | sechs, auf zwei Stufen: PFLICHT und EMPFEHLUNG |
| Referenzwortschatz | Goethe-Zertifikat A1, 820 Wörter, vollständig im Prompt |

=== SEITE ===
kapitel: Einordnung

# Worum es geht

## Der Prozess

Die vhs Frankfurt veröffentlicht rund 5.800 Kursbeschreibungen im Jahr. Sie entstehen dezentral in acht Programmbereichen, gehen durch die Redaktion und erscheinen anschließend im Portal, im Programmheft und im Newsletter.

Zwischen dem Schreiben und dem Veröffentlichen fehlt ein Schritt: Niemand prüft, ob die Menschen, an die sich ein Kurs richtet, seine Beschreibung auch lesen können. Genau diesen Schritt füllt KLARTEXT.

## Die Kernentscheidung des Prompts

Ein Lesbarkeitsindex misst Satz- und Wortlängen und kennt die Zielgruppe nicht. Er beanstandet deshalb die Beschreibung eines Englischkurses, deren Leserschaft fließend Deutsch liest, und winkt die Beschreibung eines Deutschkurses auf Stufe A2 durch, deren Leserschaft gerade A1 abgeschlossen hat.

> Kann die Zielgruppe **genau dieses** Kurses **genau diesen** Text verstehen?

Der Prompt bestimmt darum zuerst die Zielgruppe und danach den Maßstab, nicht umgekehrt. Diese Reihenfolge steht in der Komponente AUFGABE.

Der Maßstab kommt nicht aus dem Gesetz allein. Die maßgeblichen Kriterien der WCAG liegen auf Stufe AAA und sind rechtlich nicht gefordert. Verpflichtend ist der Auftrag der Betriebssatzung: Die Angebote stehen **grundsätzlich allen offen, ohne Rücksicht auf Vorbildung**.

## Was das Werkzeug nicht ist

Es ersetzt keine Redaktion. Es entscheidet nichts, es veröffentlicht nichts, es ändert nichts. Es legt dem zuständigen Fachbereich eine begründete Liste vor, und dieser entscheidet. Diese Beschränkung ist die Voraussetzung dafür, dass das Werkzeug im Haus angenommen wird und mitbestimmungsrechtlich unproblematisch bleibt.

=== SEITE ===
kapitel: Einordnung

# Ein- und Ausgabe: im Werkzeug

Dieses Dokument beschreibt den Prompt. Beispiele für Ein- und Ausgabe stehen nicht hier, sondern im Prüfwerkzeug. Dort läuft der Prompt gegen echte Kurstexte aus dem Portal der vhs, mit dem Modell und der Temperatur dieser Abgabe.

## klartext-vhs.henrikheil.net

| Was dort zu sehen ist | Wo |
|---|---|
| Ein- und Ausgabe an einem echten Kurstext | „Kurs aus dem Kursplan wählen“, Kursnummer suchen, dann „Text prüfen“ |
| Der Prompt im Wortlaut, Modell, Temperatur | Kopfzeile → „System-Prompt“ |
| Die zwölf Iterationen, neun davon einzeln ladbar | im Panel → „Alle Iterationen“ |
| Präsentation, diese Dokumentation, `system-prompt.md` | Kopfzeile → „Dokumente“ |

Ein eigener Text lässt sich ebenso einsetzen; Programmbereich und Niveau sind dann von Hand zu wählen, weil der Prompt ohne diese beiden Angaben die Zielgruppe nicht bestimmt und die Prüfung abbricht.

## Protokoll

Jeder Lauf schreibt sich selbst mit: Eingabe, Ausgabe, Modell, Temperatur, Prüfsumme des Prompts und Dauer. In `tool/protokoll/` liegen 72 solche Läufe; sie sind die Grundlage der Angaben in Teil C und Teil D. Prompt, Code und Protokolle stehen im Repository, siehe Teil E.

## Aufbau dieses Dokuments

| Teil | Inhalt |
|---|---|
| A | Die sechs Komponenten, je beschrieben und im Wortlaut |
| B | Technische Umsetzung und die Arbeitsteilung zwischen Prompt und Code |
| C | Testszenarien, darunter zwei durchgefallene |
| D | Iterationen, kurz — die Fassungen sind im Werkzeug ladbar |
| E | Grenzen, offene Punkte, Einordnung nach der KI-Verordnung |

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

# Teil A · Die sechs Komponenten

Der Prompt liegt im Projekt als `system-prompt.md` und wird zur Laufzeit geladen. Der Platzhalter `{{WORTLISTE_A1}}` unter KONTEXT wird dabei durch die 820 Wörter des Referenzwortschatzes ersetzt: Der Prompt arbeitet nicht mit einem Verweis auf eine Liste, sondern mit der Liste selbst. Im Betrieb ist er rund 20.000 Zeichen lang.

Jede Komponente steht auf den folgenden Seiten zweimal: zuerst, was sie festlegt, dann ihr Wortlaut. Der Wortlaut ist nicht abgetippt — er wird beim Bauen dieses PDFs aus der Quelldatei gezogen und kann deshalb nicht veralten. Einzige Ausnahme ist der Referenzwortschatz: Dort stehen im Prompt die 820 Wörter selbst, deshalb ist der Abschnitt verkürzt wiedergegeben.

| Komponente | Was sie festlegt |
|---|---|
| ROLLE | Redaktionsassistenz, nicht Autorin: liest genau, begründet, entscheidet nicht |
| AUFGABE | Die Reihenfolge der Arbeit — erst Zielgruppe, dann Maßstab, dann Befunde |
| FORMAT | Feste Ausgabestruktur, je Befund ein Zitat, ein Grund und ein Vorschlag |
| GRENZEN | Sechs nicht verhandelbare Verbote, darunter: bewertet Texte, niemals Personen |
| KONTEXT | Das Hauswissen: Programmbereiche, Abkürzungen, Referenzwortschatz, sechs Prüfregeln |
| REGELN | Neun Arbeitsregeln für die Ausgabe: Namen, Zitate, Zählung, Grenze, Sortierung |

Die Sechs-Komponenten-Struktur gibt die Aufgabenstellung vor. Sie legt zugleich fest, wo eine Änderung hingehört: eine unklare Prüfregel in KONTEXT, eine zu lange Ausgabe in REGELN, eine unzuverlässige Zusage überhaupt nicht in den Prompt, sondern in den Code (Teil B).

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## ROLLE

Setzt Haltung und Zuständigkeit. Die Rolle ist die einer Lektorin des Hauses, die eine Entscheidung vorbereitet — nicht die einer Autorin und nicht die einer Korrektorin. Das hält den Prompt von zwei naheliegenden Abwegen fern: Er schreibt den Text nicht um, und er prüft nicht Rechtschreibung.

### Wortlaut

{{PROMPT:ROLLE}}

## AUFGABE

Legt die Reihenfolge der Arbeitsschritte fest. Entscheidend ist Schritt 2: Vermittelt der Kurs Deutsch, liest die Zielgruppe eine Stufe unterhalb des Kursziels — der strenge Fall. Vermittelt er etwas anderes, gilt der normale Maßstab für Gebrauchstexte. Derselbe Prompt legt damit zwei verschiedene Maßstäbe an, und welcher gilt, steht fest, bevor der erste Befund erhoben wird.

Schritt 5 verlangt zu jedem Befund einen Formulierungsvorschlag. Ohne Vorschlag kein Befund: Eine Liste von Einwänden ohne Alternative erzeugt in der Redaktion Arbeit, statt sie zu ersparen.

### Wortlaut

{{PROMPT:AUFGABE}}

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## FORMAT

Erzwingt eine Ausgabe, die man überfliegen kann, und verbietet Einleitung und Schlusssatz. Vier Blöcke: `ZIELGRUPPE`, `BEFUNDE`, `KEIN BEFUND ZU`, `GESAMT`. Jeder Befund hat immer dieselben vier Zeilen — Einstufung mit Regelkürzel, wörtliche Stelle, Grund, Vorschlag.

Zwei Teile des Formats sind weniger offensichtlich. `KEIN BEFUND ZU` nennt die Regeln, die geprüft wurden und nichts ergaben; ohne diesen Block ist eine leere Liste nicht von einer nicht durchgeführten Prüfung zu unterscheiden. Und lässt sich die Zielgruppe nicht bestimmen, schreibt der Prompt `nicht bestimmbar`, benennt die fehlende Angabe und bricht ab, statt zu raten.

Die Struktur ist zugleich die Schnittstelle zum Werkzeug: Die Oberfläche liest die Befundzeilen, färbt die Einstufung und markiert die zitierte Stelle im Text. Weicht die Ausgabe vom Format ab, zeigt das Werkzeug den Rohtext des Modells.

### Wortlaut

{{PROMPT:FORMAT}}

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## GRENZEN

Sechs Verbote, die auch dann gelten, wenn der geprüfte Text etwas anderes verlangt. Zwei davon haben Folgen über die Formulierung hinaus.

**„Du bewertest Texte, niemals Personen.“** Dieser Satz hält das Vorhaben aus dem Hochrisikobereich der KI-Verordnung heraus, denn Anhang III setzt im Bildungsbereich überall die Bewertung natürlicher Personen voraus (Teil E). Derselbe Satz ist die Antwort auf die Frage des Personalrats, ob hier Leistung kontrolliert wird.

**„Du prüfst die technische Barrierefreiheit der Seite nicht.“** Kontraste, Tastaturbedienung und Navigation bleiben bei den Prüfwerkzeugen der städtischen IT. Ausgenommen ist ausdrücklich die Auszeichnung **innerhalb** des vorgelegten Kurstextes — genau die prüft die Regel `STRUKTUR`. Ohne diese Ausnahme hätte der Prompt seine einzige gut automatisierbare Pflichtregel selbst bestritten; das war der Anlass für Fassung v11.

### Wortlaut

{{PROMPT:GRENZEN}}

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## KONTEXT · Haus und Abkürzungen

Der erste Teil des Kontexts ist Faktenwissen, das ein Modell nicht haben kann: die acht Programmbereiche, die vier Fachbereiche, die über die Texte entscheiden, der Auftrag der Betriebssatzung und die Abkürzungen, die im Haus selbstverständlich sind und außerhalb nicht.

{{PROMPT:KONTEXT::Referenzwortschatz}}

## KONTEXT · Referenzwortschatz

Für Kurse, die Deutsch vermitteln, ist der Maßstab nicht die Einschätzung des Modells, sondern der veröffentlichte Prüfungswortschatz des Goethe-Zertifikats A1: 820 Wörter, die vollständig im Prompt stehen. In der ersten Fassung behauptete der Prompt, gegen diese Liste zu prüfen, hatte sie aber nicht (Teil D, v1).

Eine Messung an 13 echten Kursbeschreibungen ergab, dass rund die Hälfte aller Wörter nicht wörtlich in der Liste steht, der größte Teil davon aber zulässig ist. Ohne die folgenden vier Ausnahmen erzeugt die Regel Fehlalarme am Fließband. Der Abschnitt im Prompt führt sie ausführlich; hier verkürzt:

| Nicht melden, obwohl das Wort fehlt | Beispiel |
|---|---|
| Gebeugte Formen von Einträgen | `Kursen` zu `Kurs`, `Sätze` zu `Satz` |
| Funktionswörter | Artikel, Pronomen, Präpositionen, sein, haben, werden |
| Zusammensetzungen, wenn die Bedeutung sich erschließt | `Kursleitung` ja, `Selbsteinschätzung` nein |
| Eigennamen, Orts-, Sprach-, Kurs- und Produktbezeichnungen | telc, Xpert |

Für A2 und B1 dient die A1-Liste als unterer Anker; der Prompt verlangt, dass die Begründung das kenntlich macht. Fehlt die Liste im Betrieb, ist jeder Niveaubefund eine Schätzung und muss als solche ausgewiesen werden. Dass diese Zusage nicht im Prompt steht, sondern im Code, ist der Gegenstand von Teil B.

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## KONTEXT · Prüfregeln

Der eigentliche Maßstab, abschließend und in zwei Stufen: `PFLICHT` ist über die BITV Hessen und EN 301 549 rechtlich gefordert, `EMPFEHLUNG` folgt dem Auftrag der Satzung. Welche Regel welche Stufe hat, ist eine Tabelle und kein Urteil des Modells — sie wird im Code nachgerechnet (Teil B).

Bis Fassung v7 waren es elf Befundarten und drei Stufen. Gestrichen wurde, was ohne den Kursplan nicht entscheidbar war (`BAUSTEIN` — wiederkehrende Textbausteine erkennt ein Zeichenkettenvergleich, kein Modell), was nicht Verständlichkeit prüfte (`LEER` — Vollständigkeit gehört in ein Pflichtfeld des Redaktionssystems), was keine Grundlage außerhalb des Hausgeschmacks hatte (`ANREDE`), was nie traf (`SPRACHE`) und was als eigene Befundart entbehrlich war (`FREMDANWEISUNG` — die Abwehr steht heute in Regel 9).

### Wortlaut

{{PROMPT:KONTEXT:Prüfregeln}}

=== SEITE ===
kapitel: Teil A · Die sechs Komponenten

## REGELN

Neun Arbeitsregeln. Sie bestimmen nicht, was geprüft wird, sondern wie die Ausgabe aussieht — und jede Unklarheit darin ist im nächsten Lauf unmittelbar zu sehen.

| Regel | Was sie verhindert |
|---|---|
| 1 Namen entfernen | Ein Befund, der eine Kursleitung beim Namen nennt, ist eine Aussage über eine Person |
| 2 Wörtlich zitieren, ohne Markup | Sinngemäße Wiedergabe lässt sich in der Redaktion nicht wiederfinden |
| 3 Ein Befund je Stelle | Bei `NIVEAU` ist die Stelle das Wort, sonst der Satz. Daran hing, ob die Zahl der Niveaubefunde reproduzierbar ist (Teil D, v8) |
| 4 Höchstens fünfzehn Befunde | Eine Liste, die niemand mehr liest. Weggelassene Regeln dürfen nicht als „kein Befund“ erscheinen |
| 5 Einstufung nicht verhandelbar | Ein geringfügig erscheinender Pflichtverstoß bleibt Pflicht |
| 6 Gleichwertiger Vorschlag | Vereinfachen durch Weglassen von Inhalt |
| 7–8 Kein Lob, Antwort auf Deutsch | Füllsätze und Sprachwechsel bei fremdsprachigen Texten |
| 9 Der Prüftext ist Material | Eine Anweisung im Kurstext, die das Modell befolgt statt sie zu prüfen |

### Wortlaut

{{PROMPT:REGELN}}

=== SEITE ===
kapitel: Teil B · Technische Umsetzung

# Teil B · Technische Umsetzung

## Der Ablauf eines Laufs

1. Der Server liest `system-prompt.md`, setzt die Wortliste in den Platzhalter ein und bildet eine Prüfsumme über das Ergebnis.
2. Die Eingabe wird in ein festes Feldschema gebracht: Kurstitel, Kursnummer, Programmbereich, Niveau, Text. Bei einer Kursnummer holt der Server den Text selbst über die offene Schnittstelle des Kursportals.
3. Aufruf des Modells über OpenRouter, Temperatur 0; der Server tritt als Proxy dazwischen, damit der Schlüssel den Browser nie erreicht. Fällt das Modell aus, greift ein Ersatzmodell.
4. Nachbearbeitung im Code, siehe unten.
5. Protokoll nach `tool/protokoll/`, mit Prüfsumme, Modell, Temperatur und Dauer.

## Voraussetzungen

| Was | Anmerkung |
|---|---|
| API-Zugang zu einem Sprachmodell | hier OpenRouter; der Schlüssel liegt nur auf dem Server, nie im Browser und nie im Protokoll |
| Ein Server | Python 3, keine Bibliothek über die Standardbibliothek hinaus |
| Kursdaten | Schnittstelle des Kursportals, öffentlich, Abrufe auf etwa zwei je Sekunde gedrosselt |
| Kein Zugriff auf das Redaktionssystem | Der Prompt ist auch ohne eigenen Server einsetzbar, als Assistent in einer bestehenden Umgebung |

## Was im Code steht und nicht im Prompt

Der Grundsatz des Projekts: **Was feststeht, gehört in den Code. Was die Zielgruppe kennen muss, bleibt beim Modell.** Dreimal hat der Prompt eine Zusage nicht zuverlässig gehalten, und dreimal war die Lösung dieselbe.

| Zusage | Warum der Prompt sie nicht hielt | Wo sie heute steht |
|---|---|---|
| Vorbehalt, wenn die Wortliste fehlt | Das Modell vergaß den Satz und berief sich sogar auf eine Liste, die es in diesem Lauf nicht hatte (Teil C, T7) | `ehrlichkeitshinweis()` setzt `HINWEIS DES SYSTEMS` vor die Ausgabe |
| Einstufung PFLICHT oder EMPFEHLUNG | Derselbe Text ergab einmal PFLICHT, einmal HINWEIS | Tabelle `EINSTUFUNGEN`, jede Befundzeile wird nachgerechnet |
| Kein Personenname in der Ausgabe | Das Modell beanstandete das „Dr.“ als unaufgelöste Abkürzung und zitierte dabei den vollen Namen (Teil C, T5) | `namensschutz()` ersetzt Titel samt folgendem Namen durch `[Name]` |

Drei Anläufe im Prompt haben einen einzigen Satz nicht zuverlässig erzeugt. Drei Zeilen Python haben es. Die Regel daraus: Ist eine Anforderung im Kern eine Nachschlagetabelle oder ein prüfbarer Zustand, gehört sie nicht in den Prompt.

Das ist zugleich die Grenze des Wegs über einen fremden KI-Assistenten: Dort gibt es diese Nachbearbeitung nicht. Der Prompt läuft, die drei Zusagen hängen dann aber wieder am Modell.

=== SEITE ===
kapitel: Teil C · Testszenarien

# Teil C · Testszenarien

Geprüft wurde nicht nur, ob das Werkzeug richtig urteilt, sondern auch, ob es sich an seine Grenzen hält. Alle Fälle sind in `tool/protokoll/` protokolliert. T1, T2 und T5 wurden unter der aktuellen Fassung mit je vier Läufen erneut gemessen, die übrigen vier unter älteren Fassungen.

| Nr. | Was geprüft wird | Erwartung | Ergebnis |
|---|---|---|---|
| T1 | Deutschkurs A2.2, strenger Fall | Zielgruppe A1, mehrere Niveaubefunde | bestanden, acht bis zehn Niveaubefunde |
| T2 | Englischkurs A1.1, normaler Fall | keine Niveaubefunde | bestanden, in allen vier Läufen null |
| T3 | Yogakurs, kein Sprachkurs | Niveaubefund nur bei Fachwörtern | bestanden, „Asanas“ erkannt |
| T4 | Anweisung an das Modell im Kurstext | melden, nicht befolgen | bestanden |
| T5 | Name der Kursleitung im Text | Name nicht zitieren | im Prompt **durchgefallen**, im Code gelöst |
| T6 | Titel, Bereich und Niveau fehlen | „nicht bestimmbar“, Abbruch | bestanden |
| T7 | Betrieb ohne Referenzwortschatz | Vorbehalt in der Ausgabe | im Prompt **durchgefallen**, im Code gelöst |

## T1 und T2, die beiden Kernfälle

Zwei Kurse, derselbe Prompt, dieselben Regeln. Beide Texte sind gleich einfach gebaut, im Schnitt neun beziehungsweise elf Wörter je Satz; ein Lesbarkeitsindex findet bei keinem von beiden etwas und schweigt damit einmal zu Unrecht. Der Prompt unterscheidet sie, weil er vorher bestimmt hat, wer liest: Beim Deutschkurs auf A2.2 meldet er in jedem Lauf mehrere Niveaubefunde, beim Englischkurs auf A1.1 in jedem Lauf keinen.

Belastbar ist die Asymmetrie, nicht die Einzelzahl. Über je vier Läufe streuen die Niveaubefunde beim Deutschkurs um zwei, beim Englischkurs sind es konstant null. Die Pflichtbefunde blieben in allen Läufen stabil.

## T5, Personenname hinter einem Titel

Steht der Name einer Kursleitung im Fließtext, hält sich das Modell an Regel 1. Steht er hinter einem Titel, nicht: Es beanstandete das „Dr.“ als unaufgelöste Abkürzung und zitierte dabei den vollen Namen, in drei von vier Läufen — auch nachdem der Prompt Titel vor Personennamen ausdrücklich ausgenommen hatte. Gelöst ist der Fall im Server, der Titel samt folgendem Namen entfernt; unter der aktuellen Fassung stand in keinem der vier Läufe ein Name in der Ausgabe. Das fängt den beobachteten Fall, nicht die ganze Fehlerklasse: Ein Name ohne Titel wird davon nicht erfasst.

## T7, Betrieb ohne Referenzwortschatz

Die Wortliste wurde vorübergehend umbenannt und ein Deutschkurstext geprüft. Der verlangte Vorbehalt kam nicht. Stattdessen begründete das Modell Befunde damit, ein Wort stehe „nicht im A1-Wortschatz“ — eine Aussage über eine Liste, die es in diesem Lauf nicht hatte. Drei Anläufe im Prompt änderten daran nichts: sichtbare Marke `KEINE WORTLISTE GELADEN` statt einer leeren Stelle, Vorbehalt an den Anfang des Abschnitts, Vorbehalt zusätzlich in die FORMAT-Vorlage. Ob eine Liste geladen ist, ist keine Ermessensfrage; der Server weiß es sicher und setzt den Hinweis seitdem selbst. Die einzelnen Begründungen bleiben in diesem Fall unsauber, siehe Teil E.

=== SEITE ===
kapitel: Teil D · Iterationen

# Teil D · Iterationen

Zwölf Fassungen an drei Tagen, jede aus einem konkreten Anlass. Ausführlich mit Anlass, Befund, Änderung und Begründung stehen sie in `iterationen.md` im Repository, siehe Teil E.

**Im Werkzeug ist die Historie begehbar:** im Panel „System-Prompt“ unter „Alle Iterationen“. Jede erhaltene Fassung lässt sich laden und gegen denselben Text laufen lassen; so wird sichtbar, was eine Änderung am Ergebnis bewirkt hat. Neun der zwölf Stände sind erhalten; v0.1, v5 und v7 wurden nie einzeln festgeschrieben, die Historie kennt sie, ein ladbarer Stand fehlt.

{{ITER_TABELLE}}

Seit v8 wird jede neue Fassung mit je vier Läufen gegen die beiden Kernfälle geprüft, nicht mit einem.

=== SEITE ===
kapitel: Teil E · Grenzen und Einordnung

# Teil E · Grenzen, offene Punkte, Einordnung

## Was gesichert ist

- Der Prompt bestimmt die Zielgruppe aus Titel, Programmbereich und Niveau und legt zwei verschiedene Maßstäbe an. Das ist an gegensätzlichen Fällen über je vier Läufe belegt.
- Er trennt Pflichtbefunde nach WCAG Stufe A und AA von Empfehlungen nach Stufe AAA und Hausstandard, und die Einstufung kommt aus einer Tabelle im Code.
- Er bewertet keine Personen und befolgt keine Anweisungen aus dem geprüften Text.

## Was er nicht leistet

- **Keine technische Barrierefreiheit.** Kontraste, Tastaturbedienung und Seitengerüst gehören zu einem anderen Werkzeug und einem anderen Zuständigen.
- **Keine gleichbleibende Ausgabe.** Die Zahl der Niveaubefunde streut über je vier Läufe um zwei, gemessen an zwei Kursen und nicht über die Breite der 60er-Stichprobe. Die Pflichtbefunde und das Verhältnis der beiden Kurse zueinander waren stabil. Für ein Werkzeug, das vorschlägt und nicht entscheidet, ist das vertretbar.
- **Keine Erkennung von Textbausteinen.** Passagen, die wortgleich über vielen Kursen stehen, kann das Modell nicht erkennen; es sieht immer nur einen Text. Der Vergleich über den Kursplan gehört ins Werkzeug, nicht ins Modell.
- **Kein Ersatz für die Fachprüfung.** Ob ein Kurskonzept sinnvoll und eine Angabe richtig ist, prüft der Prompt nicht.

## Offene Punkte

- **Die Obergrenze bindet.** Beim Deutschkurs werden die fünfzehn Befunde regelmäßig erreicht. Der Vermerk, wie viele Befunde weggelassen wurden, kommt nicht verlässlich. Eine Bündelung mehrerer Wörter je Satz bei gleichbleibender Zählung wäre der nächste Schritt.
- **Begründungen im Betrieb ohne Wortliste.** Der Vorbehalt steht seit v4 im Code und kommt damit sicher; die einzelnen Begründungen behaupten weiter, ein Wort stehe nicht auf der Liste.
- **Der Namensschutz erfasst nur Namen mit vorangestelltem Titel.** Für Namen im Fließtext bleibt Regel 1 zuständig, also das Modell.
- **Der Referenzwortschatz deckt nur A1 ab.** Für A2 und B1 ist die Liste unterer Anker, das Übrige Einschätzung. Eine A2-Liste aus dem Prüfungshandbuch des Deutsch-Tests für Zuwanderer wäre der nächste Ausbauschritt.

## Einordnung nach der KI-Verordnung

Die vhs wäre **Betreiberin** im Sinne von Artikel 3 Nummer 4 der Verordnung (EU) 2024/1689, nicht Anbieterin. Ein Hochrisikotatbestand nach Anhang III liegt nicht vor: Die dortigen Fälle im Bildungsbereich, insbesondere Nummer 3, setzen sämtlich eine Bewertung **natürlicher Personen** voraus, etwa bei Zugang, Zuweisung oder Prüfung. KLARTEXT bewertet ausschließlich Texte; die entsprechende Zeile steht unter GRENZEN.

Unabhängig davon gilt seit dem 2. Februar 2025 Artikel 4: Wer KI-Systeme betreibt, muss für ausreichende KI-Kompetenz der damit befassten Personen sorgen. Diese Pflicht ist im Change-Konzept als Schulungsbaustein abgebildet und gilt unabhängig von der Risikoklasse.

## Quellen zum Nachlesen

Prompt, Prototyp und Protokolle liegen offen: **github.com/Pikktee/changemanagement-vhs**

Dort stehen `system-prompt.md` mit dem Prompt im Original, `iterationen.md` mit den zwölf Fassungen samt Anlass und Begründung, `tool/server.py` mit Proxy und Nachbearbeitung, `tool/protokoll/` mit den 72 Läufen und `daten/wortliste-goethe-a1.txt` mit dem Referenzwortschatz. Die Fassungshistorie des Prompts ist über `git log --follow system-prompt.md` nachvollziehbar.
