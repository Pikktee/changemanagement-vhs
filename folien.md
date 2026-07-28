# KLARTEXT — Foliendatei
#
# Das ist die EINZIGE Datei, die du bearbeitest.
# Danach: python3 build.py     (oder watch.py laufen lassen)
#
# Regeln:
#   "## " beginnt eine neue Folie. Der Text dahinter ist nur ein Merkzettel
#         fuer dich und erscheint nirgends auf der Folie.
#   "schluessel: wert"  setzt ein Feld.
#   "schluessel:" allein, dann Zeilen mit "- ", ergibt eine Liste.
#   "### NOTIZ" leitet den Sprechtext ein. Alles danach bis zur naechsten
#         Folie ist Referentennotiz und landet in der PowerPoint.
#   **fett** funktioniert in allen Texten.
#
# Folientypen: titel, schluss, kapitel, punkte, zahlen, zweispalt,
#              tabelle, zitat, text
# Alle Felder pro Typ stehen in README-FOLIEN.md


## 1 — Titelfolie

typ: titel
titel: Wer Deutsch lernen will,
akzent: muss erst Deutsch können.
untertitel: Ein KI-gestützter Prüfassistent für die Kursbeschreibungen der Volkshochschule Frankfurt am Main.
fussl: ABSCHLUSSPROJEKT · CHANGE UND KI
fussr: CIMDATA · HENRIK HEIL · JULI 2026
bild: bilder/01-titel-wand.jpg
bildprompt: Kleine Figur vor einer Wand aus dichten horizontalen Balken, ein schmaler Durchgang. Flach-geometrisch, Bauhaus, Palette Petrol/Papier/Mint/Orange, keine Schrift.

### NOTIZ

Ich stelle euch heute mein Abschlussprojekt vor. Es geht um die
Volkshochschule Frankfurt und um einen Prozess, den man leicht übersieht:
das Schreiben von Kursbeschreibungen.

Der Titel ist der Befund, mit dem alles angefangen hat. Die Volkshochschule
bietet Deutschkurse für Menschen an, die gerade erst Deutsch lernen. Und die
Beschreibungen dieser Kurse sind in einem Deutsch geschrieben, das man erst
nach dem Kurs versteht.

Alle Zahlen, die ihr gleich seht, habe ich selbst gemessen, an der echten
Website, am 28. Juli. Der Datensatz liegt der Arbeit bei.


## 2 — Executive Summary

typ: punkte
kapitel: ÜBERBLICK
bild: bilder/02-teile-ganzes.jpg
bu: Sechs Teile, ein Bild.
bildprompt: Einzelne geometrische Formen, die sich zu einer geordneten Komposition fuegen. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Das Ganze
akzent: in sechs Sätzen.
punkte:
  - "**Ausgangslage** || Die vhs Frankfurt veröffentlicht rund 5.800 Kursbeschreibungen im Jahr. Niemand prüft sie vor der Veröffentlichung auf Verständlichkeit."
  - "**Befund** || In einer Stichprobe von 60 Kursen haben 90 Prozent mindestens einen Befund. Beschreibungen von Deutschkursen liegen sprachlich über dem Niveau ihrer Zielgruppe."
  - "**Ziel** || Jeder Kurstext wird vor der Veröffentlichung gegen die Zielgruppe genau dieses Kurses geprüft."
  - "**Lösung** || Ein System-Prompt im bereits vorhandenen KI-Rahmen des Volkshochschul-Verbands. Keine Beschaffung, kein neuer Vertrag."
  - "**Abgrenzung** || Technische Barrierefreiheit prüft weiterhin ein deterministisches Werkzeug. Die KI übernimmt nur, was Urteil verlangt."
  - "**Ergebnis** || Befundquote nach drei Monaten unter 40 Prozent statt heute 90. Alle neuen Texte im Pilotbereich geprüft. Messung mit demselben Skript, das den Ausgangswert erhoben hat."
callout: Ich bitte um Freigabe eines Pilotprojekts in einem Programmbereich, drei Monate, ohne Beschaffung.
calloutsub: Der Prompt schlägt vor, der Mensch entscheidet und veröffentlicht.

### NOTIZ

Bevor ich ins Detail gehe, das Ganze in der Kurzfassung.

Die Volkshochschule veröffentlicht rund fünftausendachthundert
Kursbeschreibungen im Jahr. Diese Texte entstehen in acht Programmbereichen,
und niemand prüft sie vor der Veröffentlichung darauf, ob die Zielgruppe sie
versteht.

Ich habe eine Stichprobe von sechzig Kursen gezogen. Neun von zehn Texten
haben mindestens einen Befund. Der wichtigste: Bei Deutschkursen liegt die
Beschreibung sprachlich über dem Niveau, das der Kurs erst vermitteln soll.

Mein Vorschlag ist ein System-Prompt, der jeden Text gegen die Zielgruppe
genau dieses Kurses prüft. Das Besondere daran: Die technische Grundlage
existiert bereits, der Volkshochschul-Verband hat einen datenschutzkonformen
KI-Rahmen für alle Volkshochschulen. Es muss nichts beschafft werden.

