#!/usr/bin/env python3
from __future__ import annotations
import copy, json, re, unicodedata
from pathlib import Path
from typing import Any
import yaml

from presentation_contract import load_contract, field_label, relation_label, object_display
try:
    from resolve_project_metamodel import resolve as resolve_metamodel, ExtensionResolutionError
except Exception:
    resolve_metamodel = None
    ExtensionResolutionError = RuntimeError

CORE_FILES = {
 'driver': ('drivers.yaml','drivkrafter','Drivkrafter'),
 'goal': ('goals.yaml','mal','Mål'),
 'principle': ('principles.yaml','principer','Principer'),
 'capability': ('capabilities.yaml','formagor','Förmågor'),
 'it_support': ('it-support.yaml','it-stod','IT-stöd'),
 'platform_service': ('platform-services.yaml','plattformstjanster','Plattformstjänster'),
 'platform': ('platforms.yaml','plattformar','Plattformar'),
 'product': ('products.yaml','produkter','Produkter'),
 'standard': ('standards.yaml','standarder','Standarder'),
 'solution_pattern': ('solution-patterns.yaml','losningsmonster','Lösningsmönster'),
 'reference_architecture': ('reference-architectures.yaml','referensarkitekturer','Referensarkitekturer'),
}
STATUS={'working':{'candidate','approved','deprecated'},'published':{'approved'}}
FALLBACK_LABELS={
 'description':'Beskrivning','status':'Status','category':'Kategori','time_horizon':'Tidshorisont','target_state':'Måltillstånd','measure':'Mått',
 'capability_type':'Förmågetyp','in_scope':'Omfattar','out_of_scope':'Omfattar inte','consumer_scope':'Avsedda konsumenter',
 'functions':'Funktioner','lifecycle':'Livscykel','criticality':'Kritikalitet','service_level':'Servicenivå','realization_pattern':'Realiseringsmönster',
 'technology':'Teknik','products':'Produkter','product_kind':'Produkttyp','vendor':'Leverantör','website':'Webbplats','version':'Version','market_notes':'Marknadsnotering',
 'standard_type':'Standardtyp','reference':'Referens','mandatory':'Obligatorisk','scope':'Scope','applicability':'Tillämplighet','building_blocks':'Byggblock','guidance':'Vägledning',
 'statement':'Principformulering','rationale':'Motivering','implications':'Implikationer','problem':'Problem','context':'Kontext','approach':'Angreppssätt','consequences':'Konsekvenser',
 'owner':'Ägare','aliases':'Alias','tags':'Taggar','notes':'Arbetsnotering'
}


def load_yaml(p:Path)->dict:
    return yaml.safe_load(p.read_text(encoding='utf-8')) or {}

def slug(s:str)->str:
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'(^-|-$)','',re.sub(r'[^a-z0-9]+','-',s)) or 'objekt'

def _metamodel_path(root:Path)->Path|None:
    for p in [root/'model-definition/project-metamodel.yaml', root/'project-metamodel.yaml']:
        if p.exists(): return p
    return None

def _core_specs(repo_root:Path)->dict[str,dict]:
    obj=load_yaml(repo_root/'schemas/object-types.yaml').get('object_types',{})
    result={}
    for typ,(fn,folder,title) in CORE_FILES.items():
        spec=copy.deepcopy(obj.get(typ,{}) or {})
        spec.update({'type':typ,'model_file':fn,'folder':folder,'display_name':spec.get('display_name') or title,'catalog_title':title})
        result[typ]=spec
    return result

