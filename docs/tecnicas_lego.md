# Techniques from official LEGO instructions, applied to Corona de Espinas

_Resumen del estudio de los libros de instrucciones oficiales (10276, 21035, 21056, 21061) hecho antes de diseñar el gajo. Las páginas y recortes citados (`crops/`, `pages/`, `sheets/`) no se redistribuyen; se regeneran con `scripts/pdf_pages.py` y `scripts/pdf_contact_sheets.py` a partir de los PDF públicos de LEGO._

This is a catalogue of building techniques taken from the official instruction PDFs of
10276 Colosseum, 21035 Guggenheim, 21056 Taj Mahal and 21061 Notre-Dame de Paris. For each
technique it notes how it could be used on the 1:250 Corona de Espinas model.

Model conventions: 1 stud = 2 m, 1 plate = 0.8 m, floor = 5 plates (4 m). A gajo is 4 studs
wide at the façade. Balcony bands are 2 plates thick and stick out 1 stud. The ring is 28 × 12°.

Part numbers are Rebrickable/BrickLink design IDs. They come from the official inventories
(saved in `parts/*.json` and flattened in `parts/all_parts.txt`) and were matched against the
instruction pages. When a part number is marked "(verify)", the pairing of that step with that
part was inferred.

Source PDFs (deleted after rendering to save disk space; download them again from these URLs):
- 10276 Colosseum: https://www.lego.com/cdn/product-assets/product.bi.core.pdf/6381439.pdf (book 1), 6381441 (book 2), 6381443 (book 3), 6381445 (book 4)
- 21035 Guggenheim: …/6199022.pdf
- 21056 Taj Mahal: …/6398433.pdf
- 21061 Notre-Dame: …/6634577.pdf
- 21042 Statue of Liberty: …/6532391.pdf. Not useful: its pedestal is square, and the star-shaped Fort Wood base is not modelled.

Folders: contact sheets (20 pages per image) in `sheets/<set>/`, full pages at 100–110 dpi in
`pages/<set>/`, and the selected crops in `crops/`.

---

## A. Curves and rings from repeated straight modules

### T1. Chain of identical wedge modules joined by 5.9 mm towball joints at 3 heights (the main Colosseum trick)
- **Source:** 10276 book 2 p105, p119–122 and p144 (a curved chain of 8 modules per bag). The same pattern repeats in books 3 and 4.
- **How it works:** each wall "pie-slice" module is built on a tan 2×8 plate (3034). A small plate carrying a ball or a socket is placed at each end of the module, at three levels: the base plate, mid-height, and the top. Each new module snaps onto the previous one ball-to-socket. The ball joint lets two neighbours rotate about a vertical axis, so the same module can follow any curvature. Along an oval the angle changes all the way round; the joints absorb that, and the module stays identical.
- **Parts:** 14419 plate 1×2 with towball socket + towball (dark bluish grey, 19 in the set); 14417 plate 1×2 with centre-side towball (79); 14704 plate 1×2 with centre-side towball socket (75); 22890 plate 1×2 with end towball (9). The joints are grey and sit hidden inside the wall thickness.
- **Crops:** `01_…b2p105`, `02_…b2p121`, `02b_…zoom`, `03_…b2p119`, `03b_…zoom`.
- **For Corona:** this solves the gajo hinge chain directly. Put a 14419 (or a 14417 + 14704 pair) on the base plate and on the roof plate of each gajo, so there are two joint levels. The 28 gajos can then be built identically and closed into the ring without any fixed angle. The ball joint takes a small vertical misalignment, but it will not hold 12° on its own. The fixed angle comes from the base (see T3), and the joints only keep neighbours flush. For the spike ring you could add a third joint level at mid-height.

### T2. Seam alignment check between modules ("✓ / ✗" callout)
- **Source:** 10276 book 2 p120 (crop `04_…b2p120`).
- **How it works:** a red-bordered callout compares a correct and a wrong seam. In the correct version the joint plates sit fully inside and the masonry courses line up across the seam. In the wrong version, grey joint plates show on the façade and the courses are offset by 1 plate. The designers accept that the façade shows a visible seam every module, but they line up every horizontal band across it so the eye reads a continuous ring.
- **For Corona:** make sure the three balcony bands and the floor-slab lines sit at exactly the same plate heights in every gajo. The radial seam is acceptable; a step in the bands is not. Put a similar ✓/✗ callout in your own instructions.

