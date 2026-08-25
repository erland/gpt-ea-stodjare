#!/usr/bin/env python3
"""Detect EA Stödjare project model profile without interpreting project content."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_json_schema(instance: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    return [e.message for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))]


def result(classification: str, confidence: str, selected_profile: str | None,
           evidence: list[str], blockers: list[str], next_action: str) -> dict[str, Any]:
    return {
        "classification": classification,
        "confidence": confidence,
        "selected_profile": selected_profile,
        "evidence": evidence,
        "blockers": blockers,
        "next_action": next_action,
    }


def v1_manifest_matches(manifest: dict[str, Any]) -> bool:
    model = manifest.get("model", {})
    return (
        manifest.get("format") == "ea-stodjare-project"
        and str(manifest.get("format_version")) == "1.0"
        and str(model.get("model_format_version")) == "1.0"
        and str(model.get("metamodel_version")) == "1.0"
        and str(model.get("relation_model_version")) == "1.0"
        and str(model.get("provenance_model_version")) == "1.0"
    )


def detect(project_root: Path, repository_root: Path = ROOT) -> dict[str, Any]:
    project_root = project_root.resolve()
    # 1. Explicit v2 project metamodel.
    pm = project_root / "project-metamodel.yaml"
    if pm.exists():
        try:
            data = load_yaml(pm)
        except Exception as exc:
            return result("invalid_explicit_model", "high", None,
                          ["project-metamodel.yaml finns"], [f"YAML kan inte läsas: {exc}"],
                          "Rätta project-metamodel.yaml innan projektdata tolkas.")
        errors = validate_json_schema(data, repository_root / "schemas/project-metamodel.schema.json")
        if errors:
            return result("invalid_explicit_model", "high", None,
                          ["project-metamodel.yaml finns"], errors,
                          "Rätta project-metamodel.yaml; fall inte tillbaka till legacyprofil.")
        base = data["project_metamodel"]["base_profile"]["id"]
        return result("native_v2", "high", base,
                      ["project-metamodel.yaml validerar mot v2-schemat"], [],
                      "Ladda base profile och projektets deklarerade delta innan projektdata tolkas.")

    # 2. Explicit legacy marker.
    marker = project_root / "project-compatibility.yaml"
    if marker.exists():
        try:
            data = load_yaml(marker)
        except Exception as exc:
            return result("unknown", "low", None, ["project-compatibility.yaml finns"],
                          [f"Markören kan inte läsas: {exc}"], "Rätta eller ta bort den explicita markören.")
        errors = validate_json_schema(data, repository_root / "schemas/project-compatibility-marker.schema.json")
        if errors:
            return result("unknown", "low", None, ["project-compatibility.yaml finns"], errors,
                          "Rätta project-compatibility.yaml innan projektet redigeras.")
        c = data["compatibility"]
        profile = c["profile"]
        mode = c.get("mode", "legacy")
        if profile != "ea-stodjare-v1":
            return result("unknown", "low", profile, [f"explicit profil: {profile}"],
                          ["Profilen stöds inte av denna GPT-version."],
                          "Ladda kompatibel profil eller migrera kontrollerat.")
        classification = "extended_legacy" if mode == "extended_legacy" else "legacy_v1"
        return result(classification, "high", profile,
                      ["explicit project-compatibility.yaml", f"mode={mode}"], [],
                      "Ladda den frysta v1-profilen; inventera deklarerade extensions vid extended legacy.")

    # 3/4. v1 manifest + extension detection.
    manifest_path = project_root / "project-manifest.json"
    if manifest_path.exists():
        try:
            manifest = load_json(manifest_path)
        except Exception as exc:
            return result("unknown", "low", None, ["project-manifest.json finns"],
                          [f"Manifestet kan inte läsas: {exc}"], "Rätta manifestet innan modellprofil väljs.")
        # Older extended-legacy packages (including rev80) used a flat archive manifest
        # before the standardized ea-stodjare-project envelope existed. Detect such
        # projects from the frozen reference signature before ordinary v1 matching.
        rev80_meta = load_yaml(repository_root / "compatibility/reference-projects/rev80/metamodel.yaml")
        sig = rev80_meta["detection_signature"]
        req = sig["required_paths"]
        flat_rev = manifest.get("revision")
        flat_root = str(manifest.get("root_directory", ""))
        flat_count = manifest.get("file_count")
        if (manifest.get("schema_version") == "1.0" and flat_rev == sig["manifest"]["revision"]
                and flat_count == sig["manifest"]["file_count"] and all((project_root / x).exists() for x in req)
                and ("it-formagemodell" in flat_root or "it-formagemodell" in project_root.name)):
            return result("extended_legacy", "high", "ea-stodjare-v1 + rev80-reconstruction",
                          ["flat extended-legacy manifest", "rev80 required paths", f"revision={flat_rev}"], [],
                          "Ladda v1-profilen och rev80-rekonstruktionen; migrera via extended-legacy-adaptern om v2 önskas.")

        if v1_manifest_matches(manifest):
            ext_signals = [
                "supporting/market-product-catalog.yaml",
                "supporting/relation-roles.yaml",
                "supporting/model-freeze-baseline.yaml",
                "supporting/documentation-presentation-model.yaml",
            ]
            found = [p for p in ext_signals if (project_root / p).exists()]
            # Known rev80 snapshot/signature: required paths + revision 80 + known root/id clues.
            rev80_meta = load_yaml(repository_root / "compatibility/reference-projects/rev80/metamodel.yaml")
            sig = rev80_meta["detection_signature"]
            req = sig["required_paths"]
            rev80_required = all((project_root / p).exists() for p in req)
            rev = manifest.get("project", {}).get("revision")
            project_id = manifest.get("project", {}).get("id", "")
            root_name = project_root.name
            if rev80_required and rev == 80 and ("it-formagemodell" in project_id or "it-formagemodell" in root_name):
                return result("extended_legacy", "high", "ea-stodjare-v1 + rev80-reconstruction",
                              ["v1 manifestmarkörer", "rev80 required paths", "revision=80"], [],
                              "Ladda v1-profilen och rev80-rekonstruktionen; respektera pensionerade/derived lager.")
            if found:
                return result("extended_legacy", "medium", "ea-stodjare-v1",
                              ["v1 manifestmarkörer"] + [f"extension signal: {p}" for p in found], [],
                              "Ladda v1-profilen och inventera extensions innan kanoniska ändringar görs.")
            return result("legacy_v1", "high", "ea-stodjare-v1",
                          ["samtliga v1 manifestmarkörer matchar"], [],
                          "Ladda den frysta v1-profilen och fortsätt i legacy-läge om migration inte valts.")

    return result("unknown", "low", None, [],
                  ["Ingen entydig native v2-, legacy v1- eller extended legacy-signatur hittades."],
                  "Inventera projektets filer och semantik; applicera inte standardmetamodellen automatiskt.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-root", required=True, type=Path)
    ap.add_argument("--repository-root", type=Path, default=ROOT)
    ap.add_argument("--pretty", action="store_true")
    args = ap.parse_args()
    out = detect(args.project_root, args.repository_root)
    print(json.dumps(out, ensure_ascii=False, indent=2 if args.pretty else None))
    return 2 if out["classification"] in {"unknown", "invalid_explicit_model"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
