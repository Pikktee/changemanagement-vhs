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
link: klartext-vhs.henrikheil.net
meta: Volkshochschule Frankfurt am Main | Acht Programmbereiche | 5.800 Texte im Jahr
fussl: ABSCHLUSSPROJEKT · CHANGE UND KI
fussr: CIMDATA · HENRIK HEIL · JULI 2026
bild: bilder/01-titel-wand.png
bildnotiz: Wand aus Textzeilen mit einem Schlitz. Gezeichnet von bilder/zeichnen.py, Gegenstueck auf der Schlussfolie.

### NOTIZ

Ich stelle euch heute mein Abschlussprojekt vor: KLARTEXT, ein Prüfschritt für
die Kursbeschreibungen der Volkshochschule Frankfurt.

Es geht um Barrierefreiheit. Die meisten denken dabei an Technik: Kontraste,
Tastaturbedienung, Vorleseprogramme. Mich interessiert der andere Teil — ob
der Text ankommt bei denen, für die er geschrieben ist. Das betrifft alle acht
Programmbereiche.

Angefangen hat es mit dem schärfsten Fall. Die Volkshochschule bietet
Deutschkurse für Menschen an, die gerade erst Deutsch lernen, und die
Beschreibungen dieser Kurse sind in einem Deutsch geschrieben, das man erst
nach dem Kurs versteht. Wer Deutsch lernen will, muss also erst Deutsch
können. Das ist der Extremfall, aber das Prinzip dahinter gilt überall.

Ich habe das Projekt allein bearbeitet, alle Rollen liegen also bei mir. Und
alle Zahlen, die gleich kommen, habe ich selbst gemessen, an der echten
Website, am achtundzwanzigsten Juli. Der Datensatz liegt der Arbeit bei.

Am Ende zeige ich das Werkzeug an einem echten Kurstext.


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

Drei Zahlen zum Einstieg.

Die Volkshochschule veröffentlicht rund fünftausendachthundert
Kursbeschreibungen im Jahr. In meiner Stichprobe von sechzig Kursen haben
achtundfünfzig Prozent mindestens einen Befund, und das ist die Untergrenze:
Die Zahl stammt von einem Skript, das ohne KI auskommt und deshalb eine der
sechs Regeln nicht prüfen kann. Mit dem Prüfassistenten liegt der Wert höher.

Die dritte Zahl stammt aus dem Unternehmen selbst. In der Erklärung zur
Barrierefreiheit steht, wann die Website zuletzt extern geprüft wurde: am
ersten Juli zweitausendeinundzwanzig, heute auf den Tag genau fünf Jahre her.
Seitdem bewertet sich das Unternehmen selbst.

Dieselbe Erklärung enthält den Satz, der mich auf dieses Projekt gebracht hat.
Die wichtigsten Informationen zu Betrieb und Kursgeschäft, heißt es dort,
seien in einfacher Sprache verfügbar. Das Unternehmen hat die Frage nach der
Verständlichkeit also längst gestellt und für einen Bereich beantwortet. Nur
für die Kursbeschreibungen selbst, den mit Abstand größten Textbestand, gilt
das nicht.

Da setze ich an. Unten steht die Frage, um die es geht: Mehr als jeder zweite
Text hat einen Befund. Für wen ist er eigentlich zu schwer?


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

Das Ziel oben ist von den Lesenden her formuliert. Wer einen Kurs sucht, soll
die Beschreibung verstehen, ob er sie liest oder vorgelesen bekommt. Die
Betriebssatzung sagt, die Angebote stehen allen offen — dann muss das auch für
die Texte gelten, mit denen wir sie ankündigen.

Geprüft wird zweierlei: ob die Zielgruppe den Text versteht, und ob ein
Vorleseprogramm etwas damit anfangen kann.

Dafür genügt ein System-Prompt in dem KI-Rahmen, den der Volkshochschul-
Verband ohnehin für alle Volkshochschulen bereitstellt. Es muss nichts
beschafft werden.

Die Abgrenzung darunter zieht sich durch das ganze Konzept: Für die technische
Barrierefreiheit der Website bleibt ein normales Prüfwerkzeug zuständig,
zusammen mit der städtischen IT. Die KI sieht nur den Kurstext.

Unten steht der erste Schritt: ein Pilot in einem Programmbereich, drei
Monate. Der Prompt schlägt vor, der Mensch entscheidet.


## 4 — Das Unternehmen und der Prozess heute

typ: zweispalt
kapitel: 01 · UNTERNEHMEN UND IST-ANALYSE
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
  - "Ablauf des Hauses: eigene Recherche, Belege und Annahmen dokumentiert"

### NOTIZ

Das Unternehmen und der Prozess.

Die Volkshochschule Frankfurt ist kein Amt, sondern ein Eigenbetrieb der
Stadt. Geleitet wird sie von einem Direktor, der laut Impressum auch
persönlich für die redaktionellen Inhalte der Website verantwortlich ist.
Darüber steht eine Betriebskommission mit sechzehn Sitzen, zwei davon für den
Personalrat. Diese zwei Sitze spielen später noch eine Rolle.