def build_context(project_root:Path, repo_root:Path|None=None, mode:str='working')->dict[str,Any]:
    root=project_root.resolve(); repo=(repo_root or Path(__file__).resolve().parents[1]).resolve(); model=root/'model'
    contract=load_contract(repo)
    core=_core_specs(repo)
    pm_path=_metamodel_path(root); resolved=None
    if pm_path and resolve_metamodel:
        resolved=resolve_metamodel(pm_path,repo)
        pm=resolved['project_metamodel']
        enabled=list(pm.get('object_types',{}).get('enabled',[]))
        disabled=set(pm.get('object_types',{}).get('disabled',[]))
        enabled_set=set(enabled); core_order=list(CORE_FILES)
        active=[t for t in core_order if t in enabled_set and t not in disabled]
        active += [t for t in enabled if t not in disabled and t not in active]
        custom=list(pm.get('object_types',{}).get('custom',[]))
        for c in custom:
            typ=c['type']; fn=c.get('model_file') or f"{typ.replace('_','-')}.yaml"; title=c.get('display_name') or typ.replace('_',' ').title()
            core[typ]={**c,'type':typ,'model_file':fn,'folder':typ.replace('_','-'),'display_name':title,'catalog_title':title}
            if typ not in active: active.append(typ)
        # Project and extension presentation labels override the standard contract.
        labels=(pm.get('presentation') or {}).get('labels') or {}
        labels={**labels, **((resolved or {}).get('project_metamodel',{}).get('presentation',{}).get('labels') or {})}
        for key,val in labels.items():
            if '.' in key:
                typ,field=key.split('.',1); contract.setdefault('field_labels',{}).setdefault(typ,{})[field]=val
            else:
                contract.setdefault('relation_labels',{}).setdefault(key,{'forward':val,'reverse':val})['forward']=val
        for typ,pattern in (resolved.get('extension_object_display_patterns') or {}).items():
            contract.setdefault('object_display',{}).setdefault('patterns_by_type',{})[typ]=pattern
        active_rel=set(pm.get('relations',{}).get('enabled',[])) | {r['type'] for r in pm.get('relations',{}).get('custom',[])}
        active_rel -= set(pm.get('relations',{}).get('disabled',[]))
    else:
        # Legacy / simple projects: preserve historical behavior by using only model files actually present.
        active=[t for t,s in core.items() if (model/s['model_file']).exists()]
        active_rel=None
    specs=[core[t] for t in active if t in core]
    by_type={}; all_objects={}
    for spec in specs:
        p=model/spec['model_file']; objs=load_yaml(p).get('objects',[]) if p.exists() else []
        objs=[o for o in objs if o.get('status') in STATUS[mode]]
        objs=sorted(objs,key=lambda o:((o.get('capability_type','') if spec['type']=='capability' else ''),o.get('name','').casefold(),o.get('id','')))
        by_type[spec['type']]=objs; all_objects.update({o['id']:o for o in objs})
    rels=load_yaml(model/'relations.yaml').get('relations',[]) if (model/'relations.yaml').exists() else []
    rels=[r for r in rels if r.get('status') in STATUS[mode] and (active_rel is None or r.get('type') in active_rel)]
    sources={x['id']:x for x in load_yaml(model/'sources.yaml').get('sources',[])} if (model/'sources.yaml').exists() else {}
    manifest=json.loads((root/'project-manifest.json').read_text(encoding='utf-8')) if (root/'project-manifest.json').exists() else {}
    return {'root':root,'repo_root':repo,'model':model,'contract':contract,'resolved_metamodel':resolved,'specs':specs,'by_type':by_type,'all_objects':all_objects,'relations':rels,'sources':sources,'manifest':manifest,'mode':mode}

def label(ctx:dict, typ:str, field:str, obj:dict|None=None)->str:
    v=field_label(ctx['contract'],typ,field,obj)
    return FALLBACK_LABELS.get(field,field.replace('_',' ').capitalize()) if v==field else v

def rel_label(ctx:dict, typ:str, direction:str)->str:
    lookup='realized_by' if typ=='legacy_realized_by' else typ
    v=relation_label(ctx['contract'],lookup,direction)
    return v if v!=lookup else typ.replace('_',' ').capitalize()

def display(ctx:dict,obj:dict)->str:
    return object_display(ctx['contract'],obj)

def fmt_value(v:Any)->str:
    if v is None: return ''
    if isinstance(v,bool): return 'ja' if v else 'nej'
    if isinstance(v,list):
        vals=[]
        for x in v:
            if isinstance(x,dict):
                name=x.get('name') or x.get('id')
                if name:
                    details=[]
                    if x.get('description'): details.append(str(x['description']))
                    if 'required' in x: details.append('obligatorisk' if x['required'] else 'valfri')
                    vals.append(str(name)+(f" — {', '.join(details)}" if details else ''))
                else: vals.append(json.dumps(x,ensure_ascii=False,sort_keys=True))
            else: vals.append(str(x))
        return ', '.join(vals)
    if isinstance(v,dict): return json.dumps(v,ensure_ascii=False,sort_keys=True)
    return str(v)

