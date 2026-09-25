"""Minimal LDraw toolkit: library lookup, BFC-aware flattening to triangles, LDCad shadow snaps, MPD writing.

Coordinates are LDraw LDU (1 stud = 20, 1 plate = 8, -Y is up).
"""
from __future__ import annotations
import os, re, functools, pickle, hashlib
from dataclasses import dataclass, field
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LDRAW = os.path.join(ROOT, 'tools', 'ldraw')
SHADOW = os.path.join(ROOT, 'tools', 'shadow')
CACHE = os.path.join(ROOT, '.cache'); os.makedirs(CACHE, exist_ok=True)

# ----------------------------------------------------------------------------- library lookup
def _index(base, subs):
    idx = {}
    for sub in subs:
        d = os.path.join(base, sub)
        for dp, _, fs in os.walk(d):
            rel = os.path.relpath(dp, d)
            for f in fs:
                key = (f if rel == '.' else os.path.join(rel, f)).replace(os.sep, '\\').lower()
                idx.setdefault((sub, key), os.path.join(dp, f))
    return idx

@functools.lru_cache(None)
def _lib_index():
    return _index(LDRAW, ['parts', 'p', 'models'])

@functools.lru_cache(None)
def _shadow_index():
    return _index(SHADOW, ['parts', 'p'])

def norm(name):
    return name.strip().replace('/', '\\').lower()

def find(name, prefer=None):
    """Return (kind, path) for an LDraw reference; kind in parts/p/models."""
    n = norm(name); idx = _lib_index()
    order = ['parts', 'p', 'models'] if prefer != 'p' else ['p', 'parts', 'models']
    for sub in order:
        p = idx.get((sub, n))
        if p: return sub, p
    return None, None

def shadow_path(kind, name):
    return _shadow_index().get((kind, norm(name)))

@functools.lru_cache(None)
def read_lines(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        return fh.read().splitlines()

def part_title(name):
    k, p = find(name)
    if not p: return None
    for l in read_lines(p):
        if l.startswith('0 '): return l[2:].strip()
    return ''

def official(name):
    """True if the part file carries an official LDraw !LDRAW_ORG header (not Unofficial)."""
    k, p = find(name)
    if not p or k != 'parts': return False
    for l in read_lines(p)[:12]:
        if l.startswith('0 !LDRAW_ORG'): return 'Unofficial' not in l
    return False

def mat(vals):
    x, y, z, a, b, c, d, e, f, g, h, i = map(float, vals)
    M = np.eye(4); M[:3, :3] = [[a, b, c], [d, e, f], [g, h, i]]; M[:3, 3] = [x, y, z]
    return M

# ----------------------------------------------------------------------------- geometry (BFC aware)
def _geom_raw(name, kind_hint=None):
    """Triangles of a file in its own coords with outward (CCW) winding when certified. Returns (tris, certified)."""
    kind, path = find(name, kind_hint)
    if not path: return np.zeros((0, 3, 3), np.float32), True
    tris = []; certified = False; ccw = True; invert_next = False
    for l in read_lines(path):
        t = l.split()
        if not t: continue
        if t[0] == '0':
            if len(t) >= 3 and t[1] == 'BFC':
                w = t[2:]
                if 'CERTIFY' in w: certified = True; ccw = 'CW' not in w
                if 'CW' in w and 'CERTIFY' not in w: ccw = False
                if 'CCW' in w and 'CERTIFY' not in w: ccw = True
                if 'INVERTNEXT' in w: invert_next = True
            continue
        if t[0] == '1' and len(t) >= 15:
            M = mat(t[2:14]); sub = ' '.join(t[14:])
            st, sc = geom(sub, 'p' if kind == 'p' else None)
            inv = invert_next; invert_next = False
            if len(st):
                v = st.reshape(-1, 3) @ M[:3, :3].T + M[:3, 3]
                v = v.reshape(-1, 3, 3)
                flip = (np.linalg.det(M[:3, :3]) < 0) ^ inv
                if flip: v = v[:, ::-1]
                tris.append(v)
            continue
        invert_next = False
        if t[0] == '3' and len(t) >= 11:
            v = np.array(t[2:11], float).reshape(1, 3, 3)
            tris.append(v if ccw else v[:, ::-1])
        elif t[0] == '4' and len(t) >= 14:
            q = np.array(t[2:14], float).reshape(4, 3)
            v = np.stack([q[[0, 1, 2]], q[[0, 2, 3]]])
            tris.append(v if ccw else v[:, ::-1])
    out = np.concatenate(tris).astype(np.float32) if tris else np.zeros((0, 3, 3), np.float32)
    return out, certified

@functools.lru_cache(None)
def geom(name, kind_hint=None):
    return _geom_raw(name, kind_hint)

def part_mesh(name):
    """Cached (vertices, faces) for a part (deduplicated)."""
    key = hashlib.md5(norm(name).encode()).hexdigest()
    cp = os.path.join(CACHE, f'mesh_{key}.pkl')
    if os.path.exists(cp):
        return pickle.load(open(cp, 'rb'))
    tris, cert = geom(name)
    v = tris.reshape(-1, 3).round(3)
    uv, inv = np.unique(v, axis=0, return_inverse=True)
    f = inv.reshape(-1, 3)
    f = f[(f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])]
    res = (uv.astype(np.float64), f.astype(np.int64))
    pickle.dump(res, open(cp, 'wb'))
    return res

