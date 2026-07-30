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
bild: bilder/01-titel-wand.png
bildnotiz: Wand aus Textzeilen mit einem Schlitz. Gezeichnet von bilder/zeichnen.py, Gegenstueck auf der Schlussfolie.

### NOTIZ

Ich stelle euch heute mein Abschlussprojekt vor: KLARTEXT, ein Prüfschritt für
die Kursbeschreibungen der Volkshochschule Frankfurt.

Das Feld heißt Barrierefreiheit. Die meisten denken dabei an Technik:
Kontraste, Tastaturbedienung, Vorleseprogramme. Mein Thema ist der andere
Teil. Ob der Text ankommt bei denen, für die er geschrieben ist. Das betrifft
alle acht Programmbereiche des Unternehmens.

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
lede: Die Kursbeschreibungen entstehen in acht Programmbereichen und erscheinen unverändert im Portal, im Programmheft und im Newsletter. Einfache Sprache bietet das Unternehmen an — für Betrieb und Kursgeschäft, nicht für die Kurstexte selbst.
zahlen:
  - "5.800 || Kursbeschreibungen im Jahr"
  - "58 % || haben mindestens einen Befund || warn"
  - "5 Jahre || seit dem letzten externen Barrierefreiheitstest || warn"
callout: Mehr als jeder zweite Text hat einen Befund. Die Frage ist, für wen er zu schwer ist.
quellen:
  - "Eigene Auswertung von 60 Kursbeschreibungen, 29.07.2026"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"
  - "Erklärung zur Barrierefreiheit der vhs, 23.09.2025 | https://vhs.frankfurt.de/de/special-pages/support/barrierefreiheit"

### NOTIZ

Zuerst das Ganze in drei Zahlen.

Die Volkshochschule veröffentlicht rund fünftausendachthundert
Kursbeschreibungen im Jahr. In meiner Stichprobe von sechzig Kursen haben
achtundfünfzig Prozent mindestens einen Befund. Und das ist die Untergrenze.
Die Zahl stammt von einem Skript, das ohne KI auskommt und deshalb eine der
sechs Regeln nicht prüfen kann. Mit dem Prüfassistenten liegt der Wert höher.

Die dritte Zahl stammt aus dem Unternehmen selbst. In der Erklärung zur
Barrierefreiheit steht, wann die Website zuletzt extern geprüft wurde: am
ersten Juli zweitausendeinundzwanzig. Das ist heute auf den Tag genau fünf
Jahre her. Seitdem bewertet sich das Unternehmen selbst. Ich habe die Seite mit einem
gängigen Prüfprogramm laufen lassen, und sie erfüllt die Anforderungen heute
nicht mehr, da kommen etliche Verstöße zusammen.

Das ist aber ausdrücklich nicht mein Thema. Dafür ist die städtische IT
zuständig, und ich komme darauf noch einmal zurück.

Denn dieselbe Erklärung enthält den Satz, der mich auf dieses Projekt gebracht
hat. Die wichtigsten Informationen zu Betrieb und Kursgeschäft, heißt es dort,
seien in einfacher Sprache verfügbar. Das Unternehmen hat die Frage nach der
Verständlichkeit also längst gestellt und für einen Bereich beantwortet. Nur
für die Kursbeschreibungen selbst, den mit Abstand größten Textbestand, gilt
das nicht.

Genau da setze ich an. Und unten steht die Frage, um die es dabei geht: Neun
von zehn Texten haben einen Befund. Für wen sind sie eigentlich zu schwer?


## 3 — Executive Summary II: Der Vorschlag

typ: punkte
kapitel: ÜBERBLICK
bild: bilder/03-prozess-voll.png
bildnotiz: Die Kette der Arbeitsschritte mit besetzter Stelle. Was neu ist, steht in der Akzentfarbe. Gegenstueck auf Folie 4.
titel: Der Vorschlag,
akzent: und was er bringt.
punkte:
  - "**Ziel** || Wer einen Kurs sucht, versteht die Beschreibung, ob gelesen oder vorgelesen. Laut Betriebssatzung stehen die Angebote allen offen — das soll auch für die Texte gelten."
  - "**Lösung** || Ein Prüfschritt vor der Veröffentlichung, als System-Prompt im vorhandenen KI-Rahmen des Volkshochschul-Verbands. Keine Beschaffung, kein neuer Vertrag."
  - "**Abgrenzung** || Die technische Barrierefreiheit der Website bleibt beim deterministischen Prüfwerkzeug und bei der städtischen IT. Die KI sieht nur den Kurstext."
  - "**Ergebnis** || Befundquote nach drei Monaten unter 25 Prozent statt heute 58. Aufwand im Regelbetrieb 29 Stunden im Jahr."
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


## 4 — Das Unternehmen und der Prozess heute

typ: zweispalt
kapitel: 01 · UNTERNEHMEN UND IST-ANALYSE
bild: bilder/04-prozess-luecke.png
bildnotiz: Vier Arbeitsschritte, dazwischen eine leere Stelle ohne Verbindung nach oben und unten.
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

Wichtig ist der erste Punkt, ganz am Ende. Das Unternehmen ist seit zweitausendfünf
nach L Q W testiert. Das steht für Lernerorientierte Qualitätstestierung in
der Weiterbildung, ein Verfahren mit regelmäßiger externer Prüfung, inzwischen
in der sechsten Runde. Dazu kommt eine Zertifizierung nach der Akkreditierungs-
und Zulassungsverordnung Arbeitsförderung. Das ist mir wichtig zu betonen: Hier
fehlt keine Qualitätskultur. Es fehlt genau ein Schritt darin.

Der Satz oben stammt wörtlich aus der Betriebssatzung. Die Angebote stehen
grundsätzlich allen offen, ohne Rücksicht auf Vorbildung. Daran messe ich das
Unternehmen. Nicht am Gesetz, sondern an seinem eigenen Anspruch.

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

typ: tabelle2
kapitel: 01 · POTENZIALERMITTLUNG
titel: Was zählt als Befund,
akzent: und für wen.
klein: ja
lede: 60 Kursbeschreibungen, sieben Programmbereiche, Portalabruf vom 28.07.2026. 35 davon haben einen Befund.
regelntitel: Wonach gemessen wurde
regeln:
  - "PFLICHT · verbindlich nach WCAG | STRUKTUR | Überschrift oder Liste ohne semantisches HTML"
  - "| LINKTEXT | Linktext nennt sein Ziel nicht"
  - "EMPFEHLUNG | NIVEAU | Wort über dem Sprachniveau der Zielgruppe"
  - "| AMTSDEUTSCH | Behördenwort, wo ein Alltagswort reicht"
  - "| SATZ | über 25 Wörter, bei Deutschkursen über 15"
  - "| ABK | Kürzel ohne Auflösung, etwa DTZ"