def visible_fields(ctx:dict,spec:dict,obj:dict)->list[str]:
    common={'id','type','name','description','status','provenance','owner','aliases','tags','notes'}
    declared=[]
    for k in ('required_attributes','recommended_attributes','optional_attributes'):
        declared.extend(spec.get(k) or [])
    for a in spec.get('attributes',[]) or []: declared.append(a['name'])
    # Include extension/custom attributes present in data, but keep common metadata separate.
    extras=[k for k in obj if k not in common and k not in declared]
    seen=set(); fields=[]
    for f in declared+extras:
        if f not in seen and f not in common and f in obj and obj[f] not in (None,'',[]): fields.append(f); seen.add(f)
    return fields

def _get_field(row:dict, expr:str):
    alias,field=expr.split('.',1); return (row.get(alias) or {}).get(field)

def compute_view_rows(ctx:dict, view_id:str)->list[dict]:
    catalog=load_yaml(ctx['repo_root']/'derived-views/views.yaml')
    v=next((x for x in catalog.get('views',[]) if x.get('id')==view_id),None)
    if not v: return []
    by_type=ctx['by_type']; objects=ctx['all_objects']; rels=ctx['relations']
    alias=v['anchor']['alias']; rows=[]
    for typ in v['anchor']['object_types']:
        for o in by_type.get(typ,[]): rows.append({alias:o})
    current_alias=alias
    for step in v.get('join_path',[]):
        nxt=[]; relnames=step['relation']; relnames=[relnames] if isinstance(relnames,str) else relnames
        for row in rows:
            current=row.get(current_alias)
            if not current: continue
            for r in rels:
                if r.get('type') not in relnames: continue
                oid=None
                if step['direction']=='forward' and r.get('source')==current.get('id'): oid=r.get('target')
                elif step['direction']=='reverse' and r.get('target')==current.get('id'): oid=r.get('source')
                if not oid: continue
                obj=objects.get(oid)
                if not obj or (step.get('target_types') and obj.get('type') not in step['target_types']): continue
                nr=dict(row); nr[step['alias']]=obj; nxt.append(nr)
        rows=nxt; current_alias=step['alias']
    for f in v.get('filters',[]) or []:
        if f.get('kind')=='not_equal': rows=[r for r in rows if _get_field(r,f['left']) != _get_field(r,f['right'])]
    # Navigation views use non-aggregated rows. Aggregated views remain available to the standalone derived-view generator.
    uniq={json.dumps({a:o.get('id') for a,o in r.items()},sort_keys=True):r for r in rows}
    rows=list(uniq.values())
    for key in reversed(v.get('sort',[]) or []): rows.sort(key=lambda r:( _get_field(r,key) is None, str(_get_field(r,key) or '').casefold()))
    return rows

def navigation_for_object(ctx:dict,obj:dict)->list[dict]:
    sections=[]; typ=obj.get('type')
    for sec in (ctx['contract'].get('navigation_sections') or {}).get(typ,[]) or []:
        rows=compute_view_rows(ctx,sec['derived_view'])
        view=next((v for v in load_yaml(ctx['repo_root']/'derived-views/views.yaml').get('views',[]) if v.get('id')==sec['derived_view']),{})
        anchor_alias=(view.get('anchor') or {}).get('alias')
        rows=[r for r in rows if (r.get(anchor_alias) or {}).get('id')==obj.get('id')]
        items=[]
        for row in rows:
            parts=[]
            for alias,target in row.items():
                if alias==anchor_alias: continue
                parts.append(display(ctx,target))
            if parts: items.append(' → '.join(parts))
        items=sorted(set(items),key=str.casefold)
        if items or sec.get('when_empty')!='omit':
            sections.append({'title':sec['title'],'items':items,'epistemic_note':sec.get('epistemic_note'),'source_of_truth':False,'derived_view':sec['derived_view']})
    return sections
