// Laboratorio 6.1.0 -> 6.3.0: ejecuta un toolkit Verovio de npm sobre un corpus MusicXML y guarda
// SVG, MEI, timemap, alturas MIDI por nota y tiempos.
//
// Uso:
//   node lab/run.mjs <dir-con-node_modules/verovio> <dir-corpus> <dir-salida> [repeticiones]
//
// El corpus es un directorio con ficheros .xml, .musicxml o .mxl (ver lab/fetch-corpus.sh).
// Cada perfil de opciones (PROFILES) se ejecuta para cada fichero. Los tiempos se repiten
// <repeticiones> veces con un toolkit nuevo en cada repetición; los artefactos se guardan solo
// en la primera.

import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { performance } from 'node:perf_hooks';
import { pathToFileURL } from 'node:url';

const [, , vrvDir, corpusDir, outDir, repsArg] = process.argv;
if (!vrvDir || !corpusDir || !outDir) {
    console.error('uso: node lab/run.mjs <dir-verovio> <dir-corpus> <dir-salida> [repeticiones]');
    process.exit(1);
}
const reps = parseInt(repsArg || '5', 10);

// Perfiles de opciones. "defecto" no toca nada; los otros dos imitan un visor que fija escala y
// maquetación propias (valores supuestos, no los del visor real).
const PROFILES = {
    defecto: {},
    'visor-paginado': {
        scale: 40,
        pageWidth: 2100,
        pageHeight: 2970,
        adjustPageHeight: true,
        breaks: 'auto',
        header: 'none',
        footer: 'none',
    },
    'visor-continuo': {
        scale: 35,
        breaks: 'none',
        adjustPageWidth: true,
        adjustPageHeight: true,
        header: 'none',
        footer: 'none',
    },
};

const base = resolve(vrvDir, 'node_modules/verovio/dist');
const createVerovioModule = (await import(pathToFileURL(join(base, 'verovio-module.mjs')).href)).default;
const { VerovioToolkit, enableLogToBuffer } = await import(pathToFileURL(join(base, 'verovio.mjs')).href);
const VerovioModule = await createVerovioModule();
// Los avisos del importador van a getLog() en lugar de stderr.
enableLogToBuffer(true, VerovioModule);

function load(tk, file) {
    if (file.endsWith('.mxl')) {
        const buf = readFileSync(file);
        return tk.loadZipDataBuffer(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength));
    }
    return tk.loadData(readFileSync(file, 'utf8'));
}

function timed(fn) {
    const t0 = performance.now();
    const result = fn();
    return [result, performance.now() - t0];
}

const files = readdirSync(corpusDir)
    .filter((f) => /\.(xml|musicxml|mxl)$/.test(f))
    .sort();

const probe = new VerovioToolkit(VerovioModule);
const version = probe.getVersion();
const summary = { version, reps, profiles: PROFILES, defaultOptions: probe.getDefaultOptions(), runs: [] };
probe.destroy();

mkdirSync(outDir, { recursive: true });

for (const file of files) {
    for (const [profileName, options] of Object.entries(PROFILES)) {
        const stem = `${file.replace(/\.(xml|musicxml|mxl)$/, '')}__${profileName}`;
        const dir = join(outDir, stem);
        mkdirSync(dir, { recursive: true });
        const timings = [];
        for (let rep = 0; rep < reps; ++rep) {
            const tk = new VerovioToolkit(VerovioModule);
            // Semilla fija: los ids generados son reproducibles entre ejecuciones de una misma versión.
            tk.setOptions({ ...options, xmlIdSeed: 1 });
            const [ok, tLoad] = timed(() => load(tk, join(corpusDir, file)));
            // getLog() se vacía en cada llamada al toolkit: los avisos del importador se leen aquí.
            const loadLog = tk.getLog();
            if (!ok) {
                timings.push({ ok: false });
                tk.destroy();
                continue;
            }
            const pageCount = tk.getPageCount();
            const svgs = [];
            const [, tSvg] = timed(() => {
                for (let p = 1; p <= pageCount; ++p) svgs.push(tk.renderToSVG(p));
            });
            const [timemap, tTimemap] = timed(() => tk.renderToTimemap());
            const [mei, tMei] = timed(() => tk.getMEI());
            timings.push({ ok: true, load: tLoad, svg: tSvg, timemap: tTimemap, mei: tMei, pageCount });

            if (rep === 0) {
                svgs.forEach((svg, i) => writeFileSync(join(dir, `page-${String(i + 1).padStart(3, '0')}.svg`), svg));
                writeFileSync(join(dir, 'score.mei'), mei);
                writeFileSync(join(dir, 'timemap.json'), JSON.stringify(timemap));
                writeFileSync(
                    join(dir, 'timemap-measures-rests.json'),
                    JSON.stringify(tk.renderToTimemap({ includeMeasures: true, includeRests: true }))
                );
                // Alturas MIDI por nota (orden del documento MEI) y página de cada nota.
                const noteIds = [...mei.matchAll(/<note\b[^>]*\bxml:id="([^"]+)"/g)].map((m) => m[1]);
                const midi = noteIds.map((id) => {
                    const v = tk.getMIDIValuesForElement(id);
                    return { id, pitch: v.pitch ?? null, time: v.time ?? null, page: tk.getPageWithElement(id) };
                });
                writeFileSync(join(dir, 'midi-values.json'), JSON.stringify(midi));
                // Página que devuelve getElementsAtTime para cada instante "on" del timemap, frente a la
                // página real de la primera nota que suena. En pasajes repetidos el timemap da ids de la
                // expansión ("<id>-rend2") que no están en el SVG: se pasan antes por getNotatedIdForElement.
                const atTime = timemap
                    .filter((e) => e.on && e.on.length)
                    .map((e) => {
                        const r = tk.getElementsAtTime(Math.round(e.tstamp) + 1);
                        const notated = tk.getNotatedIdForElement(e.on[0]);
                        return { tstamp: e.tstamp, page: r.page ?? null, expected: tk.getPageWithElement(notated) };
                    });
                writeFileSync(join(dir, 'elements-at-time.json'), JSON.stringify(atTime));
                // ¿Están en el SVG los ids "on" del timemap, tal cual y tras getNotatedIdForElement?
                const svgIds = new Set(svgs.flatMap((svg) => [...svg.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1])));
                const onIds = timemap.flatMap((e) => e.on || []);
                const idCheck = {
                    on: onIds.length,
                    missingRaw: onIds.filter((id) => !svgIds.has(id)).length,
                    missingNotated: onIds.filter((id) => !svgIds.has(tk.getNotatedIdForElement(id))).length,
                    example: onIds.find((id) => !svgIds.has(id)) ?? null,
                };
                writeFileSync(join(dir, 'timemap-ids-in-svg.json'), JSON.stringify(idCheck));
                writeFileSync(join(dir, 'log.txt'), loadLog);
            }
            tk.destroy();
        }
        summary.runs.push({ file, profile: profileName, timings });
        console.error(`${version} ${stem}: ${timings.map((t) => (t.ok ? (t.load + t.svg).toFixed(0) : 'ERR')).join(' ')}`);
    }
}

writeFileSync(join(outDir, 'summary.json'), JSON.stringify(summary, null, 1));
