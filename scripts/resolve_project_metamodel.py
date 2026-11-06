#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource


class ExtensionResolutionError(RuntimeError):
    pass


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_json_schema(instance: Any, schema: dict[str, Any], registry: Registry | None = None) -> list[str]:
    validator = Draft202012Validator(schema, registry=registry or Registry())
    return [f"{'/'.join(str(x) for x in err.path) or '<root>'}: {err.message}" for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def schema_registry(repo_root: Path) -> Registry:
    pm_schema = load_json(repo_root / "schemas/project-metamodel.schema.json")
    pm_resource = Resource.from_contents(pm_schema)
    return Registry().with_resources([
        ("https://example.invalid/ea-stodjare/project-metamodel.schema.json", pm_resource),
        ("project-metamodel.schema.json", pm_resource),
    ])


def load_registry(repo_root: Path) -> dict[tuple[str, str], dict[str, Any]]:
    path = repo_root / "extensions/registry.yaml"
    data = load_yaml(path) or {}
    rows = data.get("extensions", [])
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        key = (str(row.get("id")), str(row.get("version")))
        if key in result:
            raise ExtensionResolutionError(f"Dubblett i extension-registret: {key[0]}@{key[1]}")
        result[key] = row
    return result


def compatible(extension: dict[str, Any], base_profile: dict[str, Any]) -> bool:
    base_id = base_profile.get("id")
    base_version = base_profile.get("version")
    for rule in extension.get("compatible_base_profiles", []):
        if rule.get("id") != base_id:
            continue
        versions = rule.get("versions")
        if not versions or base_version in versions:
            return True
    return False


def collect_core_names(repo_root: Path) -> tuple[set[str], set[str], dict[str, set[str]]]:
    types = load_yaml(repo_root / "schemas/object-types.yaml") or {}
    relations = load_yaml(repo_root / "schemas/relations.yaml") or {}
    core_types = set((types.get("object_types") or {}).keys())
    core_relations = set((relations.get("relation_types") or {}).keys())
    attrs: dict[str, set[str]] = {}
    common = types.get("common") or {}
    common_attrs = set(common.get("required_attributes") or []) | set(common.get("optional_attributes") or [])
    for name, spec in (types.get("object_types") or {}).items():
        attrs[name] = set(common_attrs)
        attrs[name].update(spec.get("required_attributes") or [])
        attrs[name].update(spec.get("optional_attributes") or [])
        attrs[name].update(spec.get("recommended_attributes") or [])
    return core_types, core_relations, attrs


def resolve(project_path: Path, repo_root: Path) -> dict[str, Any]:
    project_doc = load_yaml(project_path)
    pm_schema = load_json(repo_root / "schemas/project-metamodel.schema.json")
    errors = validate_json_schema(project_doc, pm_schema)
    if errors:
        raise ExtensionResolutionError("Ogiltig project-metamodell:\n" + "\n".join(errors))

    result = copy.deepcopy(project_doc)
    pm = result["project_metamodel"]
    refs = [r for r in pm.get("extensions", []) if r.get("enabled")]
    registry_rows = load_registry(repo_root)
    ext_schema = load_json(repo_root / "schemas/project-extension.schema.json")
    ref_registry = schema_registry(repo_root)

    active: list[dict[str, Any]] = []
    active_ids: set[str] = set()
    namespaces: set[str] = set()
    for ref in refs:
        version = ref.get("version")
        if version is None:
            matches = [k for k in registry_rows if k[0] == ref["id"]]
            if len(matches) != 1:
                raise ExtensionResolutionError(f"Extension {ref['id']} måste ange version när registret inte ger exakt en kandidat.")
            key = matches[0]
        else:
            key = (ref["id"], str(version))
        row = registry_rows.get(key)
        if row is None:
            raise ExtensionResolutionError(f"Aktiv extension saknas i registret: {key[0]}@{key[1]}")
        package_path = repo_root / row["path"]
        package = load_yaml(package_path)
        ext_errors = validate_json_schema(package, ext_schema, ref_registry)
        if ext_errors:
            raise ExtensionResolutionError(f"Ogiltigt extensionpaket {package_path}:\n" + "\n".join(ext_errors))
        ext = package["extension"]
        if ext["id"] != key[0] or str(ext["version"]) != key[1]:
            raise ExtensionResolutionError(f"Registry-identitet matchar inte paketet för {key[0]}@{key[1]}")
        if not compatible(ext, pm["base_profile"]):
            raise ExtensionResolutionError(f"Extension {ext['id']}@{ext['version']} är inte kompatibel med basprofil {pm['base_profile'].get('id')}@{pm['base_profile'].get('version')}")
        if ext["namespace"] in namespaces:
            raise ExtensionResolutionError(f"Namespace-kollision: {ext['namespace']}")
        namespaces.add(ext["namespace"])
        active.append(ext)
        active_ids.add(ext["id"])

    for ext in active:
        missing = set(ext.get("requires", [])) - active_ids
        if missing:
            raise ExtensionResolutionError(f"Extension {ext['id']} saknar beroenden: {', '.join(sorted(missing))}")
        conflicts = set(ext.get("conflicts_with", [])) & active_ids
        if conflicts:
            raise ExtensionResolutionError(f"Extension {ext['id']} konflikterar med: {', '.join(sorted(conflicts))}")

    core_types, core_relations, core_attrs = collect_core_names(repo_root)
    inline_types = {x["type"] for x in pm["object_types"].get("custom", [])}
    inline_relations = {x["type"] for x in pm["relations"].get("custom", [])}
    known_types = set(core_types) | inline_types
    known_relations = set(core_relations) | inline_relations
    known_attrs = {k: set(v) for k, v in core_attrs.items()}
    for item in pm["object_types"].get("custom", []):
        known_attrs[item["type"]] = {a["name"] for a in item.get("attributes", [])}
    for ext in pm.get("attribute_extensions", []):
        target = ext["object_type"]
        known_attrs.setdefault(target, set())
        for attr in ext["attributes"]:
            if attr["name"] in known_attrs[target]:
                raise ExtensionResolutionError(f"Projektets attributextension krockar med befintligt attribut: {target}.{attr['name']}")
            known_attrs[target].add(attr["name"])

    value_sets: dict[str, list[str]] = {x["id"]: list(x["values"]) for x in pm.get("value_sets", [])}
    qualifier_names = {x["name"] for x in pm.get("relation_qualifiers", [])}
    qa_rules: list[dict[str, Any]] = []
    presentation_labels = dict((pm.get("presentation") or {}).get("labels") or {})
    presentation_patterns: dict[str, str] = {}
    applied: list[dict[str, str]] = []

    for ext in active:
        c = ext.get("contributions") or {}
        for obj in c.get("object_types", []):
            name = obj["type"]
            if name in known_types:
                raise ExtensionResolutionError(f"Objekttypskollision från {ext['id']}: {name}")
            known_types.add(name)
            known_attrs[name] = {a["name"] for a in obj.get("attributes", [])}
            pm["object_types"]["custom"].append(copy.deepcopy(obj))

        for attr_ext in c.get("attribute_extensions", []):
            target = attr_ext["object_type"]
            if target not in known_types:
                raise ExtensionResolutionError(f"Attributextension från {ext['id']} riktar sig mot okänd objekttyp: {target}")
            known_attrs.setdefault(target, set())
            for attr in attr_ext["attributes"]:
                if attr["name"] in known_attrs[target]:
                    raise ExtensionResolutionError(f"Attributkollision från {ext['id']}: {target}.{attr['name']}")
                known_attrs[target].add(attr["name"])
            pm.setdefault("attribute_extensions", []).append(copy.deepcopy(attr_ext))

        for rel in c.get("relations", []):
            name = rel["type"]
            if name in known_relations:
                raise ExtensionResolutionError(f"Relationskollision från {ext['id']}: {name}")
            for endpoint in rel["endpoints"]:
                unknown = (set(endpoint["source"]) | set(endpoint["target"])) - known_types
                if unknown:
                    raise ExtensionResolutionError(f"Relation {name} från {ext['id']} refererar okända objekttyper: {', '.join(sorted(unknown))}")
            known_relations.add(name)
            pm["relations"]["custom"].append(copy.deepcopy(rel))

        for qual in c.get("relation_qualifiers", []):
            if qual["name"] in qualifier_names:
                raise ExtensionResolutionError(f"Relationskvalificerarkollision från {ext['id']}: {qual['name']}")
            unknown = set(qual["applies_to"]) - known_relations
            if unknown:
                raise ExtensionResolutionError(f"Kvalificeraren {qual['name']} refererar okända relationer: {', '.join(sorted(unknown))}")
            qualifier_names.add(qual["name"])
            pm.setdefault("relation_qualifiers", []).append(copy.deepcopy(qual))

        for vs in c.get("value_sets", []):
            if vs["id"] in value_sets:
                raise ExtensionResolutionError(f"Value-set-kollision från {ext['id']}: {vs['id']}")
            value_sets[vs["id"]] = list(vs["values"])
            pm.setdefault("value_sets", []).append(copy.deepcopy(vs))

        for vse in c.get("value_set_extensions", []):
            target = vse["target"]
            if target not in value_sets:
                raise ExtensionResolutionError(f"Value-set-extension från {ext['id']} riktar sig mot okänd värdemängd: {target}")
            dup = set(vse["add_values"]) & set(value_sets[target])
            if dup:
                raise ExtensionResolutionError(f"Value-set-extension från {ext['id']} försöker återdefiniera värden i {target}: {', '.join(sorted(dup))}")
            value_sets[target].extend(vse["add_values"])
            for vs in pm["value_sets"]:
                if vs["id"] == target:
                    vs["values"].extend(vse["add_values"])
                    break

        qa_rules.extend(copy.deepcopy(c.get("qa_rules", [])))
        pres = c.get("presentation") or {}
        for key, label in (pres.get("labels") or {}).items():
            if key in presentation_labels and presentation_labels[key] != label:
                raise ExtensionResolutionError(f"Presentationsetikett från {ext['id']} krockar med projektets etikett för {key}")
            presentation_labels[key] = label
        for key, pattern in (pres.get("object_display_patterns") or {}).items():
            if key in presentation_patterns and presentation_patterns[key] != pattern:
                raise ExtensionResolutionError(f"Presentationsmönster från {ext['id']} krockar för {key}")
            presentation_patterns[key] = pattern
        applied.append({"id": ext["id"], "version": str(ext["version"]), "namespace": ext["namespace"]})

    pm.setdefault("presentation", {})["labels"] = presentation_labels
    result["resolved_extensions"] = applied
    result["extension_qa_rules"] = qa_rules
    result["extension_object_display_patterns"] = presentation_patterns
    result["derived_artifact"] = True
    result["source_of_truth"] = False
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a v2 project metamodel with enabled extension packages.")
    parser.add_argument("project_metamodel", type=Path)
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        resolved = resolve(args.project_metamodel.resolve(), args.repo_root.resolve())
    except (ExtensionResolutionError, OSError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"ERROR EXT-RESOLVE: {exc}", file=sys.stderr)
        return 2
    text = yaml.safe_dump(resolved, allow_unicode=True, sort_keys=False)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
