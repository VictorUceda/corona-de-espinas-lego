# AGENTS.md: contexto de trabajo para agentes

Este documento contiene todo lo necesario para que un agente de IA continúe el proyecto o diseñe con la misma
metodología una maqueta LEGO de otro edificio sin partir de cero. Léelo entero antes de tocar nada.

---

## 1. Qué es y en qué estado está

- **Modelo:** Corona de Espinas (sede del IPCE, Higueras y Miró, Madrid) a escala 1:250.
  - 4.937 piezas, 102 lotes y 8 colores: LBG 71, DBG 72, White 15, Black 0, Trans-Clear 47, Tan 19, Reddish Brown 70 y Dark Green 288.
  - 28 gajos y 55 espinas; Ø 35 cm.
- **Estado:** completo y verificado (`dist/verification_report.json`, `ok: true`). Entregables:
  - modelo LDraw;
  - libro de instrucciones con notas de arquitectura y de técnica LEGO (153 pasos, 79 páginas);
  - vídeo del montaje;
  - visor 3D autónomo;
  - lista de BrickLink.
- **Pendiente u opcional:**
  - consultar la guía de precios de BrickLink para esta lista (`data/price_guide.json`) y regenerar `dist/piezas.csv` con los costes;
  - la cúpula 50990b en Trans-Clear figura con 0 sets en Rebrickable, pero existe en venta en BrickLink;
  - vídeo de presentación corto (documentos → montaje → libro pasando páginas), si se pide.

## 2. Reglas del encargo (vinculantes salvo que el usuario diga otra cosa)

1. **Piezas:** solo piezas LDraw oficiales (`!LDRAW_ORG` sin `Unofficial`). Nada de stickers, piezas impresas ni custom.
2. **Disponibilidad:** cada combinación pieza + color debe existir en BrickLink con al menos 3 vendedores de piezas nuevas.
3. **Colores:** 8 como máximo, y comunes.
4. **Técnicas:** solo las legales del BrickLink Designer Program. Nada tensionado, forzado ni fuera de sistema salvo geometría exacta demostrada.
5. **Herramientas:** sin Blender en ninguna fase. Se usa Python (trimesh, python-fcl, networkx), three.js con LDrawLoader, Playwright y ffmpeg.
6. **Formato del modelo:** `.mpd` con submodelos.
7. **Criterio de fidelidad:** la estética exterior y las fotografías pesan más que la exactitud arquitectónica, pero los detalles ocultos reales (estructura, ejes, patinejos) son un valor añadido para un público de arquitectos.
8. **Compras:**
   - nunca confirmar un pedido ni hacer checkout sin el OK explícito del usuario;
   - preparar carritos y subir listas sí está permitido si lo pide.
9. **Material de referencia:** es personal. No redistribuir fotos, planos ni artículos. Solo están en el repositorio los datos abiertos de `refs/geo` y el BOE (ver §9).
10. **Textos del libro:**
    - explican la técnica o el dato del edificio; no dicen de qué set oficial viene la idea;
    - no hay textos que expliquen lo obvio;
    - no se menciona ninguna versión anterior ni el modelo de IA usado.

## 3. Mapa del repositorio y pipeline

