#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, zipfile

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
KNOWLEDGE=[
 '00-knowledge-index.md','01-domain-model.md','02-evidence-and-research.md',
 '03-analysis-and-modeling-workflows.md','04-quality-assurance.md','05-project-and-output.md']
RUNTIME_SCRIPTS=[
 'validate_project.py','detect_project_profile.py','resolve_project_metamodel.py',
 'resolve_quality_rules.py','change_control.py','generate_derived_views.py',
 'generate_markdown.py','generate_confluence.py','generator_context.py',
 'presentation_contract.py','export_documents.py','docx-pagebreak.lua',
 'migrate_v1_to_v2.py','migrate_rev80_to_v2.py','verify_v1_v2_migration.py']

def valid(v):
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?', v):
        raise SystemExit(f'Ogiltig version: {v}')
    return v

def starters():
    text=(ROOT/'custom-gpt/builder-config.md').read_text(encoding='utf-8')
    m=re.search(r'## Primära conversation starters\s+(.*?)\s+Starters är', text, re.S)
    if not m: raise SystemExit('Kunde inte läsa conversation starters ur builder-config.md')
    vals=re.findall(r'^\d+\. \*\*(.+?)\*\*\s*$', m.group(1), re.M)
    if len(vals)!=4: raise SystemExit(f'Väntade 4 conversation starters, fick {len(vals)}')
    return vals

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def cp(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)

def cptree(src,dst):
    if not src.exists(): return
    for p in src.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix not in {'.pyc','.pyo'}:
            cp(p,dst/p.relative_to(src))

def zipdir(src,out):
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file():
                i=zipfile.ZipInfo(str(p.relative_to(src)).replace(os.sep,'/'))
                i.date_time=(2020,1,1,0,0,0); i.compress_type=zipfile.ZIP_DEFLATED; i.external_attr=0o644<<16
                z.writestr(i,p.read_bytes())