tabellentitel: Zwei Kurse im Vergleich
spalten: Kurs | Wer die Beschreibung liest | Wörter über Niveau | Befunde
zeilen:
  - "Englisch A1.1 | + liest Deutsch fließend | 0 | 1"
  - "Deutsch als Fremdsprache A2.2 | ! lernt Deutsch, kann bisher A1 | 24 | 28"
callout: Beide Kurse tragen A im Titel. Nur bei einem ist der Text zu schwer für seine Leser.
calloutsub: Ob ein Text verständlich ist, entscheidet nicht der Text — sondern die Zielgruppe, die ihn lesen soll.
quellen:
  - "Eigene Auswertung von 60 Kursbeschreibungen, 29.07.2026 — Auswertung und Daten liegen der Arbeit bei"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"

### NOTIZ

Damit zur Potenzialermittlung. Hier habe ich nicht geschätzt, sondern
gemessen.

Das Kursportal hat eine offene Schnittstelle. Darüber habe ich sechzig
Kursbeschreibungen aus sieben der acht Programmbereiche gezogen und mit einem
eigenen Skript ausgewertet. Fünfunddreißig von sechzig Texten haben mindestens
einen Befund.

Oben steht, wonach ich gemessen habe. Sechs Regeln, und die Reihenfolge auf
dieser Folie ist Absicht: erst der Maßstab, dann das Ergebnis. Dieselben sechs
Regeln sind zugleich der Maßstab des Prüfassistenten, den ich gleich zeige.

Links stehen die beiden Pflichtregeln. Sie stehen auf Stufe A der
Barrierefreiheitsrichtlinien und sind damit verbindlich.

Struktur heißt: Eine Zeile sieht aus wie eine Überschrift, ist im Quelltext
aber gewöhnlicher Fließtext. Dasselbe gilt für Aufzählungen, die jemand nur
mit Bindestrichen gebaut hat. Wer sehend liest, merkt davon nichts. Ein
Screenreader dagegen bietet seinen Nutzern an, sich alle Überschriften einer
Seite vorlesen zu lassen, um gezielt dorthin zu springen. Was technisch keine
Überschrift ist, taucht in dieser Liste nicht auf. Die Gliederung ist dann
sichtbar vorhanden und für das Vorleseprogramm nicht da.

Linktext heißt: Der Link sagt nicht, wohin er führt. Das bekannteste Beispiel
ist ein Link, der schlicht „hier“ heißt. Der Grund ist derselbe wie eben:
Screenreader lesen auf Wunsch nur die Links einer Seite vor, ohne den Text
drumherum. Eine Liste aus fünfmal „hier“ hilft niemandem weiter.

Rechts stehen die vier Empfehlungen. Verbindlich sind sie nicht, aber sie sind
der eigentliche Ertrag dieses Projekts. Zwei davon, zu schwere Wörter und nicht
aufgelöste Abkürzungen, stehen auf Stufe AAA der Richtlinien — der höchsten,
die niemand einhalten muss. Die beiden anderen habe ich selbst gesetzt.

Niveau heißt: Ein Wort liegt über dem Sprachniveau derer, die den Text lesen
sollen. Das ist die Regel, die sich ohne Kenntnis der Zielgruppe überhaupt
nicht anwenden lässt.

Amtsdeutsch heißt: Im Text steht ein Verwaltungswort, obwohl ein alltägliches
genügen würde. Umbuchung statt Wechsel, gegebenenfalls statt wenn nötig. Das
trifft nicht nur Sprachanfänger, sondern auch geübte Leserinnen und Leser.

Satz heißt: über fünfundzwanzig Wörter, bei Deutschkursen über fünfzehn. Diese
beiden Zahlen habe ich gesetzt, nicht gemessen. Sie orientieren sich an den
Empfehlungen für einfache Sprache. Zur Satzlänge sagen die
Barrierefreiheitsrichtlinien nämlich nichts, und ob es die richtigen Zahlen
sind, gehört zu den Fragen, die der Pilot beantworten soll.

Abkürzung heißt: Ein Kürzel steht im Text, ohne beim ersten Mal aufgelöst zu
werden. Davon hat die vhs einige eigene. D-T-Z zum Beispiel, der
Deutsch-Test für Zuwanderer.

Damit zur Tabelle darunter. Sie zeigt zwei Sprachkurse, und beide tragen eine
niedrige Stufe im Titel. Das bedeutet aber zweimal etwas völlig Verschiedenes.

Beim Englischkurs steht A1 für das Englisch, das dort gelernt wird. Wer die
Beschreibung liest, ist deutschsprachig und liest Deutsch fließend. Beim
Deutschkurs steht A2 für das Deutsch, das dort gelernt wird. Wer diese
Beschreibung liest, kann Deutsch bisher eine Stufe darunter, also A1.

Und jetzt der Unterschied. Der Englischkurs hat kein einziges Wort über dem
Niveau seiner Leser, einen Befund insgesamt, und das ist eine nicht
aufgelöste Abkürzung. Der Deutschkurs hat vierundzwanzig zu schwere Wörter und
achtundzwanzig Befunde.

Dabei sind beide Texte gleich einfach gebaut. Die Sätze sind in beiden Fällen
kurz, im Schnitt neun beziehungsweise elf Wörter. Ein Lesbarkeitsindex, der
Satz- und Wortlängen zählt, findet bei keinem der beiden etwas. Er schweigt
zweimal, und einmal davon zu Unrecht.

Deshalb reicht kein Werkzeug, das nur den Text ansieht. Man muss wissen, für
wen der Text ist. In meiner Stichprobe stehen sechs Deutschkurse auf den
Stufen A1 und A2. Alle sechs enthalten Wörter, die über dem Niveau ihrer
Zielgruppe liegen. Selbsteinschätzung, Fehleinschätzung, Umbuchung. Das sind
Wörter, die man erst weit oberhalb des Kursziels lernt. Genau hier kann ein
fachlich eingestellter Prompt etwas, was ein Standardwerkzeug nicht kann.

Ein Wort zu den Zahlen, das mir wichtig ist. Achtundfünfzig Prozent sind eine
Untergrenze. Mein Messskript prüft fünf der sechs Regeln. Die erste, ob eine
hervorgehobene Zeile eine Überschrift sein sollte, kann kein Skript
entscheiden. Ich messe also bewusst zu niedrig statt zu hoch.


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

Und jetzt der Block in der Mitte, der Punkt, an dem ich beim Recherchieren
selbst falsch lag. Er zeigt nur die Kriterien, die am Text der
Kursbeschreibung selbst hängen. Die Seite hat weitere Pflichten — Kontraste,
Seitentitel, Tastaturbedienung. Die gehören einem anderen Werkzeug, dazu
komme ich auf der nächsten Folie.