Am Ende der ersten Zeile steht die Qualitätstestierung. Das Unternehmen ist
seit zweitausendfünf nach L Q W testiert, Lernerorientierte
Qualitätstestierung in der Weiterbildung, ein Verfahren mit regelmäßiger
externer Prüfung, inzwischen in der sechsten Runde. Hier fehlt also keine
Qualitätskultur. Es fehlt genau ein Schritt darin.

Der Satz oben stammt wörtlich aus der Betriebssatzung: Die Angebote stehen
grundsätzlich allen offen, ohne Rücksicht auf Vorbildung. Daran messe ich das
Unternehmen — nicht am Gesetz, sondern an seinem eigenen Anspruch.

Rechts steht, wie ein Kurstext entsteht. Geplant wird halbjährlich, von den
Teams der vier Fachbereiche. Der Text wird geschrieben und ins
Kursverwaltungssystem eingepflegt, und dann erscheint er. Über der Spalte
steht das Wort angenommen, denn wer bei der vhs Frankfurt die Texte schreibt,
ist nicht öffentlich dokumentiert.

Zwischen dem Einpflegen und dem Erscheinen ist kein Prüfschritt auf
Verständlichkeit vorgesehen. Das ist kein Vorwurf, denn dieser Arbeitsschritt
ist nirgends vorgesehen. Genau deshalb ist es ein Fall für Prozessgestaltung
und nicht für einen Appell, sich mehr Mühe zu geben.

Für das gedruckte Programmheft gibt es sehr wohl eine Redaktion, das Impressum
nennt sie mit Namen. Für das Portal gibt es sie nicht, und dort stehen die
Texte, um die es hier geht.

Ich habe nachgezählt: Vierundfünfzig Prozent aller Kurse teilen sich ihren
Text mit mindestens einem anderen. Ein schlecht formulierter Text ist hier nie
ein Einzelfall.


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
  - "Englisch A1.1 | liest Deutsch fließend | 0 | 1"
  - "Deutsch als Fremdsprache A2.2 | lernt Deutsch, kann bisher A1 | 24 | 28"
callout: Beide Kurse tragen A im Titel. Nur bei einem ist der Text zu schwer für seine Leser.
calloutsub: Ob ein Text verständlich ist, entscheidet nicht der Text — sondern die Zielgruppe, die ihn lesen soll.
quellen:
  - "Eigene Auswertung von 60 Kursbeschreibungen, 29.07.2026 — Auswertung und Daten liegen der Arbeit bei"
  - "Kursportal-Schnittstelle der vhs | https://vhs.frankfurt.de/KundenportalApi/api/angebot"

### NOTIZ

Zur Potenzialermittlung. Hier habe ich nicht geschätzt, sondern gemessen.

Das Kursportal hat eine offene Schnittstelle. Darüber habe ich sechzig
Kursbeschreibungen aus sieben der acht Programmbereiche gezogen und mit einem
eigenen Skript ausgewertet. Fünfunddreißig von sechzig Texten haben mindestens
einen Befund.

Oben steht, wonach ich gemessen habe: sechs Regeln, erst der Maßstab, dann das
Ergebnis. Dieselben sechs Regeln sind zugleich der Maßstab des
Prüfassistenten, den ich gleich zeige.

Links stehen die beiden Pflichtregeln. Sie stehen auf Stufe A der
Barrierefreiheitsrichtlinien und sind damit verbindlich.

Struktur heißt: Eine Zeile sieht aus wie eine Überschrift, ist im Quelltext
aber gewöhnlicher Fließtext. Dasselbe gilt für Aufzählungen, die jemand nur
mit Bindestrichen gebaut hat. Wer sehend liest, merkt davon nichts. Ein
Screenreader dagegen bietet an, sich alle Überschriften einer Seite vorlesen
zu lassen, um gezielt dorthin zu springen — was technisch keine Überschrift
ist, taucht in dieser Liste nicht auf. Die Gliederung ist dann sichtbar
vorhanden und für das Vorleseprogramm nicht da.

Linktext heißt: Der Link sagt nicht, wohin er führt. Das bekannteste Beispiel
ist ein Link, der schlicht „hier“ heißt. Der Grund ist derselbe: Screenreader
lesen auf Wunsch nur die Links einer Seite vor, ohne den Text drumherum. Eine
Liste aus fünfmal „hier“ hilft niemandem weiter.

Rechts stehen die vier Empfehlungen. Verbindlich sind sie nicht, aber sie sind
der eigentliche Ertrag dieses Projekts. Zwei davon, zu schwere Wörter und
nicht aufgelöste Abkürzungen, stehen auf Stufe AAA — der höchsten, die niemand
einhalten muss. Die beiden anderen habe ich selbst gesetzt.

Niveau heißt: Ein Wort liegt über dem Sprachniveau derer, die den Text lesen
sollen. Das ist die Regel, die sich ohne Kenntnis der Zielgruppe überhaupt
nicht anwenden lässt.

Amtsdeutsch heißt: Im Text steht ein Verwaltungswort, obwohl ein alltägliches
genügen würde. Umbuchung statt Wechsel, gegebenenfalls statt wenn nötig. Das
trifft nicht nur Sprachanfänger, sondern auch geübte Leserinnen und Leser.

