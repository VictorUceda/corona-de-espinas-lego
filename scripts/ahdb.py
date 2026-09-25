"""Fetch pages from ahdb.upm.es (AtoM archive) passing its simple JS-cookie challenge.
Usage: ahdb.py URL OUTFILE
"""
import sys, re, base64, time, urllib.parse, requests
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
_s = None

def session():
    global _s
    if _s: return _s
    s = requests.Session(); s.headers['User-Agent'] = UA
    r = s.get('https://ahdb.upm.es/challenge', timeout=60)
    val = re.search(r'data-cookie-value="([0-9a-f]+)"', r.text).group(1)
    time.sleep(5)
    s.cookies.set('atom_js', val, domain='ahdb.upm.es', path='/')
    s.cookies.set('atom_headless', urllib.parse.quote(base64.b64encode((val + ':false').encode()).decode()), domain='ahdb.upm.es', path='/')
    _s = s
    return s

def get(url):
    s = session()
    r = s.get(url, timeout=120)
    if 'Verificando su navegador' in r.text[:3000] or '/challenge' in r.text[:1500]:
        global _s; _s = None
        s = session(); r = s.get(url, timeout=120)
    return r

if __name__ == '__main__':
    r = get(sys.argv[1])
    open(sys.argv[2], 'wb').write(r.content)
    print(r.status_code, len(r.content), r.headers.get('content-type'))