Links steht, was am Text verbindlich ist: dass eine Zeile, die eine
Gliederungsebene eröffnet, auch technisch als Überschrift ausgezeichnet wird.
Und dass ein Linktext sagt, wohin er führt. Beides sind die Pflichtregeln von
eben.

Rechts steht, was freiwillig ist. Dass Abkürzungen erklärt werden. Und dass
das Leseniveau zur Zielgruppe passt. Beides ist dreifach A und damit nicht
gefordert. Genau die beiden Kriterien also, um die es in diesem Projekt geht.

Ich könnte jetzt mit einem drohenden Bußgeld argumentieren. Das wäre bequem,
und es wäre falsch.

Freiwillig heißt aber nicht belanglos, und das ist der Kern dieser Folie.
Paragraph drei Absatz eins der hessischen Verordnung verlangt eigenständig,
dass Angebote verständlich sind. Die Konformitätsstufe begründet eine
Vermutung, keine Obergrenze der Pflicht. Ich argumentiere also nicht gegen das
Recht, sondern in einer Lücke, die es selbst offenlässt.

Und den eigentlichen Auftrag gibt sich das Unternehmen selbst. Die
Betriebssatzung sagt, die Angebote stünden allen offen, ohne Rücksicht auf
Vorbildung. Für ein solches Unternehmen ist es nicht vertretbar, dass ausgerechnet
die Kriterien für Menschen mit geringer Vorbildung die freiwilligen sind.


## 7 — Die Arbeitsteilung

typ: zweispalt
kapitel: 02 · LÖSUNG
titel: Was die Technik prüft,
akzent: und was nur ein Mensch sieht.
klein: ja
spalte1: DAS SEITENGERÜST · städtische IT
punkte1:
  - "Kontraste, Tastaturbedienung, Seitentitel, Navigation"
  - "Prüfbar, ohne den einzelnen Kurs zu kennen"
  - "Etablierte Programme wie axe-core, kostenlos, bei jeder Änderung"
  - "Gilt für alle 5.800 Texte gleich"
spalte2: DER EINZELNE TEXT · Programmbereiche
punkte2:
  - "Versteht die Zielgruppe genau dieses Kurses ihn?"
  - "Auch Überschriften, die keine sind, und Linktexte ohne Aussage"
  - "Nicht prüfbar, ohne zu wissen, wer liest"
  - "Vorschlag der KI, Entscheidung beim Fachbereich"
callout: Ob ein Text zu seinen Lesern passt, steht in keinem Regelwerk.
calloutfolge: Die Technik bleibt bei der städtischen IT. Neu ist allein der Schritt, der die Zielgruppe kennen muss.
calloutsub: Technische Voraussetzungen: der vorhandene KI-Rahmen des Volkshochschul-Verbands, ein hinterlegter Assistent, die Wortliste als Datei. Keine Beschaffung, kein Eingriff ins Kursverwaltungssystem.
quellen:
  - "WCAG 2.1 | https://www.w3.org/TR/WCAG21/"
  - "Deque axe-core | https://github.com/dequelabs/axe-core"

### NOTIZ

Damit zur Lösung. Sie beginnt mit einer Abgrenzung, die ich für den
wichtigsten Teil meines Konzepts halte.

Auf der vorigen Folie habe ich nur die Kriterien gezeigt, die am Text der
Kursbeschreibung hängen. Die Seite hat weitere Pflichten, und die Frage ist,
warum dafür nicht dasselbe Werkzeug reicht.

Links steht, was am Gerüst der Seite hängt: Kontraste, Tastaturbedienung,
Seitentitel, Navigation. Das kann man prüfen, ohne einen einzigen Kurs zu
kennen. Es gilt für alle fünftausendachthundert Texte gleich, dafür gibt es
etablierte Programme wie axe-core, und zuständig ist die städtische IT.

Rechts steht, was am einzelnen Text hängt. Versteht die Zielgruppe genau
dieses Kurses ihn? Diese Frage lässt sich nicht beantworten, ohne zu wissen,
wer liest. Zuständig sind die Programmbereiche.

Und jetzt der Punkt, auf den es mir ankommt. Die Trennlinie verläuft nicht
zwischen Sprache und Technik. Zwei meiner sechs Regeln sind selbst
Pflichtkriterien der Barrierefreiheit. Ein Beispiel: eine hervorgehobene
Zeile, die als Überschrift gemeint ist, aber im Quelltext keine ist. Das
Prüfprogramm sieht dort nur Fließtext und meldet nichts. Ob diese Zeile eine
Überschrift sein sollte, kann man dem Text nicht ansehen, sondern nur
verstehen. Deshalb liegt ausgerechnet dieses Pflichtkriterium rechts.

Ein Wort dazu, warum links kein Sprachmodell steht. Nicht, weil dort keine KI
im Spiel wäre — die Hersteller solcher Prüfprogramme bauen selbst KI ein, um
schneller zu werden. Sondern weil dort keine nötig ist. Für alles, was
feststeht, ist ein Sprachmodell das schlechtere Werkzeug: langsamer, teurer,
und es liefert nicht immer dasselbe Ergebnis. Ein Kontrastwert ist eine
Rechnung, keine Einschätzung.

Diese Trennung hat sich beim Bauen zweimal selbst bestätigt. Zwei Zusagen, die
ich zuerst in den Prompt geschrieben hatte, hat das Modell nicht zuverlässig
eingehalten. Beide stehen jetzt im Programmcode, weil sie feststehen und keine
Einschätzung verlangen.

Zu den technischen Voraussetzungen: Es braucht den KI-Rahmen, den der
Volkshochschul-Verband ohnehin bereitstellt, einen dort hinterlegten
Assistenten und die Wortliste als Datei. Kein neuer Vertrag, kein Eingriff ins
Kursverwaltungssystem.


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
calloutfolge: „Bewertet Texte, niemals Personen.“ Anhang III setzt überall die Bewertung natürlicher Personen voraus. Derselbe Satz beantwortet die Frage des Personalrats nach Leistungskontrolle.
quellen:
  - "system-prompt.md, Fassung v11 vom 29.07.2026, zwölf Fassungen in der Versionsverwaltung"
  - "KI-Verordnung (EU) 2024/1689, Anhang III | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Damit zum Kern der Aufgabe, dem System-Prompt. Er folgt der
Sechs-Komponenten-Struktur aus dem Aufgabenblatt.

