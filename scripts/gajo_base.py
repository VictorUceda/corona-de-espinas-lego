"""Chain geometry of the gajo (12.02 deg sector) at 1 stud = 2.0 m (1:250), 1 plate = 0.8 m, and the hidden
structure shared by every gajo: joints, inner blocks, low spine, crown. gajo.py builds the detailed gajo on top.

Plan grid (studs): columns x in {-1.5,-0.5,0.5,1.5}; y radial (outwards); x positive = clockwise.
  Gi = inner joint blocks, rows centred on integers (9..12)  -> J1 = (+-1, 9.5) are grid corners
  Go = main body, rows centred on half-integers (11.5..21.5) -> J2 = (+-2, 19) are grid corners
  Gi <-> Go bonded with 1x2 jumpers turned radially (half-stud offset).

Assembly: gajos are added COUNTER-CLOCKWISE; the new gajo's RIGHT side drops onto the LEFT side of the gajo
already placed. So at every rib: left-side joint parts are LOW (placed first), right-side ones HIGH.
  J1 (inner): left = round 2x2 centre-stud jumper 18674 (z3) on a 1x4 support (z2);
              right = round plate 4032b (z4, centre antistud) clamped by a 1x4 (z5).
  J2 (outer): swivel hinge at z8: left = base 2429, right = top 2430 (pin drops into the base).
Exclusion zones (so the vertical drop is free): nothing of this gajo above z3 inside the left J1 circle, nothing
below z4 inside the right J1 circle; nothing above z8 at cell (-1.5,19.5), nothing below z8 at (1.5,18.5..19.5).
Wedge: rows >= 19.5 are 4 studs wide inside the sector; below that only columns +-0.5 are inside.
Column +1.5 (rows 15.5..18.5) crosses the right rib: used only above z8 on the RIGHT side (it lies over the
neighbour's empty left zone); column -1.5 is used only from row 19.5 outwards.
Radii (y): cloister face 11 | spine 11..19 | PB wall row 19.5 | windows row 20.5 | balcony tips row 21.5.
Heights (plates above base top): podium top 2 | PB 2-8 | P1 8-13 | P2 13-18 | P3 18-23 | cornice 23-24 |
roof 24-30 | crown 30-32 (gajo.py lifts the roof and crown 1 plate: P3 has 6 plates).
"""
from kit import P, box, J1, J2

LBG, DBG, WHITE, TBLK, TCLR, BLACK = 71, 72, 15, 40, 47, 0
CONC, ROOF, HID, GLASS = LBG, DBG, DBG, BLACK   # window glass: black plates (1x4 trans-black does not exist)
ZH = 8                       # J2 hinge level

def plate(c, *a): return box('plate', c, *a)
def brick(c, *a): return box('brick', c, *a)
def tile(c, *a): return box('tile', c, *a)

def joints():
    return [
        P('3710', HID, -0.5, 10.5, 2, rot=90, tag='J1L_support'),      # Gi rows 9..12, x -1..0
        P('18674', HID, -J1[0], J1[1], 3, tag='J1L_jumper'),
        P('4032b', HID, J1[0], J1[1], 4, tag='J1R_round'),
        P('3710', HID, 0.5, 10.5, 5, rot=90, tag='J1R_clamp'),         # Gi rows 9..12, x 0..1
        P('2429', CONC, -J2[0], J2[1], ZH, rot=180, tag='J2L_base', zoff=8),
        P('2430', CONC, J2[0], J2[1], ZH, rot=180, tag='J2R_top', zoff=8),
    ]

def inner_blocks():
    return [
        P('3794b', HID, -0.5, 11.5, 3, rot=90, tag='GiGoL'),          # support Gi 11,12 -> Go (-0.5, 11.5)
        plate(HID, 0, 1, 10.5, 12.5, 2, 'GiR2'), plate(HID, 0, 1, 10.5, 12.5, 3, 'GiR3'),
        plate(HID, 0, 1, 10.5, 12.5, 4, 'GiR4'),                       # under the right clamp
        P('3794b', HID, 0.5, 11.5, 6, rot=90, tag='GiGoR'),           # clamp Gi 11,12 -> Go (0.5, 11.5)
    ]

