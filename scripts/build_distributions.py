#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, os, re, shutil, zipfile
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
KNOWLEDGE=[
 '00-knowledge-index.md','01-domain-model.md','02-evidence-and-research.md',
 '03-analysis-and-modeling-workflows.md','04-quality-assurance.md','05-project-and-output.md']

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
        if p.is_file(): cp(p,dst/p.relative_to(src))

def zipdir(src,out):
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file():
                i=zipfile.ZipInfo(str(p.relative_to(src)).replace(os.sep,'/')); i.date_time=(2020,1,1,0,0,0); i.compress_type=zipfile.ZIP_DEFLATED; i.external_attr=0o644<<16
                z.writestr(i,p.read_bytes())

def main(version):
    version=valid(version)
    for k in KNOWLEDGE:
        if not (ROOT/'custom-gpt/knowledge'/k).is_file(): raise SystemExit(f'Saknad Builder Knowledge: {k}')
    shutil.rmtree(DIST,ignore_errors=True); DIST.mkdir()
    stage=ROOT/'.build-distributions'; shutil.rmtree(stage,ignore_errors=True)
    custom=stage/'custom'; chat=stage/'chat'; custom.mkdir(parents=True); chat.mkdir(parents=True)

    # Custom GPT install bundle
    for rel in ['README.md','custom-gpt/builder-config.md','custom-gpt/instructions.md']:
        cp(ROOT/rel,custom/rel)
    for k in KNOWLEDGE: cp(ROOT/'custom-gpt/knowledge'/k,custom/'custom-gpt/knowledge'/k)
    (custom/'VERSION').write_text(version+'\n',encoding='utf-8')

    # Portable Chat bundle
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
    zipdir(custom,DIST/f'ea-stodjare-custom-gpt-v{version}.zip')
    zipdir(chat,DIST/f'ea-stodjare-chat-v{version}.zip')
    shutil.rmtree(stage,ignore_errors=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--version'); a=ap.parse_args(); main(a.version or (ROOT/'VERSION').read_text().strip())
