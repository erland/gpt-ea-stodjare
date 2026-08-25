#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse

BUNDLES = {
    "01-domain-model.md": [
        "docs/v2-design-principles.md",
        "docs/runtime-domain-contract-v2.md",
        "docs/information-layers.md",
    ],
    "02-evidence-and-research.md": [
        "docs/runtime-evidence-contract-v2.md",
        "docs/source-policy.md",
        "knowledge/workflow-research.md",
        "knowledge/conflicts-and-uncertainty.md",
    ],
    "03-analysis-and-modeling-workflows.md": [
        "docs/runtime-workflows-v2.md",
        "knowledge/workflow-project-open.md",
        "knowledge/workflow-boundary-first.md",
        "docs/v1-to-v2-migration-engine.md",
        "docs/rev80-migration-verification.md",
    ],
    "04-quality-assurance.md": [
        "docs/runtime-quality-contract-v2.md",
        "knowledge/quality-metamodel-aware.md",
        "knowledge/change-control.md",
    ],
    "05-project-and-output.md": [
        "docs/runtime-project-output-v2.md",
        "docs/backward-compatibility-contract.md",
        "docs/project-metamodel-format.md",
        "docs/derived-views.md",
        "docs/presentation-contract.md",
        "docs/metamodel-aware-generation.md",
        "docs/structural-validation-v2.md",
    ],
}

INDEX = """# EA Stödjare – Builder Knowledge index

Detta är det genererade Knowledge-paketet för Custom GPT-versionen av **EA Stödjare v2**. Paketet innehåller detaljreglerna som avsiktligt hålls utanför den kompakta Builder-instruktionen.

## Läsordning

1. `01-domain-model.md` – v2-principer, objekttyper, relationer, klassificering, informationslager och extensions.
2. `02-evidence-and-research.md` – proveniens, källpolicy, lagerseparation, research, konflikter och osäkerhet.
3. `03-analysis-and-modeling-workflows.md` – projektöppning, extraktion, boundary-first, modellarbete, uppdatering, användning och migration.
4. `04-quality-assurance.md` – objekt-/modell-QA, metamodellstyrd QA och change-control.
5. `05-project-and-output.md` – kompatibilitet, projektmetamodell, projektformat, derived views, presentation, dokumentation och export.

## Styrhierarki

Builder-instruktionen i `custom-gpt/instructions.md` styr övergripande beteende. Projektets detekterade profil och faktiska metamodell styr projektsemantiken. Dessa Knowledge-filer innehåller detaljregler. Om en detalj här motsäger Builder-instruktionen ska Builder-instruktionen följas och konflikten flaggas.

## Projektprofiler

Vid projektarbete ska profilen fastställas innan modellsemantik används:

- native v2 → projektmetamodell + basprofil + aktiva extensions,
- legacy v1 → fryst v1-kompatibilitetsprofil,
- extended legacy → rekonstruerad/projektspecifik legacy-semantik,
- unknown → ingen automatisk v2-tolkning.

## Source of truth

Filerna i denna katalog är **genererade distributionsartefakter**. De ska inte handredigeras. Ändra i stället motsvarande kanoniska dokument under `docs/` eller `knowledge/` och kör `scripts/build_builder_knowledge.py`.

Maskinläsbara schemas ligger kvar under `schemas/` i projektet och används av validering. Builder Knowledge är optimerat för LLM-läsning och återger därför främst mänskligt läsbara semantiska regler. Derived views och presentation är aldrig source of truth.
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
