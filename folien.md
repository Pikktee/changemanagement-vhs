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
# Im NOTIZ-Block ist Markdown erlaubt und wird im Vortragswerkzeug gesetzt:
#   "# " und "### " Ueberschrift, "- " und "1. " Liste, "> " Zitat,
#   "---" Trennlinie, **fett**, *kursiv*.
#   ((Text in doppelten Klammern)) ist eine Nebenbemerkung: kleiner und leicht
#   gedaempft, fuer Saetze, die nur bei genug Zeit vorgelesen werden. Sie darf
#   ueber mehrere Zeilen gehen, aber nicht ueber eine Leerzeile.
#   ==Text zwischen Gleichheitszeichen== ist das Gegenteil: roetlich und fett,
#   fuer die Stelle, die nicht untergehen darf. Nur innerhalb einer Zeile.
#   HTML geht nicht — ein <small> erscheint woertlich auf der Notizseite.
#   NICHT "## " am Zeilenanfang — das beginnt auch mitten in einer Notiz eine
#   neue Folie und zerlegt die Datei. Fuer eine Ueberschrift "# " oder "### ".
#
# Notizen lassen sich auch im Vortragswerkzeug bearbeiten:
#   python3 notizen.py --server, dann Taste E oder der Stift.
#   Wer diese Datei hier aendert, waehrend dort eine Seite offen ist, muss sie
#   neu laden — sonst schreibt sie beim Speichern ihren alten Stand zurueck.
#
# Folientypen: titel, schluss, kapitel, punkte, zahlen, zweispalt,
#              tabelle, zitat, text
# Alle Felder pro Typ stehen in README-FOLIEN.md


## 1 — Titelfolie

typ: titel
titel: KLARTEXT — Kursbeschreibungen
akzent: barrierefrei prüfen.
untertitel: Ein KI-gestützter Prüfschritt vor der Veröffentlichung.
link: klartext-vhs.henrikheil.net
meta: Volkshochschule Frankfurt am Main | Acht Programmbereiche | 5.800 Texte im Jahr
fussl: ABSCHLUSSPROJEKT · CHANGE UND KI
fussr: CIMDATA · HENRIK HEIL · JULI 2026
bild: bilder/01-titel-wand.png
bildnotiz: Wand aus Textzeilen mit einem Schlitz. Gezeichnet von bilder/zeichnen.py, Gegenstueck auf der Schlussfolie.

### NOTIZ

### Begrüßung

Willkommen zu meinem Abschlussprojekt!
- KLARTEXT, ein KI-gestützter Prüfschritt für die Kursbeschreibungen der Volkshochschule Frankfurt.

### Worum geht es?

- Barrierefreiheit.
- Aber nicht der technische Teil wie Kontraste oder Tastaturbedienung, sondern:
- ob der Text ankommt bei denen, für die er geschrieben ist.

### Ein konkreter Fall
- Beispiel: Die Volkshochschule bietet Deutschkurse für Menschen an, die gerade erst Deutsch lernen.
- Die Beschreibungen dieser Kurse sind oft in einem Deutsch geschrieben, das man erst nach dem Kurs versteht.


## 2 — Executive Summary I: Worum es geht

typ: zahlen
kapitel: ÜBERBLICK
titel: Die Technik wird geprüft,
akzent: die Texte nicht.
lede: Die Kursbeschreibungen entstehen in acht Programmbereichen und erscheinen unverändert im Portal, im Programmheft und im Newsletter. Einfache Sprache bietet das Unternehmen an — für Betrieb und Kursgeschäft, nicht für die Kurstexte selbst.
zahlen:
  - "5.800 || Kursbeschreibungen im Jahr"
  - "57 % || haben mindestens einen Befund || warn"
  - "5 Jahre || seit dem letzten externen Barrierefreiheitstest || warn"
callout: Mehr als jeder zweite Text hat einen Befund. Die Frage ist, für wen er zu schwer ist.
quellen:
  - "Eigene Auswertung aller 3.111 Kurstexte des Portals, 30.07.2026"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"
  - "Erklärung zur Barrierefreiheit der vhs, 23.09.2025 | https://vhs.frankfurt.de/de/special-pages/support/barrierefreiheit"

### NOTIZ

Erstmal eine kurze Übersicht zum Projekt.

### 5.800 Texte und 57 Prozent

- Die Volkshochschule veröffentlicht rund 5800 Kursbeschreibungen im Jahr.
- Von allen Texten, die heute im Portal stehen, hat mehr als jeder zweite Text einen Befund. ((Die Zahl stammt von einem Skript, das ohne KI auskommt und deshalb eine der sechs Regeln nicht prüfen kann. Mit dem Prüfassistenten liegt der Wert höher.))

### Fünf Jahre ohne externe Prüfung
Die letzte externe Prüfung auf Barrierefreiheit der Website ist etwa 5 Jahre
her. Die Zahl stammt aus der Erklärung zur Barrierefreiheit der
Volkshochschule.

### Einfache Sprache, der eigentliche Anlass
Dort heißt es auch, dass Informationen zu Betrieb und Kursgeschäft in
einfacher Sprache verfügbar sind. Das gilt jedoch nicht für die
Kursbeschreibungen selbst, die immerhin den größten Textbestand darstellen.

### Der Kasten unten
Vor allem hier setzt das Projekt an.


## 3 — Executive Summary II: Der Vorschlag

