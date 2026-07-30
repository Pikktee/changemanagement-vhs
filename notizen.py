#!/usr/bin/env python3
"""
KLARTEXT — Vortragswerkzeug.

Erzeugt zwei eigenstaendige Seiten fuer den Vortrag:

    ausgabe/notizen.html   Referentennotizen, eine Folie je Bildschirm,
                           entworfen fuer einen zweiten Monitor im Hochformat
    ausgabe/vortrag.html   nur die Folie als Bild, formatfuellend, schwarz

    python3 notizen.py

Beide Seiten sind an keiner Abgabe beteiligt. Sie gehen weder in die
Praesentation noch in die Dokumentation ein und werden von build.py nicht
angefasst. folien.md wird ausschliesslich gelesen.

Bedienung (auf beiden Seiten gleich):
    vor      Pfeil rechts, Pfeil runter, Leertaste, Bild ab
    zurueck  Pfeil links, Pfeil hoch, Bild auf
    Anfang   Pos1        Ende   Ende
    Schrift  + und -  (nur Notizen, in Schritten von 5 Prozent,
                       gemerkt in localStorage)
    Ein Klick blaettert ebenfalls vor.

Direkt anspringen laesst sich eine Folie mit ?folie=5 in der Adresse. Das
zaehlt nicht als Blaettern, der Hinweis in der Fusszeile bleibt stehen.

Praesentations-Fernbedienungen senden PageUp und PageDown; beide sind
belegt.

WICHTIG — die Kopplung braucht denselben Ursprung:
    Die beiden Seiten reden ueber einen BroadcastChannel miteinander.
    BroadcastChannel verlangt gleiche Herkunft (Protokoll, Host, Port).
    Ueber file:// ist die Herkunft "null", und Chrome laesst den Kanal dort
    nicht zu — die Seiten blaettern dann jede fuer sich. Beide Fenster
    muessen deshalb ueber denselben lokalen Server geoeffnet werden:

        cd abschlussprojekt-vhs && python3 -m http.server 8795
        http://localhost:8795/ausgabe/notizen.html
        http://localhost:8795/ausgabe/vortrag.html

    Der Hinweis steht zusaetzlich sichtbar in der Fusszeile der Notizseite
    und verschwindet, sobald zum ersten Mal geblaettert wird.

Aufbau der Notizseite:
    Kopf   Foliennummer, Folientitel, darunter klein die naechste Folie
    Text   die Notiz, Absaetze durch Leerzeilen getrennt
    Fuss   der Hinweis auf den Server

Die Notizen stecken als JSON in der Datei selbst, es wird zur Laufzeit
nichts nachgeladen. Nur die Folienbilder der Vortragsseite kommen als
Datei dazu (ausgabe/folie-NN.png), die liegen daneben.

Die Schriftgroesse der Notiz wird im Browser gesucht, nicht hier
geschaetzt: Der Text wird so lange verkleinert, bis er in das Fenster
passt (Halbierungssuche zwischen MIN und MAX). Reicht MIN nicht, darf
diese eine Folie scrollen — abschneiden waere der schlimmere Fehler.

Gemessen bei 1080x1920: alle 15 Folien passen ohne Scrollen, die Groessen
liegen zwischen 21px (Folie 5, 612 Woerter) und 56px (Folie 15), der Rest
zum unteren Rand zwischen 5 und 149 Pixeln.
"""

import html
import importlib.util
import json
import re
from pathlib import Path

WURZEL = Path(__file__).parent
QUELLE = WURZEL / "folien.md"
AUS = WURZEL / "ausgabe"


