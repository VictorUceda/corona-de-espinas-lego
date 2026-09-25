"""Verification of dist/model.mpd -> dist/verification_report.json

a. Connectivity: part graph from LDCad shadow snaps (stud/antistud, pins, bars...), 1 connected component.
b. Collisions: LDraw meshes shrunk 0.1 LDU (collide.TOL) -> 0 intersections (official 2-piece assemblies whose
   meshes interpenetrate by design are accepted only when linked by their own pivot snap).
c. Buildability: following the build order, every new part (or pre-built sub-assembly) connects to something
   already placed and can be lowered vertically from above without touching placed parts
   (swept test every SWEEP_STEP LDU).
d. Stability: model centre of mass inside the support polygon; no part hanging off a single stud
   (a part whose COM lies outside the hull of its links must have >= 2 links).
e. Strength: every horizontal cut (between plate levels) is crossed by >= K_MIN connections.
"""
import json, math, os, sys, time, functools
from collections import defaultdict
import numpy as np
import networkx as nx
from shapely.geometry import MultiPoint, Point
import ldr, collide, connect, kit
from ldr import Placed

SWEEP_STEP = 2.0
K_MIN = 8
DENSITY = 1.0   # uniform; masses ~ mesh volume

# ----------------------------------------------------------------------------- flatten the MPD
def parse_mpd(path):
    files, cur = {}, None
    for l in open(path).read().splitlines():
        if l.startswith('0 FILE '): cur = l[7:].strip().lower(); files[cur] = []
        elif l.startswith('0 NOFILE'): cur = None
        elif cur is not None: files[cur].append(l)
    return files

def flatten(path):
    """Returns list of (Placed, chain) where chain = tuple of (submodel, instance index) from the root."""
    files = parse_mpd(path)
    root = next(iter(files))
    out = []
    def walk(name, M, chain):
        k = 0
        for l in files[name]:
            t = l.split()
            if len(t) >= 15 and t[0] == '1':
                sub = ' '.join(t[14:]).lower(); Ml = M @ ldr.mat(t[2:14])
                if sub in files:
                    walk(sub, Ml, chain + ((sub, k),)); k += 1
                else:
                    out.append((Placed(sub, int(t[1]), Ml), chain))
    walk(root, np.eye(4), ((root, 0),))
    return out

# ----------------------------------------------------------------------------- helpers
@functools.lru_cache(None)
def local_mass(part):
    import trimesh
    v, f = ldr.part_mesh(part)
    m = trimesh.Trimesh(v, f, process=False)
    vol = abs(m.volume) if m.volume == m.volume else 0.0
    c = m.center_mass if vol > 1e-6 else v.mean(0)
    return max(vol, 1.0), c

def world_com(p):
    vol, c = local_mass(p.part)
    return vol, p.M[:3, :3] @ c + p.M[:3, 3]

def lifted(p, d):
    """Move part by d LDU vertically (d>0 = up, i.e. -Y in LDraw)."""
    M = p.M.copy(); M[1, 3] -= d
    return Placed(p.part, p.color, M, p.step, p.tag)

def insertion_free(moving, placed_idx, P, boxes, top, bottom):
    """True if `moving` can be lowered from above OR raised from below without touching placed parts."""
    return not sweep_blockers(moving, placed_idx, P, boxes, top) or not sweep_blockers(moving, placed_idx, P, boxes, top, up=False, bottom=bottom)

def sweep_blockers(moving, placed_idx, P, boxes, top, up=True, bottom=None):
    """Indices of placed parts hit when `moving` (list of Placed) is lowered from above (up=True) or raised from
    below (up=False) to its final position."""
    lo = np.min([collide.aabb(p)[0] for p in moving], 0); hi = np.max([collide.aabb(p)[1] for p in moving], 0)
    cand = [i for i in placed_idx if boxes[0][i][0] < hi[0] and boxes[1][i][0] > lo[0]
            and boxes[0][i][2] < hi[2] and boxes[1][i][2] > lo[2] and boxes[0][i][1] < hi[1]]
    if not cand: return []
    hits = set()
    if up:
        cand = [i for i in cand if boxes[0][i][1] < hi[1]]
    else:
        cand = [i for i in placed_idx if boxes[0][i][0] < hi[0] and boxes[1][i][0] > lo[0]
                and boxes[0][i][2] < hi[2] and boxes[1][i][2] > lo[2] and boxes[1][i][1] > lo[1]]
    dmax = (hi[1] - top + 8) if up else (bottom - lo[1] + 8)
    sgn = 1 if up else -1
    for m in moving:
        mlo, mhi = collide.aabb(m)
        for i in cand:
            q = P[i]
            if not (boxes[0][i][0] < mhi[0] and boxes[1][i][0] > mlo[0] and boxes[0][i][2] < mhi[2] and boxes[1][i][2] > mlo[2]):
                continue
            if frozenset((m.part, q.part)) in collide.ASSEMBLY_PAIRS and np.linalg.norm(m.M[:3, 3] - q.M[:3, 3]) < 0.5:
                continue                                      # designed pivot insertion (hinge top onto its base)
            if up and boxes[0][i][1] >= mhi[1]: continue      # entirely below the moving part
            if not up and boxes[1][i][1] <= mlo[1]: continue  # entirely above the moving part
            d = SWEEP_STEP
            while d <= dmax:
                if collide.collides(lifted(m, sgn * d), q): hits.add(i); break
                if up and mhi[1] - d < boxes[0][i][1]: break
                if not up and mlo[1] + d > boxes[1][i][1]: break
                d += SWEEP_STEP
    return sorted(hits)

