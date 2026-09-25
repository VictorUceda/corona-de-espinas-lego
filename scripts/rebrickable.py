"""Rebrickable API v3 helpers (LDraw -> BrickLink part and colour ids). Needs REBRICKABLE_KEY in the environment."""
import json, os, time
import requests
from ldr import ROOT

KEY = os.environ.get('REBRICKABLE_KEY', '')          # https://rebrickable.com/api/
H = {'Authorization': f'key {KEY}', 'User-Agent': 'corona-lego/0.1'}
API = 'https://rebrickable.com/api/v3/lego'

def get(url, params=None):
    for a in range(6):
        r = requests.get(url, headers=H, params=params, timeout=60)
        if r.status_code == 429: time.sleep(2 + 2 * a); continue
        r.raise_for_status(); time.sleep(1.1)       # stay under the 1 req/s limit
        return r.json()
    raise RuntimeError(url)

def colors():
    out, url = {}, f'{API}/colors/?page_size=1000'
    while url:
        d = get(url)
        for c in d['results']:
            ext = c.get('external_ids', {})
            ld = ext.get('LDraw', {}).get('ext_ids', [])
            bl = ext.get('BrickLink', {})
            for l in ld:
                out[str(l)] = {'rb_id': c['id'], 'name': c['name'], 'bl_id': (bl.get('ext_ids') or [None])[0],
                               'bl_name': ((bl.get('ext_descrs') or [[None]])[0] or [None])[0], 'rgb': c['rgb']}
        url = d.get('next')
    return out

def part(ldraw_id):
    d = get(f'{API}/parts/', {'ldraw_id': ldraw_id, 'inc_part_details': 1})
    res = d['results']
    if not res:   # fall back: Rebrickable part number = LDraw number without variant letter
        d = get(f'{API}/parts/{ldraw_id}/'); res = [d] if d.get('part_num') else []
    if not res: return None
    p = res[0]; ext = p.get('external_ids', {})
    return {'rb_id': p['part_num'], 'name': p['name'], 'bl_ids': ext.get('BrickLink', []), 'ldraw_ids': ext.get('LDraw', [])}
