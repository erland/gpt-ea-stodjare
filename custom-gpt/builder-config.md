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
- **Image generation:** Valfri; v2:s kärna kräver inte bildgenerering och modell-/diagramsemantik ska inte härledas från dekorativa bilder.

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

## V2-beteende att kontrollera i Builder-test

Builder-versionen ska tydligt kunna:

- detektera native v2, legacy v1, extended legacy och unknown innan projektsemantik används,
- följa projektets faktiska metamodell och aktiva extensions i stället för en hårdkodad typkatalog,
- skilja `explicit`/`derived`/`proposed`/`external` samt conceptual/market/actual,
- skilja Produkt från IT-stöd, Plattformstjänst och Plattform samt förstå `can_realize` och `provided_by`,
- arbeta boundary-first och använda review-flöden utan automatisk kanonisk mutation,
- behandla derived views och presentation contract som icke-kanoniska,
- migrera legacy-projekt konservativt och granskningsbart utan tyst semantisk normalisering,
- köra metamodellstyrd QA och följa change-control/retired-ID-policy,
- använda YAML som source of truth och regenerera dokumentationsoutput när miljön medger det,
- hålla detaljerad lösningsarkitektur utanför standardmetamodellens scope om projektet inte uttryckligen utökar den.
