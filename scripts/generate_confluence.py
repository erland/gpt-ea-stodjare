#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import yaml

TYPE_CFG = {
    'driver': ('drivers.yaml', 'drivkrafter.txt', 'drivers', 'Drivkrafter'),
    'goal': ('goals.yaml', 'mal.txt', 'goals', 'Mål'),
    'principle': ('principles.yaml', 'principer.txt', 'principles', 'Principer'),
    'capability': ('capabilities.yaml', 'formagor.txt', 'capabilities', 'Förmågor'),
    'it_support': ('it-support.yaml', 'it-stod.txt', 'it-support', 'IT-stöd'),
    'platform_service': ('platform-services.yaml', 'plattformstjanster.txt', 'platform-services', 'Plattformstjänster'),
    'platform': ('platforms.yaml', 'plattformar.txt', 'platforms', 'Plattformar'),
    'standard': ('standards.yaml', 'standarder.txt', 'standards', 'Standarder'),
    'solution_pattern': ('solution-patterns.yaml', 'losningsmonster.txt', 'solution-patterns', 'Lösningsmönster'),
    'reference_architecture': ('reference-architectures.yaml', 'referensarkitekturer.txt', 'reference-architectures', 'Referensarkitekturer'),
}

STATUS = {
    'working': {'candidate', 'approved', 'deprecated'},
    'published': {'approved'},
}

REL_LABELS = {
    'influences': ('Påverkar', 'Påverkas av'),
    'supports': ('Stödjer', 'Stöds av'),
    'uses': ('Använder', 'Används av'),
    'realized_by': ('Realiseras av', 'Realiserar'),
    'governed_by': ('Styrs av', 'Styr'),
    'constrains': ('Begränsar', 'Begränsas av'),
    'depends_on': ('Beror på', 'Är beroende för'),
    'derived_from': ('Härleds från', 'Ligger till grund för'),
    'related_to': ('Relaterar till', 'Relaterar till'),
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding='utf-8')) or {}


def slug(value: str) -> str:
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'(^-|-$)', '', re.sub(r'[^a-z0-9]+', '-', value)) or 'objekt'


def inline(value) -> str:
    if value is None:
        return ''
    # Confluence wiki tables use | as cell delimiters. Escaping with a backslash
    # keeps user content from changing the table structure.
    return str(value).replace('\\', '\\\\').replace('|', '\\|').replace('\r', ' ').replace('\n', ' ')


def fmt_list(value) -> str:
    if not value:
        return ''
    if not isinstance(value, list):
        return str(value)
    items = []
    for item in value:
        if isinstance(item, dict):
            items.append(str(item.get('name') or item.get('id') or ''))
        else:
            items.append(str(item))
    return ', '.join(x for x in items if x)


def bullet_lines(value) -> list[str]:
    if not value:
        return []
    if not isinstance(value, list):
        value = [value]
    result = []
    for item in value:
        if isinstance(item, dict):
            item = item.get('name') or item.get('id') or json.dumps(item, ensure_ascii=False)
        result.append(f'* {item}')
    return result


def page_title(obj: dict) -> str:
    return f"{obj['id']} – {obj['name']}"


def catalog_columns(typ: str):
    return {
        'driver': ['ID', 'Namn', 'Beskrivning', 'Kategori', 'Status'],
        'goal': ['ID', 'Namn', 'Beskrivning', 'Tidshorisont', 'Status'],
        'principle': ['ID', 'Namn', 'Principformulering', 'Status'],
        'capability': ['ID', 'Namn', 'Förmågetyp', 'Beskrivning', 'Status'],
        'it_support': ['ID', 'Namn', 'Beskrivning', 'Funktioner', 'Status'],
        'platform_service': ['ID', 'Namn', 'Beskrivning', 'Konsumentomfång', 'Funktioner', 'Status'],
        'platform': ['ID', 'Namn', 'Beskrivning', 'Teknik/produkter', 'Funktioner', 'Status'],
        'standard': ['ID', 'Namn', 'Standardtyp', 'Referens/version', 'Obligatorisk', 'Status'],
        'solution_pattern': ['ID', 'Namn', 'Problem/kontext', 'Status'],
        'reference_architecture': ['ID', 'Namn', 'Scope/tillämplighet', 'Status'],
    }[typ]


