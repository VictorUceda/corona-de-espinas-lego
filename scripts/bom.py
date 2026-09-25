"""Bill of materials of dist/model.mpd + Rebrickable check that each part/colour exists (num_sets > 0)
-> data/bom_rebrickable.json (cached; only new lots are queried). Needs REBRICKABLE_KEY for new lots.
"""
import json, os, sys
from collections import Counter
import verify, ldr, rebrickable as rb

def bom(path=os.path.join(ldr.ROOT, 'dist', 'model.mpd')):
    items = verify.flatten(path)
    return Counter((p.part.replace('.dat', ''), p.color) for p, _ in items)

if __name__ == '__main__':
    b = bom()
    out_p = os.path.join(ldr.ROOT, 'data', 'bom_rebrickable.json')
    old = json.load(open(out_p)) if os.path.exists(out_p) else {}
    m = {'parts': {}}
    cmap = old.get('_colors') or rb.colors()
    res = {'_colors': cmap}
    for (p, c), n in sorted(b.items()):
        k = f'{p}_{c}'
        if k in old and 'num_sets' in old[k]: res[k] = {**old[k], 'qty': n}; continue
        info = m['parts'].get(p) or rb.part(p)
        rbid = info['rb_id'] if info else p
        try:
            d = rb.get(f"{rb.API}/parts/{rbid}/colors/{cmap[str(c)]['rb_id']}/")
            ns = d.get('num_sets', 0)
        except Exception as e:
            ns = f'ERR {e}'[:60]
        res[k] = {'part': p, 'color': c, 'qty': n, 'rb_id': rbid, 'bl_ids': info and info.get('bl_ids'),
                  'name': info and info.get('name'), 'num_sets': ns}
        print(k, n, ns, flush=True)
    json.dump(res, open(out_p, 'w'), indent=1)
    lots = [v for k, v in res.items() if k != '_colors']
    print('lots', len(lots), 'pieces', sum(v['qty'] for v in lots))
    print('MISSING:', [(v['part'], v['color'], v['num_sets']) for v in lots if not isinstance(v['num_sets'], int) or v['num_sets'] == 0])
