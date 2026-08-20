import hashlib, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
EX=ROOT/'examples/minimal-model'
OUT=EX/'docs/generated'
def tree_hash():
    h=hashlib.sha256()
    for p in sorted(OUT.rglob('*.md')):
        h.update(p.relative_to(OUT).as_posix().encode()); h.update(p.read_bytes())
    return h.hexdigest()
def run(mode='working'):
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_markdown.py'),'--project-root',str(EX),'--mode',mode],check=True)
run(); a=tree_hash(); run(); b=tree_hash(); assert a==b
assert (OUT/'formagor.md').exists()
assert 'Hantera ärenden digitalt' in (OUT/'formagor.md').read_text(encoding='utf-8')
run('published')
assert 'Driftsätta och köra applikationer' not in (OUT/'formagor.md').read_text(encoding='utf-8')
run('working')
print('OK deterministic markdown generation')
