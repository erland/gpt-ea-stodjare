# Arbetsflöde – öppna projekt och välj metamodell

## Syfte

EA Stödjare ska **alltid fastställa projektets faktiska metamodell innan projektdata tolkas eller ändras**. Standardmetamodellen får inte användas som tyst fallback för ett okänt projekt.

## Detektionsordning

Följ ordningen strikt:

1. **Explicit native v2** – `project-metamodel.yaml` finns och validerar.
2. **Explicit legacy-markör** – `project-compatibility.yaml` anger stödd profil/mode.
3. **Legacy v1 via manifest** – v1:s format- och modellversionsmarkörer matchar den frysta profilen.
4. **Extended legacy** – v1-bas + tydliga semantiska extensions eller känd referensrekonstruktion.
5. **Unknown** – allt annat.

En ogiltig explicit `project-metamodel.yaml` är blockerande. Hoppa inte vidare till en legacyprofil för att få projektet att "fungera".

## Native v2

När `project-metamodel.yaml` validerar:

1. läs `base_profile`,
2. ladda basprofilens semantik,
3. applicera projektets enabled/disabled types,
4. applicera custom types/attributes/relations/value sets,
5. ladda extensions, derived views och presentation,
6. bygg den **effektiva projektmetamodellen**,
7. tolka först därefter projektdata.

## Legacy v1

När v1:s manifestmarkörer matchar och inga semantikändrande extensions upptäcks:

- ladda `compatibility/ea-stodjare-v1/`,
- använd frysta v1-definitioner och relationer,
- respektera legacy guards,
- fortsätt gärna redigera i v1-format om användaren inte valt migration,
- skriv inte v2-only-fält i den kanoniska modellen.

## Extended legacy

När projektet är v1-baserat men innehåller extensions:

1. ladda v1-profilen,
2. inventera extension-filer och semantiska overrides,
3. använd känd rekonstruktion när projektet matchar en verifierad referenssnapshot,
4. rekonstruera annars projektets effektiva metamodell innan ändring,
5. dokumentera osäkerheter,
6. migrera inte automatiskt.

För rev80 ska `compatibility/reference-projects/rev80/` användas som referens. Actual-platform-experiment är pensionerade och derived views är inte source of truth.

## Unknown

När ingen profil kan fastställas:

- stoppa kanoniska modelländringar,
- inventera manifest, schemas, modellfiler och extensions,
- redovisa vilka signaler som saknas eller motsäger varandra,
- skapa vid behov en projektspecifik metamodellbeskrivning,
- börja inte tolka objekt enligt v2-standardsemantik av bekvämlighet.

## Explicit legacy-markör

Ett projekt kan frivilligt lägga till `project-compatibility.yaml`:

```yaml
compatibility:
  profile: ea-stodjare-v1
  mode: legacy
```

För extended legacy:

```yaml
compatibility:
  profile: ea-stodjare-v1
  mode: extended_legacy
  reference_project: it-formagemodell-del3-rev80
```

Markören är ett tolkningsbeslut, inte migration.

## Maskinellt stöd

Kör:

```bash
python scripts/detect_project_profile.py --project-root <projekt> --pretty
```

Resultatet innehåller:

- `classification`,
- `confidence`,
- `selected_profile`,
- `evidence`,
- `blockers`,
- `next_action`.

Klassificeringar:

- `native_v2`
- `legacy_v1`
- `extended_legacy`
- `invalid_explicit_model`
- `unknown`

Detektionsscriptet avgör **vilken semantik som ska laddas**. Det ersätter inte senare full schema-/modellvalidering.
