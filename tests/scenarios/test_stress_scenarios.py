from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCENARIOS = ROOT / "tests" / "scenarios"
REPORT = ROOT / "docs" / "stress-test-report.md"


def test_ten_planned_scenarios_exist():
    files = sorted(p for p in SCENARIOS.glob("[0-9][0-9]-*.md"))
    assert len(files) == 10, [p.name for p in files]


def test_each_scenario_has_required_sections():
    for path in sorted(SCENARIOS.glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        for heading in ["## Syfte", "## Syntetiskt underlag", "## Förväntat beteende", "## Primär risk", "## Bedömning steg 26"]:
            assert heading in text, f"{path}: saknar {heading}"


def test_stress_report_records_all_scenarios_and_correction():
    text = REPORT.read_text(encoding="utf-8")
    assert "10/10" in text
    assert "consumer_scope" in text
    assert "detaljerad lösningsarkitektur" in text.lower()
