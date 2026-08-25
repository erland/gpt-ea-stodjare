from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def test_research_model_proposal_keeps_external_and_organizational_claims_separate():
    scenario=(ROOT/'tests/scenarios/08-research-based-model-proposal.md').read_text(encoding='utf-8')
    workflow=(ROOT/'knowledge/workflow-research.md').read_text(encoding='utf-8')
    model=(ROOT/'knowledge/workflow-model-design.md').read_text(encoding='utf-8')
    assert 'proposed' in scenario and 'external' in scenario
    assert 'Extern research får inte automatiskt skriva om den kanoniska modellen.' in workflow
    assert 'överförbarhet' in scenario.lower() or 'transferability' in scenario.lower()
    assert 'research' in model.lower() and 'förslag' in model.lower()