def lade_build():
    """parse() aus build.py holen, statt den Parser ein zweites Mal zu
    schreiben. Sonst driften die beiden Leser auseinander."""
    spec = importlib.util.spec_from_file_location("klartext_build", WURZEL / "build.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


# --------------------------------------------------------------------------
# Notiztext aufbereiten
# --------------------------------------------------------------------------

def absaetze(notiz):
    """Notiz in Absaetze zerlegen.

    folien.md ist hart auf rund 76 Zeichen umbrochen. Diese Umbrueche sind
    ein Artefakt der Quelldatei und keine Absatzgrenzen — innerhalb eines
    Blocks werden die Zeilen deshalb mit einem Leerzeichen zusammengezogen
    und der Browser bricht selbst um. Getrennt wird nur an Leerzeilen.

    (build.py macht das anders herum: dort wird jede Quellzeile ein eigener
    Absatz. Fuer die Notizen der PowerPoint ist das richtig, hier nicht.)
    """
    roh = re.split(r"\n\s*\n", notiz.strip())
    fertig = []
    for block in roh:
        text = " ".join(z.strip() for z in block.splitlines() if z.strip())
        if text:
            fertig.append(text)
    return fertig


def fett(text):
    """HTML-escapen, **fett** in <strong> uebersetzen.

    Auf Folie 10 stehen die Stakeholder-Namen so am Zeilenanfang; ohne die
    Auszeichnung verliert die Notiz dort ihre Gliederung. *kursiv* kommt in
    den Notizen nicht vor und wird bewusst nicht uebersetzt — ein einzelner
    Stern soll nicht stillschweigend verschwinden.
    """
    s = html.escape(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)


def folientitel(f):
    """Titel und Akzent zu einer Zeile verbinden. In folien.md ist der Titel
    zweiteilig ('Was zaehlt als Befund,' + 'und fuer wen.')."""
    teile = [str(f.get("titel", "")).strip(), str(f.get("akzent", "")).strip()]
    return " ".join(t for t in teile if t)


def daten(folien):
    """Die Liste, die in beide Seiten eingebettet wird."""
    liste = []
    for nr, f in enumerate(folien, 1):
        liste.append({
            "nr": nr,
            "titel": folientitel(f),
            "bild": f"folie-{nr:02d}.png",
            "text": [fett(a) for a in absaetze(f.get("notiz", ""))],
        })
    return liste


# --------------------------------------------------------------------------
# CSS
# --------------------------------------------------------------------------

# Warum dunkelblaue Flaeche und weisse Schrift:
#
# Die Notizseite steht im abgedunkelten Raum unmittelbar neben dem Beamer.
# Eine weisse Flaeche von 1080x1920 leuchtet dort den Referenten an und
# stoert im Blickfeld des Publikums. Eine dunkle Flaeche ist die
# naheliegende Wahl.
#
# DESIGN.md kennt genau eine dunkle Flaeche: --marke. Ein eigenes Grau oder
# Schwarz waere ein neuer Farbwert und damit ein Regelbruch ("Keine neuen
# Grautoene"). Auf --marke gilt: "Auf Markenflaeche gilt Weiss oder
# --auf-marke, sonst nichts." Also Weiss fuer den Text (8,84:1, AAA) und
# --auf-marke fuer die beiden Nebenrollen — Foliennummer und Ausblick auf
# die naechste Folie (6,32:1). Das ist AAA fuer grossen Text (ab 24px);
# beide Rollen sind deshalb nach unten auf 26px begrenzt und werden von der
# automatischen Verkleinerung des Textkoerpers nicht erfasst.
#
# Keine Signalfarbe. Rot und Gruen sind im System mit Bedeutung belegt und
# haben auf einer Notizseite nichts zu suchen.
#
# Die Farbwerte stehen hier ein zweites Mal, weil die Seite ohne stil.css
# auskommen muss: stil.css legt html,body hart auf 1280x720 fest und wuerde
# die Notizseite zerlegen. Diese Datei ist an keiner Abgabe beteiligt;
# pruefe-design.py liest sie deshalb nicht. Wer die Palette aendert, aendert
# sie in stil.css und traegt sie hier von Hand nach.

FARBEN = """
:root{
  --marke:#14459E;
  --auf-marke:#B9DFFA;
  --papier:#FFFFFF;
  --schrift:"Atkinson Hyperlegible Next","Helvetica Neue",Arial,sans-serif;
}
"""

CSS_NOTIZEN = FARBEN + """
*{ box-sizing:border-box; margin:0; padding:0; }

html,body{ height:100%; }

body{
  font-family:var(--schrift);
  background:var(--marke);
  color:var(--papier);
  -webkit-font-smoothing:antialiased;
  overflow:hidden;
}

/* Drei Zeilen: Kopf, Text (nimmt den Rest), Fuss. Der Textbereich ist der
   einzige, der wachsen und schrumpfen darf — min-height:0 ist noetig,
   sonst laesst Grid ihn ueber das Fenster hinauswachsen und die Messung
   im Skript findet nie einen Ueberlauf. */
.seite{
  height:100%;
  display:grid;
  grid-template-rows:auto minmax(0,1fr) auto;
  padding:3.2vmin 3.6vmin 2.4vmin;
  gap:2.2vmin;
}

/* ---------- Kopf ---------- */
.kopf{ display:flex; align-items:baseline; gap:.55em; }

.nr{
  font-size:clamp(26px, 3.4vmin, 46px);
  font-weight:700;
  color:var(--auf-marke);
  font-variant-numeric:tabular-nums;
  flex:none;
}

h1{
  font-size:clamp(26px, 3.4vmin, 46px);
  font-weight:700;
  line-height:1.15;
  letter-spacing:-0.01em;
}

.weiter{
  margin-top:.5em;
  font-size:clamp(26px, 2.4vmin, 32px);
  font-weight:400;
  color:var(--auf-marke);
}

/* ---------- Notiz ---------- */
/* --gr wird von der Halbierungssuche gesetzt. overflow bleibt hidden,
   solange der Text passt; erst wenn selbst die Untergrenze nicht reicht,
   schaltet das Skript .rollt und damit Scrollen frei. */
#notiz{
  font-size:var(--gr, 30px);
  line-height:1.42;
  overflow:hidden;
  /* Keine Silbentrennung. Sie spart Platz, aber dieser Text wird unter Druck
     vorgelesen — ein am Zeilenende zerschnittenes Wort muss das Auge erst
     wieder zusammensetzen. Der rechte Rand wird dafuer unruhiger, das ist
     der guenstigere Tausch. */
  -webkit-hyphens:none; hyphens:none;
}
#notiz.rollt{ overflow-y:auto; }
#notiz p + p{ margin-top:.62em; }
#notiz strong{ font-weight:700; }

/* ---------- Fuss ---------- */
/* Der Hinweis auf den Server steht nur, bis zum ersten Mal geblaettert
   wurde. Danach ist die Seite leer bis zum Rand. */
/* Weiss, nicht --auf-marke: die Zeile ist klein, und --auf-marke haelt auf
   --marke 6,32:1 — AAA fuer grossen Text, nicht fuer kleinen. */
.fuss{
  font-size:clamp(15px, 1.5vmin, 21px);
  color:var(--papier);
  min-height:1.4em;
}
.fuss[hidden]{ display:block; visibility:hidden; }

/* Querformat: derselbe Aufbau, nur schmalere Raender. Zerbrechen kann
   nichts, weil die Groesse ohnehin gemessen und nicht gesetzt wird. */
@media (orientation:landscape){
  .seite{ padding:2.6vmin 3vmin 2vmin; gap:1.8vmin; }
}
"""

CSS_VORTRAG = """
*{ box-sizing:border-box; margin:0; padding:0; }
html,body{ height:100%; background:#000; overflow:hidden; }
img{
  width:100%; height:100%;
  object-fit:contain;           /* nie verzerren, lieber Rand lassen */
  display:block;
}
"""


# --------------------------------------------------------------------------
# JavaScript
# --------------------------------------------------------------------------

# Gemeinsamer Teil: Kanal, Tastatur, Adresszeile.
JS_GEMEINSAM = """
const KANAL = 'klartext-vortrag';
const kanal = (() => { try { return new BroadcastChannel(KANAL); }
                       catch (e) { return null; } })();

let folie = 0;                 // 0-basiert
let geblaettert = false;

function ausAdresse(){
  const m = /[?&#]folie=(\\d+)/.exec(location.search + location.hash);
  if (m) return Math.min(FOLIEN.length, Math.max(1, parseInt(m[1], 10))) - 1;
  return 0;
}

// senden=false, wenn der Sprung selbst aus dem Kanal kam. Sonst schickt die
// Gegenseite ihn zurueck und beide springen im Kreis.
function gehe(i, senden){
  folie = Math.min(FOLIEN.length - 1, Math.max(0, i));
  zeige(folie);
  if (senden !== false && kanal) kanal.postMessage({folie: folie});
}

// Blaettern von Hand. Nur das laesst den Hinweis in der Fusszeile
// verschwinden — der erste Aufbau der Seite (auch mit ?folie=N) nicht.
function blaettern(i){
  geblaettert = true;
  gehe(i);
}

if (kanal) kanal.onmessage = e => {
  if (e.data && typeof e.data.folie === 'number') {
    geblaettert = true;
    gehe(e.data.folie, false);
  }
};

const VOR    = ['ArrowRight','ArrowDown',' ','Spacebar','PageDown'];
const ZURUCK = ['ArrowLeft','ArrowUp','PageUp','Backspace'];

// Vollbild auf Taste F. Der Browser verlangt dafuer eine Nutzeraktion, ein
// Tastendruck ist eine. F11 des Browsers tut dasselbe, ist aber auf jedem
// System anders belegt.
function vollbild(){
  const d = document;
  if (d.fullscreenElement) { d.exitFullscreen && d.exitFullscreen(); }
  else { d.documentElement.requestFullscreen && d.documentElement.requestFullscreen(); }
}

document.addEventListener('keydown', ev => {
  const k = ev.key;
  if (VOR.includes(k))          { blaettern(folie + 1); }
  else if (ZURUCK.includes(k))  { blaettern(folie - 1); }
  else if (k === 'Home')        { blaettern(0); }
  else if (k === 'End')         { blaettern(FOLIEN.length - 1); }
  else if (typeof groesser === 'function' &&
           (k === '+' || k === '=' || k === 'Add'))      { groesser(+1); }
  else if (typeof groesser === 'function' &&
           (k === '-' || k === '_' || k === 'Subtract')) { groesser(-1); }
  else if (k === 'f' || k === 'F')  { vollbild(); }
  else return;
  ev.preventDefault();
});

// Maus- und Fingerbedienung: ein Klick blaettert vor. Praktisch, wenn die
// Fernbedienung streikt. Nicht in einem Bereich, den man rollen kann —
// dort will man scrollen und nicht weiterblaettern.
document.addEventListener('click', ev => {
  if (ev.target.closest && ev.target.closest('.rollt')) return;
  blaettern(folie + 1);
});
"""

JS_NOTIZEN = """
// Untergrenze der Halbierungssuche, in px. Auf dem Zielgeraet (1080x1920)
// kommt keine Folie ihr nahe — die laengste Notiz, Folie 5 mit 612 Woertern,
// passt bei 21px. Die Grenze greift erst in kleinen Fenstern; dort rollt die
// Folie dann lieber, statt unleserlich zu werden.
const MIN = 18;
const MAX = 64;          // Obergrenze
const SPEICHER = 'klartext-notizen-nachstellung';

// Nachstellung des Referenten, in Prozent. + und - verschieben sie, der
// Wert ueberlebt einen Neustart des Browsers.
let nachstellung = 100;
try { nachstellung = parseInt(localStorage.getItem(SPEICHER), 10) || 100; }
catch (e) {}

const eNr     = document.getElementById('nr');
const eTitel  = document.getElementById('titel');
const eWeiter = document.getElementById('weiter');
const eNotiz  = document.getElementById('notiz');
const eFuss   = document.getElementById('fuss');

let letzteGroesse = 0;   // fuer die Messseite

// Groesste Schriftgroesse suchen, bei der der Text noch in den Kasten
// passt. Halbierungssuche in ganzen Pixeln: rund sieben Durchlaeufe, das
// merkt niemand. Gemessen wird scrollHeight gegen clientHeight — genau der
// Wert, der auch entscheidet, ob abgeschnitten wuerde.
function passtBei(px){
  eNotiz.style.setProperty('--gr', px + 'px');
  return eNotiz.scrollHeight <= eNotiz.clientHeight;
}

function sucheGroesse(){
  if (passtBei(MAX)) return MAX;
  let lo = MIN, hi = MAX, best = 0;
  while (lo <= hi) {
    const mitte = (lo + hi) >> 1;
    if (passtBei(mitte)) { best = mitte; lo = mitte + 1; }
    else { hi = mitte - 1; }
  }
  return best || MIN;      // 0 heisst: passt selbst bei MIN nicht
}

function einpassen(){
  eNotiz.classList.remove('rollt');
  const basis = sucheGroesse();

  // Die Nachstellung wirkt auf das gefundene Mass. Ohne sie fuellt der Text
  // den Kasten genau aus, und + und - haetten fast nie eine Wirkung — die
  // Groesse haengt ja am Platz, nicht am Geschmack. Stellt der Referent
  // groesser, als es passt, rollt die Folie. Das ist gewollt: lieber rollen
  // als abschneiden, denn ein abgeschnittener Satz faellt auf der Buehne
  // nicht auf.
  const px = Math.min(128, Math.max(10, Math.round(basis * nachstellung / 100)));
  if (!passtBei(px)) eNotiz.classList.add('rollt');
  letzteGroesse = px;
}

function zeige(i){
  const f = FOLIEN[i];
  eNr.textContent = String(f.nr).padStart(2, '0');
  eTitel.textContent = f.titel;
  const n = FOLIEN[i + 1];
  eWeiter.textContent = n ? 'Weiter: ' + n.titel : 'Letzte Folie.';
  eNotiz.innerHTML = f.text.map(p => '<p>' + p + '</p>').join('');
  eNotiz.scrollTop = 0;
  eFuss.hidden = geblaettert;
  einpassen();
  document.title = 'Notizen ' + String(f.nr).padStart(2, '0');
}

function groesser(richtung){
  nachstellung = Math.min(200, Math.max(50, nachstellung + richtung * 5));
  try { localStorage.setItem(SPEICHER, String(nachstellung)); } catch (e) {}
  einpassen();
}

// Nach einer Groessenaenderung erst messen, wenn der Umbruch steht.
//
// einpassen() sucht die Groesse ueber eine Halbierungssuche und misst dabei
// mehrfach die Hoehe des Textes. Wer ein Fenster am Rand zieht, loest
// Dutzende resize-Ereignisse aus; ohne Zusammenfassung liefe die Suche
// jedes Mal komplett durch. Ein Takt Verzoegerung plus Bildrahmen fasst sie
// zusammen und stellt zugleich sicher, dass gegen den neuen und nicht gegen
// den alten Kasten gemessen wird.
let nachlauf = 0;
function einpassenSpaeter(){
  clearTimeout(nachlauf);
  nachlauf = setTimeout(() => requestAnimationFrame(einpassen), 60);
}
addEventListener('resize', einpassenSpaeter);
// Beim Wechsel ins Vollbild aendert sich die Fensterhoehe; das Ereignis kommt
// je nach Browser vor oder nach dem Neuaufbau. Der Beobachter greift in
// beiden Faellen, auch wenn resize einmal ausbleibt.
addEventListener('fullscreenchange', einpassenSpaeter);
if (window.ResizeObserver) new ResizeObserver(einpassenSpaeter).observe(document.documentElement);
document.fonts.ready.then(einpassen);

// Haken fuer die Ueberlaufmessung. Die Messseite laedt diese Datei in einen
// iframe, springt jede Folie an und liest hier ab.
// Unterkante des Textes im Kasten. scrollHeight taugt dafuer nicht: er ist
// nie kleiner als clientHeight und meldet deshalb immer 0 Rest.
function unterkante(){
  const oben = eNotiz.getBoundingClientRect().top;
  let tief = 0;
  for (const p of eNotiz.children) {
    const u = p.getBoundingClientRect().bottom - oben + eNotiz.scrollTop;
    if (u > tief) tief = u;
  }
  return Math.round(tief);
}

window.klartext = {
  gehe: i => gehe(i, false),
  anzahl: () => FOLIEN.length,
  messung: () => ({
    folie: folie + 1,
    groesse: letzteGroesse,
    inhalt: unterkante(),
    kasten: eNotiz.clientHeight,
    rest: eNotiz.clientHeight - unterkante(),
    rollt: eNotiz.classList.contains('rollt'),
    fett: eNotiz.querySelectorAll('strong').length,
    absaetze: eNotiz.querySelectorAll('p').length
  })
};

gehe(ausAdresse(), false);
"""

JS_VORTRAG = """
const eBild = document.getElementById('bild');

function zeige(i){
  const f = FOLIEN[i];
  eBild.src = f.bild;
  eBild.alt = 'Folie ' + f.nr + ': ' + f.titel;
  document.title = 'Folie ' + String(f.nr).padStart(2, '0');
}

// Alle Folienbilder einmal vorladen, damit beim Blaettern kein schwarzer
// Zwischenzustand entsteht.
FOLIEN.forEach(f => { const v = new Image(); v.src = f.bild; });

window.klartext = { gehe: i => gehe(i, false), anzahl: () => FOLIEN.length };

gehe(ausAdresse(), false);
"""


# --------------------------------------------------------------------------
# Seiten zusammensetzen
# --------------------------------------------------------------------------

# Das ist der einzige Text, der auf dem Bildschirm erscheint und deshalb in
# vollstaendiger Rechtschreibung stehen muss.
HINWEIS_ANZEIGE = ("Kopplung nur über den lokalen Server: Beide Fenster unter "
                   "„http://localhost/…“ öffnen, nicht als Datei. Weiter mit "
                   "Pfeiltaste, Leertaste oder Bild ab.")


def seite(titel, css, js, koerper, liste):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titel}</title>
<link rel="stylesheet" href="../schriften/schriften.css">
<style>{css}</style>
</head>
<body>
{koerper}
<script>
const FOLIEN = {json.dumps(liste, ensure_ascii=False)};
</script>
<script>{JS_GEMEINSAM}</script>
<script>{js}</script>
</body>
</html>
"""


def baue():
    build = lade_build()
    folien = build.parse(QUELLE.read_text(encoding="utf-8"))
    liste = daten(folien)

    koerper_notizen = f"""<div class="seite">
  <header>
    <div class="kopf"><span class="nr" id="nr"></span><h1 id="titel"></h1></div>
    <p class="weiter" id="weiter"></p>
  </header>
  <div id="notiz"></div>
  <p class="fuss" id="fuss">{html.escape(HINWEIS_ANZEIGE)}</p>
</div>"""

    (AUS / "notizen.html").write_text(
        seite("KLARTEXT — Referentennotizen", CSS_NOTIZEN, JS_NOTIZEN,
              koerper_notizen, liste), encoding="utf-8")

    (AUS / "vortrag.html").write_text(
        seite("KLARTEXT — Folien", CSS_VORTRAG, JS_VORTRAG,
              '<img id="bild" src="" alt="">', liste), encoding="utf-8")

    laengste = max(liste, key=lambda f: sum(len(p) for p in f["text"]))
    print(f"notizen.py: {len(liste)} Folien geschrieben")
    print(f"  ausgabe/notizen.html   laengste Notiz: Folie {laengste['nr']}, "
          f"{sum(len(p.split()) for p in laengste['text'])} Woerter")
    print("  ausgabe/vortrag.html")
    print("  Beide ueber den lokalen Server oeffnen, sonst koppeln sie nicht:")
    print("    http://localhost:8795/ausgabe/notizen.html")
    print("    http://localhost:8795/ausgabe/vortrag.html")


if __name__ == "__main__":
    baue()
