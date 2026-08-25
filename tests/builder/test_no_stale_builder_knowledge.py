from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STALE=(
    'metamodel v2 (under utveckling)',
    'definieras först i steg 4',
    'specificeras tekniskt i steg 5',
    'fastställs först i steg 6',
    'det kommer i steg 20',
    'införs först i steg 10',
    'före steg 20 ska',
)

def test_builder_knowledge_contains_no_obsolete_future_step_language():
    text='\n'.join(p.read_text(encoding='utf-8') for p in sorted((ROOT/'custom-gpt/knowledge').glob('*.md'))).lower()
    for phrase in STALE:
        assert phrase not in text, phrase
    assert 'runtimekontrakt – domänmodell v2' in text
    assert 'runtimekontrakt – kvalitet v2' in text
    assert 'structural-validation-v2.md' in text
    assert 'metamodel-aware-generation.md' in text