Und eine Abgrenzung, die mir wichtig ist: Für die technische Barrierefreiheit
bleibt ein normales Prüfwerkzeug zuständig. Die KI übernimmt nur den Teil, der
Urteil verlangt.

Der Satz unten ist das Leitprinzip: Der Prompt schlägt vor, der Mensch
entscheidet.


## 3 — Das Unternehmen

typ: zahlen
kapitel: 01 · UNTERNEHMEN
bild: bilder/03-unternehmen.jpg
bu: Ein Haus, das allen offensteht. So steht es in der Betriebssatzung.
bildprompt: Gebaeude aus einfachen Bloecken, davor kleine Figuren, die hineingehen. Flach-geometrisch, Bauhaus, Palette Petrol/Papier/Mint/Orange, keine Schrift.
titel: Ein Eigenbetrieb mit
akzent: kommunalem Auftrag.
lede: Volkshochschule Frankfurt am Main, gegründet 1890, größte öffentliche Weiterbildungseinrichtung Hessens.
zahlen:
  - "5.800 || Veranstaltungen im Jahr"
  - "8 || Programmbereiche, von Sprachen bis Grundbildung"
  - "16 || Mitglieder der Betriebskommission, darunter zwei des Personalrats"
  - "154 T€ || Stammkapital als Eigenbetrieb"
callout: Auftrag laut Betriebssatzung: Die Angebote stehen grundsätzlich allen offen, ohne Rücksicht auf Vorbildung.
quellen: Betriebssatzung der vhs Frankfurt, Impressum, Selbstdarstellung

### NOTIZ

Zunächst das Unternehmen.

Die Volkshochschule Frankfurt ist kein Amt, sondern ein Eigenbetrieb der
Stadt nach dem Eigenbetriebsgesetz. Sie wird kaufmännisch geführt, hat ein
Stammkapital und einen Wirtschaftsplan. Geleitet wird sie von einem Direktor,
der laut Impressum auch persönlich für die redaktionellen Inhalte der Website
verantwortlich ist. Das ist für mein Projekt nicht unwichtig.

Darüber steht eine Betriebskommission mit sechzehn Mitgliedern: Stadtverordnete,
Magistratsmitglieder und zwei Vertretungen des Personalrats. Diese zwei Sitze
werden später noch eine Rolle spielen.

Achtzehnhundertneunzig gegründet, größte öffentliche Weiterbildungseinrichtung
Hessens, acht Programmbereiche, rund fünftausendachthundert Veranstaltungen im
Jahr.

Der Satz unten stammt wörtlich aus der Betriebssatzung. Die Angebote stehen
grundsätzlich allen offen, ohne Rücksicht auf Vorbildung. Daran messe ich das
Haus im Folgenden. Nicht am Gesetz, sondern an seinem eigenen Anspruch.


## 4 — Der Prozess heute

typ: punkte
kapitel: 01 · IST-ANALYSE
bild: bilder/04-prozess-luecke.jpg
bu: Vier Schritte, eine fehlende Verbindung.
bildprompt: Vier Kreise in einer Reihe, verbunden durch Linien, die Verbindung zwischen drittem und viertem Kreis fehlt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Wie ein Kurstext
akzent: heute entsteht.
punkte:
  - "Die Programmbereichsleitung plant den Kurs und gewinnt eine Kursleitung."
  - "Der Beschreibungstext wird geschrieben, oft von der Kursleitung zugeliefert."
  - "Der Text wird in das Kursverwaltungssystem eingepflegt."
  - "Er erscheint unverändert im Portal, im Programmheft und im Newsletter."
callout: Zwischen Schritt drei und vier prüft niemand, ob die Zielgruppe den Text versteht.
calloutsub: Es gibt keine Freigabestufe für Verständlichkeit. Das ist keine Nachlässigkeit, es ist schlicht kein Arbeitsschritt.

### NOTIZ

Jetzt die Ist-Analyse. Der Prozess hat vier Schritte.

Erstens: Die Programmbereichsleitung plant den Kurs und sucht eine Kursleitung.
Zweitens: Der Beschreibungstext entsteht, häufig liefert die Kursleitung ihn zu.
Drittens: Der Text wird ins Kursverwaltungssystem eingepflegt. Viertens: Er
erscheint im Portal, im zweihundertvierzig Seiten starken Programmheft und im
Newsletter.

Und jetzt der entscheidende Punkt: Zwischen Schritt drei und vier passiert
nichts. Es gibt keine Prüfstufe für Verständlichkeit.

Das ist ausdrücklich kein Vorwurf. Es ist kein Arbeitsschritt, der irgendwo
vorgesehen wäre. Genau deshalb ist es ein Fall für Prozessgestaltung und nicht
für einen Appell, sich mehr Mühe zu geben.

Zwei Einschränkungen, die ich offenlege: Den genauen Redaktionsablauf der vhs
Frankfurt konnte ich nicht belegen, es gibt dazu keine öffentliche
Dokumentation. Was ihr seht, ist die branchenübliche Rollenverteilung aus
Stellenausschreibungen von Volkshochschulverbänden. Das ist eine begründete
Annahme, keine Messung.


## 5 — Die Messung

