#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, zipfile

ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'
K=['00-knowledge-index.md','01-domain-model.md','02-evidence-and-research.md','03-analysis-and-modeling-workflows.md','04-quality-assurance.md','05-project-and-output.md']
RUNTIME_SCRIPTS={
 'validate_project.py','detect_project_profile.py','resolve_project_metamodel.py',
 'resolve_quality_rules.py','change_control.py','generate_derived_views.py',
 'generate_markdown.py','generate_confluence.py','generator_context.py',
 'presentation_contract.py','export_documents.py','docx-pagebreak.lua',
 'migrate_v1_to_v2.py','migrate_rev80_to_v2.py','verify_v1_v2_migration.py'}

def rd(z,n):
    try:return z.read(n)
    except KeyError:raise SystemExit(f'Saknad fil: {n}')
def hb(b):return hashlib.sha256(b).hexdigest()

def validate_plugin(path:Path,v:str):
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad: raise SystemExit(f'Korrupt zip {path.name}: {bad}')
        names=set(z.namelist())
        required={'plugin.json','README.md','VERSION','MANIFEST.json','runtime-contract.json','skills/ea-stodjare/SKILL.md'}
        missing=required-names
        if missing: raise SystemExit('Plugin saknar rot-/skillfiler: '+', '.join(sorted(missing)))
        if any(n.startswith('ea-stodjare/') for n in names): raise SystemExit('Plugin ZIP får inte ha wrapper-katalog')
        if rd(z,'VERSION').decode().strip()!=v: raise SystemExit('Fel VERSION i plugin')
        plugin=json.loads(rd(z,'plugin.json'))
        if plugin.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json': raise SystemExit('Plugin schema mismatch')
        if plugin.get('name')!='ea-stodjare' or plugin.get('version')!=v: raise SystemExit('Plugin metadata mismatch')
        skill=rd(z,'skills/ea-stodjare/SKILL.md').decode()
        canonical=(ROOT/'custom-gpt/instructions.md').read_text(encoding='utf-8').strip()
        if canonical not in skill: raise SystemExit('Plugin SKILL saknar canonical instruktion')
        for marker in ('projektprofil och effektiv metamodell','projektfilerna auktoritativ state','Migration är explicit','ingen MCP-wrapper'):
            if marker.lower() not in skill.lower(): raise SystemExit(f'Plugin SKILL saknar runtime-regel: {marker}')
        for k in K:
            target='skills/ea-stodjare/references/knowledge/'+k
            if rd(z,target)!=(ROOT/'custom-gpt/knowledge'/k).read_bytes(): raise SystemExit('Plugin Knowledge avviker: '+k)

        contract=json.loads(rd(z,'runtime-contract.json'))
        if contract.get('runtime_id')!='openai_plugin': raise SystemExit('Plugin runtime_id mismatch')
        a=contract.get('adapter',{})
        if a.get('mode')!='skills_first' or a.get('compatibility')!='ready_runtime_dependent': raise SystemExit('Plugin adapter mismatch')
        for key in ('filesystem_read','filesystem_write','code_execution','persistent_state'):
            if a.get(key)!='required_host_runtime': raise SystemExit(f'Plugin host dependency mismatch: {key}')
        if a.get('web_research')!='conditional_host_runtime': raise SystemExit('Plugin web research dependency mismatch')
        if a.get('state_authority')!='project_files' or a.get('conversation_fallback') is not False: raise SystemExit('Plugin state contract mismatch')
        if a.get('mcp_generated') is not False: raise SystemExit('Plugin får inte generera MCP')
        declared={Path(x.get('path','')).name for x in a.get('script_resources',[])}
        if declared!=RUNTIME_SCRIPTS: raise SystemExit('Plugin runtime script set mismatch')
        packaged={Path(n).name for n in names if n.startswith('skills/ea-stodjare/scripts/') and not n.endswith('/')}
        if packaged!=RUNTIME_SCRIPTS: raise SystemExit('Plugin paketerade scripts mismatch')
        for name in RUNTIME_SCRIPTS:
            if rd(z,'skills/ea-stodjare/scripts/'+name)!=(ROOT/'scripts'/name).read_bytes(): raise SystemExit('Plugin script drift: '+name)
        forbidden={'build_distributions.py','validate_distributions.py','build_builder_knowledge.py','package_release.py','run_v2_ci_gate.py','run_full_e2e_regression.py'}
        if packaged & forbidden: raise SystemExit('Plugin innehåller build-/release-scripts')

        for rel in (
          'skills/ea-stodjare/schemas/project-metamodel.schema.json',
          'skills/ea-stodjare/extensions/registry.yaml',
          'skills/ea-stodjare/presentation/presentation-contract.yaml',
          'skills/ea-stodjare/derived-views/views.yaml',
          'skills/ea-stodjare/compatibility/ea-stodjare-v1/schemas/model-format.yaml',
          'skills/ea-stodjare/compatibility/reference-projects/rev80/metamodel.yaml',
        ):
            if rel not in names: raise SystemExit('Plugin saknar runtime support resource: '+rel)
        manifest=json.loads(rd(z,'MANIFEST.json'))
        if manifest.get('runtime_id')!='openai_plugin' or manifest.get('version')!=v: raise SystemExit('Plugin MANIFEST metadata mismatch')
        for item in manifest.get('files',[]):
            n=item['path']
            if n not in names or hb(rd(z,n))!=item['sha256']: raise SystemExit('Plugin MANIFEST hash mismatch: '+n)