### T3. Wall module sits on a faceted base; the ring angle comes from the base
- **Source:** 10276 book 2 p104 (the first module placed on the base), book 1 p63–p80 (the rim).
- **How it works:** the base is an orthogonal Technic-brick frame (32531 and 32532 Technic bricks with openings, 3703 1×16 Technic brick, 2780 pins). Around it sit faceted rim segments of 3–4 dark grey 1×N brick columns. Each segment is built as a small sub-assembly and mounted sideways (SNOT) through Technic pin holes, 99207 inverted brackets and 87087 bricks with a side stud. The top is tiled (87079 tile 2×4, 26603 tile 2×3, 10202 tile 6×6), with only a few studs left exposed where the wall modules plug in. Tan 1×1 round plates (6141/85861) mark the pick-up points.
- **Crops:** `05_…b2p104`, `06_…b1p67`, `07_…b1p73`.
- **For Corona:** build the ring base as 28 wedge "sectors" on an orthogonal core, or as 4 quadrants of 7 gajos. Mostly tile the top and leave exposed only the 2–4 studs where each gajo plugs in. A gajo placed on tiles can still be rotated to its 12° position, and the plugged studs then lock it. The faceted plinth band around the ring can reuse the Colosseum rim idea: short 1×N columns mounted sideways, one facet per gajo.

### T4. Single-stud pivot tie plates across module joints (capping the top)
- **Source:** 10276 book 3 p109 (step 255), book 4 p233 and p239–245 (crops `09`, `10`).
- **How it works:** once the modules are joined, the top is capped with plates that rest on one stud of each neighbour. Those plates have rounded ends, so they can sit at an angle without their corners clashing. Longer inner parapet panels are then laid along the ring, and each panel bridges a joint. These panels are 1×2 or 1×3 wall panels, brick 1×2 with masonry profile, and tiles, built as ×N sub-assemblies such as "15×" and "8×" (book 4 p238 and p240). Because panels and joints are offset, no module seam runs through the full height.
- **Parts:** 35480 plate 1×2 rounded with 2 open studs (239 dark tan + 40 tan in the set); 77850 plate 1×3 rounded with 3 open studs (used in 21061); 15573 jumper 1×2 (237); 34103 plate 1×3 with 2 studs jumper (126); 4865b and 23950 panels.
- **For Corona:** use 35480 plates at the parapet or gutter line of the gable roof, pivoting on the last stud of each gajo, so the joint is covered at the roofline. For the 55-spike crown, mounting the spikes on these tie plates staggers them relative to the 28 seams (55 spikes ≈ 2 per gajo).

### T5. Curve in plan from curved bricks mounted sideways (Guggenheim spiral)
- **Source:** 21035 p110, p113, p116 (×2), p123 (crops `12`, `13`).
- **How it works:** the curved band is not built upright. White "curved slope" bricks with no studs are turned 90° and fixed to the side studs of a black SNOT core, so their curved top now faces outward as a convex band in plan. Sub-assembly: 30414 brick 1×4 with 4 side studs, plus 11211 brick 1×2 with 2 side studs or 87087 brick 1×1 with 1 side stud, then 11153 curved 4×1 or 50950 curved 3×1 on the side studs. 1×2 and 1×1 white plates (3023/3024) fill between them. The ends turn inward with 4070 headlight bricks and a 3040 slope. Each band ring is set back from the one below by a plate or a jumper offset, which gives the stepped spiral.
- **For Corona:** this gives a faceted or curved balcony front in 2 plates of thickness. Mount the front of each balcony band on 30414 or 11211 side studs, facing out, and clip a 1-plate-thick front onto it. Options: 11153 or 50950 for a gently curved front, 85984 slope 30 1×2×2/3 or 54200 cheese slopes for a faceted look, or 3069b tiles for a flat face. The band then sticks out a full stud without extra plates, and the SNOT depth equals the 1-stud cantilever.

### T6. Short curved chains from overlapping plates pivoting on one stud
- **Source:** 10276 book 2 p71–p80 (the hypogeum curved walls; sheet `sheets/10276_2/p061.jpg`).
- **How it works:** curved walls in the arena floor are chains of tan 1×N plates, each overlapping the next by one stud, so the chain can bend a few degrees at every overlap. A top layer of tiles and cheese slopes then locks the shape. No hinges are used.
- **For Corona:** use this for the curved edges of the central cloister terrace and the ring's inner courtyard kerb, built from 1×4 and 1×6 plates overlapping on single studs.