Die ROLLE macht ihn zur Redaktionsassistenz, nicht zur Autorin. Die AUFGABE
schreibt die Reihenfolge vor: erst die Zielgruppe bestimmen, dann prüfen. Das
FORMAT erzwingt zu jedem Befund ein wörtliches Zitat, eine Begründung und
einen konkreten Vorschlag. Ohne Vorschlag kein Befund.

Der KONTEXT enthält das Hauswissen: die acht Programmbereiche, die
internen Abkürzungen, sechs Prüfregeln und, das ist der wichtigste Teil,
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

Und jetzt zur Zeile GRENZEN. Dort steht: bewertet Texte, niemals Personen.
Dieser eine Satz leistet zweierlei. Er hält das Projekt aus dem
Hochrisikobereich der KI-Verordnung heraus, denn Anhang III setzt überall eine
Bewertung natürlicher Personen voraus. Und er ist die Antwort auf die Frage
des Personalrats, ob hier Leistung kontrolliert wird.


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

Bleibt die Frage, wie das praktisch in den Alltag kommt. Dafür gibt es zwei
Wege, und beide stehen vom ersten Tag an offen.

Der erste braucht keine eigene Technik. Der Deutsche Volkshochschul-Verband hat
im Mai zweitausendfünfundzwanzig eine Rahmenvereinbarung mit einem Anbieter
namens fobizz geschlossen. Mitarbeitende aller Volkshochschulen in Deutschland
haben darüber datenschutzkonformen Zugang zu KI-Anwendungen, und man kann dort
eigene Assistenten mit eigenen Anweisungen anlegen. Genau das ist mein Prompt.
Es braucht dafür keine Zustimmung außerhalb des Pilotbereichs, weil der
Rahmenvertrag schon da ist. Zu klären ist allerdings, ob die vhs Frankfurt die
Lizenz auch tatsächlich gebucht hat — der Rahmenvertrag schafft die
Möglichkeit, er ist nicht die Buchung.

Zwei Einschränkungen gehören dazu, und ich nenne sie lieber selbst, weil ich
sie nicht ausprobiert habe.

Die erste: Mein Prompt ist mit der Wortliste rund einundzwanzigtausend Zeichen
lang. Ob der Anbieter Anweisungen dieser Länge annimmt, veröffentlicht er
nicht. Es ist gut möglich, dass der Prompt für diese Umgebung angepasst werden
muss. Das gehört zu den ersten Aufgaben im Pilotprojekt.

Die zweite, und die ist wichtiger: Mein Prüfwerkzeug bearbeitet jede Antwort
nach. Es rechnet die Einstufung anhand einer Tabelle nach und entfernt
Personennamen. Beides stand ursprünglich im Prompt, und beides hielt das Modell
nicht zuverlässig ein — deshalb steht es heute im Programmcode. In einem
fremden Assistenten gibt es diesen Code nicht. Was das praktisch bedeutet, muss
der Pilot zeigen. Ich behaupte hier nicht, der eine Weg sei besser als der
andere, sondern nur: Sie sind nicht identisch.

Der zweite Weg ist das Prüfwerkzeug, das ich gebaut habe. Dort fügt man den
Entwurf ein — oder gibt bei einem vorhandenen Kurs nur die Nummer ein, dann
holt es den Text selbst. Die Schnittstelle des Kursportals ist öffentlich, das
kostet keinen Zugang. Es braucht nur einen eigenen Server.

Ein Hinweis dazu, warum das Einfügen der wichtigere Fall ist: Über die
Schnittstelle kommen nur Kurse, die schon veröffentlicht sind. Der Prüfschritt
soll aber vorher greifen. Der Kursnummer-Abruf ist deshalb vor allem dafür da,
den vorhandenen Bestand nachzuprüfen — fünftausendachthundert Texte, die
niemand einzeln durchgehen kann.

Rechts sehen Sie, was dabei herauskommt. Ein Befund aus einem echten Durchlauf,
dem Deutschkurs auf A2. Jeder Befund hat dieselben vier Teile: die Einstufung,
die Regel, die wörtliche Stelle aus dem Text und einen konkreten Vorschlag.
Dieser hier ist Pflicht: Der Link heißt schlicht „hier“. Wer sich die Seite
vorlesen lässt und von Link zu Link springt, hört nur „hier“. Der Vorschlag
daneben ist kein Kommentar, sondern fertiger Text zum Übernehmen.

Zur Einordnung: Das ist ein Prototyp, den ich für diese Arbeit gebaut habe. Er
belegt, dass der Weg funktioniert, er ist keine fertige Anwendung.

Die Nachbemerkung unten ist bewusst kein Teil des Pilotprojekts. Man könnte die
Prüfung ins Redaktionssystem selbst einbauen, dort, wo der Text entsteht. Das
wäre für die Beteiligten am bequemsten. Nur wird das Portal von einem externen
Dienstleister betreut, also hieße das: Auftrag, Budget, Vorlauf. Diese
Entscheidung gehört ans Ende des Pilotprojekts, nicht an den Anfang. Man kauft
nichts, bevor man weiß, ob es wirkt.


## 10 — Stakeholder

typ: matrix
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer eingebunden
akzent: werden muss.
klein: ja
lede: Der Pilot beschränkt sich auf einen der acht Programmbereiche. Nur so bleibt der Kreis der eng Eingebundenen klein genug, um ihn wirklich einzubinden.
yhoch: Einfluss hoch
yniedrig: Einfluss niedrig
xniedrig: Betroffenheit niedrig
xhoch: Betroffenheit hoch
oben_links: Beobachten || Städtische IT || Advellence als Portaldienstleister || Betriebskommission als Aufsichtsgremium
oben_rechts: Eng einbinden || Direktor als Verantwortlicher der Inhalte || Der Fachbereich des Pilotbereichs || Redaktion des Programmhefts || Personalrat, Zustimmung erforderlich
unten_links: Informieren || Die sieben übrigen Programmbereiche || Volkshochschul-Verband, stellt den KI-Rahmen
unten_rechts: Konsultieren || Kursleitungen auf Honorarbasis || Teilnehmende, besonders in Deutschkursen und Grundbildung

### NOTIZ

Damit komme ich zum Change-Teil. Er beginnt mit der Frage, wer eigentlich
betroffen ist. Die beiden Achsen sind Einfluss und Betroffenheit, und die Pfeile
zeigen jeweils dorthin, wo sie zunehmen.

