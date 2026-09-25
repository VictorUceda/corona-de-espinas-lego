"""BrickLink purchase files from the bill of materials (data/bom_rebrickable.json, see bom.py):
dist/wanted_list.xml (BrickLink XML: Wanted List -> Upload) and dist/piezas.csv.

Optional price guide data/price_guide.json {"<blid>_<blcolor>": [sold_times, sold_avg, sold_qty_avg, stock_lots,
stock_qty, stock_qty_avg]} (new condition, 6-month sales, EUR; read from BrickLink's price guide pages): adds the unit
price, the estimated cost and the availability check (>= 3 sellers with enough stock) to the CSV.
"""
import csv, json, os
from xml.sax.saxutils import escape
from ldr import ROOT

MIN_SELLERS = 3

def main():
    b = json.load(open(os.path.join(ROOT, 'data', 'bom_rebrickable.json')))
    cm = b.pop('_colors')
    pgp = os.path.join(ROOT, 'data', 'price_guide.json')
    pg = json.load(open(pgp)) if os.path.exists(pgp) else {}
    rows, xml, total = [], ['<INVENTORY>'], 0.0
    for v in sorted(b.values(), key=lambda v: -v['qty']):
        bl = (v['bl_ids'] or [v['part']])[0]; col = cm[str(v['color'])]['bl_id']
        xml.append(f"<ITEM><ITEMTYPE>P</ITEMTYPE><ITEMID>{escape(bl)}</ITEMID><COLOR>{col}</COLOR>"
                   f"<MINQTY>{v['qty']}</MINQTY><CONDITION>N</CONDITION></ITEM>")
        r = {'ldraw': v['part'], 'bricklink': bl, 'color': cm[str(v['color'])]['name'], 'cantidad': v['qty'],
             'nombre': v['name'], 'sets_rebrickable': v['num_sets']}
        d = pg.get(f'{bl}_{col}')
        if d:
            unit = d[2] or d[5]; cost = (unit or 0) * v['qty']; total += cost
            r.update(precio_unit_eur=unit, coste_eur=round(cost, 2), lotes_en_venta=d[3],
                     cumple_3_vendedores='sí' if (d[3] or 0) >= MIN_SELLERS and (d[4] or 0) >= v['qty'] else 'NO')
        rows.append(r)
    xml.append('</INVENTORY>')
    os.makedirs(os.path.join(ROOT, 'dist'), exist_ok=True)
    open(os.path.join(ROOT, 'dist', 'wanted_list.xml'), 'w').write('\n'.join(xml) + '\n')
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(os.path.join(ROOT, 'dist', 'piezas.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=keys, delimiter=';'); w.writeheader(); w.writerows(rows)
    print('lots', len(rows), 'pieces', sum(r['cantidad'] for r in rows), 'estimated EUR' if pg else '', round(total, 2) if pg else '')

if __name__ == '__main__':
    main()
