#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, zipfile
ROOT=Path(__file__).resolve().parents[1]; DIST=ROOT/'dist'
K=['00-knowledge-index.md','01-domain-model.md','02-evidence-and-research.md','03-analysis-and-modeling-workflows.md','04-quality-assurance.md','05-project-and-output.md']
def rd(z,n):
    try:return z.read(n)
    except KeyError:raise SystemExit(f'Saknad fil: {n}')
def hb(b):return hashlib.sha256(b).hexdigest()
def main(v):
    c=DIST/f'ea-stodjare-custom-gpt-v{v}.zip'; p=DIST/f'ea-stodjare-chat-v{v}.zip'
    for f in [c,p]:
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
        m=json.loads(rd(z,'MANIFEST.json')); 
        if m['version']!=v or m['knowledge_count']!=6:raise SystemExit('Fel manifest')
        for n,h in m['files'].items():
            if hb(rd(z,n))!=h:raise SystemExit('Hashfel: '+n)
    print(f'OK: EA Stödjare distributioner v{v} validerade.')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--version');x=a.parse_args();main(x.version or (ROOT/'VERSION').read_text().strip())
