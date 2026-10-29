# Informe de laboratorio: Verovio 6.1.0 → 6.3.0

Rama `lab-6-1-a-6-3` del fork `repepone/verovio`, solo para estudio. Sin PR hacia el original.
Fecha de las mediciones: 2026-10-29.

## Resumen en llano

- **Las alteraciones se corrigen.** 6.1.0 deduce la altura de cada nota a partir de la armadura y de las alteraciones anteriores del compás, e ignora `<alter>`. 6.3.0 usa `<alter>`. En 9 MusicXML públicos y un caso sintético, 6.1.0 da 105 notas con altura MIDI errónea (50 de ellas en un Schubert exportado con Sibelius). 6.3.0 no da ninguna.
- **Aparecen ligaduras que faltaban.** Con la altura mal deducida, 6.1.0 no podía cerrar algunas ligaduras sobre la barra y no las dibujaba. 6.3.0 deja 3 ligaduras abiertas donde 6.1.0 dejaba 26.
- **El timemap no cambia**, salvo los ids. Coinciden el número de entradas, los tiempos y las notas en todos los casos. `getElementsAtTime` ya devuelve la página correcta en partituras de varias páginas; 6.1.0 se equivocaba.
- **El SVG cambia algo.** Desaparecen muchos `<g class="accid">` vacíos que llevaban id. Entran las ligaduras nuevas y dos reglas CSS `g.cursor`. En una partitura con letra (Beach) cambia el reparto de compases por sistema y la anchura del modo continuo.
- **Va más rápido.** Carga más SVG: un 20 % menos de tiempo (suma de medianas). Timemap: un 27 % menos. El módulo WASM pesa un 4,5 % más y tarda unos 18 ms más en arrancar.
- **Un riesgo nuevo.** Un MEI con un número no válido en ciertos atributos (`@tstamp="abc"`) hace que 6.3.0 lance una excepción WASM; 6.1.0 lo cargaba. Con MusicXML no se ha probado.
- Ninguna opción se renombra ni se retira, y ningún valor por defecto cambia.

Cada afirmación lleva una de dos marcas: **[leído]**, sacado del código, los commits, el changelog o los ficheros del repo o del paquete; o **[medido]**, sacado de ejecutar los scripts de `lab/` en esta sesión. Al final está la lista **SIN MEDIR**.

---

## 0. Licencia

- **[leído]** `COPYING.LESSER` es la GNU LGPL v3 (29-06-2007), que incorpora la GPL v3 de `COPYING` con permisos adicionales. `README.md` dice: «Verovio is available under the LGPL license (see COPYING and COPYING.LESSER)».
- **[leído]** Las cabeceras de los fuentes (p. ej. `src/note.cpp`) solo dicen «Copyright (c) Authors and others. All rights reserved.», sin identificador SPDX.
- **[leído]** El identificador no es igual en todas partes:
  - En `develop` es `LGPL-3.0-only`: `codemeta.json`, `pyproject.toml` y `emscripten/npm/package.json`, por el commit b6903d8e6 «align license identifiers» del 2026-10-14.
  - En los commits de release 6.1.0 y 6.3.0, `emscripten/npm/package.json` decía `LGPL-3.0-or-later`.
  - **[medido]** El `package.json` de los paquetes npm `verovio@6.1.0` y `verovio@6.3.0` instalados dice `"license": "LGPL-3.0-or-later"`.
- **[medido]** El tarball npm contiene solo `README.md`, `dist/` y `package.json`. No incluye `COPYING` ni `COPYING.LESSER`.
- **[leído]** La LGPL v3 §4 exige, para una «Combined Work», un aviso visible de que se usa la biblioteca bajo esta licencia y acompañarla de copias de la GPL y la LGPL. Si la biblioteca no se enlaza como biblioteca compartida (§4 d 1), pide además dar el código fuente mínimo correspondiente (§4 d 0). Un visor web que sirve el WASM tiene que poner esos textos por su cuenta, porque el paquete npm no los trae. Esto es una lectura del texto, no asesoramiento legal.
- **[leído]** Para este laboratorio: el fork es público y solo se suben scripts y resultados propios. Los MusicXML de prueba no se suben, porque cada obra del corpus de music21 tiene su propia licencia (`music21/corpus/license.txt`); `lab/fetch-corpus.sh` los descarga.

## 1. Cambios entre 6.1.0 y 6.3.0