Oben rechts stehen die vier, die eng eingebunden werden müssen. Der Direktor,
der laut Impressum persönlich für die redaktionellen Inhalte verantwortlich
ist. Der Fachbereich, zu dem der Pilotbereich gehört — und zwar nur dieser
eine, denn acht Programmbereiche gleichzeitig einzubinden wäre kein Pilot mehr.
Die Redaktion des Programmhefts, die es für den Druck bereits gibt und die
deshalb schon weiß, wie Textprüfung geht. Und der Personalrat, und bei dem ist
die Einordnung eigentlich zu schwach. Sein Einfluss ist kein hoher, sondern ein
sperrender: Die Einführung des Werkzeugs ist mitbestimmungspflichtig, sie
braucht seine Zustimmung. Zwei von sechzehn Sitzen in der Betriebskommission
sind dagegen als Stimmblock bedeutungslos. Was das genau heißt, steht auf der
nächsten Folie.

Deshalb stehen die sieben übrigen Programmbereiche unten links, bei
informieren. Sie sollen wissen, dass es läuft, und sie sollen sehen, was
herauskommt. Aber sie sind im Pilot nicht dabei.

Oben links stehen drei mit hohem Einfluss, aber geringer Betroffenheit, weil
mein Projekt ihre Arbeit nicht verändert. Die städtische IT, die für die
technische Seite zuständig bleibt. Advellence, die Schweizer Firma, die laut
Impressum das Portal programmiert — sie wird erst wichtig, wenn die Prüfung
später ins Redaktionssystem soll. Und die Betriebskommission, das
Aufsichtsgremium eines städtischen Eigenbetriebs.

Daneben steht dort der Deutsche Volkshochschul-Verband. Er stellt den
KI-Rahmen bereit, den ich nutze, ist von dem Projekt aber nicht betroffen.

Ein Wort dazu, was in dieser Matrix nicht steht. Ich hatte zuerst mehr
eingetragen, unter anderem die Kämmerei und die hessische Durchsetzungsstelle.
Beide habe ich gestrichen. Es fließt kein Geld, also ist die Kämmerei nicht
beteiligt. Und mit einer Aufsichtsbehörde zu drohen wäre unredlich, wenn die
Kriterien, um die es geht, ausdrücklich freiwillig sind.

Und unten rechts der Quadrant, der mich am meisten beschäftigt hat. Die
Kursleitungen auf Honorarbasis sind maximal betroffen, denn in der Branche
schreiben sie viele dieser Texte. In keinem Gremium sitzen sie, und
vorschreiben kann man ihnen als Honorarkräften nichts. Einen Kanal haben sie
aber doch, und den hatte ich zuerst übersehen: Arbeitnehmerähnliche Personen
gelten nach dem Personalvertretungsgesetz als Beschäftigte, der Personalrat
vertritt sie also mit. Ob sie hier überhaupt Texte schreiben, kann ich nicht
belegen: Für die Branche ist die Zulieferung durch Kursleitungen gut
dokumentiert, für dieses Unternehmen nicht. Meine beiden Beispielkurse sprechen
sogar dagegen, sie sind mit N. N. als Kursleitung gedruckt und bestehen
vollständig aus Textbausteinen.

Darunter stehen die Teilnehmenden selbst, besonders in den Deutschkursen und in
der Grundbildung. Sie sind diejenigen, für die das ganze Projekt gemacht ist,
und sie haben in keinem Gremium eine Stimme.

Für diesen ganzen unteren rechten Quadranten gilt dasselbe: hoch betroffen,
kein formaler Einfluss. Beteiligung ist dort kein guter Stil, sondern das
einzige Instrument, das überhaupt zur Verfügung steht. Was das praktisch heißt,
steht auf der nächsten Folie.

Ein Hinweis zur Matrix selbst. Ich verwende die Achsen aus dem Aufgabenblatt,
Einfluss und Betroffenheit. In der Change Toolbox ist sie als
Einfluss-Interesse-Matrix geführt. Betroffenheit halte ich hier für
trennschärfer, weil die Kursleitungen sehr betroffen sind, ohne besonderes
Interesse an dem Thema zu haben.


## 11 — Widerstand

typ: einwaende
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer Nein sagt,
akzent: und was darauf antwortet.
klein: ja
einwaende:
  - "Programmbereich || „Die Befunde stehen in Bausteinen, über die ich nicht entscheide.“ || Die Freigabe der Bausteine gehört geklärt, bevor der Pilot beginnt. Im Beispielkurs liegen alle neun Befunde in zwei Bausteinen; einer davon steht in 105 Kursen."
  - "Kursleitung auf Honorarbasis || „Noch eine Aufgabe, für die es keine Unterrichtseinheit gibt.“ || Geprüft wird im Programmbereich, am eingegangenen Text. Die Kursleitung bekommt eine Rückmeldung — keine Pflicht, kein Werkzeug, keinen Nachweis."
  - "Redaktion des Programmhefts || „Verständlicher heißt länger, und ich habe eine feste Seitenzahl.“ || Geprüft wird der Text im Portal. Dort gibt es keine Seitenzahl, und das Heft verweist für die Einzelheiten ohnehin dorthin."
  - "Personalrat || „Eine technische Einrichtung. Das braucht unsere Zustimmung.“ || Richtig, und zwar vorher. § 78 HPVG knüpft die Mitbestimmung an die Eignung zur Überwachung, nicht an die Absicht. Instrument ist die Dienstvereinbarung."
callout: Betroffene zu Beteiligten machen — hier heißt das: entscheiden, bevor geschult wird.
calloutsub: Bausteinfreigabe, Zuständigkeit und Umgang mit den Protokollen sind keine Kommunikationsaufgaben. Wer sie offenlässt, schult gegen einen Widerstand, der berechtigt ist.
quellen:
  - "Häufigkeit der Bausteine: eigene Auszählung an daten/vhs-kursplan.json"
  - "§ 78 Abs. 1 Nr. 5 und § 66 HPVG, Fassung 2023 | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"

### NOTIZ

Jetzt zum Widerstand. Der Unterricht nennt vier Ursachen: Verlustangst,
Unsicherheit, Gewohnheit und fehlende Perspektive. Ich habe zuerst versucht,
für jede den Satz aufzuschreiben, den ich hier erwarte. Dabei ist mir
aufgefallen, dass alle vier Sätze aus demselben Mund kamen — aus dem einer
festangestellten Person. Deshalb habe ich die Folie umgestellt: Sie zeigt
jetzt vier Rollen von der Folie davor, und jede sagt Nein aus einem anderen
Grund.

Der Programmbereich zuerst. Sein Einwand lautet: Die Befunde stehen in
Bausteinen, über die ich nicht entscheide. Ich habe das nachgezählt, und es
stimmt vollständig. Der Beispielkurs, den ich gleich vorführe, hat keinen
eigenen Satz. Er besteht restlos aus zwei Bausteinen — dem Anmeldehinweis und
der Niveaubeschreibung. Alle neun Befunde liegen dort, und der Anmeldehinweis
steht wortgleich in hundertfünf Kursen. Das ist die Ursache Verlustangst in
ihrer echten Form: nicht Angst vor der Maschine, sondern die Aussicht, für
etwas gemessen zu werden, das man nicht ändern darf. Meine Antwort ist deshalb
keine Schulung, sondern eine Zuständigkeitsfrage, die vor dem Pilot geklärt
wird. Nebenbei ist es die gute Nachricht: Ein Baustein einmal in Ordnung
gebracht, und hundertfünf Kurse sind es mit.

