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
titel: KLARTEXT — Kursbeschreibungen
akzent: barrierefrei prüfen.
untertitel: Ein KI-gestützter Prüfschritt vor der Veröffentlichung.
meta: Volkshochschule Frankfurt am Main | Acht Programmbereiche | 5.800 Texte im Jahr
fussl: ABSCHLUSSPROJEKT · CHANGE UND KI
fussr: CIMDATA · HENRIK HEIL · JULI 2026
bild: bilder/01-titel-wand.jpg
bildprompt: Kleine Figur vor einer Wand aus dichten horizontalen Balken, ein schmaler Durchgang. Flach-geometrisch, Bauhaus, Palette Petrol/Papier/Mint/Orange, keine Schrift.

### NOTIZ

Ich stelle euch heute mein Abschlussprojekt vor: KLARTEXT, ein Prüfschritt für
die Kursbeschreibungen der Volkshochschule Frankfurt.

Das Feld heißt Barrierefreiheit. Die meisten denken dabei an Technik:
Kontraste, Tastaturbedienung, Vorleseprogramme. Mein Thema ist der andere
Teil. Ob der Text ankommt bei denen, für die er geschrieben ist. Das betrifft
alle acht Programmbereiche des Hauses.

Angefangen hat es mit dem schärfsten Fall. Die Volkshochschule bietet
Deutschkurse für Menschen an, die gerade erst Deutsch lernen. Und die
Beschreibungen dieser Kurse sind in einem Deutsch geschrieben, das man erst
nach dem Kurs versteht. Wer Deutsch lernen will, muss erst Deutsch können. Das
ist der Extremfall, aber das Prinzip dahinter gilt überall.

Zwei Hinweise vorweg. Ich habe dieses Projekt allein bearbeitet, alle Rollen
liegen also bei mir. Und alle Zahlen, die gleich kommen, habe ich selbst
gemessen, an der echten Website, am achtundzwanzigsten Juli. Der Datensatz
liegt der Arbeit bei.

Am Ende zeige ich das Werkzeug live an einem echten Kurstext.


## 2 — Executive Summary I: Worum es geht

typ: zahlen
kapitel: ÜBERBLICK
titel: 5.800 Texte im Jahr,
akzent: geprüft wird die Technik.
lede: Die Kursbeschreibungen entstehen in acht Programmbereichen und erscheinen unverändert im Portal, im Programmheft und im Newsletter. Einfache Sprache bietet das Haus an — für Betrieb und Kursgeschäft, nicht für die Kurstexte selbst.
zahlen:
  - "5.800 || Kursbeschreibungen im Jahr"
  - "90 % || haben mindestens einen Befund || warn"
  - "5 Jahre || seit dem letzten externen Barrierefreiheitstest || warn"
callout: Neun von zehn Texten haben einen Befund. Die Frage ist, für wen sie zu schwer sind.
quellen:
  - "eigene Erhebung an 60 Kursen, 28.07.2026"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"
  - "Erklärung zur Barrierefreiheit der vhs, 23.09.2025 | https://vhs.frankfurt.de/de/special-pages/support/barrierefreiheit"

### NOTIZ

Zuerst das Ganze in drei Zahlen.

Die Volkshochschule veröffentlicht rund fünftausendachthundert
Kursbeschreibungen im Jahr. In meiner Stichprobe von sechzig Kursen haben neun
von zehn Texten mindestens einen Befund.

Die dritte Zahl stammt aus dem Haus selbst. In der Erklärung zur
Barrierefreiheit steht, wann die Website zuletzt extern geprüft wurde: am
ersten Juli zweitausendeinundzwanzig. Das ist heute auf den Tag genau fünf
Jahre her. Seitdem bewertet sich das Haus selbst. Ich habe die Seite mit einem
gängigen Prüfprogramm laufen lassen, und sie erfüllt die Anforderungen heute
nicht mehr, da kommen etliche Verstöße zusammen.

Das ist aber ausdrücklich nicht mein Thema. Dafür ist die städtische IT
zuständig, und ich komme darauf noch einmal zurück.

Denn dieselbe Erklärung enthält den Satz, der mich auf dieses Projekt gebracht
hat. Die wichtigsten Informationen zu Betrieb und Kursgeschäft, heißt es dort,
seien in einfacher Sprache verfügbar. Das Haus hat die Frage nach der
Verständlichkeit also längst gestellt und für einen Bereich beantwortet. Nur
für die Kursbeschreibungen selbst, den mit Abstand größten Textbestand, gilt
das nicht.

Genau da setze ich an. Und unten steht die Frage, um die es dabei geht: Neun
von zehn Texten haben einen Befund. Für wen sind sie eigentlich zu schwer?


## 3 — Executive Summary II: Der Vorschlag

typ: punkte
kapitel: ÜBERBLICK
bild: bilder/02-teile-ganzes.jpg
bildprompt: Einzelne geometrische Formen, die sich zu einer geordneten Komposition fuegen. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Der Vorschlag,
akzent: und was er bringt.
punkte:
  - "**Ziel** || Wer einen Kurs sucht, versteht die Beschreibung, ob gelesen oder vorgelesen. Laut Betriebssatzung stehen die Angebote allen offen — das soll auch für die Texte gelten."
  - "**Lösung** || Ein Prüfschritt vor der Veröffentlichung, als System-Prompt im vorhandenen KI-Rahmen des Volkshochschul-Verbands. Keine Beschaffung, kein neuer Vertrag."
  - "**Abgrenzung** || Die technische Barrierefreiheit der Website bleibt beim deterministischen Prüfwerkzeug und bei der städtischen IT. Die KI sieht nur den Kurstext."
  - "**Ergebnis** || Befundquote nach drei Monaten unter 40 Prozent statt heute 90. Aufwand im Regelbetrieb 29 Stunden im Jahr."