typ: zahlen
kapitel: 01 · POTENZIAL
bild: bilder/05-raster.jpg
bu: 60 geprüfte Texte. Die wenigen hellen Felder sind die ohne Befund.
bildprompt: Dichtes Raster kleiner Quadrate, die grosse Mehrheit orange, nur wenige in einer Ecke petrol. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Neun von zehn Texten
akzent: haben einen Befund.
lede: Stichprobe von 60 Kursbeschreibungen über sieben der acht Programmbereiche, gezogen über die öffentliche Schnittstelle des Kursportals am 28. Juli 2026.
zahlen:
  - "90 % || der Texte mit mindestens einem Befund || warn"
  - "55 % || mit ungeklärten Abkürzungen wie DaF, DTZ, C1.2"
  - "50 % || mit mindestens einem Satz über 25 Wörtern"
  - "74 || Wörter im längsten gemessenen Satz || warn"
callout: Nur 6 der 60 Texte blieben ohne jeden Befund.
quellen: eigene Erhebung, Datensatz liegt der Arbeit bei

### NOTIZ

Damit zur Potenzialermittlung. Und hier wird es konkret, denn ich habe nicht
geschätzt, sondern gemessen.

Das Kursportal der vhs hat eine offene Schnittstelle. Darüber habe ich eine
Stichprobe von sechzig Kursbeschreibungen aus sieben der acht Programmbereiche
gezogen und automatisch ausgewertet. Der Datensatz liegt der Arbeit bei, jede
Zahl ist nachrechenbar.

Neunzig Prozent der Texte haben mindestens einen Befund. Fünfundfünfzig Prozent
enthalten Abkürzungen, die nirgends erklärt werden. Die Hälfte hat mindestens
einen Satz mit über fünfundzwanzig Wörtern, der längste hat
vierundsiebzig Wörter.

Sechs von sechzig Texten waren ohne jeden Befund.

Ich sage gleich dazu, was diese Zahlen nicht sind: Sie sind kein Nachweis von
Rechtsverstößen. Warum, zeige ich auf der übernächsten Folie.


## 6 — Der eigentliche Befund

typ: tabelle
kapitel: 01 · POTENZIAL
bild: bilder/06-zwei-blicke.jpg
bu: Zwei Leserschaften, ein Text.
bildprompt: Zwei Figuren betrachten dasselbe Rechteck, links offen und klar, rechts durch dichte Streifen verdeckt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Dieselbe Zahl bedeutet
akzent: zweimal etwas anderes.
spalten: Kurs | Ø Satzlänge | längster Satz | Zielgruppe liest Deutsch
zeilen:
  - "Englisch A1.1 | 21,3 Wörter | 41 Wörter | + fließend"
  - "DaF Deutsch 4 A2.2 | 10,6 Wörter | 16 Wörter | ! auf A2-Niveau"
callout: Ein Lesbarkeitswerkzeug würde hier den falschen Kurs beanstanden.
quellen: eigene Erhebung, 17 Sprachkurse mit Niveauangabe in der Stichprobe

### NOTIZ

Das hier ist der Befund, auf dem mein ganzes Projekt steht. Ich bitte um einen
Moment Aufmerksamkeit, weil er auf den ersten Blick unscheinbar aussieht.

Oben ein Englischkurs auf Stufe A1, unten ein Deutschkurs auf Stufe A2.

Der Englischkurs hat eine Beschreibung mit durchschnittlich einundzwanzig
Wörtern pro Satz, der längste Satz hat einundvierzig. Der Deutschkurs hat
knapp elf Wörter pro Satz, der längste sechzehn.

Ein Lesbarkeitsindex, ein Textprüfprogramm oder ein Standard-KI-Assistent
würde jetzt den Englischkurs beanstanden und den Deutschkurs durchwinken. Und
das ist genau falsch herum.

Denn der Englischkurs richtet sich an Menschen, die fließend Deutsch lesen. Für
die ist ein langer Satz unschön, aber kein Hindernis. Der Deutschkurs richtet
sich an Menschen, die Deutsch auf A2-Niveau lesen. Für die ist jedes Wort
oberhalb dieses Niveaus eine Hürde.

Und deshalb reicht kein Werkzeug, das nur den Text ansieht. Man muss wissen,
für wen der Text ist. Neun von dreizehn Kursen für Deutschlernende enthalten
Wörter wie Selbsteinschätzung, Fehleinschätzung und Umbuchung. Das ist
C1-Vokabular über einem A2-Kurs.

Das ist der Punkt, an dem ein fachlich eingestellter Prompt etwas kann, was ein
Standardwerkzeug nicht kann.


## 7 — Rechtslage und Einführung

