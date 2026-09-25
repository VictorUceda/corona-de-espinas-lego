"""Instruction book -> build/instructions/book.html (then render/pdf.mjs -> dist/instrucciones.pdf).

Page style from book_style.py (split cover, yellow section badges, white step pages, blue parts boxes,
yellow-outlined new parts). Every step page carries the notes of notas.py that its steps trigger
('Arquitectura' = the real building, dark panel; 'Técnica LEGO' = design technique, yellow panel), plus an intro
chapter on the building and on the techniques, the parts inventory and a sources page.
"""
import html, json, os, sys
import book_style as b1
from ldr import ROOT

INS = os.path.join(ROOT, 'build', 'instructions')
COLOR = {71: 'Light Bluish Gray', 72: 'Dark Bluish Gray', 15: 'White', 0: 'Black', 47: 'Trans-Clear',
         19: 'Tan', 70: 'Reddish Brown', 288: 'Dark Green'}
SWATCH = {71: '#A0A5A9', 72: '#6C6E68', 15: '#F4F4F4', 0: '#1B2A34', 47: '#E8EEF2', 19: '#E4CD9E', 70: '#582A12', 288: '#184632'}
Y = b1.Y
FOOT = 'Instrucciones no oficiales · Corona de Espinas · 1:250'

CSS = b1.CSS + f"""
.note {{ border-radius: 2.5mm; padding: 3mm 3.5mm; font-size: 8.3pt; line-height: 1.45; break-inside: avoid }}
.note .lab {{ font-size: 6.5pt; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 1mm }}
.note b {{ display: block; font-size: 10pt; margin-bottom: 1mm; line-height: 1.2 }}
.note.arq {{ background: #2e3236; color: #e3e7ea }} .note.arq .lab {{ color: #9fb3c2 }}
.note.lego {{ background: #fff4cc; color: #2b2f33; border-left: 1.6mm solid {Y} }} .note.lego .lab {{ color: #a07c00 }}
.withnotes {{ position: absolute; top: 18mm; left: 10mm; right: 10mm; bottom: 14mm; display: grid; grid-template-columns: 1fr 78mm; gap: 6mm }}
.withnotes .steps {{ position: static }}
.withnotes .col {{ display: flex; flex-direction: column; gap: 4mm; overflow: hidden }}
.open .notes {{ margin-top: 6mm; display: flex; flex-direction: column; gap: 3mm; width: 95mm }}
.intro {{ position: absolute; inset: 18mm 14mm 16mm; display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5mm; align-content: start }}
.intro h2 {{ grid-column: 1 / -1; margin: 0 }}
.intro .lead {{ grid-column: 1 / -1; font-size: 10pt; color: #5c6670; line-height: 1.5; margin: -2mm 0 2mm }}
.intro img {{ grid-column: span 2; width: 100%; height: 72mm; object-fit: contain; background: #f4f7fa; border-radius: 3mm }}
.src {{ position: absolute; inset: 18mm 14mm 16mm; columns: 2; column-gap: 10mm; font-size: 8.5pt; line-height: 1.5; color: #3d464f }}
.src h2 {{ column-span: all }} .src li {{ margin-bottom: 1.5mm }}
"""
TXT = dict(b1.SECTION_TEXT)
TXT.update({
    'base': 'Placa base 48×48 con parque en las esquinas y podio de dos placas: tiles donde apoya el anillo, studs donde se ancla y los ejes de replanteo en blanco.',
    'gajo': 'Un sector de 12°: celosía y tornapunta en PB, bandejas con pico en P1-P3, persianas, aletas, P3 inclinada con jabalcón, canalón, lucernarios, corona y dos espinas.',
    'pilares': 'El vestíbulo bajo la cúpula: suelo de piedra, lámina de agua con el Chillida que nunca se hizo, 12 pilares y la linterna.',
    'plaza': 'El forjado de la plaza, con su entramado de vigas y anillos rígidos, la losa, los lucernarios en diente de sierra y los casetones. Se monta aparte.',
    'cupula': 'La cúpula estrella se apoya en la plaza y se engancha a la linterna.',
    'entrada': 'Testeros de hormigón de tablas, las dos pasarelas y la escalinata del cañón de entrada.',
})
MAXN = 3            # notes per step page (column)

def note(n):
    k, t, x = (n['kind'], n['title'], n['text']) if isinstance(n, dict) else n
    lab = 'Arquitectura' if k == 'arq' else 'Técnica LEGO'
    return f"<div class='note {k}'><div class='lab'>{lab}</div><b>{html.escape(t)}</b>{html.escape(x)}</div>"