Satz heißt: über fünfundzwanzig Wörter, bei Deutschkursen über fünfzehn. Diese
beiden Zahlen habe ich gesetzt, nicht gemessen; sie orientieren sich an den
Empfehlungen für einfache Sprache. Zur Satzlänge sagen die
Barrierefreiheitsrichtlinien nämlich nichts, und ob es die richtigen Zahlen
sind, soll der Pilot beantworten.

Abkürzung heißt: Ein Kürzel steht im Text, ohne beim ersten Mal aufgelöst zu
werden. Davon hat die vhs einige eigene, D-T-Z zum Beispiel, der Deutsch-Test
für Zuwanderer.

Die Tabelle darunter zeigt zwei Sprachkurse, und beide tragen eine niedrige
Stufe im Titel. Das bedeutet zweimal etwas völlig Verschiedenes.

Beim Englischkurs steht A1 für das Englisch, das dort gelernt wird. Wer die
Beschreibung liest, ist deutschsprachig und liest Deutsch fließend. Beim
Deutschkurs steht A2 für das Deutsch, das dort gelernt wird. Wer diese
Beschreibung liest, kann Deutsch bisher eine Stufe darunter, also A1.

Der Englischkurs hat kein einziges Wort über dem Niveau seiner Leser und einen
Befund insgesamt, eine nicht aufgelöste Abkürzung. Der Deutschkurs hat
vierundzwanzig zu schwere Wörter und achtundzwanzig Befunde.

Dabei sind beide Texte gleich einfach gebaut. Die Sätze sind in beiden Fällen
kurz, im Schnitt neun beziehungsweise elf Wörter. Ein Lesbarkeitsindex, der
Satz- und Wortlängen zählt, findet bei keinem der beiden etwas. Er schweigt
zweimal, und einmal davon zu Unrecht.

Deshalb reicht kein Werkzeug, das nur den Text ansieht. Man muss wissen, für
wen der Text ist. In meiner Stichprobe stehen sechs Deutschkurse auf den
Stufen A1 und A2, und alle sechs enthalten Wörter, die über dem Niveau ihrer
Zielgruppe liegen: Selbsteinschätzung, Fehleinschätzung, Umbuchung. Wörter,
die man erst weit oberhalb des Kursziels lernt. Genau hier kann ein fachlich
eingestellter Prompt etwas, was ein Standardwerkzeug nicht kann.

Noch einmal zu den achtundfünfzig Prozent: Das ist eine Untergrenze. Mein
Messskript prüft fünf der sechs Regeln; die erste, ob eine hervorgehobene
Zeile eine Überschrift sein sollte, kann kein Skript entscheiden. Ich messe
also bewusst zu niedrig statt zu hoch.


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

Kurz die Rechtslage.

Digitale Barrierefreiheit bedeutet, dass eine Website auch für Menschen mit
Behinderung nutzbar sein muss. Der Maßstab sind die WCAG, mit drei Stufen: A,
doppel A und dreifach A.

Für die vhs gilt weder die EU-Richtlinie noch das
Barrierefreiheitsstärkungsgesetz unmittelbar. Sie ist eine kommunale
Einrichtung in Hessen, also greift Landesrecht: Paragraph vierzehn des
Hessischen Behindertengleichstellungsgesetzes und die hessische Verordnung.
Gefordert wird Stufe doppel A.

Der Block in der Mitte zeigt nur die Kriterien, die am Text der
Kursbeschreibung selbst hängen. Links steht, was daran verbindlich ist: dass
eine Zeile, die eine Gliederungsebene eröffnet, auch technisch als Überschrift
ausgezeichnet wird, und dass ein Linktext sagt, wohin er führt. Rechts steht,
was freiwillig ist: dass Abkürzungen erklärt werden und dass das Leseniveau
zur Zielgruppe passt. Beides ist dreifach A und damit nicht gefordert — genau
die beiden Kriterien also, um die es in diesem Projekt geht.

Ich könnte jetzt mit einem drohenden Bußgeld argumentieren. Das wäre bequem,
und es wäre falsch.

Freiwillig heißt aber nicht belanglos. Paragraph drei Absatz eins der
hessischen Verordnung verlangt eigenständig, dass Angebote verständlich sind.
Die Konformitätsstufe begründet eine Vermutung, keine Obergrenze der Pflicht.
Ich argumentiere also nicht gegen das Recht, sondern in einer Lücke, die es
selbst offenlässt.

Den eigentlichen Auftrag gibt sich das Unternehmen ohnehin selbst. Die
Betriebssatzung sagt, die Angebote stünden allen offen, ohne Rücksicht auf
Vorbildung. Für ein solches Unternehmen ist es nicht vertretbar, dass
ausgerechnet die Kriterien für Menschen mit geringer Vorbildung die
freiwilligen sind.


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

Zur Lösung. Sie beginnt mit einer Abgrenzung, und die halte ich für den
wichtigsten Teil meines Konzepts.