typ: text
kapitel: 01 · EINORDNUNG
bild: bilder/11-zeitleiste.jpg
bu: Von der UN-Konvention bis zur hessischen Verordnung.
bildprompt: Waagerechte Zeitleiste als dicker Balken mit unterschiedlich hohen Markierungen. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Welches Recht hier
akzent: überhaupt gilt.
klein: ja
absaetze:
  - "Digitale Barrierefreiheit heißt: Websites und Anwendungen müssen so gebaut sein, dass auch Menschen mit Behinderung sie nutzen können. Der technische Maßstab dafür sind die **WCAG**, eine internationale Richtlinie mit drei Stufen."
  - "Die Kette beginnt 2009 mit der **UN-Behindertenrechtskonvention**, führt über die **EU-Richtlinie 2016/2102** für öffentliche Stellen und mündet 2025 im **Barrierefreiheitsstärkungsgesetz** für Unternehmen."
  - "Für die vhs Frankfurt gilt keines davon direkt. Als kommunale Einrichtung in Hessen greift **Landesrecht**: § 14 HessBGG und die **BITV HE** von 2019. Gefordert ist Konformitätsstufe **AA**."
callout: Nicht die BITV 2.0 des Bundes. Das ist der häufigste Zitierfehler kommunaler Stellen.
quellen: HessBGG, BITV HE 2019, EN 301 549, Landesfachstelle Barrierefreie IT Hessen

### NOTIZ

Bevor ich zur Lösung komme, kurz die Rechtslage. Ich halte mich knapp, weil
das nicht der Kern meiner Arbeit ist, aber ohne diese Folie fehlt der Rahmen.

Digitale Barrierefreiheit bedeutet, dass eine Website auch für Menschen mit
Behinderung nutzbar sein muss. Der technische Maßstab sind die WCAG, eine
internationale Richtlinie mit drei Stufen: A, doppel A und dreifach A.

Die Rechtskette beginnt 2009 mit der UN-Behindertenrechtskonvention. Dann kam
2016 die EU-Richtlinie für öffentliche Stellen, und seit Juni 2025 gilt das
Barrierefreiheitsstärkungsgesetz für Unternehmen.

Für die vhs gilt keines davon unmittelbar. Sie ist eine kommunale Einrichtung
in Hessen, und damit greift Landesrecht: Paragraph vierzehn des Hessischen
Behindertengleichstellungsgesetzes und die hessische Verordnung von 2019.
Gefordert wird Stufe doppel A.

Der Satz unten ist wichtiger, als er aussieht. Sehr viele kommunale Stellen
berufen sich auf die BITV 2.0 des Bundes. Die gilt für Bundesbehörden, nicht
für Kommunen. Wer das verwechselt, prüft am falschen Maßstab.

Eine Randnotiz für Nachfragen: Die hessische Verordnung tritt Ende 2027 außer
Kraft, und sie verweist dynamisch auf die jeweils gültige europäische Norm.
Der Maßstab kann sich also ändern, ohne dass ein Gesetz geändert wird.


## 8 — Pflicht und Kür

typ: tabelle
kapitel: 01 · EINORDNUNG
bild: bilder/07-stufen.jpg
bu: Zwei Stufen sind gebaut. Die dritte ist nur gedacht.
bildprompt: Treppe aus drei Stufen, die unteren zwei massiv petrol, die oberste nur als duenner Umriss. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Was Pflicht ist,
akzent: und was nicht.
klein: ja
spalten: Kriterium nach WCAG 2.1 | Stufe | bei AA verbindlich
zeilen:
  - "1.3.1 Struktur programmatisch bestimmbar | A | + ja"
  - "2.4.2 Seite mit aussagekräftigem Titel | A | + ja"
  - "3.1.2 Sprache von Textteilen ausgezeichnet | AA | + ja"
  - "3.1.4 Abkürzungen erklärt | AAA | ! nein"
  - "3.1.5 Leseniveau der Zielgruppe angemessen | AAA | ! nein"
callout: Ausgerechnet die Kriterien für Menschen mit geringer Vorbildung sind optional.
quellen: WCAG 2.1, HessBGG und BITV HE, Landesfachstelle Barrierefreie IT Hessen

### NOTIZ

Diese Folie habe ich eingebaut, weil ich beim Recherchieren selbst falsch lag
und die Korrektur das Projekt verbessert hat.

Für die vhs als kommunale Einrichtung in Hessen gilt Landesrecht, das
Hessische Behindertengleichstellungsgesetz und die hessische Verordnung dazu.
Verlangt wird die Konformitätsstufe AA.

Und jetzt schaut euch die Tabelle an. Dass Struktur programmatisch bestimmbar
sein muss, ist Stufe A, also Pflicht. Dass Textteile in anderen Sprachen
ausgezeichnet werden, ist AA, also Pflicht.

Aber: Dass Abkürzungen erklärt werden, ist Stufe AAA. Und dass das Leseniveau
zur Zielgruppe passt, ist ebenfalls AAA. Beides ist also **nicht** verbindlich.

Drei Dinge lege ich offen, bewusst genau formuliert.

Erstens: Für Websites von Kommunen in Hessen besteht keine Pflicht zu Leichter
Sprache oder Gebärdensprache, die hessische Verordnung adressiert dort nur
Landesstellen. Aber Paragraph zwölf a des Hessischen
Behindertengleichstellungsgesetzes enthält eine Soll-Vorschrift: Träger
öffentlicher Gewalt sollen mit Menschen mit geistigen oder seelischen
Behinderungen in leicht verständlicher Sprache kommunizieren, und das gilt auch
für Kommunen. Die vhs bietet ihre Rubrik Einfache Sprache also freiwillig an,
bewegt sich damit aber nicht im luftleeren Raum.

