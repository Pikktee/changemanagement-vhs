#!/usr/bin/env python3
"""
KLARTEXT — Build.

Liest folien.md, rendert jede Folie als HTML, schiesst sie mit headless Chrome
als PNG und packt alles in eine PPTX mit Referentennotizen sowie ein PDF.

    python3 build.py            # alles bauen
    python3 build.py --schnell  # nur HTML, ohne Chrome (fuer Layout-Checks)
    python3 build.py --nur 3,7  # nur Folie 3 und 7 neu schiessen

Format von folien.md siehe README-FOLIEN.md.
"""

import html
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WURZEL = Path(__file__).parent
QUELLE = WURZEL / "folien.md"
AUS = WURZEL / "ausgabe"
STIL = WURZEL / "stil.css"
PORT = 8791

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Sprechtempo fuer die Zeitschaetzung: Woerter pro Minute, ruhiger Vortrag
WPM = 125


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------

def entkleide(wert):
    """Umschliessende Anfuehrungszeichen entfernen. Sie sind optional und
    dienen nur dazu, Werte mit Doppelpunkt eindeutig zu machen."""
    w = wert.strip()
    if len(w) >= 2 and w[0] == w[-1] and w[0] in ('"', "'"):
        return w[1:-1].strip()
    return w


def parse(text):
    """Zerlegt folien.md in eine Liste von Folien-Dicts."""
    folien = []
    aktuell = None
    modus = None          # None | "kopf" | "notiz"
    liste_key = None

    for nr, zeile in enumerate(text.splitlines(), 1):
        roh = zeile.rstrip()

        # Neue Folie
        if roh.startswith("## "):
            if aktuell:
                folien.append(aktuell)
            aktuell = {"_titel_kommentar": roh[3:].strip(), "_zeile": nr, "notiz": []}
            modus, liste_key = "kopf", None
            continue

        if aktuell is None:
            continue      # Vorspann vor der ersten Folie wird ignoriert

        # Notizblock
        if roh.strip().upper() in ("### NOTIZ", "### NOTIZEN"):
            modus, liste_key = "notiz", None
            continue

        if modus == "notiz":
            aktuell["notiz"].append(roh)
            continue

        # Kopfbereich
        if not roh.strip():
            liste_key = None
            continue

        if roh.lstrip().startswith("- ") and liste_key:
            aktuell[liste_key].append(entkleide(roh.lstrip()[2:]))
            continue

        m = re.match(r"^([a-zA-ZäöüÄÖÜ_][\w\-äöüÄÖÜß]*)\s*:\s*(.*)$", roh)
        if m:
            key, wert = m.group(1).strip(), entkleide(m.group(2))
            if wert == "":
                aktuell[key] = []
                liste_key = key
            else:
                aktuell[key] = wert
                liste_key = None
        else:
            raise SyntaxError(
                f"folien.md Zeile {nr}: verstehe ich nicht.\n  >>> {roh}\n"
                f"  Erwartet: 'schluessel: wert', '- Listenpunkt', '## Neue Folie' "
                f"oder '### NOTIZ'."
            )

    if aktuell:
        folien.append(aktuell)

    for f in folien:
        f["notiz"] = "\n".join(f["notiz"]).strip()
    return folien


# --------------------------------------------------------------------------
# Hilfen fuer die Ausgabe
# --------------------------------------------------------------------------

def e(s):
    """HTML-escapen, aber **fett** und *kursiv* durchlassen."""
    s = html.escape(str(s or ""))
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", s)
    return s


def kopf(f, seite, gesamt):
    return f"""<div class="head">
  <div class="mark"><span class="sq"></span><span class="w">KLARTEXT</span></div>
  <div class="sec">{e(f.get('kapitel',''))}</div>
  <div class="pg">{seite:02d} / {gesamt:02d}</div>
</div>
<div class="headrule"></div>"""


def fuss(f):
    links = f.get("fussl", "vhs Frankfurt · Projekt KLARTEXT")
    rechts = f.get("fussr", "Henrik Heil · cimdata 2026")
    return f'<div class="foot"><span>{e(links)}</span><span>{e(rechts)}</span></div>'