Die Kursleitung auf Honorarbasis. Ihr Einwand lautet: Noch eine Aufgabe, für
die es keine Unterrichtseinheit gibt. Das ist die Ursache fehlende
Perspektive, und sie ist bei dieser Gruppe schärfer als bei allen anderen,
weil deren Abrechnungseinheit die Unterrichtsstunde ist. Textarbeit kommt darin
nicht vor. Meine Antwort ist der Zuschnitt: Geprüft wird im Programmbereich,
an dem Text, der dort eingeht. Die Kursleitung bekommt eine Rückmeldung, aber
keine Pflicht, kein Werkzeug und keinen Nachweis. Das hat noch einen zweiten
Grund. Verbindliche Regeln, Schulungspflicht und ein Protokoll je Text sind
genau die Merkmale, aus denen das Bundessozialgericht im Herrenberg-Urteil eine
Eingliederung in den Betrieb hergeleitet hat. Ein Projekt, das Honorarkräfte in
diese Kette holt, erzeugt ein Statusrisiko, das größer ist als sein Nutzen.

Die Redaktion des Programmhefts. Ihr Einwand ist der, an den ich zuletzt
gedacht hätte: Verständlicher heißt länger, und ich habe eine feste Seitenzahl.
Das ist die Ursache Gewohnheit, aber nicht als Trägheit, sondern als
konkurrierendes Regelwerk. Diese Redaktion kürzt beruflich. Ein Werkzeug, das
Erklärungen verlangt, arbeitet gegen ihren Auftrag. Meine Antwort trennt die
Medien: Geprüft wird der Text im Portal, und dort gibt es keine Seitenzahl. Das
Heft verweist für die Einzelheiten ohnehin auf das Portal, das steht wörtlich
darin.

Und der Personalrat. Sein Einwand lautet: Das ist eine technische Einrichtung,
dafür brauchen Sie unsere Zustimmung. Auf dieser Folie stand vorher, ich würde
eine Zusicherung schriftlich geben und dem Personalrat vorlegen. Das war
falsch, und ich sage das ausdrücklich, weil der Fehler lehrreich ist.
Paragraf achtundsiebzig des Hessischen Personalvertretungsgesetzes knüpft die
Mitbestimmung an technische Einrichtungen, die zur Überwachung geeignet sind.
Geeignet, nicht verwendet. Meine Zusage, nicht nach Urheber auszuwerten,
betrifft die Verwendung und räumt den Tatbestand gar nicht aus. Und vorlegen
ist keine Zustimmung. Das vorgesehene Instrument nennt der Paragraf selbst: die
Dienstvereinbarung. Dort gehören Zweckbindung, Zugriffskreis und Löschfrist
hinein.

Zwei Dinge dazu, die ich beim Nachlesen gelernt habe. Erstens vertritt der
Personalrat die Honorarkräfte doch, denn arbeitnehmerähnliche Personen gelten
nach diesem Gesetz als Beschäftigte. Auf der Folie davor habe ich gesagt, sie
hätten keinen formalen Einfluss; das gilt für die Gremien, nicht für die
Vertretung. Zweitens ist der Einfluss des Personalrats hier kein hoher, sondern
ein sperrender. Zwei von sechzehn Sitzen in der Betriebskommission sind als
Stimmblock bedeutungslos. Der Zustimmungsvorbehalt in eigener Sache ist es
nicht.

Damit zum Satz unten. Betroffene zu Beteiligten machen, das ist der Kern jeder
Widerstandsarbeit. Hier heißt er konkret: entscheiden, bevor geschult wird.
Drei der vier Einwände sind überhaupt keine Kommunikationsaufgabe. Wer die
Bausteinfreigabe, die Zuständigkeit und den Umgang mit den Protokollen
offenlässt und stattdessen eine Schulung ansetzt, schult gegen einen
Widerstand, der berechtigt ist. Der vierte Einwand, der der Redaktion, ist
einer — und er wird beantwortet, indem man zugibt, dass sie mit dem fehlenden
Prüfschritt die ganze Zeit recht hatte.

Eine Rolle fehlt auf der Folie, weil kein Platz war: die Direktion. Ihre Frage
lautet, wer die Protokolle sieht. Für jemanden, der laut Impressum persönlich
für die Inhalte verantwortlich ist, ist ein Protokoll zuerst eine Gefahr und
nicht ein Gewinn — es belegt datiert, was vorher nur unbemerkt war. Zum Gewinn
wird es mit einem Abstellplan: Ein dokumentierter Mangel mit Datum und Plan
steht besser da als ungeprüfter Bestand. Dieselbe Dienstvereinbarung, die den
Personalrat schützt, beantwortet auch diese Frage.


## 12 — Timeline

typ: timeline
kapitel: 03 · CHANGE MANAGEMENT
titel: Drei Monate,
akzent: drei Stränge.
klein: ja
monate: Monat 1 | Monat 2 | Monat 3
tortitel: Vorher
tor: Zustimmung des Personalrats, als Dienstvereinbarung
strang1: Technische Implementation || Setup > Assistent im vorhandenen KI-Rahmen anlegen, Regeln an echten Texten schärfen || Pilot > Ein Programmbereich, und nur die Texte, die neu entstehen || Rollout > Vorbereitet, freigegeben aber erst nach der Nachmessung
strang2: Kommunikation || Ankündigung > Erst die Dienstvereinbarung, dann die Bekanntgabe im Bereich || Training > Schulung nach Artikel 4 KI-Verordnung, für alle, die das System bedienen || Support > Feste Sprechstunde im Pilotbereich, nicht auf Zuruf
strang3: Change || Vorbereitung > Betroffene befragen, Freigabe der Textbausteine klären || Einbindung > Der Bereich wählt, welche Regeln scharf gestellt werden, dazu der Quick Win || Begleitung > Nachmessung mit demselben Skript, dann Entscheidung
callout: Der Kommunikationsstrang beginnt nicht aus Höflichkeit vor dem technischen, sondern weil er muss.
calloutsub: Die Einführung ist mitbestimmungspflichtig. Ohne Zustimmung des Personalrats darf der Assistent nicht angelegt werden — deshalb steht sie links vor Monat 1 und nicht in ihm.
quellen:
  - "§ 78 Abs. 1 Nr. 5 und § 66 HPVG, Fassung 2023 | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"
  - "KI-Verordnung (EU) 2024/1689, Artikel 4 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Der Zeitplan, drei Monate, drei Stränge. Die Aufgabenstellung gibt für jeden