callout: Erster Schritt: ein Pilot in einem Programmbereich, drei Monate, ohne Beschaffung.
calloutsub: Der Prompt schlägt vor, der Mensch entscheidet und veröffentlicht.
quellen:
  - "Betriebssatzung der vhs Frankfurt | https://vhs.frankfurt.de/de/special-pages/important/betriebssatzung"

### NOTIZ

Daraus folgt mein Vorschlag.

Das Ziel oben ist bewusst von den Lesenden her formuliert. Wer einen Kurs
sucht, soll die Beschreibung verstehen, ob er sie liest oder vorgelesen
bekommt. Die Betriebssatzung sagt, die Angebote stehen allen offen. Mein Punkt
ist: Dann muss das auch für die Texte gelten, mit denen wir sie ankündigen.

Geprüft wird deshalb zweierlei. Ob die Zielgruppe den Text versteht, und ob ein
Vorleseprogramm etwas damit anfangen kann. Eine fett gesetzte Zeile, die als
Überschrift gemeint ist, aber technisch keine ist, wird beim Vorlesen nicht als
Sprungmarke angeboten.

Dafür genügt ein System-Prompt in dem KI-Rahmen, den der Volkshochschul-Verband
ohnehin für alle Volkshochschulen bereitstellt. Es muss nichts beschafft
werden.

Die Abgrenzung darunter zieht sich durch das ganze Konzept. Für die technische
Barrierefreiheit der Website bleibt ein normales Prüfwerkzeug zuständig,
zusammen mit der städtischen IT. Die KI sieht nur den Kurstext.

Unten steht der erste Schritt: ein Pilot in einem Programmbereich, drei Monate.
Der Prompt schlägt vor, der Mensch entscheidet.


## 4 — Das Haus und der Prozess heute

typ: zweispalt
kapitel: 01 · UNTERNEHMEN UND IST-ANALYSE
bild: bilder/04-prozess-luecke.jpg
bildprompt: Vier Kreise in einer Reihe, verbunden durch Linien, die Verbindung zwischen drittem und viertem Kreis fehlt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Die vhs Frankfurt,
akzent: und wie ein Kurstext entsteht.
klein: ja
lede: Volkshochschule Frankfurt am Main, gegründet 1890. Laut Betriebssatzung stehen die Angebote grundsätzlich allen offen, ohne Rücksicht auf Vorbildung.
spalte1: DAS UNTERNEHMEN
punkte1:
  - "Eigenbetrieb der Stadt, 154 T€ Stammkapital, seit 2005 nach LQW testiert"
  - "5.800 Veranstaltungen im Jahr, acht Programmbereiche in vier Fachbereichen"
  - "Betriebskommission mit 16 Sitzen, zwei davon für den Personalrat"
  - "Der Direktor ist laut Impressum persönlich für die Inhalte verantwortlich"
spalte2: SO ENTSTEHT EIN KURSTEXT · ANGENOMMENER ABLAUF
punkte2:
  - "Die Teams der vier Fachbereiche planen das Programm halbjährlich"
  - "Der Text wird geschrieben — zugeliefert oder aus Bausteinen zusammengesetzt"
  - "Der Text wird in das Kursverwaltungssystem eingepflegt"
  - "Er erscheint unverändert im Portal, teils wortgleich im Programmheft"
callout: Zwischen Einpflegen und Veröffentlichen ist kein Prüfschritt auf Verständlichkeit vorgesehen.
calloutsub: Soll-Zustand: Hier steht künftig ein Prüfschritt, der meldet und nicht ändert.
quellen:
  - "Betriebssatzung der vhs Frankfurt | https://vhs.frankfurt.de/de/special-pages/important/betriebssatzung"
  - "Impressum | https://vhs.frankfurt.de/de/special-pages/important/impressum"
  - "Fachbereiche und Qualitätstestierung | https://vhs.frankfurt.de/de/about/featured/fachbereiche-an-der-vhs"
  - "Ablauf: eigene Recherche, daten/recherche-redaktionsablauf.md"

### NOTIZ

Zunächst das Unternehmen und der Prozess, um den es geht.

Die Volkshochschule Frankfurt ist kein Amt, sondern ein Eigenbetrieb der
Stadt. Geleitet wird sie von einem Direktor, der laut Impressum auch
persönlich für die redaktionellen Inhalte der Website verantwortlich ist.
Darüber steht eine Betriebskommission mit sechzehn Sitzen, zwei davon für den
Personalrat. Diese zwei Sitze spielen später noch eine Rolle.

Wichtig ist der erste Punkt, ganz am Ende. Das Haus ist seit zweitausendfünf
nach L Q W testiert. Das steht für Lernerorientierte Qualitätstestierung in
der Weiterbildung, ein Verfahren mit regelmäßiger externer Prüfung, inzwischen
in der sechsten Runde. Dazu kommt eine Zertifizierung nach der Akkreditierungs-
und Zulassungsverordnung Arbeitsförderung. Das ist mir wichtig zu betonen: Hier
fehlt keine Qualitätskultur. Es fehlt genau ein Schritt darin.

Der Satz oben stammt wörtlich aus der Betriebssatzung. Die Angebote stehen
grundsätzlich allen offen, ohne Rücksicht auf Vorbildung. Daran messe ich das
Haus. Nicht am Gesetz, sondern an seinem eigenen Anspruch.

Rechts steht, wie ein Kurstext entsteht. Geplant wird halbjährlich, von den
Teams der vier Fachbereiche. Der Text wird geschrieben und ins
Kursverwaltungssystem eingepflegt, und dann erscheint er.