Links steht, was am Gerüst der Seite hängt: Kontraste, Tastaturbedienung,
Seitentitel, Navigation. Das kann man prüfen, ohne einen einzigen Kurs zu
kennen. Es gilt für alle fünftausendachthundert Texte gleich, dafür gibt es
etablierte Programme wie axe-core, und zuständig ist die städtische IT.

Rechts steht, was am einzelnen Text hängt. Versteht die Zielgruppe genau
dieses Kurses ihn? Diese Frage lässt sich nicht beantworten, ohne zu wissen,
wer liest. Zuständig sind die Programmbereiche.

Die Trennlinie verläuft also nicht zwischen Sprache und Technik. Zwei meiner
sechs Regeln sind selbst Pflichtkriterien der Barrierefreiheit. Ein Beispiel:
eine hervorgehobene Zeile, die als Überschrift gemeint ist, aber im Quelltext
keine ist. Das Prüfprogramm sieht dort nur Fließtext und meldet nichts. Ob
diese Zeile eine Überschrift sein sollte, kann man dem Text nicht ansehen,
sondern nur verstehen. Deshalb liegt ausgerechnet dieses Pflichtkriterium
rechts.

Diese Trennung hat sich beim Bauen zweimal selbst bestätigt. Zwei Zusagen, die
ich zuerst in den Prompt geschrieben hatte, hat das Modell nicht zuverlässig
eingehalten. Beide stehen jetzt im Programmcode, weil sie feststehen und keine
Einschätzung verlangen.

Technisch braucht es den KI-Rahmen, den der Volkshochschul-Verband ohnehin
bereitstellt, einen dort hinterlegten Assistenten und die Wortliste als Datei.
Kein neuer Vertrag, kein Eingriff ins Kursverwaltungssystem.


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
  - "System-Prompt, Fassung v11 vom 29.07.2026 — zwölf Fassungen mit Anlass und Begründung"
  - "KI-Verordnung (EU) 2024/1689, Anhang III | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Zum Kern der Aufgabe, dem System-Prompt. Er folgt der Sechs-Komponenten-
Struktur aus dem Aufgabenblatt.

Die ROLLE macht ihn zur Redaktionsassistenz, nicht zur Autorin. Die AUFGABE
schreibt die Reihenfolge vor: erst die Zielgruppe bestimmen, dann prüfen. Das
FORMAT erzwingt zu jedem Befund ein wörtliches Zitat, eine Begründung und
einen konkreten Vorschlag. Ohne Vorschlag kein Befund.

Der KONTEXT enthält das Hauswissen: die acht Programmbereiche, die internen
Abkürzungen, sechs Prüfregeln und — der wichtigste Teil — achthundertzwanzig
Wörter des Prüfungswortschatzes für das Goethe-Zertifikat A1. Diese Liste
steht vollständig im Prompt, nicht als Verweis. Er schätzt das Sprachniveau
also nicht, sondern begründet es.

Das ist das Ergebnis der ersten Überarbeitung. In meiner ersten Fassung
behauptete der Prompt, gegen die Wortlisten zu prüfen, hatte sie aber gar
nicht. Er schätzte weiter frei und klang dabei nach Beleg — derselbe Fehler,
den ich anderen Werkzeugen vorwerfe. Der Grundstock dieser Listen stammt
übrigens laut Goethe-Institut aus einer Veröffentlichung der Prüfungszentrale
des Deutschen Volkshochschulverbands in Frankfurt.

In der Zeile GRENZEN steht: bewertet Texte, niemals Personen. Dieser eine Satz
leistet zweierlei. Er hält das Projekt aus dem Hochrisikobereich der KI-
Verordnung heraus, denn Anhang III setzt überall eine Bewertung natürlicher
Personen voraus. Und er ist die Antwort auf die Frage des Personalrats, ob
hier Leistung kontrolliert wird.


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

Bleibt die Frage, wie das in den Alltag kommt. Dafür gibt es zwei Wege, und
beide stehen vom ersten Tag an offen.

Der erste braucht keine eigene Technik. Der Deutsche Volkshochschul-Verband
hat im Mai zweitausendfünfundzwanzig eine Rahmenvereinbarung mit einem
Anbieter namens fobizz geschlossen. Mitarbeitende aller Volkshochschulen in
Deutschland haben darüber datenschutzkonformen Zugang zu KI-Anwendungen, und
man kann dort eigene Assistenten mit eigenen Anweisungen anlegen. Genau das
ist mein Prompt. Zustimmung außerhalb des Pilotbereichs braucht es dafür
nicht, weil der Rahmenvertrag schon da ist. Zu klären ist allerdings, ob die
vhs Frankfurt die Lizenz auch tatsächlich gebucht hat — der Rahmenvertrag
schafft die Möglichkeit, er ist nicht die Buchung.

Eine Einschränkung gehört dazu, denn diesen Weg habe ich nicht ausprobiert:
Mein Prüfwerkzeug bearbeitet jede Antwort nach. Es rechnet die Einstufung
anhand einer Tabelle nach und entfernt Personennamen. Beides stand
ursprünglich im Prompt, und beides hielt das Modell nicht zuverlässig ein —
deshalb steht es heute im Programmcode. In einem fremden Assistenten gibt es
diesen Code nicht. Was das praktisch bedeutet, muss der Pilot zeigen.

