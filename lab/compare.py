#!/usr/bin/env python3
"""Compara las salidas de lab/run.mjs para Verovio 6.1.0 (A) y 6.3.0 (B).

Uso:
    python3 -I lab/compare.py <corpus> <salida-dir> <A1> <B1> [<A2> <B2> ...]

Los artefactos (SVG, MEI, timemap, MIDI) se comparan entre A1 y B1. Los tiempos se agregan de
todos los directorios A* y B* (mediana de todas las repeticiones). Escribe resultados.json y
RESULTADOS.md en <salida-dir>.
"""

import hashlib
import json
import re
import statistics
import sys
import zipfile
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
MEI_NS = "http://www.music-encoding.org/ns/mei"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
STEP_PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def local(tag):
    return tag.split("}", 1)[-1]


# ---------------------------------------------------------------------------
# MusicXML: alturas esperadas por índice de compás


def read_musicxml(path):
    if path.suffix == ".mxl":
        with zipfile.ZipFile(path) as z:
            container = ET.fromstring(z.read("META-INF/container.xml"))
            rootfile = next(e for e in container.iter() if local(e.tag) == "rootfile").get("full-path")
            return ET.fromstring(z.read(rootfile))
    return ET.parse(path).getroot()


def expected_pitches(path):
    """Devuelve {índice de compás: Counter(alturas MIDI)} según step/alter/octave (+transpose)."""
    root = read_musicxml(path)
    per_measure = {}
    for part in root.findall("part"):
        chromatic = 0
        for idx, measure in enumerate(part.findall("measure")):
            for tr in measure.iter("transpose"):
                chromatic = int(tr.findtext("chromatic", "0")) + 12 * int(tr.findtext("octave-change", "0"))
            for note in measure.findall("note"):
                pitch = note.find("pitch")
                if pitch is None:
                    continue
                midi = (
                    STEP_PC[pitch.findtext("step").strip()]
                    + float(pitch.findtext("alter", "0"))
                    + (int(pitch.findtext("octave")) + 1) * 12
                    + chromatic
                )
                per_measure.setdefault(idx, Counter())[round(midi)] += 1
    return per_measure


# ---------------------------------------------------------------------------
# MEI


def mei_notes(mei_path):
    """Lista de (xml:id, índice de compás) en orden de documento, y la raíz."""
    root = ET.parse(mei_path).getroot()
    notes = []
    for idx, measure in enumerate(root.iter(f"{{{MEI_NS}}}measure")):
        for note in measure.iter(f"{{{MEI_NS}}}note"):
            notes.append((note.get(XML_ID), idx))
    return notes, root


def mei_stats(mei_path):
    root = ET.parse(mei_path).getroot()
    tags = Counter(local(e.tag) for e in root.iter())
    attrs = Counter()
    for e in root.iter():
        for k in e.attrib:
            attrs[f"{local(e.tag)}@{local(k)}"] += 1
    return {
        "bytes": mei_path.stat().st_size,
        "meiversion": root.get("meiversion"),
        "tags": tags,
        "attrs": attrs,
    }


def normalized_lines(text):
    # ids aleatorios o desplazados no deben contar como diferencia de contenido
    text = re.sub(r'xml:id="[^"]*"', 'xml:id="#"', text)
    text = re.sub(r'(startid|endid|plist|corresp|sameas|next|prev|follows|precedes)="[^"]*"', r'\1="#"', text)
    text = re.sub(r"<application[\s\S]*?</application>", "", text)
    text = re.sub(r'(isodate|version)="[^"]*"', r'\1="#"', text)
    return text.splitlines()


# ---------------------------------------------------------------------------
# SVG


def summarize_css(rule):
    # la fuente incrustada ocupa decenas de KB: se resume por tamaño y huella
    if rule.startswith("@font-face"):
        family = re.search(r"font-family:\s*'([^']+)'", rule)
        return f"@font-face {family.group(1) if family else '?'} ({len(rule)} bytes, sha1 {hashlib.sha1(rule.encode()).hexdigest()[:10]})"
    # el prefijo "#<id-del-documento>" cambia en cada carga
    return re.sub(r"^#\S+\s+", "", rule)


