"""Plan-grid helpers shared by the base, the cloister and the entrance: disks of cells and rectangle covers.

Global grid: origin = building centre, stud centres on half-integers (matches the north gajo's Go grid).
x = east, y = north (studs); z = plates above baseplate top.
"""
import math
from kit import box

LBG, DBG, WHITE, TBLK, TCLR, GREEN = 71, 72, 15, 40, 47, 2

def cells_disk(r_out, r_in=0.0, margin=0.0):
    """Unit cells (cx, cy) whose four corners lie within [r_in, r_out]."""
    n = int(math.ceil(r_out)) + 1; out = []
    for i in range(-n, n):
        for j in range(-n, n):
            cs = [(i + a, j + b) for a in (0, 1) for b in (0, 1)]
            rs = [math.hypot(*c) for c in cs]
            if max(rs) <= r_out - margin and min(rs) >= r_in + margin: out.append((i + 0.5, j + 0.5))
    return out

def cover(cells, kind, color, z, tag, sizes=((6, 6), (4, 8), (4, 6), (4, 4), (2, 8), (2, 6), (2, 4), (2, 3), (2, 2), (1, 4), (1, 3), (1, 2), (1, 1)), avoid_seams=None, transpose=False):
    """Greedy rectangle cover of a cell set with available part sizes (largest first). Returns parts."""
    from kit import SIZES
    left = set(cells); parts = []
    avail = [(a, b) for a, b in sizes if (min(a, b), max(a, b)) in SIZES[kind]]
    for w, d in avail:
        for (a, b) in (((d, w), (w, d)) if transpose else ((w, d), (d, w))):
            for (cx, cy) in sorted(left, key=(lambda c: (c[0], c[1])) if transpose else (lambda c: (c[1], c[0]))):
                if (cx, cy) not in left: continue
                x0, y0 = cx - 0.5, cy - 0.5
                rect = [(x0 + 0.5 + i, y0 + 0.5 + j) for i in range(a) for j in range(b)]
                if all(c in left for c in rect):
                    if avoid_seams and any(s(x0, y0, a, b) for s in avoid_seams): continue
                    parts.append(box(kind, color, x0, x0 + a, y0, y0 + b, z, f'{tag}{len(parts)}'))
                    left -= set(rect)
    return parts, left

BIG = ((16, 16), (8, 16), (6, 16), (8, 8), (6, 12), (6, 10), (6, 8), (4, 12), (4, 10), (6, 6), (4, 8), (4, 6), (4, 4),
       (2, 8), (2, 6), (2, 4), (2, 3), (2, 2), (1, 4), (1, 3), (1, 2), (1, 1))
BIGT = ((6, 6), (2, 6), (2, 4), (2, 2), (1, 4), (1, 3), (1, 2), (1, 1))

def coarse_disk(r, step=2):
    """Cells of a disk quantised to step x step blocks (block kept if its centre is within r)."""
    n = int(r // step) + 1; out = []
    for i in range(-n, n):
        for j in range(-n, n):
            cx, cy = (i + 0.5) * step, (j + 0.5) * step
            if math.hypot(cx, cy) <= r - step * 0.35:
                out += [(i * step + a + 0.5, j * step + b + 0.5) for a in range(step) for b in range(step)]
    return out
