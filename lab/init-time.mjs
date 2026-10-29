// Mide el arranque del toolkit (import del módulo WASM + createVerovioModule + primer toolkit).
// Cada medida debe hacerse en un proceso nuevo para no reutilizar el módulo ya compilado.
// Uso: node lab/init-time.mjs <dir-con-node_modules/verovio>
import { join, resolve } from 'node:path';
import { performance } from 'node:perf_hooks';
import { pathToFileURL } from 'node:url';

const base = resolve(process.argv[2], 'node_modules/verovio/dist');
const t0 = performance.now();
const createVerovioModule = (await import(pathToFileURL(join(base, 'verovio-module.mjs')).href)).default;
const { VerovioToolkit } = await import(pathToFileURL(join(base, 'verovio.mjs')).href);
const t1 = performance.now();
const VerovioModule = await createVerovioModule();
const t2 = performance.now();
const tk = new VerovioToolkit(VerovioModule);
const t3 = performance.now();
console.log(
    JSON.stringify({ version: tk.getVersion(), importMs: t1 - t0, moduleMs: t2 - t1, toolkitMs: t3 - t2, totalMs: t3 - t0 })
);
