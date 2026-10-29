# Resultados medidos: 6.1.0-682d606 (A) frente a 6.3.0-425dd7b (B)

Repeticiones de tiempo por caso: A=10, B=10. Generado por `lab/compare.py`.

## Opciones (getDefaultOptions)
- Solo en A: ninguna
- Solo en B: ['gabcAquitanianContext', 'gabcExtendedSymbols', 'gabcStaffLines', 'liquescentWithoutTails', 'showHidden']
- Valor por defecto distinto: ninguno

## Alturas MIDI frente a `<pitch>` de MusicXML (perfil defecto)
| fichero | notas esperadas | notas MEI A → B | errores A | errores B | notas con altura distinta A/B |
|---|---:|---:|---:|---:|---:|
| alter-sintetico.musicxml | 15 | 15 → 15 | 4 | 0 | 4 |
| bach--bwv66.6.mxl | 165 | 165 → 165 | 0 | 0 | 0 |
| beach--prayer_of_a_tired_child.musicxml | 1089 | 1089 → 1089 | 12 | 0 | 12 |
| beethoven--opus18no1--movement3.mxl | 1289 | 1289 → 1289 | 26 | 0 | 26 |
| demos--two-parts.xml | 32 | 32 → 32 | 0 | 0 | 0 |
| demos--voices_with_chords.xml | 37 | 37 → 37 | 0 | 0 | 0 |
| joplin--maple_leaf_rag.mxl | 1581 | 1581 → 1581 | 12 | 0 | 12 |
| mozart--k545--movement1_exposition.mxl | 191 | 191 → 191 | 0 | 0 | 0 |
| schubert--Lindenbaum.xml | 1668 | 1668 → 1668 | 50 | 0 | 50 |
| schumann_robert--dichterliebe_no2.xml | 254 | 254 → 254 | 1 | 0 | 1 |

## MEI (perfil defecto)
| fichero | bytes A → B | meiversion | líneas cambiadas (ids normalizados) | elementos (B−A) | atributos (B−A) |
|---|---:|---|---:|---|---|
| alter-sintetico.musicxml | 6560 → 5219 | 6.0-dev → 6.0-dev | 45 | accid -11 | accid@accid.ges -9, accid@glyph.auth -5, accid@glyph.name -5, accid@id -11, note@accid.ges +5, tie@endid +1 |
| bach--bwv66.6.mxl | 55553 → 36427 | 6.0-dev → 6.0-dev | 483 | accid -155 | accid@accid.ges -87, accid@glyph.auth -77, accid@glyph.name -77, accid@id -155, note@accid.ges +77 |
| beach--prayer_of_a_tired_child.musicxml | 415671 → 314366 | 6.0-dev → 6.0-dev | 2720 | accid -1030, syl +53, verse +53 | accid@accid.ges -500, accid@glyph.auth -441, accid@glyph.name -441, accid@id -1030, note@accid.ges +433, syl@id +53, tie@endid +1, verse@id +53, verse@n +53 |
| beethoven--opus18no1--movement3.mxl | 510224 → 407086 | 6.0-dev → 6.0-dev | 2844 | accid -1090 | accid@accid.ges -346, accid@glyph.auth -147, accid@glyph.name -147, accid@id -1090, note@accid.ges +163, tie@endid +14 |
| demos--two-parts.xml | 14289 → 10870 | 6.0-dev → 6.0-dev | 94 | accid -31 | accid@accid.ges -6, accid@glyph.auth -5, accid@glyph.name -5, accid@id -31, note@accid.ges +5 |
| demos--voices_with_chords.xml | 12397 → 8736 | 6.0-dev → 6.0-dev | 112 | accid -37 | accid@id -37 |
| joplin--maple_leaf_rag.mxl | 541558 → 337381 | 6.0-dev → 6.0-dev | 4562 | accid -1432 | accid@accid.ges -1171, accid@glyph.auth -1022, accid@glyph.name -1022, accid@id -1432, note@accid.ges +982, tie@endid +5 |
| mozart--k545--movement1_exposition.mxl | 55126 → 35801 | 6.0-dev → 6.0-dev | 574 | accid -189 | accid@accid.ges -3, accid@glyph.auth -1, accid@glyph.name -1, accid@id -189, note@accid.ges +1 |
| schubert--Lindenbaum.xml | 659258 → 460564 | 6.0-dev → 6.0-dev | 4611 | accid -1589 | accid@accid.ges -821, accid@glyph.auth -742, accid@glyph.name -742, accid@id -1589, note@accid.ges +647, tie@endid +2 |
| schumann_robert--dichterliebe_no2.xml | 105032 → 77088 | 6.0-dev → 6.0-dev | 661 | accid -245, space -3 | accid@accid.ges -111, accid@glyph.auth -102, accid@glyph.name -102, accid@id -245, note@accid.ges +96, space@dur -3, space@dur.ppq -3, space@id -3 |

