#!/usr/bin/env bash
# Instala desde npm los toolkits JS/WASM de Verovio 6.1.0 y 6.3.0 en <dir-trabajo>/v610 y v630.
# Uso: lab/setup.sh <dir-trabajo>
set -euo pipefail

WORK="${1:?dir-trabajo}"
for v in 6.1.0 6.3.0; do
    d="$WORK/v${v//./}"
    mkdir -p "$d"
    (cd "$d" && [ -f package.json ] || npm init -y > /dev/null)
    (cd "$d" && npm install --silent "verovio@$v")
    node -e "import('$d/node_modules/verovio/dist/verovio-module.mjs').then(async (m) => {
        const { VerovioToolkit } = await import('$d/node_modules/verovio/dist/verovio.mjs');
        const tk = new VerovioToolkit(await m.default());
        console.log('$v ->', tk.getVersion());
    })"
done
