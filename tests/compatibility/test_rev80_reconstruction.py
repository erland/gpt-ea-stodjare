from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
REF = ROOT / 'compatibility' / 'reference-projects' / 'rev80'


def load(name):
    return yaml.safe_load((REF / name).read_text(encoding='utf-8'))


def test_rev80_reconstruction_shape():
    m = load('metamodel.yaml')
    rp = m['reference_project']
    assert rp['compatibility_class'] == 'extended_legacy'
    assert rp['source_revision'] == 80
    assert rp['base_profile'] == 'ea-stodjare-v1'
    counts = m['detection_signature']['canonical_counts_at_reference']
    assert counts == {
        'capabilities': 13,
        'it_supports': 10,
        'platform_services': 92,
        'platforms': 35,
        'relations': 385,
        'sources': 14,
        'market_products': 295,
    }


def test_rev80_semantic_guards():
    m = load('metamodel.yaml')
    core = m['canonical_core']
    assert 'konceptuell' in core['object_types']['platform']['semantic_override'].lower() or 'konceptuella' in core['object_types']['platform']['semantic_override'].lower()
    assert 'konceptuell hemvist' in core['relation_model']['semantic_overrides']['realized_by'].lower()
    actual = m['retired_or_noncanonical_experiments']['actual_platform_layer']
    assert actual['active'] is False
    assert actual['retired_candidate_count'] == 10
    assert m['project_extensions']['derived_views']['source_of_truth'] is False


def test_extension_inventory_is_complete_reference_snapshot():
    inv = load('extension-inventory.yaml')
    assert inv['source_revision'] == 80
    assert inv['supporting_yaml_count'] == 92
    assert len(inv['items']) == 92
    assert len({x['path'] for x in inv['items']}) == 92
    required = {
        'supporting/market-product-catalog.yaml',
        'supporting/market-product-service-realization.yaml',
        'supporting/model-change-control.yaml',
        'supporting/model-freeze-baseline.yaml',
        'supporting/documentation-presentation-model.yaml',
        'supporting/actual-platform-offering-assessment.yaml',
        'supporting/retired-actual-platform-candidates.yaml',
    }
    assert required.issubset({x['path'] for x in inv['items']})