## SVG
| fichero | perfil | páginas A → B | bytes A → B | `<g>` A → B | elementos con id A → B | `g.accid` vacíos A → B | páginas con tamaño distinto | páginas con estructura idéntica (sin / con `g.accid` vacíos) | elementos estructurales distintos | páginas con nº de cabezas distinto | cabezas comparadas / movidas | máx \|Δx\|, \|Δy\| | clases (B−A) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| alter-sintetico.musicxml | defecto | 1 → 1 | 36494 → 36454 | 109 → 103 | 94 → 88 | 11 → 5 | 0 | 0 / 0 | 1 | 0 | 15 / 0 | 0, 0 | accid -6 |
| alter-sintetico.musicxml | visor-paginado | 1 → 1 | 17085 → 17048 | 103 → 97 | 88 → 82 | 11 → 5 | 0 | 0 / 0 | 1 | 0 | 15 / 0 | 0, 0 | accid -6 |
| alter-sintetico.musicxml | visor-continuo | 1 → 1 | 17086 → 17049 | 103 → 97 | 88 → 82 | 11 → 5 | 0 | 0 / 0 | 1 | 0 | 15 / 0 | 0, 0 | accid -6 |
| bach--bwv66.6.mxl | defecto | 1 → 1 | 156574 → 152110 | 896 → 818 | 723 → 645 | 155 → 77 | 0 | 1 / 0 | 0 | 0 | 165 / 0 | 0, 0 | accid -78 |
| bach--bwv66.6.mxl | visor-paginado | 1 → 1 | 137702 → 133233 | 890 → 812 | 720 → 642 | 155 → 77 | 0 | 1 / 0 | 0 | 0 | 165 / 0 | 0, 0 | accid -78 |
| bach--bwv66.6.mxl | visor-continuo | 1 → 1 | 132140 → 127682 | 863 → 785 | 688 → 610 | 155 → 77 | 0 | 1 / 0 | 0 | 0 | 165 / 0 | 0, 0 | accid -78 |
| beach--prayer_of_a_tired_child.musicxml | defecto | 4 → 4 | 1196348 → 1178326 | 6440 → 5962 | 5665 → 5171 | 1030 → 433 | 0 | 0 / 0 | 5989 | 4 | 0 / 0 | 0, 0 | accid -597, hairpin +2, slur +6, spanning +16, syl +54, tie +7, verse +53 |
| beach--prayer_of_a_tired_child.musicxml | visor-paginado | 4 → 4 | 1117887 → 1099847 | 6419 → 5941 | 5640 → 5146 | 1030 → 433 | 4 | 0 / 0 | 5989 | 4 | 0 / 0 | 0, 0 | accid -597, hairpin +2, slur +6, spanning +16, syl +54, tie +7, verse +53 |
| beach--prayer_of_a_tired_child.musicxml | visor-continuo | 1 → 1 | 1061229 → 1039488 | 6159 → 5668 | 5392 → 4901 | 1030 → 433 | 1 | 0 / 0 | 168 | 0 | 1089 / 1054 | 2262, 7 | accid -597, syl +53, verse +53 |
| beethoven--opus18no1--movement3.mxl | defecto | 7 → 7 | 1621437 → 1571981 | 8734 → 7811 | 7327 → 6400 | 1090 → 163 | 0 | 3 / 0 | 24 | 0 | 1289 / 111 | 0, 32 | accid -927, peicadq -1, spanning +4, tie +4, xqalbhe +1 |
| beethoven--opus18no1--movement3.mxl | visor-paginado | 7 → 7 | 1483630 → 1434160 | 8692 → 7769 | 7273 → 6346 | 1090 → 163 | 1 | 3 / 0 | 24 | 0 | 1289 / 111 | 0, 32 | accid -927, peicadq -1, spanning +4, tie +4, xqalbhe +1 |
| beethoven--opus18no1--movement3.mxl | visor-continuo | 1 → 1 | 1360161 → 1309080 | 8193 → 7266 | 6692 → 5765 | 1090 → 163 | 0 | 0 / 0 | 14 | 0 | 1289 / 0 | 0, 0 | accid -927 |
| demos--two-parts.xml | defecto | 1 → 1 | 92970 → 91895 | 192 → 166 | 166 → 140 | 31 → 5 | 0 | 1 / 0 | 0 | 0 | 32 / 0 | 0, 0 | accid -26 |
| demos--two-parts.xml | visor-paginado | 1 → 1 | 92531 → 91456 | 191 → 165 | 163 → 137 | 31 → 5 | 0 | 1 / 0 | 0 | 0 | 32 / 0 | 0, 0 | accid -26 |
| demos--two-parts.xml | visor-continuo | 1 → 1 | 92532 → 91456 | 191 → 165 | 163 → 137 | 31 → 5 | 0 | 1 / 0 | 0 | 0 | 32 / 0 | 0, 0 | accid -26 |
| demos--voices_with_chords.xml | defecto | 1 → 1 | 46409 → 44349 | 196 → 159 | 155 → 118 | 37 → 0 | 0 | 1 / 0 | 0 | 0 | 37 / 0 | 0, 0 | accid -37 |
| demos--voices_with_chords.xml | visor-paginado | 1 → 1 | 27005 → 24949 | 190 → 153 | 149 → 112 | 37 → 0 | 0 | 1 / 0 | 0 | 0 | 37 / 0 | 0, 0 | accid -37 |
| demos--voices_with_chords.xml | visor-continuo | 1 → 1 | 27003 → 24947 | 190 → 153 | 149 → 112 | 37 → 0 | 0 | 1 / 0 | 0 | 0 | 37 / 0 | 0, 0 | accid -37 |
| joplin--maple_leaf_rag.mxl | defecto | 3 → 3 | 1335823 → 1309856 | 7694 → 7245 | 5987 → 5537 | 1432 → 982 | 0 | 0 / 0 | 7 | 0 | 1581 / 0 | 0, 0 | accid -450, spanning +1, tie +1 |
| joplin--maple_leaf_rag.mxl | visor-paginado | 3 → 3 | 1278852 → 1252861 | 7678 → 7229 | 5976 → 5526 | 1432 → 982 | 0 | 0 / 0 | 7 | 0 | 1581 / 0 | 0, 0 | accid -450, spanning +1, tie +1 |
| joplin--maple_leaf_rag.mxl | visor-continuo | 1 → 1 | 1166825 → 1139997 | 7431 → 6981 | 5710 → 5260 | 1432 → 982 | 0 | 0 / 0 | 5 | 0 | 1581 / 0 | 0, 0 | accid -450 |
| mozart--k545--movement1_exposition.mxl | defecto | 1 → 1 | 165712 → 154513 | 967 → 779 | 767 → 579 | 189 → 1 | 0 | 1 / 0 | 0 | 0 | 191 / 0 | 0, 0 | accid -188 |
| mozart--k545--movement1_exposition.mxl | visor-paginado | 1 → 1 | 146836 → 135638 | 961 → 773 | 764 → 576 | 189 → 1 | 0 | 1 / 0 | 0 | 0 | 191 / 0 | 0, 0 | accid -188 |
| mozart--k545--movement1_exposition.mxl | visor-continuo | 1 → 1 | 142147 → 130951 | 939 → 751 | 739 → 551 | 189 → 1 | 0 | 1 / 0 | 0 | 0 | 191 / 0 | 0, 0 | accid -188 |
| schubert--Lindenbaum.xml | defecto | 6 → 6 | 1686828 → 1630088 | 9875 → 8935 | 8337 → 7395 | 1589 → 647 | 0 | 5 / 0 | 6 | 0 | 1668 / 0 | 0, 0 | accid -942, spanning +2, tie +2 |
| schubert--Lindenbaum.xml | visor-paginado | 6 → 6 | 1681493 → 1624741 | 9869 → 8929 | 8303 → 7361 | 1589 → 647 | 0 | 5 / 0 | 6 | 0 | 1668 / 0 | 0, 0 | accid -942, spanning +2, tie +2 |
| schubert--Lindenbaum.xml | visor-continuo | 1 → 1 | 1542584 → 1484843 | 9299 → 8357 | 7670 → 6728 | 1589 → 647 | 0 | 0 / 0 | 2 | 0 | 1668 / 0 | 0, 0 | accid -942 |
| schumann_robert--dichterliebe_no2.xml | defecto | 1 → 1 | 292840 → 283807 | 1631 → 1479 | 1425 → 1273 | 245 → 96 | 0 | 0 / 0 | 3 | 0 | 254 / 0 | 0, 0 | accid -149, space -3 |
| schumann_robert--dichterliebe_no2.xml | visor-paginado | 1 → 1 | 272744 → 263715 | 1625 → 1473 | 1416 → 1264 | 245 → 96 | 0 | 0 / 0 | 3 | 0 | 254 / 0 | 0, 0 | accid -149, space -3 |
| schumann_robert--dichterliebe_no2.xml | visor-continuo | 1 → 1 | 265546 → 256522 | 1588 → 1436 | 1378 → 1226 | 245 → 96 | 0 | 0 / 0 | 3 | 0 | 254 / 0 | 0, 0 | accid -149, space -3 |