Der zweite Weg ist das Prüfwerkzeug, das ich gebaut habe. Dort fügt man den
Entwurf ein — oder gibt bei einem vorhandenen Kurs nur die Nummer ein, dann
holt es den Text selbst. Die Schnittstelle des Kursportals ist öffentlich, das
kostet keinen Zugang; es braucht nur einen eigenen Server.

Rechts steht, was dabei herauskommt: ein Befund aus einem echten Durchlauf,
dem Deutschkurs auf A2. Jeder Befund hat dieselben vier Teile: die Einstufung,
die Regel, die wörtliche Stelle aus dem Text und einen konkreten Vorschlag.
Dieser hier ist Pflicht, der Link heißt schlicht „hier“. Wer sich die Seite
vorlesen lässt und von Link zu Link springt, hört nur „hier“. Der Vorschlag
daneben ist kein Kommentar, sondern fertiger Text zum Übernehmen.

Ich zeige euch das kurz live, an genau diesem Kurs.

Das ist ein Prototyp, den ich für diese Arbeit gebaut habe. Er belegt, dass
der Weg funktioniert, er ist keine fertige Anwendung.

Die Nachbemerkung unten ist kein Teil des Pilotprojekts. Man könnte die
Prüfung ins Redaktionssystem selbst einbauen, dort, wo der Text entsteht. Nur
wird das Portal von einem externen Dienstleister betreut, also hieße das:
Auftrag, Budget, Vorlauf. Man kauft nichts, bevor man weiß, ob es wirkt.


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
oben_links: Beobachten || Städtische IT || Advellence als Portaldienstleister || Betriebskommission als Aufsichtsgremium || Volkshochschul-Verband, stellt den KI-Rahmen
oben_rechts: Eng einbinden || Direktor als Verantwortlicher der Inhalte || Der Fachbereich des Pilotbereichs || Redaktion des Programmhefts || Personalrat, Zustimmung erforderlich
unten_links: Informieren || Die drei übrigen Fachbereiche
unten_rechts: Konsultieren || Kursleitungen auf Honorarbasis || Teilnehmende, besonders in Deutschkursen und Grundbildung
quellen:
  - "§ 4 Abs. 4 Satz 2 HPVG — Honorarkräfte werden mitvertreten | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"

### NOTIZ

Damit zum Change-Teil, und der beginnt mit den **Stakeholdern**. Die
**Einfluss-Betroffenheits-Matrix** sortiert sie nach zwei Fragen: Wer ist
betroffen, und wer hat Einfluss.

Oben rechts, eng einbinden.

**Der Direktor** — laut Impressum persönlich für die redaktionellen Inhalte
verantwortlich.

**Der Fachbereich des Pilotbereichs** — und zwar nur dieser eine. Vier
Fachbereiche gleichzeitig einzubinden wäre kein Pilot mehr.

**Die Redaktion des Programmhefts** — prüft Texte für den Druck schon heute,
weiß also, wie Textprüfung geht.

**Der Personalrat** — hier ist die Einordnung eigentlich zu schwach. Sein
Einfluss ist kein hoher, sondern ein **sperrender**: Die Einführung des
Werkzeugs ist mitbestimmungspflichtig, sie braucht seine Zustimmung. Seine
zwei von sechzehn Sitzen in der Betriebskommission sind daneben bedeutungslos.

Nur dieser eine Fachbereich — deshalb unten links, informieren.

**Die drei übrigen Fachbereiche** — sollen wissen, dass es läuft, und sehen,
was herauskommt. Im Pilot sind sie nicht dabei.

Oben links: hoher Einfluss, aber mein Projekt verändert ihre Arbeit nicht.

**Die städtische IT** — bleibt für die technische Seite zuständig.

**Advellence** — die Schweizer Firma, die laut Impressum das Portal
programmiert.

**Die Betriebskommission** — Aufsichtsgremium.

**Der Volkshochschul-Verband** — stellt den KI-Rahmen, den ich nutze.

Und unten rechts der Quadrant, der mich am meisten beschäftigt hat.

**Die Kursleitungen auf Honorarbasis** — maximal betroffen, denn in der
Branche schreiben sie viele dieser Texte. In keinem Gremium sitzen sie, und
vorschreiben kann man ihnen als Honorarkräften nichts. Einen Kanal haben sie
aber doch: Arbeitnehmerähnliche Personen gelten nach dem
Personalvertretungsgesetz als Beschäftigte, der Personalrat vertritt sie mit.

**Die Teilnehmenden** — besonders in den Deutschkursen und in der
Grundbildung. Für sie ist das ganze Projekt gemacht, und sie haben keine
Stimme, in keinem Gremium und in keinem Gesetz.

Bei ihnen ist Beteiligung kein guter Stil, sondern das einzige Instrument, das
überhaupt zur Verfügung steht. Was das praktisch heißt, steht auf der nächsten
Folie.


## 11 — Widerstand

