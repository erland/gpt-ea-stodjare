#!/usr/bin/env python3
from __future__ import annotations
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / 'examples' / 'minimal-model'
SCRIPT = ROOT / 'scripts' / 'export_documents.py'


def run(mode: str, out: Path):
    subprocess.run([
        'python3', str(SCRIPT), '--project-root', str(EXAMPLE), '--mode', mode,
        '--output-dir', str(out), '--basename', f'ea-{mode}'
    ], check=True)
    return out / f'ea-{mode}.docx', out / f'ea-{mode}.pdf'


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read('word/document.xml').decode('utf-8')
    import re
    return ' '.join(re.sub(r'<[^>]+>', ' ', xml).split())


def pdf_text(path: Path) -> str:
    proc = subprocess.run(['pdftotext', str(path), '-'], check=True, text=True, stdout=subprocess.PIPE)
    return proc.stdout


def main():
    with tempfile.TemporaryDirectory(prefix='ea-export-test-') as td:
        out = Path(td)
        pub_docx, pub_pdf = run('published', out / 'published')
        work_docx, work_pdf = run('working', out / 'working')
        for p in (pub_docx, pub_pdf, work_docx, work_pdf):
            assert p.exists() and p.stat().st_size > 1000, p

        pub = docx_text(pub_docx)
        work = docx_text(work_docx)
        assert 'Minimal EA-modell' in pub
        assert 'Förmågor' in pub
        assert 'Hantera ärenden digitalt' in pub
        assert 'Driftsätta och köra applikationer' not in pub  # candidate
        assert 'Driftsätta och köra applikationer' in work

        pdf = pdf_text(pub_pdf)
        assert 'Minimal EA-modell' in pdf
        assert 'Förmågor' in pdf

    print('OK: DOCX/PDF-export verifierad i working och published.')


if __name__ == '__main__':
    main()
