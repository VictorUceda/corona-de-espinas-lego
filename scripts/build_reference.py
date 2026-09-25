"""Reference model of the building (measured from the sources in refs/) -> data/reference.json, data/planta.svg, data/alzado.svg.

Units: metres. Plan origin = building centre. Azimuth measured from grid north, clockwise.
Heights: h = metres above the surrounding terrain (LiDAR ground 614.22 m); project datum ±0.00 ≈ h 1.25.
"""
import json, math

# ---------------------------------------------------------------- measured / sourced data
REF = {
    "nombre": "Corona de Espinas — sede del IPCE (Higueras & Miró, 1965-1989)",
    "direccion": "C/ Pintor El Greco 4, 28040 Madrid",
    "unidades": "m; azimut desde norte de cuadrícula (UTM30N), sentido horario; h sobre terreno exterior",
    "sitio": {
        "centro_epsg25830": [437677.50, 4476982.68],
        "centro_latlon": [40.441159, -3.734864],
        "cota_terreno_msnm": 614.22,
        "datum_proyecto_h": 1.25,
        "ref_catastral": "7773607VK3777D",
        "fuente": "ajuste de circulo a huella Catastro + ortofoto PNOA 2023 + LiDAR PNOA 2024",
    },
    "modulacion": {
        "gajos_principales": 30,
        "modulos_teoricos": 60,
        "modulos_en_fachada": 56,
        "porticos_principales": 56,
        "angulo_modulo_deg": 6.0,
        "fase_nervios_deg": 0.3,  # radial ribs / spikes at 0.3 + 6k
        "modulos_suprimidos_entrada": 4,
        "nota": "Los datos fijos decian '4 gajos eliminados'; BOE y COAM dicen 4 MODULOS (=2 gajos) ocupados por la escalera de acceso. El LiDAR lo confirma: hueco de 24 deg.",
        "fuente": "BOE 287/2001 RD 1261/2001; AHDB ETSAM Fondo Miro (planos originales); COAM Arquitectura 299 (1994); LiDAR 2024 (espaciado medio 6.0 deg)",
    },
    "entrada": {
        "eje_azimut_deg": 186.3,
        "nervios_sin_espina_deg": [174.3, 180.3, 186.3, 192.3, 198.3],
        "hueco_fachada_deg": [174.3, 198.3],
        "canon_ancho_m": 14.0,
        "canon_lados": "paralelos entre r=22 y r=34; testeros abocinados hacia fuera (r>36)",
        "testeros": "muros ciegos trapezoidales de hormigon hasta la corona (h~27), con 1-2 espinas en coronacion",
        "puentes": "dos pasarelas-balcon (plantas 2a y 3a) cruzan el canon en r~20-30, con barandilla en cubierta",
        "escalera": "escalinata exterior que sube por el canon hasta la plaza del claustro",
        "fuente": "LiDAR (huecos por radio/altura), fotos commons: Entrada_del_Instituto_del_Patrimonio_Cultural_de_España,_Madrid.JPG, Instituto_del_Patrimonio_Histórico_Español_(Madrid)_02.jpg, Instituto_del_Patrimonio_Histórico_Español_(Madrid)_11.jpg",
    },
    "radios": {
        "voladizo_max_balcones": 41.5,
        "canto_balcones": 40.5,
        "fachada_pb_catastro": 38.0,
        "planta_ultima_pie": 41.0,
        "planta_ultima_cabeza": 38.3,
        "canalon_exterior": 38.0,
        "cumbrera_corona": 32.0,
        "espinas": 31.5,
        "canalon_interior": 26.0,
        "borde_claustro": 21.0,
        "cupula_central": 9.5,
        "circulo_teorico": 40.0,
        "fuente": "LiDAR perfil radial; Catastro r=37.98 (huella PB); BOE 'circulo de unos 40 m de radio'",
    },
    "niveles": [
        {"id": "sotano", "cota_proyecto": -5.60, "h": -4.35, "nota": "solo bajo parte del anillo (713 m2 Catastro)"},
        {"id": "exterior_bajo", "cota_proyecto": -1.75, "h": -0.50},
        {"id": "PB", "cota_proyecto": 0.00, "h": 1.25, "radio_fachada": 38.0, "nota": "retranqueada, celosia blanca, pilares con tornapuntas en Y"},
        {"id": "P1", "cota_proyecto": 3.90, "h": 5.15, "radio_voladizo": 40.5, "canto_voladizo_h": 7.3},
        {"id": "P2", "cota_proyecto": 7.80, "h": 9.05, "radio_voladizo": 41.5, "canto_voladizo_h": 10.8},
        {"id": "P3", "cota_proyecto": 11.70, "h": 12.95, "radio_voladizo": 41.5, "canto_voladizo_h": 14.5,
         "nota": "ultima planta: fachada inclinada hacia dentro de r41.0/h14.5 a r38.3/h18.6"},
        {"id": "cubierta_P3", "cota_proyecto": 15.60, "h": 16.85},
        {"id": "canalon", "h": 18.7},
        {"id": "cumbrera", "h": 24.5},
        {"id": "coronacion_corona", "h": 27.0},
        {"id": "punta_espinas", "h": 29.5},
        {"id": "plaza_claustro", "h": 15.2, "nota": "terraza abierta sobre el atrio, con lucernarios"},
        {"id": "cupula_claustro_max", "h": 17.5},
    ],
    "altura_planta_m": 3.90,
    "seccion_exterior": {
        "desc": "perfil (r,h) del anillo, de fuera a dentro, fuera de la entrada",
        "puntos": [[41.5, 14.5], [41.0, 14.5], [38.3, 18.6], [38.0, 19.3], [37.0, 18.6], [32.0, 24.5],
                   [26.0, 18.8], [21.0, 18.8], [21.0, 15.2], [9.5, 15.2], [0.0, 17.5]],
        "cubierta": "dos aguas ~50 deg a ambos lados de la cumbrera r=32; faldon exterior con malla gris y lucernarios semi-hexagonales blancos (uno por modulo) junto al canalon; faldon interior con teja oscura y lucernarios iguales",
        "fuente": "LiDAR 2024 + 2016 (work/section_lidar.png)",
    },
    "espinas": {
        "n": 55,
        "posicion": "sobre cada nervio radial, en la cumbrera r~31.5",
        "forma": "piramide de 4 caras blanca (lucernario de poliester/chapa) sobre pilastra de hormigon; entre espinas el muro de corona hace una W con vertiente blanca",
        "base_ancho_m": 3.0,
        "h_base": 24.5,
        "h_punta": 29.5,
        "fuente": "LiDAR (54 picos detectados, espaciado 6.0 deg, hueco de 5 en la entrada) + foto commons: Agujas_del_inmueble_sede_del_Instituto_del_Patrimonio_Cultural_de_España.JPG",
    },
    "claustro": {
        "tipo": "plaza-terraza abierta a h~15 sobre atrio cubierto (vidrio desde la rehabilitacion); 'claustro porticado' en el interior",
        "radio": 21.0,
        "cupula": {"radio": 9.5, "fuente": "plano 56 AHDB MIRO_002caP_T003_001 (acotado: cercha 785+165 cm); ortofoto da ~8.7-9", "forma": "estrella de vidrio de ~32 facetas con linterna central", "h": 17.5},
        "alas_lucernario": {"n": 6, "azimutes_deg": [6.3, 66.3, 126.3, 186.3, 246.3, 306.3], "ancho_deg": 22,
                             "r": [10, 20], "forma": "dientes de sierra radiales de vidrio"},
        "patios_laterales": 5,
        "casetones": "10-12 casetones blancos de ventilacion (rejillas) en la plaza",
        "fuente": "ortofoto (desenrollado polar), fotos commons: Cubierta_o_terraza_de_la_sede_del_Instituto_del_Patrimonio_Cultural_de_España,_en_Madrid.jpg, Instituto_del_Patrimonio_Histórico_Español_(Madrid)_04.jpg, Instituto_del_Patrimonio_Histórico_Español_(Madrid)_08.jpg",
    },
    "fachada": {
        "pb": "retranqueada; celosia blanca de hormigon prefabricado entre pilares; tornapuntas en Y bajo el voladizo de P1",
        "p1_p3": "voladizos corridos facetados (un tramo recto por modulo, 6 deg) con aletas verticales en cada nervio; frentes de balcon trapezoidales; ventanas con persiana enrollable gris claro",
        "ultima": "P3 inclinada hacia dentro con jabalcones diagonales en cada nervio que suben hasta el canalon",
        "modulo_alzado_original": "AHDB MIRO_002jP_CR005-02_014: por modulo PB con puertas/celosia, 2 filas de ventanas en triplete, planta ultima inclinada con ventanas, faldon de teja (escamas), y remate en V con lucernario y dos brazos que suben a las espinas de los nervios",
        "cantos": "barandilla metalica ligera en canalon y en plaza",
    },
    "materiales_color": {
        "hormigon_visto": {"hex_muestras": ["#a29c96", "#8c8a87", "#7b786e", "#6a6761"], "lego": "Light Bluish Gray (71) / Dark Bluish Gray (72)"},
        "espinas_y_lucernarios": {"hex": "#dadde3", "lego": "White (15)"},
        "persianas": {"hex": "#a5a7ac", "lego": "Light Bluish Gray / White"},
        "vidrio": {"lego": "Trans-Clear (47) / Trans-Black (40)"},
        "cubierta_faldones": {"hex": "#707273", "lego": "Dark Bluish Gray (72)"},
        "encofrado": "tabla de 8 cm (textura horizontal)",
    },
    "superficies": {"parcela_m2": 12405, "huella_m2": 4536, "construida_m2": 16774,
                    "por_planta_m2": {"sotano": 713, "PB": 4508, "P1": 3907, "P2": 3706, "P3": 3706, "P4": 234}},
    "cronologia": {"concurso": 1961, "proyecto": 1965, "inicio_obras": 1966, "fin": 1989, "BIC": "RD 1261/2001"},
    "planos_clave": ["refs/planos/ahdb/MIRO_002aaP_T003_001.jpg (planta 3a 1:100 + seccion corona)", "refs/planos/ahdb/MIRO_002jP_CR005-02_014.jpg (alzado 4 modulos)", "refs/planos/ahdb/MIRO_002caP_T003_001.jpg (cupula acotada)", "refs/planos/coam299_p69_planta_baja_seccion_cotas.jpg (cotas de nivel)", "refs/planos/metalocus-coronadeespinas-ohm16-24.jpg (planta con escala grafica)"],
    "discrepancias_con_datos_fijos": [
        "Diametro: 80 m nominal (circulo teorico r=40). Medido: 83 m en voladizos de balcones, 76 m en PB (Catastro).",
        "Entrada: se suprimen 4 MODULOS (2 gajos, 24 deg), no 4 gajos.",
        "55 espinas confirmado: 60 nervios menos 5 (3 dentro del hueco + los 2 testeros).",
        "4 plantas = PB+P1+P2+P3; la 'fachada inclinada' es la de la P3 (ultima). Catastro lista una P4 residual de 234 m2 (cuartos en la corona).",
        "El 'claustro central' no es un patio a cota 0 sino una plaza elevada (h~15) con lucernarios sobre un atrio cubierto.",
        "Espinas: los planos (subagente) dan punta ~+25..+27 sobre ±0.00; el LiDAR da h 29.5 (= +28.25). Se usa LiDAR.",
        "El hormigon visto en las fotos es gris neutro-calido; las espinas y lucernarios son BLANCOS, no de hormigon.",
    ],
}

