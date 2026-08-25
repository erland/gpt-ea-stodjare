from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]

def test_final_release_contract_is_complete():
    assert (ROOT/'VERSION').read_text(encoding='utf-8').strip()=='2.0.0'
    manifest=json.loads((ROOT/'project-manifest.json').read_text(encoding='utf-8'))
    assert manifest['project']['revision'] >= 59
    assert manifest['project']['lifecycle_status']=='approved'
    assert manifest['model']['metamodel_version']=='2.0'
    assert manifest['model']['relation_model_version']=='2.0'
    for rel in ('docs/final-release-review-v2.0.0.md','docs/release-notes-v2.0.0.md','docs/migration-guide-v1-to-v2.md'):
        assert (ROOT/rel).is_file() and len((ROOT/rel).read_text(encoding='utf-8'))>500

def test_superseded_rc_artifacts_are_not_shipped():
    removed=(
      'docs/release-candidate-review-v2.0.0-rc1.md','docs/release-candidate-review-v2.0.0-rc2.md',
      'docs/release-notes-v2.0.0-rc1.md','docs/release-notes-v2.0.0-rc2.md',
      'compatibility/reports/rc-hardening-v2.0.0-rc2.yaml','compatibility/reports/step32-release-candidate.yaml',
    )
    assert all(not (ROOT/x).exists() for x in removed)
