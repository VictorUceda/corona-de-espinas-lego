"""Fetch a web page / PDF into refs/, save clean text, and register in index.json.
Usage: fetchref.py page URL NAME "descripcion" [licencia]
       fetchref.py file URL RELPATH tipo vista "descripcion" [licencia]
"""
import sys, os, subprocess, re
sys.path.insert(0, os.path.dirname(__file__))
import refindex
ROOT = os.path.join(os.path.dirname(__file__), '..')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

def curl(url, out):
    subprocess.run(['curl', '-sSL', '--max-time', '120', '-A', UA, '-o', out, url], check=True)

def html2txt(html):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, 'html.parser')
    for t in s(['script', 'style', 'noscript', 'nav', 'footer', 'header', 'form', 'svg']):
        t.decompose()
    txt = ''
    for main in (s.find('article'), s.find('main'), s.body, s):
        if main is not None:
            txt = main.get_text('\n')
            if len(txt.strip()) > 800: break
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n\n', txt)
    return txt.strip()

def page(url, name, desc, lic='desconocida/© autor'):
    h = os.path.join(ROOT, 'refs/texts', name + '.html')
    curl(url, h)
    raw = open(h, 'rb').read().decode('utf-8', 'replace')
    t = os.path.join(ROOT, 'refs/texts', name + '.txt')
    open(t, 'w').write('URL: ' + url + '\n\n' + html2txt(raw))
    for ext, tipo in (('.html', 'texto'), ('.txt', 'texto')):
        refindex.add(dict(file='refs/texts/' + name + ext, url=url, licencia=lic, vista=None, tipo=tipo,
                          descripcion=desc + (' (HTML original)' if ext == '.html' else ' (texto extraído)')))
    print(t, os.path.getsize(t))

def file(url, rel, tipo, vista, desc, lic='desconocida/© autor'):
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p):
        curl(url, p)
    refindex.add(dict(file=rel, url=url, licencia=lic, vista=(None if vista in ('', 'null') else vista), tipo=tipo, descripcion=desc))
    print(p, os.path.getsize(p))

if __name__ == '__main__':
    a = sys.argv[1:]
    {'page': page, 'file': file}[a[0]](*a[1:])
