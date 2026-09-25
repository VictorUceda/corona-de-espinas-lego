"""Instruction-book style: page CSS (A4 landscape, yellow section badges, white step pages, blue parts boxes)
and small HTML helpers used by book.py."""
import json, os, html
from ldr import ROOT

COLOR = {71: 'Light Bluish Gray', 72: 'Dark Bluish Gray', 15: 'White', 40: 'Trans-Black', 47: 'Trans-Clear', 2: 'Green'}
SWATCH = {71: '#A0A5A9', 72: '#6C6E68', 15: '#F4F4F4', 40: '#635F52', 47: '#E8EEF2', 2: '#237841'}
Y = '#F5C518'

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
@page {{ size: A4 landscape; margin: 0 }}
* {{ box-sizing: border-box }}
body {{ margin: 0; font-family: Inter, 'Helvetica Neue', Arial, sans-serif; color: #1d2227; -webkit-print-color-adjust: exact }}
.page {{ width: 297mm; height: 210mm; page-break-after: always; position: relative; overflow: hidden; background: #fff }}
.foot {{ position: absolute; bottom: 6mm; left: 12mm; right: 12mm; display: flex; justify-content: space-between; font-size: 7pt; color: #9aa3ab }}
.pill {{ position: absolute; top: 8mm; right: 12mm; background: {Y}; border-radius: 10mm; padding: 1.2mm 3.5mm 1.2mm 1.2mm;
         font-size: 8pt; font-weight: 700; display: flex; align-items: center; gap: 2mm }}
.pill i {{ font-style: normal; background: #1d2227; color: {Y}; width: 5.2mm; height: 5.2mm; border-radius: 50%; display: grid; place-items: center; font-size: 7pt }}
.badge {{ display: inline-grid; place-items: center; width: 13mm; height: 13mm; border-radius: 50%; background: {Y}; font-weight: 800; font-size: 16pt }}
.cover {{ display: grid; grid-template-columns: 38% 62% }}
.cover .l {{ background: #2e3236; color: #fff; padding: 20mm 14mm; position: relative }}
.cover .r {{ background: #b4b8bc url(img/cover_gray.png) 50% 55% / cover no-repeat }}
.cover .k {{ font-size: 8pt; letter-spacing: .18em; text-transform: uppercase; color: #aeb5bc }}
.cover h1 {{ font-size: 40pt; line-height: 1; margin: 3mm 0 4mm; font-weight: 800; letter-spacing: -.02em }}
.cover .s {{ font-size: 10.5pt; line-height: 1.5; color: #d6dbe0 }}
.cover .yb {{ margin-top: 10mm; background: {Y}; color: #1d2227; font-weight: 800; font-size: 11pt; line-height: 1.3; padding: 3mm 4mm; border-radius: 1.5mm; display: inline-block }}
.cover .n {{ margin-top: 10mm; font-size: 24pt; font-weight: 800 }} .cover .n span {{ font-size: 11pt; font-weight: 500 }}
.cover .m {{ font-size: 9.5pt; color: #c3c9cf; margin-top: 1mm }}
.cover .fine {{ position: absolute; left: 14mm; right: 14mm; bottom: 12mm; font-size: 7pt; color: #8f979e; line-height: 1.5 }}
.two {{ position: absolute; inset: 18mm 14mm 16mm; display: grid; grid-template-columns: 1fr 1fr; gap: 12mm }}
h2 {{ font-size: 18pt; margin: 0 0 5mm; font-weight: 800 }}
.how {{ display: grid; grid-template-columns: 1fr 1fr; gap: 4mm }}
.how .c {{ background: #f4f7fa; border-radius: 3mm; padding: 3mm; font-size: 8.5pt; line-height: 1.45 }}
.how .c b {{ display: block; font-size: 9.5pt; margin-bottom: 1mm }}
.toc {{ width: 100%; border-collapse: collapse; font-size: 9pt }}
.toc td {{ padding: 2.2mm 1mm; border-bottom: .25mm solid #e3e8ec }} .toc td.num {{ text-align: right; color: #6f7a84 }}
.toc .b {{ display: inline-grid; place-items: center; width: 6mm; height: 6mm; border-radius: 50%; background: {Y}; font-weight: 800; font-size: 8pt; margin-right: 2mm }}
.open .t {{ position: absolute; left: 16mm; top: 22mm; width: 95mm }}
.open h3 {{ font-size: 26pt; line-height: 1.05; margin: 5mm 0 4mm; font-weight: 800 }}
.open p {{ font-size: 10pt; line-height: 1.55; color: #5c6670 }}
.open .meta {{ font-size: 8.5pt; color: #8a949d; margin-top: 4mm }}
.open img {{ position: absolute; right: 8mm; top: 12mm; width: 175mm; height: 180mm; object-fit: contain }}
.steps {{ position: absolute; top: 18mm; left: 10mm; right: 10mm; bottom: 14mm; display: grid; gap: 6mm }}
.steps.n1 {{ grid-template-columns: 1fr }} .steps.n2 {{ grid-template-columns: 1fr 1fr }} .steps.n3 {{ grid-template-columns: 1fr 1fr 1fr }}
.step {{ position: relative; display: flex; flex-direction: column; min-height: 0 }}
.step .hd {{ display: flex; align-items: flex-start; gap: 3mm; min-height: 20mm }}
.step .num {{ font-size: 20pt; font-weight: 800; line-height: 1; min-width: 12mm }}
.parts {{ background: #dcebf7; border-radius: 2.5mm; padding: 1.5mm 2mm; display: flex; flex-wrap: wrap; gap: 1mm 2mm }}
.pt {{ width: 12.5mm; text-align: center; font-size: 7pt; font-weight: 700 }}
.pt img {{ width: 12.5mm; height: 10mm; object-fit: contain; display: block; mix-blend-mode: multiply }}
.step img.r {{ flex: 1; width: 100%; min-height: 0; object-fit: contain }}
.callout {{ outline: .5mm solid {Y}; outline-offset: 2mm; border-radius: 2mm }}
.mult {{ position: absolute; right: 2mm; bottom: 2mm; background: {Y}; font-size: 20pt; font-weight: 800; padding: 1mm 4mm; border-radius: 2mm }}
.inv {{ position: absolute; top: 30mm; left: 10mm; right: 10mm; display: grid; grid-template-columns: repeat(10, 1fr); gap: 2mm }}
.inv .it {{ font-size: 6pt; color: #6a747d; text-align: center }}
.inv .it img {{ width: 100%; height: 13mm; object-fit: contain; mix-blend-mode: multiply }}
.inv .q {{ font-size: 9pt; font-weight: 800; color: #1d2227 }}
.inv .sw {{ display: inline-block; width: 2mm; height: 2mm; border-radius: .5mm; vertical-align: -.2mm; margin-right: .8mm; border: .2mm solid #0002 }}
.about .imgs {{ position: absolute; right: 12mm; top: 20mm; width: 150mm; display: grid; gap: 4mm }}
.about .imgs img {{ width: 100%; border-radius: 3mm; background: #f4f7fa }}
.about .t {{ position: absolute; left: 14mm; top: 20mm; width: 110mm; font-size: 9pt; line-height: 1.55; color: #3d464f }}
"""

SECTION_TEXT = {}
FOOT = 'Instrucciones no oficiales hechas por un fan · Corona de Espinas 1:250'

def pthumb(part, color): return f"img/part_{part.replace('.dat', '')}_{color}.png"

def parts_box(parts):
    out = []
    for p in parts:
        if p['part'] in ('gajo_tipo', 'anillo', 'plaza'):
            img = {'gajo_tipo': 'img/gajo_final.png', 'anillo': 'img/anillo_final.png', 'plaza': 'img/plaza_final.png'}[p['part']]
        else:
            img = pthumb(p['part'], p['color'])
        out.append(f"<div class='pt'><img src='{img}'>{p['qty']}×</div>")
    return f"<div class='parts'>{''.join(out)}</div>"

def page(body, pno, pill=None, cls=''):
    pl = f"<div class='pill'><i>{pill[0]}</i>{html.escape(pill[1])}</div>" if pill else ''
    return f"<div class='page {cls}'>{pl}{body}<div class='foot'><span>{FOOT}</span><span>{pno}</span></div></div>"