def parts_box(parts):
    return b1.parts_box(parts).replace("src='img/", "src='img/")

def page(body, pno, pill=None, cls=''):
    pl = f"<div class='pill'><i>{pill[0]}</i>{html.escape(pill[1])}</div>" if pill else ''
    return f"<div class='page {cls}'>{pl}{body}<div class='foot'><span>{FOOT}</span><span>{pno}</span></div></div>"

def main():
    book = json.load(open(os.path.join(INS, 'steps.json')))
    secs = book['sections']
    nsteps = sum(len(s['steps']) for s in secs)
    nnotes = sum(len(s['notes']) + sum(len(st.get('notes', [])) for st in s['steps']) for s in secs) + len(book['intro'])
    npcs = f"{book['n_parts']:,}".replace(',', '.')
    Pg = []
    Pg.append(f"""<div class='page cover'><div class='l'>
<div class='k'>Una maqueta en piezas LEGO® de la</div><h1>Corona de Espinas</h1>
<div class='s'>la sede del Instituto del Patrimonio Cultural de España (Fernando Higueras y Antonio Miró, Madrid, 1965–1989), a escala 1:250</div>
<div class='n'>{npcs} <span>piezas</span></div><div class='m'>{nsteps} pasos · {nnotes} notas de arquitectura y técnica · 28 gajos · 55 espinas · Ø 35 cm</div>
<div class='fine'>LEGO® es una marca registrada de LEGO Group, que no patrocina, autoriza ni respalda estas instrucciones.
Diseño basado en fotografías, planos originales y LiDAR PNOA.</div></div><div class='r'></div></div>""")
    pno = 2
    how = """<div class='how'>
<div class='c'><b>Piezas del paso</b>La caja azul muestra las piezas que añades en ese paso y cuántas.</div>
<div class='c'><b>Submontajes</b>Las secciones enmarcadas en amarillo se montan aparte. El gajo se repite <b style='display:inline'>×28</b>.</div>
<div class='c'><b>Piezas que se apoyan</b>Algunas piezas (las bandejas con pico) se apoyan sin encajar y las atrapa el paso siguiente. Sujétalas con un dedo.</div></div>"""
    rows = ''.join(f"<tr><td><span class='b'>{i}</span>{html.escape(s['title'])}</td><td class='num'>{len(s['steps'])} paso{'s' if len(s['steps']) != 1 else ''}</td></tr>"
                   for i, s in enumerate(secs, 1))
    Pg.append(page(f"<div class='two'><div><h2>Cómo leer este libro</h2>{how}</div><div><h2>Secciones</h2><table class='toc'>{rows}</table></div></div>", pno))
    arq = [n for n in book['intro'] if n[0] == 'arq']; lego = [n for n in book['intro'] if n[0] == 'lego']
    pno += 1
    Pg.append(page("<div class='intro'><h2>El edificio</h2><div class='lead'>Antes de empezar: qué vas a construir.</div>"
                   f"{note(arq[0])}<img src='img/intro_edificio.png'>{''.join(note(n) for n in arq[1:])}</div>", pno))
    pno += 1
    Pg.append(page("<div class='intro'><h2>Cómo se traduce a LEGO</h2><div class='lead'>Las tres ideas que hacen posible un anillo de 55 espinas con piezas rectas.</div>"
                   f"{note(lego[0])}<img src='img/intro_cadena.png'>{''.join(note(n) for n in lego[1:])}</div>", pno))
    n = 0
    for si, sec in enumerate(secs, 1):
        steps = sec['steps']; co = sec.get('callout')
        pill = (si, sec['title'])
        pno += 1
        cnt = sum(sum(p['qty'] for p in st['parts'] if p['part'] not in ('gajo_tipo', 'anillo', 'plaza')) for st in steps)
        meta = f"{len(steps)} paso{'s' if len(steps) != 1 else ''}" + (f" · {cnt} piezas" if cnt else '') + (f" · se construye {co['label']}" if co and co.get('mult', 1) > 1 else '')
        on = ''.join(note(x) for x in sec['notes'][:3])
        Pg.append(page(f"<div class='open'><div class='t'><span class='badge'>{si}</span><h3>{html.escape(sec['title'])}</h3>"
                       f"<p>{html.escape(TXT.get(sec['key'], ''))}</p><div class='meta'>{meta}</div><div class='notes'>{on}</div></div>"
                       f"<img src='img/{sec['key']}_final.png'></div>", pno, pill, 'open'))
        queue = list(sec['notes'][3:])
        i = 0
        while i < len(steps):
            per = 1 if len(steps) == 1 else 3
            nxt = [st for st in steps[i:i + per]]
            pend = queue + [x for st in nxt for x in st.get('notes', [])]
            if pend and per > 1:          # page with a notes column: 2 steps
                nxt = steps[i:i + 2]
                pend = queue + [x for st in nxt for x in st.get('notes', [])]
            cells = []
            for j, st in enumerate(nxt):
                n += 1; k = i + j + 1
                mult = f"<div class='mult'>{co['label']}</div>" if co and k == len(steps) and co.get('mult', 1) > 1 else ''
                cells.append(f"<div class='step{' callout' if co else ''}'><div class='hd'><div class='num'>{n}</div>{parts_box(st['parts'])}</div>"
                             f"<img class='r' src='img/{sec['key']}_{k}.png'>{mult}</div>")
            i += len(nxt)
            pno += 1
            if pend:
                show, queue = pend[:MAXN], pend[MAXN:]
                Pg.append(page(f"<div class='withnotes'><div class='steps n{len(cells)}'>{''.join(cells)}</div>"
                               f"<div class='col'>{''.join(note(x) for x in show)}</div></div>", pno, pill))
            else:
                queue = []
                Pg.append(page(f"<div class='steps n{len(cells)}'>{''.join(cells)}</div>", pno, pill))
        while queue:                       # leftover notes: a notes-only page
            pno += 1
            show, queue = queue[:6], queue[6:]
            Pg.append(page(f"<div class='intro'><h2>{html.escape(sec['title'])}: más notas</h2>{''.join(note(x) for x in show)}</div>", pno, pill))
    bom = book['bom']
    for i in range(0, len(bom), 50):
        items = ''.join(f"<div class='it'><img src='{b1.pthumb(b['part'], b['color'])}'><div class='q'>{b['qty']}×</div>"
                        f"<span class='sw' style='background:{SWATCH.get(b['color'], '#ccc')}'></span>{b['part'].replace('.dat', '')}</div>" for b in bom[i:i + 50])
        pno += 1
        Pg.append(page(f"<div style='position:absolute;left:14mm;top:16mm'><h2>Inventario de piezas{' (cont.)' if i else ''}</h2></div><div class='inv'>{items}</div>", pno))
    pno += 1
    Pg.append(page(f"""<div class='about'><div class='t'><h2>Sobre este modelo</h2>
<p>28 gajos idénticos, cada uno en su propia cuadrícula girada 12,02°, se encadenan con dos articulaciones exactas y forman el anillo
abierto hacia la entrada. Sobre esa cadena, cada gajo reproduce la fachada real: la celosía y la tornapunta de la planta baja,
las bandejas con pico, las persianas, las aletas de los nervios, la última planta inclinada con sus jabalcones, el canalón,
los lucernarios y las espinas.</p>
<p>Dentro quedan ocultos el pórtico radial con su pasillo anular, los ejes de replanteo del podio y el entramado de vigas bajo la plaza.</p>
<p>{npcs} piezas en 8 colores. Todas las piezas y colores existen en BrickLink y todas las uniones son legales: nada forzado ni tensionado.</p>
</div><div class='imgs'><img src='img/about_e.png'><img src='img/about_top.png' style='width:70%;justify-self:end'></div></div>""", pno))
    pno += 1
    Pg.append(page("""<div class='src'><h2>Fuentes</h2><ul>
<li>Memoria del proyecto (1965) y sección acotada: revista <i>Arquitectura</i> nº 299, COAM, 1994.</li>
<li>Planos originales de Higueras y Miró (plantas, secciones A-A y B-B, plano 56 de la cúpula, julio de 1988): Archivo Histórico Digital de la ETSAM, Fondo Miró.</li>
<li>Real Decreto 1261/2001 de declaración como Bien de Interés Cultural (BOE 287/2001).</li>
<li>Ortofoto PNOA 2023 y LiDAR PNOA 2016/2024 (IGN): radios, alturas, 54 picos detectados a 6° y el hueco de la entrada.</li>
<li>Cartografía catastral: huella de 37,98 m de radio.</li>
<li>Fotografías de Wikimedia Commons (fachada, espinas, cubierta, biblioteca, patio y escalera).</li>
<li>Metalocus y otros artículos sobre el edificio (retranqueo y cimentación, "vientre de la ballena").</li>
</ul></div>""", pno))
    open(os.path.join(INS, 'book.html'), 'w').write(
        f"<!doctype html><html><head><meta charset='utf-8'><title>Corona de Espinas — instrucciones</title><style>{CSS}</style></head>"
        f"<body>{''.join(Pg)}</body></html>")
    print('pages', len(Pg), 'steps', n, 'notes', nnotes)

if __name__ == '__main__':
    main()
