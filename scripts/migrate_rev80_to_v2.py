#!/usr/bin/env python3
"""Controlled migration/reconstruction of the rev80 extended-legacy reference project.

This adapter exists because rev80 predates the standardized v1 manifest envelope.
It preserves the source, upgrades only semantics proven by the frozen reconstruction,
and keeps non-native supporting artifacts verbatim with an explicit migration map.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import yaml

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'compatibility/reference-projects/rev80/metamodel.yaml'

def ly(p): return yaml.safe_load(Path(p).read_text(encoding='utf-8'))
def dy(p,d): Path(p).parent.mkdir(parents=True,exist_ok=True); Path(p).write_text(yaml.safe_dump(d,allow_unicode=True,sort_keys=False),encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def products(root:Path):
    d=ly(root/'supporting/market-product-catalog.yaml'); rows=[]
    for area in d.get('areas',[]):
        for x in area.get('products',[]): rows.append(x)
    by={x['id']:x for x in rows}
    return by

def realization_rows(root:Path):
    d=ly(root/'supporting/market-product-service-realization.yaml'); out=[]
    for prof in d.get('product_platform_profiles',[]):
        for sr in prof.get('service_realization',[]):
            out.append((prof,sr))
    return out

def inspect(source:Path)->dict[str,Any]:
    m=json.loads((source/'project-manifest.json').read_text(encoding='utf-8')); ref=ly(REF)['detection_signature']
    if m.get('schema_version')!='1.0' or m.get('revision')!=80 or m.get('file_count')!=245: raise ValueError('Källan matchar inte rev80 flat-manifest-signaturen.')
    for rel in ref['required_paths']:
        if not (source/rel).is_file(): raise ValueError(f'Saknar rev80-signaturfil: {rel}')
    def count_obj(fn): return len((ly(source/fn) or {}).get('objects',[]))
    rels=(ly(source/'model/relations.yaml') or {}).get('relations',[])
    srcs=(ly(source/'model/sources.yaml') or {}).get('sources',[])
    prod=products(source); rr=realization_rows(source)
    roles=(ly(source/'supporting/relation-roles.yaml') or {}).get('roles',{})
    dep=(ly(source/'supporting/market-product-deployment-model.yaml') or {}).get('products',[])
    op=(ly(source/'supporting/market-product-openness-model.yaml') or {}).get('products',[])
    mat=ly(source/'supporting/platform-structure-maturity-assessment.yaml') or {}
    retired=(ly(source/'supporting/retired-actual-platform-candidates.yaml') or {}).get('retired_ids',[])
    support=list((source/'supporting').glob('*.yaml'))
    queries=list((source/'supporting').glob('query-*.yaml'))
    freeze=ly(source/'supporting/model-freeze-baseline.yaml') or {}
    change=ly(source/'supporting/model-change-control.yaml') or {}
    positive=[(p,s) for p,s in rr if s.get('realization_level')!='not_supported']
    return {'manifest':m,'capabilities':count_obj('model/capabilities.yaml'),'it_supports':count_obj('model/it-support.yaml'),'platform_services':count_obj('model/platform-services.yaml'),'platforms':count_obj('model/platforms.yaml'),'relations':len(rels),'sources':len(srcs),'products':len(prod),'realization_rows':len(rr),'positive_realizations':len(positive),'relation_roles':len(roles),'deployment_products':len(dep),'openness_products':len(op),'maturity_summary':mat.get('summary',{}),'retired_actual_platforms':len(retired),'supporting_yaml':len(support),'derived_view_files':len(queries),'freeze_baseline_id':freeze.get('baseline_id'),'freeze_status':freeze.get('status'),'change_classes':[x.get('id') for x in change.get('change_classes',[]) if isinstance(x,dict)]}

def project_metamodel()->dict:
    return {'schema_version':'2.0','project_metamodel':{
      'id':'it-formagemodell-del3-rev80-v2','version':'2.0-migrated-rev80','description':'Kontrollerad v2-rekonstruktion av rev80 extended legacy. Native v2-semantik används endast där rev80-rekonstruktionen ger entydigt stöd.',
      'base_profile':{'id':'ea-stodjare-v2','version':'2.0','compatibility_mode':'extended_legacy'},
      'object_types':{'enabled':['capability','it_support','platform_service','platform'],'disabled':['driver','goal','principle','standard','solution_pattern','reference_architecture','product'],'custom':[]},
      'attribute_extensions':[],
      'relations':{'enabled':['supports','uses','related_to','provided_by'],'disabled':['realized_by','can_realize','influences','governed_by','constrains','depends_on','derived_from'],'custom':[]},
      'relation_qualifiers':[{'name':'relation_role','applies_to':['related_to','supports','uses'],'type':'enum','value_set':'rev80_relation_role','description':'Rev80:s analytiska relationsroll.'}],
      'value_sets':[{'id':'rev80_relation_role','values':['responsibility_boundary','cross_capability_support','information_dependency','lifecycle_dependency','operational_dependency']}],
      'extensions':[{'id':'ea.product-deployment','version':'1.0','enabled':False,'configuration':{}},{'id':'ea.product-openness','version':'1.0','enabled':False,'configuration':{}},{'id':'ea.platform-maturity','version':'1.0','enabled':False,'configuration':{}}],
      'derived_views':[],
      'presentation':{'contract':'reader-oriented-v1','object_display_pattern':'{name} ({id})','labels':{'capability.in_scope':'Stödjer','capability.out_of_scope':'Omfattar inte','provided_by':'Tillhandahålls av'}},
      'governance':{'change_control':True,'baseline_id':'IT-FORMAGEMODELL-CONCEPTUAL-v1.1','freeze_status':'frozen','baseline_version':'1.1','retired_id_registry':'migration/rev80-retired-ids.yaml','model_changelog':None,'metamodel_changelog':None},
      'notes':['Marknadsprodukt-, deployment-, openness- och maturity-underlag bevaras som explicit legacy-support i detta steg; de verifieras och mappas men flyttas inte tyst till conceptual/actual state.','Rev80:s PLS→PLT realized_by är entydigt konceptuell hemvist och migreras därför till provided_by.']}}

def apply(source:Path,target:Path):
    if target.exists(): raise FileExistsError(target)
    stats=inspect(source); shutil.copytree(source,target)
    # Preserve original flat manifest for audit.
    (target/'migration').mkdir(parents=True, exist_ok=True)
    shutil.copy2(target/'project-manifest.json',target/'migration/rev80-source-manifest.json')
    # Proven semantic conversion: PLS -> PLT home.
    rp=target/'model/relations.yaml'; d=ly(rp); roles=(ly(target/'supporting/relation-roles.yaml') or {}).get('roles',{})
    converted=0; role_applied=0
    for r in d.get('relations',[]):
        if r.get('type')=='realized_by' and str(r.get('source','')).startswith('PLS-') and str(r.get('target','')).startswith('PLT-'):
            r['type']='provided_by'; converted+=1
        role=(roles.get(r.get('id')) or {}).get('relation_role')
        if role and r.get('type') in {'related_to','supports','uses'}:
            r['relation_role']=role; role_applied+=1
    dy(rp,d)
    dy(target/'project-metamodel.yaml',project_metamodel())
    retired=ly(target/'supporting/retired-actual-platform-candidates.yaml').get('retired_ids',[])
    dy(target/'migration/rev80-retired-ids.yaml',{'schema_version':'1.0','policy':'retire_never_reuse','retired_ids':[{'id':x['id'],'reason':'Pensionerad actual-platform-kandidat från rev80; får inte återanvändas.'} for x in retired]})
    report={'schema_version':'1.0','migration':{'profile':'rev80-extended-legacy','source_revision':80,'source_manifest_sha256':sha(source/'project-manifest.json'),'target_revision':81,'status':'applied_with_preserved_legacy_support','counts':stats|{'provided_by_converted':converted,'relation_roles_applied':role_applied},'transformations':[
      {'id':'REV80-MIG-001','action':'realized_by_to_provided_by','count':converted,'basis':'rev80 reconstruction explicitly defines all PLS→PLT realized_by as conceptual home'},
      {'id':'REV80-MIG-002','action':'relation_role_merged','count':role_applied,'basis':'supporting/relation-roles.yaml'},
      {'id':'REV80-MIG-003','action':'legacy_support_preserved','count':stats['supporting_yaml'],'basis':'No silent epistemic reclassification; supporting YAML remains byte-preserved except migration files are added outside supporting/'},
      {'id':'REV80-MIG-004','action':'retired_ids_registered','count':stats['retired_actual_platforms'],'basis':'retire_never_reuse'}],
      'epistemic_guards':['market product reference != actual organizational use','product-service realization != actual use','retired actual-platform candidates remain retired','derived/query views remain non-canonical'],
      'native_v2_deferred':['market product catalog normalization to Product objects','can_realize materialization','deployment/openness attribute materialization','platform maturity attribute materialization','derived-view regeneration','full governance-log normalization'],
      'supporting_byte_preserved':all(sha(source/'supporting'/p.name)==sha(target/'supporting'/p.name) for p in (source/'supporting').glob('*.yaml')),'information_loss_hidden':False}}
    dy(target/'migration/rev80-migration-report.yaml',report)
    # New standardized manifest. Supporting files are retained as support.
    now='2026-08-25T00:00:00+00:00'; files=[]
    for p in sorted(x for x in target.rglob('*') if x.is_file() and x.name!='project-manifest.json' and '__pycache__' not in x.parts):
        rel=p.relative_to(target).as_posix(); role='canonical_model' if rel.startswith('model/') else ('governance' if rel.startswith('migration/') or rel=='project-metamodel.yaml' else ('documentation_source' if rel.endswith('.md') else 'support'))
        files.append({'path':rel,'role':role,'required':rel.startswith('model/') or rel in {'project-metamodel.yaml','migration/rev80-migration-report.yaml'},'sha256':sha(p)})
    manifest={'format':'ea-stodjare-project','format_version':'1.0','project':{'id':'it-formagemodell-del3-rev80-v2','name':'IT-förmågemodell del 3 rev80 – migrerad v2','kind':'enterprise-architecture','language':'sv','revision':81,'created_at':now,'updated_at':now,'lifecycle_status':'review'},'model':{'root':'model','serialization':'YAML','model_format_version':'1.0','metamodel_version':'2.0','relation_model_version':'2.0','provenance_model_version':'1.0'},'integrity':{'algorithm':'sha256','manifest_self_hash':False,'inventory_order':'path-ascending','canonical_model_required':True},'files':files}
    (target/'project-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return report

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',type=Path,required=True); ap.add_argument('--mode',choices=['inspect','apply'],default='inspect'); ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    if a.mode=='inspect': print(yaml.safe_dump({'rev80':inspect(a.source)},allow_unicode=True,sort_keys=False)); return
    if not a.output: ap.error('--output krävs för apply')
    print(yaml.safe_dump(apply(a.source,a.output),allow_unicode=True,sort_keys=False))
if __name__=='__main__': main()
