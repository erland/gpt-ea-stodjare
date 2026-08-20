# EA Stödjare – Builder Knowledge index

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