typ: einwaende
kapitel: 03 · CHANGE MANAGEMENT
titel: Wer Nein sagt,
akzent: und was darauf antwortet.
klein: ja
einwaende:
  - "Programmbereich || „Die Befunde stehen in Bausteinen, über die ich nicht entscheide.“ || Stimmt — und vor dem Pilot zu klären. Alle neun Befunde des Beispielkurses liegen in zwei Bausteinen, einer steht in 105 Kursen."
  - "Kursleitung auf Honorarbasis || „Noch eine Aufgabe, für die es keine Unterrichtseinheit gibt.“ || Geprüft wird im Programmbereich, am eingegangenen Text. Rückmeldung ja — keine Pflicht, kein Werkzeug, kein Nachweis."
  - "Redaktion des Programmhefts || „Verständlicher heißt länger, und ich habe eine feste Seitenzahl.“ || Geprüft wird der Text im Portal. Dort gibt es keine Seitenzahl, und das Heft verweist ohnehin dorthin."
  - "Personalrat || „Eine technische Einrichtung. Das braucht unsere Zustimmung.“ || Richtig, und zwar vorher. § 78 HPVG knüpft an die Eignung zur Überwachung, nicht an die Absicht."
callout: Betroffene zu Beteiligten machen — hier heißt das: entscheiden, bevor geschult wird.
calloutsub: Drei der vier Einwände sind keine Kommunikationsaufgabe, sondern eine offene Entscheidung.
quellen:
  - "Häufigkeit der Bausteine: eigene Auszählung im Kursplan der vhs"
  - "§ 78 Abs. 1 Nr. 5 und § 66 HPVG, Fassung 2023 | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"

### NOTIZ

Jetzt zum Widerstand. Der Unterricht nennt vier Ursachen: Verlustangst,
Unsicherheit, Gewohnheit und fehlende Perspektive. Ich zeige sie nicht als
Liste, sondern an vier Rollen von der Folie davor — jede sagt Nein aus einem
anderen Grund.

Der Programmbereich zuerst. Sein Einwand: Die Befunde stehen in Bausteinen,
über die ich nicht entscheide. Ich habe das nachgezählt, und es stimmt
vollständig. Der Beispielkurs, den ich gleich vorführe, hat keinen eigenen
Satz. Er besteht restlos aus zwei Bausteinen, dem Anmeldehinweis und der
Niveaubeschreibung. Alle neun Befunde liegen dort, und der Anmeldehinweis
steht wortgleich in hundertfünf Kursen. Das ist Verlustangst in ihrer echten
Form: nicht Angst vor der Maschine, sondern die Aussicht, für etwas gemessen
zu werden, das man nicht ändern darf. Meine Antwort ist deshalb keine
Schulung, sondern eine Zuständigkeitsfrage, die vor dem Pilot geklärt wird.
Nebenbei ist es die gute Nachricht: ein Baustein in Ordnung gebracht, und
hundertfünf Kurse sind es mit.

Die Kursleitung auf Honorarbasis. Noch eine Aufgabe, für die es keine
Unterrichtseinheit gibt — das ist fehlende Perspektive, und bei dieser Gruppe
schärfer als bei allen anderen, weil ihre Abrechnungseinheit die
Unterrichtsstunde ist. Textarbeit kommt darin nicht vor. Meine Antwort ist der
Zuschnitt: Geprüft wird im Programmbereich, an dem Text, der dort eingeht. Das
schützt auch den Status. Verbindliche Regeln, Schulungspflicht und ein
Protokoll je Text sind genau die Merkmale, aus denen das Bundessozialgericht
im Herrenberg-Urteil eine Eingliederung in den Betrieb hergeleitet hat.

Die Redaktion des Programmhefts. Ihr Einwand ist der, an den ich zuletzt
gedacht hätte: Verständlicher heißt länger, und ich habe eine feste
Seitenzahl. Das ist Gewohnheit, aber nicht als Trägheit, sondern als
konkurrierendes Regelwerk. Diese Redaktion kürzt beruflich, ein Werkzeug, das
Erklärungen verlangt, arbeitet gegen ihren Auftrag. Meine Antwort trennt die
Medien: Geprüft wird der Text im Portal, und dort gibt es keine Seitenzahl.

Und der Personalrat. Der Paragraf knüpft die Mitbestimmung an technische
Einrichtungen, die zur Überwachung geeignet sind — geeignet, nicht verwendet.
Eine Zusage, nicht nach Urheber auszuwerten, räumt den Tatbestand also gar
nicht aus, und etwas vorzulegen ist keine Zustimmung. Das Instrument nennt der
Paragraf selbst: die Dienstvereinbarung, mit Zweckbindung, Zugriffskreis und
Löschfrist. Sie ist die Voraussetzung für alles Weitere und kommt auf den
nächsten beiden Folien noch zweimal vor.

Der Satz unten: Betroffene zu Beteiligten machen. Hier heißt das konkret,
entscheiden, bevor geschult wird. Drei der vier Einwände sind überhaupt keine
Kommunikationsaufgabe. Wer die Bausteinfreigabe, die Zuständigkeit und den
Umgang mit den Protokollen offenlässt und stattdessen eine Schulung ansetzt,
schult gegen einen Widerstand, der berechtigt ist. Der vierte, der der
Redaktion, ist einer — und er wird beantwortet, indem man zugibt, dass sie mit
dem fehlenden Prüfschritt die ganze Zeit recht hatte.


