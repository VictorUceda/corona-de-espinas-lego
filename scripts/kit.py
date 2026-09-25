"""Design kit: gajo-local placement helpers and neighbour checks.

Gajo frame (plan): x = tangential (studs, + = clockwise/right looking outwards), y = radial outwards (studs),
z = height in plates above the base top. LDraw: X = x*20, Z = -y*20, Y = -z*8 - (part bottom offset).
"""
import math, functools
import numpy as np
import ldr, collide, connect
from ldr import Placed, rot_y, translate

SCALE_M_PER_STUD = 2.15
ALPHA = 2 * math.degrees(math.atan(1 / 9.5))      # 12.0214 deg, exact gajo angle (hinge geometry)
J1 = (1.0, 9.5)                                   # inner joint on the right rib
J2 = (2.0, 19.0)                                  # outer joint on the right rib

@functools.lru_cache(None)
def bottom(part):
    v, _ = ldr.part_mesh(part)
    return float(v[:, 1].max())

def P(part, color, x, y, z, rot=0, tag='', zoff=None):
    """Place `part` with its origin above plan point (x, y) [studs], bottom face at plate level z, rotated `rot` deg."""
    if not part.endswith('.dat'): part += '.dat'
    b = bottom(part) if zoff is None else zoff
    M = translate(x * 20, -z * 8 - b, -y * 20) @ rot_y(rot)
    return Placed(part, color, M, tag=tag)

def frame(deg):
    return rot_y(deg)

def xform(parts, M):
    return [Placed(p.part, p.color, M @ p.M, p.step, p.tag) for p in parts]

def check_ring(parts, verbose=True, label='gajo'):
    """Self collisions, collisions with right neighbour (rotated +ALPHA), links to neighbour, isolated parts."""
    rep = {}
    self_hits = collide.pair_hits(parts)
    nb = xform(parts, frame(ALPHA))
    nb_hits = collide.pair_hits(parts, nb)
    both = parts + nb
    links = connect.connections(both)
    n = len(parts)
    linked = {frozenset((i, j)) for i, j, *_ in links}
    def ok_asm(a, b, ia, ib):
        return frozenset((a.part, b.part)) in collide.ASSEMBLY_PAIRS and frozenset((ia, ib)) in linked
    self_hits = [(i, j) for i, j in self_hits if not ok_asm(parts[i], parts[j], i, j)]
    nb_hits = [(i, j) for i, j in nb_hits if not ok_asm(parts[i], nb[j], i, j + n)]
    cross = [(i, j - n) for i, j, *_ in links if i < n <= j] + [(j, i - n) for i, j, *_ in links if j < n <= i]
    G = connect.graph(parts)
    import networkx as nx
    comps = list(nx.connected_components(G))
    rep = dict(n=n, self_hits=[(parts[i].part, parts[i].tag, parts[j].part, parts[j].tag) for i, j in self_hits],
               nb_hits=[(parts[i].part, parts[i].tag, nb[j].part, nb[j].tag) for i, j in nb_hits],
               cross_links=sorted(set((parts[i].tag or parts[i].part, parts[j].tag or parts[j].part) for i, j in cross)),
               components=len(comps),
               small_components=[[parts[i].tag or parts[i].part for i in c] for c in comps if len(c) < max(len(x) for x in comps)])
    if verbose:
        print(f'[{label}] parts={n} self_hits={len(self_hits)} nb_hits={len(nb_hits)} cross_links={len(cross)} components={len(comps)}')
        for h in rep['self_hits'][:15]: print('   self', h)
        for h in rep['nb_hits'][:15]: print('   nb  ', h)
        for c in rep['small_components'][:10]: print('   island', c)
    return rep

def mpd(submodels, main):
    """submodels: dict name -> list of Placed or (name, M) refs; returns MPD text with `main` first."""
    order = [main] + [k for k in submodels if k != main]
    out = []
    for name in order:
        out += [f'0 FILE {name}', f'0 {name[:-4]}', f'0 Name: {name}', '0 Author: Corona LEGO build', '0 BFC CERTIFY CCW']
        items = submodels[name]
        last_step = None
        for it in items:
            if isinstance(it, Placed):
                if last_step is not None and it.step != last_step: out.append('0 STEP')
                last_step = it.step
                out.append(ldr.line1(it.color, it.M, it.part))
            else:
                ref, M, col = it if len(it) == 3 else (*it, 16)
                out.append(ldr.line1(col, M, ref))
        out += ['0 STEP', '0 NOFILE', '']
    return '\n'.join(out)

# ----------------------------------------------------------------------------- rectangular parts by cell edges
SIZES = {
    'plate': {(1, 1): '3024', (1, 2): '3023b', (1, 3): '3623', (1, 4): '3710', (1, 6): '3666', (1, 8): '3460',
              (2, 2): '3022', (2, 3): '3021', (2, 4): '3020', (2, 6): '3795', (2, 8): '3034', (2, 10): '3832',
              (4, 4): '3031', (4, 6): '3032', (4, 8): '3035', (4, 10): '3030', (4, 12): '3029', (6, 6): '3958',
              (6, 8): '3036', (6, 10): '3033', (6, 12): '3028', (6, 14): '3456', (6, 16): '3027', (8, 8): '41539',
              (8, 16): '92438', (16, 16): '91405'},
    'brick': {(1, 1): '3005', (1, 2): '3004', (1, 3): '3622', (1, 4): '3010', (1, 6): '3009', (1, 8): '3008',
              (2, 2): '3003', (2, 3): '3002', (2, 4): '3001', (2, 6): '2456', (2, 8): '3007'},
    'tile': {(1, 1): '3070b', (1, 2): '3069b', (1, 3): '63864', (1, 4): '2431', (1, 6): '6636', (1, 8): '4162',
             (2, 2): '3068b', (2, 4): '87079', (2, 6): '69729', (6, 6): '10202'},
}
HEIGHT = {'plate': 1, 'brick': 3, 'tile': 1}

def box(kind, color, x0, x1, y0, y1, z, tag=''):
    """Rectangular plate/brick/tile covering plan cells [x0,x1]x[y0,y1] (stud edges), bottom at plate z."""
    w, d = round(x1 - x0), round(y1 - y0)
    key = (min(w, d), max(w, d))
    part = SIZES[kind].get(key)
    if part is None: raise ValueError(f'no {kind} {key}')
    rot = 0 if w >= d else 90
    return P(part, color, (x0 + x1) / 2, (y0 + y1) / 2, z, rot=rot, tag=tag)