Zweitens, und das ist für meine Argumentation der wichtigste Punkt: Nicht Teil
der doppel-A-Konformität heißt nicht rechtlich irrelevant. Paragraph drei
Absatz eins der hessischen Verordnung verlangt eigenständig, dass Angebote
verständlich sind. Die Konformitätsstufe begründet nur eine Vermutung, keine
Obergrenze der Pflicht. Ich argumentiere also nicht gegen das Recht, sondern in
einer Lücke, die das Recht selbst offenlässt.

Drittens: Das oft zitierte B2-Sprachniveau aus dem
Barrierefreiheitsstärkungsgesetz steht in Paragraph siebzehn der zugehörigen
Verordnung und gilt ausschließlich für Bankdienstleistungen.

Ich könnte jetzt mit einem drohenden Bußgeld argumentieren. Das wäre bequem und
es wäre falsch.

Der ehrliche Satz ist der unten: Ausgerechnet die Kriterien, die den Zugang für
Menschen mit geringer Vorbildung regeln, sind optional. Für die meisten
Websites ist das vertretbar. Für ein Haus, dessen Satzung sagt, die Angebote
stünden allen offen ohne Rücksicht auf Vorbildung, ist es das nicht.

Ich argumentiere deshalb nicht mit dem Gesetz, sondern mit dem Auftrag.


## 8 — Die Arbeitsteilung

typ: zweispalt
kapitel: 02 · LÖSUNG
bild: bilder/08-zahnrad-auge.jpg
bu: Das Regelhafte und das Urteilende.
bildprompt: Komposition geteilt durch eine vertikale Linie, links ein praezises Zahnrad, rechts ein stilisiertes Auge. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Zwei Werkzeuge,
akzent: zwei Zuständigkeiten.
spalte1: DETERMINISTISCH · axe-core
punkte1:
  - Markup, Struktur, Kontraste
  - Reproduzierbar und kostenlos
  - Läuft automatisch bei jeder Änderung
  - Deckt 30 bis 40 Prozent der Kriterien ab
  - Adressat: städtische IT und Portaldienstleister
spalte2: URTEILEND · System-Prompt
punkte2:
  - Verständlichkeit gegen die Zielgruppe
  - Abkürzungen, Aussagekraft von Linktexten
  - Braucht Gegenlesen durch einen Menschen
  - Deckt einen Teil der übrigen 60 bis 70 Prozent ab
  - Adressat: Programmbereiche und Redaktion
callout: Für alles Regelhafte ist ein Sprachmodell das schlechtere Werkzeug.
quellen: WCAG 2.1, Deque axe-core, Erhebungen zur Abdeckung automatischer Prüfung

### NOTIZ

Damit zur Lösung. Und die beginnt mit einer Abgrenzung, die ich für den
wichtigsten Teil meines Konzepts halte.

Es gibt zwei Sorten von Problemen, und sie brauchen zwei verschiedene
Werkzeuge.

Links das Regelhafte: Markup, Struktur, Kontraste. Dafür gibt es etablierte
Prüfprogramme wie axe-core. Die sind kostenlos, laufen automatisch und liefern
bei gleicher Eingabe immer dasselbe Ergebnis. Sie decken dreißig bis vierzig
Prozent der Kriterien ab. Adressat ist die städtische IT und der
Portaldienstleister.

Rechts das Urteilende: Ob ein A2-Lernender diesen Satz versteht. Ob dieser
Linktext etwas aussagt. Dafür gibt es kein Regelwerk, das braucht Urteil.
Adressat sind die Programmbereiche.

Und jetzt der Satz, den ich bewusst so deutlich hinschreibe: Für alles
Regelhafte ist ein Sprachmodell das schlechtere Werkzeug. Es ist langsamer,
teurer und liefert nicht immer dasselbe Ergebnis. Wer behauptet, eine KI
ersetze axe-core, hat entweder das eine oder das andere nicht verstanden.

Mein Projekt betrifft ausschließlich die rechte Spalte. Die linke gehört ins
Konzept, weil sie sonst niemand macht, aber sie ist kein KI-Thema.



## 10 — Der Prompt in sechs Bausteinen

typ: tabelle
kapitel: 02 · SYSTEM-PROMPT
bild: bilder/10-sechs-bloecke.jpg
bu: Sechs Bausteine, festgelegte Reihenfolge.
bildprompt: Sechs gestapelte Rechtecke unterschiedlicher Breite wie ein Bauplan, verbunden durch duenne Linien. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Der Prompt in
akzent: sechs Bausteinen.
klein: ja
spalten: Baustein | Was darin steht
zeilen:
  - "ROLLE | Redaktionsassistenz der vhs. Liest wie eine erfahrene Lektorin, entscheidet nichts."
  - "AUFGABE | Zielgruppe des Kurses bestimmen, dann prüfen, ob sie den Text verstehen kann."
  - "FORMAT | Feste Ausgabe: Zielgruppe, Befunde mit Zitat, Grund und Vorschlag, Zusammenfassung."
  - "GRENZEN | ! Bewertet Texte, niemals Personen. Ändert nichts, veröffentlicht nichts, erfindet nichts."
  - "KONTEXT | Die acht Programmbereiche, Hausabkürzungen, neun Prüfregeln, Goethe- und DTZ-Wortlisten."
  - "REGELN | Namen entfernen, wörtlich zitieren, höchstens zehn Befunde, Pflicht vor Empfehlung."
