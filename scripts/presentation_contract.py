#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator


def load_contract(repo_root: Path) -> dict:
    p=repo_root/'presentation/presentation-contract.yaml'
    data=yaml.safe_load(p.read_text(encoding='utf-8')) or {}
    schema=json.loads((repo_root/'schemas/presentation-contract.schema.json').read_text(encoding='utf-8'))
    errs=sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e:list(e.path))
    if errs:
        raise ValueError('; '.join(f"{'/'.join(map(str,e.path))}: {e.message}" for e in errs))
    return data


def object_display(contract: dict, obj: dict) -> str:
    typ=obj.get('type') or obj.get('object_type')
    cfg=contract.get('object_display') or {}
    pattern=(cfg.get('patterns_by_type') or {}).get(typ) or cfg.get('default_pattern','{name} ({id})')
    return pattern.format_map({'name':obj.get('name',''), 'id':obj.get('id',''), 'type':typ or ''})


def field_label(contract: dict, object_type: str, field: str, obj: dict | None=None) -> str:
    rule=((contract.get('field_labels') or {}).get(object_type) or {}).get(field)
    if rule is None:
        return field
    if isinstance(rule,str):
        return rule
    label=rule.get('default',field)
    by=rule.get('by_attribute') or {}
    if obj is not None:
        value=obj.get(by.get('attribute'))
        label=(by.get('values') or {}).get(value,label)
    return label


def relation_label(contract: dict, relation_type: str, direction: str='forward') -> str:
    rule=(contract.get('relation_labels') or {}).get(relation_type) or {}
    return rule.get(direction,relation_type)


def navigation_sections(contract: dict, object_type: str) -> list[dict]:
    return list((contract.get('navigation_sections') or {}).get(object_type) or [])


def main() -> int:
    ap=argparse.ArgumentParser(description='Inspect the reader-oriented presentation contract.')
    ap.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument('--object-type')
    ap.add_argument('--field')
    ap.add_argument('--attribute',action='append',default=[],help='key=value, used for contextual field labels')
    ap.add_argument('--relation')
    ap.add_argument('--direction',choices=['forward','reverse'],default='forward')
    args=ap.parse_args()
    c=load_contract(args.repo_root.resolve())
    if args.relation:
        print(relation_label(c,args.relation,args.direction)); return 0
    if args.object_type and args.field:
        obj={}
        for raw in args.attribute:
            k,_,v=raw.partition('='); obj[k]=v
        print(field_label(c,args.object_type,args.field,obj)); return 0
    print(yaml.safe_dump(c,allow_unicode=True,sort_keys=False),end='')
    return 0

if __name__=='__main__': raise SystemExit(main())
