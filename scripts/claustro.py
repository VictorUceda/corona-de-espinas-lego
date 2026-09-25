"""Claustro: the cloister core as an architect would discover it while building.

Real references: COAM 299 memoria ('doce patinejos formados por los pilares del claustro'; 'forjado reticular
poligonal con anillos rígidos'; Chillida granite sculpture 'sobre una lámina de agua' planned in the 1965 project),
AHDB plano 45 sección A-A/B-B (central vestíbulo at ±0.00 under the glass dome), plano 56 (star dome, central
lantern), Higueras' 'vientre de la ballena' (interlaced beams of the 2nd floor).

Global grid: origin = building centre, stud centres on half-integers. z in plates above the baseplate top.
"""
import math, os, sys
from kit import P, box
from core import cells_disk, cover, BIG, BIGT

LBG, DBG, WHITE, BLACK, TCLR = 71, 72, 15, 0, 47
TAN, RBROWN, TLBLUE = 19, 70, 43

HOLE_R = 4.2          # light well under the dome (cells fully inside are left open)
PILLAR_R = 6.4

def ring_cells(r0, r1):
    return [c for c in cells_disk(r1) if min(math.hypot(c[0] + a, c[1] + b) for a in (-.5, .5) for b in (-.5, .5)) >= r0]

def cells_of(p):
    import collide
    lo, hi = collide.aabb(p)
    x0, x1, y0, y1 = lo[0] / 20, hi[0] / 20, -hi[2] / 20, -lo[2] / 20
    return {(math.floor(x0 + .01) + .5 + i, math.floor(y0 + .01) + .5 + j)
            for i in range(round(x1 - x0)) for j in range(round(y1 - y0))}

def bridged_cover(cells, below, kind, color, z, tag):
    """Cover `cells` so that every 1x1 piece of the layer below is bridged to a neighbour by a 1x2 on top."""
    cs = set(cells); out = []; used = set()
    for p in below:
        cc = cells_of(p)
        if len(cc) != 1: continue
        (x, y), = cc
        if (x, y) in used: continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n in cs and n not in used:
                out.append(box(kind, color, min(x, n[0]) - .5, max(x, n[0]) + .5, min(y, n[1]) - .5, max(y, n[1]) + .5, z, f'{tag}br{len(out)}'))
                used |= {(x, y), n}; break
    rest, _ = cover([c for c in cells if c not in used], kind, color, z, tag, sizes=BIG, transpose=True)
    return out + rest

def pillars():
    """12 round pillars of the 'claustro porticado' (2x2 round bricks), z2-14, on grid corners."""
    pts = []
    for k in range(12):
        a = math.radians(15 + 30 * k)
        pts.append((round(PILLAR_R * math.sin(a)), round(PILLAR_R * math.cos(a))))
    return sorted(set(pts))