def main(v):
    c=DIST/f'ea-stodjare-custom-gpt-v{v}.zip'
    p=DIST/f'ea-stodjare-chat-v{v}.zip'
    plugin=DIST/f'ea-stodjare-openai-plugin-v{v}.zip'
    for f in [c,p,plugin]:
        if not f.is_file():raise SystemExit(f'Saknad distribution: {f.name}')
        with zipfile.ZipFile(f) as z:
            bad=z.testzip()
            if bad:raise SystemExit(f'Korrupt zip {f.name}: {bad}')
    with zipfile.ZipFile(c) as z:
        if rd(z,'custom-gpt/instructions.md')!=(ROOT/'custom-gpt/instructions.md').read_bytes():raise SystemExit('Custom instructions avviker')
        if rd(z,'custom-gpt/builder-config.md')!=(ROOT/'custom-gpt/builder-config.md').read_bytes():raise SystemExit('Builder config avviker')
        for k in K:
            if rd(z,'custom-gpt/knowledge/'+k)!=(ROOT/'custom-gpt/knowledge'/k).read_bytes():raise SystemExit('Custom Knowledge avviker: '+k)
        if rd(z,'VERSION').decode().strip()!=v:raise SystemExit('Fel VERSION i custom')
    with zipfile.ZipFile(p) as z:
        if rd(z,'assistant/instructions.md')!=(ROOT/'custom-gpt/instructions.md').read_bytes():raise SystemExit('Portable instructions avviker')
        for k in K:
            if rd(z,'knowledge/'+k)!=(ROOT/'custom-gpt/knowledge'/k).read_bytes():raise SystemExit('Portable Knowledge avviker: '+k)
        if rd(z,'VERSION').decode().strip()!=v:raise SystemExit('Fel VERSION i portable')
        m=json.loads(rd(z,'MANIFEST.json'))
        if m['version']!=v or m['knowledge_count']!=6:raise SystemExit('Fel manifest')
        for n,h in m['files'].items():
            if hb(rd(z,n))!=h:raise SystemExit('Hashfel: '+n)

    validate_plugin(plugin,v)

    sums={}
    for line in (DIST/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        if line.strip():
            digest,name=line.split(None,1); sums[name.strip()]=digest
    for f in (c,p,plugin):
        if sums.get(f.name)!=hb(f.read_bytes()): raise SystemExit('SHA256SUMS mismatch: '+f.name)
    delivery=json.loads((DIST/'DELIVERY-MANIFEST.json').read_text(encoding='utf-8'))
    types={x.get('type') for x in delivery.get('artifacts',[])}
    if types!={'custom_gpt_zip','chat_zip','plugin_zip'}: raise SystemExit('Delivery manifest artifact set mismatch')
    if delivery.get('runtime_status',{}).get('openai_plugin')!='ready_runtime_dependent': raise SystemExit('Delivery manifest plugin status mismatch')
    print(f'OK: EA Stödjare distributioner v{v} validerade inklusive OpenAI Plugin.')

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--version');x=a.parse_args();main(x.version or (ROOT/'VERSION').read_text().strip())
