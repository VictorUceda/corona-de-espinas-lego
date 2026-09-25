"""Quick preview: ring of gajos + base + claustro -> build/ring.mpd and build/ring_gajo.mpd."""
import os, sys
import numpy as np
import kit, build_ring, core
import gajo, claustro, base

def write(out):
    subs = {'gajo_tipo.ldr': gajo.build(), 'base.ldr': base.base(), 'claustro.ldr': claustro.build()}
    ring = [('gajo_tipo.ldr', kit.frame(a), 16) for a in build_ring.gajo_angles()]
    subs = {'main.ldr': ring + [('base.ldr', np.eye(4), 16), ('claustro.ldr', np.eye(4), 16)], **subs}
    open(out, 'w').write(kit.mpd(subs, 'main.ldr'))
    only = {'g.ldr': subs['gajo_tipo.ldr']}
    open(out.replace('.mpd', '_gajo.mpd'), 'w').write(kit.mpd(only, 'g.ldr'))

if __name__ == '__main__':
    write(os.path.join(kit.ldr.ROOT, 'build', 'ring.mpd'))