### T7. Drum and ring from macaroni bricks and tiles
- **Source:** 21056 p113 (crop `15`).
- **How it works:** a circular drum 6 studs across is made from 4 layers of 48092 brick round corner 4×4 macaroni wide, 2 bricks per layer, capped with 27507 tile 4×4 curved macaroni. It sits on top of a normal square SNOT core.
- **For Corona:** use the same parts, at small diameter, for the base of the star-shaped glass dome over the cloister, or for a round lightwell.

---

## B. Micro-scale façade detail

### T8. Arch-and-pillar sub-assembly built separately, then attached as one piece
- **Source:** 10276 book 2 p119 (step 294: a 5-step white inset), repeated in every module.
- **How it works:** a small inset shows an arch built upside-down: a 1×4 masonry brick (15533) on a 3659 arch 1×4, a 15573 jumper under the keystone, and an 85861 1×1 round plate as a column-capital spacer. Two 14716 1×1×3 bricks form the piers. The finished arch goes onto the module in one move. On the Colosseum façade, 4490 arch 1×3 (340 in the set) and 38585 arch 1½×1½ corner are the standard openings.
- **For Corona:** the recessed ground floor with white lattice screens can be one ×28 sub-assembly: a frame of 1×1×3 bricks carrying a 60592 or 90195 window 1×2×2 with a 38320 latticed pane, or a 3633 lattice fence. Build it as its own module and push it one stud back from the façade.

### T9. Pilasters and columns: SNOT strips and stacked round elements
- **Source:** 10276 book 3 p227 (step 546 ×2, crop `08`), 21061 p130 (28× columns, see `pages/21061/p130.png`).
- **How it works:** in the Colosseum, a pilaster strip is built flat: plate 1×8, tile, a cheese slope at the top as capital, and a 1×1 round plate. It is then mounted vertically on side studs (32952 brick 1×1×1⅔ with studs on 1 side, 39 in the set). Free-standing columns are 37762 candlestick (115 in 10276, 180 in 21061) or 20482 1×1 round tile with hollow bar. 21061 uses 2× 3062b 1×1 round bricks stacked, repeated 28 times.
- **For Corona:** use this for the vertical fins or mullions between the bays of the top floor, and for the V-brackets. A candlestick, or a 30374 bar in a 20482 tile, reads as a slender strut at 1:250.

### T10. Repeated window bay as a 3-part stack (×14)
- **Source:** 21061 p126 (crop `21`).
- **How it works:** stack 3004 brick 1×2 (tan), then 15573 jumper (dark tan), then a 3005 1×1 trans-clear brick, then a 3005 1×1 trans-black brick, then a 49307 1×1×⅔ double-curved top in black for the pointed head. The bay is 1 stud wide, alternates with solid piers, and is placed 14× in a single step.
- **For Corona:** a glazed band 1 stud wide, 5 plates high: 3024 plates in trans-clear or trans-black, or 3065 1×2 trans bricks, between 1×1 white piers. The jumper on top gives a half-stud offset, which can centre the glazing behind a balcony V-bracket.

### T11. Grilles, ingots, cheese slopes and half-circle tiles as texture
- **Source:** 21035 (2412b grille tile, 3070b trans-brown 1×1 tiles as windows, 24246 1×1 half-circle tile); 21056 (99563 ingot ×96 on the enclosure wall, 3070b checkerboard); 21061 (2877 brick 1×2 with grille, 2412b ×44, 49668 1×1 plate with tooth ×70).
- **For Corona:** 99563 ingot tiles make faceted spandrels on the balcony fronts. 2412b grille tiles give the ribbed look of a concrete underside at the level below a balcony. Rows of 49668 1×1 tooth plates give a sawtooth profile along the balcony edge.

### T12. Lattice railings and screens
- **Source:** 21056 p101 (step 153 ×4, crop `18`).
- **How it works:** 3633 fence lattice 1×4×1 sits on a 1×6 plate. A 4070 headlight brick at each end adds a small corner pier and gives a side stud for mounting.
- **For Corona:** use this for the white lattice screens on the recessed ground floor and for the cloister railings. For finer mesh, use 38320 latticed window pane 1×2×2 (in 21056) inside a 60592 window frame.