def svg_page_stats(path):
    root = ET.parse(path).getroot()
    classes = Counter()
    tags = Counter()
    attr_names = Counter()
    ids = 0
    signature = []
    signature_no_empty_accid = []
    empty_accid = 0
    page_ids = {e.get("id") for e in root.iter() if e.get("id")}
    for e in root.iter():
        tag = local(e.tag)
        tags[tag] += 1
        # las clases pueden llevar ids referenciados ("id-xxxx", "systemMilestoneEnd <id>"): se descartan
        cls = " ".join(c for c in e.get("class", "").split() if not c.startswith("id-") and not re.search(r"\d", c) and c not in page_ids)
        for c in cls.split():
            classes[c] += 1
        if e.get("id"):
            ids += 1
        for k in e.attrib:
            attr_names[f"{tag}@{local(k)}"] += 1
        signature.append(f"{tag}.{cls}")
        if tag == "g" and cls == "accid" and len(e) == 0:
            empty_accid += 1
        else:
            signature_no_empty_accid.append(f"{tag}.{cls}")
    style = " ".join(s.text or "" for s in root.iter(f"{{{SVG_NS}}}style"))
    # posición de cada cabeza de nota: primer <use> dentro de g.notehead, por orden
    heads = []
    for g in root.iter(f"{{{SVG_NS}}}g"):
        if "notehead" in g.get("class", "").split():
            use = g.find(f".//{{{SVG_NS}}}use")
            m = re.search(r"translate\(([-\d.]+),\s*([-\d.]+)\)", use.get("transform", "")) if use is not None else None
            if m:
                heads.append((float(m.group(1)), float(m.group(2))))
    inner = next((e for e in root.iter(f"{{{SVG_NS}}}svg") if e is not root), root)
    return {
        "bytes": path.stat().st_size,
        "width": root.get("width"),
        "height": root.get("height"),
        "viewBox": inner.get("viewBox"),
        "classes": classes,
        "tags": tags,
        "attr_names": attr_names,
        "ids": ids,
        "signature": signature,
        "signature_no_empty_accid": signature_no_empty_accid,
        "empty_accid": empty_accid,
        "style_rules": set(summarize_css(r.strip() + "}") for r in style.split("}") if r.strip()),
        "heads": heads,
    }


def compare_svg(dir_a, dir_b):
    pages_a = sorted(dir_a.glob("page-*.svg"))
    pages_b = sorted(dir_b.glob("page-*.svg"))
    res = {
        "pages": [len(pages_a), len(pages_b)],
        "bytes": [0, 0],
        "ids": [0, 0],
        "g": [0, 0],
        "class_diff": Counter(),
        "attr_diff": Counter(),
        "style_only_a": set(),
        "style_only_b": set(),
        "size_changed_pages": 0,
        "signature_equal_pages": 0,
        "signature_equal_pages_no_empty_accid": 0,
        "empty_accid": [0, 0],
        "sig_ops": Counter(),
        "heads": [0, 0],
        "heads_compared": 0,
        "pages_head_count_differs": 0,
        "heads_moved": 0,
        "heads_max_dx": 0.0,
        "heads_max_dy": 0.0,
    }
    totals = [Counter(), Counter()]
    attrs = [Counter(), Counter()]
    for i in range(max(len(pages_a), len(pages_b))):
        sa = svg_page_stats(pages_a[i]) if i < len(pages_a) else None
        sb = svg_page_stats(pages_b[i]) if i < len(pages_b) else None
        for k, s in enumerate((sa, sb)):
            if s is None:
                continue
            res["bytes"][k] += s["bytes"]
            res["ids"][k] += s["ids"]
            res["g"][k] += s["tags"]["g"]
            res["heads"][k] += len(s["heads"])
            res["empty_accid"][k] += s["empty_accid"]
            totals[k].update(s["classes"])
            attrs[k].update(s["attr_names"])
        if sa is None or sb is None:
            continue
        res["style_only_a"] |= sa["style_rules"] - sb["style_rules"]
        res["style_only_b"] |= sb["style_rules"] - sa["style_rules"]
        if (sa["width"], sa["height"], sa["viewBox"]) != (sb["width"], sb["height"], sb["viewBox"]):
            res["size_changed_pages"] += 1
        if sa["signature"] == sb["signature"]:
            res["signature_equal_pages"] += 1
        if sa["signature_no_empty_accid"] == sb["signature_no_empty_accid"]:
            res["signature_equal_pages_no_empty_accid"] += 1
        else:
            for op, a1, a2, b1, b2 in SequenceMatcher(
                None, sa["signature_no_empty_accid"], sb["signature_no_empty_accid"], autojunk=False
            ).get_opcodes():
                if op != "equal":
                    res["sig_ops"][op] += max(a2 - a1, b2 - b1)
        if len(sa["heads"]) != len(sb["heads"]):
            res["pages_head_count_differs"] += 1
        if len(sa["heads"]) == len(sb["heads"]):
            for (xa, ya), (xb, yb) in zip(sa["heads"], sb["heads"]):
                res["heads_compared"] += 1
                if (xa, ya) != (xb, yb):
                    res["heads_moved"] += 1
                res["heads_max_dx"] = max(res["heads_max_dx"], abs(xa - xb))
                res["heads_max_dy"] = max(res["heads_max_dy"], abs(ya - yb))
    for c in set(totals[0]) | set(totals[1]):
        if totals[0][c] != totals[1][c]:
            res["class_diff"][c] = totals[1][c] - totals[0][c]
    for c in set(attrs[0]) | set(attrs[1]):
        if (attrs[0][c] == 0) != (attrs[1][c] == 0):
            res["attr_diff"][c] = attrs[1][c] - attrs[0][c]
    return res