def build_plugin(stage: Path, version: str) -> Path:
    plugin=stage/'plugin'
    skill=plugin/'skills/ea-stodjare'
    refs=skill/'references'
    assets=skill/'assets'
    scripts=skill/'scripts'
    for p in (refs,assets,scripts): p.mkdir(parents=True,exist_ok=True)

    canonical=(ROOT/'custom-gpt/instructions.md').read_text(encoding='utf-8').strip()
    skill_text=(
      '---\n'
      'name: ea-stodjare\n'
      'description: Stateful enterprise-architecture-stöd för metamodel-first modellering, evidens, change-control, migration, kvalitetssäkring och dokumentgenerering.\n'
      '---\n\n'
      '# EA Stödjare\n\n'
      '## Plugin-runtime\n\n'
      '- Identifiera alltid projektprofil och effektiv metamodell innan EA-objekt eller relationer tolkas eller ändras.\n'
      '- När ett faktiskt EA-projekt är öppet är projektfilerna auktoritativ state. Chattminne får inte ersätta project-manifest.json, project-metamodel.yaml, model/, governance/, market-reference/ eller actual-state/.\n'
      '- Full verifierad projektändring kräver filesystem read/write, code execution och persistent workspace-state. Utan dessa får analys och förslag göras, men ingen ändring får beskrivas som genomförd eller verifierad.\n'
      '- Webbresearch är obligatorisk för den del av en uppgift som kräver aktuell standard, ramverk, praxis, marknads- eller produktinformation.\n'
      '- Migration är explicit och får aldrig ske implicit vid projektöppning. Bevara original, stabila ID:n, proveniens och tvetydig legacysemantik.\n'
      '- Kör relevanta runtimeverktyg i scripts/ när projektprofil, metamodell, QA, change-control, migration eller generering ska verifieras.\n'
      '- DOCX kräver Pandoc. PDF kräver Pandoc och LibreOffice. Påstå inte export om hosten saknar verktygen eller körningen inte faktiskt lyckades.\n'
      '- Pluginen genererar ingen MCP-wrapper.\n\n'
      '## Canonical behavior\n\n'+canonical+'\n\n'
      '## References\n\n'
      + '\n'.join(f'- references/knowledge/{k}' for k in KNOWLEDGE)
      + '\n- references/baseline/model/\n- references/baseline/governance/\n\n'
      '## Runtime resources\n\n'
      '- schemas/, extensions/, presentation/, derived-views/ och compatibility/ stödjer de deklarerade runtimeverktygen.\n'
      '- assets/templates/ innehåller genereringsmallar.\n'
      '- scripts/ innehåller endast runtimeverktyg, inte CI-/releaseinfrastruktur.\n'
    )
    (skill/'SKILL.md').write_text(skill_text,encoding='utf-8')

    for k in KNOWLEDGE: cp(ROOT/'custom-gpt/knowledge'/k,refs/'knowledge'/k)
    cptree(ROOT/'model',refs/'baseline/model')
    cptree(ROOT/'governance',refs/'baseline/governance')
    cptree(ROOT/'templates',assets/'templates')
    for name in RUNTIME_SCRIPTS: cp(ROOT/'scripts'/name,scripts/name)

    for d in ('schemas','extensions','presentation','derived-views'):
        cptree(ROOT/d,skill/d)
    cptree(ROOT/'compatibility/ea-stodjare-v1',skill/'compatibility/ea-stodjare-v1')
    cptree(ROOT/'compatibility/migration-rules',skill/'compatibility/migration-rules')
    cptree(ROOT/'compatibility/migrations',skill/'compatibility/migrations')
    cptree(ROOT/'compatibility/reference-projects/rev80',skill/'compatibility/reference-projects/rev80')

    plugin_json={
      '$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
      'name':'ea-stodjare','version':version,
      'description':'Stateful enterprise-architecture-stöd med metamodel-first modellering, verifiering, migration och generering.'
    }
    (plugin/'plugin.json').write_text(json.dumps(plugin_json,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    script_resources=[]
    required={'validate_project.py','detect_project_profile.py','resolve_project_metamodel.py','resolve_quality_rules.py','change_control.py'}
    for name in RUNTIME_SCRIPTS:
        script_resources.append({
          'path':f'skills/ea-stodjare/scripts/{name}',
          'requirement':'required' if name in required else 'recommended',
          'materialize_to':f'scripts/{name}',
        })
    contract={
      'schema_version':1,'runtime_id':'openai_plugin','version':version,
      'adapter':{
        'mode':'skills_first','compatibility':'ready_runtime_dependent',
        'filesystem_read':'required_host_runtime','filesystem_write':'required_host_runtime',
        'code_execution':'required_host_runtime','persistent_state':'required_host_runtime',
        'web_research':'conditional_host_runtime',
        'state_authority':'project_files','conversation_fallback':False,
        'profile_gate':['native_v2','legacy_v1','extended_legacy','unknown'],
        'mcp_generated':False,'script_resources':script_resources,
        'external_dependencies':{
          'docx':['pandoc'],
          'pdf':['pandoc','libreoffice'],
        },
        'fallback_policy':{
          'without_workspace_or_write':'allow_analysis_and_proposals_only_do_not_claim_project_change',
          'without_code_execution':'do_not_claim_profile_validation_qa_migration_or_regeneration_verified',
          'without_web':'do_not_claim_current_external_standard_market_product_or_practice_verified',
          'without_persistent_state':'do_not_claim_stateful_project_management',
        },
      }
    }
    (plugin/'runtime-contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (plugin/'README.md').write_text(
      '# EA Stödjare – OpenAI Plugin\n\n'
      'Skills-first peer-runtime enligt GPT Byggaren 1.5.1. Full verifierad projektändring kräver hoststöd för fil read/write, code execution och persistent state. '
      'Aktuell extern research är ett villkorligt krav. Runtimeverktyg paketeras som script resources; CI/releaseverktyg och MCP-wrapper ingår inte.\n',
      encoding='utf-8')
    (plugin/'VERSION').write_text(version+'\n',encoding='utf-8')

    files=[]
    for p in sorted(x for x in plugin.rglob('*') if x.is_file() and x.name!='MANIFEST.json'):
        files.append({'path':p.relative_to(plugin).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    (plugin/'MANIFEST.json').write_text(json.dumps({
      'schema_version':1,'runtime_id':'openai_plugin','version':version,
      'entrypoint':'plugin.json','files':files
    },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return plugin

def main(version):
    version=valid(version)
    for k in KNOWLEDGE:
        if not (ROOT/'custom-gpt/knowledge'/k).is_file(): raise SystemExit(f'Saknad Builder Knowledge: {k}')
    shutil.rmtree(DIST,ignore_errors=True); DIST.mkdir()
    stage=ROOT/'.build-distributions'; shutil.rmtree(stage,ignore_errors=True)
    custom=stage/'custom'; chat=stage/'chat'; custom.mkdir(parents=True); chat.mkdir(parents=True)

    for rel in ['README.md','custom-gpt/builder-config.md','custom-gpt/instructions.md']:
        cp(ROOT/rel,custom/rel)
    for k in KNOWLEDGE: cp(ROOT/'custom-gpt/knowledge'/k,custom/'custom-gpt/knowledge'/k)
    (custom/'VERSION').write_text(version+'\n',encoding='utf-8')

    cp(ROOT/'portable/START-HERE.md',chat/'START-HERE.md')
    cp(ROOT/'custom-gpt/instructions.md',chat/'assistant/instructions.md')
    st=starters()
    (chat/'assistant').mkdir(parents=True,exist_ok=True)
    (chat/'assistant/conversation-starters.md').write_text('# Conversation starters\n\n'+''.join(f'- {s}\n' for s in st),encoding='utf-8')
    cp(ROOT/'custom-gpt/builder-config.md',chat/'assistant/builder-config.md')
    for k in KNOWLEDGE: cp(ROOT/'custom-gpt/knowledge'/k,chat/'knowledge'/k)
    for d in ['schemas','model','templates']:
        cptree(ROOT/d,chat/'supporting'/d)
    (chat/'VERSION').write_text(version+'\n',encoding='utf-8')
    files={}
    for p in sorted(chat.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json': files[str(p.relative_to(chat)).replace(os.sep,'/')]=sha(p)
    (chat/'MANIFEST.json').write_text(json.dumps({'package':'ea-stodjare','format':'portable-chat-assistant','version':version,'entrypoint':'START-HERE.md','instructions':'assistant/instructions.md','knowledge_count':6,'files':files},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    plugin=build_plugin(stage,version)

    custom_zip=DIST/f'ea-stodjare-custom-gpt-v{version}.zip'
    chat_zip=DIST/f'ea-stodjare-chat-v{version}.zip'
    plugin_zip=DIST/f'ea-stodjare-openai-plugin-v{version}.zip'
    zipdir(custom,custom_zip); zipdir(chat,chat_zip); zipdir(plugin,plugin_zip)

    artifacts=[
      ('custom_gpt_zip',custom_zip,'chatgpt_custom'),
      ('chat_zip',chat_zip,'chatgpt_chat'),
      ('plugin_zip',plugin_zip,'openai_plugin'),
    ]
    (DIST/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for _,p,_ in artifacts),encoding='utf-8')
    (DIST/'DELIVERY-MANIFEST.json').write_text(json.dumps({
      'schema_version':1,'project':'ea-stodjare','version':version,
      'artifacts':[{'type':t,'runtime_id':rid,'file':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for t,p,rid in artifacts],
      'runtime_status':{
        'chatgpt_chat':'ready_active','chatgpt_custom':'ready_active',
        'openai_plugin':'ready_runtime_dependent','claude_project':'reduced_inactive','opencode':'reduced_inactive'
      }
    },ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    shutil.rmtree(stage,ignore_errors=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--version'); a=ap.parse_args(); main(a.version or (ROOT/'VERSION').read_text().strip())
