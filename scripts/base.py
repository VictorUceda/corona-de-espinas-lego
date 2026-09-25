"""Base: 48x48 baseplate, two-plate podium, hidden setting-out axes and the park round the podium.

* Ejes de replanteo: every podium cell within 1 stud of the E-W or N-S diameter is white at z1 (tiles where
  the ring rests, plates under the core / north gajo / entrance). The ring and the cloister hide them.
* Parque: dark-green lawn in the four corners of the baseplate with micro olive trees
  (two 1x1 round plates as trunk + three 5-petal plates, each turned 24 deg).
"""
import math, os, sys
from kit import P
import core, entrada
from core import cover, coarse_disk, BIG, BIGT

LBG, WHITE, RBROWN, DKGREEN = 71, 15, 70, 288

def axis(c): return abs(c[0]) < 1 or abs(c[1]) < 1

def base():
    g = [P('4186', LBG, 0, 0, 0, tag='baseplate', zoff=0)]
    podium = coarse_disk(23.0)
    pl, _ = cover(podium, 'plate', LBG, 0, 'pod0_', sizes=BIG)
    g += pl
    core_ = set(c for c in podium if max(math.hypot(c[0] + a, c[1] + b) for a in (-.5, .5) for b in (-.5, .5)) < 8.4)
    anchor = {(x, y) for x in (-0.5, 0.5) for y in (13.5, 14.5, 15.5, 16.5)}
    anchor |= entrada.studded_cells()
    ring_zone = [c for c in podium if c not in core_ and c not in anchor]
    for cells, kind, sizes, tag in ((ring_zone, 'tile', BIGT, 'pod1t'), (list(core_ | anchor), 'plate', BIG, 'pod1p')):
        ax = [c for c in cells if axis(c)]
        rest = [c for c in cells if not axis(c)]
        t, left = cover(ax, kind, WHITE, 1, f'{tag}_eje_', sizes=((1, 8), (1, 6), (1, 4), (1, 3), (1, 2), (1, 1), (2, 2)))
        g += t
        t, left2 = cover(rest, kind, LBG, 1, f'{tag}_', sizes=sizes)
        g += t
        if kind == 'tile' and left2:                       # tile leftovers -> plates
            t, _ = cover(list(left2), 'plate', LBG, 1, f'{tag}_x', sizes=BIG)
            g += t
    g += park(set(podium))
    return g

def park(podium):
    """Lawn plates on the baseplate outside the podium + olive trees."""
    lawn = [(x + 0.5, y + 0.5) for x in range(-24, 24) for y in range(-24, 24)
            if (x + 0.5, y + 0.5) not in podium and math.hypot(x + 0.5, y + 0.5) > 23.6]
    g, _ = cover(lawn, 'plate', DKGREEN, 0, 'lawn_', sizes=((2, 8), (2, 6), (2, 4), (2, 3), (1, 6), (1, 4), (1, 3), (1, 2), (1, 1)))
    trees = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for (a, b) in ((22.5, 22.5), (20.5, 22.5), (22.5, 20.5), (23.5, 18.5), (18.5, 23.5)):
                trees.append((sx * a, sy * b))
    for k, (x, y) in enumerate(trees):
        g += [P('6141', RBROWN, x, y, z, tag=f'olivo{k}_tronco{z}') for z in (1, 2)]
        g += [P('24866', DKGREEN, x, y, 3 + i, rot=24 * i, tag=f'olivo{k}_copa{i}') for i in range(3)]
    return g

if __name__ == '__main__':
    import collide, connect, networkx as nx
    b = base()
    G = connect.graph(b)
    print('base parts', len(b), 'hits', collide.pair_hits(b)[:5], 'components', nx.number_connected_components(G))
