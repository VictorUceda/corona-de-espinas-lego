"""Snap-based connectivity between placed parts (LDCad shadow library data).

A connection = male CYL snap coaxial with a female CYL snap (same axis direction, radial offset <= POS_TOL),
overlapping along the axis by >= MIN_OVERLAP LDU, with matching radius on the overlapping female section.
"""
import functools
from collections import defaultdict
import numpy as np
import networkx as nx
import ldr

POS_TOL = 0.05     # LDU, radial misalignment accepted
ANG_TOL = 0.9995   # cos of max axis misalignment (~1.8 deg)
MIN_OVERLAP = 1.0  # LDU

@functools.lru_cache(None)
def local_cyl(part):
    out = []
    for s in ldr.snaps(part):
        if s.kind != 'CYL' or s.gender not in ('M', 'F') or not s.secs: continue
        out.append(s)
    return out

def world_snaps(P):
    """List of (part_idx, gender, origin(3), axis(3), secs, snap)."""
    res = []
    for i, p in enumerate(P):
        for s in local_cyl(p.part):
            W = p.M @ s.M
            res.append((i, s.gender, W[:3, 3], -W[:3, 1] / np.linalg.norm(W[:3, 1]), s.secs, s))
    return res

def _sec_radius_at(secs, t0, t1):
    """Female radius over the axial interval [t0, t1] measured from the female origin (list of (shape, r))."""
    out, a = [], 0.0
    for sh, r, L in secs:
        b = a + L
        if b > t0 + 1e-6 and a < t1 - 1e-6: out.append((sh, r))
        a = b
    return out

def match(m, f):
    """Return overlap length if male snap m fits female snap f, else 0 (axes parallel or antiparallel)."""
    _, _, om, am, sm, _ = m; _, _, of, af, sf, _ = f
    c = float(np.dot(am, af))
    if abs(c) < ANG_TOL: return 0.0
    sgn = 1.0 if c > 0 else -1.0
    d = of - om
    along = np.dot(d, am)
    radial = np.linalg.norm(d - along * am)
    if radial > POS_TOL: return 0.0
    Lm = sum(x[2] for x in sm); Lf = sum(x[2] for x in sf)
    f0, f1 = (along, along + Lf) if sgn > 0 else (along - Lf, along)
    lo, hi = max(0.0, f0), min(Lm, f1)
    ov = hi - lo
    if ov < MIN_OVERLAP: return 0.0
    mr = _sec_radius_at(sm, lo, hi)
    u0, u1 = sorted(((lo - along) * sgn, (hi - along) * sgn))
    fr = _sec_radius_at(sf, u0, u1)
    if not fr or not mr: return 0.0
    # every male section in the overlap must fit the female radius there (use outermost of each)
    rm = max(r for _, r in mr); rf = min(r for _, r in fr)
    if abs(rm - rf) > 0.6: return 0.0
    return ov

def _canon(a):
    a = np.round(a, 2) + 0.0
    k = np.nonzero(np.abs(a) > 1e-6)[0][0]
    return a if a[k] > 0 else -a + 0.0

def connections(P):
    """Return list of (i, j, n_links) and per-link details."""
    W = world_snaps(P)
    males = [w for w in W if w[1] == 'M']; females = [w for w in W if w[1] == 'F']
    # bucket females by (rounded axis, rounded perpendicular coordinates)
    def key(o, a):
        a = np.round(a, 2) + 0.0
        # project origin onto plane perpendicular to axis
        p = o - np.dot(o, a) * a
        return (tuple(a), tuple(np.round(p / 0.5).astype(int)))
    buck = defaultdict(list)
    for f in females:
        a = _canon(f[3])
        p = f[2] - np.dot(f[2], a) * a
        base = np.round(p / 0.5).astype(int)
        buck[(tuple(a), tuple(base))].append(f)
    links = []
    for m in males:
        a = _canon(m[3])
        p = m[2] - np.dot(m[2], a) * a
        base = np.round(p / 0.5).astype(int)
        seen = set()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for f in buck.get((tuple(a), tuple(base + (dx, dy, dz))), ()):
                        if f[0] == m[0] or id(f) in seen: continue
                        seen.add(id(f))
                        ov = match(m, f)
                        if ov > 0: links.append((m[0], f[0], ov, m, f))
    return links

def graph(P, links=None):
    links = connections(P) if links is None else links
    G = nx.Graph(); G.add_nodes_from(range(len(P)))
    for i, j, ov, m, f in links:
        if G.has_edge(i, j): G[i][j]['n'] += 1
        else: G.add_edge(i, j, n=1)
    return G
