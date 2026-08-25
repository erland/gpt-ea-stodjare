#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from generator_context import build_context, slug, label, rel_label, display, fmt_value, visible_fields, navigation_for_object

def inline(v): return str(v).replace('\\','\\\\').replace('|','\\|').replace('\r',' ').replace('\n',' ')
def bullets(v):
    if not isinstance(v,list): v=[v]
    return [f"* {fmt_value(x)}" for x in v]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--project-root',default='.'); ap.add_argument('--mode',choices=['working','published'],default='working'); ap.add_argument('--output-dir',default='exports/confluence'); a=ap.parse_args()
    ctx=build_context(Path(a.project_root),mode=a.mode); root=ctx['root']; out=Path(a.output_dir); out=out if out.is_absolute() else root/out; out.mkdir(parents=True,exist_ok=True)
    for p in out.rglob('*.txt'): p.unlink()
    rev=ctx['manifest'].get('project',{}).get('revision','-'); catalog_manifest=[]
    for spec in ctx['specs']:
        typ=spec['type']; objs=ctx['by_type'].get(typ,[]); title=spec['catalog_title']; fn=spec['folder']+'.txt'; folder=spec['folder']
        lines=[f'h1. {title}','','{info:title=Genererad artefakt}',f"Genererad från kanonisk YAML · läge {a.mode} · projektrevision {rev} · presentationskontrakt {ctx['contract'].get('contract',{}).get('id','-')}",' {info}'.strip(),'','|| ID || Namn || Beskrivning || Status ||']
        if objs:
            for o in objs: lines.append(f"| {o['id']} | [{inline(o['name'])}|{inline(display(ctx,o))}] | {inline(o.get('description',''))} | {o.get('status','')} |")
        else: lines.append('| _Inga objekt i valt läge_ |  |  |  |')
        (out/fn).write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8'); catalog_manifest.append({'type':typ,'title':title,'file':fn,'folder':folder,'object_count':len(objs)})
        ddir=out/'objects'/folder; ddir.mkdir(parents=True,exist_ok=True)
        for o in objs:
            d=[f"h1. {display(ctx,o)}",'', '{info:title=Genererad artefakt}',f"Genererad från kanonisk YAML · läge {a.mode} · projektrevision {rev}",'{info}','',f"* *ID:* {o['id']}",f"* *Objekttyp:* {typ}",f"* *Status:* {o.get('status','')}"]
            if o.get('description'): d += ['','h2. Beskrivning','',str(o['description'])]
            fields=visible_fields(ctx,spec,o); boundary=[f for f in ('in_scope','out_of_scope') if f in fields]
            if boundary:
                d += ['','h2. Avgränsning']
                for f in boundary: d += ['',f"h3. {label(ctx,typ,f,o)}",'']+bullets(o[f])
                fields=[f for f in fields if f not in boundary]
            if 'functions' in fields: d += ['','h2. Funktioner','']+bullets(o['functions']); fields.remove('functions')
            if fields:
                d += ['','h2. Egenskaper','']+[f"* *{label(ctx,typ,f,o)}:* {fmt_value(o[f])}" for f in fields]
            for nav in navigation_for_object(ctx,o):
                d += ['',f"h2. {nav['title']}",'']
                if nav.get('epistemic_note'): d += [f"_ {nav['epistemic_note']} _",'']
                d += [f'* {x}' for x in nav['items']]
            groups={}
            for r in ctx['relations']:
                if r.get('source')==o['id']: other=r.get('target'); direction='forward'
                elif r.get('target')==o['id']: other=r.get('source'); direction='reverse'
                else: continue
                target=ctx['all_objects'].get(other); text=f"[{target['name']}|{display(ctx,target)}] ({{{{{other}}}}})" if target else str(other)
                groups.setdefault((rel_label(ctx,r.get('type',''),direction),r.get('type','')),[]).append(text)
            if groups:
                d += ['','h2. Relationer']
                for (lab,rt),items in sorted(groups.items()): d += ['',f"h3. {lab} ({{{{{rt}}}}})"]+[f'* {x}' for x in sorted(items,key=str.casefold)]
            ev=o.get('provenance') or []
            if ev:
                d += ['','h2. Proveniens']
                for e in ev:
                    sid=e.get('source_id'); src=ctx['sources'].get(sid,{}) if sid else {}; bits=[]
                    if sid: bits.append(f"källa: {src.get('title',sid)} ({{{{{sid}}}}})")
                    if e.get('reference'): bits.append(f"referens: {e['reference']}")
                    d.append(f"* *{e.get('evidence_type','okänd')}*"+(f" — {'; '.join(bits)}" if bits else ''))
            extras=[]
            for f in ('owner','aliases','tags'):
                if o.get(f): extras.append(f"* *{label(ctx,typ,f,o)}:* {fmt_value(o[f])}")
            if a.mode=='working' and o.get('notes'): extras.append(f"* *{label(ctx,typ,'notes',o)}:* {fmt_value(o['notes'])}")
            if extras: d += ['','h2. Övrig metadata','']+extras
            (ddir/f"{o['id']}-{slug(o['name'])}.txt").write_text('\n'.join(d).rstrip()+'\n',encoding='utf-8')
    (out/'generation-manifest.json').write_text(json.dumps({'source_of_truth':False,'mode':a.mode,'revision':rev,'catalogs':catalog_manifest},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Generated Confluence markup in {out} ({a.mode}), {len(catalog_manifest)} active object types')
if __name__=='__main__': main()