- Reglas CSS de `<style>` solo en A: ['@font-face Leipzig (58227 bytes, sha1 336df8431d)']
- Reglas CSS de `<style>` solo en B: ['@font-face Leipzig (58603 bytes, sha1 8c074c64a3)', 'g.cursor {fill:dodgerblue; color:dodgerblue;}', 'g.cursor.chord {fill:limegreen; color:limegreen;}']
- Atributos (elemento@atributo) presentes solo en una versión, suma B−A: {'path@stroke-linejoin': 3, 'path@stroke-linecap': 3}

## Timemap
| fichero | perfil | entradas A → B | fin (ms) A → B | igual salvo ids | entradas distintas | máx Δt absoluto (ms) | con measures+rests: igual salvo ids | getElementsAtTime página errónea A / B (de n) | ids `on` ausentes del SVG A / B (de n) | … tras getNotatedIdForElement A / B |
|---|---|---:|---:|---|---:|---:|---|---:|---:|---:|
| alter-sintetico.musicxml | defecto | 17 → 17 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 15) | 0 / 0 |
| alter-sintetico.musicxml | visor-paginado | 17 → 17 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 15) | 0 / 0 |
| alter-sintetico.musicxml | visor-continuo | 17 → 17 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 15) | 0 / 0 |
| bach--bwv66.6.mxl | defecto | 52 → 52 | 22500 → 22500 | sí | 0 | 0 | sí | 0 / 0 (de 51) | 0 / 0 (de 165) | 0 / 0 |
| bach--bwv66.6.mxl | visor-paginado | 52 → 52 | 22500 → 22500 | sí | 0 | 0 | sí | 0 / 0 (de 51) | 0 / 0 (de 165) | 0 / 0 |
| bach--bwv66.6.mxl | visor-continuo | 52 → 52 | 22500 → 22500 | sí | 0 | 0 | sí | 0 / 0 (de 51) | 0 / 0 (de 165) | 0 / 0 |
| beach--prayer_of_a_tired_child.musicxml | defecto | 225 → 225 | 62000 → 62000 | sí | 0 | 0 | sí | 160 / 0 (de 224) | 0 / 0 (de 1089) | 0 / 0 |
| beach--prayer_of_a_tired_child.musicxml | visor-paginado | 225 → 225 | 62000 → 62000 | sí | 0 | 0 | sí | 160 / 0 (de 224) | 0 / 0 (de 1089) | 0 / 0 |
| beach--prayer_of_a_tired_child.musicxml | visor-continuo | 225 → 225 | 62000 → 62000 | sí | 0 | 0 | sí | 0 / 0 (de 224) | 0 / 0 (de 1089) | 0 / 0 |
| beethoven--opus18no1--movement3.mxl | defecto | 1227 → 1227 | 511500 → 511500 | sí | 0 | 0 | sí | 947 / 0 (de 1150) | 1714 / 1714 (de 3003) | 0 / 0 |
| beethoven--opus18no1--movement3.mxl | visor-paginado | 1227 → 1227 | 511500 → 511500 | sí | 0 | 0 | sí | 947 / 0 (de 1150) | 1714 / 1714 (de 3003) | 0 / 0 |
| beethoven--opus18no1--movement3.mxl | visor-continuo | 1227 → 1227 | 511500 → 511500 | sí | 0 | 0 | sí | 0 / 0 (de 1150) | 1714 / 1714 (de 3003) | 0 / 0 |
| demos--two-parts.xml | defecto | 19 → 19 | 13171 → 13171 | sí | 0 | 0 | sí | 0 / 0 (de 18) | 0 / 0 (de 32) | 0 / 0 |
| demos--two-parts.xml | visor-paginado | 19 → 19 | 13171 → 13171 | sí | 0 | 0 | sí | 0 / 0 (de 18) | 0 / 0 (de 32) | 0 / 0 |
| demos--two-parts.xml | visor-continuo | 19 → 19 | 13171 → 13171 | sí | 0 | 0 | sí | 0 / 0 (de 18) | 0 / 0 (de 32) | 0 / 0 |
| demos--voices_with_chords.xml | defecto | 16 → 16 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 37) | 0 / 0 |
| demos--voices_with_chords.xml | visor-paginado | 16 → 16 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 37) | 0 / 0 |
| demos--voices_with_chords.xml | visor-continuo | 16 → 16 | 8000 → 8000 | sí | 0 | 0 | sí | 0 / 0 (de 15) | 0 / 0 (de 37) | 0 / 0 |
| joplin--maple_leaf_rag.mxl | defecto | 905 → 905 | 155100 → 155100 | sí | 0 | 0 | sí | 612 / 0 (de 899) | 883 / 883 (de 2464) | 0 / 0 |
| joplin--maple_leaf_rag.mxl | visor-paginado | 905 → 905 | 155100 → 155100 | sí | 0 | 0 | sí | 544 / 0 (de 899) | 883 / 883 (de 2464) | 0 / 0 |
| joplin--maple_leaf_rag.mxl | visor-continuo | 905 → 905 | 155100 → 155100 | sí | 0 | 0 | sí | 0 / 0 (de 899) | 883 / 883 (de 2464) | 0 / 0 |
| mozart--k545--movement1_exposition.mxl | defecto | 146 → 146 | 21818 → 21818 | sí | 0 | 0 | sí | 0 / 0 (de 144) | 0 / 0 (de 191) | 0 / 0 |
| mozart--k545--movement1_exposition.mxl | visor-paginado | 146 → 146 | 21818 → 21818 | sí | 0 | 0 | sí | 0 / 0 (de 144) | 0 / 0 (de 191) | 0 / 0 |
| mozart--k545--movement1_exposition.mxl | visor-continuo | 146 → 146 | 21818 → 21818 | sí | 0 | 0 | sí | 0 / 0 (de 144) | 0 / 0 (de 191) | 0 / 0 |
| schubert--Lindenbaum.xml | defecto | 814 → 814 | 133000 → 133000 | sí | 0 | 0 | sí | 657 / 0 (de 779) | 0 / 0 (de 1668) | 0 / 0 |
| schubert--Lindenbaum.xml | visor-paginado | 814 → 814 | 133000 → 133000 | sí | 0 | 0 | sí | 657 / 0 (de 779) | 0 / 0 (de 1668) | 0 / 0 |
| schubert--Lindenbaum.xml | visor-continuo | 814 → 814 | 133000 → 133000 | sí | 0 | 0 | sí | 0 / 0 (de 779) | 0 / 0 (de 1668) | 0 / 0 |
| schumann_robert--dichterliebe_no2.xml | defecto | 83 → 83 | 40500 → 40500 | sí | 0 | 0 | sí | 0 / 0 (de 73) | 0 / 0 (de 254) | 0 / 0 |
| schumann_robert--dichterliebe_no2.xml | visor-paginado | 83 → 83 | 40500 → 40500 | sí | 0 | 0 | sí | 0 / 0 (de 73) | 0 / 0 (de 254) | 0 / 0 |
| schumann_robert--dichterliebe_no2.xml | visor-continuo | 83 → 83 | 40500 → 40500 | sí | 0 | 0 | sí | 0 / 0 (de 73) | 0 / 0 (de 254) | 0 / 0 |

