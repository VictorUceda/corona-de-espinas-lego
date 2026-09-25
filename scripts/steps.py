"""Build steps (1-8 parts) from the verified build order of dist/model.mpd -> build/instructions/steps.json
+ sec_*.ldr. Each step also records the tags of its parts so the book notes (notas.py) can attach to it.
"""
import json, os, sys
import connect, verify, steps_core as s1
from ldr import ROOT
import gajo, notas

OUT = os.path.join(ROOT, 'build', 'instructions'); os.makedirs(OUT, exist_ok=True)
s1.OUT = OUT

_TAGS = None
def retag(parts):
    """Parts read back from the .mpd have no tags: recover them from the Python submodels (same world matrix)."""
    global _TAGS
    import build_model, numpy as np
    key = lambda p: (p.part, p.color, tuple(np.round(p.M[:3, :], 2).ravel()))
    if _TAGS is None:
        _TAGS = {}
        for name, items in build_model.submodels().items():
            for p in items:
                if hasattr(p, 'tag'): _TAGS.setdefault(key(p), p.tag)
    for p in parts:
        if not p.tag: p.tag = _TAGS.get(key(p), '')
    return parts

def section(key, title, parts, order, callout=None, context=None):
    retag(parts)
    sec = s1.section(key, title, parts, order, callout, context)
    st = s1.chunk(parts, order)
    for d, ix in zip(sec['steps'], st): d['tags'] = [parts[i].tag for i in ix]
    return sec

def attach_notes(book):
    for sec in book['sections']:
        sec['notes'] = []
        for n in notas.NOTES:
            if n['sec'] != sec['key']: continue
            if n['trigger'] is None: sec['notes'].append(n); continue
            for k, st in enumerate(sec['steps']):
                if any(t.startswith(n['trigger']) for t in st.get('tags', [])):
                    st.setdefault('notes', []).append(n); break
            else: sec['notes'].append(n)

def main():
    items = verify.flatten(os.path.join(ROOT, 'dist', 'model.mpd'))
    P = [p for p, _ in items]
    G = connect.graph(P)
    units, ring = verify.build_order(items, verify.SPEC)
    groups = {n: ix for n, ix, _ in units if n != 'base'}
    groups['base'] = [ix[0] for n, ix, _ in units if n == 'base']
    book = {'title': 'Corona de Espinas — IPCE, Madrid', 'scale': '1:250', 'n_parts': len(P), 'sections': []}
    ix = groups['base']; order = verify.grow_order(ix, G, [], P)
    bp = [P[i] for i in order]
    book['sections'].append(section('base', 'Base, podio y parque', bp, list(range(len(bp)))))
    g = gajo.build(); Gg = connect.graph(g)
    gorder = verify.grow_order(range(len(g)), Gg, [], g, resting=True)
    book['sections'].append(section('gajo', 'Gajo tipo', g, gorder, callout={'mult': len(ring), 'label': f'×{len(ring)}'}))
    anillo_parts, anillo_steps = [], []
    for k, (name, ix) in enumerate(ring):
        s = list(range(len(anillo_parts), len(anillo_parts) + len(ix)))
        anillo_parts += [P[i] for i in ix]
        if k == 0 or len(anillo_steps[-1]) >= 2 * len(ring[1][1]): anillo_steps.append(s)
        else: anillo_steps[-1] += s
    s1.write_ldr('sec_anillo.ldr', anillo_parts, anillo_steps)
    ng = len(ring[1][1])
    book['sections'].append({'key': 'anillo', 'title': 'Anillo: unir los 28 gajos (sentido antihorario)', 'ldr': 'sec_anillo.ldr',
                             'context_steps': 0, 'unit': 'gajo',
                             'steps': [{'n_parts': max(1, round(len(s) / ng)), 'parts': [{'part': 'gajo_tipo', 'qty': max(1, round(len(s) / ng))}]} for s in anillo_steps]})
    base_ctx = [P[i] for i in groups['base']]
    ring_all = [P[i] for i in groups['anillo']]
    s1.write_ldr('sec_anillo_base.ldr', base_ctx + ring_all, [list(range(len(base_ctx))), list(range(len(base_ctx), len(base_ctx) + len(ring_all)))])
    book['sections'].append({'key': 'anillo_base', 'title': 'Colocar el anillo sobre la base', 'ldr': 'sec_anillo_base.ldr',
                             'context_steps': 1, 'steps': [{'n_parts': 1, 'parts': [{'part': 'anillo', 'qty': 1}]}]})
    placed = groups['base'] + groups['anillo']
    ctx = [P[i] for i in groups['base']]
    ix = groups['claustro_pilares']; order = verify.grow_order(ix, G, placed, P)
    cp = [P[i] for i in order]
    book['sections'].append(section('pilares', 'Claustro: vestíbulo, pilares y biblioteca', cp, list(range(len(cp))), context=ctx))
    ix = groups['claustro_plaza']; sub = [P[i] for i in ix]; Gs = connect.graph(sub)
    book['sections'].append(section('plaza', 'Claustro: el vientre de la ballena y la plaza', sub,
                                    verify.grow_order(range(len(sub)), Gs, [], sub), callout={'mult': 1, 'label': 'submontaje'}))
    ctx2 = ctx + cp
    s1.write_ldr('sec_plaza_place.ldr', ctx2 + sub, [list(range(len(ctx2))), list(range(len(ctx2), len(ctx2) + len(sub)))])
    book['sections'].append({'key': 'plaza_place', 'title': 'Colocar la plaza sobre los pilares', 'ldr': 'sec_plaza_place.ldr',
                             'context_steps': 1, 'steps': [{'n_parts': 1, 'parts': [{'part': 'plaza', 'qty': 1}]}]})
    placed = groups['base'] + groups['anillo'] + groups['claustro_pilares'] + groups['claustro_plaza']
    ix = groups['claustro_cupula']; order = verify.grow_order(ix, G, placed, P)
    cu = [P[i] for i in order]
    ctx3 = [P[i] for i in groups['base'] + groups['claustro_pilares'] + groups['claustro_plaza']]
    book['sections'].append(section('cupula', 'La cúpula estrella', cu, list(range(len(cu))), context=ctx3))
    placed += ix
    ix = groups['entrada']; order = verify.grow_order(ix, G, placed, P)
    ep = [P[i] for i in order]
    ctx4 = [P[i] for i in placed]
    book['sections'].append(section('entrada', 'Entrada: testeros, pasarelas y escalinata', ep, list(range(len(ep))), context=ctx4))
    from collections import Counter
    import ldr
    bom = Counter((p.part, p.color) for p in P)
    book['bom'] = [{'part': p, 'color': c, 'qty': q, 'title': ldr.part_title(p)} for (p, c), q in sorted(bom.items(), key=lambda x: (-x[1], x[0]))]
    book['intro'] = notas.INTRO
    attach_notes(book)
    json.dump(book, open(os.path.join(OUT, 'steps.json'), 'w'), indent=1, ensure_ascii=False)
    for s in book['sections']: print(s['key'], len(s['steps']), 'steps', sum(len(st.get('notes', [])) for st in s['steps']) + len(s['notes']), 'notes')
    print('total steps', sum(len(s['steps']) for s in book['sections']))

if __name__ == '__main__':
    main()