callout: Die Zeile GRENZEN trägt zwei Lasten gleichzeitig.
calloutsub: Sie hält das Projekt aus Anhang III des EU AI Act heraus und nimmt dem Personalrat die Sorge vor Leistungskontrolle.
quellen: system-prompt.md, Fassung v2 vom 28.07.2026

### NOTIZ

Damit zum Kern der Aufgabe, dem System-Prompt. Er folgt der
Sechs-Komponenten-Struktur aus dem Aufgabenblatt.

Die ROLLE macht ihn zur Redaktionsassistenz, nicht zur Autorin. Die AUFGABE
schreibt die Reihenfolge vor: erst die Zielgruppe bestimmen, dann prüfen. Das
FORMAT erzwingt zu jedem Befund ein wörtliches Zitat, eine Begründung und
einen konkreten Vorschlag. Ohne Vorschlag kein Befund.

Der KONTEXT enthält das Hauswissen: die acht Programmbereiche, die
Abkürzungen des Hauses, neun Prüfregeln und, das ist der wichtigste Teil, die
veröffentlichten Wortlisten des Goethe-Instituts und des Deutsch-Tests für
Zuwanderer. Der Prompt schätzt das Sprachniveau also nicht frei, sondern
begründet am tatsächlichen Prüfungswortschatz. Eine schöne Fußnote dazu: Der
Grundstock dieser Wortlisten stammt laut Goethe-Institut aus einer
Veröffentlichung der Prüfungszentrale des Deutschen Volkshochschulverbands in
Frankfurt.

Die REGELN sagen unter anderem, dass Personennamen aus der Ausgabe entfernt
werden. Kursbeschreibungen enthalten die Namen der Kursleitungen.

Und jetzt zur Zeile GRENZEN, die ich hervorgehoben habe. Dort steht: bewertet
Texte, niemals Personen. Dieser eine Satz leistet zweierlei. Er hält das
Projekt aus dem Hochrisikobereich des EU AI Act heraus, denn dort geht es um
Systeme, die Personen bewerten. Und er ist die Antwort auf die Frage des
Personalrats, ob hier Leistung kontrolliert wird. Ein Satz, zwei Wirkungen.


## 11 — Ein Durchlauf am echten Text

typ: zweispalt
kapitel: 02 · SYSTEM-PROMPT
bild: bilder/12-passstueck.jpg
bu: Der fehlende Schritt zwischen Schreiben und Veröffentlichen.
bildprompt: Eine bestehende Struktur mit einer Luecke, ein passendes kleines Teil wird eingesetzt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Ein Durchlauf,
akzent: an einem echten Text.
klein: ja
lede: Kurs 4074-74, DaF Deutsch 4 A2.2. Zielgruppe liest Deutsch auf A2-Niveau.
spalte1: EINGABE · ORIGINALTEXT
punkte1:
  - "Eine Anmeldung zum Kurs erfolgt idealerweise über einen Termin bei der Sprachberatung DaF."
  - "Eine individuelle Buchung ist nach Selbsteinschätzung und Online-Test ebenfalls möglich."
  - "Diesen können Sie hier ablegen."
  - "Bei einer Fehleinschätzung können wir eine Umbuchung allerdings nicht garantieren."
spalte2: AUSGABE · BEFUNDE
punkte2:
  - "PFLICHT · LINKTEXT: „hier" sagt allein nicht, wohin der Link führt."
  - "EMPFEHLUNG · NIVEAU: „Selbsteinschätzung", „Fehleinschätzung", „Umbuchung" stehen nicht im A2-Wortschatz."
  - "EMPFEHLUNG · AMTSDEUTSCH: „idealerweise" statt „am besten"."
  - "EMPFEHLUNG · ABK: „DaF" wird nicht aufgelöst."
  - "HINWEIS · BAUSTEIN: Passage steht wortgleich über weiteren Kursen, auch über A1."
callout: Der Prüfschritt sitzt genau dort, wo auf Folie 4 die Lücke war.
quellen: eigene Erhebung, Kurs 4074-74, Portalabruf vom 28.07.2026

### NOTIZ

Damit das nicht abstrakt bleibt, ein echter Durchlauf. Links steht ein
Originaltext aus dem Portal, die Anmeldehinweise über einem Deutschkurs auf
Stufe A2. Rechts steht, was der Prompt daraus macht.

Der erste Befund ist Pflicht: Der Link heißt schlicht „hier". Wer sich die
Seite vorlesen lässt und von Link zu Link springt, hört nur „hier".

Die nächsten drei sind Empfehlungen, und sie sind für diese Zielgruppe die
eigentlich wichtigen. Selbsteinschätzung, Fehleinschätzung, Umbuchung. Diese
Wörter stehen nicht im A2-Wortschatz. Sie stehen über einem Kurs, der A2 erst
vermittelt.

