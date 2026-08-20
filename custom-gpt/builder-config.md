# EA Stödjare – Builder-konfiguration

Detta dokument är en **konfigurationsguide för Custom GPT Builder**. Det är inte ett exportformat från OpenAI och ska därför tillämpas manuellt i Buildern.

## Namn

**EA Stödjare**

## Kort beskrivning

Stöd för enterprise architecture: analysera underlag, identifiera och strukturera EA-objekt, granska och utveckla modeller samt komplettera med relevant research och generera dokumentation.

## Instructions

Använd innehållet i:

- `custom-gpt/instructions.md`

Instruktionen är avsedd att klistras in i Builderns Instructions-fält.

## Knowledge

Ladda upp de genererade filerna i:

- `custom-gpt/knowledge/00-knowledge-index.md`
- `custom-gpt/knowledge/01-domain-model.md`
- `custom-gpt/knowledge/02-evidence-and-research.md`
- `custom-gpt/knowledge/03-analysis-and-modeling-workflows.md`
- `custom-gpt/knowledge/04-quality-assurance.md`
- `custom-gpt/knowledge/05-project-and-output.md`

Filerna genereras med `scripts/build_builder_knowledge.py` och ska inte handredigeras.

## Rekommenderade capabilities

Aktivera där Buildern erbjuder motsvarande funktion:

- **Web/research:** På – central för aktuell omvärldsresearch, standarder och jämförelser.
- **Filanalys/data analysis/code interpreter:** På – behövs för zip-projekt, YAML, validering, generering och export när miljön stödjer det.
- **Image generation:** Inte nödvändig för v1; visualisering ligger utanför första versionens scope.

## Primära conversation starters

1. **Analysera detta underlag och identifiera relevanta EA-objekt.**
2. **Hjälp mig ta fram en lämplig förmågemodell för organisationen.**
3. **Granska vår EA-modell och identifiera överlapp, felklassificeringar och luckor.**
4. **Jämför vår modell med relevant aktuell omvärldspraxis och föreslå förbättringar.**

Starters är medvetet breda. Användarhandledningen innehåller mer specifika exempel för IT-förmågor, plattformstjänster, principer och andra vanliga uppgifter.

## Förväntat startspråk

Svenska. Behåll etablerade tekniska begrepp på engelska när en översättning skulle bli mindre precis, men använd de svenska objektnamnen från metamodel i användarsynligt innehåll.

## Användarhandledning

Se:

- `docs/user-guide.md`
- `knowledge/workflow-usage.md`

## V1-scope att kontrollera i Builder-test

Builder-versionen ska tydligt kunna:

- analysera underlag,
- skilja explicit/derived/proposed/external,
- föreslå EA-modeller med researchstöd,
- klassificera centrala EA-objekt,
- granska befintliga modeller,
- arbeta med EA Stödjare-projekt och YAML som source of truth,
- generera/hantera dokumentationsoutput när verktygsmiljön medger det,
- hålla detaljerad lösningsarkitektur utanför scope.
