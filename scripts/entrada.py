"""Entrance: canyon, two bridges and the stair (layout in entrada_base.py), clipped against the two end gajos.
Testeros are built from plates only, in alternating directions: every plate seam is one board line of the
board-formed concrete ('encofrado de tabla', 8 cm boards on the real walls). No pinnacles: the 55 spikes are all
on the ring, as on the real building.
"""
import os, sys
import entrada_base as e1
from kit import P, box

LBG, WHITE = 71, 15
Z_TOP = 33

def zmax(cell):
    """Stepped south face: P3 + cornice top (z25), roof course (z28), crown (z31), top (z33)."""
    d = cell[1] - e1.Y_OUT - 0.5
    return 25 if d < 1 else 28 if d < 2 else 31 if d < 3 else Z_TOP

def in_slope(c, z, tcells):
    d = c[1] - e1.Y_OUT - 0.5
    if d not in (1.0, 2.0) or (c[0], c[1] - 1) not in tcells: return False
    z0 = zmax((c[0], c[1] - 1))
    return z0 <= z < z0 + 3

def _cover(cells, z, tag):
    # alternate the long direction every layer so the seams bond like masonry
    import core
    sizes = ((2, 8), (2, 6), (2, 4), (2, 3), (2, 2), (1, 8), (1, 6), (1, 4), (1, 3), (1, 2), (1, 1))
    parts, _ = core.cover(cells, 'plate', LBG, z, tag, sizes=sizes, transpose=bool(z % 2))
    return parts

_TC = None
def testero_cells():
    global _TC
    if _TC is None: _TC = e1.testero_cells()
    return _TC

def build():
    g = []
    tcells = testero_cells()
    bridge_layers = {z for zb, _ in e1.BRIDGES for z in (zb, zb + 1)}
    for z in range(2, Z_TOP):
        live = [c for c in tcells if z < zmax(c) and not in_slope(c, z, tcells)]
        if z in bridge_layers:
            g.append(box('plate', LBG, e1.XL - 1, e1.XR + 1, e1.BRIDGE_Y[0], e1.BRIDGE_Y[1], z, f'bridge{z}'))
            span = {(x + 0.5, y + 0.5) for x in range(e1.XL - 1, e1.XR + 1) for y in range(*e1.BRIDGE_Y)}
            live = [c for c in live if c not in span]
        g += _cover(live, z, f'tb{z}_')
    for c in tcells:
        d = c[1] - e1.Y_OUT - 0.5
        if d in (1.0, 2.0) and (c[0], c[1] - 1) in tcells:
            g.append(P('3040b', LBG, c[0], c[1], zmax((c[0], c[1] - 1)), rot=180, tag=f'tsl{c}'))
    for zb, name in e1.BRIDGES:
        row = [(x + 0.5, e1.BRIDGE_Y[0] + 0.5) for x in range(e1.XL, e1.XR)]
        g += [box('plate', 0, e1.XL, e1.XR, e1.BRIDGE_Y[0], e1.BRIDGE_Y[0] + 1, zb + 2, f'br{name}_glass')]
        g += [box('plate', WHITE, e1.XL, e1.XR, e1.BRIDGE_Y[0], e1.BRIDGE_Y[0] + 1, zb + 3, f'br{name}_shut')]
    g += e1.stairs()
    return g

def studded_cells():
    cells = set(testero_cells())
    cells |= {(x + 0.5, y + 0.5) for x in range(-3, 0) for y in range(-18, -11)}
    return cells

if __name__ == '__main__':
    import collide
    g = build()
    ends = e1.end_gajos()
    print('entrada parts', len(g), 'cells', len(testero_cells()))
    print('hits vs end gajos', collide.pair_hits(g, ends)[:10], 'self', collide.pair_hits(g)[:10])