### Cómo se ha delimitado el rango

- **[medido]** `npm view verovio@6.1.0 gitHead` da `682d60684450…` y `verovio@6.3.0` da `425dd7b6ba26…`. `getVersion()` devuelve `6.1.0-682d606` y `6.3.0-425dd7b`.
- **[leído]** Los commits «Release 6.1.0» (2026-03-12) y «Release 6.3.0» (2026-08-19) no estaban en `develop` del fork; se trajeron por SHA. Entre ellos hay 369 commits, 295 sin contar merges, y 557 ficheros cambiados (+26 582 / −7 520 líneas).
- **[leído]** Entradas de `CHANGELOG.md`:
  - 6.1.1: arreglo de cabeceras de CocoaPods.
  - 6.2.0: binding de Go, importación G-ABC, `keyAccid@oct` y opciones de neumas.
  - 6.3.0: `volta`/`refrain`, tamaños de fuente `pt`/`vu`, alteraciones turcas, API de editor, `ending@label`, armadura al reiniciar sección, `--show-hidden`, arreglo multihilo, página de elementos temporizados, superíndices de harmony, `getElementAttr` para `grpSym`/`keyAccid`, `--font-text-liberation`, empaquetado de Python y «Various improvements to the MusicXML importer».

### 1.1 Importación de MusicXML

**El arreglo de `<alter>` [leído]:**

| PR | Commits | Qué hace |
|---|---|---|
| rism-digital/verovio#4383 «Use `pitch/alter` for gestural accidentals» (merge 46a4df525, 2026-07-10, infojunkie) | d11c392fb, 2d0dea2d3, 4d76e16af | Lee `<pitch><alter>` como fuente de la alteración gestual. Recuerda la relación altura/alter → alteración escrita en `m_alterAccids`. Deja de emitir `@accid.ges` cuando coincide con `@accid`, y deja de poner `glyph.name` SMuFL en el caso normal. |
| rism-digital/verovio#4400 «Use pitch/alter to derive accid.ges» (merge 27db07fe8, 2026-08-17) | e59ec90d6, a761ed4bd | Elimina el arrastre de alteraciones por armadura y compás: se van `m_currentAccids`, `m_currentKeySig` y `ResetAccidentals()`. `@accid.ges` sale siempre de `<alter>`. Los becuadros gestuales sobran y no se emiten. El `accid` gestual se marca `IsAttribute(true)`, así que en el MEI sale como atributo de `<note>`. |
| rism-digital/verovio#4356 (merge 52fb952b5) | 7e02fe4ea | «Avoid generating empty accid» (#4340). |

**[leído]** El mecanismo del fallo en 6.1.0 (`src/iomusxml.cpp`, `ReadMusicXmlNote`):
- Si una nota no tiene `<accidental>`, se le crea un `<accid>` hijo con la alteración «vigente» de su nombre de nota. Esa alteración se reinicia a la armadura en cada compás (`ResetAccidentals(m_currentKeySig)`).
- No distingue octavas.
- No conoce las ligaduras que cruzan la barra.
- `<alter>` no se lee.
- La altura MIDI sale solo de `accid`/`accid.ges` de la nota (`Note::GetChromaticAlteration`), sin consultar la armadura. Por eso el error llega al MIDI y al cierre de ligaduras.