def catalog_values(typ: str, obj: dict):
    linked_name = f"[{inline(obj['name'])}|{inline(page_title(obj))}]"
    desc = inline(obj.get('description', ''))
    return {
        'driver': [obj['id'], linked_name, desc, inline(obj.get('category', '')), obj.get('status', '')],
        'goal': [obj['id'], linked_name, desc, inline(obj.get('time_horizon', '')), obj.get('status', '')],
        'principle': [obj['id'], linked_name, inline(obj.get('statement', '')), obj.get('status', '')],
        'capability': [obj['id'], linked_name, inline(obj.get('capability_type', '')), desc, obj.get('status', '')],
        'it_support': [obj['id'], linked_name, desc, inline(fmt_list(obj.get('functions'))), obj.get('status', '')],
        'platform_service': [obj['id'], linked_name, desc, inline(obj.get('consumer_scope', '')), inline(fmt_list(obj.get('functions'))), obj.get('status', '')],
        'platform': [obj['id'], linked_name, desc, inline(' / '.join(filter(None, [str(obj.get('technology', '')), fmt_list(obj.get('products'))]))), inline(fmt_list(obj.get('functions'))), obj.get('status', '')],
        'standard': [obj['id'], linked_name, inline(obj.get('standard_type', '')), inline(' / '.join(filter(None, [str(obj.get('reference', '')), str(obj.get('version', ''))]))), inline(str(obj.get('mandatory', '')).lower() if 'mandatory' in obj else ''), obj.get('status', '')],
        'solution_pattern': [obj['id'], linked_name, inline(' / '.join(filter(None, [str(obj.get('problem', '')), str(obj.get('context', ''))]))), obj.get('status', '')],
        'reference_architecture': [obj['id'], linked_name, inline(' / '.join(filter(None, [str(obj.get('scope', '')), str(obj.get('applicability', ''))]))), obj.get('status', '')],
    }[typ]


def add_optional_attributes(lines: list[str], obj: dict, fields: list[tuple[str, str]]):
    rows = []
    for field, label in fields:
        if field in obj and obj[field] not in (None, '', []):
            rows.append((label, fmt_list(obj[field])))
    if rows:
        lines += ['', 'h2. Egenskaper', '']
        for label, value in rows:
            lines.append(f'* *{label}:* {value}')


def render_relations(obj: dict, relations: list[dict], all_objects: dict[str, dict]) -> list[str]:
    groups: dict[tuple[str, str], list[str]] = {}
    for rel in relations:
        if rel.get('source') == obj['id']:
            other = rel.get('target')
            label = REL_LABELS.get(rel.get('type'), (rel.get('type'), rel.get('type')))[0]
        elif rel.get('target') == obj['id']:
            other = rel.get('source')
            label = REL_LABELS.get(rel.get('type'), (rel.get('type'), rel.get('type')))[1]
        else:
            continue
        target = all_objects.get(other)
        if target:
            text = f"[{target['name']}|{page_title(target)}] ({{{{{other}}}}})"
        else:
            text = str(other)
        groups.setdefault((label, rel.get('type', '')), []).append(text)
    if not groups:
        return []
    lines = ['', 'h2. Relationer']
    for (label, rel_type), items in sorted(groups.items()):
        lines += ['', f'h3. {label} ({{{{{rel_type}}}}})']
        lines += [f'* {x}' for x in sorted(items, key=str.casefold)]
    return lines


def render_provenance(obj: dict, sources: dict[str, dict], mode: str) -> list[str]:
    evidence = obj.get('provenance') or []
    if not evidence:
        return []
    lines = ['', 'h2. Proveniens']
    for entry in evidence:
        source_id = entry.get('source_id')
        source = sources.get(source_id, {}) if source_id else {}
        bits = []
        if source_id:
            bits.append(f"källa: {source.get('title', source_id)} ({{{{{source_id}}}}})")
        if entry.get('reference'):
            bits.append(f"referens: {entry['reference']}")
        if mode == 'working' and entry.get('confidence'):
            bits.append(f"confidence: {entry['confidence']}")
        if mode == 'working' and entry.get('transferability'):
            bits.append(f"överförbarhet: {entry['transferability']}")
        suffix = f" — {'; '.join(bits)}" if bits else ''
        lines.append(f"* *{entry.get('evidence_type', 'okänd')}*{suffix}")
        if mode == 'working' and entry.get('rationale'):
            lines.append(f"** Motiv: {entry['rationale']}")
        if mode == 'working' and entry.get('derived_from'):
            lines.append(f"** Härledd från: {', '.join(entry['derived_from'])}")
    return lines