Zwischen dem Einpflegen und dem Erscheinen ist kein Prüfschritt auf
Verständlichkeit vorgesehen. Das ist kein Vorwurf, denn dieser Arbeitsschritt
ist nirgends vorgesehen. Genau deshalb ist es ein Fall für Prozessgestaltung
und nicht für einen Appell, sich mehr Mühe zu geben.

Eine Einschränkung sage ich offen dazu. Für das gedruckte Programmheft gibt es
sehr wohl eine Redaktion, das Impressum nennt sie mit Namen. Für das Portal
gibt es sie nicht, und dort stehen die Texte, um die es hier geht.

Und noch eine Einschränkung. Über der rechten Spalte steht nicht ohne Grund
das Wort angenommen. Wer bei der vhs Frankfurt die Texte schreibt, ist nicht
öffentlich dokumentiert. Für die Branche ist es gut belegt: Das Standardwerk
des Deutschen Instituts für Erwachsenenbildung führt die fristgerechte Abgabe
von Ankündigungstexten unter den Pflichten der Kursleitung. Bei den
Sprachkursen hier spricht der Befund allerdings dagegen. Beide Kurse, die ich
gleich zeige, sind im Programmheft mit N. N. als Kursleitung gedruckt. Da war
noch niemand gewonnen, der einen Text hätte liefern können. Diese Texte
bestehen vollständig aus Bausteinen.

Das ist übrigens kein Randbefund. Ich habe nachgezählt: Vierundfünfzig Prozent
aller Kurse teilen sich ihren Text mit mindestens einem anderen Kurs. Ein
schlecht formulierter Text ist hier nie ein Einzelfall.


## 5 — Messung und eigentlicher Befund

typ: tabelle
kapitel: 01 · POTENZIALERMITTLUNG
bild: bilder/06-zwei-blicke.jpg
bildprompt: Zwei Figuren betrachten dasselbe Rechteck, links offen und klar, rechts durch dichte Streifen verdeckt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Dieselbe Zahl bedeutet
akzent: zweimal etwas anderes.
klein: ja
lede: Stichprobe von 60 Kursbeschreibungen aus sieben Programmbereichen, gezogen über die offene Schnittstelle des Kursportals am 28.07.2026. 90 Prozent haben mindestens einen Befund, nur 6 von 60 blieben ohne. Der längste gemessene Satz hat 74 Wörter.
spalten: Kurs | Ø Satzlänge | längster Satz | Zielgruppe liest Deutsch
zeilen:
  - "Englisch A1.1 | 21,3 Wörter | 41 Wörter | + fließend"
  - "DaF Deutsch 4 A2.2 | 10,6 Wörter | 16 Wörter | ! erst auf A1-Niveau"
callout: Ein Lesbarkeitswerkzeug würde hier den falschen Kurs beanstanden.
calloutsub: 9 von 13 Kursen für Deutschlernende enthalten C1-Vokabular: Selbsteinschätzung, Fehleinschätzung, Umbuchung.
quellen:
  - "eigene Erhebung an 60 Kursen, Datensatz liegt der Arbeit bei"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"

### NOTIZ

Damit zur Potenzialermittlung. Hier habe ich nicht geschätzt, sondern
gemessen.

Das Kursportal hat eine offene Schnittstelle. Darüber habe ich sechzig
Kursbeschreibungen aus sieben der acht Programmbereiche gezogen und
automatisch ausgewertet. Neunzig Prozent der Texte haben mindestens einen
Befund. Sechs von sechzig blieben ohne.

Der eigentliche Befund steht aber in der Tabelle, und er sieht auf den ersten
Blick unscheinbar aus.

Oben ein Englischkurs auf Stufe A1, unten ein Deutschkurs auf Stufe A2. Der
Englischkurs hat durchschnittlich einundzwanzig Wörter pro Satz, der längste
hat einundvierzig. Der Deutschkurs hat knapp elf Wörter pro Satz, der längste
sechzehn.

Ein Lesbarkeitsindex oder ein Standard-KI-Assistent würde jetzt den
Englischkurs beanstanden und den Deutschkurs durchwinken. Das ist genau falsch
herum.

Denn der Englischkurs richtet sich an Menschen, die fließend Deutsch lesen.
Für die ist ein langer Satz unschön, aber kein Hindernis. Der Deutschkurs
richtet sich an Menschen, die Deutsch erst auf A1-Niveau lesen. Für die ist
jedes Wort oberhalb dieses Niveaus eine Hürde.

Deshalb reicht kein Werkzeug, das nur den Text ansieht. Man muss wissen, für
wen der Text ist. Neun von dreizehn Kursen für Deutschlernende enthalten
Wörter wie Selbsteinschätzung, Fehleinschätzung und Umbuchung. Das ist
C1-Vokabular über einem Kurs, den man mit A1 beginnt. Genau hier kann ein
fachlich eingestellter Prompt etwas, was ein Standardwerkzeug nicht kann.


## 6 — Rechtslage

typ: text
kapitel: 01 · EINORDNUNG
bild: bilder/07-stufen.jpg
bildprompt: Treppe aus drei Stufen, die unteren zwei massiv petrol, die oberste nur als duenner Umriss. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Welches Recht gilt,
akzent: und was nicht.
klein: ja
absaetze:
  - "Digitale Barrierefreiheit heißt: Websites müssen so gebaut sein, dass auch Menschen mit Behinderung sie nutzen können. Der Maßstab sind die **WCAG** mit den Stufen A, AA und AAA."
  - "Für die vhs gilt weder die EU-Richtlinie noch das Barrierefreiheitsstärkungsgesetz direkt. Als kommunale Einrichtung in Hessen greift **Landesrecht**: § 14 HessBGG und die **BITV HE**. Gefordert ist Stufe **AA** — nicht die BITV 2.0 des Bundes, der häufigste Zitierfehler kommunaler Stellen."
  - "**Pflicht auf AA:** Struktur (1.3.1), Seitentitel (2.4.2), Sprache von Textteilen (3.1.2). **Nicht Pflicht:** Abkürzungen erklärt (3.1.4) und Leseniveau der Zielgruppe (3.1.5), beides Stufe AAA. Nicht Teil der AA-Konformität heißt aber nicht belanglos: **§ 3 Abs. 1 BITV HE** verlangt eigenständig, dass Angebote verständlich sind."