**Otros cambios del importador [leído]:**
- 92b03ade9 (rism-digital/verovio#4339): conserva el final de los extensores de letra creando `verse`/`syl` vacíos.
- 8300807c9 (#4347): `grace@slash` respeta el valor, no solo su presencia.
- 75df1a822 y 44c85a898 (#4382, #4373): respiraciones.
- 1f51c826a (#4396): los elementos de control se asignan al compás por posición, no por número (#3902).
- e2c687382 (#4411): tresillos ocultos.
- e2f797f22 (#4416): silencios en una sola pauta de TAB.
- 6d5d4f85a (#4426): notaciones de notas cross-staff.
- 8817c3033 (#4433): revierte el relleno con `<space>` de un `<forward>` final, que venía de 276a435b6 (2021).

### 1.2 Salida MEI

- **[leído]** 4383 y 4400 cambian cómo sale la alteración gestual: antes era un `<accid>` hijo con `accid.ges` y `glyph.*`; ahora es `note@accid.ges`.
- **[leído]** Nuevos escritores de MEI:
  - `WriteVolta`, `WriteRefrain` y `WriteLyricElement` (a09acec80, #4405).
  - `WriteEpisema` y `WriteStrophicus` (00e814110, G-ABC).
  - Clase `MEIOutputExtended::ExportScoreDef` para exportar el scoreDef en JSON (a92e89fc2 y 5bc5e1153).
- **[leído]** be44d3e0a: `getMEI` evita el cast-off mensural cuando no hace falta.
- **[leído]** Cambios en LibMEI:
  - Tipos `NOTATIONTYPE_neume_square` y `neume_hufnagel`.
  - Tamaños de fuente con unidad `pt`/`vu` (a8c54ca04).
  - Los conversores pasan de `atof`/`atoi` a `stof`/`stoi` (04cf3e934, #4326). Ver el riesgo R13.
- **[medido]** `meiversion` sigue siendo `6.0-dev` en las dos versiones.

### 1.3 Estructura del SVG (clases, ids, grupos)

- **[leído]** `svgdevicecontext.cpp`:
  - El CSS de `<style>` incluye siempre `g.cursor {…}` y `g.cursor.chord {…}` (cursor del editor, 2880a4f0a / 1ea6e2310).
  - Con `--show-hidden` se añade la clase `show-hidden` y una regla CSS extra (782e1931f, 140958178, #4367).
  - `MoveTextVerticallyTo` escribe `dy` relativo en lugar de `y` absoluto (975f7c28d, #4402), para superíndices y subíndices de harmony.
- **[leído]** Grupos nuevos en `view_*.cpp`:
  - `g.volta` y `voltaGroupingSym`.
  - `lyricElement` en lugar de `verse` en `DrawVerse` (#4405).
  - Grupos personalizados `bTremNum`, `mRptNum` y `multiRestNum` con `show-hidden`.
  - `g.cursor`, solo del editor.
- **[leído]** La fuente Leipzig se actualizó: b7b5510c1 (5.2.101) y db899e42a (alteraciones turcas).

### 1.4 `renderToTimemap`

- **[leído]** `src/timemap.cpp` no cambia en el rango.
- **[leído]** En `midifunctor.cpp` solo cambia lo de letra y volta: `VisitVolta`, `VisitRefrain` (a09acec80) y `Syl::IsEmpty` (8497ed330).
- **[leído]** `Toolkit::SetOptions` reinicia el documento MIDI al cambiar `midiTempoAdjustment` o `midiNoCue` (97b9a59a8, #4325).
- **[leído]** `GetElementsAtTime` busca la página a través del id notado cuando el documento MIDI es la expansión (da57e000e, #4434).

### 1.5 Opciones

- **[leído]** El diff de `src/options.cpp` entre los dos release solo registra opciones nuevas: `showHidden`, `gabcAquitanianContext`, `gabcExtendedSymbols`, `gabcStaffLines` y `liquescentWithoutTails`. No hay renombradas ni retiradas, y ningún `Init()` cambia de valor.
- **[medido]** `getDefaultOptions()` lo confirma: 5 claves nuevas en 6.3.0, ninguna desaparece y ningún valor por defecto cambia.
- **[leído]** API JS: `editInfo()` pasa a estar deprecada (escribe `console.warn` y llama a `editStatus()`). Aparecen `editStatus()` y `editResponse()` (ce1094f5e). En C++ se va `Toolkit::EditInfo()` y algunos miembros pasan a `protected` (03c2f786d).

### 1.6 Rendimiento

- **[leído]** Commits relacionados:
  - 8800ccd2b / c3a503db6 (#4352): `BoundingBox::IsAnyOf` usa `std::array` y evita crear un vector.
  - 5e8dc3db8 (#4420): `std::shared_mutex` en el `ObjectFactory`.
  - 1712ca6f8 (#4386): mapas `thread_local` en `customtuning`.
  - Los dos últimos son arreglos para entornos multihilo; el WASM del visor se ejecuta en un solo hilo.
- **[leído]** Hay otras causas probables de ir más rápido que no se han aislado. La más visible: el MEI interno tiene muchos menos objetos `accid` (ver 2.3).
- **[leído]** `emscripten/buildToolkit` solo cambia `SINGLE_FILE` en compilaciones de depuración; en release sigue igual.

## 2. Comparación medida

### 2.1 Montaje

- **Versiones [medido]:** paquetes npm `verovio@6.1.0` y `verovio@6.3.0` (WASM), Node v22.22.0, Linux, 4 vCPU Intel Xeon a 2,10 GHz, 16 GB.
- **Corpus [medido]:** 9 MusicXML públicos de la rueda PyPI `music21==10.5.2` (sha256 `dba8696e…`), más un caso sintético propio, `lab/casos/alter-sintetico.musicxml`.

| Fichero | Programa que lo exportó | Notas `<note>` |
|---|---|---:|
| `schubert/Lindenbaum.xml` | Sibelius 8.4.1 | 1812 |
| `demos/two-parts.xml` | Sibelius 7.1.3 | 36 |
| `demos/voices_with_chords.xml` | Sibelius 7.5.1 | 39 |
| `joplin/maple_leaf_rag.mxl` | MuseScore 2.1.0 | 1647 |
| `beethoven/opus18no1/movement3.mxl` | Finale | 1532 |
| `beach/prayer_of_a_tired_child.musicxml` | Finale v25 | 1102 |
| `schumann_robert/dichterliebe_no2.xml` | Finale 2011 | 278 |
| `mozart/k545/movement1_exposition.mxl` | Finale 2011 | 205 |
| `bach/bwv66.6.mxl` | Finale / Dolet 2006 | — |

- **Perfiles de opciones [leído en `lab/run.mjs`]:** son supuestos; no se conocen las opciones reales del visor.
  - `defecto`: sin opciones.
  - `visor-paginado`: escala 40, 2100×2970, `breaks:auto`, `adjustPageHeight`, sin cabecera ni pie.
  - `visor-continuo`: escala 35, `breaks:none`, `adjustPageWidth/Height`.
  - Los tres llevan `xmlIdSeed: 1`.
- **Procedimiento [leído en los scripts]:**
  - 4 pasadas alternas (6.1.0, 6.3.0, 6.3.0, 6.1.0), cada una en un proceso aparte, con 5 repeticiones por fichero y perfil. Son 10 tiempos por versión y caso.
  - Los artefactos (SVG, MEI, timemap, MIDI) son los de la primera repetición de la pasada «a».
- **Métrica de error de altura [leído en `lab/compare.py`]:**
  - Para cada compás (por índice), se compara el multiconjunto de alturas MIDI que da `getMIDIValuesForElement` con el que sale de `<step>`, `<alter>` y `<octave>` del MusicXML.
  - Cuenta las notas esperadas que no aparecen.

Los resultados completos están en `lab/resultados/RESULTADOS.md` y `lab/resultados/resultados.json`.

### 2.2 Alturas (el arreglo de `<alter>`) — perfil `defecto` [medido]

| Fichero | Notas | Errores 6.1.0 | Errores 6.3.0 |
|---|---:|---:|---:|
| alter-sintetico | 15 | 4 | 0 |
| schubert Lindenbaum (Sibelius) | 1668 | 50 | 0 |
| beethoven op.18/1 iii | 1289 | 26 | 0 |
| beach prayer | 1089 | 12 | 0 |
| joplin maple leaf | 1581 | 12 | 0 |
| schumann dichterliebe 2 | 254 | 1 | 0 |
| bach, mozart, two-parts, voices_with_chords | 165 / 191 / 32 / 37 | 0 | 0 |
| **Total** | **6321** | **105** | **0** |

- **[medido]** Caso sintético, alturas en orden de documento:
  - Esperado: `78 65 72 66 | 66 67 70 70 | 66 60 73 60 | 68 67 64`.
  - 6.1.0: `78 66 72 66 | 65 67 70 70 | 66 60 72 60 | 67 67 64`.
  - 6.3.0: idéntico al esperado.
- **[medido]** Los 4 fallos de 6.1.0 son exactamente los cuatro patrones del caso:
  - El sostenido de Fa5 se arrastra a Fa4.
  - La nota ligada sobre la barra pierde el sostenido.
  - El becuadro de Do4 se arrastra a Do5.
  - Un Sol#4 sin `<accidental>` sale como Sol natural.
- **[medido, visual]** Captura del caso sintético en Chromium: en 6.1.0 falta la ligadura Fa#4–Fa#4 entre los compases 1 y 2; en 6.3.0 aparece. Las alteraciones escritas se ven igual en las dos.
- **[medido]** Avisos «There are N ties left open» del importador (6.1.0 → 6.3.0):

| Fichero | 6.1.0 | 6.3.0 |
|---|---:|---:|
| sintético | 1 | 0 |
| Beach | 2 | 1 |
| Beethoven | 16 | 2 |
| Joplin | 5 | 0 |
| Lindenbaum | 2 | 0 |
| **Total** | **26** | **3** |

### 2.3 MEI — perfil `defecto` [medido]

- **[medido]** El MEI pesa entre un 20 % y un 38 % menos en todos los ficheros. Por ejemplo, Lindenbaum pasa de 659 258 a 460 564 bytes, y Joplin de 541 558 a 337 381.
- **[medido]** Desaparecen elementos `<accid>`: 1589 en Lindenbaum, 1432 en Joplin, 1090 en Beethoven, 1030 en Beach, 245 en Schumann, 189 en Mozart, 155 en Bach, 37 en voices_with_chords, 31 en two-parts y 11 en el sintético.
  - En `voices_with_chords`, los 37 `<accid>` de 6.1.0 solo tenían `xml:id`: estaban vacíos.
- **[medido]** Aparecen atributos `note@accid.ges`: 647 en Lindenbaum, 982 en Joplin, 433 en Beach, 163 en Beethoven…
- **[medido]** Se cierran más ligaduras (`tie@endid`): +14 en Beethoven, +5 en Joplin, +2 en Lindenbaum y +1 en Beach y en el sintético.
- **[medido]** Hay diferencias estructurales aparte de las alteraciones (diff ignorando ids y `accid`):
  - Beach: 53 `<verse><syl/></verse>` vacíos nuevos, en las notas donde acaba un extensor de letra (92b03ade9).
  - Schumann: 3 `<space>` menos, por la reversión del `<forward>` final (8817c3033).
  - Beethoven, Joplin y Lindenbaum: sin otras diferencias estructurales.
- **[medido]** Con `xmlIdSeed: 1` y el mismo fichero, los ids de nota casi nunca coinciden entre versiones (p. ej. 2 de 15 en el sintético, 13 de 1089 en Beach). La causa probable es que 6.1.0 consume ids en los `<accid>` extra. El detalle es de la otra sesión, la de ids.

### 2.4 SVG [medido]

**Grupos `g.accid` vacíos con id**, de 6.1.0 a 6.3.0:

| Fichero | 6.1.0 | 6.3.0 |
|---|---:|---:|
| Lindenbaum | 1589 | 647 |
| Joplin | 1432 | 982 |
| Beethoven | 1090 | 163 |
| Beach | 1030 | 433 |
| Mozart | 189 | 1 |
| voices_with_chords | 37 | 0 |

- **[medido]** El total de `<g>` y de elementos con id baja lo mismo, por ejemplo de 8337 a 7395 elementos con id en Lindenbaum (`defecto`).
- **[medido]** Clases que suben en 6.3.0 (perfil `defecto`): `tie` (+2 Lindenbaum, +4 Beethoven, +1 Joplin, +7 Beach), `spanning`, `slur` (+6 Beach), `hairpin` (+2 Beach) y `syl`/`verse` (+54/+53 Beach).
  - `path@stroke-linecap` y `stroke-linejoin` aparecen solo en el sintético de 6.3.0, porque son atributos de la ligadura que 6.1.0 no dibujaba.
- **[medido]** Reglas CSS de `<style>`:
  - 6.3.0 añade `g.cursor {fill:dodgerblue; color:dodgerblue;}` y `g.cursor.chord {fill:limegreen; color:limegreen;}`. Van con el prefijo `#<id-del-documento>`.
  - El `@font-face` de Leipzig incrustado pasa de 58 227 a 58 603 bytes.
- **[medido]** Posición de las cabezas de nota (`translate` del `<use>` en `g.notehead`, comparando nota a nota en el mismo orden):
  - Bach, Mozart, Schumann, two-parts, voices_with_chords, Joplin y Lindenbaum (todos los perfiles): 0 cabezas movidas.
  - Beethoven (`defecto` y `visor-paginado`): 111 de 1289 cabezas bajan 32 unidades SVG en la página 5 (sistemas 2 y 3). En `visor-continuo`, 0.
  - Beach (`visor-continuo`): 1054 de 1089 cabezas se mueven, con un |Δx| máximo de 2262 y un |Δy| máximo de 7.
  - Beach (`defecto` y `visor-paginado`): las 4 páginas cambian de número de cabezas, o sea que hay reflujo de compases entre sistemas y páginas.
  - En la captura de la página 1 (`visor-paginado`), el sistema 2 lleva los compases 5–8 en 6.1.0 y los 5–9 en 6.3.0.
- **[medido]** Tamaño de página distinto (`width`, `height` o `viewBox`):
  - Beach: 4 páginas en `visor-paginado` y 1 en `visor-continuo`.
  - Beethoven: 1 página en `visor-paginado`.
  - El número de páginas no cambia en ningún caso.

### 2.5 Timemap [medido]

- **[medido]** En los 30 casos (10 ficheros × 3 perfiles), el timemap por defecto y el de `includeMeasures + includeRests` son iguales salvo los ids. Para comprobarlo, cada id se sustituye por la posición de su nota en el MEI. Coinciden el número de entradas, `tstamp`, `qstamp`, `tempo` y las notas en `on`/`off`. Δt máximo: 0 ms.
- **[medido]** Los ids `on` del timemap que no existen en el SVG:
  - Beethoven: 1714 de 3003.
  - Joplin: 883 de 2464.
  - Son iguales en las dos versiones. Son copias de la expansión de repeticiones (p. ej. `n1u2rwal-rend2`).
  - Tras `getNotatedIdForElement`, faltan 0 en las dos versiones.
- **[medido]** `getElementsAtTime(t+1)` en cada instante `on`, comparado con la página real de la primera nota:

| Fichero (perfil `defecto`) | Páginas erróneas 6.1.0 | Páginas erróneas 6.3.0 | Instantes |
|---|---:|---:|---:|
| Lindenbaum | 657 | 0 | 779 |
| Beethoven | 947 | 0 | 1150 |
| Joplin | 612 | 0 | 899 |
| Beach | 160 | 0 | 224 |

  - En los ficheros de una sola página, ninguna de las dos versiones falla.
  - 6.1.0 devuelve página 1 en esos casos de varias páginas.

### 2.6 Tiempo de render [medido]

Mediana de 10 repeticiones por versión y caso, en ms, sumando los 30 casos:

| Fase | 6.1.0 | 6.3.0 | 6.3.0 / 6.1.0 |
|---|---:|---:|---:|
| `loadData` | 3480 | 2743 | 0,79 |
| `renderToSVG` (todas las páginas) | 3015 | 2461 | 0,82 |
| `renderToTimemap` | 3059 | 2234 | 0,73 |
| `getMEI` | 152 | 112 | 0,74 |
| carga + SVG | 6495 | 5204 | 0,80 |

- **[medido]** Por caso, el cociente carga+SVG va de 0,59 a 1,32. Solo hay uno por encima de 1: el sintético en `visor-continuo` (12 → 14 ms, un fichero diminuto donde el ruido domina).
  - Ejemplo: Lindenbaum `defecto`, carga 347 → 298 ms y SVG 211 → 194 ms.
- **[medido]** Arranque, en 5 procesos por versión: mediana total (import + `createVerovioModule` + toolkit) de 269 ms en 6.1.0 y 287 ms en 6.3.0 (rangos 246–295 y 266–330).
- **[medido]** Tamaño del paquete:
  - `dist/verovio-module.mjs`: 6 983 039 → 7 296 807 bytes (+4,5 %).
  - `verovio-toolkit-wasm.js`: 6 996 257 → 7 310 681 bytes.
  - `verovio-module-hum.mjs`: 11 585 952 → 12 374 836 bytes.
- **[medido]** Una pasada preliminar del mismo corpus, con una versión anterior de los scripts y 5 repeticiones por versión, dio un cociente total carga+SVG de 0,87. No se conserva en la rama. Indica el orden de variabilidad entre pasadas.

### 2.7 Robustez ante MEI inválido [medido]

- **[medido]** `lab/casos/tstamp-no-numerico.mei` (`<dynam tstamp="abc">`): 6.1.0 carga y dibuja (`ok:1`); 6.3.0 lanza `WebAssembly.Exception` desde `loadData`.
- **[medido]** Con `note@dur.ppq="x"`, prueba hecha a mano en la sesión pero no guardada como caso: mismo resultado.
- **[leído]** `Att::StrToDbl` y `StrToInt` usan `stof`/`stoi` desde 04cf3e934. En `develop`, a 2026-10-29, sigue igual.

## 3. Riesgos para un visor que resalta notas por id, usa el timemap y aplica escala y layouts propios

| # | Riesgo | Evidencia | Impacto en el visor | Gravedad | Qué hacer |
|---|---|---|---|---|---|
| R1 | Cambian alturas MIDI y `accid.ges` (es el arreglo buscado) | [medido] 105 notas corregidas en 6321 | Cualquier lógica que lea la altura (nombres de nota, colores por altura, audio propio) da otros valores, ahora correctos | Positivo / bajo | Revisar las pruebas que tengan alturas «esperadas» sacadas de 6.1.0 |
| R2 | Ligaduras nuevas en el SVG (`g.tie` con id) y cambios de forma en las ya dibujadas | [medido] tie +1…+7 por fichero; 26 → 3 ligaduras abiertas | CSS o resaltado que cuente `g.tie`; aparecen arcos que antes no estaban | Bajo | Ninguna, salvo pruebas visuales de referencia (snapshots) |
| R3 | Desaparecen muchos `g.accid` vacíos con id | [medido] p. ej. 1589 → 647 (Lindenbaum) | Si el visor selecciona, cuenta o guarda ids de `g.accid`, o recorre hijos de `g.note` por índice, le salen distintos | Medio si se usan; nulo si solo se usa `g.note` | Seleccionar por clase (`g.note`, `g.notehead`), no por índice de hijo; no persistir ids de `accid` |
| R4 | `getMEI()`: alteración gestual en `note@accid.ges`, no en `<accid>` hijo; MEI de 20–38 % menos | [medido] | Un parser propio del MEI que busque `accid/@accid.ges` deja de encontrarla | Medio si se parsea el MEI | Leer `@accid.ges` en `note` y en `accid` |
| R5 | Reflujo de maquetación en partituras con letra (extensores) y algún desplazamiento vertical | [medido] Beach: cambia el reparto de compases y la anchura en continuo (|Δx| hasta 2262); Beethoven: 32 unidades en la página 5 | Rompe posiciones guardadas, offsets de scroll, mapas nota→página o nota→coordenada precalculados con 6.1.0 y miniaturas cacheadas | Medio | Recalcular en tiempo de ejecución con `getPageWithElement` y el bbox del SVG; invalidar las cachés al cambiar de versión |
| R6 | Tamaño de página distinto con `adjustPageHeight` / `adjustPageWidth` | [medido] Beach 4 páginas, Beethoven 1 | La escala propia basada en `width`/`height`/`viewBox` del SVG da otro tamaño | Bajo-medio | Leer el tamaño de cada SVG, no fijarlo por partitura |
| R7 | Timemap | [medido] igual salvo ids en 30 de 30 casos | Sin impacto en tiempos ni en agrupación | Bajo | Nada (los ids son cosa de la otra sesión) |
| R8 | Ids del timemap en repeticiones (`…-rend2`) que no están en el SVG | [medido] 1714 de 3003 (Beethoven), 883 de 2464 (Joplin), **igual en las dos versiones** | Si el visor resalta con el id tal cual, falla en los pasajes repetidos (ya pasaba con 6.1.0) | Medio, pero no es nuevo | `getNotatedIdForElement(id)` antes de buscar en el SVG (con eso, 0 ausentes) |
| R9 | `getElementsAtTime` devuelve ahora la página correcta | [medido] 6.1.0 se equivocaba en 160–947 instantes por fichero de varias páginas; 6.3.0 en 0 | Si el visor compensaba el fallo (p. ej. ignoraba `page` o la recalculaba), revisar que no se duplique la corrección | Bajo (mejora) | Quitar los parches y usar `page` |
| R10 | CSS incrustado: reglas `g.cursor` nuevas y fuente Leipzig distinta | [medido] | Colisión si el visor usa la clase `cursor` en el SVG; cambia el aspecto de los glifos de texto SMuFL | Bajo | No usar `.cursor` dentro del SVG o subir la especificidad |
| R11 | Texto de harmony con `dy` relativo | [leído] 975f7c28d | Afecta si el visor recoloca o lee la `y` de los `tspan` | Bajo | SIN MEDIR (el corpus no lo ejercita) |
| R12 | Opciones | [medido] ninguna renombrada ni retirada, defaults iguales, 5 nuevas | Ninguno | Muy bajo | Nada |
| R13 | Excepción WASM ante MEI con números no válidos | [medido] `@tstamp="abc"`, `@dur.ppq="x"` | Si el visor carga MEI de terceros sin `try/catch`, la carga revienta en lugar de devolver `false`; no se sabe en qué estado queda el toolkit | Medio si se carga MEI externo; bajo con solo MusicXML | `try/catch` en `loadData` y recrear el toolkit tras una excepción |
| R14 | API JS de editor: `editInfo()` deprecada | [leído] | Solo `console.warn` si se usa | Muy bajo | Usar `editStatus()` |
| R15 | Rendimiento | [medido] carga+SVG ×0,80, timemap ×0,73; arranque +18 ms (mediana); módulo +4,5 % | Mejor en uso; primera carga algo más pesada | Bajo | Nada; medir en navegador (SIN MEDIR) |
| R16 | `<forward>` final ya no rellena con `<space>` | [medido] −3 `space` en Schumann; [leído] 8817c3033 | Posibles diferencias de espaciado en voces que acaban con `<forward>` | Bajo | Incluir en las pruebas visuales |
| R17 | Licencia: el paquete npm no trae `COPYING*`; identificador `or-later` en npm y `only` en el repo actual | [medido] / [leído] | Obligaciones de aviso y copia de la LGPL §4 al distribuir el visor | Administrativo | Incluir los textos de la licencia y el aviso en el visor |

## 4. Cómo reproducir

Desde la raíz del repositorio, con Node ≥ 22, Python 3, `pip`, `unzip` y acceso a npm y PyPI:

```bash
lab/run-all.sh /tmp/lab-verovio
```

Lo hace todo: `setup.sh` instala los dos paquetes npm; `fetch-corpus.sh` descarga music21 10.5.2 y comprueba su sha256; `run.mjs` hace las 4 pasadas; `init-time.mjs` mide el arranque; `load-one.mjs` prueba los casos MEI; `compare.py` escribe `lab/resultados/`. Comandos ejecutados en esta sesión (dir. de trabajo en el scratchpad):

```bash
lab/fetch-corpus.sh "$W" "$W/corpus"
lab/setup.sh "$W"
node lab/run.mjs "$W/v610" "$W/corpus" "$W/out610-a" 5   # y out630-a, out630-b, out610-b
node lab/init-time.mjs "$W/v610"                       # ×5 por versión
node lab/load-one.mjs "$W/v630" lab/casos/tstamp-no-numerico.mei
python3 -I lab/compare.py "$W/corpus" lab/resultados "$W/out610-a" "$W/out630-a" "$W/out610-b" "$W/out630-b"
```

Las capturas visuales se hicieron con Playwright y Chromium a partir de los SVG; ni ese script ni las imágenes están en la rama.

## SIN MEDIR

- Las opciones, la escala y el layout reales del visor: los tres perfiles son supuestos.
- El comportamiento y el tiempo en navegadores. Todo se midió en Node 22, en una sola máquina virtual de 4 vCPU.
- El consumo de memoria.
- Los ids de nota, que estudia otra sesión. Aquí solo se anota que, con la misma semilla, no coinciden entre versiones.
- Exportaciones de versiones actuales de Sibelius (Ultimate 202x). Los ficheros de Sibelius del corpus son de las versiones 7.1.3, 7.5.1 y 8.4.1. El caso sintético está escrito a mano; no es una exportación de Sibelius.
- Las causas exactas del reflujo de Beach y del desplazamiento de 32 unidades de Beethoven. Se sospecha de 92b03ade9 (extensores de letra) y de las ligaduras nuevas, pero no se ha aislado.
- El efecto del `dy` relativo en el texto de harmony (R11).
- `volta`/`refrain`, `--show-hidden`, tamaños de fuente `pt`/`vu`, alteraciones turcas, G-ABC y el editor.
- `renderToMIDI` byte a byte. Solo se comparó la altura por nota con `getMIDIValuesForElement`.
- El módulo con Humdrum (`verovio-module-hum.mjs`).
- La versión 6.2.0 por separado.
- Si la excepción de `stof`/`stoi` puede saltar con entrada MusicXML, y el estado del toolkit después de una excepción.
- `getElementsAtTime` en instantes que no sean el inicio de una nota (+1 ms).
- La inspección visual se limitó a 2 páginas: el caso sintético y la página 1 de Beach en `visor-paginado`. Del resto solo hay métricas automáticas.