def build():
    g = []
    pil = pillars()
    pil_cells = {(x + dx, y + dy) for x, y in pil for dx in (-.5, .5) for dy in (-.5, .5)}
    # --- vestibulo floor (tan 'stone') inside the pillar ring, leaving the lantern, the pond and the pillars
    lantern = {(x, y) for x in (-.5, .5) for y in (-.5, .5)}
    pond = {(2.5, -.5), (2.5, .5), (3.5, .5), (3.5, -.5)}
    floor = [c for c in cells_disk(5.4) if c not in lantern | pond | pil_cells]
    t, _ = cover(floor, 'tile', TAN, 2, 'vest_', sizes=BIGT)
    g += t
    # --- lamina de agua + Chillida-style granite sculpture (a 'peine' of tooth plates on a pedestal)
    # (a dark basin under trans-clear tiles reads as still water, and keeps the palette at 8 colours)
    g.append(box('plate', DBG, 2, 4, -1, 1, 2, 'pond_basin'))
    g += [box('tile', TCLR, 2, 3, -1, 1, 3, 'pond_a'), box('tile', TCLR, 3, 4, 0, 1, 3, 'pond_b')]
    g.append(P('3005', DBG, 3.5, -0.5, 3, tag='chillida_block'))
    g.append(P('49668', DBG, 3.5, -0.5, 6, rot=90, tag='chillida_claw1'))
    g.append(P('49668', DBG, 3.5, -0.5, 7, rot=-30 + 180, tag='chillida_claw2'))
    # --- linterna: trans-clear light column carrying the centre of the star dome
    for z in (2, 5, 8, 11, 14):
        g.append(P('3941', TCLR, 0, 0, z, tag=f'lantern{z}'))
    g.append(P('3941', TCLR, 0, 0, 17, tag='lantern_p17'))          # (4032b trans-clear does not exist)
    # --- 12 pillars (claustro porticado)
    for k, (x, y) in enumerate(pil):
        for z in (2, 5, 8, 11):
            g.append(P('3941', LBG, x, y, z, tag=f'pil{k}_{z}'))
    # --- biblioteca: ring of reddish-brown bookshelves between the pillars and the ring's joint blocks
    shelves = [c for c in ring_cells(6.9, 8.4) if c not in pil_cells]
    for z in (2, 3):
        s, _ = cover(shelves, 'plate', RBROWN, z, f'libro{z}_', sizes=((1, 4), (1, 3), (1, 2), (1, 1)))
        g += s
    # --- 'vientre de la ballena': polygonal ring beam + 12 radial beams under the plaza slab (z14)
    ring = set(ring_cells(5.4, 7.4))
    radial = set()
    for k in range(12):
        a = math.radians(15 + 30 * k)
        for r in [4.4 + 0.25 * i for i in range(22)]:
            c = (math.floor(r * math.sin(a)) + .5, math.floor(r * math.cos(a)) + .5)
            if 4.3 < math.hypot(*c) < 9.4: radial.add(c)
    # --- plaza slab (2 crossed plate layers) with the light well open under the dome
    slab = [c for c in cells_disk(9.85) if math.hypot(*c) > HOLE_R + 0.3]
    ss = set(slab)                                   # drop cells touching the rest only diagonally
    slab = [c for c in slab if sum((c[0] + dx, c[1] + dy) in ss for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 2]
    rims = set(ring_cells(4.4, 5.6)) | set(ring_cells(8.2, 9.85))       # 'anillos rigidos' at both slab edges
    beams = sorted(((ring | radial | rims) - lantern) & set(slab))
    b, _ = cover(beams, 'plate', DBG, 14, 'ballena_', sizes=((1, 4), (1, 3), (2, 2), (1, 2), (1, 1)))
    g += b
    s15, _ = cover(slab, 'plate', DBG, 15, 'slabA_', sizes=BIG)
    s16 = bridged_cover(slab, s15, 'plate', LBG, 16, 'slabB_')
    g += s15 + s16
    # --- plaza surface: tiles, six sawtooth glass wings, white ventilation boxes (casetones)
    wings = set()
    for a in (6 + 60 * k for k in range(6)):
        for c in slab:
            r = math.hypot(*c); ang = (math.degrees(math.atan2(c[0], c[1])) - a + 540) % 360 - 180
            if 5.6 <= r <= 9.3 and abs(ang) <= 11: wings.add(c)
    boxes_ = []
    for a in (36 + 60 * k for k in range(6)):
        x, y = round(8.2 * math.sin(math.radians(a)) - .5) + .5, round(8.2 * math.cos(math.radians(a)) - .5) + .5
        if (x, y) in set(slab) and (x, y) not in wings: boxes_.append((x, y))
    top = [c for c in slab if c not in wings and c not in boxes_]
    t17, _ = cover(top, 'tile', LBG, 17, 'plaza_', sizes=BIGT)
    g += t17
    for k, c in enumerate(sorted(wings)):
        g.append(P('54200', TCLR, c[0], c[1], 17, rot=0, tag=f'wing{k}'))
    for k, (x, y) in enumerate(boxes_):
        g.append(P('3005', WHITE, x, y, 17, tag=f'caseton{k}'))
        g.append(P('3070b', WHITE, x, y, 20, tag=f'caseton_t{k}'))
    # --- star dome on the tile ring around the light well, centre on the lantern
    g.append(P('50990b', TCLR, 0, 0, 18, tag='dome'))
    return g

if __name__ == '__main__':
    import collide, connect, networkx as nx
    g = build()
    G = connect.graph(g)
    print('parts', len(g), 'hits', [(g[i].tag, g[j].tag) for i, j in collide.pair_hits(g)][:8],
          'components', nx.number_connected_components(G))
