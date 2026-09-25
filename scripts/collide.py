"""Mesh collision checks between placed LDraw parts (tolerance: each mesh shrunk by TOL LDU along vertex normals)."""
import functools
import numpy as np
import fcl, trimesh
import ldr

TOL = 0.1
# Official two-piece assemblies whose LDraw meshes interpenetrate by design (pivot pin inside its socket).
# A hit between these is ignored only when the two parts are also linked by their pivot snap (checked by caller).
ASSEMBLY_PAIRS = {frozenset(('2429.dat', '2430.dat'))}

def inset(v, f, tol):
    """Per-vertex displacement that moves every adjacent face plane inwards by `tol` (least squares over the
    distinct adjacent face normals). Plain averaged vertex normals under-shrink flat faces next to finely
    tessellated curves, so touching parts (e.g. 24201 side by side) were reported as colliding."""
    m = trimesh.Trimesh(v, f, process=False)
    fn = m.face_normals
    ok = np.isfinite(fn).all(1) & (np.linalg.norm(fn, axis=1) > 0.5)
    _, cl = np.unique(np.round(v / 0.02), axis=0, return_inverse=True)   # weld near-duplicate vertices
    cl = cl.reshape(-1)
    adj = [[] for _ in range(cl.max() + 1)]
    for fi in np.nonzero(ok)[0]:
        for vi in f[fi]: adj[cl[vi]].append(fi)
    dc = np.zeros((len(adj), 3))
    for ci, fs in enumerate(adj):
        if not fs: continue
        N = np.unique(np.round(fn[fs], 3), axis=0)
        x, *_ = np.linalg.lstsq(N, -tol * np.ones(len(N)), rcond=None)
        nx = np.linalg.norm(x)
        dc[ci] = x if nx <= 3 * tol else x * (3 * tol / nx)
    return dc[cl]

@functools.lru_cache(None)
def shrunk(part):
    v, f = ldr.part_mesh(part)
    vs = v + inset(v, f, TOL)
    bvh = fcl.BVHModel(); bvh.beginModel(len(vs), len(f)); bvh.addSubModel(vs, f); bvh.endModel()
    return bvh, v.min(0), v.max(0)

def _obj(p):
    bvh, _, _ = shrunk(p.part)
    return fcl.CollisionObject(bvh, fcl.Transform(p.M[:3, :3], p.M[:3, 3]))

def aabb(p):
    _, lo, hi = shrunk(p.part)
    c = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    w = c @ p.M[:3, :3].T + p.M[:3, 3]
    return w.min(0), w.max(0)

def candidate_pairs(boxA, boxB=None, pad=0.0):
    """Sweep-and-prune on x; returns index pairs whose AABBs overlap."""
    loA, hiA = boxA
    if boxB is None:
        order = np.argsort(loA[:, 0]); out = []
        for a_i, a in enumerate(order):
            for b in order[a_i + 1:]:
                if loA[b, 0] > hiA[a, 0] + pad: break
                if np.all(loA[b] <= hiA[a] + pad) and np.all(loA[a] <= hiA[b] + pad): out.append((min(a, b), max(a, b)))
        return out
    loB, hiB = boxB; out = []
    for a in range(len(loA)):
        m = np.all(loB <= hiA[a] + pad, 1) & np.all(loA[a] <= hiB + pad, 1)
        out += [(a, int(b)) for b in np.nonzero(m)[0]]
    return out

def boxes(P):
    bb = [aabb(p) for p in P]
    return np.array([b[0] for b in bb]), np.array([b[1] for b in bb])

def collides(p, q):
    r = fcl.CollisionResult()
    return fcl.collide(_obj(p), _obj(q), fcl.CollisionRequest(), r) > 0

def pair_hits(A, B=None):
    """Colliding index pairs within A (B None) or between A and B."""
    cand = candidate_pairs(boxes(A), None if B is None else boxes(B))
    if B is None: return [(i, j) for i, j in cand if collides(A[i], A[j])]
    return [(i, j) for i, j in cand if collides(A[i], B[j])]