Strang drei Phasen vor, und Sie finden sie hier als Überschrift jeder Zelle
wieder: Setup, Pilot, Rollout, dann Ankündigung, Training, Support, dann
Vorbereitung, Einbindung, Begleitung. Darunter steht jeweils, was das hier
konkret heißt.

Links, blau, sehen Sie etwas, das in keinem der drei Monate steht, sondern
davor. Das ist die Zustimmung des Personalrats als Dienstvereinbarung, und sie
steht dort, weil sie ein Tor ist und keine Parallelaufgabe. Hätte ich sie in
den ersten Monat gesetzt, sähe es aus, als könne daneben schon der Assistent
angelegt werden. Das darf er nicht.

Damit zum ersten Strang. Technisch ist wenig zu tun, und das ist ein Vorteil
dieses Projekts. Im ersten Monat wird der Assistent im vorhandenen KI-Rahmen
angelegt und an echten Texten nachgeschärft. Im zweiten läuft der Pilot, in
einem Programmbereich und nur an den Texten, die neu entstehen — das sind, wie
gerechnet, ungefähr dreiundsiebzig im Jahr. Im dritten wird die Ausweitung
vorbereitet, aber nicht freigegeben. Freigegeben wird sie erst, wenn die
Nachmessung sie trägt, und die liegt am Ende desselben Monats. Vorher wäre die
Entscheidung ein Vorgriff.

Der Kommunikationsstrang. Ankündigung heißt hier: erst die Dienstvereinbarung,
dann die Bekanntgabe. In dieser Reihenfolge, denn eine Ankündigung vor der
Mitbestimmung erzeugt genau den Ärger, den man vermeiden wollte. Das Training
im zweiten Monat ist keine Kür. Artikel vier der KI-Verordnung verpflichtet
Betreiber seit Februar zweitausendfünfundzwanzig zu ausreichender KI-Kompetenz,
und zwar wörtlich für ihr Personal und für andere Personen, die in ihrem
Auftrag mit dem Betrieb und der Nutzung befasst sind. Deshalb steht in der
Zelle nicht das Wort Personal, sondern alle, die das System bedienen. Wer es
nicht bedient, braucht die Schulung nicht — das betrifft die Kursleitungen, und
es ist der Grund, warum wir sie aus dieser Kette heraushalten.

Support im dritten Monat heißt: eine feste Sprechstunde, nicht auf Zuruf. Eine
Zusage, jederzeit ansprechbar zu sein, ist in einem Haus mit
fünftausendachthundert Veranstaltungen keine Zusage.

Der Change-Strang folgt einer einfachen Reihenfolge: erst fragen, dann handeln.
In der Vorbereitung werden die Betroffenen befragt, und die Freigabe der
Textbausteine wird geklärt — das ist die offene Frage vom Widerstandsteil, und
sie gehört in den ersten Monat, weil der Quick Win sonst im zweiten auf eine
Zuständigkeit läuft, die niemand hat. In der Einbindung wählt der Bereich
selbst, welche der sechs Regeln scharf gestellt werden. Und die Begleitung
endet mit der Nachmessung, mit demselben Skript wie die Ausgangsmessung.


## 13 — Die ersten 30 Tage und die Ressourcen

typ: plan
kapitel: 03 · ZEITPLAN UND RESSOURCEN
titel: Die ersten 30 Tage,
akzent: und was sie kosten.
klein: ja
schrittetitel: ERSTE 30 TAGE · IN DIESER REIHENFOLGE
schritte:
  - "Dienstvereinbarung mit dem Personalrat schließen > Vorher darf nichts angelegt werden."
  - "Einen Programmbereich freiwillig als Pilotbereich gewinnen > Ein zugewiesener liefert kein belastbares Ergebnis."
  - "Die Freigabe der Textbausteine klären > Sonst trifft der Quick Win auf niemanden."
  - "Assistent im vorhandenen KI-Rahmen anlegen > Keine Beschaffung, keine zusätzliche Stelle."
kennzahlentitel: PRÜFAUFWAND IM JAHR
kennzahlen:
  - "290 Std. || so lautet der Einwand: jede der 5.800 Veranstaltungen einzeln geprüft || einwand"
  - "29 Std. || gemessen: nur die rund 600 Texte, die im Jahr wirklich neu entstehen"
  - "4 Std. || im Pilot, ein Programmbereich, rund 73 neue Texte"
callout: Der Einwand rechnet mit 5.800 Texten. Es sind rund 600, weil 54 Prozent der Kurse ihren Text teilen.
calloutsub: Gemessen an 489 Kursen. Offen bleibt, was die vhs als „neu“ zählt — im Grenzfall wären es 220 Stunden. Auch das liegt unter dem Einwand, gehört aber im Pilot gemessen.
quellen: eigene Erhebung, daten/wirtschaftlichkeit.md mit allen Szenarien und Einschränkungen

### NOTIZ

Damit zu den nächsten Schritten. Links stehen die ersten dreißig Tage, und die
Nummern sind keine Zierde: Das ist eine Reihenfolge, in der jeder Schritt den
nächsten bedingt.

Zuerst die Dienstvereinbarung mit dem Personalrat. In sie gehören
Zweckbindung, Zugriffskreis und Löschfrist der Protokolle. Sie steht an erster
Stelle, weil vorher nichts angelegt werden darf.

Zweitens einen Programmbereich als Pilotbereich gewinnen, und zwar freiwillig.
Ein zugewiesener Pilotbereich liefert kein belastbares Ergebnis, sondern nur
Erfüllung.

Drittens die Freigabe der Textbausteine klären. Das ist der Punkt vom
Widerstandsteil. Bleibt er offen, läuft der Quick Win im zweiten Monat auf eine
Zuständigkeit, die niemand hat.

Und erst viertens das Technische: den Assistenten im vorhandenen KI-Rahmen
anlegen. Keine Beschaffung, kein neuer Vertrag, keine zusätzliche Stelle.

Rechts die Zahlen, denn der häufigste Einwand lautet, das koste zu viel Zeit.
Er rechnet so: fünftausendachthundert Veranstaltungen, drei Minuten pro Text,
das sind zweihundertneunzig Stunden im Jahr. Diese Rechnung unterstellt, dass
jede Veranstaltung einen eigenen Text hat. Das ist nicht so. Vierundfünfzig
Prozent der Kurse teilen ihren Text mit mindestens einem anderen, und nur rund
zehn Prozent der Angebote sind je Semester neu. Übrig bleiben ungefähr
sechshundert Texte im Jahr und damit neunundzwanzig Stunden. Im Pilot, in einem
von acht Bereichen, sind es vier.

