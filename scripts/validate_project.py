#!/usr/bin/env python3
"""Structural validator for EA Stödjare projects.

Validates canonical YAML, IDs, provenance/source references, relation semantics,
project manifest/integrity, required file structure and (when present)
deterministic generated Markdown/Confluence artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    path: str | None = None

    def format(self) -> str:
        loc = f" [{self.path}]" if self.path else ""
        return f"{self.severity.upper()} {self.code}{loc}: {self.message}"


class ValidationContext:
    def __init__(self) -> None:
        self.findings: list[Finding] = []

    def error(self, code: str, message: str, path: Path | str | None = None) -> None:
        self.findings.append(Finding(code, "error", message, str(path) if path else None))

    def warning(self, code: str, message: str, path: Path | str | None = None) -> None:
        self.findings.append(Finding(code, "warning", message, str(path) if path else None))

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == "warning"]


def load_yaml(path: Path, ctx: ValidationContext) -> Any | None:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    except Exception as exc:  # yaml parser emits several exception types
        ctx.error("STR-YAML-001", f"YAML kan inte parsas: {exc}", path)
        return None


def load_json(path: Path, ctx: ValidationContext) -> Any | None:
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        ctx.error("STR-JSON-001", f"JSON kan inte parsas: {exc}", path)
        return None


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_manifest(project_root: Path, repo_root: Path, ctx: ValidationContext) -> dict[str, Any] | None:
    manifest_path = project_root / "project-manifest.json"
    schema_path = repo_root / "schemas" / "project-manifest.schema.json"
    if not manifest_path.is_file():
        ctx.error("STR-MAN-001", "project-manifest.json saknas.", manifest_path)
        return None
    manifest = load_json(manifest_path, ctx)
    schema = load_json(schema_path, ctx) if schema_path.is_file() else None
    if manifest is None:
        return None
    if schema is None:
        ctx.error("STR-MAN-002", "Manifestets JSON Schema saknas eller kan inte läsas.", schema_path)
    else:
        validator = Draft202012Validator(schema)
        errors = sorted(validator.iter_errors(manifest), key=lambda e: list(e.path))
        for err in errors:
            ptr = "/".join(str(x) for x in err.path) or "<root>"
            ctx.error("STR-MAN-003", f"Manifestet bryter mot schema vid {ptr}: {err.message}", manifest_path)

    files = manifest.get("files") if isinstance(manifest, dict) else None
    if not isinstance(files, list):
        return manifest

    listed_paths: set[str] = set()
    previous = None
    for i, entry in enumerate(files):
        if not isinstance(entry, dict):
            ctx.error("STR-MAN-004", f"files[{i}] är inte ett objekt.", manifest_path)
            continue
        rel = entry.get("path")
        if not isinstance(rel, str):
            continue
        if rel in listed_paths:
            ctx.error("STR-MAN-005", f"Dubblett i manifestinventering: {rel}", manifest_path)
        listed_paths.add(rel)
        if previous is not None and rel < previous:
            ctx.error("STR-MAN-006", "Manifestets filinventering är inte sorterad i stigande sökvägsordning.", manifest_path)
        previous = rel
        target = project_root / rel
        required = bool(entry.get("required"))
        if not target.is_file():
            if required:
                ctx.error("STR-MAN-007", f"Obligatorisk manifestfil saknas: {rel}", target)
            else:
                ctx.warning("STR-MAN-008", f"Valfri manifestfil saknas: {rel}", target)
            continue
        expected = entry.get("sha256")
        if isinstance(expected, str):
            actual = sha256(target)
            if actual != expected:
                ctx.error("STR-MAN-009", f"SHA-256 stämmer inte. Förväntad {expected}, faktisk {actual}.", target)

    model = as_mapping(manifest.get("model"))
    model_root = model.get("root", "model")
    if not isinstance(model_root, str) or not (project_root / model_root).is_dir():
        ctx.error("STR-MAN-010", f"Kanonisk modellkatalog saknas: {model_root}", project_root / str(model_root))

    return manifest


def load_domain_specs(repo_root: Path, ctx: ValidationContext) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    paths = {
        "format": repo_root / "schemas" / "model-format.yaml",
        "types": repo_root / "schemas" / "object-types.yaml",
        "relations": repo_root / "schemas" / "relations.yaml",
        "provenance": repo_root / "schemas" / "provenance.yaml",
    }
    loaded: dict[str, Any] = {}
    for name, path in paths.items():
        if not path.is_file():
            ctx.error("STR-SCHEMA-001", f"Nödvändig schemaspecifikation saknas: {path.name}", path)
            loaded[name] = {}
        else:
            loaded[name] = load_yaml(path, ctx) or {}
    return loaded["format"], loaded["types"], loaded["relations"], loaded["provenance"]


def validate_source(source: Any, source_ids: set[str], source_types: set[str], ctx: ValidationContext, path: Path) -> None:
    if not isinstance(source, dict):
        ctx.error("STR-SRC-001", "Källpost måste vara ett objekt.", path)
        return
    for field in ("id", "title", "source_type"):
        if not source.get(field):
            ctx.error("STR-SRC-002", f"Källpost saknar obligatoriskt fält: {field}", path)
    sid = source.get("id")
    if isinstance(sid, str):
        if not re.fullmatch(r"SRC-(?:EXT-)?[0-9]{3,}", sid):
            ctx.error("STR-SRC-003", f"Ogiltigt source-id: {sid}", path)
        if sid in source_ids:
            ctx.error("STR-ID-001", f"Dubblett-ID: {sid}", path)
        source_ids.add(sid)
    st = source.get("source_type")
    if st and st not in source_types:
        ctx.error("STR-SRC-004", f"Okänd source_type: {st}", path)


def validate_provenance(
    entries: Any,
    owner_id: str,
    source_map: dict[str, dict[str, Any]],
    object_ids: set[str],
    evidence_types: dict[str, Any],
    confidence_values: set[str],
    transferability_values: set[str],
    external_source_types: set[str],
    ctx: ValidationContext,
    path: Path,
) -> None:
    if not isinstance(entries, list) or not entries:
        ctx.error("STR-PROV-001", f"{owner_id} måste ha minst en provenienspost.", path)
        return
    for i, entry in enumerate(entries):
        label = f"{owner_id}.provenance[{i}]"
        if not isinstance(entry, dict):
            ctx.error("STR-PROV-002", f"{label} måste vara ett objekt.", path)
            continue
        et = entry.get("evidence_type")
        if et not in evidence_types:
            ctx.error("STR-PROV-003", f"{label} har okänd evidence_type: {et}", path)
            continue
        semantics = as_mapping(evidence_types[et])
        sid = entry.get("source_id")
        derived_from = entry.get("derived_from")
        rationale = entry.get("rationale")
        if semantics.get("source_required") and not sid:
            ctx.error("STR-PROV-004", f"{label} kräver source_id.", path)
        if semantics.get("source_or_derived_from_required") and not sid and not derived_from:
            ctx.error("STR-PROV-005", f"{label} kräver source_id eller derived_from.", path)
        if semantics.get("rationale_required") and not rationale:
            ctx.error("STR-PROV-006", f"{label} kräver rationale.", path)
        if sid:
            if sid not in source_map:
                ctx.error("STR-PROV-007", f"{label} refererar okänd källa: {sid}", path)
            elif et == "external" and source_map[sid].get("source_type") not in external_source_types:
                ctx.error("STR-PROV-008", f"Extern evidens {label} använder inte en extern källtyp: {sid}", path)
        if derived_from is not None:
            if not isinstance(derived_from, list) or not derived_from:
                ctx.error("STR-PROV-009", f"{label}.derived_from måste vara en icke-tom lista.", path)
            else:
                for ref in derived_from:
                    if ref not in object_ids:
                        ctx.error("STR-PROV-010", f"{label} refererar okänt objekt i derived_from: {ref}", path)
        confidence = entry.get("confidence")
        if confidence is not None and confidence not in confidence_values:
            ctx.error("STR-PROV-011", f"{label} har ogiltigt confidence: {confidence}", path)
        trans = entry.get("transferability")
        if trans is not None:
            if trans not in transferability_values:
                ctx.error("STR-PROV-012", f"{label} har ogiltig transferability: {trans}", path)
            if et != "external":
                ctx.error("STR-PROV-013", f"{label} får bara ange transferability för external evidens.", path)


def validate_model(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    format_spec, type_spec, rel_spec, prov_spec = load_domain_specs(repo_root, ctx)
    file_structure = as_mapping(format_spec.get("file_structure"))
    object_files = as_mapping(file_structure.get("object_files"))
    special_files = as_mapping(file_structure.get("special_files"))
    object_types = as_mapping(type_spec.get("object_types"))
    statuses = set(as_list(as_mapping(type_spec.get("common")).get("statuses")))
    model_root_name = "model"
    if manifest:
        model_root_name = as_mapping(manifest.get("model")).get("root", "model")
    model_root = project_root / str(model_root_name)
    if not model_root.is_dir():
        return

    # Required canonical files and no unexpected YAML files in canonical model root.
    expected_files = set(object_files) | set(special_files)
    for name in sorted(expected_files):
        if not (model_root / name).is_file():
            ctx.error("STR-MODEL-001", f"Kanonisk modellfil saknas: {name}", model_root / name)
    for path in sorted(model_root.glob("*.yaml")):
        if path.name not in expected_files:
            ctx.warning("STR-MODEL-002", f"Okänd YAML-fil i kanonisk modellkatalog: {path.name}", path)

    parsed_objects: list[tuple[dict[str, Any], Path, str]] = []
    object_ids: set[str] = set()
    # First pass: envelopes, types, IDs, common fields.
    for filename, expected_type in object_files.items():
        path = model_root / filename
        if not path.is_file():
            continue
        data = load_yaml(path, ctx)
        if not isinstance(data, dict):
            ctx.error("STR-MODEL-003", "Objektfilens toppnivå måste vara ett objekt.", path)
            continue
        if data.get("schema_version") != "1.0":
            ctx.error("STR-MODEL-004", f"Ogiltig schema_version: {data.get('schema_version')!r}", path)
        if data.get("object_type") != expected_type:
            ctx.error("STR-MODEL-005", f"object_type ska vara {expected_type}, fick {data.get('object_type')!r}", path)
        objects = data.get("objects")
        if not isinstance(objects, list):
            ctx.error("STR-MODEL-006", "objects måste vara en lista.", path)
            continue
        spec = as_mapping(object_types.get(expected_type))
        prefix = spec.get("id_prefix")
        extra_required = set(as_list(spec.get("required_attributes")))
        for idx, obj in enumerate(objects):
            if not isinstance(obj, dict):
                ctx.error("STR-MODEL-007", f"objects[{idx}] måste vara ett objekt.", path)
                continue
            oid = obj.get("id")
            for field in ("id", "type", "name", "description", "status", "provenance"):
                if field not in obj or obj.get(field) in (None, ""):
                    ctx.error("STR-MODEL-008", f"Objekt {oid or idx} saknar obligatoriskt fält: {field}", path)
            for field in extra_required:
                if field not in obj or obj.get(field) in (None, ""):
                    ctx.error("STR-MODEL-009", f"Objekt {oid or idx} saknar typspecifikt obligatoriskt fält: {field}", path)
            if obj.get("type") != expected_type:
                ctx.error("STR-MODEL-010", f"Objekt {oid or idx} har type {obj.get('type')!r}, ska vara {expected_type}.", path)
            if isinstance(oid, str):
                if prefix and not oid.startswith(str(prefix)):
                    ctx.error("STR-ID-002", f"ID {oid} har fel prefix; förväntar {prefix}", path)
                if not re.fullmatch(r"[A-Z]+-[0-9]{3,}", oid):
                    ctx.error("STR-ID-003", f"ID {oid} följer inte stabilt ID-format.", path)
                if oid in object_ids:
                    ctx.error("STR-ID-001", f"Dubblett-ID: {oid}", path)
                object_ids.add(oid)
            status = obj.get("status")
            if status not in statuses:
                ctx.error("STR-MODEL-011", f"Objekt {oid or idx} har ogiltig status: {status}", path)
            if expected_type == "capability" and obj.get("capability_type") not in {"business", "it"}:
                ctx.error("STR-MODEL-012", f"Förmåga {oid or idx} måste ha capability_type business eller it.", path)
            functions = obj.get("functions")
            supports_functions = bool(spec.get("supports_functions"))
            if functions is not None:
                if not supports_functions:
                    ctx.error("STR-MODEL-013", f"Objekttyp {expected_type} får inte ha functions i v1.", path)
                elif not isinstance(functions, list):
                    ctx.error("STR-MODEL-014", f"{oid}.functions måste vara en lista.", path)
                else:
                    for fi, fn in enumerate(functions):
                        if not isinstance(fn, dict) or not fn.get("name"):
                            ctx.error("STR-MODEL-015", f"{oid}.functions[{fi}] måste vara ett objekt med name.", path)
                        if isinstance(fn, dict) and "id" in fn:
                            ctx.error("STR-MODEL-016", f"{oid}.functions[{fi}] får inte ha globalt id i v1.", path)
            parsed_objects.append((obj, path, expected_type))

    # Sources.
    source_path = model_root / "sources.yaml"
    source_ids: set[str] = set()
    source_map: dict[str, dict[str, Any]] = {}
    source_types_spec = as_mapping(prov_spec.get("source_types"))
    if source_path.is_file():
        data = load_yaml(source_path, ctx)
        if isinstance(data, dict):
            if data.get("schema_version") != "1.0":
                ctx.error("STR-SRC-005", "sources.yaml måste ha schema_version '1.0'.", source_path)
            sources = data.get("sources")
            if not isinstance(sources, list):
                ctx.error("STR-SRC-006", "sources måste vara en lista.", source_path)
            else:
                for src in sources:
                    validate_source(src, source_ids, set(source_types_spec), ctx, source_path)
                    if isinstance(src, dict) and isinstance(src.get("id"), str):
                        source_map[src["id"]] = src

    # Provenance for objects now that all object IDs and sources are known.
    evidence_types = as_mapping(prov_spec.get("evidence_types"))
    confidence_values = set(as_mapping(prov_spec.get("confidence_values")))
    transferability_values = set(as_mapping(prov_spec.get("transferability_values")))
    external_source_types = {k for k, v in source_types_spec.items() if isinstance(v, dict) and v.get("external") is True}
    for obj, path, _ in parsed_objects:
        validate_provenance(obj.get("provenance"), str(obj.get("id", "<unknown>")), source_map, object_ids,
                            evidence_types, confidence_values, transferability_values, external_source_types, ctx, path)
        # Proposed object should normally be candidate.
        if obj.get("status") != "candidate":
            if any(isinstance(p, dict) and p.get("evidence_type") == "proposed" for p in as_list(obj.get("provenance"))):
                ctx.warning("STR-PROV-014", f"Föreslaget objekt {obj.get('id')} är inte candidate.", path)

    # Relations.
    rel_path = model_root / "relations.yaml"
    relation_types = as_mapping(rel_spec.get("relation_types"))
    if rel_path.is_file():
        data = load_yaml(rel_path, ctx)
        if isinstance(data, dict):
            if data.get("schema_version") != "1.0":
                ctx.error("STR-REL-001", "relations.yaml måste ha schema_version '1.0'.", rel_path)
            relations = data.get("relations")
            if not isinstance(relations, list):
                ctx.error("STR-REL-002", "relations måste vara en lista.", rel_path)
            else:
                relation_ids: set[str] = set()
                exact: set[tuple[str, str, str]] = set()
                object_type_by_id = {obj["id"]: typ for obj, _, typ in parsed_objects if isinstance(obj.get("id"), str)}
                object_by_id = {obj["id"]: obj for obj, _, _ in parsed_objects if isinstance(obj.get("id"), str)}
                for i, rel in enumerate(relations):
                    if not isinstance(rel, dict):
                        ctx.error("STR-REL-003", f"relations[{i}] måste vara ett objekt.", rel_path)
                        continue
                    rid = rel.get("id")
                    for field in ("id", "type", "source", "target", "status", "provenance"):
                        if field not in rel or rel.get(field) in (None, ""):
                            ctx.error("STR-REL-004", f"Relation {rid or i} saknar fält: {field}", rel_path)
                    if isinstance(rid, str):
                        if not re.fullmatch(r"REL-[0-9]{3,}", rid):
                            ctx.error("STR-REL-005", f"Ogiltigt relations-ID: {rid}", rel_path)
                        if rid in relation_ids or rid in object_ids or rid in source_ids:
                            ctx.error("STR-ID-001", f"Dubblett globalt ID: {rid}", rel_path)
                        relation_ids.add(rid)
                    status = rel.get("status")
                    if status not in statuses:
                        ctx.error("STR-REL-006", f"Relation {rid or i} har ogiltig status: {status}", rel_path)
                    rtype = rel.get("type")
                    src, tgt = rel.get("source"), rel.get("target")
                    if src not in object_ids:
                        ctx.error("STR-REL-007", f"Relation {rid or i} har okänd source: {src}", rel_path)
                    if tgt not in object_ids:
                        ctx.error("STR-REL-008", f"Relation {rid or i} har okänd target: {tgt}", rel_path)
                    spec = as_mapping(relation_types.get(rtype))
                    if not spec:
                        ctx.error("STR-REL-009", f"Relation {rid or i} har okänd relationstyp: {rtype}", rel_path)
                    elif src in object_type_by_id and tgt in object_type_by_id:
                        if not relation_allowed(spec, object_type_by_id[src], object_type_by_id[tgt], object_by_id[tgt]):
                            ctx.error("STR-REL-010", f"Otillåten kombination för {rtype}: {object_type_by_id[src]} -> {object_type_by_id[tgt]}", rel_path)
                        if src == tgt and spec.get("self_reference_allowed") is False:
                            ctx.error("STR-REL-011", f"Självrelation är inte tillåten för {rtype}: {src}", rel_path)
                    key = (str(rtype), str(src), str(tgt))
                    if key in exact:
                        ctx.error("STR-REL-012", f"Exakt dubblettrelation: {rtype} {src}->{tgt}", rel_path)
                    exact.add(key)
                    validate_provenance(rel.get("provenance"), str(rid or f"relation-{i}"), source_map, object_ids,
                                        evidence_types, confidence_values, transferability_values, external_source_types, ctx, rel_path)


def relation_allowed(spec: dict[str, Any], source_type: str, target_type: str, target_obj: dict[str, Any]) -> bool:
    allowed = as_list(spec.get("allowed"))
    for rule in allowed:
        if not isinstance(rule, dict):
            continue
        src = rule.get("source")
        targets = as_list(rule.get("targets"))
        if src not in ("*", source_type):
            continue
        if "*" not in targets and target_type not in targets:
            continue
        constraints = as_mapping(rule.get("target_constraints"))
        if any(target_obj.get(k) != v for k, v in constraints.items()):
            continue
        return True
    return False


def compare_tree(expected: Path, actual: Path, ctx: ValidationContext, code: str, label: str) -> None:
    expected_files = {p.relative_to(expected) for p in expected.rglob("*") if p.is_file()} if expected.is_dir() else set()
    actual_files = {p.relative_to(actual) for p in actual.rglob("*") if p.is_file()} if actual.is_dir() else set()
    if expected_files != actual_files:
        missing = sorted(str(p) for p in actual_files - expected_files)
        extra = sorted(str(p) for p in expected_files - actual_files)
        if missing:
            ctx.error(code, f"{label}: lagrade artefakter saknar filer som generatorn producerar: {missing}", expected)
        if extra:
            ctx.error(code, f"{label}: lagrade artefakter innehåller oväntade filer: {extra}", expected)
        return
    for rel in sorted(expected_files):
        if (expected / rel).read_bytes() != (actual / rel).read_bytes():
            ctx.error(code, f"{label}: artefakt är inaktuell eller manuellt ändrad: {rel}", expected / rel)


def validate_generated(project_root: Path, repo_root: Path, ctx: ValidationContext) -> None:
    """Validate deterministic generated text artifacts when they exist.

    Binary DOCX/PDF outputs are checked for basic signatures only; deterministic
    regeneration is covered by the dedicated generation regression tests.
    """
    md_dir = project_root / "docs" / "generated"
    conf_dir = project_root / "exports" / "confluence"
    py = sys.executable
    if md_dir.is_dir() and (repo_root / "scripts/generate_markdown.py").is_file():
        with tempfile.TemporaryDirectory(prefix="ea-validate-md-") as tmp:
            out = Path(tmp) / "out"
            subprocess.run([py, str(repo_root / "scripts/generate_markdown.py"), "--project-root", str(project_root), "--mode", "working", "--output-dir", str(out)], check=True, capture_output=True, text=True)
            compare_tree(md_dir, out, ctx, "STR-GEN-001", "Markdown")
    if conf_dir.is_dir() and (repo_root / "scripts/generate_confluence.py").is_file():
        with tempfile.TemporaryDirectory(prefix="ea-validate-conf-") as tmp:
            out = Path(tmp) / "out"
            subprocess.run([py, str(repo_root / "scripts/generate_confluence.py"), "--project-root", str(project_root), "--mode", "working", "--output-dir", str(out)], check=True, capture_output=True, text=True)
            compare_tree(conf_dir, out, ctx, "STR-GEN-002", "Confluence")

    doc_dir = project_root / "exports" / "document"
    if doc_dir.is_dir():
        for path in sorted(doc_dir.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() == ".pdf":
                if not path.read_bytes().startswith(b"%PDF-"):
                    ctx.error("STR-GEN-003", "PDF saknar giltig PDF-signatur.", path)
            elif path.suffix.lower() == ".docx":
                if not path.read_bytes().startswith(b"PK"):
                    ctx.error("STR-GEN-004", "DOCX saknar giltig ZIP/OOXML-signatur.", path)


def validate_project(project_root: Path, repo_root: Path, check_generated: bool = True) -> ValidationContext:
    ctx = ValidationContext()
    if not project_root.is_dir():
        ctx.error("STR-PROJ-001", "Projektkatalogen finns inte.", project_root)
        return ctx
    manifest = validate_manifest(project_root, repo_root, ctx)
    validate_model(project_root, repo_root, manifest, ctx)
    if check_generated:
        try:
            validate_generated(project_root, repo_root, ctx)
        except subprocess.CalledProcessError as exc:
            ctx.error("STR-GEN-005", f"Generator kunde inte köras: {exc.stderr or exc}")
    return ctx


def main() -> int:
    parser = argparse.ArgumentParser(description="Validera strukturen i ett EA Stödjare-projekt.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Projektrot som ska valideras.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="EA Stödjare-reporot med schemas/scripts.")
    parser.add_argument("--no-generated", action="store_true", help="Hoppa över kontroll av genererade artefakter.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Skriv resultat som JSON.")
    args = parser.parse_args()

    ctx = validate_project(args.project_root.resolve(), args.repo_root.resolve(), check_generated=not args.no_generated)
    if args.json_output:
        print(json.dumps({
            "valid": not ctx.errors,
            "errors": [f.__dict__ for f in ctx.errors],
            "warnings": [f.__dict__ for f in ctx.warnings],
        }, ensure_ascii=False, indent=2))
    else:
        for finding in ctx.findings:
            print(finding.format())
        print(f"Validering: {'GODKÄND' if not ctx.errors else 'UNDERKÄND'} ({len(ctx.errors)} fel, {len(ctx.warnings)} varningar)")
    return 0 if not ctx.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
