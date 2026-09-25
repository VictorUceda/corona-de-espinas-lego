"""Entrance (global grid, anchored on the podium): two testeros with parallel canyon faces, two bridges across
the canyon, a stair from the podium up to the cloister terrace (entrada.py builds the final version from this layout).

The canyon runs along global -y (south). Its faces are x = XL (west) and x = XR (east); the testeros are clipped
against the two end gajos (ordinary gajo_tipo instances of the ring) so nothing collides.
"""
import math
import numpy as np
import kit, gajo, collide, build_ring, core
from kit import P, box, frame, xform

LBG, DBG, WHITE, TBLK = 71, 72, 15, 40
XL, XR = -4, 0                 # canyon faces (studs): 4 studs = 8 m wide, parallel
Y_OUT, Y_IN = -21, -13         # testero extent (facade line -> inner end)
Z_TOP = 32                     # testero top (plates)
BRIDGES = ((13, 'P2'), (18, 'P3'))   # bridge band bottom levels (2 plates band + glass + parapet)
BRIDGE_Y = (-16, -14)

def end_gajos():
    ang = build_ring.gajo_angles()
    tipo = gajo.build()
    return xform(tipo, frame(max(ang))) + xform(tipo, frame(min(ang)))

def testero_cells():
    """Candidate footprint cells west of XL and east of XR, kept if a full-height column does not hit the end gajos."""
    ends = end_gajos()
    keep = []
    for x0 in list(range(XL - 3, XL)) + list(range(XR, XR + 3)):
        for y0 in range(Y_OUT, Y_IN):
            probe = [box('brick', LBG, x0, x0 + 1, y0, y0 + 1, z) for z in range(2, Z_TOP - 2, 3)]
            if not collide.pair_hits(probe, ends): keep.append((x0 + 0.5, y0 + 0.5))
    return keep

def zmax(cell):
    """Testero height by depth from the facade: P3 top, roof course, crown (stepped south face)."""
    d = cell[1] - Y_OUT - 0.5          # 0 at the facade row
    return 23 if d < 1 else 26 if d < 2 else 29 if d < 3 else Z_TOP

def in_slope(c, z, tcells):
    """Cells of step rows (depth 1, 2) are left free where the south-face slope sits (3 plates)."""
    d = c[1] - Y_OUT - 0.5
    if d not in (1.0, 2.0) or (c[0], c[1] - 1) not in tcells: return False
    z0 = zmax((c[0], c[1] - 1))
    return z0 <= z < z0 + 3

def layer_cover(cells, z, kind, color, tag):
    parts, left = core.cover(cells, kind, color, z, tag, sizes=((2, 8), (2, 6), (2, 4), (2, 3), (2, 2), (1, 8), (1, 6), (1, 4), (1, 3), (1, 2), (1, 1)))
    return parts

def build():
    g = []
    tcells = testero_cells()
    bridge_cells = [(x + 0.5, y + 0.5) for x in range(XL, XR) for y in range(*BRIDGE_Y)]
    bridge_layers = {z for zb, _ in BRIDGES for z in (zb, zb + 1)}
    z = 2
    while z < Z_TOP:
        live = [c for c in tcells if z < zmax(c) and not in_slope(c, z, tcells)]
        if z in bridge_layers:
            # one 2x6 bridge plate reaching into both testero columns, then the rest of the testeros
            g.append(box('plate', LBG, XL - 1, XR + 1, BRIDGE_Y[0], BRIDGE_Y[1], z, f'bridge{z}'))
            span = {(x + 0.5, y + 0.5) for x in range(XL - 1, XR + 1) for y in range(*BRIDGE_Y)}
            g += layer_cover([c for c in live if c not in span], z, 'plate', LBG, f'tb{z}_')
            z += 1
        elif all(zz not in bridge_layers for zz in (z, z + 1, z + 2)) and all(z + 3 <= zmax(c) for c in live):
            cells = sorted(live, key=lambda c: (c[0], c[1]) if (z // 3) % 2 else (c[1], c[0]))
            g += layer_cover(cells, z, 'brick', LBG, f'tw{z}_')
            z += 3
        else:
            g += layer_cover(live, z, 'plate', LBG, f'tp{z}_')
            z += 1
    # 45 deg slopes on each step of the south face (3040b facing -y): stud row = step row + 1
    for c in tcells:
        d = c[1] - Y_OUT - 0.5
        if d in (1.0, 2.0) and (c[0], c[1] - 1) in tcells:
            g.append(P('3040b', LBG, c[0], c[1], zmax((c[0], c[1] - 1)), rot=180, tag=f'tsl{c}'))
    # bridges: glass band + parapet above each band
    for zb, name in BRIDGES:
        row = [(x + 0.5, BRIDGE_Y[0] + 0.5) for x in range(XL, XR)]
        g += layer_cover(row, zb + 2, 'plate', 0, f'br{name}_glass')
        g += layer_cover(row, zb + 3, 'plate', LBG, f'br{name}_shut')
    # pinnacles on the two testeros (front corners)
    for (x, y) in ((XL - 0.5, Y_OUT + 3.5), (XR + 0.5, Y_OUT + 3.5)):
        g.append(P('85861', LBG, x, y, Z_TOP, tag=f'pin{x}{y}_base'))
        g.append(P('24482', WHITE, x, y, Z_TOP + 1, tag=f'pin{x}{y}', zoff=4))
    g += stairs()
    return g

def stairs():
    """Steps from the podium (z2) at y=-18 up to terrace level (z18) at y=-11 (7 steps), 3 wide.
    The last step stops 1 stud short of the J1 joints of the two end gajos."""
    g = []
    x0, x1 = -3, 0
    for k in range(7):
        y0 = -18 + k
        h = round(16 * (k + 1) / 7)          # plates above podium top
        z = 2
        while h - (z - 2) >= 3:
            g.append(box('brick', LBG, x0, x1, y0, y0 + 1, z, f'st{k}_{z}')); z += 3
        while z - 2 < h:
            g.append(box('plate', LBG, x0, x1, y0, y0 + 1, z, f'st{k}_{z}')); z += 1
    return g

def studded_cells():
    """Podium cells that must expose studs (testeros, bridges' feet, stairs)."""
    cells = set(testero_cells())
    cells |= {(x + 0.5, y + 0.5) for x in range(-3, 0) for y in range(-18, -11)}
    return cells

if __name__ == '__main__':
    g = build()
    print('entrada parts', len(g))
    ends = end_gajos()
    print('hits vs end gajos', collide.pair_hits(g, ends)[:10], 'self', collide.pair_hits(g)[:10])
