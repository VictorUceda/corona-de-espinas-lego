"""Download Commons category files. Original if possible; else 1920px thumb (marked for later retry)."""
import json, re, os, sys, time, requests, urllib.parse
sys.path.insert(0, os.path.dirname(__file__)); import refindex
UA = {'User-Agent': 'CoronaLegoResearch/0.2 (personal study)'}
CAT = 'Category:Headquarters_of_the_Cultural_Heritage_Institute_of_Spain,_Madrid'
API = 'https://commons.wikimedia.org/w/api.php'
d = requests.get(API, headers=UA, params=dict(action='query', generator='categorymembers', gcmtitle=CAT,
    gcmlimit=500, gcmtype='file', prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=1920, format='json')).json()
json.dump(d, open('refs/commons/_api.json', 'w'), indent=1)
def clean(s): return re.sub('<[^>]+>', '', s or '').strip()
only_orig = '--orig' in sys.argv
for v in d['query']['pages'].values():
    ii = v['imageinfo'][0]; m = ii['extmetadata']
    name = v['title'][5:].replace(' ', '_'); path = f'refs/commons/{name}'
    have = os.path.exists(path) and os.path.getsize(path) == ii['size']
    res = 'original'
    if not have:
        r = requests.get(ii['url'], headers=UA, timeout=180)
        if r.ok: open(path, 'wb').write(r.content)
        elif only_orig: print('still', r.status_code, name, flush=True); continue
        else:
            time.sleep(2); r = requests.get(ii['thumburl'], headers=UA, timeout=180)
            if not r.ok: print('FAIL', name, r.status_code, flush=True); continue
            open(path, 'wb').write(r.content); res = 'thumb1920'
        time.sleep(2)
    refindex.add({'file': path, 'url': ii['url'], 'page': ii['descriptionurl'],
        'licencia': m.get('LicenseShortName', {}).get('value'), 'autor': clean(m.get('Artist', {}).get('value')),
        'fecha': clean(m.get('DateTimeOriginal', {}).get('value')),
        'descripcion': clean(m.get('ImageDescription', {}).get('value'))[:300],
        'size_px': [ii['width'], ii['height']], 'resolucion': res, 'tipo': 'foto', 'vista': None})
    print(res, name, flush=True)