# ---------------------------------------------------------------- helpers
M, PH, EA = 60, 0.3, 186.3
RIBS = [PH + 6 * k for k in range(M)]
def missing(a): return min(abs(((a - x + 180) % 360) - 180) for x in REF["entrada"]["nervios_sin_espina_deg"]) < 0.1
def in_gap(a): return abs(((a - EA + 180) % 360) - 180) < 12.0 - 1e-6
SPIKES = [a for a in RIBS if not missing(a)]
assert len(SPIKES) == 55
def P(r, az, s=1.0, cx=0.0, cy=0.0):
    t = math.radians(az); return (cx + s * r * math.sin(t), cy - s * r * math.cos(t))

# ---------------------------------------------------------------- planta.svg
def planta(path):
    S, W, C = 9.0, 980, 490  # px per m, size, centre
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{W+60}" viewBox="0 0 {W} {W+60}" font-family="Helvetica,Arial" font-size="11">',
         '<rect width="100%" height="100%" fill="#fff"/>',
         '<style>polyline{fill:none}.c{fill:none;stroke:#333}.t{fill:none;stroke:#999;stroke-width:.5}.d{stroke:#c0392b;stroke-width:.8;fill:none}.dt{fill:#c0392b}</style>']
    def pt(r, a): return P(r, a, S, C, C)
    def ring(r, cls="c", w=1, dash=None, gap=True):
        # draw arc skipping the entrance gap
        da = f'stroke-dasharray="{dash}"' if dash else ""
        pts = [pt(r, a / 2) for a in range(0, 721)]
        if gap:
            segs, cur = [], []
            for a in range(0, 721):
                if in_gap(a / 2): segs.append(cur); cur = []
                else: cur.append(pt(r, a / 2))
            segs.append(cur)
            return "".join(f'<polyline class="{cls}" stroke-width="{w}" {da} points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in s)}"/>' for s in segs if len(s) > 1)
        return f'<circle class="{cls}" stroke-width="{w}" cx="{C}" cy="{C}" r="{r*S:.1f}" {da}/>'
    # rings
    o.append(ring(41.5, w=1.6)); o.append(ring(40.5, "t")); o.append(ring(38.0, w=1.0, dash="6,3"))
    o.append(ring(32.0, "c", .8)); o.append(ring(26.0, "t")); o.append(ring(21.0, w=1.2, gap=False))
    o.append(ring(9.5, w=1.2, gap=False))
    # radial ribs (module lines)
    for a in RIBS:
        if in_gap(a) and not missing(a): continue
        r0 = 21.0 if not in_gap(a) else 36
        x0, y0 = pt(r0, a); x1, y1 = pt(41.5, a)
        o.append(f'<line class="t" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    # gajo lines (30 main, every other rib) reaching the cloister
    for k, a in enumerate(RIBS):
        if k % 2 == 0 and not in_gap(a):
            x0, y0 = pt(9.5, a); x1, y1 = pt(21.0, a); o.append(f'<line stroke="#bbb" stroke-width=".4" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    # spikes
    for a in SPIKES:
        x, y = pt(31.5, a); o.append(f'<polygon fill="#fff" stroke="#000" stroke-width=".7" points="{x:.1f},{y-5:.1f} {x+4:.1f},{y:.1f} {x:.1f},{y+5:.1f} {x-4:.1f},{y:.1f}" transform="rotate({a:.1f} {x:.1f} {y:.1f})"/>')
    # skylight wings
    for a in REF["claustro"]["alas_lucernario"]["azimutes_deg"]:
        pts = [pt(10, a - 11), pt(20, a - 11), pt(20, a + 11), pt(10, a + 11)]
        o.append(f'<polygon fill="#d6eaf8" stroke="#5d8aa8" stroke-width=".8" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
        for dd in range(-10, 11, 2):
            x0, y0 = pt(10, a + dd); x1, y1 = pt(20, a + dd); o.append(f'<line stroke="#5d8aa8" stroke-width=".4" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    for k in range(32):
        x1, y1 = pt(9.5, k * 360 / 32); o.append(f'<line stroke="#5d8aa8" stroke-width=".4" x1="{C}" y1="{C}" x2="{x1:.1f}" y2="{y1:.1f}"/>')
    # entrance canyon (parallel walls, 14 m) + flared ends
    t = math.radians(EA); ux, uy = math.sin(t), -math.cos(t); nx, ny = -uy, ux
    for sgn in (-1, 1):
        a0 = (C + (ux * 21 + sgn * nx * 7) * S, C + (uy * 21 + sgn * ny * 7) * S)
        a1 = (C + (ux * 35 + sgn * nx * 7) * S, C + (uy * 35 + sgn * ny * 7) * S)
        a2 = pt(41.5, EA + sgn * 12)
        o.append(f'<polyline fill="none" stroke="#000" stroke-width="2" points="{a0[0]:.1f},{a0[1]:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}"/>')
    for rr in (22.5, 27.5):  # bridges
        b0 = (C + (ux * rr - nx * 7) * S, C + (uy * rr - ny * 7) * S); b1 = (C + (ux * rr + nx * 7) * S, C + (uy * rr + ny * 7) * S)
        o.append(f'<line stroke="#555" stroke-width="1" stroke-dasharray="3,2" x1="{b0[0]:.1f}" y1="{b0[1]:.1f}" x2="{b1[0]:.1f}" y2="{b1[1]:.1f}"/>')
    # dimension lines
    def dim(r1, r2, a, label, off=0):
        x0, y0 = pt(r1, a); x1, y1 = pt(r2, a)
        o.append(f'<line class="d" x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/>')
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        o.append(f'<text class="dt" x="{xm+4:.1f}" y="{ym-4+off:.1f}">{label}</text>')
    o.insert(3, '<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,2 L10,5 L0,8" fill="#c0392b"/></marker></defs>')
    dim(41.5, 41.5, 0, "")
    o.append(f'<line class="d" x1="{C-41.5*S:.1f}" y1="{C-455:.1f}" x2="{C+41.5*S:.1f}" y2="{C-455:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/><text class="dt" x="{C-40}" y="{C-460:.1f}">Ø 83.0 voladizos</text>')
    o.append(f'<line class="d" x1="{C-38*S:.1f}" y1="{C+452:.1f}" x2="{C+38*S:.1f}" y2="{C+452:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/><text class="dt" x="{C-150}" y="{C+466:.1f}">Ø 76.0 PB (Catastro)</text>')
    dim(0, 21.0, 96.3, "R 21.0 claustro", 0); dim(0, 9.5, 66.3, "R 9.5 cúpula")
    dim(21.0, 32.0, 276.3, "R 32.0 cumbrera"); dim(32.0, 41.5, 276.3, "9.5", 14)
    b0 = (C + (ux * 30 - nx * 7) * S, C + (uy * 30 - ny * 7) * S); b1 = (C + (ux * 30 + nx * 7) * S, C + (uy * 30 + ny * 7) * S)
    o.append(f'<line class="d" x1="{b0[0]:.1f}" y1="{b0[1]:.1f}" x2="{b1[0]:.1f}" y2="{b1[1]:.1f}" marker-start="url(#ar)" marker-end="url(#ar)"/><text class="dt" x="{b1[0]+6:.1f}" y="{b1[1]+4:.1f}">14.0</text>')
    # module angle note
    x, y = pt(44, 36.3); o.append(f'<text class="dt" x="{x:.1f}" y="{y:.1f}">6° módulo</text>')
    x, y = pt(44.5, EA); o.append(f'<text x="{x-40:.1f}" y="{y+12:.1f}" font-weight="bold">ENTRADA az {EA}°</text>')
    # north arrow + scale
    o.append(f'<g transform="translate({W-60},60)"><polygon points="0,-30 8,8 0,2 -8,8" fill="#000"/><text x="-4" y="24" font-weight="bold">N</text></g>')
    o.append(f'<g transform="translate(30,{W+30})"><rect width="{10*S}" height="6" fill="#000"/><rect x="{10*S}" width="{10*S}" height="6" fill="#fff" stroke="#000"/><text y="-4">0</text><text x="{10*S-6}" y="-4">10</text><text x="{20*S-10}" y="-4">20 m</text></g>')
    o.append(f'<text x="{W-420}" y="{W+40}" font-size="12">Corona de Espinas — PLANTA de referencia (cubierta + huella). 60 nervios, 56 módulos, 55 espinas.</text>')
    o.append('</svg>'); open(path, 'w').write("\n".join(o))

# ---------------------------------------------------------------- alzado.svg (half elevation seen from the south + half section)
def alzado(path):
    S = 11.0; W = int(2 * 46 * S) + 260; H = 460; X0 = W / 2 - 70; Y0 = H - 60  # ground line
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial" font-size="11">',
         '<rect width="100%" height="100%" fill="#fff"/>',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,2 L10,5 L0,8" fill="#c0392b"/></marker></defs>',
         '<style>polyline{fill:none}.d{stroke:#c0392b;stroke-width:.8;fill:none}.dt{fill:#c0392b}</style>']
    X = lambda x: X0 + x * S; Y = lambda h: Y0 - h * S
    # view from azimuth 0 (north) looking south would show the back; we view from the NORTH-EAST? keep simple: from az 96.3 (east), entrance appears at right limb.
    # Left half: elevation (x = r*sin(az - view)), only front-facing ribs. Right half: section through the ring.
    view = 6.3  # looking from north towards south: front ribs are those with cos(az-view)>0
    def ex(r, a): return -r * math.sin(math.radians(a - view))  # x to the viewer's right is west... mirror so east is left
    front = [a for a in RIBS if math.cos(math.radians(a - view)) > 0]
    o.append(f'<clipPath id="lh"><rect x="0" y="0" width="{X0}" height="{H}"/></clipPath><g clip-path="url(#lh)">')
    # silhouette bands (horizontal lines of each level across the whole projected width)
    bands = [(0, 1.25, 38.0, '#eee'), (1.25, 5.15, 38.0, '#e8e8e8'), (5.15, 7.3, 40.5, '#cfcfcf'), (7.3, 9.05, 39.5, '#e6e6e6'),
             (9.05, 10.8, 41.5, '#cfcfcf'), (10.8, 12.95, 40.0, '#e6e6e6'), (12.95, 14.5, 41.5, '#cfcfcf')]
    for h0, h1, r, col in bands:
        o.append(f'<rect x="{X(-r):.1f}" y="{Y(h1):.1f}" width="{2*r*S:.1f}" height="{(h1-h0)*S:.1f}" fill="{col}" stroke="#555" stroke-width=".6"/>')
    o.append(f'<polygon fill="#d9d9d9" stroke="#555" stroke-width=".6" points="{X(-41):.1f},{Y(14.5):.1f} {X(41):.1f},{Y(14.5):.1f} {X(38.3):.1f},{Y(18.6):.1f} {X(-38.3):.1f},{Y(18.6):.1f}"/>')
    o.append(f'<polygon fill="#9a9c9e" stroke="#555" stroke-width=".6" points="{X(-38):.1f},{Y(18.7):.1f} {X(38):.1f},{Y(18.7):.1f} {X(32):.1f},{Y(24.5):.1f} {X(-32):.1f},{Y(24.5):.1f}"/>')
    for a in front:
        c = math.cos(math.radians(a - view))
        for (r, h0, h1, wd) in [(38.0, 1.25, 5.15, .5), (40.5, 5.15, 14.5, .9)]:
            x = X(ex(r, a)); o.append(f'<line x1="{x:.1f}" y1="{Y(h0):.1f}" x2="{x:.1f}" y2="{Y(h1):.1f}" stroke="#444" stroke-width="{wd*c:.2f}"/>')
        xa, xb = X(ex(41, a)), X(ex(38.3, a)); o.append(f'<line x1="{xa:.1f}" y1="{Y(14.5):.1f}" x2="{xb:.1f}" y2="{Y(18.6):.1f}" stroke="#444" stroke-width="{.9*c:.2f}"/>')
        xa, xb = X(ex(38, a)), X(ex(32, a)); o.append(f'<line x1="{xa:.1f}" y1="{Y(18.7):.1f}" x2="{xb:.1f}" y2="{Y(24.5):.1f}" stroke="#666" stroke-width="{.6*c:.2f}"/>')
    # crown + spikes (all spikes visible: those on the far side show above the ridge too)
    for a in [a for a in SPIKES if math.cos(math.radians(a - view)) > 0]:
        c = math.cos(math.radians(a - view)); x = ex(31.5, a); w = 1.5 * max(abs(c), .35)
        fill = "#ffffff" if c > 0 else "#e9e9e9"
        o.append(f'<rect x="{X(x-0.45):.1f}" y="{Y(27.0):.1f}" width="{0.9*S:.1f}" height="{2.5*S:.1f}" fill="#b9b6b1" stroke="#555" stroke-width=".4"/>')
        o.append(f'<polygon fill="{fill}" stroke="#333" stroke-width=".6" points="{X(x-w):.1f},{Y(24.5):.1f} {X(x):.1f},{Y(29.5):.1f} {X(x+w):.1f},{Y(24.5):.1f}"/>')
    o.append('</g>')
    # right half: section profile at az=96.3 (through ring), mirrored to the right side
    ring = [(41.5, 14.5), (41.0, 14.5), (38.3, 18.6), (38.0, 19.3), (37.0, 18.6), (32.0, 24.5), (26.0, 18.8), (21.0, 18.8),
            (21.0, 1.25), (38.0, 1.25), (38.0, 5.15), (40.5, 5.15), (40.5, 7.3), (41.5, 9.05), (41.5, 14.5)]
    o.append(f'<polygon fill="#cfd3d6" stroke="#000" stroke-width="1.4" points="{" ".join(f"{X(r):.1f},{Y(h):.1f}" for r, h in ring)}"/>')
    o.append(f'<rect x="{X(8.7):.1f}" y="{Y(15.2):.1f}" width="{12.3*S:.1f}" height="{0.6*S:.1f}" fill="#cfd3d6" stroke="#000"/>')
    o.append(f'<polyline stroke="#5d8aa8" stroke-width="1.4" points="{X(0):.1f},{Y(17.5):.1f} {X(9.5):.1f},{Y(15.2):.1f}"/>')
    o.append(f'<polyline stroke="#5d8aa8" stroke-width="1" points="{X(10):.1f},{Y(15.2):.1f} {X(10):.1f},{Y(16.5):.1f} {X(20):.1f},{Y(16.5):.1f} {X(20):.1f},{Y(15.2):.1f}"/>')
    o.append(f'<line x1="{X(0)}" y1="{Y(1.25)}" x2="{X(21)}" y2="{Y(1.25)}" stroke="#000" stroke-width="1.4"/>')
    o.append(f'<text x="{X(6)}" y="{Y(8)}" fill="#555">atrio (claustro cubierto)</text><text x="{X(10)}" y="{Y(17.3)}" fill="#5d8aa8">plaza h15.2 + lucernarios</text>')
    for lv in REF["niveles"]:
        if lv["id"] in ("PB", "P1", "P2", "P3", "cubierta_P3"):
            o.append(f'<line x1="{X(21):.1f}" y1="{Y(lv["h"]):.1f}" x2="{X(40):.1f}" y2="{Y(lv["h"]):.1f}" stroke="#000" stroke-width="1.6"/>')
    for hh, rr in [(7.3, 40.5), (10.8, 41.5), (14.5, 41.5)]:
        o.append(f'<polygon fill="#aaa" stroke="#000" stroke-width=".8" points="{X(38.5):.1f},{Y(hh-1.6):.1f} {X(rr):.1f},{Y(hh-1.2):.1f} {X(rr):.1f},{Y(hh):.1f} {X(38.5):.1f},{Y(hh):.1f}"/>')
    o.append(f'<polygon fill="#fff" stroke="#000" stroke-width=".8" points="{X(30):.1f},{Y(24.5):.1f} {X(31.5):.1f},{Y(29.5):.1f} {X(33):.1f},{Y(24.5):.1f}"/>')
    o.append(f'<line x1="{X(0)}" y1="20" x2="{X(0)}" y2="{H-20}" stroke="#888" stroke-dasharray="8,3,2,3"/>')
    o.append(f'<line x1="20" y1="{Y(0)}" x2="{W-20}" y2="{Y(0)}" stroke="#000" stroke-width="1.2"/>')
    # level cotas on the far right
    xr = X(44.5)
    for lbl, h in [("±0.00 (h 1.25)", 1.25), ("+3.90 P1", 5.15), ("+7.80 P2", 9.05), ("+11.70 P3", 12.95), ("+15.60 cub.", 16.85),
                   ("h 18.7 canalón", 18.7), ("h 24.5 cumbrera", 24.5), ("h 29.5 espinas", 29.5), ("h 0 terreno", 0)]:
        o.append(f'<line x1="{X(41.8):.1f}" y1="{Y(h):.1f}" x2="{xr:.1f}" y2="{Y(h):.1f}" stroke="#c0392b" stroke-width=".5"/><text class="dt" x="{xr+3:.1f}" y="{Y(h)+4:.1f}">{lbl}</text>')
    # horizontal dims
    o.append(f'<line class="d" x1="{X(0)}" y1="{Y(-2.5)}" x2="{X(41.5)}" y2="{Y(-2.5)}" marker-start="url(#ar)" marker-end="url(#ar)"/><text class="dt" x="{X(18)}" y="{Y(-3.4)}">R 41.5</text>')
    o.append(f'<line class="d" x1="{X(-41.5)}" y1="{Y(-2.5)}" x2="{X(0)}" y2="{Y(-2.5)}" marker-start="url(#ar)" marker-end="url(#ar)"/><text class="dt" x="{X(-24)}" y="{Y(-3.4)}">R 41.5 (Ø 83)</text>')
    o.append(f'<text x="30" y="24" font-size="12">ALZADO NORTE (mitad izq.) — SECCIÓN radial az 96° (mitad dcha.). Cotas de proyecto (COAM 299) y h sobre terreno (LiDAR).</text>')
    o.append('</svg>'); open(path, 'w').write("\n".join(o))

if __name__ == "__main__":
    REF["espinas"]["azimutes_deg"] = [round(a, 1) for a in SPIKES]
    json.dump(REF, open("data/reference.json", "w"), indent=1, ensure_ascii=False)
    planta("data/planta.svg"); alzado("data/alzado.svg")
    print("ok: data/reference.json data/planta.svg data/alzado.svg; spikes", len(SPIKES))