typ: punkte
kapitel: ÜBERBLICK
bild: bilder/03-prozess-voll.png
bildnotiz: Die Kette der Arbeitsschritte mit besetzter Stelle. Was neu ist, steht in der Akzentfarbe. Gegenstueck auf Folie 4.
titel: Der Vorschlag,
akzent: und was er bringt.
punkte:
  - "**Ziel** || Wer einen Kurs sucht, versteht die Beschreibung, ob gelesen oder vorgelesen. Laut Betriebssatzung stehen die Angebote allen offen — das soll auch für die Texte gelten."
  - "**Lösung** || Ein Prüfschritt vor der Veröffentlichung, als System-Prompt im KI-Zugang, den der Volkshochschul-Verband schon bereitstellt. Keine Beschaffung, kein neuer Vertrag."
  - "**Abgrenzung** || Die technische Barrierefreiheit der Website bleibt bei der städtischen IT. Die KI sieht nur den Kurstext."
  - "**Ergebnis** || Befundquote nach drei Monaten unter 25 Prozent statt heute 57. Aufwand im Regelbetrieb 29 Stunden im Jahr."
callout: Erster Schritt: ein Pilot in einem Programmbereich, drei Monate, ohne Beschaffung.
calloutsub: Der Prompt schlägt vor, der Mensch entscheidet und veröffentlicht.
quellen:
  - "Betriebssatzung der vhs Frankfurt | https://vhs.frankfurt.de/de/special-pages/important/betriebssatzung"

### NOTIZ

Daraus folgt mein Vorschlag.

### Ziel
- *vorlesen*

### Lösung
- ==Ein Prüfschritt zur Sicherstellung der Zugänglichkeit eines Kurstextes für die Zielgruppe des Textes vor der Veröffentlichung.== (weiter vorlesen)

### Abgrenzung
- Für die technische Barrierefreiheit der Website bleiben normale Prüfwerkzeug zuständig, zusammen mit der städtischen IT. Die KI sieht nur den Kurstext.

### Ergebnis
- *vorlesen*

### Der Kasten unten
- *vorlesen*


## 4 — Das Unternehmen und der Prozess heute

typ: zweispalt
kapitel: 01 · UNTERNEHMEN UND IST-ANALYSE
titel: Die vhs Frankfurt,
akzent: und wie ein Kurstext entsteht.
klein: ja
betont: 2
lede: Volkshochschule Frankfurt am Main, gegründet 1890. Laut Betriebssatzung stehen die Angebote grundsätzlich allen offen, ohne Rücksicht auf Vorbildung.
spalte1: DAS UNTERNEHMEN
punkte1:
  - "Eigenbetrieb der Stadt, 154.000 € Stammkapital, seit 2005 extern qualitätsgeprüft"
  - "5.800 Veranstaltungen im Jahr, acht Programmbereiche in vier Fachbereichen"
  - "Der Direktor ist laut Impressum persönlich für die Inhalte verantwortlich"
  - "Betriebskommission mit 16 Sitzen, zwei davon für den Personalrat"
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
  - "Ablauf des Hauses: eigene Recherche, Belege und Annahmen dokumentiert"

### NOTIZ

Zunächst zum Unternehmen und zum aktuellen Prozess.

### Das Unternehmen
- kein Amt, sondern ein Eigenbetrieb der Stadt.
- seit 2005 extern qualitätsgeprüft nach **LQW**, **Lernerorientierte Qualitätstestierung in der Weiterbildung**
- Es gibt acht Programmbereiche in vier Fachbereichen
- Geleitet wird sie von einem Direktor, der laut Impressum auch persönlich für die redaktionellen Inhalte der Website verantwortlich ist.
- Darüber steht eine Betriebskommission mit 16 Sitzen, 2 davon für den Personalrat.

### Der Satz oben aus der Betriebssatzung
Der Satz oben stammt wörtlich aus der Betriebssatzung: Die Angebote stehen
grundsätzlich allen offen, ohne Rücksicht auf Vorbildung.

### So entsteht ein Kurstext
- *(vorlesen)*


## 5 — Messung und eigentlicher Befund

typ: tabelle2
kapitel: 01 · POTENZIALERMITTLUNG
titel: Was zählt als Befund,
akzent: und für wen.
klein: ja
lede: Alle 3.111 Kurstexte des Portals, Abruf vom 28.07.2026. 1.765 davon haben einen Befund.
regelntitel: Wonach gemessen wurde
regeln:
  - "PFLICHT · verbindlich nach WCAG | STRUKTUR | Überschrift oder Liste ohne semantisches HTML"
  - "| LINKTEXT | Linktext nennt sein Ziel nicht"
  - "EMPFEHLUNG | NIVEAU | Wort über dem Sprachniveau der Zielgruppe"
  - "| AMTSDEUTSCH | Behördenwort, wo ein Alltagswort reicht"
  - "| SATZ | über 25 Wörter, bei Deutschkursen über 15"
  - "| ABKÜRZUNG | Kürzel ohne Auflösung, etwa DTZ"
tabellentitel: Zwei Kurse im Vergleich
spalten: Kurs | Wer die Beschreibung liest | Wörter über Niveau | Befunde
zeilen:
  - "Englisch A1.1 | liest Deutsch fließend | 0 | 1"
  - "Deutsch als Fremdsprache A2.2 | lernt Deutsch, kann bisher A1 | 53 | 57"
callout: Beide Kurse tragen A im Titel. Nur bei einem ist der Text zu schwer für seine Leser.
calloutsub: Ob ein Text verständlich ist, entscheidet nicht der Text — sondern die Zielgruppe, die ihn lesen soll.
quellen:
  - "Eigene Auswertung aller 3.111 Kurstexte, 30.07.2026 — Auswertung und Daten liegen der Arbeit bei"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"

