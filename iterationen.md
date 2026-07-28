# Iterationshistorie des System-Prompts

Dokumentiert jede Fassung des Prompts, den Anlass der Änderung und die
Begründung. Technisch nachvollziehbar über `git log --follow system-prompt.md`.

Diese Datei wird fortgeschrieben, während der Prompt an echten Kurstexten aus
`daten/vhs-stichprobe-60.json` erprobt wird. Sie ist bewusst auch dort ehrlich,
wo eine Fassung fehlerhaft war.

---

## v0.1 · 28.07.2026, 19:30 · Erste Fassung

Aufgebaut nach der geforderten Struktur ROLLE, AUFGABE, FORMAT, GRENZEN,
KONTEXT, REGELN.

Wesentliche Entscheidungen dieser Fassung:

**Zielgruppenbestimmung als erster Arbeitsschritt.** Die AUFGABE zwingt das
Modell, vor jeder Prüfung festzuhalten, wer den Text liest. Ohne diesen Schritt
prüft es gegen einen allgemeinen Lesbarkeitsmaßstab, und genau das erzeugt den
Fehler, den das Projekt vermeiden will: Ein Englischkurs für Deutschsprachige
wird beanstandet, ein Deutschkurs auf A2 durchgewinkt.

**Zwei Fälle statt eines Maßstabs.** Kurse, die Deutsch vermitteln, werden
strenger geprüft als Kurse, die etwas anderes vermitteln. Das ist die
inhaltliche Kernregel des ganzen Werkzeugs.

**Trennung von PFLICHT und EMPFEHLUNG.** Jeder Befund wird gekennzeichnet, ob
er aus WCAG Stufe A oder AA folgt und damit rechtlich gefordert ist, oder aus
Stufe AAA beziehungsweise dem Hausstandard. Grund: Ein Werkzeug, das
Pflichtverstöße und Stilfragen gleich behandelt, verliert nach zwei Wochen die
Glaubwürdigkeit bei der Redaktion.

**„Bewertet Texte, niemals Personen" unter GRENZEN.** Diese Zeile hat zwei
Funktionen. Sie hält das System aus Anhang III Nummer 3 der KI-Verordnung
heraus, weil die dortigen Hochrisikotatbestände sämtlich natürliche Personen
als Bezugsobjekt haben. Und sie ist die Antwort auf die Mitbestimmungsfrage
des Personalrats.

**Namen entfernen unter REGELN.** Kursbeschreibungen enthalten die Namen der
Kursleitungen. Sie gehen in die Eingabe ein und haben in der Ausgabe nichts zu
suchen.

**Fremdanweisungen als Befund.** Enthält ein geprüfter Text eine Anweisung an
das Modell, wird sie nicht befolgt, sondern gemeldet. Der Prüftext ist
Material, keine Aufgabe.

---

## v1 · 28.07.2026, 20:10 · Referenzwortschatz statt Verweis

**Anlass.** Beim Gegenlesen der eigenen Fassung fiel auf, dass der Prompt eine
Behauptung aufstellt, die er nicht einlöst.

**Was falsch war.** Unter KONTEXT stand sinngemäß: Der Maßstab für das
Sprachniveau sind die veröffentlichten Wortlisten des Goethe-Instituts und des
Deutsch-Tests für Zuwanderer, das Niveau werde nicht frei geschätzt. Im Prompt
stand aber nur der **Verweis** auf diese Listen, nicht ihr Inhalt. Ein
Sprachmodell kann nicht gegen eine Liste prüfen, die es nicht hat. Faktisch
schätzte es weiterhin frei, während der Prompt das Gegenteil behauptete.

Das ist derselbe Fehler, den das Projekt anderen Werkzeugen vorwirft: eine
Bewertung ohne belastbaren Bezugspunkt.

**Was geändert wurde.**

1. Der Abschnitt „Referenz für das Sprachniveau" heißt jetzt
   „Referenzwortschatz" und enthält den Platzhalter `{{WORTLISTE_A1}}`, der
   beim Laden durch den tatsächlichen Wortschatz des Goethe-Zertifikats A1
   ersetzt wird, rund 650 Einträge.
2. Die Anwendungsregel wurde konkretisiert: Ein Inhaltswort, das nicht in der
   Liste steht und sich nicht durch Wortbildung erschließen lässt, liegt
   oberhalb von A1. Funktionswörter, Eigennamen und Kursbezeichnungen sind
   ausgenommen.
3. Neu ist eine Ehrlichkeitsregel: Fehlt die Liste zur Laufzeit, muss das
   Modell unter GESAMT ausdrücklich vermerken, dass ohne Referenz geprüft
   wurde und die Niveau-Befunde Schätzungen sind.
4. Die Begründung eines Niveau-Befunds muss das konkrete Wort nennen, nicht
   nur „zu schwer".

**Warum Punkt 3 wichtig ist.** Die Alternative wäre gewesen, den Ausfall der
Liste stillschweigend zu tolerieren. Dann sähe die Ausgabe in beiden Fällen
gleich aus, obwohl sie unterschiedlich belastbar ist. Ein Befund ohne Beleg ist
eine Behauptung und muss als solche kenntlich sein.

---

## Offen für die nächsten Fassungen

Erprobung an echten Texten steht aus. Erwartete Prüfpunkte:

- Erkennt der Prompt Textbausteine zuverlässig, oder braucht es dafür einen
  eigenen Eingabemodus?
- Ist die Grenze von 25 beziehungsweise 15 Wörtern je Satz brauchbar, oder
  erzeugt sie zu viele Befunde bei ohnehin verständlichen Sätzen?
- Wie verhält sich das Modell bei Kursen ohne Niveauangabe?
- Bleibt die Ausgabe über mehrere Durchläufe desselben Textes stabil genug,
  damit die Redaktion ihr traut?