```
scripts/
  ldr.py            biblioteca LDraw: búsqueda, mallas BFC, snaps de LDCad Shadow, line1(), caché en .cache/
  kit.py            P(part,color,x,y,z,rot,tag,zoff), box(kind,color,x0,x1,y0,y1,z,tag), SIZES, ALPHA, J1, J2,
                    check_ring() (colisiones y uniones con el gajo vecino), mpd()
  collide.py        colisiones FCL con mallas reducidas TOL = 0,1 LDU (inset por mínimos cuadrados), ASSEMBLY_PAIRS
  connect.py        uniones por snaps (cilindros macho/hembra coaxiales, solape y radio) y grafo networkx
  verify.py         verificación completa (§5); SPEC = orden de montaje por submodelos
  core.py           cells_disk, cover (recubrimiento voraz por rectángulos), coarse_disk, BIG/BIGT
  gajo_base.py      geometría de la cadena: articulaciones J1/J2, bloques interiores, espina baja, crown()
  gajo.py           gajo detallado (fachada), build() = gajo_tipo
  base.py           placa base, podio, ejes de replanteo, parque (olivos)
  claustro.py       vestíbulo, estanque con escultura, pilares, biblioteca, vigas, plaza, cúpula
  entrada_base.py   trazado del cañón, pasarelas y escalinata; recorte contra los gajos extremos
  entrada.py        testeros solo con placas (textura de encofrado)
  build_model.py    ensambla dist/model.mpd (gajo_fin = gajo sin la espina del nervio -> 55 espinas)
  steps.py          pasos de 1-8 piezas a partir del orden verificado -> build/instructions/
  steps_core.py     utilidades de pasos (chunk, write_ldr)
  notas.py          fuente única de las notas del libro (INTRO + NOTES con triggers por tag)
  book.py           HTML del libro (estilo en book_style.py) -> render/pdf.mjs -> dist/instrucciones.pdf
  anim.py           orden de animación, model_packed.mpd, viewer.html, visor_3D.html autónomo
  pack.py           embebe todas las piezas en el .mpd (sin biblioteca LDraw)
  bom.py            BOM + comprobación en Rebrickable (REBRICKABLE_KEY) -> data/bom_rebrickable.json
  purchase.py       dist/wanted_list.xml y dist/piezas.csv (+ costes si hay data/price_guide.json)
  rebrickable.py    cliente de la API v3 (1 petición/s, reintentos 429)
  preview_ring.py   vista rápida del anillo -> build/ring.mpd
  build_reference.py  modelo de referencia del edificio -> data/reference.json, planta.svg, alzado.svg
  analyze_geo.py, geo_images.py, section_profile.py, count_modules.py   LiDAR y ortofoto -> radios, alturas, módulos
  fetch_commons.py, fetchref.py, ahdb.py, refindex.py   descarga de fuentes y catálogo refs/index.json
  pdf_pages.py, pdf_contact_sheets.py, contact.py       estudio de PDFs de instrucciones oficiales (hojas de contacto)
render/
  render.mjs + scene.html          render de un .ldr/.mpd a PNG (servidor local + Chromium headless)
  render_steps.mjs + steps.html    imágenes de cada paso (piezas nuevas con contorno amarillo) y miniaturas
  pdf.mjs                          HTML -> PDF (page.pdf)
  viewer_template.html             visor/animación three.js (InstancedMesh, cinemática, motion blur)
  record.mjs                       fotogramas deterministas: build (40 s), wow (16 s), turntable (12 s)
data/   reference.json, planta.svg, alzado.svg, bom_rebrickable.json, lego_sets/ (inventarios de sets oficiales)
refs/   index.json (catálogo de todas las fuentes), geo/ (Catastro, PNOA, LiDAR), texts/ (BOE)
docs/   notas.md (generado), diseno.md, tecnicas_lego.md (22 técnicas extraídas de sets oficiales), img/
dist/   entregables (versionados)
build/  intermedios (ignorado por git)
tools/  ldraw/ (complete.zip) y shadow/ (LDCad Shadow Library) (ignorado por git; ver README)
```

Orden completo de regeneración (unos 15 minutos en un portátil):

```bash
python scripts/build_model.py && python scripts/verify.py
python scripts/notas.py && python scripts/steps.py && node render/render_steps.mjs
python scripts/book.py && node render/pdf.mjs
python scripts/anim.py && node render/record.mjs build 1920 1080 build/frames && ffmpeg ... dist/build.mp4
python scripts/purchase.py
```

- Ejecuta los scripts desde la raíz del repositorio; `ldr.ROOT` se calcula a partir de la ubicación del archivo.
- Para iterar rápido: `python scripts/gajo.py` (check_ring del gajo) y `python scripts/verify.py --quick` (sin barridos, unos 15 s).

## 4. Convenciones geométricas

- **LDU:** 1 stud = 20 LDU, 1 placa = 8 LDU, 1 ladrillo = 24 LDU. En LDraw, −Y es arriba.
- **Coordenadas de diseño** (kit.P): `x` y `y` en studs en planta, `z` en placas sobre la cara superior de la placa base.
  - LDraw: `X = 20x`, `Z = −20y`, `Y = −8z − bottom(part)`.
  - `zoff` sustituye al offset automático del fondo de la pieza. Úsalo con barras y piezas cuyo origen no está en la base: 24482, bisagras.
- **Cuadrícula global:** el origen está en el centro del edificio y los centros de stud en semienteros.
  - `box()` elige la pieza rectangular por su tamaño.
  - `cover()` recubre un conjunto de celdas con rectángulos.