## 12 — Timeline

typ: timeline
kapitel: 03 · CHANGE MANAGEMENT
titel: Drei Monate,
akzent: drei Stränge.
klein: ja
monate: Monat 1 | Monat 2 | Monat 3
tortitel: Vorher
tor: Zustimmung des Personalrats, als Dienstvereinbarung
strang1: Technische Implementation || Setup > Assistent anlegen, Regeln an echten Texten schärfen || Pilot > Ein Programmbereich, nur neu entstehende Texte || Rollout > Vorbereitet, freigegeben erst nach der Nachmessung
strang2: Kommunikation || Ankündigung > Erst die Dienstvereinbarung, dann die Bekanntgabe || Training > Pflicht nach Artikel 4 KI-Verordnung, für alle, die bedienen || Support > Feste Sprechstunde, nicht auf Zuruf
strang3: Change || Vorbereitung > Betroffene befragen, Bausteinfreigabe klären || Einbindung > Der Bereich wählt die scharfen Regeln, dazu der Quick Win || Begleitung > Nachmessung, dann Entscheidung
callout: Der Kommunikationsstrang beginnt nicht aus Höflichkeit vor dem technischen, sondern weil er muss.
calloutsub: Ohne die Dienstvereinbarung darf der Assistent nicht angelegt werden — deshalb steht sie links vor Monat 1 und nicht in ihm.
quellen:
  - "§ 78 Abs. 1 Nr. 5 und § 66 HPVG, Fassung 2023 | https://www.gew-hrwm.de/fileadmin/user_upload/wiz/downloads/20230427_HEFT_HPVG_2023_FERTIG_BUCHVERSION_v3_online-Version_v3.pdf"
  - "KI-Verordnung (EU) 2024/1689, Artikel 4 | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=CELEX%3A32024R1689"

### NOTIZ

Der Zeitplan, drei Monate, drei Stränge, die neun Phasen aus der
Aufgabenstellung als Überschrift jeder Zelle. Die Zellen könnt ihr mitlesen,
ich hebe drei Dinge heraus.

Erstens das blaue Feld links. Es steht in keinem der drei Monate, sondern
davor, weil die Dienstvereinbarung ein Tor ist und keine Parallelaufgabe. Im
ersten Monat sähe es aus, als könne daneben schon der Assistent angelegt
werden. Das darf er nicht.

Zweitens das Training im zweiten Monat. Das ist keine Kür, sondern Pflicht:
Artikel vier der KI-Verordnung verlangt seit Februar zweitausendfünfundzwanzig
ausreichende KI-Kompetenz, und zwar für das Personal und für alle, die im
Auftrag mit Betrieb und Nutzung befasst sind. Deshalb steht in der Zelle nicht
Personal, sondern alle, die bedienen. Wer nicht bedient, braucht die Schulung
nicht — das ist der Grund, warum die Kursleitungen aus dieser Kette bleiben.

Und drittens die Reihenfolge im Change-Strang: erst fragen, dann handeln. Die
Freigabe der Textbausteine steht deshalb im ersten Monat und nicht im zweiten,
sonst läuft der Quick Win auf eine Zuständigkeit, die niemand hat.


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
calloutsub: Gemessen an 489 Kursen. Was die vhs als „neu“ zählt, ist offen — im Grenzfall 220 Stunden, immer noch unter dem Einwand.
quellen: eigene Erhebung — alle Szenarien und Einschränkungen in der Dokumentation zur Abgabe

### NOTIZ

Die ersten dreißig Tage, und das ist keine Aufzählung, sondern eine
Reihenfolge: Jeder Schritt bedingt den nächsten.

Die Dienstvereinbarung zuerst, aus dem Grund von eben. Dann einen
Programmbereich gewinnen, und zwar freiwillig — ein zugewiesener liefert kein
belastbares Ergebnis, sondern nur Erfüllung. Dann die Freigabe der Bausteine,
sonst trifft der Quick Win auf niemanden. Und erst als viertes das Technische,
den Assistenten anlegen.

Rechts die Zahlen, denn der häufigste Einwand lautet, das koste zu viel Zeit.
Er rechnet so: fünftausendachthundert Veranstaltungen, drei Minuten pro Text,
zweihundertneunzig Stunden im Jahr. Diese Rechnung unterstellt, dass jede
Veranstaltung einen eigenen Text hat. Hat sie nicht. Vierundfünfzig Prozent
der Kurse teilen ihren Text mit mindestens einem anderen, und nur rund zehn
Prozent der Angebote sind je Semester neu. Übrig bleiben ungefähr sechshundert
Texte und damit neunundzwanzig Stunden. Im Pilot sind es vier.

Die größte Unsicherheit steht unten: Was die vhs als neues Angebot zählt, ist
nicht dokumentiert. Im Grenzfall wären es zweihundertzwanzig Stunden — immer
noch unter dem Einwand, aber die Zahl gehört im Pilot gemessen.


