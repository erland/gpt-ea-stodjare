# OpenAI Plugin runtime

EA Stödjare distribueras som en skills-first peer-runtime enligt GPT Byggaren 1.5.1.

## Runtimeklassning

OpenAI Plugin är `ready_runtime_dependent`.

Full verifierad projektändring kräver:

- filesystem read,
- filesystem write,
- code execution,
- persistent workspace-state.

Webbresearch är ett villkorligt hostkrav när uppgiften gäller aktuella standarder, ramverk, praxis, marknads- eller produktuppgifter.

## State authority

När ett EA Stödjare-projekt är öppet är projektets filer auktoritativ state. Chattminne är inte fallback för:

- `project-manifest.json`,
- `project-metamodel.yaml`,
- `model/`,
- `market-reference/`,
- `actual-state/`,
- `governance/`.

Projektprofil och effektiv metamodell ska identifieras innan projektets objekt och relationer tolkas eller förändras.

## Runtime scripts

Pluginen paketerar runtimeverktyg för:

- projektvalidering,
- projektdetektion,
- effektiv metamodell,
- kvalitetsregler,
- change-control,
- derived views,
- Markdown/Confluence,
- DOCX/PDF-export,
- v1→v2-migration,
- rev80→v2-migration och migrationsverifiering.

CI-, regressions-, eval- och releaseverktyg paketeras inte som runtimeverktyg.

## Exportberoenden

Markdown och Confluence kan genereras med Python-runtimeverktygen.

DOCX kräver dessutom Pandoc. PDF kräver Pandoc och LibreOffice. Pluginen får inte påstå att ett exportformat skapats om hosten saknar beroendet eller körningen inte lyckades.

## Migration

Migration är alltid explicit. Legacy v1 eller extended legacy får inte implicit tolkas eller skrivas om som native v2. Original, stabila ID:n, proveniens och tvetydig legacysemantik ska bevaras enligt projektets befintliga compatibility- och change-control-kontrakt.

## MCP

Pluginen genererar ingen MCP-wrapper. Script resources körs genom hostens kompatibla code-execution-miljö.