### NOTIZ

Zur Potenzialermittlung. Was zählt als Befund und für wen?

- Erstmal kurz zur Messung: Das Kursportal hat eine offene Schnittstelle. Darüber habe ich alle Kurstexte erhalten und mit einem Skript ausgewertet.

### Wonach wurde gemssen?
- Nach 6 Regeln, die auch im System-Prompt Verwendung finden

### Es gibt 2 Pflichtregeln
- Stehen auf Stufe A der Barrierefreiheitsrichtlinien und sind damit gesetzlich verbindlich.
- **STRUKTUR**: z.B. eine Zeile sieht aus wie eine Überschrift, ist im Quelltext aber gewöhnlicher Fließtext.
- **LINKTEXT**: Der Linktext sagt nicht, wohin er führt. Beispiel: „hier“
- **Bei beiden**: Screen-Reader können die Inhalte damit nicht zuverlässig lesen.

### Die vier Empfehlungen
- Nicht verbindlich, aber sind die wichtigsten des Projekts.
- **NIVEAU:** Niveau heißt: Ein Wort liegt über dem Sprachniveau der Menschen, die den Text lesen sollen. Das ist die Regel, die sich ohne Kenntnis der Zielgruppe überhaupt nicht anwenden lässt.
- **AMTSDEUTSCH**: (vorlesen)
- **SATZ**: Zur Satzlänge sagen die Barrierefreiheitsrichtlinien nichts. Aber die Zahlen orientieren sich an den Empfehlungen für einfache Sprache.
- **ABKÜRZUNG**: Ein Kürzel steht im Text, ohne beim ersten Mal aufgelöst zu werden. Davon hat die vhs einige, D-T-Z zum Beispiel, der Deutsch-Test für Zuwanderer.

### Zwei Kurse im Vergleich als Beispiel
- Englisch A1.1 und Deutsch als Fremdsprache A2.2
- Beide Beschreibungen sind auf Deutsch. ==Nur kann die eine Zielgruppe Deutsch — die andere lernt es gerade erst.==
- Englischkurs: kein einziges zu schweres Wort. Deutschkurs: dreiundfünfzig.
- Beide Texte haben kurze Sätze. Ein Programm, das nur zählt, findet bei keinem etwas.

### Der Kasten unten
- Man muss wissen, für wen der Text ist. Für Deutschkurse auf den Stufen A1 und A2 gibt es z.B. 31 verschiedene Texte, die  Wörter über dem Niveau ihrer Leser enthalten. Genau hier kann ein KI-Prompt etwas, was ein Standardwerkzeug nicht kann.


## 6 — Rechtslage

typ: text
kapitel: 01 · RECHTLICHER RAHMEN
titel: Welches Recht gilt,
akzent: und was nicht.
klein: ja
absaetze:
  - "Digitale Barrierefreiheit heißt: Websites müssen so gebaut sein, dass auch Menschen mit Behinderung sie nutzen können. Der Maßstab sind die **WCAG** mit den Stufen A, AA und AAA."
  - "Für die vhs als kommunale Einrichtung in Hessen gilt **Landesrecht**: § 14 HessBGG und die **BITV HE**. Gefordert ist Stufe **AA**."
kriterientitel: Was das für Kursbeschreibungen bedeutet
kriterien:
  - "PFLICHT · bis Stufe AA | 1.3.1 | Struktur ausgezeichnet"
  - "| 2.4.4 | Linktext nennt sein Ziel"
  - "FREIWILLIG · Stufe AAA | 3.1.4 | Abkürzungen erklärt"
  - "| 3.1.5 | Leseniveau der Zielgruppe"
callout: Ausgerechnet die Kriterien für Menschen mit geringer Vorbildung sind freiwillig.
calloutfolge: Freiwillig heißt nicht belanglos. § 3 Abs. 1 BITV HE verlangt eigenständig, dass Angebote verständlich sind — und die Betriebssatzung, dass sie allen offenstehen, ohne Rücksicht auf Vorbildung.
quellen:
  - "HessBGG, BITV HE 2019, EN 301 549"
  - "WCAG 2.1 | https://www.w3.org/TR/WCAG21/"
  - "Landesfachstelle Barrierefreie IT Hessen | https://lbit.hessen.de/oeffentliche-stellen/allgemeine-anforderungen-der-barrierefreien-it"
  - "Erklärung zur Barrierefreiheit der vhs | https://vhs.frankfurt.de/de/special-pages/support/barrierefreiheit"

### NOTIZ

Zunächst noch kurz zur Rechtslage.

### Was bedeutet Barrierefreiheit?
- Digitale Barrierefreiheit bedeutet, dass eine Website auch für Menschen mit Behinderung nutzbar sein muss. Der Maßstab sind die WCAG, mit drei Stufen: A, Doppel A und Dreifach A.

### Welches Recht gilt?
- Wichtig: Für die vhs gilt weder die EU-Richtlinie noch das Barrierefreiheitsstärkungsgesetz unmittelbar.
- Als kommunale Einrichtung in Hessen greift Landesrecht: Paragraph 14 des Hessischen Behindertengleichstellungsgesetzes und die hessische Verordnung. Gefordert wird Stufe Doppel A.

### Callout
- Einige der Regeln sind freiwillig, da sie nicht in WCAG Doppel A enthalten sind.
- Freiwillig heißt aber nicht belanglos. Paragraph 3 Absatz 1 der hessischen Verordnung verlangt eigenständig, dass Angebote verständlich sind.
- Außerdem sagt die Betriebssatzung, dass die Angebote allen offen stehen, ohne Rücksicht auf Vorbildung.


