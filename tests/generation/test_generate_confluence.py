#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / 'examples' / 'minimal-model'
MD_SCRIPT = ROOT / 'scripts' / 'generate_markdown.py'
CONF_SCRIPT = ROOT / 'scripts' / 'generate_confluence.py'


def tree_hash(root: Path, suffix: str) -> str:
    h = hashlib.sha256()
    for path in sorted(root.rglob(f'*{suffix}')):
        h.update(path.relative_to(root).as_posix().encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def object_ids(root: Path, suffix: str) -> set[str]:
    result = set()
    for path in root.glob(f'objects/**/*{suffix}'):
        result.add(path.name.split('-', 1)[0])
    return result


def run(script: Path, mode: str, output: Path):
    subprocess.run([
        sys.executable, str(script), '--project-root', str(EXAMPLE), '--mode', mode,
        '--output-dir', str(output)
    ], check=True, capture_output=True, text=True)


def main():
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        conf_work = td / 'conf-working'
        md_work = td / 'md-working'
        conf_pub = td / 'conf-published'
        md_pub = td / 'md-published'

        run(CONF_SCRIPT, 'working', conf_work)
        first = tree_hash(conf_work, '.txt')
        run(CONF_SCRIPT, 'working', conf_work)
        second = tree_hash(conf_work, '.txt')
        assert first == second, 'Confluence export is not byte-stable across identical runs'

        run(MD_SCRIPT, 'working', md_work)
        assert object_ids(conf_work, '.txt') == object_ids(md_work, '.md'), 'Working Markdown/Confluence object sets differ'

        run(CONF_SCRIPT, 'published', conf_pub)
        run(MD_SCRIPT, 'published', md_pub)
        assert object_ids(conf_pub, '.txt') == object_ids(md_pub, '.md'), 'Published Markdown/Confluence object sets differ'

        # Candidate objects in the fixture must not appear in published output.
        assert 'CAP-002' not in object_ids(conf_pub, '.txt')
        assert 'PLS-001' not in object_ids(conf_pub, '.txt')

        catalogs = sorted(p.name for p in conf_work.glob('*.txt'))
        assert len(catalogs) == 10, f'Expected 10 Confluence catalogs, found {len(catalogs)}'

    print('OK: Confluence generation is deterministic and semantically aligned with Markdown.')


if __name__ == '__main__':
    main()
