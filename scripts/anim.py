"""Animation data for the viewer: the verified build order of dist/model.mpd -> build/anim_order.json, then
dist/model_packed.mpd, build/viewer.html (for render/record.mjs) and the standalone dist/visor_3D.html.
"""
import json, os, sys
import numpy as np
import verify, connect, build_ring, kit, pack
from ldr import ROOT
import gajo

def main():
    items = verify.flatten(os.path.join(ROOT, 'dist', 'model.mpd'))
    P = [p for p, _ in items]
    G = connect.graph(P)
    units, ring = verify.build_order(items, verify.SPEC)
    groups = {}
    for name, ix, _ in units: groups.setdefault(name, []).extend(ix)
    g = gajo.build(); Gg = connect.graph(g)
    gorder = verify.grow_order(range(len(g)), Gg, [], g, resting=True)
    key = lambda part, M: (part, tuple(np.round(M[:3, 3], 2)), tuple(np.round(M[:3, :3], 3).flatten()))
    rank = {key(g[i].part, g[i].M): r for r, i in enumerate(gorder)}
    angles = build_ring.gajo_angles()
    order, steps = [], []
    def add(ix, label):
        if not ix: return
        steps.append({'label': label, 'start': len(order), 'end': len(order) + len(ix)}); order.extend(int(i) for i in ix)
    base = verify.grow_order(groups['base'], G, [], P)
    for k in range(0, len(base), 8): add(base[k:k + 8], 'Base y podio')
    placed = list(base)
    for n, (name, ix) in enumerate(ring, 1):
        Finv = np.linalg.inv(kit.frame(angles[int(name[4:])]))
        assert all(key(P[i].part, Finv @ P[i].M) in rank for i in ix), name
        add(sorted(ix, key=lambda i: rank[key(P[i].part, Finv @ P[i].M)]), f'Gajo {n} de {len(ring)}')
    placed += groups['anillo']
    for label, gname in (('Claustro: pilares', 'claustro_pilares'), ('Claustro: plaza', 'claustro_plaza'),
                         ('Cúpula', 'claustro_cupula'), ('Entrada', 'entrada')):
        o = verify.grow_order(groups[gname], G, placed, P)
        for k in range(0, len(o), 8): add(o[k:k + 8], label)
        placed += o
    assert sorted(order) == list(range(len(P)))
    a = {'order': order, 'steps': steps}
    json.dump(a, open(os.path.join(ROOT, 'build', 'anim_order.json'), 'w'))
    pack.main(os.path.join(ROOT, 'dist', 'model.mpd'), os.path.join(ROOT, 'dist', 'model_packed.mpd'))
    t = open(os.path.join(ROOT, 'render', 'viewer_template.html')).read()
    t = t.replace('/*ANIM_DATA*/null', json.dumps(a, separators=(',', ':'))).replace("'model_packed.mpd'", "'/dist/model_packed.mpd'")
    os.makedirs(os.path.join(ROOT, 'build'), exist_ok=True)
    open(os.path.join(ROOT, 'build', 'viewer.html'), 'w').write(t)
    # standalone copy: the packed model inlined, opens with a double click (three.js from the CDN)
    m = open(os.path.join(ROOT, 'dist', 'model_packed.mpd')).read()
    t = t.replace("const text = await (await fetch(Q.get('model') || '/dist/model_packed.mpd')).text();",
                  "const text = document.getElementById('mpd').textContent;")
    i = t.index('<body>') + len('<body>')
    open(os.path.join(ROOT, 'dist', 'visor_3D.html'), 'w').write(t[:i] + '\n<script id="mpd" type="text/plain">' + m + '</script>\n' + t[i:])
    print('parts', len(P), 'steps', len(steps))

if __name__ == '__main__':
    main()