---

## C. Cantilevers, balconies, inclined floors, struts

### T13. SNOT depth equals a 1-stud cantilever
- **Source:** 21035 p110 and p116, 21056 p115, 10276 book 3 p227.
- **How it works:** in all three sets the outermost skin is mounted on side studs. Its thickness (1 plate ≈ 3.2 mm) plus the side-stud offset puts the skin about ⅓ to 1 stud beyond the core, so an overhang appears without any cantilevered plates.
- **Parts:** 11211, 30414, 87087, 4070, 99206 (plate 2×2×⅔ with 2 studs on side), 22885 (brick 1×2×1⅔ with 4 studs on 1 side), 32952, 26604 (1×1 with studs on 2 adjacent sides, which makes corners).
- **For Corona:** each balcony band can be a 2-plate slab (for example 3710 1×4 plate + 3023) that reaches 1 stud past the façade line. Its front fascia hangs on the slab edge through 99206 or 11211 SNOT and carries the faceted front (T5, T11). If you use 26604 at the gajo's side edges, the fascia can wrap the seam.

### T14. Diagonal struts from clip-and-bar arms (Notre-Dame flying buttresses)
- **Source:** 21061 p164 (step 193 ×12, crop `20`), p273 and p274 (step 371).
- **How it works:** 60478 plate 1×2 with handle on end, placed on a 3004 brick, holds a 59230 mechanical arm (droid, 2 clips at 90°). The arm clips onto a bar on the nave wall and sets its own angle. Similar joints use 78258 bar 2L with stop and 23443 bar holder with handle. 1927 hinge plate 1×4 swivel (32 in the set) gives angled plates.
- **For Corona:** use this for the diagonal struts of the inward-leaning top floor. Put a 60478 or 32828 (1×1 round plate with horizontal bar) on the balcony slab, then 59230 arms or 30377 battle-droid arms (40 in 21056) as V-struts up to a bar on the top-floor wall. For the lean itself, 2429/2430 hinge plates 1×4 on the top-floor slab and 1927 swivel plates both work. A cleaner option is to mount the whole top-floor façade panel on 73983 hinge plates 1×4 (32 in 10276) and set it to the inward angle.

---

## D. Domes, glass roofs, skylights, spikes

### T15. Sphere and dome on a SNOT core with quarter-dome bricks
- **Source:** 21056 p115 and p116 (crop `16`), p117.
- **How it works:** a core of 4733 brick 1×1 with studs on 4 sides, plus 52107 brick 1×2 with studs on 2 sides and grey 1×2 plates, carries four 93273 curved 4×1 double bricks sideways as the equator band. Blue 54200 cheese slopes fill the diagonal corners. Four 49612 brick round corner 4×4×3 quarter dome tops close the top half, and four more (8 in the set) the bottom half.
- **For Corona:** the star-shaped glass dome over the cloister is faceted, not smooth. Use the same SNOT core with trans-clear 54200 cheese slopes, or trans-clear wedge plates 51739 or 43722/43723, on the 4 side faces and the 4 diagonals. An 8-point star can be the 4733 core with 4 wedge sub-assemblies, plus 4 more rotated 45° on 18674 round 2×2 jumper plates.

### T16. Rooftop skylight on a big round plate: wedge plates plus a triple slope
- **Source:** 21035 p129 (crop `14`).
- **How it works:** a 6177b round plate 8×8 with centre 2×2 studs (or 11213 round plate 6×6 with hole) is doubled and carries two sand-green 51739 wedge plates 2×4, forming an elongated hexagonal glazed roof. Two 15571 slope 45 2×1 triple bricks sit on top as a small pyramid.
- **For Corona:** use the same layout for the half-hexagonal white skylights on the gable roof: a pair of 51739, or 43722/43723 wedge plates 3×2, plus a 15571 or 3044c double slope. For the glass sawtooth skylights of the cloister: rows of trans-clear 3040b slope 45 2×1 behind 3069b tiles.

