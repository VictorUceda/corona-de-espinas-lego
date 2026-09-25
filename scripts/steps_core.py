"""Step helpers: split a verified build order into steps of 1-8 parts and write one LDR per section with 0 STEP markers.
"""
import json, os
from collections import Counter
import numpy as np
import ldr, kit, collide, connect, verify, build_ring
from ldr import ROOT

OUT = os.path.join(ROOT, 'build', 'instructions')
MAXP = 8

def zb(p): return -collide.aabb(p)[1][1] / 8.0

def chunk(parts, order):
    """Split an ordered list into steps of <= MAXP parts; new step when height jumps > 3 plates."""
    steps, cur, z0 = [], [], None
    for i in order:
        z = zb(parts[i])
        if cur and (len(cur) >= MAXP or abs(z - z0) > 3.01):
            steps.append(cur); cur = []
        if not cur: z0 = z
        cur.append(i)
    if cur: steps.append(cur)
    return steps

def lots(parts, ix, mult=1):
    c = Counter((parts[i].part, parts[i].color) for i in ix)
    return [{'part': p, 'color': col, 'qty': q * mult, 'title': ldr.part_title(p)} for (p, col), q in sorted(c.items())]

def write_ldr(name, parts, steps):
    lines = [f'0 {name}', '0 BFC CERTIFY CCW']
    for s in steps:
        for i in s: lines.append(ldr.line1(parts[i].color, parts[i].M, parts[i].part))
        lines.append('0 STEP')
    open(os.path.join(OUT, name), 'w').write('\n'.join(lines) + '\n')

def section(key, title, parts, order, callout=None, context=None):
    steps = chunk(parts, order)
    ctx = context or []
    allp = ctx + parts
    shift = len(ctx)
    ctx_steps = [list(range(len(ctx)))] if ctx else []
    write_ldr(f'sec_{key}.ldr', allp, ctx_steps + [[i + shift for i in s] for s in steps])
    return {'key': key, 'title': title, 'callout': callout, 'ldr': f'sec_{key}.ldr', 'context_steps': len(ctx_steps),
            'steps': [{'n_parts': len(s), 'parts': lots(parts, s)} for s in steps]}