# ----------------------------------------------------------------------------- shadow snaps
@dataclass
class Snap:
    kind: str            # CYL, CLP, FGR, GEN, SPH
    gender: str          # M / F / ''
    secs: list           # [(shape, radius, length)]
    M: np.ndarray        # 4x4 frame; snap axis = local -Y (cylinder grows along -Y from origin)
    caps: str = 'one'
    id: str = ''
    slide: bool = False
    params: dict = field(default_factory=dict)

    @property
    def length(self): return sum(s[2] for s in self.secs)
    @property
    def radius(self): return max((s[1] for s in self.secs if s[0] in 'RS'), default=0)

_param_re = re.compile(r'\[(\w+)=([^\]]*)\]')

def _parse_grid(g):
    t = g.split(); cx = cz = False; i = 0
    if t[i].upper() == 'C': cx = True; i += 1
    nx = int(t[i]); i += 1
    if t[i].upper() == 'C': cz = True; i += 1
    nz = int(t[i]); i += 1
    sx, sz = float(t[i]), float(t[i + 1])
    xs = [(k - (nx - 1) / 2) * sx if cx else k * sx for k in range(nx)]
    zs = [(k - (nz - 1) / 2) * sz if cz else k * sz for k in range(nz)]
    return [(x, z) for x in xs for z in zs]

def _meta_frame(p):
    F = np.eye(4)
    if 'ori' in p: F[:3, :3] = np.array(p['ori'].split(), float).reshape(3, 3)
    if 'pos' in p: F[:3, 3] = np.array(p['pos'].split(), float)
    return F

def _grid_frames(p):
    F = _meta_frame(p)
    if 'grid' not in p: return [F]
    out = []
    for x, z in _parse_grid(p['grid']):
        T = np.eye(4); T[0, 3] = x; T[2, 3] = z
        out.append(F @ T)
    return out

def _parse_secs(s):
    t = s.split(); out = []
    for i in range(0, len(t) - 2, 3):
        out.append((t[i].upper(), float(t[i + 1]), float(t[i + 2])))
    return out

@functools.lru_cache(None)
def _shadow_own(spath):
    """(own_snaps, clears) declared in one shadow file (in that file's coords)."""
    snaps, clears = [], []
    if not spath: return snaps, clears
    for l in read_lines(spath):
        if not l.startswith('0 !LDCAD '): continue
        body = l[9:].strip(); cmd = body.split()[0]
        p = {k.lower(): v for k, v in _param_re.findall(body)}
        if cmd == 'SNAP_CLEAR':
            clears.append(p.get('id', '*').lower()); continue
        if cmd == 'SNAP_INCL':
            ref = p['ref']
            sp = shadow_path('parts', ref) or shadow_path('p', ref)
            sub = _snaps_of_shadow_file(sp) if sp else []
            for F in _grid_frames(p):
                snaps += [_xf(s, F) for s in sub]
            continue
        kind = cmd.replace('SNAP_', '')
        if kind not in ('CYL', 'CLP', 'FGR', 'GEN', 'SPH'): continue
        secs = _parse_secs(p.get('secs', '')) if 'secs' in p else []
        if kind == 'CLP': secs = [('R', float(p.get('radius', 4)), float(p.get('length', 8)))]
        if kind == 'FGR': secs = [('R', float(p.get('radius', 4)), 0.0)]
        for F in _grid_frames(p):
            snaps.append(Snap(kind, p.get('gender', '').upper(), secs, F, p.get('caps', 'one').lower(),
                              p.get('id', '').lower(), p.get('slide', 'false').lower() == 'true', p))
    return snaps, clears

@functools.lru_cache(None)
def _snaps_of_shadow_file(spath):
    s, _ = _shadow_own(spath); return tuple(s)

def _xf(s, M):
    return Snap(s.kind, s.gender, s.secs, M @ s.M, s.caps, s.id, s.slide, s.params)

@functools.lru_cache(None)
def snaps(name, kind_hint=None):
    """All snaps of an LDraw file in its own coords, inherited through type-1 references."""
    kind, path = find(name, kind_hint)
    if not path: return ()
    inherited = []
    for l in read_lines(path):
        t = l.split()
        if len(t) >= 15 and t[0] == '1':
            M = mat(t[2:14]); sub = ' '.join(t[14:])
            inherited += [_xf(s, M) for s in snaps(sub, 'p' if kind == 'p' else None)]
    own, clears = _shadow_own(shadow_path(kind, name))
    for c in clears:
        inherited = [] if c == '*' else [s for s in inherited if s.id != c]
    out, seen = [], set()
    for s in inherited + own:
        k = (s.kind, s.gender, tuple(s.secs), tuple(np.round(s.M, 3).flatten()))
        if k not in seen: seen.add(k); out.append(s)
    return tuple(out)

# ----------------------------------------------------------------------------- model building / writing
@dataclass
class Placed:
    part: str
    color: int
    M: np.ndarray
    step: int = 0
    tag: str = ''

def fmt(v):
    s = f'{v:.6f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s

def line1(color, M, name):
    R = M[:3, :3]; t = M[:3, 3]
    return '1 %d %s %s %s' % (color, ' '.join(fmt(x) for x in t), ' '.join(fmt(x) for x in R.flatten()), name)

def rot_y(deg):
    """Rotation about LDraw vertical axis. Positive deg = clockwise seen from above (plan azimuth)."""
    a = np.radians(deg); c, s = np.cos(a), np.sin(a)
    M = np.eye(4); M[:3, :3] = [[c, 0, -s], [0, 1, 0], [s, 0, c]]
    return M

def translate(x, y, z):
    M = np.eye(4); M[:3, 3] = [x, y, z]; return M
