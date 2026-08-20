#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, unicodedata
from pathlib import Path
import yaml

TYPE_CFG = {
 'driver': ('drivers.yaml','drivkrafter.md','drivers','Drivkrafter','drivers-catalog.md','driver-detail.md'),
 'goal': ('goals.yaml','mal.md','goals','Mål','goals-catalog.md','goal-detail.md'),
 'principle': ('principles.yaml','principer.md','principles','Principer','principles-catalog.md','principle-detail.md'),
 'capability': ('capabilities.yaml','formagor.md','capabilities','Förmågor','capabilities-catalog.md','capability-detail.md'),
 'it_support': ('it-support.yaml','it-stod.md','it-support','IT-stöd','it-support-catalog.md','it-support-detail.md'),
 'platform_service': ('platform-services.yaml','plattformstjanster.md','platform-services','Plattformstjänster','platform-services-catalog.md','platform-service-detail.md'),
 'platform': ('platforms.yaml','plattformar.md','platforms','Plattformar','platforms-catalog.md','platform-detail.md'),
 'standard': ('standards.yaml','standarder.md','standards','Standarder','standards-catalog.md','standard-detail.md'),
 'solution_pattern': ('solution-patterns.yaml','losningsmonster.md','solution-patterns','Lösningsmönster','solution-patterns-catalog.md','solution-pattern-detail.md'),
 'reference_architecture': ('reference-architectures.yaml','referensarkitekturer.md','reference-architectures','Referensarkitekturer','reference-architectures-catalog.md','reference-architecture-detail.md'),
}
STATUS = {'working': {'candidate','approved','deprecated'}, 'published': {'approved'}}
REL_LABELS = {
 'influences': ('Påverkar','Påverkas av'), 'supports': ('Stödjer','Stöds av'), 'uses': ('Använder','Används av'),
 'realized_by': ('Realiseras av','Realiserar'), 'governed_by': ('Styrs av','Styr'), 'constrains': ('Begränsar','Begränsas av'),
 'depends_on': ('Beror på','Är beroende för'), 'derived_from': ('Härleds från','Ligger till grund för'), 'related_to': ('Relaterar till','Relaterar till')}

def load_yaml(p):
    return yaml.safe_load(p.read_text(encoding='utf-8')) or {}

def slug(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'(^-|-$)','',re.sub(r'[^a-z0-9]+','-',s)) or 'objekt'

def esc(s):
    if s is None: return ''
    return str(s).replace('\\','\\\\').replace('|','\\|').replace('\n',' ')

def fmt_list(v):
    if not v: return ''
    if isinstance(v, list):
        vals=[]
        for x in v:
            vals.append(str(x.get('name','')) if isinstance(x,dict) else str(x))
        return ', '.join(vals)
    return str(v)

def bullets(v):
    if not v: return ''
    if not isinstance(v,list): v=[v]
    vals=[]
    for x in v:
        if isinstance(x,dict): x=x.get('name') or x.get('id') or json.dumps(x,ensure_ascii=False)
        vals.append(f'- {x}')
    return '\n'.join(vals)

def render(template, vals):
    out=template
    for k,v in vals.items(): out=out.replace('{{'+k+'}}', v or '')
    out=re.sub(r'\n## [^\n]+\n\n(?=\n## |\Z)', '\n', out)
    out=re.sub(r'\n{3,}','\n\n',out).rstrip()+"\n"
    return out

def attrs(obj, fields):
    rows=[]
    labels={'category':'Kategori','time_horizon':'Tidshorisont','target_state':'Måltillstånd','capability_type':'Förmågetyp','lifecycle':'Livscykel','criticality':'Kritikalitet','consumer_scope':'Konsumentomfång','service_level':'Servicenivå','technology':'Teknik','products':'Produkter','standard_type':'Standardtyp','reference':'Referens','version':'Version','mandatory':'Obligatorisk'}
    for f in fields:
        if f in obj and obj[f] not in (None,'',[]): rows.append(f'- **{labels.get(f,f)}:** {fmt_list(obj[f])}')
    return '\n'.join(rows)