callout: Ausgerechnet die Kriterien für Menschen mit geringer Vorbildung sind optional.
calloutsub: Ich argumentiere deshalb nicht mit einem drohenden Bußgeld, sondern mit dem Auftrag aus der Betriebssatzung.
quellen:
  - "HessBGG, BITV HE 2019, EN 301 549"
  - "WCAG 2.1 | https://www.w3.org/TR/WCAG21/"
  - "Landesfachstelle Barrierefreie IT Hessen | https://lbit.hessen.de/oeffentliche-stellen/allgemeine-anforderungen-der-barrierefreien-it"
  - "Erklärung zur Barrierefreiheit der vhs | https://vhs.frankfurt.de/de/special-pages/support/barrierefreiheit"

### NOTIZ

Bevor ich zur Lösung komme, kurz die Rechtslage.

Digitale Barrierefreiheit bedeutet, dass eine Website auch für Menschen mit
Behinderung nutzbar sein muss. Der Maßstab sind die WCAG, mit drei Stufen: A,
doppel A und dreifach A.

Für die vhs gilt weder die EU-Richtlinie noch das
Barrierefreiheitsstärkungsgesetz unmittelbar. Sie ist eine kommunale
Einrichtung in Hessen, also greift Landesrecht: Paragraph vierzehn des
Hessischen Behindertengleichstellungsgesetzes und die hessische Verordnung.
Gefordert wird Stufe doppel A. Viele kommunale Stellen berufen sich
stattdessen auf die BITV zwei null des Bundes. Die gilt für Bundesbehörden.
Wer das verwechselt, prüft am falschen Maßstab.

Und jetzt der Punkt, an dem ich beim Recherchieren selbst falsch lag. Struktur
und ausgezeichnete Fremdsprachen sind Pflicht. Aber dass Abkürzungen erklärt
werden und dass das Leseniveau zur Zielgruppe passt, ist beides dreifach A und
damit nicht verbindlich. Ich könnte jetzt mit einem drohenden Bußgeld
argumentieren. Das wäre bequem, und es wäre falsch.

Wichtig ist der letzte Absatz. Paragraph drei Absatz eins der hessischen
Verordnung verlangt eigenständig, dass Angebote verständlich sind. Die
Konformitätsstufe begründet eine Vermutung, keine Obergrenze der Pflicht. Ich
argumentiere also nicht gegen das Recht, sondern in einer Lücke, die es selbst
offenlässt.

Ausgerechnet die Kriterien für Menschen mit geringer Vorbildung sind optional.
Für ein Haus, dessen Satzung sagt, die Angebote stünden allen offen ohne
Rücksicht auf Vorbildung, ist das nicht vertretbar.


## 7 — Die Arbeitsteilung

typ: zweispalt
kapitel: 02 · LÖSUNG
bild: bilder/08-zahnrad-auge.jpg
bildprompt: Komposition geteilt durch eine vertikale Linie, links ein praezises Zahnrad, rechts ein stilisiertes Auge. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Zwei Werkzeuge,
akzent: zwei Zuständigkeiten.
klein: ja
spalte1: DETERMINISTISCH · axe-core
punkte1:
  - "Markup, Kontraste, Tastaturbedienung, Seitengerüst"
  - "Reproduzierbar, kostenlos, läuft bei jeder Änderung"
  - "Deckt 30 bis 40 Prozent der Kriterien ab"
  - "Adressat: städtische IT und Portaldienstleister"
spalte2: URTEILEND · System-Prompt
punkte2:
  - "Verständlichkeit gegen die Zielgruppe"
  - "Überschriften, die keine sind, und Linktexte ohne Aussage"
  - "Braucht Gegenlesen durch einen Menschen"
  - "Adressat: Programmbereiche und Redaktion"
callout: Für alles Regelhafte ist ein Sprachmodell das schlechtere Werkzeug.
calloutsub: Technische Voraussetzungen: der vorhandene KI-Rahmen des Volkshochschul-Verbands, ein hinterlegter Assistent, die Wortliste als Datei. Keine Beschaffung, kein Eingriff ins Kursverwaltungssystem.
quellen:
  - "WCAG 2.1 | https://www.w3.org/TR/WCAG21/"
  - "Deque axe-core | https://github.com/dequelabs/axe-core"
  - "Erhebungen zur Abdeckung automatischer Prüfung"

### NOTIZ

Damit zur Lösung. Sie beginnt mit einer Abgrenzung, die ich für den
wichtigsten Teil meines Konzepts halte.

Es gibt zwei Sorten von Problemen, und sie brauchen zwei verschiedene
Werkzeuge.

Links das Regelhafte: Markup, Kontraste, Tastaturbedienung, das Gerüst der
Seite. Dafür gibt es etablierte Prüfprogramme wie axe-core. Die sind
kostenlos, laufen automatisch und liefern bei gleicher Eingabe immer dasselbe
Ergebnis. Zuständig ist die städtische IT.

Rechts das Urteilende: Ob ein Lernender auf A1 diesen Satz versteht. Ob dieser
Linktext etwas aussagt. Dafür gibt es kein Regelwerk, das braucht Urteil.
Zuständig sind die Programmbereiche.

