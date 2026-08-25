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

from resolve_project_metamodel import resolve as resolve_project_metamodel, ExtensionResolutionError
from detect_project_profile import detect as detect_project_profile


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
        self.profile: dict[str, Any] | None = None
        self.stages: list[dict[str, Any]] = []

    def stage(self, name: str, status: str, detail: str | None = None) -> None:
        row: dict[str, Any] = {"name": name, "status": status}
        if detail:
            row["detail"] = detail
        self.stages.append(row)

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


def load_domain_specs(repo_root: Path, ctx: ValidationContext, manifest: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    # Compatibility safeguard during v2 evolution: a legacy v1 project must be
    # validated with the frozen v1 semantic snapshots, not with the evolving
    # native-v2 schemas. Full project-metamodel-driven validation is introduced
    # later in the v2 plan.
    model_meta = as_mapping((manifest or {}).get("model"))
    legacy_v1 = str(model_meta.get("metamodel_version", "")) == "1.0"
    base = repo_root / "compatibility" / "ea-stodjare-v1" / "schemas" if legacy_v1 else repo_root / "schemas"
    paths = {
        "format": base / "model-format.yaml",
        "types": base / "object-types.yaml",
        "relations": base / "relations.yaml",
        "provenance": base / "provenance.yaml",
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


def apply_project_metamodel(project_root: Path, repo_root: Path, format_spec: dict[str, Any], type_spec: dict[str, Any], rel_spec: dict[str, Any], ctx: ValidationContext) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Overlay native-v2 project metamodel + extensions on standard domain specs."""
    pm_path = project_root / "project-metamodel.yaml"
    if not pm_path.is_file():
        return format_spec, type_spec, rel_spec
    try:
        resolved = resolve_project_metamodel(pm_path, repo_root)
    except (ExtensionResolutionError, OSError, ValueError, yaml.YAMLError) as exc:
        ctx.error("STR-META-001", f"Projektmetamodellen kan inte resolveras: {exc}", pm_path)
        return format_spec, type_spec, rel_spec
    pm = as_mapping(resolved.get("project_metamodel"))
    if as_mapping(pm.get("base_profile")).get("compatibility_mode") not in {"native", "custom"}:
        return format_spec, type_spec, rel_spec

    enabled_types = set(as_list(as_mapping(pm.get("object_types")).get("enabled")))
    custom_types = as_list(as_mapping(pm.get("object_types")).get("custom"))
    enabled_types.update(str(x.get("type")) for x in custom_types if isinstance(x, dict) and x.get("type"))
    enabled_relations = set(as_list(as_mapping(pm.get("relations")).get("enabled")))
    custom_relations = as_list(as_mapping(pm.get("relations")).get("custom"))
    enabled_relations.update(str(x.get("type")) for x in custom_relations if isinstance(x, dict) and x.get("type"))

    # File requirements follow active types. Disabled standard types are not gaps.
    fs = as_mapping(format_spec.get("file_structure"))
    obj_files = as_mapping(fs.get("object_files"))
    filtered = {fn: typ for fn, typ in obj_files.items() if typ in enabled_types}
    for obj in custom_types:
        if not isinstance(obj, dict) or not obj.get("type"):
            continue
        typ = str(obj["type"])
        filename = str(obj.get("model_file") or (typ.replace("_", "-") + "s.yaml"))
        filtered[filename] = typ
    fs["object_files"] = filtered
    format_spec["file_structure"] = fs

    # Active object catalog = selected core + project/extension custom types.
    catalog = as_mapping(type_spec.get("object_types"))
    catalog = {k: v for k, v in catalog.items() if k in enabled_types}
    common_statuses = set(as_list(as_mapping(type_spec.get("common")).get("statuses")))
    for obj in custom_types:
        if not isinstance(obj, dict) or not obj.get("type"):
            continue
        required=[]; optional=[]
        for attr in as_list(obj.get("attributes")):
            if isinstance(attr, dict) and attr.get("name"):
                (required if attr.get("required") else optional).append(attr["name"])
        spec={"display_name": obj.get("display_name", obj["type"]), "definition": obj.get("definition", ""), "id_prefix": obj.get("id_prefix"), "required_attributes": required, "optional_attributes": optional}
        catalog[str(obj["type"])]=spec
        common_statuses.update(str(x) for x in as_list(obj.get("status_values")))
    # Attribute extensions affect required/optional structural fields.
    for ext in as_list(pm.get("attribute_extensions")):
        if not isinstance(ext, dict): continue
        target=str(ext.get("object_type", "")); spec=as_mapping(catalog.get(target))
        if not spec: continue
        req=list(as_list(spec.get("required_attributes"))); opt=list(as_list(spec.get("optional_attributes")))
        for attr in as_list(ext.get("attributes")):
            if not isinstance(attr,dict) or not attr.get("name"): continue
            bucket=req if attr.get("required") else opt
            if attr["name"] not in bucket: bucket.append(attr["name"])
        spec["required_attributes"]=req; spec["optional_attributes"]=opt; catalog[target]=spec
    type_spec["object_types"]=catalog
    type_spec.setdefault("common", {})["statuses"] = sorted(common_statuses)

    # Active relation catalog = selected core + custom relations.
    rcatalog = {k: v for k, v in as_mapping(rel_spec.get("relation_types")).items() if k in enabled_relations}
    for rel in custom_relations:
        if not isinstance(rel, dict) or not rel.get("type"): continue
        allowed=[]
        for ep in as_list(rel.get("endpoints")):
            if not isinstance(ep,dict): continue
            for src in as_list(ep.get("source")):
                allowed.append({"source": src, "targets": list(as_list(ep.get("target")))})
        rcatalog[str(rel["type"])]={"display_name": rel.get("display_name", rel["type"]), "definition": rel.get("definition", ""), "allowed": allowed, "qualifiers": {}}
    rel_spec["relation_types"]=rcatalog
    return format_spec, type_spec, rel_spec


def validate_model(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    format_spec, type_spec, rel_spec, prov_spec = load_domain_specs(repo_root, ctx, manifest)
    # Native v2 projects may select a subset of the standard model and enable extensions.
    if str(as_mapping((manifest or {}).get("model")).get("metamodel_version", "")) != "1.0":
        format_spec, type_spec, rel_spec = apply_project_metamodel(project_root, repo_root, format_spec, type_spec, rel_spec, ctx)
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
            allowed_values = as_mapping(spec.get("allowed_values"))
            for field, allowed in allowed_values.items():
                if field in obj and obj.get(field) is not None and obj.get(field) not in set(as_list(allowed)):
                    ctx.error("STR-MODEL-017", f"Objekt {oid or idx} har ogiltigt värde för {field}: {obj.get(field)!r}", path)
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
            function_spec = as_mapping(format_spec.get("function_instance"))
            function_rules = set(as_list(function_spec.get("rules")))
            legacy_function_semantics = "function_has_no_global_id_in_v1" in function_rules
            if functions is not None:
                if not supports_functions:
                    ctx.error("STR-MODEL-013", f"Objekttyp {expected_type} får inte ha functions.", path)
                elif not isinstance(functions, list):
                    ctx.error("STR-MODEL-014", f"{oid}.functions måste vara en lista.", path)
                else:
                    local_function_ids: set[str] = set()
                    local_id_pattern = function_spec.get("id_pattern") or r"^[A-Za-z][A-Za-z0-9._-]{0,63}$"
                    for fi, fn in enumerate(functions):
                        if not isinstance(fn, dict) or not fn.get("name"):
                            ctx.error("STR-MODEL-015", f"{oid}.functions[{fi}] måste vara ett objekt med name.", path)
                            continue
                        fid = fn.get("id")
                        if legacy_function_semantics and fid is not None:
                            ctx.error("STR-MODEL-016", f"{oid}.functions[{fi}] får inte ha id i legacy v1.", path)
                        elif fid is not None:
                            if not isinstance(fid, str) or not re.fullmatch(str(local_id_pattern), fid):
                                ctx.error("STR-FUN-001", f"{oid}.functions[{fi}].id har ogiltigt lokalt format: {fid!r}", path)
                            elif fid in local_function_ids:
                                ctx.error("STR-FUN-003", f"Dubblett lokalt funktions-ID inom {oid}: {fid}", path)
                            else:
                                local_function_ids.add(fid)
                        req = fn.get("required")
                        if req is not None and not isinstance(req, bool):
                            ctx.error("STR-FUN-002", f"{oid}.functions[{fi}].required måste vara boolean.", path)
                        allowed_function_fields = set(as_list(function_spec.get("required_fields"))) | set(as_list(function_spec.get("optional_fields")))
                        unknown_function_fields = sorted(set(fn) - allowed_function_fields)
                        if unknown_function_fields:
                            ctx.warning("STR-FUN-004", f"{oid}.functions[{fi}] har okända funktionsfält: {', '.join(unknown_function_fields)}", path)
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
                    # v2 relation qualifiers. Definitions are global; applicability is relation-specific.
                    qualifiers = as_mapping(spec.get("qualifiers")) if spec else {}
                    qualifier_defs = as_mapping(rel_spec.get("qualifier_definitions"))
                    known_qualifier_names = set(qualifier_defs)
                    for qname in known_qualifier_names:
                        if qname in rel and qname not in qualifiers:
                            ctx.error("STR-REL-016", f"Relation {rid or i} ({rtype}) använder otillåten kvalificerare: {qname}", rel_path)
                    for qname, qspec_raw in qualifiers.items():
                        qspec = as_mapping(qspec_raw)
                        qdef = dict(as_mapping(qualifier_defs.get(qname)))
                        for _k in ("type", "allowed_values", "extensible_by_project"):
                            if _k in qspec:
                                qdef[_k] = qspec[_k]
                        qval = rel.get(qname)
                        if qspec.get("required") and qval in (None, ""):
                            ctx.error("STR-REL-013", f"Relation {rid or i} ({rtype}) saknar obligatorisk kvalificerare: {qname}", rel_path)
                        if qval not in (None, ""):
                            qtype = qdef.get("type")
                            type_ok = True
                            if qtype == "boolean": type_ok = isinstance(qval, bool)
                            elif qtype == "string": type_ok = isinstance(qval, str)
                            elif qtype == "string_or_list": type_ok = isinstance(qval, str) or (isinstance(qval, list) and all(isinstance(x, str) for x in qval))
                            elif qtype == "enum": type_ok = isinstance(qval, str)
                            if not type_ok:
                                ctx.error("STR-REL-017", f"Relation {rid or i} har fel datatyp för {qname}: {qval!r}", rel_path)
                            allowed_values = set(as_list(qdef.get("allowed_values")))
                            if allowed_values and qval not in allowed_values:
                                if not qdef.get("extensible_by_project"):
                                    ctx.error("STR-REL-014", f"Relation {rid or i} har ogiltigt {qname}: {qval}", rel_path)
                    if rtype == "can_realize":
                        prov_entries = [x for x in as_list(rel.get("provenance")) if isinstance(x, dict)]
                        source_backed = any(x.get("evidence_type") in {"explicit", "external", "derived"} for x in prov_entries)
                        if not source_backed:
                            ctx.error("STR-REL-015", f"Relation {rid or i} can_realize kräver källstödd evidens; proposed-only räcker inte.", rel_path)



def validate_information_layers(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    """Validate the v2 epistemic layer envelopes and core separation guards."""
    layers_cfg = as_mapping((manifest or {}).get("information_layers"))
    if not layers_cfg:
        return
    spec_path = repo_root / "schemas" / "information-layers.yaml"
    spec = load_yaml(spec_path, ctx) if spec_path.is_file() else None
    if not isinstance(spec, dict):
        ctx.error("STR-LAYER-001", "Informationslagerspecifikation saknas eller kan inte läsas.", spec_path)
        return

    conceptual = project_root / str(layers_cfg.get("conceptual", "model"))
    market_dir = project_root / str(layers_cfg.get("market_reference", "market-reference"))
    actual_dir = project_root / str(layers_cfg.get("actual_state", "actual-state"))
    for label, path in (("conceptual", conceptual), ("market_reference", market_dir), ("actual_state", actual_dir)):
        if not path.is_dir():
            ctx.error("STR-LAYER-002", f"Informationslager saknas: {label}", path)

    object_ids: set[str] = set()
    id_types: dict[str, str] = {}
    if conceptual.is_dir():
        for path in conceptual.glob("*.yaml"):
            data = load_yaml(path, ctx)
            if isinstance(data, dict) and isinstance(data.get("objects"), list):
                for obj in data["objects"]:
                    if isinstance(obj, dict) and isinstance(obj.get("id"), str):
                        object_ids.add(obj["id"]); id_types[obj["id"]] = str(obj.get("type", ""))
    source_ids: set[str] = set()
    sp = conceptual / "sources.yaml"
    if sp.is_file():
        data = load_yaml(sp, ctx)
        if isinstance(data, dict):
            source_ids = {str(x.get("id")) for x in as_list(data.get("sources")) if isinstance(x, dict) and x.get("id")}

    def provenance_types(entries: Any, owner: str, path: Path) -> set[str]:
        if not isinstance(entries, list) or not entries:
            ctx.error("STR-LAYER-003", f"{owner} måste ha minst en provenienspost.", path); return set()
        types: set[str] = set()
        for i, row in enumerate(entries):
            if not isinstance(row, dict):
                ctx.error("STR-LAYER-004", f"{owner}.provenance[{i}] måste vara ett objekt.", path); continue
            et = row.get("evidence_type")
            if isinstance(et, str): types.add(et)
            sid = row.get("source_id")
            if sid and sid not in source_ids:
                ctx.error("STR-LAYER-005", f"{owner} refererar okänd källa: {sid}", path)
        return types

    market_path = market_dir / "assertions.yaml"
    if market_path.is_file():
        data = load_yaml(market_path, ctx)
        mspec = as_mapping(spec.get("market_reference_assertion"))
        allowed = set(as_list(mspec.get("assertion_types")))
        pattern = str(mspec.get("id_pattern", r"^MKT-[0-9]{3,}$"))
        if not isinstance(data, dict) or data.get("schema_version") != "1.0" or data.get("layer") != "market_reference" or not isinstance(data.get("assertions"), list):
            ctx.error("STR-LAYER-006", "market-reference/assertions.yaml har ogiltigt envelope.", market_path)
        else:
            seen: set[str] = set()
            for i, row in enumerate(data["assertions"]):
                if not isinstance(row, dict): ctx.error("STR-LAYER-007", f"Market assertion {i} måste vara objekt.", market_path); continue
                rid = row.get("id")
                for field in as_list(mspec.get("required_fields")):
                    if row.get(field) in (None, "", []): ctx.error("STR-LAYER-008", f"Market assertion {rid or i} saknar {field}.", market_path)
                if not isinstance(rid, str) or not re.fullmatch(pattern, rid): ctx.error("STR-LAYER-009", f"Ogiltigt market assertion-id: {rid}", market_path)
                elif rid in seen: ctx.error("STR-LAYER-010", f"Dubblett market assertion-id: {rid}", market_path)
                else: seen.add(rid)
                if row.get("assertion_type") not in allowed: ctx.error("STR-LAYER-011", f"Okänd market assertion_type: {row.get('assertion_type')}", market_path)
                subject = row.get("subject")
                if subject not in object_ids: ctx.error("STR-LAYER-012", f"Market assertion refererar okänt subject: {subject}", market_path)
                ets = provenance_types(row.get("provenance"), str(rid or i), market_path)
                if not ets.intersection({"explicit", "external", "derived"}): ctx.error("STR-LAYER-013", f"{rid or i} saknar källstödd marknadsevidens.", market_path)

    actual_path = actual_dir / "assertions.yaml"
    if actual_path.is_file():
        data = load_yaml(actual_path, ctx)
        aspec = as_mapping(spec.get("actual_state_assertion"))
        allowed = set(as_list(aspec.get("assertion_types"))); statuses=set(as_list(aspec.get("status_values")))
        pattern = str(aspec.get("id_pattern", r"^ACT-[0-9]{3,}$"))
        if not isinstance(data, dict) or data.get("schema_version") != "1.0" or data.get("layer") != "actual_state" or not isinstance(data.get("assertions"), list):
            ctx.error("STR-LAYER-014", "actual-state/assertions.yaml har ogiltigt envelope.", actual_path)
        else:
            seen: set[str] = set()
            product_actual_types = {"product_in_use", "product_selected", "product_approved", "product_retired"}
            for i, row in enumerate(data["assertions"]):
                if not isinstance(row, dict): ctx.error("STR-LAYER-015", f"Actual assertion {i} måste vara objekt.", actual_path); continue
                rid=row.get("id")
                for field in as_list(aspec.get("required_fields")):
                    if row.get(field) in (None, "", []): ctx.error("STR-LAYER-016", f"Actual assertion {rid or i} saknar {field}.", actual_path)
                if not isinstance(rid, str) or not re.fullmatch(pattern, rid): ctx.error("STR-LAYER-017", f"Ogiltigt actual assertion-id: {rid}", actual_path)
                elif rid in seen: ctx.error("STR-LAYER-018", f"Dubblett actual assertion-id: {rid}", actual_path)
                else: seen.add(rid)
                at=row.get("assertion_type")
                if at not in allowed: ctx.error("STR-LAYER-019", f"Okänd actual assertion_type: {at}", actual_path)
                if row.get("status") not in statuses: ctx.error("STR-LAYER-020", f"Ogiltig actual-state status: {row.get('status')}", actual_path)
                subject=row.get("subject")
                if subject not in object_ids: ctx.error("STR-LAYER-021", f"Actual assertion refererar okänt subject: {subject}", actual_path)
                if at in product_actual_types and id_types.get(str(subject)) != "product":
                    ctx.error("STR-LAYER-022", f"{at} ska referera Product direkt; fick {subject} ({id_types.get(str(subject))}).", actual_path)
                ets=provenance_types(row.get("provenance"), str(rid or i), actual_path)
                if row.get("status") == "verified" and not ets.intersection({"explicit", "derived"}):
                    ctx.error("STR-LAYER-023", f"Verifierad actual state kräver organisationsspecifik explicit eller derived evidens; external ensam räcker inte ({rid or i}).", actual_path)

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



def effective_catalogs(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> tuple[set[str], set[str]]:
    """Return effective object/relation catalogs for the current project profile."""
    fmt, types, rels, _ = load_domain_specs(repo_root, ctx, manifest)
    model_version = str(as_mapping((manifest or {}).get("model")).get("metamodel_version", ""))
    if model_version != "1.0":
        fmt, types, rels = apply_project_metamodel(project_root, repo_root, fmt, types, rels, ctx)
    return set(as_mapping(types.get("object_types")).keys()), set(as_mapping(rels.get("relation_types")).keys())


def validate_derived_views(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    catalog_path = project_root / "derived-views" / "views.yaml"
    if not catalog_path.is_file():
        return
    schema_path = repo_root / "schemas" / "derived-view.schema.json"
    data = load_yaml(catalog_path, ctx)
    schema = load_json(schema_path, ctx)
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return
    for err in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        ptr = "/".join(str(x) for x in err.path)
        ctx.error("STR-VIEW-001", f"Derived-view-katalog bryter mot schema vid {ptr}: {err.message}", catalog_path)
    obj_types, rel_types = effective_catalogs(project_root, repo_root, manifest, ctx)
    seen=set()
    for view in data.get("views", []) or []:
        vid=view.get("id")
        if vid in seen:
            ctx.error("STR-VIEW-002", f"Dubblett av derived view-id: {vid}", catalog_path)
        seen.add(vid)
        if view.get("source_of_truth") is not False:
            ctx.error("STR-VIEW-003", f"Derived view {vid} måste ha source_of_truth=false.", catalog_path)
        for typ in (view.get("anchor") or {}).get("object_types", []) or []:
            if typ not in obj_types:
                ctx.error("STR-VIEW-004", f"Derived view {vid} refererar okänd objekttyp: {typ}", catalog_path)
        for step in view.get("join_path", []) or []:
            rs=step.get("relation"); rs=[rs] if isinstance(rs,str) else (rs or [])
            for rel in rs:
                if rel not in rel_types:
                    ctx.error("STR-VIEW-005", f"Derived view {vid} refererar okänd relationstyp: {rel}", catalog_path)
            for typ in step.get("target_types", []) or []:
                if typ not in obj_types:
                    ctx.error("STR-VIEW-006", f"Derived view {vid} refererar okänd målobjekttyp: {typ}", catalog_path)

    # If materialized derived views are checked in, they must be exactly reproducible.
    materialized = project_root / "build" / "derived-views"
    generator = repo_root / "scripts" / "generate_derived_views.py"
    if materialized.is_dir() and generator.is_file():
        with tempfile.TemporaryDirectory(prefix="ea-validate-views-") as tmp:
            out = Path(tmp) / "views"
            try:
                subprocess.run([sys.executable, str(generator), "--project-root", str(project_root), "--output-dir", str(out)], check=True, capture_output=True, text=True)
                compare_tree(materialized, out, ctx, "STR-VIEW-007", "Derived views")
            except subprocess.CalledProcessError as exc:
                ctx.error("STR-VIEW-008", f"Derived-view-generator kunde inte köras: {exc.stderr or exc}", generator)


def validate_presentation_contract(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    contract_path = project_root / "presentation" / "presentation-contract.yaml"
    if not contract_path.is_file():
        return
    schema_path = repo_root / "schemas" / "presentation-contract.schema.json"
    data = load_yaml(contract_path, ctx)
    schema = load_json(schema_path, ctx)
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return
    for err in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        ptr = "/".join(str(x) for x in err.path)
        ctx.error("STR-PRES-001", f"Presentationskontrakt bryter mot schema vid {ptr}: {err.message}", contract_path)
    if data.get("source_of_truth") is not False:
        ctx.error("STR-PRES-002", "Presentationskontrakt måste ha source_of_truth=false.", contract_path)
    # Validate presentation references against the project's effective metamodel.
    obj_types, rel_types = effective_catalogs(project_root, repo_root, manifest, ctx)
    for rel in (data.get("relation_labels") or {}):
        if rel not in rel_types:
            ctx.error("STR-PRES-003", f"Presentationskontrakt refererar okänd relationstyp: {rel}", contract_path)
    # Navigation sections must refer to declared derived views and remain non-canonical.
    views_path = project_root / "derived-views" / "views.yaml"
    view_ids = set()
    if views_path.is_file():
        views = load_yaml(views_path, ctx) or {}
        view_ids = {v.get("id") for v in (views.get("views") or []) if isinstance(v, dict)}
    for object_type, sections in (data.get("navigation_sections") or {}).items():
        if object_type not in obj_types:
            ctx.error("STR-PRES-006", f"Presentationskontrakt refererar okänd/avaktiverad objekttyp: {object_type}", contract_path)
        for section in sections or []:
            if section.get("source_of_truth") is not False:
                ctx.error("STR-PRES-004", f"Navigationssektion {object_type}.{section.get('id')} måste vara source_of_truth=false.", contract_path)
            view_id = section.get("derived_view")
            if view_id not in view_ids:
                ctx.error("STR-PRES-005", f"Navigationssektion {object_type}.{section.get('id')} refererar okänd derived view: {view_id}", contract_path)



def _collect_active_ids_for_governance(project_root: Path, ctx: ValidationContext) -> set[str]:
    active: set[str] = set()
    roots = [project_root / "model", project_root / "market-reference", project_root / "actual-state", project_root / "derived-views"]
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            rid = value.get("id")
            if isinstance(rid, str):
                active.add(rid)
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.glob("*.yaml")):
            data = load_yaml(path, ctx)
            if data is not None:
                walk(data)
    return active


def validate_change_control(project_root: Path, repo_root: Path, manifest: dict[str, Any] | None, ctx: ValidationContext) -> None:
    control_path = project_root / "governance" / "change-control.yaml"
    if not control_path.is_file():
        # Legacy projects and projects that have not enabled v2 change control remain valid.
        return
    schema_path = repo_root / "schemas" / "change-control.schema.json"
    registry_schema_path = repo_root / "schemas" / "retired-id-registry.schema.json"
    log_schema_path = repo_root / "schemas" / "change-log.schema.json"
    data = load_yaml(control_path, ctx); schema = load_json(schema_path, ctx)
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return
    for err in sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path)):
        ptr = "/".join(str(x) for x in err.path)
        ctx.error("STR-GOV-001", f"Change-control bryter mot schema vid {ptr}: {err.message}", control_path)
    cc = as_mapping(data.get("change_control"))
    if not cc.get("enabled"):
        return
    baseline = as_mapping(cc.get("baseline")); project = as_mapping((manifest or {}).get("project")); model = as_mapping((manifest or {}).get("model"))
    if project and baseline.get("model_revision") != project.get("revision"):
        ctx.error("STR-GOV-002", f"Baseline model_revision {baseline.get('model_revision')} matchar inte manifestrevision {project.get('revision')}.", control_path)
    if model and str(baseline.get("metamodel_version")) != str(model.get("metamodel_version")):
        ctx.error("STR-GOV-003", f"Baseline metamodel_version {baseline.get('metamodel_version')} matchar inte manifestets {model.get('metamodel_version')}.", control_path)
    pol = as_mapping(cc.get("policies")); frozen = as_mapping(pol.get("frozen_baseline"))
    allowed = set(as_list(frozen.get("allowed_without_reopen"))); reopen = set(as_list(frozen.get("requires_reopen")))
    all_classes = {"editorial","evidence_update","controlled_model_change","breaking_model_change","metamodel_change"}
    if allowed & reopen or (allowed | reopen) != all_classes:
        ctx.error("STR-GOV-004", "Freeze-policyn måste klassificera varje ändringsklass exakt en gång.", control_path)
    registries = as_mapping(cc.get("registries")); logs = as_mapping(cc.get("changelogs"))
    reg_path = project_root / str(registries.get("retired_ids", ""))
    registry = load_yaml(reg_path, ctx) if reg_path.is_file() else None
    reg_schema = load_json(registry_schema_path, ctx) if registry_schema_path.is_file() else None
    if not reg_path.is_file():
        ctx.error("STR-GOV-005", "Retired-ID-registry saknas.", reg_path)
    elif isinstance(registry, dict) and isinstance(reg_schema, dict):
        for err in sorted(Draft202012Validator(reg_schema).iter_errors(registry), key=lambda e: list(e.path)):
            ptr = "/".join(str(x) for x in err.path); ctx.error("STR-GOV-006", f"Retired-ID-registry bryter mot schema vid {ptr}: {err.message}", reg_path)
        ids=[r.get("id") for r in as_list(registry.get("retired_ids")) if isinstance(r,dict)]
        if len(ids) != len(set(ids)):
            ctx.error("STR-GOV-007", "Retired-ID-registry innehåller dubblett-ID.", reg_path)
        active = _collect_active_ids_for_governance(project_root, ctx)
        for rid in ids:
            if rid in active:
                ctx.error("STR-GOV-008", f"Pensionerat ID återanvänds i aktiv modell/lager: {rid}", reg_path)
    log_schema = load_json(log_schema_path, ctx) if log_schema_path.is_file() else None
    seen_changes: set[str] = set()
    for kind in ("model", "metamodel"):
        path = project_root / str(logs.get(kind, ""))
        if not path.is_file():
            ctx.error("STR-GOV-009", f"{kind}-changelog saknas.", path); continue
        log = load_yaml(path, ctx)
        if isinstance(log, dict) and isinstance(log_schema, dict):
            for err in sorted(Draft202012Validator(log_schema).iter_errors(log), key=lambda e: list(e.path)):
                ptr = "/".join(str(x) for x in err.path); ctx.error("STR-GOV-010", f"{kind}-changelog bryter mot schema vid {ptr}: {err.message}", path)
            if log.get("log_type") != kind:
                ctx.error("STR-GOV-011", f"Changelog har log_type={log.get('log_type')} men ligger som {kind}-logg.", path)
            for row in as_list(log.get("changes")):
                if not isinstance(row, dict): continue
                cid=row.get("id")
                if cid in seen_changes: ctx.error("STR-GOV-012", f"Dubblett change-id mellan changeloggar: {cid}", path)
                if isinstance(cid,str): seen_changes.add(cid)
                cls=row.get("change_class")
                if kind == "model" and cls == "metamodel_change":
                    ctx.error("STR-GOV-013", f"metamodel_change får inte ligga i modellchangelog ({cid}).", path)
                if kind == "metamodel" and cls != "metamodel_change":
                    ctx.error("STR-GOV-014", f"Metamodellchangelog får endast innehålla metamodel_change ({cid}).", path)
                if isinstance(row.get("revision"), int) and project and row["revision"] > project.get("revision", 0):
                    ctx.error("STR-GOV-015", f"Change {cid} refererar framtida revision {row['revision']}.", path)


def validate_rev80_unmigrated(project_root: Path, repo_root: Path, ctx: ValidationContext) -> None:
    """Validate the frozen unmigrated rev80 extended-legacy reference contract.

    This route deliberately avoids applying the modern project-manifest schema.
    """
    meta = load_yaml(repo_root / "compatibility/reference-projects/rev80/metamodel.yaml", ctx) or {}
    sig = as_mapping(meta.get("detection_signature"))
    expected_manifest = as_mapping(sig.get("manifest"))
    manifest_path = project_root / "project-manifest.json"
    manifest = load_json(manifest_path, ctx)
    if not isinstance(manifest, dict):
        return
    for field in ("schema_version", "revision", "file_count"):
        if str(manifest.get(field)) != str(expected_manifest.get(field)):
            ctx.error("STR-REV80U-001", f"Omigrerad rev80 har oväntat {field}: {manifest.get(field)!r}; förväntat {expected_manifest.get(field)!r}.", manifest_path)
    for rel in as_list(sig.get("required_paths")):
        if not (project_root / str(rel)).is_file():
            ctx.error("STR-REV80U-002", f"Omigrerad rev80 saknar signaturfil: {rel}", project_root / str(rel))

    counts = as_mapping(sig.get("canonical_counts_at_reference"))
    file_keys = {
        "capabilities": "model/capabilities.yaml", "it_supports": "model/it-support.yaml",
        "platform_services": "model/platform-services.yaml", "platforms": "model/platforms.yaml",
        "relations": "model/relations.yaml", "sources": "model/sources.yaml",
    }
    for key, rel in file_keys.items():
        path = project_root / rel
        if not path.is_file():
            continue
        data = load_yaml(path, ctx) or {}
        rows = as_list(as_mapping(data).get("relations" if key == "relations" else "sources" if key == "sources" else "objects"))
        expected = counts.get(key)
        if isinstance(expected, int) and len(rows) != expected:
            ctx.error("STR-REV80U-003", f"{rel}: förväntade {expected} poster, fick {len(rows)}.", path)
    products = project_root / "supporting/market-product-catalog.yaml"
    if products.is_file():
        pdata = load_yaml(products, ctx) or {}
        # rev80 supporting files have changed envelope names during experimentation; count the first list value.
        lists = [v for v in pdata.values() if isinstance(v, list)] if isinstance(pdata, dict) else []
        if lists and len(lists[0]) != counts.get("market_products"):
            ctx.error("STR-REV80U-004", f"Marknadsproduktkatalog: förväntade {counts.get('market_products')} poster, fick {len(lists[0])}.", products)

    # Exact frozen fingerprints are a strong guarantee when validating the original reference snapshot.
    fp_path = repo_root / "compatibility/reference-projects/rev80/source-fingerprints.yaml"
    fps = load_yaml(fp_path, ctx) or {}
    mismatches = []
    checked = 0
    for row in as_list(fps.get("files")):
        if not isinstance(row, dict):
            continue
        target = project_root / str(row.get("path", ""))
        if target.is_file() and isinstance(row.get("sha256"), str):
            checked += 1
            if sha256(target) != row["sha256"]:
                mismatches.append(str(row.get("path")))
    if checked and mismatches:
        ctx.warning("STR-REV80U-005", "Projektet matchar rev80-strukturen men avviker från den frysta referensens SHA-256 för: " + ", ".join(mismatches), project_root)


def is_rev80_extended_target(project_root: Path) -> bool:
    pm = project_root / "project-metamodel.yaml"
    if not pm.is_file():
        return False
    try:
        data = yaml.safe_load(pm.read_text(encoding="utf-8")) or {}
        meta = data.get("project_metamodel") or {}
        base = meta.get("base_profile") or {}
        return meta.get("id") == "it-formagemodell-del3-rev80-v2" and base.get("compatibility_mode") == "extended_legacy"
    except Exception:
        return False


def validate_rev80_extended_model(project_root: Path, repo_root: Path, ctx: ValidationContext) -> None:
    """Compatibility validation for the frozen rev80 migration/reconstruction.

    This intentionally validates the declared extended-legacy contract rather than
    pretending that all rev80 provenance/ID conventions are already native v2.
    """
    pm_path = project_root / "project-metamodel.yaml"
    pm = load_yaml(pm_path, ctx)
    if isinstance(pm, dict):
        schema = load_json(repo_root / "schemas/project-metamodel.schema.json", ctx)
        if isinstance(schema, dict):
            for err in sorted(Draft202012Validator(schema).iter_errors(pm), key=lambda e:list(e.path)):
                ctx.error("STR-REV80-001", f"Projektmetamodellen bryter mot schema: {err.message}", pm_path)
    expected = {"capabilities.yaml":13,"it-support.yaml":10,"platform-services.yaml":92,"platforms.yaml":35}
    object_ids=set(); active_retired=set()
    for fn,count in expected.items():
        path=project_root/"model"/fn; data=load_yaml(path,ctx)
        rows=as_list(as_mapping(data).get("objects"))
        if len(rows)!=count: ctx.error("STR-REV80-002", f"{fn}: förväntade {count} objekt, fick {len(rows)}.", path)
        for o in rows:
            if isinstance(o,dict) and isinstance(o.get("id"),str): object_ids.add(o["id"]); active_retired.add(o["id"])
    rel_path=project_root/"model/relations.yaml"; rels=as_list(as_mapping(load_yaml(rel_path,ctx)).get("relations"))
    if len(rels)!=385: ctx.error("STR-REV80-003", f"Förväntade 385 relationer, fick {len(rels)}.", rel_path)
    provided=[r for r in rels if isinstance(r,dict) and r.get("type")=="provided_by"]
    if len(provided)!=92: ctx.error("STR-REV80-004", f"Förväntade 92 provided_by efter migration, fick {len(provided)}.", rel_path)
    if any(isinstance(r,dict) and r.get("type")=="realized_by" and str(r.get("source","")).startswith("PLS-") and str(r.get("target","")).startswith("PLT-") for r in rels):
        ctx.error("STR-REV80-005", "PLS→PLT realized_by finns kvar trots entydig rev80 provided_by-semantik.", rel_path)
    for r in rels:
        if isinstance(r,dict) and (r.get("source") not in object_ids or r.get("target") not in object_ids): ctx.error("STR-REV80-006", f"Relation {r.get('id')} har okänd endpoint.", rel_path)
    report_path=project_root/"migration/rev80-migration-report.yaml"; report=load_yaml(report_path,ctx)
    counts=as_mapping(as_mapping(report).get("migration")).get("counts") if isinstance(report,dict) else {}
    required_counts={"products":295,"supporting_yaml":92,"retired_actual_platforms":10,"provided_by_converted":92}
    for k,v in required_counts.items():
        if as_mapping(counts).get(k)!=v: ctx.error("STR-REV80-007", f"Migreringsrapport {k}: förväntat {v}, fick {as_mapping(counts).get(k)}.", report_path)
    retired_path=project_root/"migration/rev80-retired-ids.yaml"; retired=as_list(as_mapping(load_yaml(retired_path,ctx)).get("retired_ids"))
    retired_ids={x.get("id") for x in retired if isinstance(x,dict)}
    if len(retired_ids)!=10: ctx.error("STR-REV80-008", f"Förväntade 10 pensionerade actual-platform-ID:n, fick {len(retired_ids)}.", retired_path)
    reused=sorted(retired_ids & active_retired)
    if reused: ctx.error("STR-REV80-009", f"Pensionerade ID:n återanvänds: {', '.join(reused)}", retired_path)
    supporting=list((project_root/"supporting").glob("*.yaml"))
    if len(supporting)!=92: ctx.error("STR-REV80-010", f"Förväntade 92 bevarade supporting-YAML, fick {len(supporting)}.", project_root/"supporting")


def validate_project(project_root: Path, repo_root: Path, check_generated: bool = True) -> ValidationContext:
    ctx = ValidationContext()
    if not project_root.is_dir():
        ctx.error("STR-PROJ-001", "Projektkatalogen finns inte.", project_root)
        return ctx

    try:
        profile = detect_project_profile(project_root, repo_root)
    except Exception as exc:
        ctx.error("STR-PROFILE-001", f"Projektprofil kunde inte detekteras: {exc}", project_root)
        return ctx
    # The EA Stödjare repository itself is a development/reference template and
    # intentionally has no project-metamodel.yaml. Its manifest explicitly declares v2.
    if profile.get("classification") == "unknown":
        mp = project_root / "project-manifest.json"
        try:
            rm = json.loads(mp.read_text(encoding="utf-8")) if mp.is_file() else {}
        except Exception:
            rm = {}
        reference_template = as_mapping(rm.get("project")).get("id") == "ea-stodjare-reference"
        if reference_template and str(as_mapping(rm.get("model")).get("metamodel_version")) == "2.0":
            profile = {
                "classification": "native_v2", "confidence": "high",
                "selected_profile": "ea-stodjare-v2-reference-template",
                "evidence": ["repository reference manifest metamodel_version=2.0"],
                "blockers": [], "next_action": "Validera mot repositoryts native v2-basprofil."
            }
    ctx.profile = profile
    classification = str(profile.get("classification"))
    if classification in {"unknown", "invalid_explicit_model"}:
        ctx.error("STR-PROFILE-002", f"Projektprofil är {classification}; semantik får inte appliceras automatiskt. Blockers: {profile.get('blockers')}", project_root)
        return ctx
    ctx.stage("profile_detection", "passed", classification)

    # Frozen, unmigrated rev80 has an older flat manifest and must be validated
    # against its reconstructed extended-legacy contract before modern schemas.
    if classification == "extended_legacy" and "rev80-reconstruction" in str(profile.get("selected_profile")) and not (project_root / "project-metamodel.yaml").is_file():
        validate_rev80_unmigrated(project_root, repo_root, ctx)
        ctx.stage("extended_legacy_rev80", "passed" if not ctx.errors else "failed")
        return ctx

    before = len(ctx.errors)
    manifest = validate_manifest(project_root, repo_root, ctx)
    ctx.stage("manifest", "passed" if len(ctx.errors) == before else "failed")
    if is_rev80_extended_target(project_root):
        before = len(ctx.errors)
        validate_rev80_extended_model(project_root, repo_root, ctx)
        ctx.stage("extended_legacy_rev80_migrated", "passed" if len(ctx.errors) == before else "failed")
        return ctx

    before = len(ctx.errors); validate_model(project_root, repo_root, manifest, ctx); ctx.stage("model", "passed" if len(ctx.errors)==before else "failed")
    before = len(ctx.errors); validate_information_layers(project_root, repo_root, manifest, ctx); ctx.stage("information_layers", "passed" if len(ctx.errors)==before else "failed")
    before = len(ctx.errors); validate_derived_views(project_root, repo_root, manifest, ctx); ctx.stage("derived_views", "passed" if len(ctx.errors)==before else "failed")
    before = len(ctx.errors); validate_presentation_contract(project_root, repo_root, manifest, ctx); ctx.stage("presentation", "passed" if len(ctx.errors)==before else "failed")
    before = len(ctx.errors); validate_change_control(project_root, repo_root, manifest, ctx); ctx.stage("change_control", "passed" if len(ctx.errors)==before else "failed")
    if check_generated:
        before = len(ctx.errors)
        try:
            validate_generated(project_root, repo_root, ctx)
        except subprocess.CalledProcessError as exc:
            ctx.error("STR-GEN-005", f"Generator kunde inte köras: {exc.stderr or exc}")
        ctx.stage("generated_artifacts", "passed" if len(ctx.errors)==before else "failed")
    return ctx


def main() -> int:
    parser = argparse.ArgumentParser(description="Validera strukturen i ett EA Stödjare-projekt.")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(), help="Projektrot som ska valideras.")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1], help="EA Stödjare-reporot med schemas/scripts.")
    parser.add_argument("--no-generated", action="store_true", help="Hoppa över kontroll av genererade artefakter.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Skriv resultat som JSON.")
    parser.add_argument("--report-file", type=Path, help="Skriv maskinläsbar valideringsrapport som JSON.")
    args = parser.parse_args()

    ctx = validate_project(args.project_root.resolve(), args.repo_root.resolve(), check_generated=not args.no_generated)
    report = {
        "schema_version": "1.0",
        "valid": not ctx.errors,
        "profile": ctx.profile,
        "stages": ctx.stages,
        "summary": {"errors": len(ctx.errors), "warnings": len(ctx.warnings)},
        "errors": [f.__dict__ for f in ctx.errors],
        "warnings": [f.__dict__ for f in ctx.warnings],
    }
    if args.report_file:
        args.report_file.parent.mkdir(parents=True, exist_ok=True)
        args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for finding in ctx.findings:
            print(finding.format())
        print(f"Validering: {'GODKÄND' if not ctx.errors else 'UNDERKÄND'} ({len(ctx.errors)} fel, {len(ctx.warnings)} varningar)")
    return 0 if not ctx.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
