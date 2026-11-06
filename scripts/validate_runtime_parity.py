#!/usr/bin/env python3
"""Verify EA Stödjare's declared five peer runtimes (GPT Byggaren 1.6.33).

This checks configuration and parity declarations, not real host execution.
"""
from __future__ import annotations
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
cfg = yaml.safe_load((ROOT / 'gpt-project.yaml').read_text(encoding='utf-8'))
parity = yaml.safe_load((ROOT / 'runtime-parity.yaml').read_text(encoding='utf-8'))
expected = {'chatgpt_chat', 'claude_project', 'claude_skills', 'opencode', 'openai_plugin'}
categories = {'behavior', 'capability', 'artifact', 'workspace_state', 'tool'}
errors = []
def check(condition, explanation):
    if not condition:
        errors.append(explanation)

check(set(cfg.get('runtime_parity', {}).get('registered_runtimes', [])) == expected, 'project registered runtimes mismatch')
check(set(parity.get('registered_runtimes', [])) == expected, 'parity registered runtimes mismatch')
check(set(parity.get('compared_categories', [])) == categories, 'parity categories mismatch')
runtime = cfg.get('runtime', {})
for key in ('chat_zip', 'plugin', 'claude', 'opencode'):
    check(runtime.get(key, {}).get('enabled') is True, f'{key} runtime disabled')
check(runtime.get('custom_gpt', {}).get('enabled') is False, 'retired Custom GPT must be disabled')
targets = cfg.get('build_system', {}).get('runtime_targets', {})
check(set(targets) == {'chat', 'plugin', 'claude_project', 'claude_skills', 'opencode'}, 'runtime build targets mismatch')
for key in expected:
    item = parity.get('runtimes', {}).get(key, {})
    check(item.get('active') is True, f'{key} must be declared active')
    check(item.get('suitability') in {'ready', 'host_dependent'}, f'{key} suitability not assessed')
check(parity.get('host_execution_verified') is False, 'host verification must not be claimed without tests')
if errors:
    print('RUNTIME PARITY: FAIL')
    for error in errors:
        print('-', error)
    sys.exit(1)
print('RUNTIME PARITY: PASS (declarative; host verification remains open)')
