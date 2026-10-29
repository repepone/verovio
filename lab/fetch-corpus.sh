#!/usr/bin/env bash
# Descarga de PyPI la rueda de music21 10.5.2, comprueba su sha256 y copia a <dir-corpus> los
# MusicXML públicos usados en el laboratorio, más el caso sintético de lab/casos/.
# Los ficheros de music21 no se suben a la rama: cada uno tiene su propia licencia
# (ver music21/corpus/license.txt dentro de la rueda).
#
# Uso: lab/fetch-corpus.sh <dir-trabajo> <dir-corpus>
set -euo pipefail

WORK="${1:?dir-trabajo}"
CORPUS="${2:?dir-corpus}"
LAB="$(cd "$(dirname "$0")" && pwd)"
WHEEL="music21-10.5.2-py3-none-any.whl"
SHA256="dba8696eafab709a244b6f18c64399edcccf4e96ddd1e0e4de7eff0a291c2dec"

FILES=(
    schubert/Lindenbaum.xml
    demos/voices_with_chords.xml
    demos/two-parts.xml
    joplin/maple_leaf_rag.mxl
    mozart/k545/movement1_exposition.mxl
    beethoven/opus18no1/movement3.mxl
    schumann_robert/dichterliebe_no2.xml
    bach/bwv66.6.mxl
    beach/prayer_of_a_tired_child.musicxml
)

mkdir -p "$WORK/dl" "$CORPUS"
if [ ! -f "$WORK/dl/$WHEEL" ]; then
    pip download music21==10.5.2 --no-deps -d "$WORK/dl" -q
fi
echo "$SHA256  $WORK/dl/$WHEEL" | sha256sum -c -

for f in "${FILES[@]}"; do
    # nombre plano: schubert/Lindenbaum.xml -> schubert--Lindenbaum.xml
    unzip -p "$WORK/dl/$WHEEL" "music21/corpus/$f" > "$CORPUS/${f//\//--}"
done
cp "$LAB/casos/alter-sintetico.musicxml" "$CORPUS/"
ls -l "$CORPUS"