## 7 — Die Arbeitsteilung

typ: zweispalt
kapitel: 02 · ABGRENZUNG
titel: Was die Technik prüft,
akzent: und wo KLARTEXT ansetzt.
klein: ja
betont: 2
betontmarke: → Hier setzt Projekt KLARTEXT an
spalte1: DIE WEBSITE · städtische IT
punkte1:
  - "Kontraste, Tastaturbedienung, Seitentitel, Navigation"
  - "Prüfbar, ohne den einzelnen Kurs zu kennen"
  - "Etablierte Programme wie axe-core, bei jeder Änderung"
  - "Gilt für alle 5.800 Texte gleich"
spalte2: DER EINZELNE TEXT · Programmbereiche
punkte2:
  - "Versteht die Zielgruppe genau dieses Kurses ihn?"
  - "Nicht prüfbar, ohne zu wissen, wer liest"
  - "Vorschlag der KI, Entscheidung beim Fachbereich"
callout: Ob ein Text zu seinen Lesern passt, steht in keinem Regelwerk.
calloutfolge: Die Technik bleibt bei der städtischen IT. Neu ist allein der Schritt, der die Zielgruppe kennen muss.
calloutsub: Technische Voraussetzungen: der KI-Zugang, den der Volkshochschul-Verband schon bereitstellt, ein dort angelegter Assistent, die Wortliste als Datei. Keine Beschaffung, kein Eingriff ins Kursverwaltungssystem.
quellen:
  - "WCAG 2.1 | https://www.w3.org/TR/WCAG21/"
  - "Deque axe-core | https://github.com/dequelabs/axe-core"

### NOTIZ

Zur Lösung. Sie beginnt mit einer Abgrenzung, und die halte ich für den
wichtigsten Teil meines Konzepts.

### Die Website
- Links steht, was an der Website als Ganzem hängt: Kontraste, Tastaturbedienung, Seitentitel, Navigation.
- Prüfbar, ohne einen einzigen Kurs zu kennen. Gilt für alle 5800 Texte gleich.
- Dafür gibt es etablierte Programme wie **axe-core**. Zuständig ist die städtische IT.

### Der einzelne Text
- Rechts steht, was am einzelnen Text hängt: ==Versteht die Zielgruppe genau dieses Kurses ihn?==
- Das lässt sich nicht beantworten, ohne zu wissen, wer liest. Zuständig sind die Programmbereiche.

### Der Kasten unten
- Die Trennlinie verläuft also nicht zwischen Sprache und Technik. Zwei meiner sechs Regeln sind selbst Pflichtkriterien.
- Beispiel: eine hervorgehobene Zeile, die als Überschrift gemeint ist, im Quelltext aber keine. Das Prüfprogramm sieht dort nur Fließtext und meldet nichts.
- Ob sie eine Überschrift sein sollte, kann man dem Text nicht ansehen, sondern nur verstehen. Deshalb liegt dieses Pflichtkriterium rechts.
- ((Beim Bauen hat sich das dreimal bestätigt: Drei Zusagen, die zuerst im Prompt standen, hielt das Modell nicht zuverlässig ein. Alle drei stehen heute im Programmcode.))

### Technische Voraussetzungen
- Der KI-Zugang, den der Volkshochschul-Verband ohnehin bereitstellt, ein dort angelegter Assistent, die Wortliste als Datei.
- Kein neuer Vertrag, kein Eingriff ins Kursverwaltungssystem.


## 8 — Der Prompt in sechs Bausteinen

typ: tabelle
kapitel: 02 · SYSTEM-PROMPT
titel: Der System-Prompt in
akzent: sechs Bausteinen.
klein: ja
spalten: Baustein | Was darin steht
zeilen:
  - "ROLLE | Redaktionsassistenz der vhs. Liest wie eine erfahrene Lektorin, entscheidet nichts."
  - "AUFGABE | Zielgruppe des Kurses bestimmen, dann prüfen, ob sie den Text verstehen kann."
  - "FORMAT | Feste Ausgabe: Zielgruppe, Befunde mit Zitat, Grund und Vorschlag, Zusammenfassung."
  - "GRENZEN | Bewertet Texte, niemals Personen. Ändert nichts, veröffentlicht nichts, erfindet nichts."
  - "KONTEXT | Acht Programmbereiche, interne Abkürzungen, sechs Prüfregeln, 820 Wörter des Goethe-Zertifikats A1."
  - "REGELN | Namen entfernen, wörtlich zitieren, höchstens fünfzehn Befunde, Pflicht vor Empfehlung."
callout: Ein einziger Satz hält das Projekt aus dem Hochrisikobereich der KI-Verordnung.
calloutfolge: „Bewertet Texte, niemals Personen.“ Die Verordnung stuft nur hoch ein, was Menschen bewertet — dieses System bewertet Texte. Derselbe Satz beantwortet die Frage des Personalrats nach Leistungskontrolle.
quellen:
  - "System-Prompt, Fassung v11 vom 29.07.2026 — zwölf Fassungen mit Anlass und Begründung"
  - "KI-Verordnung (EU) 2024/1689, Anhang III | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Zum Kern der Aufgabe, dem System-Prompt. Er folgt der Sechs-Komponenten-
Struktur aus dem Aufgabenblatt.

### Rolle, Aufgabe, Format
- **ROLLE**: Redaktionsassistenz, nicht Autorin.
- **AUFGABE**: erst die Zielgruppe bestimmen, dann prüfen. Die Reihenfolge steht fest.
- **FORMAT**: zu jedem Befund ein wörtliches Zitat, eine Begründung, ein konkreter Vorschlag. ==Ohne Vorschlag kein Befund.==