Die Trennlinie verläuft dabei nicht zwischen Sprache und Technik. Zwei meiner
sechs Regeln sind selbst Pflichtkriterien der Barrierefreiheit. Ein Beispiel:
Eine fett gesetzte Zeile, die als Überschrift gemeint ist, aber technisch
keine ist. Das Prüfprogramm sieht dort nur fetten Text und meldet nichts. Ob
diese Zeile eine Überschrift sein sollte, kann man dem Text nicht ansehen,
sondern nur verstehen. Deshalb liegt ausgerechnet dieses Pflichtkriterium auf
der rechten Seite.

Der Satz in der Mitte ist mir wichtig genug, ihn so deutlich hinzuschreiben.
Für alles Regelhafte ist ein Sprachmodell das schlechtere Werkzeug. Es ist
langsamer, teurer und liefert nicht immer dasselbe Ergebnis. Wer behauptet,
eine KI ersetze axe-core, hat entweder das eine oder das andere nicht
verstanden.

Diese Trennung hat sich beim Bauen zweimal selbst bestätigt. Zwei Zusagen, die
ich zuerst in den Prompt geschrieben hatte, hat das Modell nicht zuverlässig
eingehalten. Beide stehen jetzt im Programmcode, weil sie feststehen und kein
Urteil verlangen.

Zu den technischen Voraussetzungen: Es braucht den KI-Rahmen, den der
Volkshochschul-Verband ohnehin bereitstellt, einen dort hinterlegten
Assistenten und die Wortliste als Datei. Kein neuer Vertrag, kein Eingriff ins
Kursverwaltungssystem.


## 8 — Der Prompt in sechs Bausteinen

typ: tabelle2
kapitel: 02 · SYSTEM-PROMPT
titel: Der Prompt in
akzent: sechs Bausteinen.
klein: ja
spalten: Baustein | Was darin steht
zeilen:
  - "ROLLE | Redaktionsassistenz der vhs. Liest wie eine erfahrene Lektorin, entscheidet nichts."
  - "AUFGABE | Zielgruppe des Kurses bestimmen, dann prüfen, ob sie den Text verstehen kann."
  - "FORMAT | Feste Ausgabe: Zielgruppe, Befunde mit Zitat, Grund und Vorschlag, Zusammenfassung."
  - "GRENZEN | ! Bewertet Texte, niemals Personen. Ändert nichts, veröffentlicht nichts, erfindet nichts."
  - "KONTEXT | Acht Programmbereiche, Hausabkürzungen, sechs Prüfregeln, 820 Wörter des Goethe-Zertifikats A1."
  - "REGELN | Namen entfernen, wörtlich zitieren, höchstens fünfzehn Befunde, Pflicht vor Empfehlung."
regelntitel: Die sechs Befundarten
regeln:
  - "PFLICHT | STRUKTUR | Überschrift, die keine ist"
  - "| LINKTEXT | „hier" sagt nicht, wohin der Link führt"
  - "EMPFEHLUNG | NIVEAU | Wort zu schwer für diese Zielgruppe"
  - "| AMTSDEUTSCH | Verwaltungssprache statt Alltagssprache"
  - "| SATZ | über 25 Wörter, bei Deutschkursen über 15"
  - "| ABK | Abkürzung nicht aufgelöst"
quellen:
  - "system-prompt.md, Fassung v10 vom 29.07.2026, elf Fassungen in der Versionsverwaltung"
  - "KI-Verordnung (EU) 2024/1689, Anhang III | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Damit zum Kern der Aufgabe, dem System-Prompt. Er folgt der
Sechs-Komponenten-Struktur aus dem Aufgabenblatt.

Die ROLLE macht ihn zur Redaktionsassistenz, nicht zur Autorin. Die AUFGABE
schreibt die Reihenfolge vor: erst die Zielgruppe bestimmen, dann prüfen. Das
FORMAT erzwingt zu jedem Befund ein wörtliches Zitat, eine Begründung und
einen konkreten Vorschlag. Ohne Vorschlag kein Befund.

Der KONTEXT enthält das Hauswissen: die acht Programmbereiche, die
Abkürzungen des Hauses, sechs Prüfregeln und, das ist der wichtigste Teil,
achthundertzwanzig Wörter des Prüfungswortschatzes für das Goethe-Zertifikat
A1. Diese Liste steht vollständig im Prompt, nicht als Verweis. Er schätzt das
Sprachniveau also nicht, sondern begründet es.

Das ist das Ergebnis der ersten Überarbeitung. In meiner ersten Fassung
behauptete der Prompt, gegen die Wortlisten zu prüfen, hatte sie aber gar
nicht. Er schätzte weiter frei und klang dabei nach Beleg. Das ist derselbe
Fehler, den ich anderen Werkzeugen vorwerfe. Eine schöne Fußnote: Der
Grundstock dieser Listen stammt laut Goethe-Institut aus einer
Veröffentlichung der Prüfungszentrale des Deutschen Volkshochschulverbands in
Frankfurt.

Unten stehen die sechs Befundarten, die er kennt. Pflicht sind genau zwei:
eine Zeile, die wie eine Überschrift aussieht, aber keine ist, und ein
Linktext, der nicht sagt, wohin er führt. Beides ist Stufe A und damit
verbindlich. Die übrigen vier sind Empfehlungen.

Und jetzt zur Zeile GRENZEN. Dort steht: bewertet Texte, niemals Personen.
Dieser eine Satz leistet zweierlei. Er hält das Projekt aus dem
Hochrisikobereich der KI-Verordnung heraus, denn Anhang III setzt überall eine
Bewertung natürlicher Personen voraus. Und er ist die Antwort auf die Frage
des Personalrats, ob hier Leistung kontrolliert wird.


## 9 — Ein Durchlauf am echten Text