### T17. Pinnacles and spikes from round-plate stacks and finials (×16 or ×30 in one step)
- **Source:** 21056 p119 (step 188 ×16, crop `17`); 21061 p273, p274 and p276 (crop `19`).
- **How it works (Taj):** a 3024 plate 1×1, 2× 85861 round 1×1 plates with open stud, and a 90540 bar 3L (ski pole) plugged into the open stud. The inventory lists 16 ski poles and 32 open-stud round plates.
- **How it works (Notre-Dame):** 3–4 stacked 85861 round plates carry a 24482 spear tip with fins (30), a 6124 magic wand (40) or a 59900 cone 1×1 with top groove.
- **Other spike options:** 22388 slope 45 1×1×⅔ quadruple convex pyramid (20 in 21042), 49668 tooth plates, 89522 unicorn horn (in 21042).
- **For Corona:** the 55 white pyramidal spikes of the crown. The closest shape at 1:250 is a white 22388 pyramid on a 1×1 round plate, or a white 59900 cone on 1–2 85861 plates for a taller spike. Both are 1 stud across, which is 2 m. Place them on the T4 tie plates or on the roof ridge. Draw the spike once as a sub-assembly and call it out ×55, or ×2 per gajo in 28 steps. That is the same way both sets handle repeated finials.

### T18. Triangular tile floors and star patterns
- **Source:** 21061 p126 and p130: nave floor made of 35787 tile 45° cut 2×2 (triangle), 72 black + 70 white.
- **For Corona:** tile the cloister terrace with 35787 triangles in white and light bluish grey. They can also spell out the 8-point star plan of the dome at floor level. 27263 facet corner tiles (21056) make the 45° corners of the terrace.

---

## E. Base, landscaping, trees

### T19. Micro trees: cones on a bar, flower stems, stacked flower plates
- **Source:** 10276 book 4 p250 (crop `11`); 21061 p280 (crop `22`).
- **How it works:** Colosseum cypresses are 2× 59900 green cone 1×1 threaded point-to-point on a 30374 bar 4L, or larger 3942c cones 2×2×2 on a 63965 bar 6L. Notre-Dame trees are a 64644 telescope trunk with a 19119 flower stem with 6 stems and 24866 1×1 flower plates on each stem. Shrubs are 2× stacked 24866.
- **For Corona:** use 24866 and 19119 for the trees around the ring (the park setting), 59900 cone pairs for columnar trees, and single 24866 in dark green for the planters on the cloister terrace.

### T20. Tile-dominant base with a few studs as anchors; the base is modular too
- **Source:** 10276 book 1 p9–p20: the base is 2+ big sections built separately ("2×") and pinned together through Technic bricks (2780 pins, 32054 long pins with stop). 65803 brick 16×16 with pin holes serves as the lower-arena floor. 21061 p6–p20: the base is plates, then tiles, with only a few 1×1 round plates as stud anchors.
- **For Corona:** build the ring base in 4 quadrant sections, each 7 gajos, pinned together through 3700 or 3703 Technic bricks. The model then comes apart for transport, and each quadrant is a natural book or bag in the instructions.

---

## F. Presentation of repeated sub-assemblies

### T21. Instruction conventions worth copying
- **Source:** all four sets.
- **What they do:**
  - The bag or book start page shows the result of that bag. The Colosseum has 40 bags, and bags 11–18 each produce one curved 8-module chain (book 2 p105, p121, p136, p152, p224).
  - At the start of each repeated module, a white inset shows the finished module as a thumbnail (for example book 2 p121 top left). Every step is repeated in full for every module; the Colosseum does not use "build this ×8" loops for wall modules. Only small parts get ×N (2×, 4×, 14×, 15×, 16×, 28×).
  - Red outlines mark the new parts in each step. Newer sets (21061) use green arrows.
  - A rotate icon appears before any step that must be built from underneath.
  - Sub-assemblies go in a white inset with numbered sub-steps (1, 2, 3, 4) and a "×N" in the corner. A 1:1 length check is used for bars and long tiles (21035 p96).
  - ✓/✗ callouts show alignment where a mistake would be invisible until later (T2).
  - Short historical text panels break up long repetitive runs. This is a pacing device.
- **For Corona:** show one gajo in full detail, then ×27 with its thumbnail. The alternative is to repeat full steps per gajo, as in the Colosseum, which gives huge page counts. Use ×N callouts for the lattice screen, the balcony front, the spike and the V-bracket sub-assemblies. Add a ✓/✗ callout for the band alignment and for the hinge orientation.