def spine_low():
    """Hidden radial wall z2-8 (cols +-0.5). Go row 11.5 used on the left from z4 (on GiGoL), right from z7."""
    return [
        plate(HID, -1, 1, 13, 17, 2, 'sl2a'), plate(HID, -1, 1, 17, 18, 2, 'sl2b'),
        plate(HID, -1, 1, 14, 18, 3, 'sl3a'), plate(HID, -1, 1, 18, 19, 3, 'sl3b'),
        plate(HID, -1, 0, 11, 17, 4, 'sl4L'), plate(HID, 0, 1, 13, 17, 4, 'sl4R'), plate(HID, -1, 1, 17, 19, 4, 'sl4b'),
        plate(HID, -1, 1, 13, 17, 5, 'sl5a'), plate(HID, -1, 0, 11, 13, 5, 'sl5L'), plate(HID, -1, 1, 17, 19, 5, 'sl5b'),
        plate(HID, -1, 0, 11, 15, 6, 'sl6L'), plate(HID, 0, 1, 13, 17, 6, 'sl6R'), plate(HID, -1, 1, 17, 19, 6, 'sl6b'),
        plate(HID, -1, 1, 11, 15, 7, 'sl7a'), plate(HID, -1, 1, 15, 19, 7, 'sl7b'),
    ]

def pb():
    """PB z2-8: recessed white lattice wall (row 19.5, x -2..1; the right rib cell stays free below the hinge)
    + Y-struts (inverted 45 slopes, base row 19.5, overhang row 20.5) under the P1 band."""
    return [
        plate(WHITE, -1, 1, 18, 20, 2, 'pb_base'),                     # ties the lattice to the spine (under sl3b)
        plate(WHITE, -2, -1, 19, 20, 2, 'pb_base_l'),
        plate(WHITE, -2, 1, 19, 20, 3, 'pb_lat_a'),                    # white lattice screen, 2 plates
        plate(WHITE, -2, 1, 19, 20, 4, 'pb_lat_b'),
        P('3665a', CONC, -1.5, 19.5, 5, tag='strut_a'),
        P('3665a', CONC, -0.5, 19.5, 5, tag='strut_b'),
        P('3665a', CONC, 0.5, 19.5, 5, tag='strut_c'),
    ]