- **Gajo** (marco local, eje +y radial hacia fuera, +x horario):
  - `ALPHA = 2·atan(1/9,5) = 12,018°`, el único ángulo con el que dos puntos del nervio, J1 = (±1; 9,5) y J2 = (±2; 19), son puntos de la red en los dos gajos vecinos.
  - J1: 18674 (plato redondo 2×2 con stud central, lado izquierdo, abajo) dentro de 4032b (lado derecho, arriba).
  - J2: bisagra giratoria 2429 (base, izquierda) + 2430 (superior, derecha), a z8.
  - Cuadrícula Gi (filas centradas en enteros) para el bloque interior; cuadrícula Go (semienteros) para el cuerpo; ambas cosidas con jumpers 3794b en radial.
- **Montaje por gravedad:** se coloca en sentido antihorario y el lado derecho del gajo nuevo baja sobre el izquierdo del anterior. Zonas de exclusión:
  - nada por encima de z3 en el círculo J1 izquierdo;
  - nada por debajo de z4 en el círculo J1 derecho;
  - **nada por encima de z8 en (−1,5; 19,5) y nada por debajo de z8 en (1,5; 18,5–19,5)**. Ahí baja la bisagra del vecino.
  - La columna +1,5 cruza el nervio derecho: solo se usa por encima de z8.
- **Filas de fachada:** 19,5 PB · 20,5 ventanas · 21,5 punta de bandeja · 22,5 cornisa. Cara del claustro en y = 11.
- **Alturas** (placas): podio 0–2 · PB 2–8 · P1 8–13 · P2 13–18 · P3 18–24 (6 placas, exageración vertical) · cornisa 24 · cubierta 25–31 · cumbrera 31–33 · espinas hasta unos 41.
- **Tags:** cada pieza lleva un `tag` descriptivo (`P2_soffit-0.5`, `rim_o1.5`...).
  - Sirven para depurar, para dividir en submodelos y como *trigger* de las notas del libro.
  - Al releer el .mpd se pierden y `steps.retag()` los recupera por matriz.

## 5. Qué comprueba `verify.py` (y cómo interpretar los fallos)

1. **Conectividad:** grafo de uniones por snaps y un solo componente. Una isla es una pieza que solo se apoya o que cae en una rejilla desplazada.
2. **Colisiones:**
   - cada malla se contrae 0,1 LDU con un inset por mínimos cuadrados, con vértices soldados a 0,02 LDU;
   - el inset por normal promedio fallaba con caras planas junto a curvas finamente teseladas: daba falsos choques en 24201;
   - `ASSEMBLY_PAIRS` admite pares diseñados para interpenetrarse (2429/2430) solo si están unidos por su pivote.
3. **Construibilidad:**
   - se sigue el orden: base (grow) → anillo (gajos antihorarios, cada uno como bloque premontado) → claustro_pilares (grow) → claustro_plaza (submontaje) → claustro_cupula → entrada;
   - cada pieza o bloque debe unirse a algo ya colocado y poder bajar (o subir) en vertical sin tocar nada, en pasos de 2 LDU;
   - dentro del gajo se admiten piezas que **se apoyan** y que un paso posterior atrapa (`rests_on`). Así se colocan los 24201, que no tienen anti-studs.
4. **Estabilidad:** centro de masas dentro del polígono de apoyo; ninguna pieza con una sola unión y el centro de masas a más de 0,6 studs.
5. **Resistencia:** en cada plano horizontal, uniones más piezas que lo atraviesan ≥ K_MIN. El mínimo está a z35, en la base de las espinas: 55.

Un fallo de barrido ("insertion blocked by 2429") casi siempre significa que algo del gajo invade una zona de exclusión (§4). El análisis estático no lo detecta.

## 6. Libro de instrucciones

- **Pasos:** `steps.py` agrupa el orden verificado en pasos de 1 a 8 piezas y crea uno nuevo si la altura salta más de 3 placas.
  - El gajo se muestra una vez con ×28.
  - La plaza es un submontaje.
- **Notas:** `notas.py` es la fuente única.
  - Cada nota lleva `sec`, `kind` ('arq' = edificio real, 'lego' = técnica), `trigger` (prefijo de tag), `title` y `text`.
  - La nota aparece en el primer paso que contiene una pieza con ese tag, o en la portadilla de la sección si `trigger=None`.
  - Una página con notas muestra 2 pasos y una columna de hasta 3 notas; las que sobran pasan a las páginas siguientes.
- **Estilo:** A4 apaisado, portada partida (panel oscuro y render), badges amarillos de sección, cajas azules de piezas, contorno amarillo en las piezas nuevas, inventario e índice de fuentes.
- **Renders:** `render_steps.mjs` usa cámara ortográfica y fondo blanco, y atenúa las piezas anteriores.

## 7. Vídeo y visor