Eine Einschränkung sage ich dazu, weil sie die größte der ganzen Rechnung ist.
Was die vhs als neues Angebot zählt, ist nicht dokumentiert. Wenn zusätzlich
bestehende Texte überarbeitet werden, steigt die Zahl, im Grenzfall auf
zweihundertzwanzig Stunden. Selbst das liegt noch unter dem Einwand. Aber die
Zahl gehört im Pilot gemessen und nicht geschätzt, und deshalb steht sie unten
auf der Folie und nicht nur in meinen Unterlagen.


## 14 — Erfolgsmessung und Risiken

typ: tabelle
kapitel: 03 · ERFOLGSMESSUNG
titel: Woran man merkt,
akzent: ob es gewirkt hat.
klein: ja
kompakt: ja
spalten: Kennzahl | heute | Ziel nach 3 Monaten | gemessen mit
zeilen:
  - "Texte mit mindestens einem Befund | 58 % | ! unter 25 % | daten/messung.py, unverändert"
  - "Neue Texte im Pilotbereich geprüft | 0 | + alle | Protokoll des Werkzeugs"
  - "Deutschkurse A1/A2 mit Wörtern über Niveau | 6 von 6 | ! höchstens 2 von 6 | daten/messung.py, unverändert"
  - "Teilnehmende, die die Beschreibung verstanden haben | nicht erhoben | + Ausgangswert und Trend | Kurzbefragung am Kursende, freiwillig und vergütet"
risiken:
  - "Die Mitbestimmung stockt, der Pilot verschiebt sich. > Die Dienstvereinbarung ist Schritt eins, nicht der letzte. Der Entwurf liegt vor, bevor gefragt wird."
  - "Die Protokolle werden gegen das Unternehmen verwendet. > Zweckbindung, Zugriffskreis, Löschfrist in dieselbe Dienstvereinbarung — dazu ein Abstellplan mit Datum."
  - "Die Bausteine werden nicht freigegeben, Befunde ohne Adressat. > Die Freigabe ist Schritt drei, also vor dem Quick Win. Sonst wird der Pilot begrenzt, offen benannt."
callout: Die Nachmessung läuft mit demselben eingefrorenen Skript wie die Ausgangsmessung. Über die Methode kann später niemand streiten.
quellen: Ausgangsmessung mit daten/messung.py, Stichprobe vom 28.07.2026 · Wirtschaftlichkeit an 489 Kursen

### NOTIZ

Und woran würde man merken, ob es gewirkt hat?

Vier Kennzahlen mit Ausgangswert und Ziel. Die Befundquote soll von
achtundfünfzig Prozent unter fünfundzwanzig fallen. Alle neuen Texte im
Pilotbereich sollen geprüft sein. Und von den sechs Deutschkursen auf A1 und
A2, die heute alle Wörter über dem Niveau ihrer Zielgruppe enthalten, sollen
höchstens noch zwei betroffen sein.

Die vierte Zeile ist mir wichtig, weil die ersten drei nur den Text messen und
nicht die Wirkung. Deshalb frage ich die Teilnehmenden selbst. Nicht über einen
Fragebogen auf der Website, denn den füllt genau die Zielgruppe nicht aus, um
die es geht. Sondern im Kurs, am Ende einer Stunde, in einfacher Sprache. Das
erreicht die Menschen wirklich.

Dazu ein Punkt, an dem ich mich selbst korrigiert habe. Hier stand vorher, die
Befragung erledige die Kursleitung. Das widerspricht der Zusage von der
Widerstandsfolie, dass für die Kursleitungen keine neue Pflicht entsteht. Eine
Befragung ist eine Aufgabe, und Aufgaben ohne Vergütung sind bei
Honorarkräften genau das Problem. Sie ist deshalb freiwillig und wird vergütet.
Das ist keine neue Stelle und keine Beschaffung, sondern ein Zusatzhonorar für
eine begrenzte Zahl von Kursen im Pilotbereich.

Wichtig ist die letzte Spalte. Die Nachmessung läuft mit demselben Skript wie
die Ausgangsmessung, und das Skript ist dafür eingefroren. Wäre es zwischendurch
verbessert worden, wüsste man hinterher nicht, ob die Texte besser geworden sind
oder nur die Messung anders. Über die Methode kann später niemand streiten.

Unten drei Risiken. Das erste ist, dass die Mitbestimmung stockt und sich der
Pilot verschiebt. Dagegen hilft nur, sie an den Anfang zu stellen und dem
Personalrat einen Entwurf vorzulegen, bevor man ihn fragt.

Das zweite Risiko habe ich zuerst übersehen, und es ist das unangenehmste: Die
Protokolle können gegen das Unternehmen verwendet werden. Sie belegen datiert
und zitierbar, dass Texte Kriterien verletzen, die das Haus sich freiwillig
gibt. Wer laut Impressum persönlich für die Inhalte verantwortlich ist, hat nach
dem Pilot eine Kenntnis, die er vorher nicht hatte. Deshalb gehören die
Protokolle in die Dienstvereinbarung, mit Zweckbindung, Zugriffskreis und
Löschfrist. Und deshalb gehört zu jedem Befundstand ein Abstellplan mit Datum.
Ein dokumentierter Mangel mit Plan steht besser da als ungeprüfter Bestand — aber
das gilt nur, wenn der Plan wirklich existiert.

Das dritte Risiko ist die Bausteinfreigabe. Bleibt sie aus, meldet der Pilot
Befunde, für die niemand zuständig ist. Dann wird der Pilot auf
kursindividuelle Texte begrenzt, und ich sage das offen statt es zu verschweigen.

Ein viertes nenne ich nur kurz, weil es auf der Folie keinen Platz mehr hatte:
Sollte der KI-Rahmen des Verbands nicht bereitstehen, läuft der Prompt auch
außerhalb. Das ist der Grund, warum ich vorhin zwei Wege gezeigt habe.


## 15 — Schlussfolie

typ: schluss
bild: bilder/15-durchgang.png
bildnotiz: Dieselbe Wand wie auf der Titelfolie, der Durchgang jetzt begehbar und hell.
titel: Danke für die Aufmerksamkeit —
akzent: jetzt läuft der Prompt live.
untertitel: An einem echten Kurstext aus dem Portal. Danach gerne eure Fragen.
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

Damit danke ich für die Aufmerksamkeit. Ich zeige euch jetzt kurz, wie es
läuft, an einem echten Kurstext aus dem Portal. Danach gerne eure Fragen.
