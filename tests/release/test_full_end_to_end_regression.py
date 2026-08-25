from pathlib import Path
import json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[2]

def test_full_regression_contract_lists_all_twelve_scenarios():
    text=(ROOT/'scripts/run_full_e2e_regression.py').read_text(encoding='utf-8')
    required=['simple_v2_project','advanced_v2_extensions','open_v1_without_migration','continue_editing_v1','migrate_v1','open_rev80','migrate_rev80','product_analysis_it_support','product_analysis_platform_service','research_model_proposal','derived_views','export']
    assert all(x in text for x in required)

def test_product_platform_service_scenario_is_part_of_repository():
    assert (ROOT/'examples/product-analysis-platform-service/expected-analysis.yaml').exists()
    assert (ROOT/'tests/compatibility/test_platform_service_product_analysis_scenario.py').exists()