def h1(f):
    t = e(f.get("titel", ""))
    if f.get("akzent"):
        t += f' <span class="g">{e(f["akzent"])}</span>'
    klasse = " klein" if f.get("klein") else ""
    out = f'<h1 class="{klasse.strip()}">{t}</h1>'
    if f.get("lede"):
        out += f'<p class="lede">{e(f["lede"])}</p>'
    return out


def callout(f):
    if not f.get("callout"):
        return ""
    kl = f'<span class="kl">{e(f["calloutsub"])}</span>' if f.get("calloutsub") else ""
    return f'<div class="callout">{e(f["callout"])}{kl}</div>'


def quellen(f):
    if not f.get("quellen"):
        return ""
    q = f["quellen"]
    q = " · ".join(q) if isinstance(q, list) else q
    return f'<div class="quellen">Quellen: {e(q)}</div>'


# --------------------------------------------------------------------------
# Folientypen
# --------------------------------------------------------------------------

def t_panel(f, seite, gesamt, schluss=False):
    sub = f'<p class="sub">{e(f["untertitel"])}</p>' if f.get("untertitel") else ""
    titel = e(f.get("titel", ""))
    if f.get("akzent"):
        titel += f' <span class="g">{e(f["akzent"])}</span>'
    return f"""<div class="panel">
  <div class="mark"><span class="sq"></span><span class="w">KLARTEXT</span></div>
  <div class="spacer"></div>
  <div class="rule"></div>
  <h1>{titel}</h1>
  {sub}
  <div class="spacer"></div>
  <div class="pfoot">
    <span>{e(f.get('fussl','ABSCHLUSSPROJEKT · CHANGE UND KI'))}</span>
    <span>{e(f.get('fussr','CIMDATA · HENRIK HEIL · 2026'))}</span>
  </div>
</div>"""


def t_kapitel(f, seite, gesamt):
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  <div class="kap">
    <div class="kapnum">{e(f.get('nummer','01'))}</div>
    <div class="kaptxt">{h1(f)}</div>
  </div>
  {fuss(f)}
</div>"""


def t_punkte(f, seite, gesamt):
    items = []
    for p in f.get("punkte", []):
        if "||" in p:
            haupt, sub = p.split("||", 1)
            inner = f'{e(haupt.strip())}<span class="psub">{e(sub.strip())}</span>'
        else:
            inner = e(p)
        items.append(f'<div class="pkt"><div class="bar"></div>'
                     f'<div class="ptxt">{inner}</div></div>')
    call = callout(f)
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  {h1(f)}
  <div class="body">
    <div class="punkte">{''.join(items)}</div>
    {call}
  </div>
  {quellen(f)}
  {fuss(f)}
</div>"""


def t_zahlen(f, seite, gesamt):
    zs = []
    for z in f.get("zahlen", []):
        teile = [x.strip() for x in z.split("||")]
        wert = teile[0]
        lab = teile[1] if len(teile) > 1 else ""
        klassen = []
        if len(teile) > 2 and teile[2] == "warn":
            klassen.append("warn")
        # lange Werte wie "154 T€" wuerden sonst umbrechen
        if len(wert) > 8:
            klassen.append("sehrlang")
        elif len(wert) > 5:
            klassen.append("lang")
        kl = (" " + " ".join(klassen)) if klassen else ""
        zs.append(f'<div class="z"><div class="znum{kl}">{e(wert)}</div>'
                  f'<div class="zlab">{e(lab)}</div></div>')
    call = callout(f)
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  {h1(f)}
  <div class="body">
    <div class="zahlen">{''.join(zs)}</div>
    {call}
  </div>
  {quellen(f)}
  {fuss(f)}