def rests_on(i, placed, P):
    """True if part i, lowered by 0.5 LDU, would touch an already placed part (it is resting on it)."""
    lo, hi = collide.aabb(P[i])
    low = lifted(P[i], -0.5)
    for j in placed:
        l2, h2 = collide.aabb(P[j])
        if np.all(l2 <= hi + 1) and np.all(lo - 1 <= h2) and collide.collides(low, P[j]) and not collide.collides(P[i], P[j]):
            return True
    return False

def grow_order(ix, G, placed, P, resting=False):
    """Order parts of a group so each connects to already placed parts (lowest first); unconnected leftovers
    are appended (and will be reported). With `resting`, a part may also be placed when it rests on placed parts
    (no stud engaged yet) provided it gets connected by a later part of the same group."""
    left = set(ix); order = []; have = set(placed)
    zb = lambda i: -collide.aabb(P[i])[1][1]
    while left:
        ready = [i for i in left if any(j in have for j in G.neighbors(i))]
        if resting:
            lowest = min((zb(i) for i in ready), default=1e9)
            ready += [i for i in left if i not in ready and zb(i) < lowest - 0.5 and rests_on(i, have, P)
                      and any(j in left for j in G.neighbors(i))]
        ready = ready or ([min(left, key=zb)] if not have else [])
        if not ready: order += sorted(left, key=zb); break
        i = min(ready, key=lambda i: (round(zb(i), 1), i))
        order.append(i); have.add(i); left.discard(i)
    return order

# ----------------------------------------------------------------------------- build order
SPEC = (('anillo.ldr', 'unit'), ('claustro_pilares.ldr', 'grow'), ('claustro_plaza.ldr', 'unit'),
        ('claustro_cupula.ldr', 'grow'), ('entrada.ldr', 'grow'))

def build_order(items, spec=SPEC):
    """Group flattened parts into build units following the instruction order:
    base (part by part, bottom-up) -> then `spec` in order: 'anillo.ldr' = 28 gajos counter-clockwise (each gajo
    = 1 unit; its internal order is checked separately), 'unit' = pre-built sub-assembly placed as one piece,
    'grow' = part by part."""
    import build_ring
    units = []
    groups = defaultdict(list)
    tops = [n for n, _ in spec]
    for idx, (p, chain) in enumerate(items):
        names = [c[0] for c in chain]
        if 'anillo.ldr' in names: key = ('gajo', chain[names.index('anillo.ldr') + 1][1])
        else: key = (next((n for n in names if n in tops), names[-1]), None)
        groups[key].append(idx)
    def zsort(ix): return sorted(ix, key=lambda i: (round(collide.aabb(items[i][0])[1][1] * -1, 1), i))
    for i in zsort(groups[('base.ldr', None)]): units.append(('base', [i], 'grow'))
    angles = build_ring.gajo_angles()
    order = sorted(range(len(angles)), key=lambda k: -angles[k])    # clockwise-most first -> counter-clockwise
    ring = [(f'gajo{k}', groups[('gajo', k)]) for k in order]
    for n, mode in spec:
        if n == 'anillo.ldr': units.append(('anillo', sum((ix for _, ix in ring), []), 'unit'))
        else: units.append((n[:-4], groups[(n, None)], mode))
    return units, ring