def detail_lines(typ: str, obj: dict, rev, mode: str, relations: list[dict], all_objects: dict[str, dict], sources: dict[str, dict]):
    lines = [
        f"h1. {page_title(obj)}",
        '',
        '{info:title=Genererad artefakt}',
        f"Genererad från kanonisk YAML · läge {mode} · projektrevision {rev}",
        '{info}',
        '',
        f"* *ID:* {obj['id']}",
        f"* *Objekttyp:* {obj['type']}",
        f"* *Status:* {obj.get('status', '')}",
    ]
    if obj.get('description'):
        lines += ['', 'h2. Beskrivning', '', obj['description']]

    fields = {
        'driver': [('category', 'Kategori'), ('time_horizon', 'Tidshorisont')],
        'goal': [('target_state', 'Måltillstånd'), ('time_horizon', 'Tidshorisont')],
        'capability': [('capability_type', 'Förmågetyp')],
        'it_support': [('lifecycle', 'Livscykel'), ('criticality', 'Kritikalitet')],
        'platform_service': [('consumer_scope', 'Konsumentomfång'), ('service_level', 'Servicenivå')],
        'platform': [('technology', 'Teknik'), ('products', 'Produkter')],
        'standard': [('standard_type', 'Standardtyp'), ('reference', 'Referens'), ('version', 'Version'), ('mandatory', 'Obligatorisk')],
        'reference_architecture': [('scope', 'Scope'), ('applicability', 'Tillämplighet')],
        'principle': [],
        'solution_pattern': [],
    }[typ]
    add_optional_attributes(lines, obj, fields)

    if typ == 'principle':
        for field, label in [('statement', 'Principformulering'), ('rationale', 'Motivering')]:
            if obj.get(field):
                lines += ['', f'h2. {label}', '', str(obj[field])]
        if obj.get('implications'):
            lines += ['', 'h2. Implikationer', ''] + bullet_lines(obj['implications'])
    elif typ == 'solution_pattern':
        for field, label in [('problem', 'Problem'), ('context', 'Kontext'), ('approach', 'Angreppssätt')]:
            if obj.get(field):
                lines += ['', f'h2. {label}', '', str(obj[field])]
        if obj.get('consequences'):
            lines += ['', 'h2. Konsekvenser', ''] + bullet_lines(obj['consequences'])
    elif typ == 'reference_architecture':
        if obj.get('building_blocks'):
            lines += ['', 'h2. Byggblock', ''] + bullet_lines(obj['building_blocks'])
        if obj.get('guidance'):
            lines += ['', 'h2. Vägledning', ''] + bullet_lines(obj['guidance'])

    if obj.get('functions'):
        lines += ['', 'h2. Funktioner', ''] + bullet_lines(obj['functions'])

    extra = []
    for field, label in [('owner', 'Ägare'), ('aliases', 'Alias'), ('tags', 'Taggar')]:
        if obj.get(field):
            extra.append(f'* *{label}:* {fmt_list(obj[field])}')
    if mode == 'working' and obj.get('notes'):
        extra.append(f"* *Arbetsnotering:* {obj['notes']}")
    if extra:
        lines += ['', 'h2. Övrig metadata', ''] + extra

    lines += render_relations(obj, relations, all_objects)
    lines += render_provenance(obj, sources, mode)
    return lines


def main():
    parser = argparse.ArgumentParser(description='Generate Confluence wiki markup from EA Stödjare YAML model.')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--mode', choices=['working', 'published'], default='working')
    parser.add_argument('--output-dir', default='exports/confluence')
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    model = root / 'model'
    out = root / args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    manifest = {}
    if (root / 'project-manifest.json').exists():
        manifest = json.loads((root / 'project-manifest.json').read_text(encoding='utf-8'))
    rev = manifest.get('project', {}).get('revision', '-')

    sources = {}
    if (model / 'sources.yaml').exists():
        sources = {x['id']: x for x in load_yaml(model / 'sources.yaml').get('sources', [])}

    by_type = {}
    all_objects = {}
    for typ, cfg in TYPE_CFG.items():
        objects = load_yaml(model / cfg[0]).get('objects', []) if (model / cfg[0]).exists() else []
        objects = [obj for obj in objects if obj.get('status') in STATUS[args.mode]]
        if typ == 'capability':
            objects = sorted(objects, key=lambda obj: (obj.get('capability_type', ''), obj.get('name', '').casefold(), obj.get('id', '')))
        else:
            objects = sorted(objects, key=lambda obj: (obj.get('name', '').casefold(), obj.get('id', '')))
        by_type[typ] = objects
        all_objects.update({obj['id']: obj for obj in objects})

    relations = load_yaml(model / 'relations.yaml').get('relations', []) if (model / 'relations.yaml').exists() else []
    relations = [rel for rel in relations if rel.get('status') in STATUS[args.mode]]

    # Remove stale text exports so removed/filtered objects cannot survive from an earlier run.
    for stale in out.rglob('*.txt'):
        stale.unlink()

    for typ, cfg in TYPE_CFG.items():
        objects = by_type[typ]
        columns = catalog_columns(typ)
        lines = [
            f'h1. {cfg[3]}',
            '',
            '{info:title=Genererad artefakt}',
            f'Genererad från kanonisk YAML · läge {args.mode} · projektrevision {rev}',
            '{info}',
            '',
            f'Denna katalog visar {cfg[3].lower()} i EA-modellen.',
            '',
            '|| ' + ' || '.join(columns) + ' ||',
        ]
        if objects:
            for obj in objects:
                lines.append('| ' + ' | '.join(catalog_values(typ, obj)) + ' |')
        else:
            lines.append('| _Inga objekt i valt läge_ |' + ' |' * (len(columns) - 1))
        (out / cfg[1]).write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')

        detail_dir = out / 'objects' / cfg[2]
        detail_dir.mkdir(parents=True, exist_ok=True)
        for obj in objects:
            path = detail_dir / f"{obj['id']}-{slug(obj['name'])}.txt"
            path.write_text('\n'.join(detail_lines(typ, obj, rev, args.mode, relations, all_objects, sources)).rstrip() + '\n', encoding='utf-8')

    print(f'Generated Confluence markup in {out} ({args.mode})')


if __name__ == '__main__':
    main()
