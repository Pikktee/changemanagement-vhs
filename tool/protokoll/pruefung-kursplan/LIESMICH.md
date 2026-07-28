# Läufe zur Prüfung des Kursplans

Diese Läufe sind am 28.07.2026 beim Umbau des Prototyps auf den vollständigen
Kursplan entstanden. Sie belegen, dass die Kernfälle mit den neu abgerufenen
Texten dieselben Ergebnisse liefern wie mit der alten Stichprobe — der
Eingabetext ist bei `4074-74` und `4213-40` byteidentisch, die Prüfsumme des
Prompts ebenfalls.

Sie liegen in diesem Unterordner und nicht daneben, weil `dokument.py` für
`{{PROTOKOLL:<nummer>:...}}` den **jüngsten** Lauf einer Kursnummer aus
`protokoll/` zieht. Läge der Prüflauf dort, stünde er im PDF der Abgabe 2
anstelle des dokumentierten Laufs, und der Fließtext mit „sieben
Niveaubefunde" passte nicht mehr zum abgedruckten Beispiel. Der Unterordner
wird von der Suche nicht erfasst.

| Datei | Kurs | Befunde | davon NIVEAU |
|---|---|---|---|
| `20260728-224458-4074-74.json` | DaF A2.2, strenger Fall | 10 | 5 |
| `20260728-224619-4213-40.json` | Englisch A1.1, Gegenprobe | 7 | 0 |
| `20260728-222836-0107-18.json` | Vortrag Stresemann, beliebiger Fall | 6 | 0 |

Die fünf Niveaubefunde bei `4074-74` gegenüber sieben im dokumentierten Lauf
sind die bekannte Streuung des Modells, nicht eine Folge der neuen Kursdaten:
Bei gleichem Text und gleichem Prompt liegen die bisherigen Läufe dieses Kurses
zwischen null und acht Niveaubefunden. Die Aussage der Gegenprobe bleibt
unberührt — der Englischkurs hat null.
