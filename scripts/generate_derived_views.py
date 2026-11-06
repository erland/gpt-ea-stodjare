#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
import yaml


def load_yaml(p: Path):
    return yaml.safe_load(p.read_text(encoding='utf-8')) or {}


def fingerprint(paths):
    h=hashlib.sha256()
    for p in sorted(paths, key=lambda x: str(x)):
        h.update(str(p.name).encode()); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
    return h.hexdigest()


def get_field(row: dict[str,Any], expr: str):
    alias, field = expr.split('.',1)
    obj=row.get(alias) or {}
    return obj.get(field)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root', default='.')
    ap.add_argument('--catalog', default='derived-views/views.yaml')
    ap.add_argument('--output-dir', default='build/derived-views')
    a=ap.parse_args(); root=Path(a.project_root).resolve()
    catalog_path=root/a.catalog
    if not catalog_path.exists(): catalog_path=Path(__file__).resolve().parents[1]/a.catalog
    catalog=load_yaml(catalog_path)
    model_files=[p for p in (root/'model').glob('*.yaml') if p.name!='relations.yaml']
    objects={}; by_type={}
    for p in model_files:
        d=load_yaml(p); typ=d.get('object_type')
        for o in d.get('objects',[]) or []:
            x=dict(o); x['object_type']=typ; objects[x['id']]=x; by_type.setdefault(typ,[]).append(x)
    rels=(load_yaml(root/'model/relations.yaml').get('relations') or [])
    outdir=Path(a.output_dir); outdir = outdir if outdir.is_absolute() else root/outdir; outdir.mkdir(parents=True, exist_ok=True)
    fp=fingerprint(model_files+[root/'model/relations.yaml', catalog_path])
    for v in catalog.get('views',[]):
        alias=v['anchor']['alias']; rows=[]
        for typ in v['anchor']['object_types']:
            for o in by_type.get(typ,[]): rows.append({alias:o})
        for step in v.get('join_path',[]):
            nxt=[]; relnames=step['relation']; relnames=[relnames] if isinstance(relnames,str) else relnames
            prior_alias=list(rows[0].keys())[-1] if rows else None
            for row in rows:
                current=row.get(prior_alias) if prior_alias else None
                if not current: continue
                for r in rels:
                    if r.get('type') not in relnames: continue
                    src=r.get('source', r.get('source_id')); tgt=r.get('target', r.get('target_id'))
                    if step['direction']=='forward' and src==current.get('id'):
                        oid=tgt
                    elif step['direction']=='reverse' and tgt==current.get('id'):
                        oid=src
                    else: continue
                    obj=objects.get(oid)
                    if not obj: continue
                    if step.get('target_types') and obj.get('object_type') not in step['target_types']: continue
                    nr=dict(row); nr[step['alias']]=obj; nxt.append(nr)
            rows=nxt
        for f in v.get('filters',[]) or []:
            if f.get('kind')=='not_equal': rows=[r for r in rows if get_field(r,f['left']) != get_field(r,f['right'])]
        # flatten rows to stable scalar representation
        flat=[]
        for row in rows:
            rr={}
            for al,obj in row.items():
                rr[f'{al}.id']=obj.get('id'); rr[f'{al}.name']=obj.get('name'); rr[f'{al}.object_type']=obj.get('object_type')
            flat.append(rr)
        if v.get('deduplicate_rows', True):
            uniq={json.dumps(r,sort_keys=True,ensure_ascii=False):r for r in flat}; flat=list(uniq.values())
        agg=v.get('aggregation')
        if agg:
            groups={}
            for r in flat:
                key=tuple(r.get(k) for k in agg['group_by']); groups.setdefault(key,[]).append(r)
            af=[]
            for key,items in groups.items():
                rr={k:val for k,val in zip(agg['group_by'],key)}
                for m in agg['metrics']:
                    vals=[x.get(m['field']) for x in items]
                    rr[m['name']]=len(set(vals)) if m['operation']=='count_distinct' else len(vals)
                af.append(rr)
            flat=af
        for key in reversed(v.get('sort',[]) or []): flat.sort(key=lambda r: (r.get(key) is None, str(r.get(key,''))))
        payload={'view_id':v['id'],'source_of_truth':False,'regeneration_policy':v['regeneration_policy'],'input_fingerprint_sha256':fp,'rows':flat}
        (outdir/f"{v['id']}.yaml").write_text(yaml.safe_dump(payload,allow_unicode=True,sort_keys=False),encoding='utf-8')
    print(f"OK: genererade {len(catalog.get('views',[]))} derived views i {outdir}")

if __name__=='__main__': main()
