// Carga un fichero con un toolkit de npm e informa del resultado (o de la excepción).
// Uso: node lab/load-one.mjs <dir-con-node_modules/verovio> <fichero>
import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const [, , vrvDir, file] = process.argv;
const base = resolve(vrvDir, 'node_modules/verovio/dist');
const createVerovioModule = (await import(pathToFileURL(join(base, 'verovio-module.mjs')).href)).default;
const { VerovioToolkit } = await import(pathToFileURL(join(base, 'verovio.mjs')).href);
const tk = new VerovioToolkit(await createVerovioModule());
try {
    const ok = tk.loadData(readFileSync(file, 'utf8'));
    const svg = ok ? tk.renderToSVG(1) : '';
    console.log(JSON.stringify({ version: tk.getVersion(), ok, svgBytes: svg.length, pages: tk.getPageCount() }));
} catch (e) {
    console.log(JSON.stringify({ version: tk.getVersion(), exception: String(e) }));
    process.exitCode = 2;
}