# ---------------------------------------------------------------------------
# Timemap


def compare_timemap(path_a, path_b, order_a, order_b):
    """order_*: {xml:id: posición de la nota en el MEI}; permite comparar sin depender de los ids."""
    ta = json.loads(path_a.read_text())
    tb = json.loads(path_b.read_text())

    def norm(entries, order):
        out = []
        for e in entries:
            out.append(
                (
                    e.get("tstamp"),
                    e.get("qstamp"),
                    tuple(sorted(order.get(i, -1) for i in e.get("on", []))),
                    tuple(sorted(order.get(i, -1) for i in e.get("off", []))),
                    len(e.get("restsOn", [])),
                    len(e.get("restsOff", [])),
                    e.get("tempo"),
                    "measureOn" in e,
                )
            )
        return out

    na, nb = norm(ta, order_a), norm(tb, order_b)
    keys_a = Counter(k for e in ta for k in e)
    keys_b = Counter(k for e in tb for k in e)
    same_ids = sum(1 for ea, eb in zip(ta, tb) if ea.get("on") == eb.get("on") and ea.get("off") == eb.get("off"))
    max_dt = None
    if len(ta) == len(tb):
        max_dt = max((abs(a["tstamp"] - b["tstamp"]) for a, b in zip(ta, tb)), default=0)
    return {
        "entries": [len(ta), len(tb)],
        "end_ms": [ta[-1]["tstamp"] if ta else None, tb[-1]["tstamp"] if tb else None],
        "equal_modulo_ids": na == nb,
        "entries_diff": sum(1 for x, y in zip(na, nb) if x != y) + abs(len(na) - len(nb)),
        "entries_same_ids": same_ids,
        "max_abs_dt_ms": max_dt,
        "keys": [dict(keys_a), dict(keys_b)],
    }


# ---------------------------------------------------------------------------


def pitch_errors(expected, notes, midi):
    """Notas cuya altura MIDI no casa con la esperada, por multiconjunto en cada compás."""
    got = {}
    pitch_by_id = {m["id"]: m["pitch"] for m in midi}
    for nid, idx in notes:
        p = pitch_by_id.get(nid)
        if p is not None:
            got.setdefault(idx, Counter())[p] += 1
    errors = 0
    for idx in set(expected) | set(got):
        exp = expected.get(idx, Counter())
        g = got.get(idx, Counter())
        errors += sum((exp - g).values())
    return errors, sum(sum(c.values()) for c in expected.values()), sum(sum(c.values()) for c in got.values())


def load_timings(dirs):
    acc = {}
    for d in dirs:
        summary = json.loads((d / "summary.json").read_text())
        for run in summary["runs"]:
            key = (run["file"], run["profile"])
            for t in run["timings"]:
                if not t.get("ok"):
                    continue
                for k in ("load", "svg", "timemap", "mei"):
                    acc.setdefault(key, {}).setdefault(k, []).append(t[k])
    return acc