### Kontext: die Wortliste
- Der KONTEXT enthält das Hauswissen: acht Programmbereiche, interne Abkürzungen, sechs Prüfregeln.
- Der wichtigste Teil: 820 Wörter des Prüfungswortschatzes für das **Goethe-Zertifikat A1**. Vollständig im Prompt, nicht als Verweis.
- ==Er schätzt das Sprachniveau also nicht, er begründet es.==
- Das ist das Ergebnis der ersten Überarbeitung: Vorher behauptete der Prompt, gegen Wortlisten zu prüfen, hatte sie aber gar nicht. Er schätzte frei und klang nach Beleg — derselbe Fehler, den ich anderen Werkzeugen vorwerfe.
- ((Der Grundstock dieser Listen stammt laut Goethe-Institut aus einer Veröffentlichung der Prüfungszentrale des Deutschen Volkshochschul-Verbands in Frankfurt.))

### Der Kasten unten: die Zeile GRENZEN
- „Bewertet Texte, niemals Personen.“ Dieser eine Satz leistet zweierlei.
- Er hält das Projekt aus dem Hochrisikobereich der KI-Verordnung: Hoch eingestuft wird dort nur, was Menschen bewertet — dieses System bewertet Texte.
- Und er ist die Antwort auf die Frage des Personalrats, ob hier Leistung kontrolliert wird.


## 9 — Wie es praktisch laeuft

typ: wege
kapitel: 02 · TECHNISCHE IMPLEMENTIERUNG
bild: bilder/09-befunde-prototyp.png
bildganz: ja
bu: Ausschnitt aus einem Durchlauf im Prototyp: Einstufung, Regel, Stelle im Text, Vorschlag.
titel: Der System-Prompt
akzent: im Einsatz.
klein: ja
wege:
  - "Als KI-Assistent bei fobizz || Prompt einmal hinterlegen, dann Kurstext einfügen und Befunde lesen || Der Rahmenvertrag des Verbands mit fobizz besteht seit Mai 2025 und erlaubt eigene Assistenten. Niemand außerhalb des Pilotbereichs muss zustimmen."
  - "Als eigenes Prüfwerkzeug || Entwurf einfügen — oder Kursnummer eingeben, dann holt es den Text selbst || Ein eigener Server, sonst nichts: die Kursportal-Schnittstelle ist öffentlich. Hier laufen Namensschutz und Korrektur der Einstufung im Code mit."
callout: Später möglich: die Prüfung im Redaktionssystem selbst, dort, wo der Text entsteht.
calloutnotiz: ja
calloutsub: Das Portal betreut ein externer Dienstleister — die Erweiterung wäre ein Auftrag mit Budget und Vorlauf.
quellen:
  - "Rahmenvereinbarung DVV und fobizz, 05.05.2025 | https://www.volkshochschule.de/meldungen/kooperation-mit-fobizz.php"
  - "fobizz für Volkshochschulen | https://fobizz.com/de/volkshochschulen/"
  - "Impressum der vhs Frankfurt, Advellence Solutions AG | https://vhs.frankfurt.de/de/special-pages/important/impressum"

### NOTIZ

Bleibt die Frage, wie das in den Alltag kommt. Zwei Wege, beide vom ersten Tag
an offen.

### Weg 1: Als KI-Assistent bei fobizz
- Braucht keine eigene Technik.
- Der Deutsche Volkshochschul-Verband hat im Mai 2025 eine Rahmenvereinbarung mit **fobizz** geschlossen: datenschutzkonformer KI-Zugang für alle Volkshochschulen, mit eigenen Assistenten und eigenen Anweisungen.
- Genau das ist mein Prompt. Zustimmung außerhalb des Pilotbereichs braucht es nicht, weil der Rahmenvertrag schon da ist.
- ((Zu klären bleibt, ob die vhs Frankfurt die Lizenz auch gebucht hat. Der Rahmenvertrag schafft die Möglichkeit, er ist nicht die Buchung.))

### Die Einschränkung dazu
- Diesen Weg habe ich nicht ausprobiert.
- Mein Prüfwerkzeug bearbeitet jede Antwort nach: Es rechnet die Einstufung anhand einer Tabelle nach und entfernt Personennamen. Beides stand ursprünglich im Prompt, beides hielt das Modell nicht zuverlässig ein.
- ==In einem fremden Assistenten gibt es diesen Code nicht.== Was das praktisch bedeutet, muss der Pilot zeigen.

### Weg 2: Als eigenes Prüfwerkzeug
- Das Werkzeug, das ich gebaut habe. Entwurf einfügen — oder bei einem vorhandenen Kurs nur die Nummer, dann holt es den Text selbst.
- Die Schnittstelle des Kursportals ist öffentlich. Es braucht nur einen eigenen Server.

### Rechts im Bild: ein Befund
- Ein Befund aus einem echten Durchlauf, dem Deutschkurs auf A2.
- Jeder Befund hat dieselben vier Teile: Einstufung, Regel, wörtliche Stelle, Vorschlag.
- Dieser hier ist Pflicht: Der Link heißt schlicht „hier“. Wer sich die Seite vorlesen lässt und von Link zu Link springt, hört nur „hier“.
- Der Vorschlag daneben ist kein Kommentar, sondern fertiger Text zum Übernehmen.

### Hier die Vorführung
- Ich zeige euch das kurz live, an genau diesem Kurs.
- ((Ein Prototyp für diese Arbeit. Er belegt, dass der Weg funktioniert — eine fertige Anwendung ist er nicht.))

