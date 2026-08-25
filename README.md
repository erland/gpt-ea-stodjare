# EA Stödjare

**Aktuell release:** **2.0.0**, revision 59  
**Status:** released / frozen  
**Legacy:** v1.0.0-rc1 bevaras som fryst kompatibilitetsprofil

EA Stödjare är ett AI-baserat stöd för enterprise architecture (EA). Det hjälper till att analysera underlag, identifiera och strukturera EA-objekt, hålla isär konceptuell modell, marknadsreferenser och faktisk organisationsstatus samt generera konsistent dokumentation från strukturerad source of truth.

## V2 i korthet

V2 bygger på **base profile + projektspecifikt delta**. Ett projekt kan aktivera/inaktivera standardtyper och deklarera egna objekttyper, attribut, relationer, värdemängder, extensions, derived views och presentationsregler.

Centrala v2-principer:

- Förmåga använder `in_scope`, `out_of_scope` och `consumer_scope`.
- Plattformstjänst är ett realiseringsneutralt tekniskt erbjudande/funktionalitetskontrakt.
- Plattform är en produktneutral konceptuell gruppering av Plattformstjänster.
- Produkt är en generell stödjande objekttyp (`PRD-*`).
- `Product --can_realize--> IT Support|Platform Service` uttrycker potential, inte faktisk användning.
- `Platform Service --provided_by--> Platform` uttrycker konceptuell hemvist.
- Funktion är embedded och lokalt identifierbar, inte en global EA-objekttyp.
- Informationslager hålls isär: `model/`, `market-reference/`, `actual-state/`.
- Derived views är regenererbara och `source_of_truth: false`.
- Presentation contract får ändra läsarrepresentation men aldrig modellsemantik.

## Viktiga kataloger

- `model/` – kanonisk konceptuell modell.
- `market-reference/` – verifierbara marknadspåståenden.
- `actual-state/` – organisationsspecifik faktisk status.
- `schemas/` – format- och metamodellkontrakt.
- `extensions/` – generella valfria extensions.
- `governance/` – baseline, freeze/change-control och retired IDs.
- `compatibility/` – aktiv legacy-/migrations- och regressionsevidens.
- `presentation/` – reader-oriented presentation contract.
- `evals/` – semantiska evaldefinitioner och runtime-evalprotokoll.
- `custom-gpt/` – Builder Instructions och Builder-konfiguration.
- `scripts/` – validatorer, migration, generatorer, distribution och releasegrindar.

## Legacy och migration

`compatibility/ea-stodjare-v1/` är en fryst v1-profil, inte en äldre kopia som kan rensas bort. Den används tillsammans med referensprojekten för att säkerställa att legacy v1 kan öppnas/redigeras utan obligatorisk migration och att v1→v2 samt rev80→v2 sker kontrollerat och icke-destruktivt.

Se:

- [`docs/backward-compatibility-contract.md`](docs/backward-compatibility-contract.md)
- [`docs/migration-guide-v1-to-v2.md`](docs/migration-guide-v1-to-v2.md)
- [`docs/rev80-migration-verification.md`](docs/rev80-migration-verification.md)

## Projektmetamodell och extensions

Projektmetamodellformatet dokumenteras i [`docs/project-metamodel-format.md`](docs/project-metamodel-format.md). Extensions dokumenteras i [`docs/project-extensions.md`](docs/project-extensions.md). De tre valfria generella extensions som härletts från rev80 är:

- `ea.product-deployment`
- `ea.product-openness`
- `ea.platform-maturity`

De ändrar inte kärnobjektens semantik.

## Dokumentgenerering

Markdown, Confluence, DOCX och PDF genereras utifrån faktisk projektmetamodell, aktiva extensions och presentation contract. `generation-manifest.json` beskriver varje körnings output och används av dokumentexporten i stället för hårdkodade objekttypslistor.

Se [`docs/metamodel-aware-generation.md`](docs/metamodel-aware-generation.md).

## Custom GPT och portable chat

Distributionerna använder v2-anpassade Builder Instructions och deterministiskt Builder Knowledge. Projektprofil och projektmetamodell ska alltid identifieras före semantisk tolkning. Legacy v1 och extended legacy får inte implicit migreras.

## Verifiering

Permanenta verifieringsgrindar:

```bash
python3 scripts/validate_project.py --project-root .
python3 scripts/run_workflow_conformance.py --project-root .
python3 scripts/run_full_e2e_regression.py --project-root . --report-file build/full-e2e-report.json
python3 scripts/run_v2_ci_gate.py --project-root . --version 2.0.0
```

`run_full_e2e_regression.py` täcker tolv arbetskedjor: native v2, extensions, legacy-redigering, v1- och rev80-migration, produktanalys för IT-stöd och Plattformstjänst, researchbaserat modellförslag, derived views och dokumentexport.

`run_workflow_conformance.py` ger en snabbare femfallsgrind för projektmetamodell, extensions, informationslager/research, legacy-redigering och v1→v2-migration.

## Semantiska evals

29 evalfall finns definierade. Runtimeverktygen kan förbereda prompts, samla in separata svar/bedömningar och fail-closed skapa en poängsättningsrapport. Extern runtime-eval mot installerad GPT har inte genomförts för 2.0.0 och redovisas därför som `not_executed_external_runtime_required`.

## Styrande dokument

- [`docs/product-vision.md`](docs/product-vision.md)
- [`docs/v2-design-principles.md`](docs/v2-design-principles.md)
- [`docs/metamodel.md`](docs/metamodel.md)
- [`docs/project-metamodel-format.md`](docs/project-metamodel-format.md)
- [`docs/information-layers.md`](docs/information-layers.md)
- [`docs/change-control.md`](docs/change-control.md)
- [`docs/final-release-review-v2.0.0.md`](docs/final-release-review-v2.0.0.md)
- [`docs/release-notes-v2.0.0.md`](docs/release-notes-v2.0.0.md)

Den genomförda utvecklingsplanen finns kvar i [`docs/v2-development-plan.md`](docs/v2-development-plan.md) eftersom eval-coverage och revisionshistorik fortfarande refererar till den; den är historisk dokumentation, inte runtimekontrakt.