typ: zweispalt
kapitel: 02 · SYSTEM-PROMPT
bild: bilder/12-passstueck.jpg
bildprompt: Eine bestehende Struktur mit einer Luecke, ein passendes kleines Teil wird eingesetzt. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Ein Durchlauf,
akzent: an einem echten Text.
klein: ja
lede: Kurs 4074-74, DaF Deutsch 4 A2.2. Der Prompt bestimmt die Zielgruppe selbst: liest Deutsch auf A1.
spalte1: EINGABE · ORIGINALTEXT
punkte1:
  - "Eine Anmeldung erfolgt idealerweise über einen Termin bei der Sprachberatung DaF."
  - "Eine individuelle Buchung ist nach Selbsteinschätzung und Online-Test ebenfalls möglich."
  - "Diesen können Sie hier ablegen."
  - "Bei einer Fehleinschätzung können wir eine Umbuchung allerdings nicht garantieren."
spalte2: AUSGABE · BEFUNDE
punkte2:
  - "PFLICHT · LINKTEXT: „hier" sagt allein nicht, wohin der Link führt."
  - "EMPFEHLUNG · NIVEAU: „idealerweise", „Selbsteinschätzung", „Fehleinschätzung", „Umbuchung"."
  - "EMPFEHLUNG · NIVEAU: „Niveaustufe", „umfasst", „Teilstufen" — keines steht auf der A1-Liste."
  - "Zusammen zwölf Befunde, elf davon zum Sprachniveau, einer Pflicht."
callout: Derselbe Prompt meldet beim Englischkurs null Niveau-Befunde und hier elf.
quellen:
  - "eigene Erhebung, Kurs 4074-74, vier Läufe am 29.07.2026"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"

### NOTIZ

Damit das nicht abstrakt bleibt, ein echter Durchlauf. Links steht ein
Originaltext aus dem Portal, die Anmeldehinweise über einem Deutschkurs auf
Stufe A2. Rechts steht, was der Prompt daraus macht.

Der erste Befund ist Pflicht. Der Link heißt schlicht „hier". Wer sich die
Seite vorlesen lässt und von Link zu Link springt, hört nur „hier".

Die übrigen sind Empfehlungen, und sie sind für diese Zielgruppe die
eigentlich wichtigen. Selbsteinschätzung, Fehleinschätzung, Umbuchung,
Niveaustufe, Teilstufen. Keines dieser Wörter steht auf der A1-Liste, die der
Prompt als Anker mitbekommt.

Der Satz unten ist der Beleg für die These vom Anfang. Ich habe denselben
Prompt auf einen Englischkurs auf Stufe A1 angesetzt. Dort meldet er null
Befunde zum Sprachniveau, hier elf. Er hat vorher bestimmt, wer liest, und
legt deshalb zwei verschiedene Maßstäbe an.

Ich habe das viermal je Kurs laufen lassen. Beim Deutschkurs elf bis zwölf
Niveau-Befunde, beim Englischkurs jedes Mal null. Ein einzelner Lauf wäre
keine Messung gewesen, und genau das war die Zahl vorher.


## 10 — Stakeholder

typ: matrix
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer eingebunden
akzent: werden muss.
klein: ja
yhoch: Einfluss hoch
yniedrig: Einfluss niedrig
xniedrig: Betroffenheit niedrig
xhoch: Betroffenheit hoch
oben_links: Beobachten || Städtische IT || Advellence, Portal- und Kursverwaltungssystem || Hessische Durchsetzungsstelle
oben_rechts: Eng einbinden || Direktor als Verantwortlicher der Inhalte || Vier Fachbereiche, acht Programmbereiche || Redaktion des Programmhefts || Personalrat, zwei Sitze in der Betriebskommission
unten_links: Informieren || Betriebskommission || Stadtkämmerei
unten_rechts: Konsultieren || Kursleitungen auf Honorarbasis || Inklusionsbeauftragte || Teilnehmende, besonders in DaF und Grundbildung
callout: Die Kursleitungen sind hoch betroffen und haben keinen formalen Einfluss.
calloutsub: Sie sind nicht weisungsgebunden. Beteiligung ist hier kein guter Stil, sondern das einzige verfügbare Instrument.

### NOTIZ

Damit komme ich zum Change-Teil. Er beginnt mit der Frage, wer eigentlich
betroffen ist. Die Achsen sind Einfluss und Betroffenheit.

Oben rechts, eng einzubinden: der Direktor, der laut Impressum persönlich für
die redaktionellen Inhalte verantwortlich ist. Die vier Fachbereiche, die die
acht Programmbereiche und damit die Texte verantworten. Die Redaktion des
Programmhefts, die es für den Druck bereits gibt. Und der Personalrat, der
zwei Sitze in der Betriebskommission hat.

Oben links, zu beobachten: die städtische IT, der Portaldienstleister und die
hessische Durchsetzungsstelle. Hoher Einfluss, aber geringe Betroffenheit,
weil mein Projekt ihre Arbeit nicht verändert. Unten links nur informieren:
die Betriebskommission und die Kämmerei.

Und unten rechts der Quadrant, der mich am meisten beschäftigt hat. Die
Kursleitungen sind maximal betroffen, denn sie schreiben viele dieser Texte.
Und sie haben keinen formalen Einfluss, weil sie in keinem Gremium sitzen. Sie
sind Honorarkräfte, man kann ihnen nichts vorschreiben.

Genau deshalb steht unten der Satz: Beteiligung ist hier kein guter Stil,
sondern das einzige Instrument, das überhaupt zur Verfügung steht.