### Der Kasten unten
- Kein Teil des Pilotprojekts: Man könnte die Prüfung ins Redaktionssystem einbauen, dort, wo der Text entsteht.
- Nur wird das Portal von einem externen Dienstleister betreut. Also Auftrag, Budget, Vorlauf.
- ==Man kauft nichts, bevor man weiß, ob es wirkt.==


## 10 — Stakeholder

typ: matrix
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer eingebunden
akzent: werden muss.
klein: ja
lede: Der Pilot beschränkt sich auf einen der acht Programmbereiche. Nur so ist der Kreis klein genug, dass man ihn wirklich einbinden kann.
yhoch: Einfluss hoch
yniedrig: Einfluss niedrig
xniedrig: Betroffenheit niedrig
xhoch: Betroffenheit hoch
oben_links: Beobachten || Städtische IT || Advellence als Portaldienstleister || Betriebskommission als Aufsichtsgremium || Volkshochschul-Verband, stellt den KI-Zugang
oben_rechts: Eng einbinden || Direktor als Verantwortlicher der Inhalte || Der Fachbereich des Pilotbereichs || Redaktion des Programmhefts || Personalrat, Zustimmung erforderlich
unten_links: Informieren || Die drei übrigen Fachbereiche
unten_rechts: Konsultieren || Kursleitungen auf Honorarbasis || Teilnehmende, besonders in Deutschkursen und Grundbildung
quellen:
  - "§ 4 Abs. 4 Satz 2 HPVG — Honorarkräfte werden mitvertreten | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"

### NOTIZ

Damit zum Change-Teil, und der beginnt mit den **Stakeholdern**. Die
**Einfluss-Betroffenheits-Matrix** sortiert sie nach zwei Fragen: Wer ist
betroffen, und wer hat Einfluss.

### Oben rechts: Eng einbinden
- Wer entscheidet oder zustimmen muss.
- **Der Direktor** — laut Impressum persönlich für die redaktionellen Inhalte verantwortlich.
- **Der Fachbereich des Pilotbereichs** — entscheidet über den Text. Und zwar nur dieser eine: Vier gleichzeitig wären kein Pilot mehr.
- **Die Redaktion des Programmhefts** — prüft Texte für den Druck schon heute, weiß also, wie Textprüfung geht.
- **Der Personalrat** — hier ist die Einordnung zu schwach. Sein Einfluss ist kein hoher, sondern ein ==sperrender==: Die Einführung ist mitbestimmungspflichtig. ((Seine zwei von sechzehn Sitzen in der Betriebskommission sind daneben bedeutungslos.))

### Unten links: Informieren
- **Die drei übrigen Fachbereiche** — sollen wissen, dass es läuft, und sehen, was herauskommt. Im Pilot sind sie nicht dabei.

### Oben links: Beobachten
- Hoher Einfluss, aber ihre Arbeit verändert das Projekt nicht.
- **Die städtische IT** — bleibt für die technische Seite zuständig.
- **Advellence** — programmiert laut Impressum das Portal.
- **Die Betriebskommission** — Aufsichtsgremium.
- **Der Volkshochschul-Verband** — stellt den KI-Zugang.

### Unten rechts: Konsultieren
- Der Quadrant, der mich am meisten beschäftigt hat.
- **Die Kursleitungen auf Honorarbasis** — maximal betroffen, denn in der Branche schreiben sie viele dieser Texte. In keinem Gremium sitzen sie, und vorschreiben kann man ihnen nichts.
- Einen Kanal haben sie doch: Arbeitnehmerähnliche Personen gelten nach dem Personalvertretungsgesetz als Beschäftigte, der Personalrat vertritt sie mit.
- **Die Teilnehmenden** — besonders in Deutschkursen und Grundbildung. ==Für sie ist das Projekt gemacht, und sie haben keine Stimme — in keinem Gremium und in keinem Gesetz.==
- Bei ihnen ist Beteiligung kein guter Stil, sondern das einzige Instrument, das es überhaupt gibt.


## 11 — Widerstand

typ: einwaende
kapitel: 03 · CHANGE MANAGEMENT
titel: Vier Widerstände,
akzent: und vier Antworten.
klein: ja
einwaende:
  - "Unsicherheit · im ganzen Haus || „Schreibt die KI jetzt unsere Texte?“ || Nein. Sie schlägt vor, der Fachbereich entscheidet und veröffentlicht. Nichts geht ohne einen Menschen ins Portal."
  - "Verlustangst · Fachbereich || „Ich werde an Texten gemessen, die ich gar nicht ändern darf.“ || Stimmt. Vieles im Text sind Bausteine, die woanders gepflegt werden. Wer sie ändern darf, wird vor dem Pilot geklärt."
  - "Fehlende Perspektive · Kursleitung || „Noch eine Aufgabe — bezahlt werde ich nach Unterrichtsstunden.“ || Der Einwand ist berechtigt. Deshalb wird im Fachbereich geprüft, am eingegangenen Text. Rückmeldung gerne, Pflicht nein."
  - "Gewohnheit · Redaktion des Programmhefts || „Die Texte stehen seit Jahren so da, beschwert hat sich nie jemand.“ || Stimmt — und ihr prüft Texte als Einzige im Haus heute schon. Nur beschwert sich niemand, der eine Beschreibung nicht versteht. Er meldet sich gar nicht erst an."
callout: Drei dieser Einwände lassen sich beantworten. Der zweite braucht eine Entscheidung.
calloutsub: Wem die Textbausteine gehören, muss vor dem Pilot geklärt sein. Das ist keine Schulungsfrage.

