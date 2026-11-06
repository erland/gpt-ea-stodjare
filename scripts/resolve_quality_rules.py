#!/usr/bin/env python3
"""Resolve the QA rule set for the project's effective metamodel."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any
import yaml

from resolve_project_metamodel import resolve, ExtensionResolutionError


def load_yaml(path: Path) -> dict[str, Any]:
    data=yaml.safe_load(path.read_text(encoding='utf-8'))
    return data if isinstance(data,dict) else {}


def legacy_mode(project_root: Path) -> bool:
    mp=project_root/'project-manifest.json'
    if not mp.is_file(): return False
    m=json.loads(mp.read_text(encoding='utf-8'))
    return str((m.get('model') or {}).get('metamodel_version',''))=='1.0'


def effective_metamodel(project_root: Path, repo_root: Path) -> dict[str,Any]:
    if legacy_mode(project_root):
        fmt=load_yaml(repo_root/'compatibility/ea-stodjare-v1/schemas/model-format.yaml')
        rel=load_yaml(repo_root/'compatibility/ea-stodjare-v1/schemas/relations.yaml')
        types=list(((load_yaml(repo_root/'compatibility/ea-stodjare-v1/schemas/object-types.yaml')).get('object_types') or {}).keys())
        return {'mode':'legacy_v1','object_types':types,'relation_types':list((rel.get('relation_types') or {}).keys()),'extensions':[],'extension_qa_rules':[], 'object_files': (fmt.get('file_structure') or {}).get('object_files',{})}
    pm=project_root/'project-metamodel.yaml'
    if pm.is_file():
        resolved=resolve(pm,repo_root)
        m=resolved['project_metamodel']
        enabled=list((m.get('object_types') or {}).get('enabled') or [])
        custom=[x.get('type') for x in ((m.get('object_types') or {}).get('custom') or []) if isinstance(x,dict)]
        rels=list((m.get('relations') or {}).get('enabled') or [])+[x.get('type') for x in ((m.get('relations') or {}).get('custom') or []) if isinstance(x,dict)]
        return {'mode':'native_v2_project','object_types':enabled+custom,'relation_types':rels,'extensions':resolved.get('resolved_extensions',[]),'extension_qa_rules':resolved.get('extension_qa_rules',[])}
    types=load_yaml(repo_root/'schemas/object-types.yaml')
    rel=load_yaml(repo_root/'schemas/relations.yaml')
    fmt=load_yaml(repo_root/'schemas/model-format.yaml')
    return {'mode':'native_v2_default','object_types':list((types.get('object_types') or {}).keys()),'relation_types':list((rel.get('relation_types') or {}).keys()),'extensions':[],'extension_qa_rules':[], 'object_files': (fmt.get('file_structure') or {}).get('object_files',{})}


def _rule_relevant(rule: dict[str,Any], active_types:set[str]) -> bool:
    applies=rule.get('applies_to')
    if isinstance(applies,list):
        return bool(set(applies)&active_types)
    # Model rules without explicit applies_to stay relevant unless their check name
    # explicitly names only disabled standard layers.
    check=str(rule.get('check',''))
    tokens={'driver':'driver','goal':'goal','capability':'capability','it_support':'it_support','platform_service':'platform_service','platform':'platform','product':'product','standard':'standard'}
    mentioned={typ for token,typ in tokens.items() if token in check}
    return not mentioned or bool(mentioned&active_types)


def resolve_quality(project_root: Path, repo_root: Path) -> dict[str,Any]:
    eff=effective_metamodel(project_root,repo_root)
    active=set(eff['object_types'])
    oq=load_yaml(repo_root/'schemas/object-quality-rules.yaml').get('quality_rules') or {}
    mq=load_yaml(repo_root/'schemas/model-quality-rules.yaml').get('quality_rules') or {}
    common=[]
    for raw in oq.get('common_rules',[]):
        if not _rule_relevant(raw,active): continue
        r=dict(raw); r['applies_to']=sorted(active); common.append(r)
    object_specific={k:v for k,v in (oq.get('object_type_rules') or {}).items() if k in active}
    model_groups={}
    for group,rules in (mq.get('rules') or {}).items():
        kept=[r for r in rules if _rule_relevant(r,active)]
        if kept: model_groups[group]=kept
    extension_rules=[]
    for rule in eff.get('extension_qa_rules',[]):
        if _rule_relevant(rule,active): extension_rules.append(rule)
    coverage={}
    for name,spec in (mq.get('coverage_profiles') or {}).items():
        row=dict(spec or {})
        if 'expected_layers' in row: row['expected_layers']=[x for x in row.get('expected_layers',[]) if x in active]
        coverage[name]=row
    return {
      'qa_resolution': {'source_of_truth':False,'mode':eff['mode'],'active_object_types':sorted(active),'active_relation_types':sorted(set(eff['relation_types'])),'resolved_extensions':eff.get('extensions',[])},
      'object_quality': {'common_rules':common,'object_type_rules':object_specific},
      'model_quality': {'coverage_profiles':coverage,'rules':model_groups},
      'extension_quality_rules':extension_rules,
    }


def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--project-root',type=Path,default=Path.cwd()); p.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1]); p.add_argument('--output',type=Path)
    a=p.parse_args()
    try: out=resolve_quality(a.project_root.resolve(),a.repo_root.resolve())
    except (OSError,ValueError,ExtensionResolutionError) as e:
        print(f'ERROR QA-RESOLVE: {e}'); return 2
    text=yaml.safe_dump(out,allow_unicode=True,sort_keys=False)
    if a.output: a.output.write_text(text,encoding='utf-8')
    else: print(text,end='')
    return 0
if __name__=='__main__': raise SystemExit(main())