def _split(kind, y0, y1, parity):
    from kit import SIZES
    ok = lambda n: n == 0 or (min(2, n), max(2, n)) in SIZES[kind]
    cuts = [c for c in range(y0 + 1, y1) if ok(c - y0) and ok(y1 - c)]
    if not cuts: return [(y0, y1)]
    c = cuts[len(cuts) // 2 - (1 if parity and len(cuts) > 1 else 0)] if len(cuts) > 1 else cuts[0]
    return [(y0, c), (c, y1)]

def spine_floor(z0, y0=11, y0_at=None):
    """Hidden radial wall (cols +-0.5, rows 11.5..18.5) for one 5-plate floor from z0:
    z0 plates to y=18 (band bond plate covers 18.5 there), z0+1 plates to 19, z0+2..z0+4 one brick course."""
    g = []
    for dz, kind, top in ((0, 'plate', 18), (1, 'plate', 19), (2, 'brick', 19)):
        z = z0 + dz
        ys = (y0_at or {}).get(z, y0)
        for i, (a, b) in enumerate(_split(kind, ys, top, z % 2)):
            g.append(box(kind, HID, -1, 1, a, b, z, f'sp{z}{"ab"[i]}'))
    return g

def floor(z0, tag, hinge=False, inclined=False):
    """Balcony band (2 plates) + windows (3 plates) or the inclined P3 face; facade rows 20.5 (windows),
    21.5 (balcony tip). Cell (-1.5, 19.5) stays empty above the hinge."""
    g = []
    t = lambda s: f'{tag}_{s}'
    g.append(plate(CONC, -2, 2, 20, 22, z0, t('band1')))
    if hinge:
        g.append(plate(HID, -1, 1, 18, 19, z0, t('band1b')))
    else:
        g.append(plate(HID, -1, 2, 18, 20, z0, t('band1b')))
    g.append(plate(CONC, -1, 1, 19, 21, z0 + 1, t('band2c')))
    g.append(plate(CONC, 1, 2, 19, 21, z0 + 1, t('band2r')))
    g.append(plate(CONC, -2, -1, 20, 21, z0 + 1, t('band2l')))
    g.append(tile(CONC, -2, 2, 21, 22, z0 + 1, t('band2tile')))
    if not inclined:
        g.append(plate(GLASS, -2, 2, 20, 21, z0 + 2, t('glass')))
        g.append(plate(CONC, -2, 2, 20, 21, z0 + 3, t('shut1')))
        g.append(plate(CONC, -2, 2, 20, 21, z0 + 4, t('shut2')))
    else:
        for x in (-1.5, -0.5, 0.5, 1.5):
            g.append(P('3040b', CONC, x, 20.5, z0 + 2, rot=0, tag=t(f'incl{x}')))
    g.append(brick(HID, -1, 2, 19, 20, z0 + 2, t('back')))
    return g

def cloister_face():
    """Row 11.5 above the plaza (z18-23): glass strip, bond plate into the spine, concrete brick."""
    return [
        plate(GLASS, -1, 1, 11, 12, 18, 'cf18'),
        plate(CONC, -1, 1, 11, 13, 19, 'cf19'),
        brick(CONC, -1, 1, 11, 12, 20, 'cf20'),
    ]

def cornice():
    return [
        tile(CONC, -2, 2, 20, 21, 23, 'corn_tile'),                    # on the P3 slope studs (row 20.5)
        plate(HID, -1, 2, 18, 20, 23, 'roofbase_o'),                   # rows 18.5..19.5 incl. right cell
        plate(HID, -1, 1, 14, 18, 23, 'roofbase_m'),
        plate(HID, -1, 1, 11, 14, 23, 'roofbase_i'),
        tile(CONC, -1, 1, 11, 12, 24, 'inner_walk'),
    ]

def crown():
    g = []
    # outer slope: course 1 (z24-27) stud row 17.5 / slope 18.5 ; course 2 (z27-30) stud 16.5 / slope 17.5
    for x in (-0.5, 0.5, 1.5):
        g.append(P('3040b', ROOF, x, 17.5, 24, rot=0, tag=f'roofo1_{x}'))
        g.append(P('3040b', WHITE if x != 1.5 else ROOF, x, 16.5, 27, rot=0, tag=f'roofo2_{x}'))
    g.append(tile(CONC, -1, 2, 19, 20, 24, 'walk_o'))                  # gutter walkway
    # inner slope: course 1 stud 13.5 / slope 12.5 ; course 2 stud 14.5 / slope 13.5
    for x in (-0.5, 0.5):
        g.append(P('3040b', ROOF, x, 13.5, 24, rot=180, tag=f'roofi1_{x}'))
        g.append(P('3040b', ROOF, x, 14.5, 27, rot=180, tag=f'roofi2_{x}'))
    g.append(brick(HID, -1, 1, 14, 17, 24, 'ridge_fill1'))
    g.append(brick(HID, 1, 2, 16, 17, 24, 'ridge_fill1r'))
    g.append(brick(HID, -1, 1, 15, 16, 27, 'ridge_fill2'))
    g.append(plate(CONC, -1, 1, 14, 15, 30, 'ridge'))
    g.append(plate(CONC, -1, 2, 15, 17, 30, 'ridge_r'))
    g.append(tile(CONC, -1, 1, 14, 15, 31, 'ridge_t1'))
    g.append(tile(CONC, -1, 1, 16, 17, 31, 'ridge_t2'))
    g.append(tile(CONC, 1, 2, 16, 17, 31, 'ridge_t3'))
    g.append(P('3794b', CONC, 0, 15.5, 31, rot=0, tag='spk_jmp'))
    g.append(P('3024', CONC, 1.5, 15.5, 31, tag='spk_pl'))
    for x in (0, 1.5):
        g.append(P('85861', CONC, x, 15.5, 32, tag=f'spk_base{x}'))
        g.append(P('24482', WHITE, x, 15.5, 33, tag=f'spk{x}', zoff=4))
    return g

def build():
    g = joints() + inner_blocks() + spine_low() + pb()
    g += floor(8, 'P1', hinge=True) + spine_floor(8)
    g += floor(13, 'P2') + spine_floor(13)
    g += floor(18, 'P3', inclined=True) + spine_floor(18, y0=12, y0_at={19: 13})
    g += cloister_face() + cornice() + crown()
    return g

if __name__ == '__main__':
    from kit import check_ring
    check_ring(build())