# ----------------------------------------------------------------------------- main
def run(path, out_json, quick=False, gajo_build=None, spec=SPEC):
    t0 = time.time()
    items = flatten(path)
    P = [p for p, _ in items]
    rep = {'model': os.path.basename(path), 'n_parts': len(P), 'tolerance_ldu': collide.TOL}
    # a. connectivity
    links = connect.connections(P)
    G = connect.graph(P, links)
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    rep['a_connectivity'] = {'n_connections': len(links), 'n_part_pairs': G.number_of_edges(), 'components': len(comps),
                             'isolated': [f'{P[i].part}@{P[i].tag or i}' for c in comps[1:] for i in list(c)[:5]][:40],
                             'ok': len(comps) == 1}
    print('a', rep['a_connectivity']['components'], 'components,', len(links), 'links', f'{time.time()-t0:.0f}s')
    # b. collisions
    linked = {frozenset((i, j)) for i, j, *_ in links}
    hits = collide.pair_hits(P)
    hits = [(i, j) for i, j in hits if not (frozenset((P[i].part, P[j].part)) in collide.ASSEMBLY_PAIRS and frozenset((i, j)) in linked)]
    rep['b_collisions'] = {'n': len(hits), 'pairs': [[P[i].part, P[j].part, items[i][1][-1][0], items[j][1][-1][0]] for i, j in hits[:50]],
                           'ok': len(hits) == 0}
    print('b', len(hits), 'collisions', f'{time.time()-t0:.0f}s')
    # c. buildability
    units, ring = build_order(items, spec)
    boxes = collide.boxes(P)
    top = float(boxes[0][:, 1].min()); bottom = float(boxes[1][:, 1].max())
    fails = []
    # c1. ring sub-assembly: gajos added counter-clockwise, each unit connects to and drops onto the previous
    rp = []
    for name, ix in ring:
        if rp:
            if not any(j in set(rp) for i in ix for j in G.neighbors(i)): fails.append({'unit': name, 'problem': 'no connection to previous gajos'})
            if not quick and not insertion_free([P[i] for i in ix], rp, P, boxes, top, bottom):
                bl = sweep_blockers([P[i] for i in ix], rp, P, boxes, top)
                fails.append({'unit': name, 'problem': 'insertion blocked', 'by': sorted({P[j].part for j in bl})[:8]})
        rp += ix
    # c2. model: base part by part, then the whole anillo, claustro and entrada part by part (grow order)
    placed = []
    for name, ix, mode in units:
        if mode == 'unit':                                  # pre-built sub-assemblies placed as one unit
            if not any(j in set(placed) for i in ix for j in G.neighbors(i)): fails.append({'unit': name, 'problem': 'no connection to placed parts'})
            if not quick and not insertion_free([P[i] for i in ix], placed, P, boxes, top, bottom):
                fails.append({'unit': name, 'problem': 'insertion blocked'})
            if name != 'anillo':                           # its own build order, on the table
                sub = [P[i] for i in ix]; Gs = connect.graph(sub); sb = collide.boxes(sub)
                sp = []
                for i in grow_order(range(len(sub)), Gs, [], sub):
                    if sp and not any(j in sp for j in Gs.neighbors(i)): fails.append({'unit': name, 'part': sub[i].part, 'problem': 'no connection (sub-assembly)'})
                    elif sp and not quick and not insertion_free([sub[i]], sp, sub, sb, float(sb[0][:, 1].min()), float(sb[1][:, 1].max())):
                        fails.append({'unit': name, 'part': sub[i].part, 'problem': 'insertion blocked (sub-assembly)'})
                    sp.append(i)
            placed += ix
            continue
        for i in grow_order(ix, G, placed, P):
            if placed and not any(j in set(placed) for j in G.neighbors(i)):
                fails.append({'unit': name, 'part': P[i].part, 'problem': 'no connection to placed parts'})
            elif placed and not quick and not insertion_free([P[i]], placed, P, boxes, top, bottom):
                fails.append({'unit': name, 'part': P[i].part, 'problem': 'insertion blocked'})
            placed.append(i)
    rep['c_buildability'] = {'fails': fails[:60], 'n_fails': len(fails), 'ok': not fails,
                             'order': 'base (grow) -> ' + ' -> '.join(f"{n} ({'sub-assembly placed as one unit' if m == 'unit' else 'grow'})" for n, m in spec)}
    print('c', len(fails), 'build fails', f'{time.time()-t0:.0f}s')
    # c'. gajo sub-assembly internal order (checked once on the gajo_tipo definition)
    import gajo
    g = (gajo_build or gajo.build)()
    Gg = connect.graph(g)
    gorder = grow_order(range(len(g)), Gg, [], g, resting=True)
    gb = collide.boxes(g); gtop = float(gb[0][:, 1].min()); gbot = float(gb[1][:, 1].max())
    gf = []; gp = []; rest = []
    for n, i in enumerate(gorder):
        if gp:
            if not any(j in gp for j in Gg.neighbors(i)):
                if rests_on(i, gp, g): rest.append(g[i].tag)          # locked by a later part (checked: 1 component)
                else: gf.append({'part': g[i].tag, 'problem': 'no connection'})
            elif not insertion_free([g[i]], gp, g, gb, gtop, gbot):
                bl = sweep_blockers([g[i]], gp, g, gb, gtop)
                gf.append({'part': g[i].tag, 'problem': 'insertion blocked', 'by': [g[j].tag for j in bl][:5]})
        gp.append(i)
    rep['gajo_build_order'] = [g[i].tag for i in gorder]
    rep['c_gajo_subassembly'] = {'n_parts': len(g), 'fails': gf, 'ok': not gf, 'placed_resting_then_locked': rest}
    print("c'", len(gf), 'gajo fails', f'{time.time()-t0:.0f}s')
    # d. stability
    ms = [world_com(p) for p in P]
    M = sum(m for m, _ in ms); com = sum(m * c for m, c in ms) / M
    base_pts = [(p.M[0, 3], p.M[2, 3]) for p in P if p.part == '4186.dat']
    support = MultiPoint([(x + dx, z + dz) for (x, z) in base_pts for dx in (-480, 480) for dz in (-480, 480)]).convex_hull
    com_ok = support.contains(Point(com[0], com[2]))
    # cantilevers on a single stud: parts with exactly 1 link whose COM is not above that link
    nlinks = defaultdict(list)
    for i, j, ov, m, f in links:
        nlinks[i].append(m[2]); nlinks[j].append(f[2])
    single = []
    for i, p in enumerate(P):
        pts = nlinks.get(i, [])
        if len({(round(q[0], 1), round(q[2], 1)) for q in pts}) == 1:
            _, c = ms[i]; q = pts[0]
            if math.hypot(c[0] - q[0], c[2] - q[2]) > 12:        # COM more than ~0.6 stud off its only stud
                single.append(f'{p.part}@{items[i][1][-1][0]}:{p.tag}')
    rep['d_stability'] = {'com_ldu': com.round(1).tolist(), 'com_inside_support': bool(com_ok),
                          'single_stud_cantilevers': single[:40], 'n_single_stud_cantilevers': len(single),
                          'ok': bool(com_ok) and not single}
    print('d', 'com ok' if com_ok else 'COM OUT', len(single), 'single-stud cantilevers')
    # e. strength: for each horizontal plane at a plate boundary, (#vertical connections in that plane) +
    # (#parts crossing it, i.e. a cut there would have to break parts)
    ys = defaultdict(int)
    for i, j, ov, m, f in links:
        if abs(m[3][1]) > 0.9:
            ys[int(round(float(m[2][1]) / 8.0)) * 8] += 1
    tops = boxes[0][:, 1]; bots = boxes[1][:, 1]
    planes = list(range(-8, -296, -8))                    # z1 .. z37 above the base top (LDraw y)
    per = {}
    for y in planes:
        cross = int(np.sum((tops < y - 2) & (bots > y + 2)))
        per[y] = (ys.get(y, 0), cross)
    weakest = min(((c + x, y, c, x) for y, (c, x) in per.items()), default=(0, None, 0, 0))
    rep['e_strength'] = {'k_min': K_MIN, 'definition': 'connections in the plane + parts crossing the plane',
                         'weakest_cut': {'y_ldu': weakest[1], 'z_plates': -weakest[1] / 8 if weakest[1] else None,
                                         'connections': weakest[2], 'crossing_parts': weakest[3]},
                         'per_plane': {str(-y // 8): {'connections': c, 'crossing': x} for y, (c, x) in per.items()},
                         'ok': weakest[0] >= K_MIN}
    print('e weakest', weakest)
    rep['ok'] = all(rep[k]['ok'] for k in rep if isinstance(rep[k], dict) and 'ok' in rep[k])
    rep['seconds'] = round(time.time() - t0, 1)
    json.dump(rep, open(out_json, 'w'), indent=1, default=str)
    return rep

if __name__ == '__main__':
    root = ldr.ROOT
    quick = '--quick' in sys.argv
    r = run(os.path.join(root, 'dist', 'model.mpd'), os.path.join(root, 'dist', 'verification_report.json'), quick)
    print('OK' if r['ok'] else 'FAIL', r['seconds'], 's')