## Tiempos (mediana en ms; entre paréntesis mín–máx)
| fichero | perfil | carga A | carga B | SVG A | SVG B | timemap A | timemap B | MEI A | MEI B | carga+SVG B/A |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| alter-sintetico.musicxml | defecto | 30 (20–89) | 27 (21–71) | 6 (4–12) | 4 (4–11) | 22 (13–41) | 18 (14–38) | 0 (0–1) | 0 (0–1) | 0.87 |
| alter-sintetico.musicxml | visor-paginado | 28 (20–33) | 21 (20–43) | 5 (4–6) | 4 (3–8) | 18 (13–23) | 13 (13–28) | 0 (0–0) | 0 (0–1) | 0.74 |
| alter-sintetico.musicxml | visor-continuo | 7 (6–11) | 9 (6–15) | 4 (3–6) | 5 (3–8) | 14 (12–23) | 20 (13–29) | 0 (0–0) | 0 (0–0) | 1.32 |
| bach--bwv66.6.mxl | defecto | 56 (39–94) | 52 (35–81) | 24 (17–46) | 22 (15–35) | 30 (22–68) | 29 (21–45) | 1 (1–4) | 1 (1–2) | 0.93 |
| bach--bwv66.6.mxl | visor-paginado | 54 (36–98) | 48 (35–67) | 26 (16–42) | 20 (14–37) | 33 (21–49) | 25 (20–42) | 2 (1–2) | 1 (1–2) | 0.85 |
| bach--bwv66.6.mxl | visor-continuo | 15 (11–29) | 15 (11–19) | 21 (15–42) | 20 (15–28) | 27 (21–51) | 28 (20–33) | 2 (1–4) | 1 (1–2) | 0.96 |
| beach--prayer_of_a_tired_child.musicxml | defecto | 316 (211–477) | 186 (174–293) | 233 (153–415) | 140 (137–198) | 175 (113–270) | 113 (93–203) | 12 (8–24) | 7 (7–17) | 0.59 |
| beach--prayer_of_a_tired_child.musicxml | visor-paginado | 256 (197–297) | 175 (168–256) | 157 (142–241) | 140 (128–162) | 115 (108–181) | 94 (91–115) | 8 (8–14) | 7 (6–8) | 0.76 |
| beach--prayer_of_a_tired_child.musicxml | visor-continuo | 70 (65–105) | 61 (57–98) | 200 (180–291) | 166 (161–257) | 119 (110–179) | 94 (90–155) | 8 (8–13) | 7 (6–11) | 0.84 |
| beethoven--opus18no1--movement3.mxl | defecto | 364 (309–474) | 267 (254–373) | 231 (189–333) | 168 (160–207) | 349 (283–470) | 232 (222–313) | 10 (9–16) | 8 (8–8) | 0.73 |
| beethoven--opus18no1--movement3.mxl | visor-paginado | 342 (297–472) | 278 (255–304) | 230 (187–290) | 172 (163–210) | 338 (290–460) | 242 (223–314) | 10 (9–16) | 8 (8–13) | 0.79 |
| beethoven--opus18no1--movement3.mxl | visor-continuo | 118 (101–172) | 89 (84–127) | 356 (307–481) | 327 (272–380) | 368 (287–451) | 235 (220–359) | 14 (9–16) | 8 (8–13) | 0.88 |
| demos--two-parts.xml | defecto | 26 (19–34) | 20 (18–32) | 7 (6–11) | 6 (6–15) | 13 (13–22) | 13 (12–16) | 0 (0–1) | 0 (0–0) | 0.78 |
| demos--two-parts.xml | visor-paginado | 20 (19–32) | 20 (19–32) | 7 (6–11) | 6 (6–10) | 13 (13–23) | 14 (12–22) | 0 (0–1) | 0 (0–0) | 0.98 |
| demos--two-parts.xml | visor-continuo | 7 (6–10) | 6 (6–9) | 7 (6–11) | 6 (6–9) | 14 (13–23) | 13 (12–21) | 0 (0–1) | 0 (0–0) | 0.90 |
| demos--voices_with_chords.xml | defecto | 20 (18–28) | 18 (17–25) | 5 (4–6) | 4 (4–8) | 13 (12–15) | 12 (11–16) | 0 (0–0) | 0 (0–0) | 0.89 |
| demos--voices_with_chords.xml | visor-paginado | 20 (17–29) | 17 (16–19) | 4 (4–8) | 4 (4–4) | 13 (12–20) | 12 (11–13) | 0 (0–0) | 0 (0–2) | 0.84 |
| demos--voices_with_chords.xml | visor-continuo | 6 (5–6) | 5 (5–5) | 4 (4–5) | 4 (3–4) | 13 (12–15) | 11 (11–12) | 0 (0–0) | 0 (0–0) | 0.88 |
| joplin--maple_leaf_rag.mxl | defecto | 239 (221–297) | 212 (192–288) | 146 (139–203) | 134 (121–193) | 211 (183–284) | 159 (144–204) | 11 (9–16) | 8 (7–12) | 0.90 |
| joplin--maple_leaf_rag.mxl | visor-paginado | 260 (217–337) | 205 (194–323) | 151 (140–211) | 128 (120–155) | 214 (186–265) | 160 (144–238) | 11 (10–17) | 8 (7–12) | 0.81 |
| joplin--maple_leaf_rag.mxl | visor-continuo | 89 (78–122) | 73 (66–111) | 189 (175–245) | 162 (151–239) | 210 (186–272) | 152 (144–186) | 11 (10–16) | 8 (7–12) | 0.85 |
| mozart--k545--movement1_exposition.mxl | defecto | 48 (47–68) | 45 (39–68) | 18 (17–26) | 14 (13–21) | 27 (24–37) | 20 (19–23) | 1 (1–2) | 1 (1–1) | 0.89 |
| mozart--k545--movement1_exposition.mxl | visor-paginado | 47 (43–67) | 39 (37–42) | 19 (16–26) | 13 (13–14) | 27 (23–36) | 19 (18–20) | 1 (1–3) | 1 (1–1) | 0.79 |
| mozart--k545--movement1_exposition.mxl | visor-continuo | 18 (13–21) | 11 (11–18) | 24 (17–28) | 14 (14–17) | 35 (24–39) | 20 (19–27) | 1 (1–2) | 1 (1–1) | 0.61 |
| schubert--Lindenbaum.xml | defecto | 404 (325–522) | 298 (269–444) | 232 (206–307) | 193 (174–251) | 165 (156–251) | 132 (123–183) | 13 (12–20) | 11 (9–14) | 0.77 |
| schubert--Lindenbaum.xml | visor-paginado | 349 (314–402) | 335 (267–413) | 219 (199–262) | 204 (178–255) | 193 (157–227) | 137 (122–206) | 13 (12–16) | 10 (9–16) | 0.95 |
| schubert--Lindenbaum.xml | visor-continuo | 110 (99–134) | 84 (81–129) | 370 (329–433) | 288 (270–374) | 168 (154–259) | 126 (117–172) | 13 (12–18) | 9 (9–14) | 0.77 |
| schumann_robert--dichterliebe_no2.xml | defecto | 68 (62–107) | 55 (53–68) | 38 (35–59) | 30 (29–41) | 38 (34–67) | 29 (28–32) | 2 (2–4) | 2 (1–2) | 0.80 |
| schumann_robert--dichterliebe_no2.xml | visor-paginado | 72 (59–107) | 55 (53–92) | 42 (35–62) | 30 (29–54) | 42 (33–60) | 30 (27–54) | 3 (2–6) | 2 (1–3) | 0.75 |
| schumann_robert--dichterliebe_no2.xml | visor-continuo | 23 (19–33) | 18 (17–30) | 39 (35–61) | 34 (30–50) | 41 (33–61) | 34 (26–48) | 3 (2–4) | 2 (1–3) | 0.84 |

Suma de medianas carga+SVG: A = 6495 ms, B = 5204 ms, B/A = 0.80.

## Avisos del log (líneas, perfil defecto)
- alter-sintetico.musicxml: 1 → 0
- bach--bwv66.6.mxl: 0 → 0
- beach--prayer_of_a_tired_child.musicxml: 1 → 1
- beethoven--opus18no1--movement3.mxl: 7 → 7
- demos--two-parts.xml: 0 → 0
- demos--voices_with_chords.xml: 0 → 0
- joplin--maple_leaf_rag.mxl: 1 → 0
- mozart--k545--movement1_exposition.mxl: 0 → 0
- schubert--Lindenbaum.xml: 2 → 1
- schumann_robert--dichterliebe_no2.xml: 0 → 0