### T22. Vertical exaggeration
- **Source:** 10276 book 3 p6 text: "If built exactly to scale, this LEGO model would actually be lower in height… [the designer] used vertical exaggeration."
- **For Corona:** at a true 5 plates per 4 m floor, the building is quite flat for its 83 m diameter. Official designers openly stretch height for legibility. Adding 1 plate per floor (6 plates) or making the balcony bands 3 plates thick would be a legitimate design choice if the model reads too flat.

---

## Geometry note: a 4-stud gajo vs an 83 m ring

- A ring of 28 flat modules at 12° each covers 336°. Check whether the missing 24° (2 gajo positions) is intentional, for example entrances.
- If hinge axes sit at the façade line and the gajo is W studs wide there, the polygon's vertex radius is R = W / (2·sin 6°) = 4.78·W. W = 4 gives R = 19.1 studs = 38.3 m, a diameter of about 76.5 m.
- For an 83 m façade diameter (R = 20.75 studs), the façade chord is 4.34 studs. Either accept the smaller ring, make the façade 4⅓ studs by closing the ~0.34-stud gap with a T4 tie plate or a hinge-cover tile, or put the 4-stud line at an inner wall.
- The balcony fronts sit 1 stud further out. On a 19.1-stud façade radius, the balcony chord is 2·20.1·sin 6° = 4.2 studs, so a 4-stud-wide band leaves about 0.2 stud (1.6 mm) of open V-gap per joint. On an 83 m façade it is 4.55 studs, leaving about 0.55 stud. Either way the gap has to be covered (T4, T5 wrap-around with 26604) or turned into a design feature, for example a V-bracket that hides it.

---

## Crop files (`crops/`)

| File | Shows |
|---|---|
| 01_colosseum_module_and_curved_chain_b2p105.png | Bag start: one wall module plus the curved chain of 8 it builds |
| 02_colosseum_module_baseplate_towball_socket_b2p121.png | Module base plate with towball and socket plates |
| 02b_colosseum_zoom_towball_socket_plate_b2p121.png | Zoom on the 14419 socket+ball plate (step 299) |
| 03_colosseum_arch_subassembly_and_side_joints_b2p119.png | Arch sub-assembly inset (5 sub-steps) and joints at 3 heights |
| 03b_colosseum_zoom_joints_3_levels_b2p119.png | Zoom: ball and socket plates at base, mid and top of the module |
| 04_colosseum_seam_alignment_check_b2p120.png | ✓/✗ seam alignment callout |
| 05_colosseum_first_module_on_base_b2p104.png | First module placed on the tiled base |
| 06_colosseum_faceted_base_rim_b1p67.png | Faceted SNOT rim segments round the orthogonal base |
| 07_colosseum_rim_segment_snot_b1p73.png | Building one rim facet |
| 08_colosseum_pilaster_snot_subassembly_b3p227.png | Pilaster strip built flat, then mounted vertically |
| 09_colosseum_tall_module_top_tie_b3p109.png | Tall module with a rounded tie plate on top |
| 10_colosseum_parapet_panels_bridge_joints_b4p239.png | Parapet panels that bridge the module joints |
| 11_colosseum_cypress_trees_b4p250.png | Cone-on-bar cypress trees |
| 12_guggenheim_curved_band_subassembly_p116.png | Curved band: 11153 sideways on 30414 |
| 13_guggenheim_band_on_snot_core_p110.png | Band placed on the building; headlight-brick end |
| 14_guggenheim_round_roof_skylight_p129.png | Round roof plate with wedge-plate skylight and triple-slope peak |
| 15_tajmahal_drum_macaroni_ring_p113.png | Drum from 48092 and 27507 macaroni parts |
| 16_tajmahal_dome_snot_core_p116.png | Dome: 4733 core, 93273 band, 49612 quarter domes |
| 17_tajmahal_pinnacles_x16_p119.png | Pinnacles ×16: round plates plus ski pole |
| 18_tajmahal_lattice_railing_p101.png | 3633 lattice railing sub-assembly ×4 |
| 19_notredame_spike_pinnacles_p274.png | Spear-tip and cone spikes on stacked round plates |
| 20_notredame_buttress_arms_diagonal_struts_p164.png | 59230 arms on 60478 as diagonal struts ×12 |
| 21_notredame_repeated_window_bay_x14_p126.png | 1-stud window bay ×14 |
| 22_notredame_trees_shrubs_p280.png | Flower-stem trees and stacked-flower shrubs |
