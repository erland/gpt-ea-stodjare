# Migrationsmotor v1 → v2

## Syfte

Migrationsmotorn gör legacy v1-projekt möjliga att flytta till v2-format på ett **reproducerbart, granskningsbart och icke-destruktivt** sätt. Originalprojektet skrivs aldrig över.

## Två faser

1. `plan` analyserar projektet och producerar en migreringsrapport utan att ändra några filer.
2. `apply` skapar en ny projektkopia, genomför endast säkra transformationer och validerar kopian.

```bash
python3 scripts/migrate_v1_to_v2.py --source /path/v1 --mode plan
python3 scripts/migrate_v1_to_v2.py --source /path/v1 --mode apply --output /path/v2
```

Målkatalogen måste saknas. Motorn vägrar skriva till källkatalogen eller skriva över en befintlig målprojektkatalog.

## Säkra transformationer

Motorn bevarar stabila objekt-, relations- och käll-ID:n. Den skapar `project-metamodel.yaml`, uppdaterar manifestets modellmarkörer till v2 och skapar `migration/migration-report.yaml`.

Legacy `capability.scope` bevaras genom en explicit projektattributextension. Det delas inte mekaniskt upp i `in_scope`/`out_of_scope`.

Legacy PLS→PLT `realized_by` byter i migrationskopian relationskod till `legacy_realized_by`. Relationens ID, endpoints, status och proveniens bevaras. Den kan senare bytas till `provided_by` först när konceptuell hemvist har verifierats.

Plattformstjänster och Plattformar bevaras men markeras för semantisk granskning eftersom deras v1- och v2-definitioner skiljer sig.

## Projektspecifika extensions

Om v1-modellen innehåller ytterligare objekttyper i `model/` deklareras de som inline custom object types i projektets explicita v2-metamodell. Deras befintliga modellfil och stabila ID:n bevaras. Motorn gissar inte organisationsfakta eller produktrealisering från stöddata utanför den kanoniska modellen.

## Genererade artefakter

`docs/generated`, `exports/confluence` och `exports/document` är derivat och tas bort ur migrationskopian när de finns. De ska regenereras från den migrerade kanoniska modellen. Detta räknas inte som förlust av kanonisk information.

## Migreringsrapport

Rapporten följer `schemas/migration-report.schema.json` och innehåller:

- käll- och målprofil/revision,
- deterministiskt source fingerprint,
- transformationslista med regel-ID,
- review-required-frågor,
- bevarandegaranti,
- summeringar.

Ett migrerat projekt med kvarstående semantiska frågor får status `applied_with_review_required` och `base_profile.compatibility_mode: custom`. Det ska inte beskrivas som fullt native-v2-semantiskt förrän frågorna är behandlade.

## Icke-mål

Steg 22 gör inte den fulla semantiska verifieringen av ett konkret v1-projekt. Minimalmodellen verifieras end-to-end i steg 23 och rev80 i steg 24.
