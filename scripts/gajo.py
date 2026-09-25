"""Gajo tipo: one 12.02 deg sector of the ring, built on the chain geometry of gajo_base.py (joints, grids,
exclusion zones, gravity assembly) and detailed from the photographs of the building.

Facade rows: 19.5 PB, 20.5 windows, 21.5 balcony tips.
  * PB: white grille-brick lattice (2877) under a column and one tornapunta (inverted 45 slope) per gajo;
  * balcony trays with a curved soffit: 24201 inverted curved slopes hung from the plates above, tile on the tip;
  * white roller shutters: the plate seams read as the slats; one open (black) window per floor;
  * rib fins: a 1x1 stack on the left tip cell of every tray;
  * P3 leans inwards: white 45 slopes with one LBG slope on the left rib (the diagonal strut / 'jabalcon');
  * white gutter band (11477 curved slopes, high end outwards), skylights next to the gutter, white crown rims,
    spikes = white cone 4589 + finned spike 24482;
  * hidden: the spine is drawn as the real structure (radial portico: two brick columns + ring corridor gap).
P3 is 6 plates (vertical exaggeration): cornice z24, roof z25-31, ridge z31-33.
"""
import os, sys
from kit import P, box, J1, J2
import gajo_base as gb

LBG, DBG, WHITE, BLACK, TCLR = 71, 72, 15, 0, 47
CONC, ROOF, HID, GLASS = LBG, DBG, DBG, BLACK
ZH = 8

def plate(c, *a): return box('plate', c, *a)
def brick(c, *a): return box('brick', c, *a)
def tile(c, *a): return box('tile', c, *a)

def pb():
    """PB z2-8: white grille lattice (2877 + 1x1) on row 19.5 under the column + tornapunta (z5-8)."""
    return [
        P('2877', WHITE, -1, 19.5, 2, tag='pb_lat'),                    # x -2..0
        P('3005', WHITE, 0.5, 19.5, 2, tag='pb_lat_r'),
        P('3665a', CONC, -0.5, 19.5, 5, rot=-90, tag='strut_l'),      # tornapunta: inverted slope branching
        P('3005', CONC, 0.5, 19.5, 5, tag='trunk'),                    # to the left rib; column at x=0.5
        # (a right-hand branch would reach cell (1.5, 19.5) below z8 and hit the previous gajo's hinge
        #  base while this gajo is lowered into place)
    ]

def tray(z0, t, hinge=False):
    """Balcony tray z0..z0+3 + tie into the spine. 24201 x4 (high end = tip row 21.5, low end row 20.5)."""
    g = [P('24201', CONC, x, 21.5, z0, tag=t(f'soffit{x}')) for x in (-1.5, -0.5, 0.5, 1.5)]
    g.append(plate(HID, -1, 1, 18, 19, z0, t('band1b')) if hinge else plate(HID, -1, 2, 18, 20, z0, t('band1b')))
    g.append(plate(CONC, -1, 2, 19, 21, z0 + 1, t('tie')))            # on band1b + the soffits' low studs
    g.append(plate(CONC, -2, -1, 20, 21, z0 + 1, t('tie_l')))
    g.append(tile(CONC, -1, 2, 21, 22, z0 + 2, t('tip')))             # on the high studs
    g.append(plate(WHITE, -1, 2, 19, 21, z0 + 2, t('shut0')))          # bonds facade row to the back row
    g.append(plate(WHITE, -2, -1, 20, 21, z0 + 2, t('shut0l')))
    # rib fin ('aleta vertical en cada nervio'): 1x1 stack on the left tip cell, up to the next tray
    g += [plate(CONC, -2, -1, 21, 22, z0 + 2, t('fin0')), plate(CONC, -2, -1, 21, 22, z0 + 3, t('fin1')),
          tile(CONC, -2, -1, 21, 22, z0 + 4, t('fin2'))]
    return g

def shutters(z0, t, open_x):
    """z0+3, z0+4: shutter plate + tile (the next tray rests on the tile). open_x = module (x0,x1) with glass."""
    g = []
    for (a, b) in ((-2, 0), (0, 2)):                                   # open window = glass, 2 plates
        c = GLASS if (a, b) == open_x else WHITE
        g.append(plate(c, a, b, 20, 21, z0 + 3, t(f'shut1_{a}')))
        g.append(tile(c, a, b, 20, 21, z0 + 4, t(f'shut2_{a}')))
    g.append(plate(HID, -1, 2, 19, 20, z0 + 3, t('back3')))
    g.append(plate(HID, -1, 2, 19, 20, z0 + 4, t('back4')))
    return g

def spine_floor(z0, y0=11, y0_at=None, top=None):
    """Hidden radial 'portico' (cols +-0.5, rows 11.5..18.5): plate, plate, then two brick columns with the
    ring corridor between them (rows 15..16 open in the brick course), for one floor from z0."""
    g = []
    for dz, kind in ((0, 'plate'), (1, 'plate')):
        z = z0 + dz
        ys = (y0_at or {}).get(z, y0)
        for i, (a, b) in enumerate(gb._split(kind, ys, 18 if dz == 0 else 19, z % 2)):
            g.append(box(kind, HID, -1, 1, a, b, z, f'sp{z}{"ab"[i]}'))
    z = z0 + 2
    ys = (y0_at or {}).get(z, y0)
    g.append(box('brick', HID, -1, 1, ys, 15, z, f'sp{z}in'))           # inner column (library side)
    g.append(box('brick', HID, -1, 1, 16, 19, z, f'sp{z}out'))          # outer column (offices)
    return g