Der letzte Befund ist der ergiebigste. Diese Passage ist ein Textbaustein. Sie
steht wortgleich über mehreren Kursen, auch über Kursen auf A1. Ein einziger
Baustein, einmal überarbeitet, verbessert viele Texte gleichzeitig. Das ist
mein Quick Win.

Und damit ist die Lücke von Folie 4 geschlossen. Der Prüfschritt sitzt
zwischen Einpflegen und Veröffentlichen. Er meldet, er ändert nicht. Die
Programmbereichsleitung entscheidet.

## 12 — Stakeholder

typ: matrix
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer eingebunden
akzent: werden muss.
klein: ja
yhoch: Einfluss hoch
yniedrig: Einfluss niedrig
xniedrig: Betroffenheit niedrig
xhoch: Betroffenheit hoch
oben_links: Beobachten || Städtische IT || Advellence, Portaldienstleister || Hessische Durchsetzungsstelle
oben_rechts: Eng einbinden || Direktor als Verantwortlicher der Inhalte || Acht Programmbereichsleitungen || Personalrat, zwei Sitze in der Betriebskommission
unten_links: Informieren || Betriebskommission || Stadtkämmerei
unten_rechts: Konsultieren || Kursleitungen auf Honorarbasis || Inklusionsbeauftragte || Teilnehmende, besonders in DaF und Grundbildung
callout: Die Kursleitungen sind hoch betroffen und haben keinen formalen Einfluss.
calloutsub: Sie sind nicht weisungsgebunden. Beteiligung ist hier kein guter Stil, sondern das einzige verfügbare Instrument.

### NOTIZ

Damit komme ich zum Change-Teil, und der beginnt mit der Frage, wer eigentlich
betroffen ist. Die Achsen sind Einfluss und Betroffenheit.

Oben rechts, eng einzubinden: der Direktor, der laut Impressum persönlich für
die redaktionellen Inhalte verantwortlich ist. Die acht
Programmbereichsleitungen, die die Texte verantworten. Und der Personalrat,
der zwei Sitze in der Betriebskommission hat. Ich hatte das auf Folie drei
angekündigt, hier wird es eingelöst.

Oben links, zu beobachten: die städtische IT, der Schweizer
Portaldienstleister und die hessische Durchsetzungsstelle. Hoher Einfluss,
aber geringe Betroffenheit, weil mein Projekt ihre Arbeit nicht verändert.

Unten links nur informieren: die Betriebskommission und die Kämmerei.

Und unten rechts der Quadrant, der mich am meisten beschäftigt hat. Die
Kursleitungen sind maximal betroffen, sie schreiben viele dieser Texte. Und
sie haben keinen formalen Einfluss, denn sie sitzen in keinem Gremium. Sie
sind Honorarkräfte. Man kann ihnen nichts vorschreiben.

Genau deshalb steht unten der Satz: Beteiligung ist hier kein guter Stil,
sondern das einzige Instrument, das überhaupt zur Verfügung steht.

Ein Hinweis zur Matrix selbst: Ich verwende die Achsen aus dem Aufgabenblatt,
also Einfluss und Betroffenheit. In der Change Toolbox ist sie als
Einfluss-Interesse-Matrix geführt. Ich halte Betroffenheit hier für
trennschärfer, weil die Kursleitungen sehr betroffen sind, ohne besonderes
Interesse an dem Thema zu haben.


## 13 — Widerstand

typ: zweispalt
kapitel: 03 · CHANGE MANAGEMENT
bild: bilder/14-widerstand.jpg
bu: Zwei Kräfte, ein Gleichgewicht.
bildprompt: Zwei entgegengesetzte Kraefte treffen an einer senkrechten Naht aufeinander, im Gleichgewicht. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Warum jemand Nein sagt,
akzent: und was hilft.
klein: ja
spalte1: URSACHE · WAS ICH HÖREN WERDE
punkte1:
  - "Verlustangst: „Jetzt korrigiert mich eine Maschine."
  - "Unsicherheit: „Wird damit meine Arbeit bewertet?"
  - "Gewohnheit: „Wir schreiben das seit fünfzehn Jahren so."
  - "Fehlende Perspektive: „Noch eine Aufgabe, für die ich keine Zeit habe."
spalte2: INTERVENTION
punkte2:
  - "Zuhören, bevor geschult wird. Der Prompt prüft Texte, nie Personen."
  - "Keine Auswertung nach Urheber, keine Rangliste. Schriftlich zusichern und dem Personalrat vorlegen."
  - "Nicht das Schreiben ändern, nur einen Schritt danach ergänzen."
  - "Quick Win zuerst: die gemeinsamen Textbausteine. Sichtbare Wirkung ohne Mehrarbeit."
callout: Betroffene zu Beteiligten machen. Der Pilotbereich wählt selbst, welche Regeln zuerst gelten.

### NOTIZ

Jetzt zum Widerstand. Ich habe die vier Ursachen aus dem Unterricht genommen
und für jede den Satz aufgeschrieben, den ich in diesem Haus tatsächlich
erwarte.