- `viewer_template.html` aplana el .mpd en el mismo orden que `verify.flatten` y dibuja una `InstancedMesh` por pieza y color. El guion `scheduleCinematic` es:
  1. lluvia de la base;
  2. gajos montados en el aire y soltados, con rampa de velocidad;
  3. plaza soltada;
  4. cúpula y entrada;
  5. coronación con las espinas en ola y a cámara lenta.
- `record.mjs` usa un reloj determinista y motion blur con 8 subfotogramas: unos 3 minutos para 1.200 fotogramas en 1080p.
- `anim.py` genera también `dist/visor_3D.html` con el .mpd incrustado en un `<script type="text/plain">`, para abrirlo con doble clic.

## 8. Compra

- `bom.py` hace el mapeo LDraw → BrickLink con la API de Rebrickable y comprueba que cada lote tiene `num_sets > 0`.
  - Rebrickable no es definitivo: una pieza puede tener 0 sets y aun así venderse en BrickLink.
- Guía de precios: se consulta en BrickLink desde el navegador del usuario, con su sesión iniciada.
  - Usa fetch same-origin de las páginas del price guide, despacio porque BrickLink devuelve 429.
  - Se guarda en `data/price_guide.json` y `purchase.py` calcula los costes.
- La wanted list se sube con Wanted List → Upload. Para comprar se usa la página Buy con el filtro de la UE y Auto-select, y se crean carritos por tienda. **No hacer checkout nunca.**
- Sustituciones descubiertas:
  - la placa 1×4 Trans-Black no existe (se usa Black);
  - 4032b Trans-Clear no existe (se usa 3941 Trans-Clear);
  - las placas 2×2 y 4×4 Dark Green no existen (se usan otros tamaños);
  - la placa base 4186 verde es cara (se usa LBG);
  - el tile 8×16 no tiene stock.

## 9. Fuentes y derechos

- `refs/index.json` cataloga todas las fuentes, con URL, autor, licencia y vista.
- **Solo** se versionan los datos abiertos: `refs/geo`, con Catastro (uso libre con cita) y PNOA ortofoto/LiDAR (© IGN, CC BY 4.0 scne.es), y `refs/texts/boe_*` (dominio público).
- Fotos de Commons, planos del AHDB/ETSAM, revista COAM, artículos y PDFs de LEGO:
  - se descargan de nuevo con los scripts de §3 y nunca se suben;
  - `.gitignore` los excluye.

## 10. Lecciones aprendidas (errores que no hay que repetir)

- **pip:** si apunta a un registro privado, usa `PIP_CONFIG_FILE=/dev/null pip install --index-url https://pypi.org/simple ...`.
- **Wikimedia:** devuelve 429. Usa miniaturas de 1920 px y reintentos lentos.
- **three.js 0.170:** `LDrawLoader.load()` reinicia los materiales. Usa `fetch` + `loader.parse()`. El color de las líneas condicionales se cambia con `.set()`.
- **Matrices:** 4 decimales en `line1` producen artefactos de colisión cerca del eje. Se escriben 6.
- **Snaps:** hay que aceptar ejes antiparalelos y comparar el radio en la sección solapada (6141, stud hueco).
- **24201** (curva invertida 2×1): tiene la parte superior escalonada y **ningún anti-stud**. Se cuelga desde arriba: placa sobre el stud bajo y tile sobre el alto. Debajo no puede haber studs: termina la persiana en tile.
- **3665a** (pendiente invertida): tiene el stud de arriba también en la celda del voladizo, y choca con piezas sin anti-stud apoyadas encima.
- **11477:** el anti-stud está en el extremo **bajo**. Girado 180° (alto hacia fuera) sirve como canalón visto.
- **Tornapuntas del gajo:** una rama hacia la derecha invade (1,5; 19,5) por debajo de z8, así que va una sola rama por gajo.
- **Recubrir anillos finos:** `ring_cells` exige las 4 esquinas en la banda, y una banda de menos de 1,4 studs puede quedar vacía. Comprueba siempre el número de piezas.
- **Zona con studs del podio:** r < 8,4 solo en el núcleo. Fuera hay tiles: lo que apoye ahí queda aislado salvo que se ancle al anillo.
- **Rim de un disco hecho con placas:** deja celdas 1×1 sueltas. Solución: anillos de vigas debajo y `bridged_cover` (cubrir cada 1×1 con un 1×2).
- **Guía de precios de BrickLink:** 429 frecuentes. Una petición cada 1–2 s.
- **Easy Buy:** no deja cambiar la lista por defecto. Usa la página Buy con los filtros.
- **Verificación rápida:** `--quick` no hace barridos y puede dar OK con 27 fallos de inserción. Pasa siempre la completa antes de dar algo por terminado.

