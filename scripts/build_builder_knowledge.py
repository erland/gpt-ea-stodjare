#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse

BUNDLES = {
    "01-domain-model.md": [
        "docs/metamodel.md",
        "docs/relations.md",
        "knowledge/classification-guide.md",
    ],
    "02-evidence-and-research.md": [
        "docs/provenance-model.md",
        "docs/source-policy.md",
        "knowledge/workflow-research.md",
        "knowledge/conflicts-and-uncertainty.md",
    ],
    "03-analysis-and-modeling-workflows.md": [
        "knowledge/workflow-extraction.md",
        "knowledge/workflow-model-design.md",
        "knowledge/workflow-update.md",
        "knowledge/workflow-usage.md",
    ],
    "04-quality-assurance.md": [
        "knowledge/quality-object.md",
        "knowledge/quality-model.md",
    ],
    "05-project-and-output.md": [
        "docs/yaml-model-format.md",
        "docs/project-format.md",
        "knowledge/project-status-rules.md",
        "docs/documentation-profiles.md",
        "docs/markdown-generation.md",
        "docs/confluence-generation.md",
        "docs/document-export.md",
        "docs/structural-validation.md",
    ],
}

INDEX = """# EA Stödjare – Builder Knowledge index

Detta är det genererade Knowledge-paketet för Custom GPT-versionen av **EA Stödjare**.

## Läsordning

1. `01-domain-model.md` – objekttyper, relationer och klassificering.
2. `02-evidence-and-research.md` – proveniens, källpolicy, research, konflikter och osäkerhet.
3. `03-analysis-and-modeling-workflows.md` – extraktion, modellförslag, inkrementella uppdateringar och normala användarflöden.
4. `04-quality-assurance.md` – kvalitetskontroll för objekt och hela modeller.
5. `05-project-and-output.md` – YAML-format, projektformat, status, dokumentation och export.

## Styrhierarki

Builder-instruktionen i `custom-gpt/instructions.md` styr övergripande beteende. Dessa Knowledge-filer innehåller detaljregler. Om en detalj här motsäger Builder-instruktionen ska Builder-instruktionen följas och konflikten flaggas.

## Source of truth

Filerna i denna katalog är **genererade distributionsartefakter**. De ska inte handredigeras. Ändra i stället motsvarande kanoniska dokument under `docs/` eller `knowledge/` och kör `scripts/build_builder_knowledge.py`.

Maskinläsbara schemas ligger kvar under `schemas/` i projektet och används av validering. Builder Knowledge är optimerat för LLM-läsning och återger därför främst de mänskligt läsbara semantiska reglerna.
"""

HEADER = """<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

"""

def build(root: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "00-knowledge-index.md").write_text(INDEX, encoding="utf-8")
    for out_name, sources in BUNDLES.items():
        parts = [HEADER, f"# Builder Knowledge – {out_name[3:-3].replace('-', ' ').title()}\n\n"]
        parts.append("Denna fil konsoliderar följande kanoniska källor:\n\n")
        parts.extend(f"- `{src}`\n" for src in sources)
        parts.append("\n---\n")
        for src in sources:
            p = root / src
            text = p.read_text(encoding="utf-8").strip()
            parts.append(f"\n\n# KÄLLA: `{src}`\n\n{text}\n")
        (out_dir / out_name).write_text("".join(parts), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bygg deterministiskt Builder Knowledge för EA Stödjare.")
    parser.add_argument("--root", default=None, help="Projektrot. Standard: katalogen ovanför scripts/.")
    parser.add_argument("--output", default="custom-gpt/knowledge", help="Output relativt projektroten.")
    args = parser.parse_args()
    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    out_dir = root / args.output
    build(root, out_dir)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