</div>"""


def t_zweispalt(f, seite, gesamt):
    sp = []
    for i in (1, 2):
        kopfz = f.get(f"spalte{i}", "")
        punkte = f.get(f"punkte{i}", [])
        alt = " alt" if i == 2 else ""
        lis = "".join(f"<li>{e(p)}</li>" for p in punkte)
        sp.append(f'<div class="sp"><span class="spkopf{alt}">{e(kopfz)}</span>'
                  f'<ul>{lis}</ul></div>')
    call = callout(f)
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  {h1(f)}
  <div class="body">
    <div class="spalten">{''.join(sp)}</div>
    {call}
  </div>
  {quellen(f)}
  {fuss(f)}
</div>"""


def t_tabelle(f, seite, gesamt):
    kopfz = [x.strip() for x in f.get("spalten", "").split("|")]
    ths = "".join(f"<th>{e(k)}</th>" for k in kopfz)
    trs = []
    for zeile in f.get("zeilen", []):
        tds = []
        for z in [x.strip() for x in zeile.split("|")]:
            kl = ""
            if z.startswith("+"):
                kl, z = ' class="ja"', z[1:].strip()
            elif z.startswith("!"):
                kl, z = ' class="nein"', z[1:].strip()
            elif re.match(r"^[\d.,]+\s*%?$", z):
                kl = ' class="num"'
            tds.append(f"<td{kl}>{e(z)}</td>")
        trs.append(f"<tr>{''.join(tds)}</tr>")
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  {h1(f)}
  <div class="body">
    <table><thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody></table>
    {callout(f)}
  </div>
  {quellen(f)}
  {fuss(f)}
</div>"""


def t_zitat(f, seite, gesamt):
    quelle = f'<div class="quelle">{e(f["quelle"])}</div>' if f.get("quelle") else ""
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  <div class="body" style="justify-content:center">
    <div class="zitat"><div class="q">{e(f.get('zitat',''))}</div>{quelle}</div>
    {callout(f)}
  </div>
  {quellen(f)}
  {fuss(f)}
</div>"""


def t_text(f, seite, gesamt):
    abs_ = "".join(f'<p class="lede" style="font-size:19px;color:var(--ink);'
                   f'max-width:960px">{e(a)}</p>' for a in f.get("absaetze", []))
    call = callout(f)
    return f"""<div class="stage">
  {kopf(f, seite, gesamt)}
  {h1(f)}
  <div class="body">{abs_}{call}</div>
  {quellen(f)}
  {fuss(f)}
</div>"""


TYPEN = {
    "titel":     lambda f, s, g: t_panel(f, s, g),
    "schluss":   lambda f, s, g: t_panel(f, s, g, True),
    "kapitel":   t_kapitel,
    "punkte":    t_punkte,
    "zahlen":    t_zahlen,
    "zweispalt": t_zweispalt,
    "tabelle":   t_tabelle,
    "zitat":     t_zitat,
    "text":      t_text,
}


def rendere(f, seite, gesamt):
    typ = f.get("typ", "punkte")
    if typ not in TYPEN:
        raise ValueError(f"Folie {seite}: Typ '{typ}' kenne ich nicht. "
                         f"Moeglich: {', '.join(sorted(TYPEN))}")
    inner = TYPEN[typ](f, seite, gesamt)
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8">'
            f'<link rel="stylesheet" href="../stil.css"></head>'
            f'<body>{inner}</body></html>')


# --------------------------------------------------------------------------
# Ausgabe
# --------------------------------------------------------------------------

def schiesse_pngs(folien, nur=None):
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        cwd=WURZEL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1.0)
    try:
        for i, _ in enumerate(folien, 1):
            if nur and i not in nur:
                continue
            ziel = AUS / f"folie-{i:02d}.png"
            subprocess.run([
                CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=2", "--window-size=1280,720",
                f"--screenshot={ziel}",
                f"http://localhost:{PORT}/ausgabe/folie-{i:02d}.html",
            ], check=True, capture_output=True)
            print(f"  Folie {i:02d} gerendert")
    finally:
        server.terminate()