### NOTIZ

Jetzt zum Widerstand. Der Unterricht nennt vier Ursachen: Unsicherheit,
Verlustangst, fehlende Perspektive und Gewohnheit. Für jede gibt es hier einen
Fall, den es wirklich gibt.

### Unsicherheit · im ganzen Haus
- Die Frage, die als Erstes kommt: Schreibt die KI jetzt unsere Texte?
- Nein. Sie schlägt vor, mehr nicht. Entschieden und veröffentlicht wird von Menschen.
- ==Das ist keine Beruhigung, sondern der Zuschnitt des Werkzeugs.==

### Verlustangst · Fachbereich
- Der einzige Einwand, der noch offen ist.
- Eine Kursbeschreibung ist selten von einer Hand: Anmeldehinweis, Beschreibung der Niveaustufe — solche Bausteine stehen wortgleich in vielen Kursen und werden nicht dort gepflegt, wo der Kurs angeboten wird.
- Wer die Befunde bekommt, darf den Text also oft gar nicht ändern.
- Keine Angst vor der Maschine, sondern die Aussicht, für etwas geradezustehen, das einem nicht gehört.
- Die Antwort ist deshalb keine Schulung, sondern eine Zuständigkeitsfrage — und die gehört vor den Pilot.

### Fehlende Perspektive · Kursleitung
- Bei den Honorarkräften schärfer als bei allen anderen: Ihre Abrechnungseinheit ist die Unterrichtsstunde, Textarbeit kommt darin nicht vor.
- Der Einwand ist berechtigt und gehört auch so beantwortet.
- Die Antwort ist der Zuschnitt: Geprüft wird im Fachbereich, an dem Text, der dort eingeht.
- ((Das schützt auch ihren Status: Verbindliche Regeln und ein Protokoll je Text wären genau die Merkmale, an denen sich eine Scheinselbständigkeit festmachen lässt.))

### Gewohnheit · Redaktion des Programmhefts
- Der Satz, der jedes Qualitätsprojekt begleitet: Es hat sich doch nie jemand beschwert. Und er stimmt vermutlich.
- Diese Redaktion prüft als Einzige im Haus heute schon Texte. Sie ist keine Bremse, sondern der nächstliegende Verbündete — und so sollte man ihr auch begegnen.
- Der Punkt ist nur: ==Wer sich beschwert, hat den Text gelesen und verstanden.==
- Die Menschen, um die es geht, fragen nicht nach und melden sich auch nicht an. Ihr Fehlen sieht von innen aus wie Zufriedenheit. ((Dass es bisher niemand gesehen hat, ist deshalb kein Versäumnis, sondern liegt in der Sache.))

### Der Kasten unten
- Betroffene zu Beteiligten machen heißt hier: entscheiden, bevor geschult wird.


## 12 — Timeline

typ: timeline
kapitel: 03 · CHANGE MANAGEMENT
titel: Der Plan
akzent: für die nächsten drei Monate.
klein: ja
monate: Monat 1 | Monat 2 | Monat 3
strang1: Technische Implementation || Setup > Assistent anlegen, Regeln an echten Texten schärfen || Pilot > Ein Programmbereich, nur neu entstehende Texte || Rollout > Vorbereitet, freigegeben erst nach der Nachmessung
strang2: Kommunikation || Ankündigung > Erst die Dienstvereinbarung, dann die Bekanntgabe || Training > Pflicht nach Artikel 4 KI-Verordnung, für alle, die bedienen || Support > Feste Sprechstunde, nicht auf Zuruf
strang3: Change || Vorbereitung > Betroffene befragen, Bausteinfreigabe klären || Einbindung > Der Bereich wählt die scharfen Regeln, dazu der Quick Win || Begleitung > Nachmessung, dann Entscheidung
callout: Im Change-Strang steht das Fragen vor dem Handeln — die Bausteinfreigabe im ersten Monat, nicht im zweiten.
calloutsub: Sonst trifft der Quick Win im zweiten Monat auf eine Zuständigkeit, die niemand geklärt hat.
quellen:
  - "§ 78 Abs. 1 Nr. 5 und § 66 HPVG, Fassung 2023 | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"
  - "KI-Verordnung (EU) 2024/1689, Artikel 4 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Der Zeitplan: drei Monate, drei Stränge, die neun Phasen aus der
Aufgabenstellung als Überschrift jeder Zelle. Die Zellen könnt ihr mitlesen,
ich hebe zwei Dinge heraus.

### Monat 2, Kommunikation: Training
- Keine Kür, sondern Pflicht: **Artikel 4 der KI-Verordnung** verlangt seit Februar 2025 ausreichende KI-Kompetenz.
- Und zwar für das Personal und für alle, die im Auftrag mit Betrieb und Nutzung befasst sind.
- Deshalb steht in der Zelle nicht „Personal“, sondern „alle, die bedienen“. ((Wer nicht bedient, braucht die Schulung nicht — deshalb bleiben die Kursleitungen aus dieser Kette.))

### Strang Change: erst fragen, dann handeln
- Die Freigabe der Textbausteine steht im ersten Monat, nicht im zweiten.
- ==Sonst läuft der Quick Win auf eine Zuständigkeit, die niemand hat.==


## 13 — Die ersten 30 Tage