Ein Hinweis zur Matrix selbst. Ich verwende die Achsen aus dem Aufgabenblatt,
Einfluss und Betroffenheit. In der Change Toolbox ist sie als
Einfluss-Interesse-Matrix geführt. Betroffenheit halte ich hier für
trennschärfer, weil die Kursleitungen sehr betroffen sind, ohne besonderes
Interesse an dem Thema zu haben.


## 11 — Widerstand

typ: zweispalt
kapitel: 03 · CHANGE MANAGEMENT
bild: bilder/14-widerstand.jpg
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
  - "Quick Win zuerst: ein Textbaustein steht in 36 Kursen. Einmal überarbeiten, 36 Texte besser."
callout: Betroffene zu Beteiligten machen. Der Pilotbereich wählt selbst, welche Regeln zuerst gelten.

### NOTIZ

Jetzt zum Widerstand. Ich habe die vier Ursachen aus dem Unterricht genommen
und für jede den Satz aufgeschrieben, den ich in diesem Haus tatsächlich
erwarte.

Verlustangst klingt hier so: Jetzt korrigiert mich eine Maschine. Dahinter
steckt Verlustaversion. Wir gewichten einen Verlust etwa doppelt so stark wie
einen gleich großen Gewinn. Die Kursleitung sieht zuerst den Kontrollverlust
über ihren eigenen Text, nicht die Entlastung.

Unsicherheit klingt so: Wird damit meine Arbeit bewertet? Das ist die
gefährlichste Frage, und sie ist berechtigt. Meine Antwort ist dieselbe wie
auf der Prompt-Folie. Es werden Texte ausgewertet, nicht Personen. Keine
Statistik nach Urheberin, keine Rangliste. Und das gehört nicht nur gesagt,
sondern schriftlich zugesichert und dem Personalrat vorgelegt, bevor der Pilot
beginnt und nicht danach.

Gewohnheit und fehlende Perspektive begegne ich mit dem Zuschnitt selbst. Ich
ändere nicht, wie jemand schreibt, sondern ergänze einen Schritt danach. Und
ich fange mit den Textbausteinen an, weil eine einzige Überarbeitung dort
sechsunddreißig Kurse gleichzeitig verbessert.

Der Satz unten ist der Kern jeder Widerstandsarbeit. Betroffene zu Beteiligten
machen. Konkret heißt das, dass der Pilotbereich selbst entscheidet, welche
der sechs Prüfregeln zuerst scharf gestellt werden.


## 12 — Timeline

typ: timeline
kapitel: 03 · CHANGE MANAGEMENT
titel: Drei Monate,
akzent: drei Stränge.
klein: ja
monate: Monat 1 | Monat 2 | Monat 3
strang1: Technische Implementation || Assistent im vorhandenen Rahmen anlegen, Regeln schärfen || +Pilot in einem Programmbereich || Ausweitung auf alle acht
strang2: Kommunikation || Ankündigung, Personalrat einbeziehen || Schulung nach Artikel 4 KI-Verordnung || ~Sprechstunde und Support
strang3: Change || Betroffene befragen, Bausteine sichten || Quick Win Textbausteine || Nachmessung und Entscheidung
callout: Der Kommunikationsstrang beginnt vor dem technischen.
calloutsub: Die Schulung im zweiten Monat ist keine Kür: Artikel 4 der KI-Verordnung verpflichtet Betreiber seit Februar 2025 zu ausreichender KI-Kompetenz ihres Personals.
quellen:
  - "KI-Verordnung (EU) 2024/1689, Artikel 4 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Der Zeitplan, drei Monate, drei Stränge.

Technisch ist wenig zu tun, und das ist ein Vorteil dieses Projekts. Im ersten
Monat wird der Assistent im vorhandenen Rahmen angelegt und an echten Texten
nachgeschärft. Im zweiten läuft der Pilot in einem Programmbereich. Im dritten
folgt die Ausweitung.

Der Kommunikationsstrang beginnt bewusst vor dem technischen. Ankündigung und
Einbeziehung des Personalrats stehen im ersten Monat, also bevor irgendetwas
läuft.

Die Schulung im zweiten Monat ist übrigens keine Kür. Artikel vier der
KI-Verordnung verpflichtet Betreiber seit Februar zweitausendfünfundzwanzig,
für ausreichende KI-Kompetenz ihres Personals zu sorgen. Mein
Qualifizierungsbaustein erfüllt damit eine Rechtspflicht.

Der Change-Strang folgt einer einfachen Reihenfolge: erst fragen, dann
handeln. Der Quick Win mit den Textbausteinen liegt im zweiten Monat, weil er
dann auf eine schon geweckte Erwartung trifft.


## 13 — Die ersten 30 Tage und die Ressourcen

typ: zweispalt
kapitel: 03 · ZEITPLAN UND RESSOURCEN
bild: bilder/11-zeitleiste.jpg
bildprompt: Waagerechte Zeitleiste als dicker Balken mit unterschiedlich hohen Markierungen. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Die ersten 30 Tage,
akzent: und was sie kosten.
klein: ja
spalte1: ERSTE 30 TAGE
punkte1:
  - "Personalrat einbinden, Zusicherung schriftlich vorlegen"
  - "Einen Programmbereich als Pilotbereich gewinnen"
  - "Assistent im vorhandenen KI-Rahmen anlegen"
  - "Textbausteine sichten, den Quick Win vorbereiten"
spalte2: RESSOURCEN
punkte2:
  - "Pilot: rund 4 Stunden in drei Monaten"
  - "Regelbetrieb: 29 Stunden im Jahr für alle neuen Texte"
  - "Von rund 2.800 Kursen im Semester sind nur 293 neu"
  - "Keine Beschaffung, keine zusätzliche Stelle"