## 14 — Erfolgsmessung und Risiken

typ: tabelle
kapitel: 03 · ERFOLGSMESSUNG
titel: Woran man merkt,
akzent: ob es gewirkt hat.
klein: ja
kompakt: ja
spalten: Kennzahl | heute | Ziel nach 3 Monaten | gemessen mit
zeilen:
  - "Texte mit mindestens einem Befund | 58 % | ! unter 25 % | eigenes Messskript, unverändert"
  - "Neue Texte im Pilotbereich geprüft | 0 | + alle | Protokoll des Werkzeugs"
  - "Deutschkurse A1/A2 mit Wörtern über Niveau | 6 von 6 | ! höchstens 2 von 6 | eigenes Messskript, unverändert"
  - "Teilnehmende, die die Beschreibung verstanden haben | nicht erhoben | + Ausgangswert und Trend | Kurzbefragung am Kursende, freiwillig und vergütet"
risiken:
  - "Die Protokolle werden gegen das Unternehmen verwendet. Sie belegen datiert, was vorher nur unbemerkt war. > Zweckbindung, Zugriffskreis und Löschfrist in dieselbe Dienstvereinbarung — und zu jedem Befundstand ein Abstellplan mit Datum."
callout: Die Nachmessung läuft mit demselben eingefrorenen Skript wie die Ausgangsmessung. Über die Methode kann später niemand streiten.
quellen: Ausgangsmessung mit eigenem Messskript, Stichprobe vom 28.07.2026 · Wirtschaftlichkeit an 489 Kursen

### NOTIZ

Und woran würde man merken, ob es gewirkt hat?

Vier Kennzahlen mit Ausgangswert und Ziel. Die Befundquote soll von
achtundfünfzig Prozent unter fünfundzwanzig fallen. Alle neuen Texte im
Pilotbereich sollen geprüft sein. Und von den sechs Deutschkursen auf A1 und
A2, die heute alle Wörter über dem Niveau ihrer Zielgruppe enthalten, sollen
höchstens noch zwei betroffen sein.

Die vierte Zeile ist mir wichtig, weil die ersten drei nur den Text messen und
nicht die Wirkung. Deshalb frage ich die Teilnehmenden selbst. Nicht über
einen Fragebogen auf der Website, denn den füllt genau die Zielgruppe nicht
aus, um die es geht. Sondern im Kurs, am Ende einer Stunde, in einfacher
Sprache.

Diese Befragung ist freiwillig und wird vergütet. Sonst wäre sie eine neue
Aufgabe ohne Bezahlung, und das ist bei Honorarkräften genau das Problem von
der Widerstandsfolie.

In der letzten Spalte steht, womit gemessen wird. Die Nachmessung läuft mit
demselben Skript wie die Ausgangsmessung, und das Skript ist dafür
eingefroren. Wäre es zwischendurch verbessert worden, wüsste man hinterher
nicht, ob die Texte besser geworden sind oder nur die Messung anders.

Unten steht das Risiko, das ich zuerst übersehen habe und das unangenehmste
ist: Die Protokolle können gegen das Unternehmen verwendet werden. Sie belegen
datiert und zitierbar, dass Texte Kriterien verletzen, die das Haus sich
freiwillig gibt. Wer laut Impressum persönlich für die Inhalte verantwortlich
ist, hat nach dem Pilot eine Kenntnis, die er vorher nicht hatte. Deshalb
gehören die Protokolle in dieselbe Dienstvereinbarung, und deshalb gehört zu
jedem Befundstand ein Abstellplan mit Datum. Ein dokumentierter Mangel mit
Plan steht besser da als ungeprüfter Bestand — aber nur, wenn der Plan
wirklich existiert.


## 15 — Schlussfolie

typ: schluss
bild: bilder/15-durchgang.png
bildnotiz: Dieselbe Wand wie auf der Titelfolie, der Durchgang jetzt begehbar und hell.
titel: Danke für die Aufmerksamkeit.
link: klartext-vhs.henrikheil.net
linktext: Probiert es selbst aus, an einem echten Kurstext aus dem Portal:
fussl: PROJEKT KLARTEXT · VHS FRANKFURT
fussr: HENRIK HEIL

### NOTIZ

Ich habe ein reales Unternehmen analysiert, einen Prozess gefunden, in dem
niemand etwas falsch macht und trotzdem etwas fehlt, und ich habe den Zustand
gemessen statt geschätzt.

Der System-Prompt selbst ist an einem Nachmittag geschrieben. Das ist meine
eigentliche Lehre aus diesem Projekt. Die Arbeit steckt in allem, was ihn
möglich macht: zu wissen, für wen ein Text ist, zu wissen, was Pflicht ist und
was Anspruch, und einen Weg zu finden, auf dem die Menschen, die diese Texte
schreiben, das Werkzeug nicht als Kontrolle erleben.

Danke für die Aufmerksamkeit. Die Adresse steht oben, dort läuft der Prototyp
weiter — mit dem Prompt in allen Fassungen und den Läufen, die ihr gesehen
habt. Jetzt gerne eure Fragen.
