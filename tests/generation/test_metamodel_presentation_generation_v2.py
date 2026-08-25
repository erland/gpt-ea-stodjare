#!/usr/bin/env python3
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]

def run(script, project, out):
    subprocess.run([sys.executable,str(ROOT/'scripts'/script),'--project-root',str(project),'--mode','working','--output-dir',str(out)],check=True,capture_output=True,text=True)

def main():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); p=td/'project'; shutil.copytree(ROOT/'examples/minimal-model',p)
        (p/'model-definition').mkdir()
        pm=yaml.safe_load((ROOT/'examples/project-metamodel/minimal.yaml').read_text(encoding='utf-8'))
        # Add a project-local object type and a reader label; disable platform types for this fixture.
        x=pm['project_metamodel']
        x['object_types']['enabled']=['capability','it_support']
        x['object_types']['disabled']=['driver','goal','principle','platform_service','platform','product','standard','solution_pattern','reference_architecture']
        x['object_types']['custom']=[{
            'type':'organization_unit','display_name':'Organisationsenhet','id_prefix':'ORG-','definition':'Projektlokal organisationsenhet.',
            'provenance_required':False,'attributes':[{'name':'responsibility','type':'string','required':False}],'model_file':'organization-units.yaml'
        }]
        x['relations']['enabled']=['supports']; x['relations']['disabled']=['influences','uses','provided_by','realized_by','can_realize','governed_by','constrains','depends_on','derived_from','related_to']
        x['presentation']['labels']={'organization_unit.responsibility':'Ansvarsområde'}
        (p/'model-definition/project-metamodel.yaml').write_text(yaml.safe_dump(pm,allow_unicode=True,sort_keys=False),encoding='utf-8')
        (p/'model/organization-units.yaml').write_text(yaml.safe_dump({'schema_version':'1.0','object_type':'organization_unit','objects':[{'id':'ORG-001','type':'organization_unit','name':'Arkitekturfunktion','description':'Ansvarar för arkitekturstyrning.','status':'approved','responsibility':'EA governance'}]},allow_unicode=True,sort_keys=False),encoding='utf-8')
        md=td/'md'; cf=td/'cf'; run('generate_markdown.py',p,md); run('generate_confluence.py',p,cf)
        mm=json.loads((md/'generation-manifest.json').read_text(encoding='utf-8'))
        assert [c['type'] for c in mm['catalogs']]==['capability','it_support','organization_unit']
        assert not (md/'plattformar.md').exists()
        detail=next((md/'objects/organization-unit').glob('*.md')).read_text(encoding='utf-8')
        assert '# Arkitekturfunktion (ORG-001)' in detail
        assert '**Ansvarsområde:** EA governance' in detail
        cm=json.loads((cf/'generation-manifest.json').read_text(encoding='utf-8'))
        assert [c['type'] for c in cm['catalogs']]==['capability','it_support','organization_unit']
    # Product is a native v2 object and must be generated when its model file is present even in legacy/simple fallback mode.
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); run('generate_markdown.py',ROOT/'examples/product-analysis-it-support',td/'md')
        text=(td/'md/produkter.md').read_text(encoding='utf-8'); assert 'Acme Writer Suite' in text
        detail=next((td/'md/objects/produkter').glob('PRD-251-*.md')).read_text(encoding='utf-8')
        assert '**Produkttyp:** application_product' in detail and '### Kan realisera (`can_realize`)' in detail
    print('OK: metamodel- and presentation-aware generation')
if __name__=='__main__': main()
