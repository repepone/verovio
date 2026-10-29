#!/usr/bin/env bash
# Reproduce el laboratorio completo: instala 6.1.0 y 6.3.0 de npm, prepara el corpus, ejecuta
# cuatro pasadas alternas (A, B, B, A) de 5 repeticiones, mide el arranque y compara.
# Uso: lab/run-all.sh <dir-trabajo> [dir-resultados]
set -euo pipefail

LAB="$(cd "$(dirname "$0")" && pwd)"
WORK="${1:?dir-trabajo}"
RES="${2:-$LAB/resultados}"
REPS="${REPS:-5}"

"$LAB/setup.sh" "$WORK"
"$LAB/fetch-corpus.sh" "$WORK" "$WORK/corpus"

for r in "v610 out610-a" "v630 out630-a" "v630 out630-b" "v610 out610-b"; do
    set -- $r
    node "$LAB/run.mjs" "$WORK/$1" "$WORK/corpus" "$WORK/$2" "$REPS" 2> "$WORK/$2.stderr"
done

mkdir -p "$RES"
: > "$RES/init-time.jsonl"
for i in 1 2 3 4 5; do
    for v in v610 v630; do
        node "$LAB/init-time.mjs" "$WORK/$v" >> "$RES/init-time.jsonl"
    done
done

for v in v610 v630; do
    for f in "$LAB"/casos/*.mei; do
        echo "{\"case\": \"$(basename "$f")\", \"result\": $(node "$LAB/load-one.mjs" "$WORK/$v" "$f" 2>/dev/null)}"
    done
done > "$RES/casos-mei.jsonl"

python3 -I "$LAB/compare.py" "$WORK/corpus" "$RES" \
    "$WORK/out610-a" "$WORK/out630-a" "$WORK/out610-b" "$WORK/out630-b"