typ: plan
kapitel: 03 · ZEITPLAN UND NÄCHSTE SCHRITTE
titel: Die ersten
akzent: 30 Tage.
klein: ja
schrittetitel: ERSTE 30 TAGE · JEDER SCHRITT BEDINGT DEN NÄCHSTEN
schritte:
  - "Dienstvereinbarung mit dem Personalrat schließen > Vorher darf nichts angelegt werden."
  - "Einen Programmbereich freiwillig als Pilotbereich gewinnen > Ein zugewiesener liefert Erfüllung, kein Ergebnis."
  - "Die Freigabe der Textbausteine klären > Sonst trifft der Quick Win auf niemanden."
  - "Assistent im KI-Zugang des Verbands anlegen > Keine Beschaffung, keine zusätzliche Stelle."
callout: Wer den dritten Schritt auslässt, misst im Pilot Befunde, die niemand ändern darf.

### NOTIZ

Die ersten dreißig Tage. Keine Aufzählung, sondern eine Reihenfolge:
==Jeder Schritt bedingt den nächsten.==

### Die vier Schritte
- Die **Dienstvereinbarung** zuerst, aus dem Grund von eben.
- Dann einen **Programmbereich** gewinnen, und zwar freiwillig — ein zugewiesener liefert kein belastbares Ergebnis, sondern nur Erfüllung.
- Dann die **Freigabe der Bausteine**.
- Und erst als viertes das Technische, den **Assistenten anlegen**. Das kostet nichts: kein Einkauf, keine neue Stelle, der KI-Zugang ist da.

### Der Kasten unten: der dritte Schritt
- Der, den man am ehesten überspringt, und der teuerste.
- Lässt man ihn aus, liefert der Pilot eine Liste von Befunden, die im Pilotbereich niemand ändern darf.
- Das Werkzeug hat sich dann beim ersten Durchlauf selbst erledigt.


## 14 — Erfolgsmessung und Risiken

typ: tabelle
kapitel: 03 · ERFOLGSMESSUNG
titel: 57 Prozent heute,
akzent: unter 25 nach dem Pilot.
klein: ja
kompakt: ja
spalten: Kennzahl | heute | Ziel nach 3 Monaten | gemessen mit
zeilen:
  - "Texte mit mindestens einem Befund | 57 % | ! unter 25 % | eigenes Messskript, unverändert"
  - "Neue Texte im Pilotbereich geprüft | 0 | + alle | Protokoll des Werkzeugs"
  - "Texte für Deutschkurse A1/A2 mit Wörtern über Niveau | 31 von 31 | ! höchstens 10 von 31 | eigenes Messskript, unverändert"
  - "Teilnehmende, die die Beschreibung verstanden haben | nicht erhoben | + Ausgangswert und Trend | Kurzbefragung am Kursende, freiwillig und vergütet"
risiken:
  - "Manche Ziele lassen sich erfüllen, ohne dass ein Text besser wird. Ein kürzerer Satz ist nicht automatisch ein verständlicherer. > Deshalb fragt die vierte Kennzahl nicht den Text, sondern die Teilnehmenden."
quellen: Eigene Auswertung aller 3.111 Kurstexte des Portals, 30.07.2026

### NOTIZ

Und woran würde man merken, ob es gewirkt hat?

### Die ersten drei Kennzahlen
- Vier Kennzahlen, jede mit Ausgangswert und Ziel.
- Die Befundquote soll von 57 Prozent unter 25 fallen.
- Alle neuen Texte im Pilotbereich sollen geprüft sein.
- Von den 31 Texten für Deutschkurse auf A1 und A2, die heute alle Wörter über dem Niveau ihrer Leser enthalten, sollen höchstens noch zehn betroffen sein.

### Die vierte Kennzahl: die Befragung
- Die ersten drei messen nur den Text, nicht die Wirkung. Deshalb frage ich die Teilnehmenden selbst.
- Nicht über einen Fragebogen auf der Website — den füllt genau die Zielgruppe nicht aus, um die es geht.
- Sondern im Kurs, am Ende einer Stunde, in einfacher Sprache.
- ==Freiwillig und vergütet.== ((Sonst wäre sie eine neue Aufgabe ohne Bezahlung — bei Honorarkräften genau das Problem von der Widerstandsfolie.))

### Letzte Spalte: womit gemessen wird
- Die Nachmessung läuft mit demselben Skript wie die Ausgangsmessung. Dafür bleibt es unverändert liegen.
- Sonst wüsste man hinterher nicht, ob die Texte besser geworden sind oder nur die Messung anders.

### Das Risiko unten
- Die ersten drei Kennzahlen lassen sich erfüllen, ohne dass ein einziger Text besser wird: Wer lange Sätze teilt und schwere Wörter austauscht, drückt die Quote.
- ==Ein kürzerer Satz ist nicht automatisch ein verständlicherer.==
- Genau dagegen steht die vierte. Sie fragt nicht den Text, sondern die Menschen, für die er geschrieben ist.
- Ohne sie misst der Pilot am Ende nur seinen eigenen Maßstab.


## 15 — Schlussfolie

typ: schluss
bild: bilder/15-durchgang.png
bildnotiz: Dieselbe Wand wie auf der Titelfolie, der Durchgang jetzt begehbar und hell.
titel: Danke für die Aufmerksamkeit.
link: klartext-vhs.henrikheil.net
linktext: Zum Testen an einem echten Kurstext aus dem Portal:
fussl: PROJEKT KLARTEXT · VHS FRANKFURT
fussr: HENRIK HEIL

### NOTIZ

- Danke für die Aufmerksamkeit.

- Zum Test an einem Kurstext aus dem Portal habe ich die URL zum Prototypen verlinkt — mit dem Prompt in allen Fassungen.

- Wenn es Fragen gibt gerne.
