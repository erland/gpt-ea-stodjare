# EA Stödjare

**Aktuell release:** **2.0.0**, revision 60  
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

## Runtime-distributioner

EA Stödjare har fem aktiva peer-distributioner från samma v2-semantik:

- **Chat ZIP** – instruktioner, Knowledge, schemas och projektrelaterade resurser.
- **Claude Project** och **Claude Skills** – två separata Claude-distributioner.
- **OpenCode** – workspace-distribution.
- **OpenAI Plugin** – skills-first `ready_runtime_dependent` runtime enligt GPT Byggaren 1.6.33.

Pluginen kräver hostens fil read/write, code execution och persistent workspace-state för verifierade projektändringar. Projektfiler är auktoritativ state och chattminne är inte fallback. Aktuell extern research är ett villkorligt krav för standarder, ramverk, praxis och marknads-/produktdata.

Runtimeverktyg för profil/metamodell, QA, change-control, migration och generering paketeras som script resources. CI-/releaseverktyg och MCP-wrapper ingår inte. Projektprofil och projektmetamodell ska alltid identifieras före semantisk tolkning; legacy v1 och extended legacy får aldrig implicit migreras.

## Verifiering

Permanenta verifieringsgrindar:

```bash
python3 scripts/validate_project.py --project-root .
python3 scripts/run_workflow_conformance.py --project-root .
python3 scripts/run_full_e2e_regression.py --project-root . --report-file build/full-e2e-report.json
python3 scripts/run_v2_ci_gate.py --project-root . --version 2.0.0
python3 scripts/validate_runtime_parity.py
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

## Migration av GPT-distributioner (1.6.33, PR #8)

Projektet har en separat migrationskopia med originalmodellen kvar och fem nya distributioner som genereras med den kanoniska GPT Byggaren-motorn 1.6.33. Se `migration/MIGRATION-1.6.33.md` och `PROJECT_STATUS.md`. Migreringen innebär inte att förändra EA Stödjares v2.0-modellsemantik. Äldre `custom-gpt/` behålls som kanonisk instruktionskälla, inte som aktiv sjätte distribution.

GitHub Actions CI med full pytest och distributionsbygge passerade på PR #8 den 6 november 2026. Externa funktionella värdtester återstår och byggvalidering ska inte tolkas som bevis på runtimeparitet.

## Migrering av CI och release (GPT Byggaren 1.6.33)

Se [MIGRATION-CI-1.6.33.md](MIGRATION-CI-1.6.33.md) för verifierade kontroller, versionslåst engine-installation och öppna releasegrindar.

## Modulära Skills

Den modulära arkitekturen är aktiverad genom `instructions.mode: modular_skills`. Gemensamma regler ligger i `canonical/core.md`; tre separata Skills finns i `canonical/skills/`. Läs [Skill-arkitekturen](canonical/SKILL-ARCHITECTURE.md). Funktionella värdtester kvarstår.

## EA Stödjare Engine ZIP (från och med 2.2.1)

De tre modulära Skillsen innehåller nu fullständiga, isolerade Python-importberoenden. Deras statiska resurser kan fortfarande inte garantera körbarhet i alla AI-värdar.

För OpenAI Plugin i ChatGPT Chat, när värden inte kan köra de inbyggda Skill-skripten direkt, används en separat, versionsbunden `ea-stodjare-engine-<version>.zip`. Den är **EA Stödjares runtimeverktyg**, inte GPT Byggarens distributionsmotor `gpt-byggaren-engine-1.6.33.zip`.

Vid publicerad version 2.2.1 hämtas [EA Engine ZIP](https://github.com/erland/gpt-ea-stodjare/releases/download/v2.2.1/ea-stodjare-engine-2.2.1.zip) från samma release som Plugin ZIP och bifogas i ChatGPT när körning krävs och direktåtkomst saknas. ZIP:en valideras med `engine-package.json`, filernas SHA-256 och `python scripts/selftest_ea_engine.py`. Exekvering kräver kompatibel Python-miljö och deklarerade PyYAML/jsonschema/referencing-beroenden; ingen bifogad ZIP garanterar åtkomst till ett användarprojekt eller externa system.

Bygget kör `scripts/check_packaged_skill_dependencies.py` efter kanonisk distributionsvalidering. Den kontrollerar de fyra runtimes som innehåller fristående Skill-skript (Chat ZIP, Plugin, Claude Skills och OpenCode), deras isolerade importer samt Engine ZIP:ens självtest. Claude Project använder istället sammanställda instruktioner.

## Ett kanoniskt projektpaket (från och med distributionsrelease 2.2.1)

GitHub Release innehåller ett komplett projektarkiv, `ea-stodjare-project-<version>.zip`, skapat av GPT Byggarens kanoniska motor. De fem runtimearkiven och den separata `ea-stodjare-engine-<version>.zip` publiceras bredvid projektpaketet. Tidigare `ea-stodjare-<version>.zip` skapades av det äldre `scripts/package_release.py` och publiceras inte längre automatiskt. Skriptet behålls som historiskt verktyg för äldre arbetsflöden och tas inte bort innan eventuella externa beroenden har bedömts.

Releasegrinden packar upp och strukturvaliderar nu just det kanoniska projektarkivet. Det äldre `.release.json`-sidopaketet produceras inte heller av releaseflödet. `DELIVERY-MANIFEST.json` och `SHA256SUMS.txt` fortsätter att levereras från GPT Byggaren.
