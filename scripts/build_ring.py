"""Assemble the 28-gajo chain (north gajo aligned with the grid) into an MPD for preview renders."""
import sys, os
import numpy as np
import kit, gajo
from kit import ALPHA

N_CW, N_CCW = 15, 13            # gajos clockwise from north (incl. north) and counter-clockwise

def gajo_angles():
    return [j * ALPHA for j in range(N_CW)] + [-j * ALPHA for j in range(1, N_CCW + 1)]

def ring_mpd(out, parts=None):
    parts = parts or gajo.build()
    subs = {'gajo_tipo.ldr': parts}
    main = [('gajo_tipo.ldr', kit.frame(a), 16) for a in gajo_angles()]
    subs = {'ring.ldr': main, **subs}
    open(out, 'w').write(kit.mpd(subs, 'ring.ldr'))
    return out

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(kit.ldr.ROOT, 'work', 'ring.mpd')
    ring_mpd(out); print(out)
