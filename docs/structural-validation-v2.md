# Strukturell validering i EA Stödjare v2

## Syfte

`validate_project.py` är den gemensamma strukturella valideringsgrinden för EA Stödjare v2. Den ska inte gissa projektets semantik. Projektprofilen fastställs före modellvalidering och styr vilka kontrakt som appliceras.

## Profilstyrd ordning

1. Detektera projektprofil.
2. Stoppa `unknown` och `invalid_explicit_model` innan modellsemantik appliceras.
3. Native v2: validera manifest, projektmetamodell, base profile, aktiva extensions och effektiv objekt-/relationskatalog.
4. Legacy v1: använd de frysta v1-schemasnapshotarna.
5. Extended legacy rev80, omigrerad: använd rev80-rekonstruktionen och det äldre flat-manifestet utan att först kräva modernt manifestformat.
6. Migrerad rev80: validera den deklarerade `extended_legacy`-kontraktet, inklusive 92 `provided_by`, bevarade supporting-filer och pensionerade ID:n.
7. Validera informationslager, derived views, presentation contract och change-control när de är aktiva.
8. Kontrollera deterministiska genererade artefakter när de finns.

## Metamodellstyrning

För native v2 resolveras `project-metamodel.yaml` mot base profile och extensions. Validering av modellfiler, custom object types, custom relations, attribute extensions, derived views och presentation contract sker mot den **effektiva** metamodellen. Avaktiverade standardtyper ska inte ge falska fel.

## Derived-view reproducibility

`derived-views/views.yaml` valideras som deklaration. Om `build/derived-views/` finns i projektet regenereras materialiserade vyer i en temporär katalog och jämförs byte-för-byte med den incheckade versionen. Materialiserade derived views är alltid `source_of_truth: false`.

## Change-control och pensionerade ID:n

När change-control är aktiverat kontrolleras baseline mot aktuell projektrevision/metamodellversion, freeze-policy, separata modell-/metamodellchangeloggar och retired-ID-registret. Ett pensionerat ID får inte förekomma i aktiva conceptual-, market-, actual- eller derived-data.

## Maskinläsbar rapport

`--json` skriver rapporten till stdout. `--report-file <path>` skriver samma rapport till fil. Rapporten följer `schemas/validation-report.schema.json` och innehåller:

- `valid`,
- detekterad `profile`,
- utförda `stages`,
- summering,
- strukturerade fel och varningar.

Exempel:

```bash
python scripts/validate_project.py --project-root . --repo-root . --report-file build/validation-report.json
```

## Säkerhetsprincip

En grön validator betyder strukturell och deklarerad semantisk konsistens enligt den valda profilen. Den betyder inte att externa påståenden är sanna, att ett föreslaget arkitekturbeslut är korrekt eller att marknadsinformation bevisar faktisk organisationsanvändning.
