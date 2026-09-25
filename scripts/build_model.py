"""Compose dist/model.mpd: base, claustro (pilares / plaza / cupula), 28 gajos (anillo), entrada.

The last clockwise gajo is 'gajo_fin' = gajo_tipo without its rib spike: 27 x 2 + 1 = 55 spikes, and the rib at
the canyon edge is bare, as on the real building (data/reference.json: 'nervios_sin_espina').
"""
import os, sys
import numpy as np
import kit, build_ring
from ldr import ROOT
import gajo, claustro, base, entrada

CUPULA = ('lantern_p', 'dome')
PLAZA = ('ballena_', 'slabA_', 'slabB_', 'plaza_', 'wing', 'caseton')

def split_claustro():
    c = claustro.build()
    cup = [p for p in c if p.tag.startswith(CUPULA)]
    plaza = [p for p in c if p.tag.startswith(PLAZA)]
    pil = [p for p in c if not p.tag.startswith(CUPULA + PLAZA)]
    return pil, plaza, cup

def submodels():
    g = gajo.build()
    fin = [p for p in g if p.tag not in ('spk_cone1.5', 'spk1.5')]
    pil, plaza, cup = split_claustro()
    angles = build_ring.gajo_angles()
    last = max(range(len(angles)), key=lambda k: angles[k])
    ring = [('gajo_fin.ldr' if k == last else 'gajo_tipo.ldr', kit.frame(a), 16) for k, a in enumerate(angles)]
    subs = {
        'base.ldr': base.base(),
        'claustro_pilares.ldr': pil, 'claustro_plaza.ldr': plaza, 'claustro_cupula.ldr': cup,
        'gajo_tipo.ldr': g, 'gajo_fin.ldr': fin,
        'anillo.ldr': ring,
        'entrada.ldr': entrada.build(),
    }
    main = [(n, np.eye(4), 16) for n in ('base.ldr', 'anillo.ldr', 'claustro_pilares.ldr', 'claustro_plaza.ldr',
                                         'claustro_cupula.ldr', 'entrada.ldr')]
    return {'model.ldr': main, **subs}

def write(path=os.path.join(ROOT, 'dist', 'model.mpd')):
    subs = submodels()
    open(path, 'w').write(kit.mpd(subs, 'model.ldr'))
    return path, subs

if __name__ == '__main__':
    p, subs = write()
    n = {k: len(v) for k, v in subs.items()}
    total = sum(n[k] for k in ('base.ldr', 'claustro_pilares.ldr', 'claustro_plaza.ldr', 'claustro_cupula.ldr', 'entrada.ldr'))
    total += n['gajo_tipo.ldr'] * 27 + n['gajo_fin.ldr']
    print(p, n, 'total parts', total)