## 11. Metodología para una maqueta nueva (reutiliza el pipeline, no empieces de cero)

1. **Fase 0 · Fuentes:** fotos (Commons), planos (archivos), textos, ortofoto/LiDAR/catastro si es España (PNOA/Catastro). Catálogo en `refs/index.json` con `refindex.add()`.
2. **Fase 1 · Referencia:** `reference.json` (radios, alturas, módulos, colores con hex medidos), `planta.svg` y `alzado.svg`. **Parar y pedir OK.**
3. **Fase 2 · Traducción a LEGO:** 2–3 opciones de escala con piezas y coste estimados. Busca la geometría exacta: ángulos que caigan en la red, como ALPHA. Elige un módulo repetible (el "gajo") y un submodelo por módulo. Documenta las decisiones en `docs/diseno.md`.
4. **Fase 3 · Verificación:** adapta `verify.SPEC` al orden de submodelos. Itera hasta 0 fallos, con `check_ring` para módulos repetidos.
5. **Fase 4 · Instrucciones:** `notas.py` (arquitectura y técnica), `steps.py`, `render_steps.mjs`, `book.py` y `pdf.mjs`.
6. **Fase 5 · Compra:** `bom.py`, guía de precios, `purchase.py`, subir la wanted list y carritos. Sin checkout.
7. **Fase 6 · Vídeo y visor:** `anim.py`, `record.mjs` (ajusta las claves de tiempo y la cámara de `SC.build` en `viewer_template.html`) y ffmpeg.

Qué se reutiliza tal cual: `ldr`, `kit`, `collide`, `connect`, `verify`, `core`, `pack`, `steps_core`, `book_style`, `book`, `steps`, `anim`, `purchase`, `bom`, `rebrickable` y todo `render/`.
Qué se reescribe: `gajo_base`/`gajo` (el módulo), `base`, `claustro`/`entrada` (piezas singulares), `build_model` (ensamblaje), `notas` y `build_reference`.

Para diseñar mejor, antes de dibujar el módulo estudia 2–4 libros de instrucciones oficiales de edificios parecidos: `pdf_pages.py` y `pdf_contact_sheets.py`, más inventarios en `data/lego_sets/`. Extrae técnicas concretas con número de pieza. `docs/tecnicas_lego.md` es el ejemplo.

## 12. Prompt para empezar otra maqueta

Copia y rellena lo que va entre corchetes:

```text
Diseña una réplica de [EDIFICIO] ([ARQUITECTOS], [DIRECCIÓN / CIUDAD]) construible con LEGO real,
reutilizando el pipeline de este repositorio (lee AGENTS.md entero antes de empezar; no partas de cero).

Entregables: modelo verificado (.mpd con submodelos), instrucciones PDF estilo LEGO con notas de arquitectura
y de técnica LEGO junto a cada paso, lista de BrickLink (wanted_list.xml + piezas.csv), visor 3D autónomo y
vídeo del montaje (piezas volando, rampas de velocidad).

Restricciones: solo piezas LDraw oficiales (sin stickers, impresas ni custom); cada pieza+color con ≥3 vendedores
de nuevo en BrickLink; ≤8 colores comunes; solo técnicas legales BrickLink Designer Program (nada forzado ni
tensionado); sin Blender; tope de [N] piezas; presupuesto [€]. Prioridad: estética exterior y fotografías
sobre exactitud arquitectónica, más detalles ocultos reales que sorprendan a un arquitecto.

Fases: 0 fuentes (refs/ + refs/index.json con url, licencia y vista) · 1 reference.json + planta.svg + alzado.svg
y PARA a esperar mi OK · 2 traducción a LEGO con 2-3 escalas justificadas · 3 verificación hasta 0 fallos
(conectividad, colisiones 0,1 LDU, construibilidad por barrido, estabilidad, resistencia) · 4 instrucciones
(1-8 piezas por paso, callouts ×N, renders isométricos, PDF) · 5 compra (Rebrickable, guía de precios, wanted list,
carritos UE; NO confirmes ningún pedido sin mi OK) · 6 visor y vídeo.

Estudia antes 2-4 libros de instrucciones oficiales de edificios con retos parecidos ([SETS]) y aplica sus
técnicas. El material de referencia es personal: no lo redistribuyas. Trabaja de forma autónoma y avísame solo
en las paradas indicadas.
```
