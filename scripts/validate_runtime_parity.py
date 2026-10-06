#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def check(cond,msg):
    if not cond: errors.append(msg)

cfg=yaml.safe_load((ROOT/'gpt-project.yaml').read_text(encoding='utf-8'))
parity=yaml.safe_load((ROOT/'runtime-parity.yaml').read_text(encoding='utf-8'))

expected={'chatgpt_chat','chatgpt_custom','claude_project','opencode','openai_plugin'}
cats={'behavior','capability','artifact','workspace_state','tool'}
check(set(cfg.get('runtime_parity',{}).get('registered_runtimes',[]))==expected,'gpt-project registered runtimes mismatch')
check(set(parity.get('registered_runtimes',[]))==expected,'runtime-parity registered runtimes mismatch')
check(set(parity.get('compared_categories',[]))==cats,'runtime-parity categories mismatch')

candidates={x['runtime_id']:x for x in cfg.get('analysis',{}).get('runtime',{}).get('candidates',[])}
for rid in expected:
    check(rid in candidates,f'missing candidate {rid}')
for rid in ('chatgpt_chat','chatgpt_custom','openai_plugin'):
    check(candidates.get(rid,{}).get('activate_by_default') is True,f'{rid} must be active')
for rid in ('claude_project','opencode'):
    check(candidates.get(rid,{}).get('activate_by_default') is False,f'{rid} must remain inactive')
    check(candidates.get(rid,{}).get('suitability')=='reduced',f'{rid} must be reduced')
check(candidates.get('openai_plugin',{}).get('suitability')=='ready','openai_plugin must be ready')

plugin=cfg.get('runtime',{}).get('openai_plugin',{})
check(plugin.get('enabled') is True,'plugin must be enabled')
check(plugin.get('mode')=='skills_first','plugin mode mismatch')
check(plugin.get('compatibility')=='ready_runtime_dependent','plugin compatibility mismatch')
for key in ('filesystem_read','filesystem_write','code_execution','persistent_state'):
    check(plugin.get(key)=='required_host_runtime',f'plugin dependency mismatch: {key}')
check(plugin.get('web_research')=='conditional_host_runtime','plugin web dependency mismatch')
check(plugin.get('state_authority')=='project_files','plugin state authority mismatch')
check(plugin.get('conversation_fallback') is False,'plugin conversation fallback must be false')
check(plugin.get('mcp_generated') is False,'plugin must not generate MCP')

model=parity.get('runtimes',{}).get('openai_plugin',{})
check(model.get('active') is True and model.get('suitability')=='ready','runtime-parity plugin activation mismatch')
check(model.get('compatibility')=='ready_runtime_dependent','runtime-parity plugin compatibility mismatch')

if errors:
    print('RUNTIME PARITY: FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('RUNTIME PARITY: PASS')
print('active: chatgpt_chat, chatgpt_custom, openai_plugin')
print('inactive assessed: claude_project, opencode')
