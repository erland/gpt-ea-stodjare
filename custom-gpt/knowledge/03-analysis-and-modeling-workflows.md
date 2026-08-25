<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Analysis And Modeling Workflows

Denna fil konsoliderar följande kanoniska källor:

- `docs/runtime-workflows-v2.md`
- `knowledge/workflow-project-open.md`
- `knowledge/workflow-boundary-first.md`
- `docs/v1-to-v2-migration-engine.md`
- `docs/rev80-migration-verification.md`

---


# KÄLLA: `docs/runtime-workflows-v2.md`

# Runtimekontrakt – arbetsflöden v2

## Projektöppning

1. Detektera profil.
2. Resolvera faktisk metamodell för native v2.
3. Läs projektstatus/change-control.
4. Tillämpa först därefter objekts- och relationssemantik.

V1 och extended legacy får redigeras vidare utan implicit migration. Migration är separat, icke-destruktiv och rapporterad.

## Modellarbete

Arbeta boundary-first: fastställ identitet, in/out scope och konsument innan produktmatchning. Använd boundary review, decomposition review, merge review, singleton sanity, product stress test och composition sanity när relevant. Review-resultat är diagnostiska och får inte själva skriva om kanonisk modell.

## Migration

Planera före apply. Bevara stabila ID:n när semantiken är densamma. Vid tvetydighet: bevara + markera för review i stället för att gissa. Originalprojekt skrivs aldrig över.

## Uppdatering och change-control

Skilj redaktion/evidensuppdatering från controlled model change, breaking model change och metamodel change. Fryst baseline får endast ändras enligt freeze-policy. Pensionerade ID:n återanvänds aldrig.

## Output

Derived views och presentation är regenererbara konsumentlager och aldrig source of truth. Dokumentgeneratorer använder projektets effektiva metamodell och presentation contract.


# KÄLLA: `knowledge/workflow-project-open.md`

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


# KÄLLA: `knowledge/workflow-boundary-first.md`

# Arbetsflöde – boundary-first modeling

Använd detta arbetsflöde när nya eller befintliga Förmågor, IT-stöd, Plattformstjänster eller Plattformar behöver granskas, särskilt före produktmatchning eller större strukturförändringar.

## Körordning

1. **Boundary review** – definiera vad objektet är till för, vad som ingår och vad som inte ingår.
2. **Decomposition review** – kontrollera om objektet innehåller flera självständiga semantiska ansvar.
3. **Merge review** – kontrollera om närliggande objekt egentligen beskriver samma stabila ansvar/erbjudande.
4. **Singleton sanity review** – för Plattform med en Plattformstjänst, verifiera legitim konceptuell boundary.
5. **Product stress test** – byt tänkt produkt/realisering och kontrollera att arkitekturobjektets identitet består.
6. **Composition sanity review** – när realiseringen är sammansatt, kontrollera att kompositionen inte blivit arkitekturens definition.

## Beslutsregler

- Gör ingen automatisk split, merge eller omklassificering.
- Produktlikhet eller delad produkt är aldrig ensam tillräcklig grund för merge.
- En singleton-Plattform är inte ett fel; den måste bara ha en självständig konceptuell mening.
- Ett product stress test ska kunna genomföras utan att `can_realize` blandas ihop med faktisk organisationsanvändning.
- Förslag som förändrar kanonisk modell måste gå genom normal evidens-, QA- och change-control-process.
- Om boundaryn fortfarande är oklar: behåll objektet som kandidat eller markera review-behov i stället för att fylla luckan med antaganden.


# KÄLLA: `docs/v1-to-v2-migration-engine.md`

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


# KÄLLA: `docs/rev80-migration-verification.md`

# Rev80 migration och kompatibilitetsverifiering

Steg 24 använder rev80 som extended-legacy stresstest. Projektet föregår det standardiserade `ea-stodjare-project`-manifestet och öppnas därför via en explicit adapter i stället för att låtsas vara ett ordinärt v1-projekt.

## Verifierat normalfall

Källan innehåller 13 IT-förmågor, 10 IT-stöd, 92 Plattformstjänster, 35 konceptuella Plattformar, 385 kanoniska relationer och 14 källor. De 92 `PLS -> PLT realized_by` är enligt rev80-rekonstruktionen entydigt konceptuell hemvist och migreras därför till `provided_by` med oförändrade relations-ID:n och endpoints.

De 55 analytiska relation roles från `supporting/relation-roles.yaml` förs in som relationskvalificerare. Samtliga 92 supporting-YAML bevaras byte-identiskt. Där ingår 295 marknadsprodukter, 295 deploymentposter, 295 opennessposter, produkt–PLS-analyser, maturity-bedömning, derived/query-vyer samt freeze/change-control.

## Epistemisk säkerhet

Marknadsproduktdata flyttas inte automatiskt till faktisk organisationsstatus. Produkt–PLS-realiseringsanalysen är fortsatt marknadspotential, inte bevis på faktisk användning. De tio tidigare Actual Platform-kandidaterna (`PLT-101`–`PLT-110`) förblir pensionerade och får inte återanvändas. Rev80 har fortsatt noll aktiva actual-platform-objekt.

## Extended legacy efter migration

Målet får ett giltigt v2 `project-metamodel.yaml` med `compatibility_mode: extended_legacy`. Det gör att v2 kan använda säker, redan verifierad semantik (`in_scope/out_of_scope`, realiseringsneutral PLS, konceptuell Plattform, `provided_by`) utan att tvinga äldre rev80-konventioner för ID och proveniens genom native-v2-validering.

Följande normalisering skjuts uttryckligen upp: materialisering av marknadsprodukter som native Product-objekt, `can_realize`, deployment/openness/maturity som native extension-attribut, regenerering av derived views och full governance-loggkonvertering. Detta är synligt i migreringsrapporten och räknas inte som dold informationsförlust.
