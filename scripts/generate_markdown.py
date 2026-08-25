#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os
from pathlib import Path
from generator_context import build_context, slug, label, rel_label, display, fmt_value, visible_fields, navigation_for_object


def esc(s): return str(s).replace('\\','\\\\').replace('|','\\|').replace('\n',' ')

def md_bullets(value):
    if not isinstance(value,list): value=[value]
    lines=[]
    for item in value:
        if isinstance(item,dict):
            name=item.get('name') or item.get('id') or json.dumps(item,ensure_ascii=False,sort_keys=True)
            suffix=[]
            if item.get('description'): suffix.append(item['description'])
            if 'required' in item: suffix.append('obligatorisk' if item['required'] else 'valfri')
            lines.append(f"- {name}" + (f" — {'; '.join(map(str,suffix))}" if suffix else ''))
        else: lines.append(f'- {item}')
    return lines

def provenance_lines(obj,sources,mode):
    ev=obj.get('provenance') or []
    if not ev: return []
    out=['## Proveniens','']
    for e in ev:
        sid=e.get('source_id'); src=sources.get(sid,{}) if sid else {}; bits=[]
        if sid: bits.append(f"källa: {src.get('title',sid)} (`{sid}`)")
        if e.get('reference'): bits.append(f"referens: {e['reference']}")
        if mode=='working' and e.get('confidence'): bits.append(f"confidence: {e['confidence']}")
        if mode=='working' and e.get('transferability'): bits.append(f"överförbarhet: {e['transferability']}")
        out.append(f"- **{e.get('evidence_type','okänd')}**"+(f" — {'; '.join(bits)}" if bits else ''))
        if mode=='working' and e.get('rationale'): out.append(f"  - Motiv: {e['rationale']}")
        if mode=='working' and e.get('derived_from'): out.append(f"  - Härledd från: {', '.join(e['derived_from'])}")
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default='.'); ap.add_argument('--mode',choices=['working','published'],default='working'); ap.add_argument('--output-dir',default='docs/generated'); a=ap.parse_args()
    ctx=build_context(Path(a.project_root),mode=a.mode); root=ctx['root']; out=Path(a.output_dir); out=out if out.is_absolute() else root/out; out.mkdir(parents=True,exist_ok=True)
    for p in out.rglob('*.md'): p.unlink()
    rev=ctx['manifest'].get('project',{}).get('revision','-')
    meta=f"> Genererad från kanonisk YAML · läge `{a.mode}` · projektrevision `{rev}` · presentationskontrakt `{ctx['contract'].get('contract',{}).get('id','-')}`"
    catalog_manifest=[]
    for spec in ctx['specs']:
        typ=spec['type']; objs=ctx['by_type'].get(typ,[]); cat_name=spec['folder']+'.md'; folder=spec['folder']; title=spec['catalog_title']
        lines=[f'# {title}','',meta,'',f'Denna katalog visar {title.lower()} i EA-modellen.','', '| ID | Namn | Beskrivning | Status |','| --- | --- | --- | --- |']
        if objs:
            for o in objs:
                link=f"objects/{folder}/{o['id']}-{slug(o['name'])}.md"
                lines.append(f"| {esc(o['id'])} | [{esc(o['name'])}]({link}) | {esc(o.get('description',''))} | {esc(o.get('status',''))} |")
        else: lines.append('| _Inga objekt i valt läge_ |  |  |  |')
        (out/cat_name).write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
        catalog_manifest.append({'type':typ,'title':title,'file':cat_name,'folder':folder,'object_count':len(objs)})
        ddir=out/'objects'/folder; ddir.mkdir(parents=True,exist_ok=True)
        for o in objs:
            d=[f"# {display(ctx,o)}",'',meta,'',f"- **ID:** `{o['id']}`",f"- **Objekttyp:** `{typ}`",f"- **Status:** `{o.get('status','')}`"]
            if o.get('description'): d += ['','## Beskrivning','',str(o['description'])]
            fields=visible_fields(ctx,spec,o)
            # Boundary is deliberately reader-oriented and comes before ordinary attributes.
            boundary=[f for f in ('in_scope','out_of_scope') if f in fields]
            if boundary:
                d += ['','## Avgränsning','']
                for f in boundary:
                    d += [f"### {label(ctx,typ,f,o)}",''] + md_bullets(o[f]) + ['']
                fields=[f for f in fields if f not in boundary]
            if 'functions' in fields:
                d += ['','## Funktioner',''] + md_bullets(o['functions'])
                fields.remove('functions')
            if fields:
                d += ['','## Egenskaper','']
                for f in fields: d.append(f"- **{label(ctx,typ,f,o)}:** {fmt_value(o[f])}")
            for nav in navigation_for_object(ctx,o):
                d += ['',f"## {nav['title']}",'']
                if nav.get('epistemic_note'): d += [f"> {nav['epistemic_note']}",'']
                d += [f'- {x}' for x in nav['items']]
            relgroups={}
            for r in ctx['relations']:
                if r.get('source')==o['id']: other=r.get('target'); direction='forward'
                elif r.get('target')==o['id']: other=r.get('source'); direction='reverse'
                else: continue
                target=ctx['all_objects'].get(other); text=f"{target.get('name',other) if target else other} (`{other}`)"
                if target:
                    target_spec=next((s for s in ctx['specs'] if s['type']==target.get('type')),None)
                    if target_spec:
                        relpath=os.path.relpath(out/'objects'/target_spec['folder']/f"{target['id']}-{slug(target['name'])}.md", start=ddir).replace(os.sep,'/')
                        text=f"[{target['name']}]({relpath}) (`{other}`)"
                relgroups.setdefault((rel_label(ctx,r.get('type',''),direction),r.get('type','')),[]).append(text)
            if relgroups:
                d += ['','## Relationer']
                for (lab,rt),items in sorted(relgroups.items()): d += ['',f"### {lab} (`{rt}`)"]+[f'- {x}' for x in sorted(items,key=str.casefold)]
            d += ['']+provenance_lines(o,ctx['sources'],a.mode)
            extras=[]
            for f in ('owner','aliases','tags'):
                if o.get(f): extras.append(f"- **{label(ctx,typ,f,o)}:** {fmt_value(o[f])}")
            if a.mode=='working' and o.get('notes'): extras.append(f"- **{label(ctx,typ,'notes',o)}:** {fmt_value(o['notes'])}")
            if extras: d += ['','## Övrig metadata','']+extras
            (ddir/f"{o['id']}-{slug(o['name'])}.md").write_text('\n'.join(d).rstrip()+'\n',encoding='utf-8')
    (out/'generation-manifest.json').write_text(json.dumps({'source_of_truth':False,'mode':a.mode,'revision':rev,'catalogs':catalog_manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Generated Markdown in {out} ({a.mode}), {len(catalog_manifest)} active object types')
if __name__=='__main__': main()