def cloister_face():
    return [
        plate(GLASS, -1, 1, 11, 12, 18, 'cf18'),
        plate(CONC, -1, 1, 11, 13, 19, 'cf19'),
        brick(CONC, -1, 1, 11, 12, 20, 'cf20'),
    ]

def p3(z0=18):
    """P3 leans INWARDS (r41/h14.5 -> r38.3/h18.6): tray, then white 45 slopes (x -0.5..1.5) and, on the left
    rib, one LBG slope = the diagonal strut ('jabalcon') that climbs from the tray tip to the gutter."""
    t = lambda s: f'P3_{s}'
    g = [P('24201', CONC, x, 21.5, z0, tag=t(f'soffit{x}')) for x in (-1.5, -0.5, 0.5, 1.5)]
    g.append(plate(HID, -1, 2, 18, 20, z0, t('band1b')))
    g.append(plate(CONC, -1, 2, 19, 21, z0 + 1, t('tie')))            # on band1b + the soffits' low studs
    g.append(plate(CONC, -2, -1, 20, 21, z0 + 1, t('tie_l')))
    g.append(tile(CONC, -2, 2, 21, 22, z0 + 2, t('tip')))
    g.append(plate(WHITE, -1, 2, 19, 21, z0 + 2, t('shut0')))
    g.append(plate(WHITE, -2, -1, 20, 21, z0 + 2, t('shut0l')))
    for x in (-1.5, -0.5, 0.5, 1.5):
        g.append(P('3040b', CONC if x == -1.5 else WHITE, x, 20.5, z0 + 3, tag=t(f'lean{x}')))
    for dz in (3, 4, 5):
        g.append(plate(HID, -1, 2, 19, 20, z0 + dz, t(f'back{dz}')))
    # spine: z18, z19 plates, z20 brick (corridor gap), z23 plate
    g += spine_floor(z0, y0=12, y0_at={19: 13})
    g.append(plate(HID, -1, 1, 11, 15, z0 + 5, 'sp23a'))
    g.append(plate(HID, -1, 1, 15, 19, z0 + 5, 'sp23b'))
    return g

def cornice(z=24):
    """Gutter z24 on the lean studs (row 20.5) + white rounded gutter band (11477, lip over the lean), roof base."""
    g = [
        plate(CONC, -2, 2, 20, 21, z, 'corn_b'),                        # lean studs row 20.5
        plate(HID, -1, 2, 18, 20, z, 'roofbase_o'),
        plate(HID, -1, 1, 14, 18, z, 'roofbase_m'),
        plate(HID, -1, 1, 11, 14, z, 'roofbase_i'),
    ]
    g += [P('11477', WHITE, x, 21, z + 1, rot=180, tag=f'gutter{x}') for x in (-1.5, -0.5, 0.5, 1.5)]
    g.append(tile(CONC, -1, 1, 11, 12, z + 1, 'inner_walk'))
    return g

def crown(dz=1):
    """Crown of gajo_base lifted 1 plate; spikes = white cone 4589 + finned spike 24482 (flared pyramid, ~6.4 m)."""
    g = []
    col = {'roofo1_-0.5': WHITE, 'roofo1_0.5': WHITE, 'roofo2_-0.5': ROOF, 'roofo2_0.5': ROOF, 'roofi1_-0.5': WHITE}
    for p in gb.crown():
        if p.tag.startswith(('spk_base', 'spk')) and p.part in ('85861.dat', '24482.dat'): continue
        if p.tag in ('ridge_t1', 'ridge_t2', 'ridge_t3'): continue          # -> white rims below
        if p.tag in col: p.color = col[p.tag]
        p.M = p.M.copy(); p.M[1, 3] -= 8 * dz
        g.append(p)
    # white 'vertiente' of the crown wall: cheese slopes falling outwards / inwards round the spike bases
    for x in (-0.5, 0.5, 1.5):
        g.append(P('54200', WHITE, x, 16.5, 31 + dz, tag=f'rim_o{x}'))
    for x in (-0.5, 0.5):
        g.append(P('54200', WHITE, x, 14.5, 31 + dz, rot=180, tag=f'rim_i{x}'))
    for x in (0, 1.5):
        g.append(P('4589', WHITE, x, 15.5, 32 + dz, tag=f'spk_cone{x}'))
        g.append(P('24482', WHITE, x, 15.5, 32 + dz + 3, tag=f'spk{x}', zoff=4))
    return g

def build():
    g = gb.joints() + gb.inner_blocks() + gb.spine_low() + pb()
    t1 = lambda s: f'P1_{s}'; t2 = lambda s: f'P2_{s}'
    g += tray(8, t1, hinge=True) + shutters(8, t1, (-2, 0)) + spine_floor(8)
    g += tray(13, t2) + shutters(13, t2, (0, 2)) + spine_floor(13)
    g += p3() + cloister_face() + cornice() + crown()
    return g

if __name__ == '__main__':
    from kit import check_ring
    check_ring(build())