def baue_pptx(folien):
    from pptx import Presentation
    from pptx.util import Emu
    B, H = Emu(12192000), Emu(6858000)
    prs = Presentation()
    prs.slide_width, prs.slide_height = B, H
    leer = prs.slide_layouts[6]
    for i, f in enumerate(folien, 1):
        png = AUS / f"folie-{i:02d}.png"
        if not png.exists():
            print(f"  ! Folie {i:02d}: PNG fehlt, uebersprungen")
            continue
        s = prs.slides.add_slide(leer)
        s.shapes.add_picture(str(png), 0, 0, width=B, height=H)
        s.notes_slide.notes_text_frame.text = f.get("notiz", "") or "(keine Notiz)"
    ziel = AUS / "Praesentation-KLARTEXT.pptx"
    prs.save(str(ziel))
    return ziel


def baue_pdf(folien):
    from PIL import Image
    seiten = []
    for i, _ in enumerate(folien, 1):
        p = AUS / f"folie-{i:02d}.png"
        if p.exists():
            seiten.append(Image.open(p).convert("RGB"))
    if not seiten:
        return None
    ziel = AUS / "Praesentation-KLARTEXT.pdf"
    seiten[0].save(ziel, save_all=True, append_images=seiten[1:])
    return ziel


def zeit(folien):
    print("\n  Sprechzeit")
    ges = 0
    for i, f in enumerate(folien, 1):
        w = len((f.get("notiz") or "").split())
        sek = round(w / WPM * 60)
        ges += sek
        marke = "  " if sek <= 90 else " !"
        print(f"   {marke} Folie {i:02d}  {w:>4} W.  {sek//60}:{sek%60:02d}"
              f"   {f.get('_titel_kommentar','')[:40]}")
    print(f"      GESAMT      {ges//60}:{ges%60:02d} Minuten")
    if ges > 15 * 60:
        print("      ! ueber 15 Minuten, das ist zu lang")


def commit(folien):
    if not (WURZEL / ".git").exists():
        return
    subprocess.run(["git", "add", "-A"], cwd=WURZEL, capture_output=True)
    st = subprocess.run(["git", "diff", "--cached", "--name-only"],
                        cwd=WURZEL, capture_output=True, text=True)
    if not st.stdout.strip():
        return
    subprocess.run(
        ["git", "commit", "-q", "-m", f"Build: {len(folien)} Folien"],
        cwd=WURZEL, capture_output=True)
    print("  Stand versioniert")


# --------------------------------------------------------------------------

def main():
    schnell = "--schnell" in sys.argv
    nur = None
    if "--nur" in sys.argv:
        nur = {int(x) for x in sys.argv[sys.argv.index("--nur") + 1].split(",")}

    if not QUELLE.exists():
        sys.exit(f"Fehlt: {QUELLE}")

    try:
        folien = parse(QUELLE.read_text(encoding="utf-8"))
    except SyntaxError as ex:
        sys.exit(f"\nFEHLER in folien.md\n\n{ex}\n")

    if not folien:
        sys.exit("folien.md enthaelt keine Folie (Zeile mit '## ' beginnen).")

    AUS.mkdir(exist_ok=True)
    print(f"\nKLARTEXT — {len(folien)} Folien\n")

    for i, f in enumerate(folien, 1):
        try:
            (AUS / f"folie-{i:02d}.html").write_text(
                rendere(f, i, len(folien)), encoding="utf-8")
        except ValueError as ex:
            sys.exit(f"\nFEHLER: {ex}\n")

    if len(folien) > 15:
        print(f"  ! {len(folien)} Folien, die Aufgabe erlaubt hoechstens 15\n")

    if schnell:
        print("  HTML geschrieben (--schnell, keine Bilder)")
        zeit(folien)
        return

    if not Path(CHROME).exists():
        sys.exit(f"Chrome nicht gefunden: {CHROME}")

    schiesse_pngs(folien, nur)
    p = baue_pptx(folien)
    d = baue_pdf(folien)
    print(f"\n  {p.name}")
    print(f"  {d.name}")
    zeit(folien)
    commit(folien)
    print()


if __name__ == "__main__":
    main()
