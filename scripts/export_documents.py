#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

CATALOGS = [
    ('drivkrafter.md', 'Drivkrafter'),
    ('mal.md', 'Mål'),
    ('principer.md', 'Principer'),
    ('formagor.md', 'Förmågor'),
    ('it-stod.md', 'IT-stöd'),
    ('plattformstjanster.md', 'Plattformstjänster'),
    ('plattformar.md', 'Plattformar'),
    ('standarder.md', 'Standarder'),
    ('losningsmonster.md', 'Lösningsmönster'),
    ('referensarkitekturer.md', 'Referensarkitekturer'),
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stdout}\n{proc.stderr}")


def strip_first_h1(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
        if lines and not lines[0].strip():
            lines = lines[1:]
    return '\n'.join(lines).strip()


def strip_md_links(text: str) -> str:
    # Links in the standalone Markdown views are navigation aids. In the assembled
    # distribution document the referenced detail sections are in the same file.
    return re.sub(r'\[([^\]]+)\]\((?:[^)]+\.md)(?:#[^)]+)?\)', r'\1', text)


def promote_detail_headings(text: str) -> str:
    # Detail page H1 becomes H2 within its catalog section, subheadings shift accordingly.
    out = []
    for line in text.splitlines():
        if line.startswith('### '):
            out.append('#' + line)
        elif line.startswith('## '):
            out.append('#' + line)
        elif line.startswith('# '):
            out.append('#' + line)
        else:
            out.append(line)
    return '\n'.join(out)


def assemble(project_root: Path, md_root: Path, mode: str) -> str:
    manifest = json.loads((project_root / 'project-manifest.json').read_text(encoding='utf-8'))
    project = manifest['project']
    title = project['name']
    revision = project['revision']
    lang = project.get('language', 'sv-SE')

    parts = [
        '---',
        f'title: "{title}"',
        'subtitle: "Enterprise Architecture-dokumentation"',
        f'lang: "{lang}"',
        '---',
        '',
        f'> Genererad från kanonisk YAML · läge `{mode}` · projektrevision `{revision}`',
        '',
        'Detta dokument är ett distributionsformat genererat från projektets kanoniska YAML-modell. '
        'Ändringar ska göras i modellen och därefter regenereras, inte direkt i DOCX- eller PDF-filen.',
        '',
    ]

    for catalog_file, catalog_title in CATALOGS:
        path = md_root / catalog_file
        if not path.exists():
            continue
        src = path.read_text(encoding='utf-8')
        # Published distribution documents omit empty catalogs. Working mode keeps
        # them visible because absence can itself be useful during modelling.
        if mode == 'published' and not re.search(r'\(objects/[^)]+\.md\)', src):
            continue
        text = strip_first_h1(src)
        text = strip_md_links(text)
        parts.extend([f'# {catalog_title}', '', text, ''])

        # Find corresponding detail folder from links in source catalog.
        folders = sorted(set(re.findall(r'\(objects/([^/]+)/[^)]+\.md\)', src)))
        for folder in folders:
            detail_dir = md_root / 'objects' / folder
            if not detail_dir.exists():
                continue
            for detail_path in sorted(detail_dir.glob('*.md')):
                detail = detail_path.read_text(encoding='utf-8')
                detail = strip_md_links(detail)
                detail = promote_detail_headings(detail)
                parts.extend([detail.strip(), ''])

    return '\n'.join(parts).rstrip() + '\n'


def main() -> int:
    ap = argparse.ArgumentParser(description='Generate DOCX and PDF from canonical EA YAML via generated Markdown.')
    ap.add_argument('--project-root', default='.', help='EA Stödjare project root')
    ap.add_argument('--mode', choices=['working', 'published'], default='published')
    ap.add_argument('--output-dir', default='exports/document', help='Output directory relative to project root unless absolute')
    ap.add_argument('--basename', default='ea-dokumentation', help='Output file basename')
    ap.add_argument('--keep-assembled-markdown', action='store_true', help='Keep assembled Markdown next to exports for debugging')
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    tool_root = Path(__file__).resolve().parents[1]
    out = Path(args.output_dir)
    if not out.is_absolute():
        out = root / out
    out.mkdir(parents=True, exist_ok=True)

    pandoc = shutil.which('pandoc')
    libreoffice = shutil.which('libreoffice') or shutil.which('soffice')
    if not pandoc:
        raise SystemExit('Pandoc saknas. Installera Pandoc för DOCX-export.')
    if not libreoffice:
        raise SystemExit('LibreOffice/soffice saknas. Det krävs för PDF-export från DOCX.')

    with tempfile.TemporaryDirectory(prefix='ea-stodjare-export-') as td:
        tmp = Path(td)
        md_dir = tmp / 'markdown'
        run([
            'python3', str(tool_root / 'scripts' / 'generate_markdown.py'),
            '--project-root', str(root), '--mode', args.mode,
            '--output-dir', str(md_dir),
        ])

        assembled = assemble(root, md_dir, args.mode)
        assembled_path = tmp / 'assembled.md'
        assembled_path.write_text(assembled, encoding='utf-8')

        docx_path = out / f'{args.basename}.docx'
        pdf_path = out / f'{args.basename}.pdf'

        run([
            pandoc, str(assembled_path),
            '--from', 'markdown+pipe_tables',
            '--to', 'docx',
            '--standalone',
            '--toc', '--toc-depth=2',
            '--metadata', 'toc-title=Innehåll',
            '--lua-filter', str(tool_root / 'scripts' / 'docx-pagebreak.lua'),
            '--output', str(docx_path),
        ])

        # Use a dedicated writable LibreOffice profile to avoid cross-run state.
        profile = tmp / 'lo-profile'
        profile.mkdir()
        run([
            libreoffice, '--headless',
            f'-env:UserInstallation=file://{profile}',
            '--convert-to', 'pdf', '--outdir', str(out), str(docx_path),
        ])
        generated_pdf = out / f'{args.basename}.pdf'
        if not generated_pdf.exists() or generated_pdf.stat().st_size == 0:
            raise RuntimeError('LibreOffice skapade ingen giltig PDF.')

        if args.keep_assembled_markdown:
            (out / f'{args.basename}.md').write_text(assembled, encoding='utf-8')

    print(f'DOCX: {docx_path}')
    print(f'PDF:  {pdf_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