callout: Alle Veranstaltungen einzeln zu prüfen wären 290 Stunden im Jahr. Nur die neuen zu prüfen sind 29.
calloutsub: Nachgerechnet an 489 Kursen über die Portalschnittstelle, nicht geschätzt.
quellen: eigene Erhebung, Wirtschaftlichkeitsrechnung liegt der Arbeit bei

### NOTIZ

Damit zu den nächsten Schritten. Links die ersten dreißig Tage: Personalrat
einbinden, einen Pilotbereich gewinnen, den Assistenten anlegen, die
Textbausteine sichten.

Rechts die Ressourcen, denn der häufigste Einwand lautet, das koste zu viel
Zeit. Jede Veranstaltung einzeln zu prüfen wären rund zweihundertneunzig
Stunden im Jahr. Von zweitausendachthundert Kursen im Semester sind aber nur
zweihundertdreiundneunzig neu. Prüft man nur diese, sind es neunundzwanzig
Stunden im Jahr, im Pilot vier.


## 14 — Erfolgsmessung und Risiken

typ: tabelle
kapitel: 03 · ERFOLGSMESSUNG
bild: bilder/17-waage.jpg
bildprompt: Geometrische Waage, Balken auf dreieckigem Drehpunkt, Kreis und Quadrat als Gewichte. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Woran man merkt,
akzent: ob es gewirkt hat.
klein: ja
lede: Die Ausgangsmessung liegt vor, erhoben mit einem Skript. Die Nachmessung läuft mit demselben Skript. Die vierte Zeile misst nicht den Text, sondern die Wirkung — dafür werden die Teilnehmenden selbst gefragt.
spalten: Kennzahl | heute | Ziel nach 3 Monaten | gemessen mit
zeilen:
  - "Texte mit mindestens einem Befund | 90 % | ! unter 40 % | demselben Skript wie die Ausgangsmessung"
  - "Neue Texte im Pilotbereich geprüft | 0 | + alle | Protokoll des Werkzeugs"
  - "DaF-Texte mit C1-Vokabular | 9 von 13 | ! höchstens 2 von 13 | Nachmessung, identisches Verfahren"
  - "Teilnehmende, die die Beschreibung verstanden haben | nicht erhoben | + Ausgangswert und Trend | Kurzbefragung am Kursende, durch die Kursleitung"
callout: Drei Risiken, drei Gegenmaßnahmen.
calloutsub: Mitbestimmung stockt → Zusicherung schriftlich, vor dem Pilot. Redaktion misstraut schwankenden Befunden → Pflichtbefunde sind stabil, der Pilotbereich wählt die scharfen Regeln selbst. KI-Rahmen doch nicht verfügbar → der Prompt läuft auch außerhalb, geklärt wird das im ersten Monat.
quellen: Ausgangsmessung 28.07.2026, Erhebung an 489 Kursen über die Portalschnittstelle

### NOTIZ

Und woran würde man merken, ob es gewirkt hat?

Vier Kennzahlen mit Ausgangswert und Ziel. Die Befundquote soll von neunzig
Prozent unter vierzig fallen. Alle neuen Texte im Pilotbereich sollen geprüft
sein. Und die Deutschkurse mit C1-Vokabular sollen von neun von dreizehn auf
höchstens zwei sinken.

Die vierte Zeile ist mir wichtig, weil die ersten drei nur den Text messen und
nicht die Wirkung. Deshalb frage ich die Teilnehmenden selbst. Nicht über einen
Fragebogen auf der Website, denn den füllt genau die Zielgruppe nicht aus, um
die es geht. Sondern im Kurs, am Ende einer Stunde, durch die Kursleitung, in
einfacher Sprache. Das erreicht die Menschen wirklich, und es bindet die
Kursleitungen ein, die sonst in keinem Gremium sitzen. Ergänzend führt die
Anmeldung im Pilotbereich eine Strichliste, wie oft jemand nachfragen muss, was
in einer Beschreibung stand.

Wichtig ist die letzte Spalte. Die Nachmessung läuft mit demselben Skript wie
die Ausgangsmessung. Niemand kann später über die Messmethode streiten.

Unten die drei Risiken. Stockt die Mitbestimmung, hilft nur die schriftliche
Zusage vorher. Misstraut die Redaktion den schwankenden Befunden, sind die
stabilen Pflichtbefunde das Gegenargument. Und sollte der KI-Rahmen nicht
bereitstehen, läuft der Prompt auch außerhalb.


## 15 — Schlussfolie

typ: schluss
bild: bilder/15-durchgang.jpg
bildprompt: Wand aus dichten Balken mit einem Durchgang, dahinter Helligkeit, eine Figur geht hindurch. Flach-geometrisch, Bauhaus, keine Schrift.
titel: Der Prompt ist ein Nachmittag Arbeit.
akzent: Alles, was ihn erlaubt, ist der eigentliche Aufwand.
untertitel: Ich zeige das Werkzeug jetzt live. Danach freue ich mich auf eure Fragen.
fussl: PROJEKT KLARTEXT · VHS FRANKFURT
fussr: HENRIK HEIL · CIMDATA 2026

### NOTIZ

Ich fasse zusammen.

Ich habe ein reales Unternehmen analysiert, einen Prozess gefunden, in dem
niemand etwas falsch macht und trotzdem etwas fehlt, und ich habe den Zustand
gemessen statt geschätzt.

Der System-Prompt selbst ist an einem Nachmittag geschrieben. Das ist meine
eigentliche Lehre aus diesem Projekt. Die Arbeit steckt in allem, was ihn
möglich macht: zu wissen, für wen ein Text ist, zu wissen, was Pflicht ist und
was Anspruch, und einen Weg zu finden, auf dem die Menschen, die diese Texte
schreiben, das Werkzeug nicht als Kontrolle erleben.

Ich zeige euch jetzt kurz, wie es läuft. Danach gerne eure Fragen.