def stem_of(name):
    return re.sub(r"\.(xml|musicxml|mxl)$", "", name)


def main():
    corpus = Path(sys.argv[1])
    out = Path(sys.argv[2])
    dirs = [Path(p) for p in sys.argv[3:]]
    a_dirs, b_dirs = dirs[0::2], dirs[1::2]
    A, B = a_dirs[0], b_dirs[0]
    sum_a = json.loads((A / "summary.json").read_text())
    sum_b = json.loads((B / "summary.json").read_text())

    results = {"versions": [sum_a["version"], sum_b["version"]], "files": []}

    # opciones por defecto
    da, db = sum_a["defaultOptions"], sum_b["defaultOptions"]
    results["options_only_a"] = sorted(set(da) - set(db))
    results["options_only_b"] = sorted(set(db) - set(da))
    results["options_default_changed"] = {k: [da[k], db[k]] for k in set(da) & set(db) if da[k] != db[k]}

    t_a, t_b = load_timings(a_dirs), load_timings(b_dirs)
    results["reps"] = {
        "A": sum(len(v["load"]) for v in t_a.values()) // max(len(t_a), 1),
        "B": sum(len(v["load"]) for v in t_b.values()) // max(len(t_b), 1),
    }

    for src in sorted(p for p in corpus.iterdir() if p.suffix in (".xml", ".musicxml", ".mxl")):
        expected = expected_pitches(src)
        for profile in sum_a["profiles"]:
            stem = f"{stem_of(src.name)}__{profile}"
            da_, db_ = A / stem, B / stem
            row = {"file": src.name, "profile": profile}
            notes_a, _ = mei_notes(da_ / "score.mei")
            notes_b, _ = mei_notes(db_ / "score.mei")
            midi_a = json.loads((da_ / "midi-values.json").read_text())
            midi_b = json.loads((db_ / "midi-values.json").read_text())
            row["notes"] = [len(notes_a), len(notes_b)]
            ea, n_exp, _ = pitch_errors(expected, notes_a, midi_a)
            eb, _, _ = pitch_errors(expected, notes_b, midi_b)
            row["expected_notes"] = n_exp
            row["pitch_errors"] = [ea, eb]
            row["pitch_changed_by_order"] = (
                sum(1 for x, y in zip(midi_a, midi_b) if x["pitch"] != y["pitch"]) if len(midi_a) == len(midi_b) else None
            )
            row["same_note_ids"] = sum(1 for (x, _), (y, _) in zip(notes_a, notes_b) if x == y)
            # MEI
            ma, mb = mei_stats(da_ / "score.mei"), mei_stats(db_ / "score.mei")
            row["mei_bytes"] = [ma["bytes"], mb["bytes"]]
            row["meiversion"] = [ma["meiversion"], mb["meiversion"]]
            row["mei_tag_diff"] = {k: mb["tags"][k] - ma["tags"][k] for k in set(ma["tags"]) | set(mb["tags"]) if ma["tags"][k] != mb["tags"][k]}
            row["mei_attr_diff"] = {k: mb["attrs"][k] - ma["attrs"][k] for k in set(ma["attrs"]) | set(mb["attrs"]) if ma["attrs"][k] != mb["attrs"][k]}
            la = normalized_lines((da_ / "score.mei").read_text())
            lb = normalized_lines((db_ / "score.mei").read_text())
            row["mei_lines_changed"] = sum(
                max(a2 - a1, b2 - b1)
                for op, a1, a2, b1, b2 in SequenceMatcher(None, la, lb, autojunk=False).get_opcodes()
                if op != "equal"
            )
            # SVG
            sv = compare_svg(da_, db_)
            row["svg"] = {
                k: (dict(v) if isinstance(v, Counter) else sorted(v) if isinstance(v, set) else v) for k, v in sv.items()
            }
            # timemap
            order_a = {nid: i for i, (nid, _) in enumerate(notes_a)}
            order_b = {nid: i for i, (nid, _) in enumerate(notes_b)}
            row["timemap"] = compare_timemap(da_ / "timemap.json", db_ / "timemap.json", order_a, order_b)
            row["timemap_mr"] = compare_timemap(
                da_ / "timemap-measures-rests.json", db_ / "timemap-measures-rests.json", order_a, order_b
            )
            # getElementsAtTime
            ata = json.loads((da_ / "elements-at-time.json").read_text())
            atb = json.loads((db_ / "elements-at-time.json").read_text())
            row["at_time_wrong_page"] = [
                sum(1 for e in ata if e["page"] != e["expected"]),
                sum(1 for e in atb if e["page"] != e["expected"]),
                len(ata),
                len(atb),
            ]
            row["timemap_ids_in_svg"] = [
                json.loads((da_ / "timemap-ids-in-svg.json").read_text()),
                json.loads((db_ / "timemap-ids-in-svg.json").read_text()),
            ]
            # log
            row["log_lines"] = [
                len((da_ / "log.txt").read_text().splitlines()),
                len((db_ / "log.txt").read_text().splitlines()),
            ]
            # tiempos
            key = (src.name, profile)
            row["time_ms"] = {}
            for k in ("load", "svg", "timemap", "mei"):
                va, vb = t_a.get(key, {}).get(k, []), t_b.get(key, {}).get(k, [])
                row["time_ms"][k] = {
                    "A": [min(va), statistics.median(va), max(va)] if va else None,
                    "B": [min(vb), statistics.median(vb), max(vb)] if vb else None,
                }
            results["files"].append(row)

    out.mkdir(parents=True, exist_ok=True)
    (out / "resultados.json").write_text(json.dumps(results, indent=1, ensure_ascii=False, default=list))
    write_markdown(results, out / "RESULTADOS.md")