Verlustangst klingt hier so: Jetzt korrigiert mich eine Maschine. Dahinter
steckt Verlustaversion, wir gewichten einen Verlust etwa doppelt so stark wie
einen gleich großen Gewinn. Die Kursleitung sieht zuerst den Kontrollverlust
über ihren eigenen Text, nicht die Entlastung.

Unsicherheit klingt so: Wird damit meine Arbeit bewertet? Das ist die
gefährlichste Frage, und sie ist berechtigt. Meine Antwort ist dieselbe wie
auf der Prompt-Folie: Es werden Texte ausgewertet, nicht Personen. Keine
Statistik nach Urheberin, keine Rangliste. Und das gehört nicht nur gesagt,
sondern schriftlich zugesichert und dem Personalrat vorgelegt, bevor der
Pilot beginnt und nicht danach.

Gewohnheit und fehlende Perspektive begegne ich mit dem Zuschnitt selbst. Ich
ändere nicht, wie jemand schreibt. Ich ergänze einen Schritt danach. Und ich
fange mit den Textbausteinen an, weil dort mit einer einzigen Überarbeitung
viele Kurse besser werden. Das ist sichtbare Wirkung, für die niemand seine
Arbeitsweise ändern muss.

Der Satz unten ist der Kern jeder Widerstandsarbeit: Betroffene zu Beteiligten
machen. Konkret heißt das, dass der Pilotbereich selbst entscheidet, welche
der neun Prüfregeln zuerst scharf gestellt werden.


## 14 — Timeline

typ: timeline
kapitel: 03 · CHANGE MANAGEMENT
titel: Drei Monate,
akzent: drei Stränge.
klein: ja
monate: Monat 1 | Monat 2 | Monat 3
strang1: Technische Implementation || Assistent in fobizz anlegen, Regeln schärfen || +Pilot in einem Programmbereich || Ausweitung auf alle acht
strang2: Kommunikation || Ankündigung, Personalrat einbeziehen || Schulung nach Artikel 4 KI-Verordnung || ~Sprechstunde und Support
strang3: Change || Betroffene befragen, Bausteine sichten || Quick Win Textbausteine || Nachmessung und Entscheidung
callout: Erste 30 Tage: Personalrat einbinden, Pilotbereich gewinnen, Textbausteine überarbeiten.
calloutsub: KPI eins: Befundquote unter 40 Prozent. KPI zwei: alle Neutexte im Pilot geprüft. KPI drei: DaF-Texte mit C1-Vokabular von 9 von 13 auf höchstens 2 von 13.
quellen: Ausgangsmessung 28.07.2026, Nachmessung mit identischem Skript

### NOTIZ

Der Zeitplan, drei Monate, drei Stränge.

Technisch ist wenig zu tun, und das ist der Vorteil dieses Projekts. Im ersten
Monat wird der Assistent im vorhandenen Rahmen angelegt und an echten Texten
nachgeschärft. Im zweiten läuft der Pilot in einem Programmbereich. Im dritten
die Ausweitung.

Der Kommunikationsstrang beginnt vor dem technischen. Ankündigung und
Einbeziehung des Personalrats stehen bewusst im ersten Monat. Die Schulung im
zweiten ist übrigens keine Kür: Artikel vier der KI-Verordnung verpflichtet
Betreiber seit Februar 2025, für ausreichende KI-Kompetenz ihres Personals zu
sorgen. Mein Qualifizierungskonzept erfüllt damit eine Rechtspflicht.

Der Change-Strang: erst fragen, dann handeln. Der Quick Win mit den
Textbausteinen liegt im zweiten Monat, weil er dann auf schon geweckte
Erwartung trifft.

Unten stehen die ersten dreißig Tage und drei Kennzahlen. Der wichtigste Punkt
daran: Die Ausgangsmessung liegt bereits vor, erhoben mit einem Skript. Die
Nachmessung läuft mit demselben Skript. Ich muss also für die Erfolgskontrolle
nichts Neues aufbauen, und niemand kann später über die Messmethode streiten.


## 15 — Schlussfolie

typ: schluss
bild: bilder/15-durchgang.jpg
bildprompt: Wand aus dichten Balken mit einem Durchgang, dahinter Helligkeit, eine Figur geht hindurch. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Der Prompt ist ein Nachmittag Arbeit.
akzent: Alles, was ihn erlaubt, ist der eigentliche Aufwand.
untertitel: Vielen Dank. Ich freue mich auf eure Fragen.
fussl: PROJEKT KLARTEXT · VHS FRANKFURT
fussr: HENRIK HEIL · CIMDATA 2026

### NOTIZ

Ich fasse zusammen.

Ich habe ein reales Unternehmen analysiert, einen Prozess gefunden, in dem
niemand etwas falsch macht und trotzdem etwas fehlt, und ich habe den Zustand
gemessen statt geschätzt.

Der System-Prompt selbst, das ist meine eigentliche Lehre aus diesem Projekt,
ist an einem Nachmittag geschrieben. Die Arbeit steckt in allem, was ihn
möglich macht: zu wissen, für wen ein Text ist, zu wissen, was Pflicht ist und
was Anspruch, und einen Weg zu finden, auf dem die Menschen, die diese Texte
schreiben, das Werkzeug nicht als Kontrolle erleben.

Vielen Dank. Gerne eure Fragen.
