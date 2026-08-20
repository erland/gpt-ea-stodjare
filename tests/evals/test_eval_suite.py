#!/usr/bin/env python3
from pathlib import Path
import json
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    suite_path = ROOT / "evals/eval-suite.yaml"
    suite = yaml.safe_load(suite_path.read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "schemas/semantic-eval.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    assert suite["format"] == "ea-stodjare-semantic-eval-suite"
    assert suite["version"] == "1.0"
    cases = suite["cases"]
    assert len(cases) >= 12, "Eval-sviten är för liten för v1"
    ids = [case["id"] for case in cases]
    assert len(ids) == len(set(ids)), "Dubblett-ID i eval-suite"

    required_tags = {
        "classification", "evidence", "research", "gap_analysis",
        "model_design", "uncertainty", "conflict", "scope"
    }
    found_tags = set()
    blocking = 0
    for entry in cases:
        path = ROOT / "evals" / entry["file"]
        assert path.exists(), f"Saknat evalfall: {entry['file']}"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            fail(f"Schemafel i {entry['file']}: " + "; ".join(e.message for e in errors))
        assert data["id"] == entry["id"]
        criterion_ids = [c["id"] for c in data["grading_criteria"]]
        assert len(criterion_ids) == len(set(criterion_ids)), f"Dubblettkriterium i {entry['id']}"
        found_tags.update(data["tags"])
        blocking += bool(entry["blocking"])

    missing = required_tags - found_tags
    assert not missing, f"Saknade obligatoriska testområden: {sorted(missing)}"
    assert blocking >= 8, "För få blockerande v1-fall"
    assert suite["release_gate"]["minimum_weighted_score_percent"] >= 80

    print(f"OK: {len(cases)} semantiska evalfall validerade; {blocking} blockerande.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