def provenance(obj, sources, mode):
    ev=obj.get('provenance') or []
    if not ev: return ''
    lines=['## Proveniens']
    for e in ev:
        sid=e.get('source_id'); src=sources.get(sid,{}) if sid else {}
        label=e.get('evidence_type','okänd')
        bits=[]
        if sid: bits.append(f"källa: {src.get('title',sid)} (`{sid}`)")
        if e.get('reference'): bits.append(f"referens: {e['reference']}")
        if mode=='working' and e.get('confidence'): bits.append(f"confidence: {e['confidence']}")
        if mode=='working' and e.get('transferability'): bits.append(f"överförbarhet: {e['transferability']}")
        lines.append(f"- **{label}**" + (f" — {'; '.join(bits)}" if bits else ''))
        if mode=='working' and e.get('rationale'): lines.append(f"  - Motiv: {e['rationale']}")
        if mode=='working' and e.get('derived_from'): lines.append(f"  - Härledd från: {', '.join(e['derived_from'])}")
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--project-root',default='.')
    ap.add_argument('--mode',choices=['working','published'],default='working')
    ap.add_argument('--output-dir',default='docs/generated')
    args=ap.parse_args()
    root=Path(args.project_root).resolve(); model=root/'model'; templates=(Path(__file__).resolve().parents[1]/'templates/markdown')
    out=(root/args.output_dir); out.mkdir(parents=True,exist_ok=True)
    manifest={}
    if (root/'project-manifest.json').exists(): manifest=json.loads((root/'project-manifest.json').read_text(encoding='utf-8'))
    rev=manifest.get('project',{}).get('revision','-')
    sources={x['id']:x for x in load_yaml(model/'sources.yaml').get('sources',[])} if (model/'sources.yaml').exists() else {}
    all_objs={}; by_type={}
    for typ,cfg in TYPE_CFG.items():
        objs=load_yaml(model/cfg[0]).get('objects',[]) if (model/cfg[0]).exists() else []
        objs=[o for o in objs if o.get('status') in STATUS[args.mode]]
        if typ=='capability': objs=sorted(objs,key=lambda o:(o.get('capability_type',''),o.get('name','').casefold(),o.get('id','')))
        else: objs=sorted(objs,key=lambda o:(o.get('name','').casefold(),o.get('id','')))
        by_type[typ]=objs
        all_objs.update({o['id']:o for o in objs})
    rels=load_yaml(model/'relations.yaml').get('relations',[]) if (model/'relations.yaml').exists() else []
    rels=[r for r in rels if r.get('status') in STATUS[args.mode]]

    def detail_path(o):
        cfg=TYPE_CFG[o['type']]; return out/'objects'/cfg[2]/f"{o['id']}-{slug(o['name'])}.md"
    def rel_md(o):
        groups={}
        for r in rels:
            if r['source']==o['id']: other=r['target']; label=REL_LABELS.get(r['type'],(r['type'],r['type']))[0]
            elif r['target']==o['id']: other=r['source']; label=REL_LABELS.get(r['type'],(r['type'],r['type']))[1]
            else: continue
            target=all_objs.get(other)
            name=target.get('name',other) if target else other
            text=f"{name} (`{other}`)"
            if target:
                rp=Path(Path(detail_path(o)).parent).relative_to(out)
                relpath=Path(__import__('os').path.relpath(detail_path(target), start=detail_path(o).parent)).as_posix()
                text=f"[{name}]({relpath}) (`{other}`)"
            groups.setdefault((label,r['type']),[]).append(text)
        if not groups: return ''
        lines=['## Relationer']
        for (label,rt),items in sorted(groups.items()):
            lines += ['',f'### {label} (`{rt}`)'] + [f'- {x}' for x in sorted(items,key=str.casefold)]
        return '\n'.join(lines)

    meta_line=f"> Genererad från kanonisk YAML · läge `{args.mode}` · projektrevision `{rev}`"
    for typ,cfg in TYPE_CFG.items():
        objs=by_type[typ]
        rows=[]
        for o in objs:
            link=f"objects/{cfg[2]}/{o['id']}-{slug(o['name'])}.md"
            desc=esc(o.get('description',''))
            vals={
              'driver':[o['id'],f"[{esc(o['name'])}]({link})",desc,esc(o.get('category','')),o.get('status','')],
              'goal':[o['id'],f"[{esc(o['name'])}]({link})",desc,esc(o.get('time_horizon','')),o.get('status','')],
              'principle':[o['id'],f"[{esc(o['name'])}]({link})",esc(o.get('statement','')),o.get('status','')],
              'capability':[o['id'],f"[{esc(o['name'])}]({link})",esc(o.get('capability_type','')),desc,o.get('status','')],
              'it_support':[o['id'],f"[{esc(o['name'])}]({link})",desc,esc(fmt_list(o.get('functions'))),o.get('status','')],
              'platform_service':[o['id'],f"[{esc(o['name'])}]({link})",desc,esc(o.get('consumer_scope','')),esc(fmt_list(o.get('functions'))),o.get('status','')],
              'platform':[o['id'],f"[{esc(o['name'])}]({link})",desc,esc(' / '.join(filter(None,[str(o.get('technology','')),fmt_list(o.get('products'))]))),esc(fmt_list(o.get('functions'))),o.get('status','')],
              'standard':[o['id'],f"[{esc(o['name'])}]({link})",esc(o.get('standard_type','')),esc(' / '.join(filter(None,[str(o.get('reference','')),str(o.get('version',''))]))),esc(str(o.get('mandatory','')).lower() if 'mandatory' in o else ''),o.get('status','')],
              'solution_pattern':[o['id'],f"[{esc(o['name'])}]({link})",esc(' / '.join(filter(None,[str(o.get('problem','')),str(o.get('context',''))]))),o.get('status','')],
              'reference_architecture':[o['id'],f"[{esc(o['name'])}]({link})",esc(' / '.join(filter(None,[str(o.get('scope','')),str(o.get('applicability',''))]))),o.get('status','')],
            }[typ]
            rows.append('| '+' | '.join(vals)+' |')
        t=(templates/cfg[4]).read_text(encoding='utf-8')
        (out/cfg[1]).write_text(render(t,{'catalog_intro':f'Denna katalog visar {cfg[3].lower()} i EA-modellen.','generated_metadata':meta_line,'catalog_rows':'\n'.join(rows) if rows else '| _Inga objekt i valt läge_ |'+' |'*(len(rows[0].split('|'))-3) if rows else '', 'related_catalogs':''}),encoding='utf-8')
        for o in objs:
            p=detail_path(o); p.parent.mkdir(parents=True,exist_ok=True)
            metadata=f"- **ID:** `{o['id']}`\n- **Objekttyp:** `{o['type']}`\n- **Status:** `{o.get('status','')}`"
            additional=[]
            for f,label in [('owner','Ägare'),('aliases','Alias'),('tags','Taggar')]:
                if o.get(f): additional.append(f'- **{label}:** {fmt_list(o[f])}')
            if args.mode=='working' and o.get('notes'): additional.append(f"- **Arbetsnotering:** {o['notes']}")
            common={'name':o['name'],'metadata':metadata,'description':o.get('description',''),'relations':rel_md(o),'provenance':provenance(o,sources,args.mode),'additional_metadata':('## Övrig metadata\n\n'+'\n'.join(additional)) if additional else '', 'functions':bullets(o.get('functions'))}
            specific={
              'driver':{'driver_attributes':attrs(o,['category','time_horizon'])},
              'goal':{'goal_attributes':attrs(o,['target_state','time_horizon'])},
              'principle':{'statement':o.get('statement',''),'rationale':o.get('rationale',''),'implications':bullets(o.get('implications'))},
              'capability':{'capability_attributes':attrs(o,['capability_type'])},
              'it_support':{'it_support_attributes':attrs(o,['lifecycle','criticality'])},
              'platform_service':{'platform_service_attributes':attrs(o,['consumer_scope','service_level'])},
              'platform':{'platform_attributes':attrs(o,['technology','products'])},
              'standard':{'standard_attributes':attrs(o,['standard_type','reference','version','mandatory'])},
              'solution_pattern':{'problem':o.get('problem',''),'context':o.get('context',''),'approach':o.get('approach',''),'consequences':bullets(o.get('consequences'))},
              'reference_architecture':{'scope_and_applicability':attrs(o,['scope','applicability']),'building_blocks':bullets(o.get('building_blocks')),'guidance':bullets(o.get('guidance'))},
            }[typ]
            t=(templates/cfg[5]).read_text(encoding='utf-8')
            p.write_text(render(t,{**common,**specific}),encoding='utf-8')
    print(f"Generated Markdown in {out} ({args.mode})")
if __name__=='__main__': main()
