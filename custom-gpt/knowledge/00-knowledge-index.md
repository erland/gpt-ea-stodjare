# EA Stödjare – Builder Knowledge index

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
