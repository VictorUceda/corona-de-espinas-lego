"""dist/model.mpd -> dist/model_packed.mpd with every referenced part/primitive embedded as '0 FILE' blocks
(equivalent to three.js utils/packLDrawModel.mjs): the result loads without the LDraw library.
Embedded names are normalised like LDrawLoader does (backslash -> slash, lower-case).
"""
import os, sys
import ldr
from ldr import ROOT

def norm(n):
    k = n.strip().replace('\\', '/').lower()
    if k.startswith('s/'): k = 'parts/' + k          # LDrawLoader's standardised subfolders
    elif k.startswith('48/'): k = 'p/' + k
    return k

def main(src=os.path.join(ROOT, 'model.mpd'), dst=os.path.join(ROOT, 'model_packed.mpd')):
    text = open(src).read()
    subs = {norm(l[7:]) for l in text.splitlines() if l.startswith('0 FILE ')}
    todo = []
    for l in text.splitlines():
        t = l.split()
        if len(t) >= 15 and t[0] == '1':
            n = ' '.join(t[14:])
            if norm(n) not in subs: todo.append((n, None))
    seen, blocks = set(), []
    while todo:
        name, hint = todo.pop()
        key = norm(name)
        if key in seen: continue
        seen.add(key)
        kind, path = ldr.find(name, hint)
        if not path: print('MISSING', name); continue
        lines = ldr.read_lines(path)
        blocks.append(f'0 FILE {key}\n' + '\n'.join(lines) + '\n0 NOFILE\n')
        for l in lines:
            t = l.split()
            if len(t) >= 15 and t[0] == '1':
                todo.append((' '.join(t[14:]), 'p' if kind == 'p' else None))
    out = text.rstrip('\n') + '\n' + ''.join(blocks)
    open(dst, 'w').write(out)
    print(dst, len(seen), 'embedded files', round(len(out) / 1e6, 2), 'MB')

if __name__ == '__main__':
    main()
