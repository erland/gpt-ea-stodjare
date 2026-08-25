#!/usr/bin/env python3
"""Verify semantic preservation for an EA Stödjare v1 -> v2 migration.

The verifier is intentionally conservative. It accepts only explicitly declared
legacy-preservation transforms and otherwise requires canonical records,
provenance, stable IDs, and regenerated reader-facing output to remain
semantically equivalent.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml

LEGACY_RELATION_EQUIVALENCE = {"legacy_realized_by": "realized_by"}


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_manifest(root: Path) -> dict[str, Any]:
    return json.loads((root / "project-manifest.json").read_text(encoding="utf-8"))


def model_root(root: Path) -> Path:
    manifest = load_manifest(root)
    return root / str((manifest.get("model") or {}).get("root", "model"))


def canonical_objects(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(model_root(root).glob("*.yaml")):
        data = load_yaml(path)
        rows = data.get("objects")
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("id"):
                out[str(row["id"])] = copy.deepcopy(row)
    return out


def canonical_relations(root: Path) -> dict[str, dict[str, Any]]:
    path = model_root(root) / "relations.yaml"
    rows = load_yaml(path).get("relations", []) if path.is_file() else []
    return {str(r["id"]): copy.deepcopy(r) for r in rows if isinstance(r, dict) and r.get("id")}


def sources(root: Path) -> dict[str, dict[str, Any]]:
    path = model_root(root) / "sources.yaml"
    rows = load_yaml(path).get("sources", []) if path.is_file() else []
    return {str(r["id"]): copy.deepcopy(r) for r in rows if isinstance(r, dict) and r.get("id")}


def normalized_relation(row: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(row)
    typ = str(out.get("type", ""))
    out["type"] = LEGACY_RELATION_EQUIVALENCE.get(typ, typ)
    return out


def provenance_map(records: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {rid: copy.deepcopy(row.get("provenance", [])) for rid, row in records.items()}


def normalize_generated_text(text: str) -> str:
    text = text.replace("legacy_realized_by", "realized_by")
    text = re.sub(r"projektrevision\s+`?\d+`?", "projektrevision <revision>", text)
    text = re.sub(r'"revision"\s*:\s*\d+', '"revision": <revision>', text)
    return text.replace("\r\n", "\n")


def file_texts(root: Path) -> dict[str, str]:
    out = {}
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        out[p.relative_to(root).as_posix()] = normalize_generated_text(p.read_text(encoding="utf-8"))
    return out


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)


def verify_generated(repo: Path, source: Path, target: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        src_md, tgt_md = t / "src-md", t / "tgt-md"
        src_cf, tgt_cf = t / "src-cf", t / "tgt-cf"
        run([sys.executable, str(repo / "scripts/generate_markdown.py"), "--project-root", str(source), "--mode", "working", "--output-dir", str(src_md)], repo)
        run([sys.executable, str(repo / "scripts/generate_markdown.py"), "--project-root", str(target), "--mode", "working", "--output-dir", str(tgt_md)], repo)
        run([sys.executable, str(repo / "scripts/generate_confluence.py"), "--project-root", str(source), "--mode", "working", "--output-dir", str(src_cf)], repo)
        run([sys.executable, str(repo / "scripts/generate_confluence.py"), "--project-root", str(target), "--mode", "working", "--output-dir", str(tgt_cf)], repo)
        md_equal = file_texts(src_md) == file_texts(tgt_md)
        cf_equal = file_texts(src_cf) == file_texts(tgt_cf)

        src_docs, tgt_docs = t / "src-docs", t / "tgt-docs"
        run([sys.executable, str(repo / "scripts/export_documents.py"), "--project-root", str(source), "--mode", "working", "--output-dir", str(src_docs), "--basename", "ea"], repo)
        run([sys.executable, str(repo / "scripts/export_documents.py"), "--project-root", str(target), "--mode", "working", "--output-dir", str(tgt_docs), "--basename", "ea"], repo)
        docs_ok = all((d / f"ea.{ext}").is_file() and (d / f"ea.{ext}").stat().st_size > 1000 for d in (src_docs, tgt_docs) for ext in ("docx", "pdf"))

    return {
        "markdown_semantically_equivalent": md_equal,
        "confluence_semantically_equivalent": cf_equal,
        "docx_pdf_generated_for_source_and_target": docs_ok,
    }


def verify(repo: Path, source: Path, target: Path, generate_documents: bool = True) -> dict[str, Any]:
    src_obj, tgt_obj = canonical_objects(source), canonical_objects(target)
    src_rel, tgt_rel = canonical_relations(source), canonical_relations(target)
    src_sources, tgt_sources = sources(source), sources(target)

    rel_equiv = set(src_rel) == set(tgt_rel) and all(normalized_relation(tgt_rel[rid]) == src_rel[rid] for rid in src_rel)
    checks = {
        "object_ids_preserved": set(src_obj) == set(tgt_obj),
        "relation_ids_preserved": set(src_rel) == set(tgt_rel),
        "source_ids_preserved": set(src_sources) == set(tgt_sources),
        "objects_exactly_preserved": src_obj == tgt_obj,
        "sources_exactly_preserved": src_sources == tgt_sources,
        "object_provenance_preserved": provenance_map(src_obj) == provenance_map(tgt_obj),
        "relation_provenance_preserved": provenance_map(src_rel) == provenance_map(tgt_rel),
        "relations_semantically_equivalent": rel_equiv,
    }
    if generate_documents:
        checks.update(verify_generated(repo, source, target))
    src_manifest, tgt_manifest = load_manifest(source), load_manifest(target)
    report = {
        "schema_version": "1.0",
        "verification": {
            "source_revision": (src_manifest.get("project") or {}).get("revision"),
            "target_revision": (tgt_manifest.get("project") or {}).get("revision"),
            "objects": len(src_obj),
            "relations": len(src_rel),
            "sources": len(src_sources),
            "legacy_relation_equivalence": LEGACY_RELATION_EQUIVALENCE,
            "checks": checks,
            "passed": all(checks.values()),
        },
    }
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifiera semantisk v1→v2-migration end-to-end.")
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    ap.add_argument("--skip-documents", action="store_true")
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[1]
    try:
        report = verify(repo, args.source.resolve(), args.target.resolve(), not args.skip_documents)
        text = yaml.safe_dump(report, allow_unicode=True, sort_keys=False)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0 if report["verification"]["passed"] else 1
    except Exception as exc:
        print(f"ERROR MIG-VERIFY: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