def fmt_pair(p):
    return f"{p[0]} → {p[1]}"


def write_markdown(r, path):
    va, vb = r["versions"]
    L = [f"# Resultados medidos: {va} (A) frente a {vb} (B)", ""]
    L.append(f"Repeticiones de tiempo por caso: A={r['reps']['A']}, B={r['reps']['B']}. Generado por `lab/compare.py`.")
    L.append("")
    L.append("## Opciones (getDefaultOptions)")
    L.append(f"- Solo en A: {r['options_only_a'] or 'ninguna'}")
    L.append(f"- Solo en B: {r['options_only_b'] or 'ninguna'}")
    L.append(f"- Valor por defecto distinto: {r['options_default_changed'] or 'ninguno'}")
    L.append("")
    L.append("## Alturas MIDI frente a `<pitch>` de MusicXML (perfil defecto)")
    L.append("| fichero | notas esperadas | notas MEI A → B | errores A | errores B | notas con altura distinta A/B |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for f in r["files"]:
        if f["profile"] != "defecto":
            continue
        L.append(
            f"| {f['file']} | {f['expected_notes']} | {fmt_pair(f['notes'])} | {f['pitch_errors'][0]} | {f['pitch_errors'][1]} | {f['pitch_changed_by_order']} |"
        )
    L.append("")
    L.append("## MEI (perfil defecto)")
    L.append("| fichero | bytes A → B | meiversion | líneas cambiadas (ids normalizados) | elementos (B−A) | atributos (B−A) |")
    L.append("|---|---:|---|---:|---|---|")
    for f in r["files"]:
        if f["profile"] != "defecto":
            continue
        tags = ", ".join(f"{k} {v:+d}" for k, v in sorted(f["mei_tag_diff"].items())) or "="
        attrs = ", ".join(f"{k} {v:+d}" for k, v in sorted(f["mei_attr_diff"].items())) or "="
        L.append(
            f"| {f['file']} | {fmt_pair(f['mei_bytes'])} | {fmt_pair(f['meiversion'])} | {f['mei_lines_changed']} | {tags} | {attrs} |"
        )
    L.append("")
    L.append("## SVG")
    L.append(
        "| fichero | perfil | páginas A → B | bytes A → B | `<g>` A → B | elementos con id A → B | `g.accid` vacíos A → B | páginas con tamaño distinto | páginas con estructura idéntica (sin / con `g.accid` vacíos) | elementos estructurales distintos | páginas con nº de cabezas distinto | cabezas comparadas / movidas | máx \\|Δx\\|, \\|Δy\\| | clases (B−A) |"
    )
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for f in r["files"]:
        s = f["svg"]
        cls = ", ".join(f"{k} {v:+d}" for k, v in sorted(s["class_diff"].items())) or "="
        L.append(
            f"| {f['file']} | {f['profile']} | {fmt_pair(s['pages'])} | {fmt_pair(s['bytes'])} | {fmt_pair(s['g'])} | {fmt_pair(s['ids'])} | {fmt_pair(s['empty_accid'])} | {s['size_changed_pages']} | {s['signature_equal_pages_no_empty_accid']} / {s['signature_equal_pages']} | {sum(s['sig_ops'].values())} | {s['pages_head_count_differs']} | {s['heads_compared']} / {s['heads_moved']} | {s['heads_max_dx']:.0f}, {s['heads_max_dy']:.0f} | {cls} |"
        )
    L.append("")
    styles_a = sorted({x for f in r["files"] for x in f["svg"]["style_only_a"]})
    styles_b = sorted({x for f in r["files"] for x in f["svg"]["style_only_b"]})
    attrs = Counter()
    for f in r["files"]:
        for k, v in f["svg"]["attr_diff"].items():
            attrs[k] += v
    L.append(f"- Reglas CSS de `<style>` solo en A: {styles_a or 'ninguna'}")
    L.append(f"- Reglas CSS de `<style>` solo en B: {styles_b or 'ninguna'}")
    L.append(f"- Atributos (elemento@atributo) presentes solo en una versión, suma B−A: {dict(attrs) or 'ninguno'}")
    L.append("")
    L.append("## Timemap")
    L.append(
        "| fichero | perfil | entradas A → B | fin (ms) A → B | igual salvo ids | entradas distintas | máx Δt absoluto (ms) | con measures+rests: igual salvo ids | getElementsAtTime página errónea A / B (de n) | ids `on` ausentes del SVG A / B (de n) | … tras getNotatedIdForElement A / B |"
    )
    L.append("|---|---|---:|---:|---|---:|---:|---|---:|---:|---:|")
    for f in r["files"]:
        t, tm, at, ids = f["timemap"], f["timemap_mr"], f["at_time_wrong_page"], f["timemap_ids_in_svg"]
        L.append(
            f"| {f['file']} | {f['profile']} | {fmt_pair(t['entries'])} | {fmt_pair(t['end_ms'])} | {'sí' if t['equal_modulo_ids'] else 'no'} | {t['entries_diff']} | {t['max_abs_dt_ms']} | {'sí' if tm['equal_modulo_ids'] else 'no'} | {at[0]} / {at[1]} (de {at[2]}) | {ids[0]['missingRaw']} / {ids[1]['missingRaw']} (de {ids[0]['on']}) | {ids[0]['missingNotated']} / {ids[1]['missingNotated']} |"
        )
    L.append("")
    L.append("## Tiempos (mediana en ms; entre paréntesis mín–máx)")
    L.append("| fichero | perfil | carga A | carga B | SVG A | SVG B | timemap A | timemap B | MEI A | MEI B | carga+SVG B/A |")
    L.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    tot_a = tot_b = 0.0
    for f in r["files"]:
        t = f["time_ms"]

        def c(x):
            return f"{x[1]:.0f} ({x[0]:.0f}–{x[2]:.0f})" if x else "—"

        ra = t["load"]["A"][1] + t["svg"]["A"][1]
        rb = t["load"]["B"][1] + t["svg"]["B"][1]
        tot_a += ra
        tot_b += rb
        L.append(
            f"| {f['file']} | {f['profile']} | {c(t['load']['A'])} | {c(t['load']['B'])} | {c(t['svg']['A'])} | {c(t['svg']['B'])} | {c(t['timemap']['A'])} | {c(t['timemap']['B'])} | {c(t['mei']['A'])} | {c(t['mei']['B'])} | {rb / ra:.2f} |"
        )
    L.append("")
    L.append(f"Suma de medianas carga+SVG: A = {tot_a:.0f} ms, B = {tot_b:.0f} ms, B/A = {tot_b / tot_a:.2f}.")
    L.append("")
    L.append("## Avisos del log (líneas, perfil defecto)")
    for f in r["files"]:
        if f["profile"] == "defecto":
            L.append(f"- {f['file']}: {fmt_pair(f['log_lines'])}")
    path.write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
