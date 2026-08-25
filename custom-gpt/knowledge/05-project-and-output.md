<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Project And Output

Denna fil konsoliderar följande kanoniska källor:

- `docs/runtime-project-output-v2.md`
- `docs/backward-compatibility-contract.md`
- `docs/project-metamodel-format.md`
- `docs/derived-views.md`
- `docs/presentation-contract.md`
- `docs/metamodel-aware-generation.md`
- `docs/structural-validation-v2.md`

---


# KÄLLA: `docs/runtime-project-output-v2.md`

# Runtimekontrakt – projekt, output och kompatibilitet v2

## Projektmetamodell

Native v2 deklarerar sin faktiska modell i `project-metamodel.yaml`: basprofil, aktiva/inaktiva standardtyper, custom types, attribut, relationer, värdemängder, extensions, derived views och presentationsdelta. Resolverad metamodell är härledd och inte source of truth.

## Kompatibilitet

- legacy v1 använder fryst v1-profil,
- extended legacy använder rekonstruerad/projektspecifik profil,
- native v2 använder aktuell projektmetamodell,
- unknown stoppas för semantisk automatiktolkning.

## Derived views och presentation

Derived views är deterministiska, regenererbara och `source_of_truth: false`. Presentation contract styr läsaretiketter, ordning, rubriker och visning men får inte ändra semantik eller proveniens.

## Dokumentgenerering

Markdown, Confluence, DOCX och PDF genereras från projektets effektiva metamodell och presentation contract. Generation manifest beskriver vilka kataloger som skapats. Product, custom types och extensions ska följa med när de är aktiva; avaktiverade typer utelämnas.

## Validering och release

`scripts/validate_project.py` är gemensam strukturell grind och kan skriva maskinläsbar valideringsrapport. CI/release ska även kontrollera legacy v1, extended legacy/rev80, migration, Builder-distributioner, dokumentexport och release unpack-and-validate.


# KÄLLA: `docs/backward-compatibility-contract.md`

# EA Stödjare v2 – bakåtkompatibilitetskontrakt

## 1. Syfte

Detta dokument definierar vad nästa EA Stödjare-version måste kunna göra med projekt som skapats med tidigare versioner.

Kontraktet är styrande för v2-utvecklingen och ska användas som releasegrind.

Målet är inte att alla äldre projekt automatiskt ska konverteras till v2. Målet är att de ska kunna **öppnas, förstås, fortsätta användas och migreras kontrollerat**.

## 2. Grundprincip

> En ny GPT-version får inte göra ett äldre EA Stödjare-projekt oanvändbart enbart för att standardmetamodellen utvecklats.

Bakåtkompatibilitet innebär därför både **read compatibility**, **work compatibility** och **migration compatibility**.

## 3. Projektklasser som v2 måste känna igen

### 3.1 Native v2 project

Projekt som innehåller en explicit v2-kompatibel projektmetamodell.

GPT:n ska läsa denna metamodell före projektets objektdata.

### 3.2 Legacy v1 project

Projekt som följer den fasta v1-metamodellen och v1-projektformatet.

GPT:n ska kunna:

1. identifiera projektet som v1,
2. ladda en explicit v1-kompatibilitetsprofil,
3. tolka v1-objekt och relationer enligt v1-semantiken,
4. fortsätta arbeta med projektet utan obligatorisk migration,
5. erbjuda migration när en v2-funktion motiverar det.

### 3.3 Extended legacy project

Projekt som utgått från v1 men där verkligt arbete har lagt till supporting-modeller, projektspecifika schemas, härledda vyer eller andra extension-liknande koncept.

Referensprojektet `it-formagemodell-del3-rev80` är obligatoriskt testfall för denna klass.

GPT:n ska kunna:

1. identifiera v1-kärnan,
2. inventera projektspecifika utvidgningar,
3. skilja aktiv semantik från experiment/pensionerade koncept,
4. rekonstruera den faktiskt använda metamodellen,
5. dokumentera denna maskinläsbart,
6. fortsätta arbeta med projektet utan att först kräva full migration,
7. skapa en kontrollerad v2-migration när användaren väljer det.

### 3.4 Unknown or ambiguous project

Om GPT:n inte säkert kan identifiera projektets metamodell får den inte tyst anta v2-standardmodellen.

Den ska:

- inventera schemas, model-filer och manifest,
- ange vad som är säkert identifierat,
- markera osäkerheter,
- undvika destruktiva modelländringar tills projektsemantiken är tillräckligt förstådd.

## 4. Read compatibility

V2 ska kunna läsa v1-projekt utan att kräva att projektfiler först skrivs om.

Minimikrav:

- v1-ID-prefix ska förstås,
- v1-objekttyper ska förstås,
- v1-attribut ska förstås,
- v1-relationssemantik ska förstås,
- v1-proveniens ska förstås,
- v1-statusvärden ska förstås,
- v1-manifest och filstruktur ska förstås.

V2 ska inte automatiskt applicera ny v2-semantik på äldre data när detta kan ändra betydelsen.

## 5. Work compatibility

Ett legacy-projekt ska kunna fortsätta utvecklas i v2 utan omedelbar migration.

Det innebär att GPT:n vid arbete i legacy mode ska:

- respektera projektets befintliga semantik,
- skapa nya objekt enligt projektets legacy-profil om användaren inte valt migration,
- undvika att skriva v2-only-attribut in i v1-filer utan explicit formatändring,
- dokumentera om en önskad funktion kräver v2-migration eller project extension.

V2 får alltså fungera som **kompatibel redigerare** av v1-projekt.

## 6. Migration compatibility

Migration ska vara:

- explicit,
- reproducerbar,
- granskningsbar,
- icke-destruktiv,
- informationsbevarande så långt semantiken tillåter.

Migration får inte skriva över originalprojektet som standard.

Den ska skapa:

- ny projektkopia eller ny kontrollerad revision,
- explicit v2-projektmetamodell,
- migreringsrapport,
- lista över automatiskt transformerade objekt/relationer,
- lista över osäkra transformationer som kräver beslut,
- lista över legacy-koncept som bevarats som extensions.

## 7. Stabil ID-princip

Migration ska behålla ett objekts ID när objektets semantiska identitet är oförändrad.

Nytt ID krävs när:

- ett objekt semantiskt ersätts av ett annat,
- en uppdelning skapar flera självständiga objekt,
- ett sammanslaget objekt får ny semantisk identitet.

Pensionerade ID:n får inte återanvändas.

## 8. V1 → v2: kända semantiska skillnader

Följande skillnader får **inte** hanteras med blind textsök/ersätt.

### 8.1 Förmåga `scope`

V1 kan använda ett generellt `scope`.

V2 planerar:

```yaml
in_scope:
out_of_scope:
consumer_scope:
```

Migration måste avgöra om legacy `scope` motsvarar positiv boundary, blandad boundary eller behöver mänsklig granskning.

### 8.2 Plattformstjänst

V1-formuleringar kan implicera ett standardiserat/gemensamt tekniskt erbjudande.

V2-semantiken är realiseringsneutral.

Legacy-data behöver normalt inte skrivas om enbart för definitionens skull, men GPT:n ska tolka äldre objekt enligt v1-profil tills migration gjorts.

### 8.3 Plattform

V1 `platform` kan ha bredare betydelse än planerad v2-standardsemantik.

Migration får inte automatiskt anta att varje v1-Plattform redan är en v2-konceptuell Plattform. Varje objekt måste kunna behållas som legacy-semantik tills en säker klassificering finns.

### 8.4 `realized_by`

V1 kan använda `realized_by` i en betydelse som senare behöver delas mellan konceptuell hemvist och konkret realisering.

Native v2 använder nu:

```text
Platform Service --provided_by--> Platform
```

för konceptuell hemvist. Migration får därför inte mekaniskt byta alla legacy-relationer:

```text
Platform Service --realized_by--> Platform
```

till `provided_by`. En relation får konverteras endast när legacybetydelsen faktiskt är konceptuell hemvist/tillhandahålls inom. Om relationen uttrycker eller kan uttrycka konkret realisering ska den bevaras för manuell semantisk granskning. Rev80 är ett känt fall där PLS→PLT `realized_by` betyder konceptuell hemvist och därmed är en stark kandidat för kontrollerad migration till `provided_by`.

### 8.5 Produkt

Produkt finns inte som standardobjekt i v1.

Legacy-projekt som själva infört produkter ska rekonstrueras som project extension eller migreras till v2:s Product-stöd först efter inventering av faktisk projektsyntax och semantik.

## 9. Referensprojekt rev80 – obligatoriskt kompatibilitetstest

`it-formagemodell-del3-rev80` ska användas som ett verkligt extended legacy-test.

V2-utvecklingen ska kunna verifiera minst:

- 13 IT-förmågor,
- befintliga IT-stöd,
- 92 Plattformstjänster,
- 35 konceptuella Plattformar,
- kanoniska relationer,
- produkt-/teknikreferenser,
- produkt→PLS-realiseringar,
- deploymentklassificering,
- opennessklassificering,
- plattformsmognad,
- relation roles,
- derived views,
- baseline/model freeze/change control,
- pensionerade actual-platform-experiment.

Dessa delar behöver inte alla bli standardfunktioner i v2-kärnan. Kompatibilitetskravet är att den nya GPT:n ska kunna **förstå vad projektet faktiskt använder** och fortsätta arbeta med det.

## 10. Extended legacy reconstruction

När ett projekt saknar explicit project metamodel men har egna supporting-filer ska GPT:n kunna skapa en rekonstruerad beskrivning med minst:

```yaml
base_profile:
detected_object_types:
detected_embedded_structures:
detected_relations:
custom_attributes:
custom_enums:
derived_views:
presentation_semantics:
governance_extensions:
uncertainties:
```

Rekonstruktionen är initialt en analysartefakt och får inte automatiskt bli kanonisk utan kontroll.

## 11. Ingen tyst informationsförlust

Om v2 inte kan representera ett legacy-koncept exakt måste GPT:n:

1. bevara originalinformationen,
2. dokumentera mismatchen,
3. representera konceptet som extension eller legacy payload om möjligt,
4. markera behov av beslut.

Det är inte tillåtet att utelämna information bara för att den inte passar standardmetamodellen.

## 12. Ingen tyst semantisk uppgradering

Följande får inte ske utan evidens eller explicit projektbeslut:

- Product → Actual Platform Offering,
- product capability → actual organizational use,
- actual product use → organizational platform offering,
- `related_to` → hårt `depends_on`,
- legacy `realized_by` → v2 `provided_by`,
- v1 Platform → v2 conceptual Platform.

## 13. Conceptual / market / actual vid migration

Legacy-projekt kan blanda dessa lager.

V2-migrationen ska, där det är möjligt, klassificera information i:

- conceptual,
- market_reference,
- actual_state.

Osäker klassificering ska markeras och bevaras, inte gissas bort.

## 14. Derived views

Legacy-rapporter och supporting-vyer som kan återskapas från kanonisk data ska i v2 kunna klassificeras som derived views.

Migration får inte göra en härledd presentation till ny source of truth.

## 15. Backward compatibility och validatorn

Den framtida v2-validatorn ska kunna arbeta i minst tre explicita lägen:

```text
native-v2
legacy-v1
extended-legacy
```

Valideringen ska använda rätt profil för respektive projekt och får inte rapportera v2-obligatoriska fält som fel i ett legitimt v1-projekt.

## 16. Backward compatibility och dokumentgeneratorer

När ett legacy-projekt öppnas utan migration ska befintlig dokumentgenerering kunna fortsätta använda legacy-semantiken.

När projektet migrerats ska generatorer i stället styras av den explicita v2-projektmetamodellen och presentation contract.

## 17. Releasegrind

En v2-releasekandidat får inte godkännas förrän följande fungerar end-to-end:

1. öppna ett minimalt v1-projekt,
2. analysera det med korrekt v1-semantik,
3. göra en avgränsad ändring utan migration,
4. validera projektet efter ändringen,
5. migrera projektet till v2 i separat kopia,
6. verifiera semantic equivalence där transformationen är säker,
7. öppna rev80 som extended legacy,
8. rekonstruera rev80:s projektmetamodell,
9. fortsätta arbeta med rev80 utan obligatorisk migration,
10. migrera rev80 i separat kopia utan dold informationsförlust.

## 18. Acceptanskriterium

Bakåtkompatibilitetskontraktet är uppfyllt när en användare kan ta en tidigare EA Stödjare-projektzip, öppna den i den nya GPT-versionen och fortsätta arbetet utan att behöva känna till intern v1/v2-migrationsmekanik för att undvika datatapp.


# KÄLLA: `docs/project-metamodel-format.md`

# Projektmetamodellformat v2

## 1. Syfte

EA Stödjare v2 ska inte förutsätta att alla projekt använder exakt samma metamodell. Varje native v2-projekt ska därför kunna bära en maskinläsbar deklaration av den **faktiska metamodell som gäller i projektet**.

Formatet är deklarativt: projektet refererar till en basprofil och beskriver endast vilka delar som aktiveras, stängs av eller utökas. Det ska inte behöva kopiera hela standardmetamodellen.

Detta format är ett styrkontrakt för projektets semantik. Det är inte en katalog över projektets EA-objekt.

## 2. Grundprinciper

1. **Basprofil + delta.** Projektet anger en `base_profile` och deklarerar sina avvikelser/extensions.
2. **Minimum sufficient model.** Ett projekt får inaktivera standardobjekt som inte behövs.
3. **Explicit extension.** Egna objekttyper, attribut och relationer måste deklareras innan de används i kanonisk data.
4. **Ingen tyst semantik.** En GPT får inte anta att en projektspecifik supporting-fil ändrar metamodel utan att detta finns deklarerat eller rekonstruerat som extended legacy.
5. **Projektmetamodellen är styrande.** QA, validering och senare dokumentgenerering ska i v2 läsa projektmetamodellen före projektdata.
6. **Bakåtkompatibilitet först.** Legacy v1-projekt behöver inte innehålla denna fil; de tolkas via compatibility profile tills de migreras.
7. **Derived views är aldrig source of truth.** Formatet tillåter vydefinitioner, men `source_of_truth` måste vara `false`.

## 3. Rekommenderad placering

För native v2-projekt rekommenderas:

```text
model-definition/
  project-metamodel.yaml
```

Projektet kan senare kompletteras med separata extension- eller presentationsfiler, men `project-metamodel.yaml` ska vara den primära ingången till modellsemantiken.

## 4. Toppnivå

```yaml
schema_version: "2.0"
project_metamodel:
  id: example-metamodel
  version: "1.0"
  base_profile:
    id: ea-stodjare-v2
    version: "2.0"
    compatibility_mode: native
```

`project_metamodel.version` är projektets egen metamodellversion och ska inte blandas ihop med projektets innehållsrevision eller EA Stödjares releaseversion.

## 5. Basprofil

`base_profile` anger vilken modell projektet bygger vidare på.

Exempel:

```yaml
base_profile:
  id: ea-stodjare-v2
  version: "2.0"
  compatibility_mode: native
```

Tillåtna compatibility modes är:

- `native`
- `legacy`
- `extended_legacy`
- `custom`

Native v2 använder normalt `native`. Legacy-projekt får sin effektiva metamodell via kompatibilitetslagret och behöver inte skrivas om bara för att detta format finns.

## 6. Aktiva och inaktiva objekttyper

```yaml
object_types:
  enabled:
    - capability
    - it_support
    - platform_service
    - platform
  disabled:
    - driver
    - goal
  custom: []
```

Regler:

- Samma typ får inte avsiktligt förekomma i både `enabled` och `disabled`.
- `enabled` betyder att typen ingår i projektets aktiva modellprofil.
- `disabled` gör frånvaron explicit och ska senare kunna hindra QA från att rapportera falska modellgap.
- Standardtypen måste finnas i basprofilen eller tillföras som `custom`.

## 7. Egna objekttyper

Projekt får deklarera egna objekttyper:

```yaml
custom:
  - type: organization_unit
    display_name: Organisationsenhet
    id_prefix: ORG-
    definition: Organisatorisk enhet som är relevant för projektets arkitekturmodell.
    provenance_required: true
    status_values: [candidate, approved, deprecated, retired]
    attributes:
      - name: name
        type: string
        required: true
```

Custom object types ska vara projektstyrda extensions, inte automatiskt föreslås bli nya kärnobjekt i den generella GPT:n.

## 8. Attribututökningar

Ett projekt kan lägga till attribut på en aktiverad basobjekttyp:

```yaml
attribute_extensions:
  - object_type: capability
    attributes:
      - name: in_scope
        type: array
        item_type: string
        required: false
      - name: out_of_scope
        type: array
        item_type: string
        required: false
```

Detta är mekanismen som kan beskriva ett extended legacy-projekt som rev80 utan att ändra den frysta v1-profilen.

## 9. Relationer

Projektet deklarerar vilka basrelationer som används samt eventuella egna relationer:

```yaml
relations:
  enabled:
    - supports
    - uses
    - related_to
  disabled:
    - influences
  custom:
    - type: owned_by
      definition: Anger ansvarig organisatorisk enhet.
      endpoints:
        - source: [capability, platform]
          target: [organization_unit]
      provenance_required: true
```

Relationens source/target-regler ska vara explicit maskinläsbara.

## 10. Relationskvalificerare

V2-formatet kan deklarera kvalificerande metadata utan att skapa en explosion av relationstyper:

```yaml
relation_qualifiers:
  - name: relation_role
    applies_to: [related_to]
    type: enum
    value_set: relation_role
```

Standardvokabulären för native v2 finns från steg 12 i `schemas/relations.yaml`. Projektmetamodellen använder samma deklarationsmekanism för att aktivera, begränsa eller projektspecifikt utöka kvalificerare där schemat uttryckligen tillåter det.

## 11. Värdemängder

```yaml
value_sets:
  - id: relation_role
    values:
      - responsibility_boundary
      - lifecycle_dependency
      - operational_dependency
```

Ett projekt får också förlänga en värdemängd genom `extension_of`, men konfliktregler och namnrymder formaliseras i extension-steget senare i planen.

## 12. Generella extensions

Projektet ska kunna aktivera paketerade extensions utan att duplicera deras schemas:

```yaml
extensions:
  - id: product-deployment
    version: "1.0"
    enabled: true
```

I steg 4 definieras kontraktet. Själva generella extension-paketen införs senare.

## 13. Derived views

Från v2 steg 17 finns den fullständiga förstaklassdefinitionen i `schemas/derived-view.schema.json` och standardkatalogen i `derived-views/views.yaml`. Projektmetamodellens `derived_views` kan fortsatt användas för projektlokala inline-vyer; semantiken ska följa samma principer och får aldrig bli source of truth.


Projektmetamodellen kan beskriva vilka härledda vyer projektet använder:

```yaml
derived_views:
  - id: capability-service-platform
    source_of_truth: false
    join_path:
      - capability
      - supports:inverse
      - platform_service
      - provided_by
      - platform
    filters: {}
    sort: [capability.name, platform_service.name]
    regeneration_policy: on_source_change
```

Krav:

- `source_of_truth` måste vara `false`.
- Vyn får inte användas för att korrigera kanonisk data bakvägen.
- Join-semantiken måste kunna härledas från projektets aktiva relationsmodell.

## 14. Presentationssemantik

```yaml
presentation:
  contract: reader-oriented-v1
  object_display_pattern: "{name} ({id})"
  labels:
    capability.in_scope: Stödjer
    capability.out_of_scope: Omfattar inte
```

Presentation ändrar inte metamodellsemantik. Den översätter strukturerade fält till ett läsarorienterat språk.

## 15. Governance

Formatet reserverar enkel deklaration för senare change-control:

```yaml
governance:
  change_control: true
  baseline_id: MY-MODEL-v1
  baseline_version: 1.0
  freeze_status: frozen
  retired_id_registry: governance/retired-ids.yaml
  model_changelog: governance/model-changelog.yaml
  metamodel_changelog: governance/metamodel-changelog.yaml
```

Detaljerad change-control finns i `docs/change-control.md`. Governancefältet är en deklarativ pekare; den fulla policyn och loggarna ligger i `governance/`.

## 16. Tre användningsnivåer

### Enkel native v2

Projektet anger basprofil och ett litet urval aktiva objekttyper. Inga custom extensions krävs.

### Avancerad native v2

Projektet aktiverar fler standardtyper, Product och generella extensions samt egna derived views.

### Extended legacy

Ett legacy-projekt behöver inte först migreras till detta format. GPT:n rekonstruerar den effektiva modellen genom v1-profile + project extensions. När projektet senare migreras kan rekonstruktionen materialiseras som en native v2 `project-metamodel.yaml`.

## 17. Rev80 som designfall

Formatet är uttryckligen utformat för att kunna beskriva rev80:s behov:

- basprofil v1,
- capability `in_scope/out_of_scope`,
- realiseringsneutral PLS-semantik som projektöverlagring,
- konceptuell Plattform som projektöverlagring,
- marknadsproduktlager,
- product→PLS-realisering,
- relation roles,
- deployment/openness,
- platform maturity,
- derived views,
- presentation contract,
- freeze/change control.

Det betyder inte att rev80 automatiskt migreras i steg 4. Det betyder att formatet har tillräcklig uttryckskraft för en senare kontrollerad migration.

## 18. Validering i steg 4

I detta steg valideras projektmetamodellfiler fristående mot `schemas/project-metamodel.schema.json`.

Den befintliga strukturvalidatorn görs **inte** ännu metamodellstyrd; detta sker i ett senare steg enligt planen. Steg 4 ändrar därför inte v1-validatorns tolkning av `model/`.

## 19. Ändringar som inte görs i steg 4

Steg 4:

- ändrar inte v1-kärnmetamodellen,
- inför inte Produkt i huvudschemat ännu,
- inför inte `provided_by` eller `can_realize` ännu,
- migrerar inte rev80,
- ändrar inte Builder Instructions/Knowledge,
- ändrar inte dokumentgeneratorernas semantik.

Detta format är kontraktet som senare v2-steg ska implementera mot.

## Extensioner och namnrymder

Återanvändbara extensions definieras separat enligt `schemas/project-extension.schema.json` och registreras i `extensions/registry.yaml`. Projektets `extensions[]` är aktiveringsreferenser, inte inline-kopior av extensionens definitioner. Namespace-, beroende- och konfliktregler samt resolveringsordning finns i `docs/project-extensions.md`.

Inline `custom`-definitioner i projektmetamodellen är fortsatt projektlokala. En resolverad metamodell är en härledd artefakt och får inte ersätta `project-metamodel.yaml` eller de versionssatta extensionpaketen som source of truth.


# KÄLLA: `docs/derived-views.md`

# Derived views i EA Stödjare v2

Derived views är maskinläsbara fråge-/presentationsdefinitioner som **återskapas från kanonisk data**. De är aldrig source of truth för arkitektur-, marknads- eller actual-state-påståenden.

## Grundregler

1. `source_of_truth` ska alltid vara `false`.
2. En vy får endast läsa aktiva objekt, relationer och informationslager; den får inte skriva tillbaka till dem.
3. En vy ska kunna regenereras deterministiskt från samma input.
4. Saknad rad i en vy betyder inte automatiskt att kanonisk data ska tas bort eller läggas till.
5. Marknadssemantik behålls i presentationen. Exempelvis betyder Product `can_realize` inte faktisk användning.
6. Generated output ska betraktas som cache/presentation och kan tas bort och byggas om.

## Katalog

Standarddefinitionerna finns i `derived-views/views.yaml` och valideras mot `schemas/derived-view.schema.json`.

Varje vy anger:

- `id`
- `source_of_truth: false`
- startpunkt (`anchor`)
- `join_path` med relation, riktning och alias
- valfria `filters`
- valfri `aggregation`
- `sort`
- `presentation_semantics`
- `regeneration_policy`

## Standardvyer i steg 17

- Förmåga → Plattformstjänst → Plattform
- Plattform → Plattformstjänst → Förmåga
- Produkt → IT-stöd
- Produkt → Plattformstjänst → Plattform
- härledda plattformsberoenden
- shared realization
- product coverage

## Regenerering

`scripts/generate_derived_views.py` materialiserar vyerna som YAML i vald outputkatalog. Outputen innehåller input-fingeravtryck och `source_of_truth: false` och ska inte behandlas som kanonisk modell.

Exempel:

```bash
python3 scripts/generate_derived_views.py --project-root . --output-dir build/derived-views
```

`on_source_change` betyder att en konsument får cacha resultatet men måste regenerera när relevant kanonisk input ändras. `always` regenereras varje gång. `manual_rebuild` tillåter explicit körning men ändrar inte vyers icke-kanoniska status.


# KÄLLA: `docs/presentation-contract.md`

# Reader-oriented presentation contract

## Syfte

Presentationskontraktet separerar **modellens maskinläsbara semantik** från det språk och den struktur som möter en läsare. Kontraktet finns i `presentation/presentation-contract.yaml` och valideras mot `schemas/presentation-contract.schema.json`.

Kontraktet är uttryckligen `source_of_truth: false`. Det får ändra **etikett, ordning, rubrik och visningsmönster**, men aldrig modellens innebörd, proveniens, informationslager eller relationer.

## Standardvisning av objekt

Standardmönstret är:

```text
Namn (ID)
```

ID visas alltid i standardkontraktet. Ett projektspecifikt kontrakt får välja annan visningspolicy, men ett genererat dokument får inte låta ett presentationsnamn ersätta objektets stabila ID i modellen.

## Fältetiketter

Maskinfält kan få läsarorienterade etiketter. V2-standardkontraktet innehåller bland annat:

| Modellfält | Läsaretikett |
|---|---|
| `capability.in_scope` för IT-förmåga | **Stödjer** |
| `capability.in_scope` för verksamhetsförmåga | **Omfattar** |
| `capability.out_of_scope` | **Omfattar inte** |
| `consumer_scope` | **Avsedda konsumenter** |
| `product.product_kind` | **Produkttyp** |

Den kontextberoende etiketten för `in_scope` ändrar inte fältets semantik. Den gör endast presentationen mer naturlig för läsaren.

## Relationsetiketter

Relationstyper behåller stabila maskinnamn men får riktade läsaretiketter. Exempel:

- `Platform Service --provided_by--> Platform` visas från tjänstens perspektiv som **Tillhandahålls av** och från Plattformens perspektiv som **Tillhandahåller**.
- `Product --can_realize--> IT Support|Platform Service` visas som **Kan realisera** och omvänt **Kan realiseras av**.
- `supports` visas som **Stödjer** / **Stöds av**.

Presentationsetiketten får inte användas för att konvertera en relationstyp till en annan.

## Härledda navigationssektioner

Kontraktet kan deklarera navigationssektioner som bygger på `derived-views/views.yaml`. Dessa sektioner är alltid:

- `source_of_truth: false`,
- regenererbara,
- read-only i presentationslagret,
- förbjudna som underlag för write-back till den kanoniska modellen.

Exempel är **Understöds av** på en Förmåga och **Tillhandahåller** på en Plattform. För Produkt kan sektionerna **Kan realisera IT-stöd** och **Kan realisera Plattformstjänster** visas, men med epistemisk not om att potential inte betyder faktiskt val eller faktisk användning.

## Tomma sektioner

Standardpolicyn är `omit`: en tom sektion visas inte. Kontraktet kan sätta `show_placeholder` globalt eller per navigationssektion om ett projekt behöver synliggöra avsaknad av data.

## Projektanpassning

`project-metamodel.yaml` och extensions får tillföra presentationssemantik enligt de kontrakt som redan etablerats i steg 4 och 14. Projektanpassningar ska vara delta ovanpå ett valt presentationskontrakt, inte kopior av hela basmodellen.

Kontraktet är implementerat och används av den metamodellstyrda Markdown/Confluence/DOCX/PDF-genereringen. Projektanpassningar förblir presentationsdelta och ändrar inte kanonisk semantik.


# KÄLLA: `docs/metamodel-aware-generation.md`

# Metamodell- och presentationsstyrd dokumentgenerering

## Syfte

Från v2 steg 26 genereras Markdown, Confluence markup, DOCX och PDF utifrån projektets **faktiskt aktiva metamodell** och det läsarorienterade presentationskontraktet. Generatorerna ska inte längre anta att alla projekt använder samma fasta uppsättning objekttyper.

## Gemensamt generator-context

`scripts/generator_context.py` är den gemensamma läsmodellen för dokumentgeneratorerna. Den:

1. hittar `model-definition/project-metamodel.yaml` eller `project-metamodel.yaml` när sådan finns,
2. resolverar aktiva extensions,
3. räknar fram aktiva respektive avaktiverade objekttyper och relationer,
4. läser custom object types och deras `model_file`,
5. applicerar presentationskontraktet samt projektspecifika/extension-bidragna etiketter och display patterns,
6. exponerar endast objekt och relationer som gäller i valt `working`/`published`-läge.

Legacy- och enklare projekt utan projektmetamodell behåller bakåtkompatibelt beteende: generatorn upptäcker de kanoniska modellfiler som faktiskt finns. Därmed tvingas inte äldre projekt att migrera enbart för att kunna exporteras.

## Aktiva kataloger

Varje körning av Markdown och Confluence skapar `generation-manifest.json` i outputkatalogen. Manifestet är en härledd artefakt (`source_of_truth: false`) och listar exakt vilka objekttyper/kataloger som genererades.

DOCX/PDF-exporten läser detta manifest i stället för en hårdkodad kataloglista. Därmed följer exempelvis `Product` och projektspecifika custom object types automatiskt med i sammansatta dokument när de är aktiva.

## Presentation contract

Generatorerna använder `presentation/presentation-contract.yaml` för:

- objektvisning, normalt `Namn (ID)`,
- kontextberoende fältetiketter, exempelvis `capability.in_scope` → **Stödjer** för IT-förmåga,
- relationsetiketter, exempelvis `can_realize` → **Kan realisera / Kan realiseras av**,
- projektspecifika och extension-bidragna etiketter.

Presentation får aldrig ändra modellsemantik eller epistemiskt lager.

## Boundary, funktioner och attribut

Native v2-fält presenteras läsarorienterat:

- `in_scope` / `out_of_scope` visas i egen **Avgränsning**-sektion,
- embedded `functions` visas i **Funktioner**,
- övriga deklarerade eller extension-bidragna attribut visas under **Egenskaper**.

Custom object types kan genereras generiskt när deras `model_file` är deklarerad. En särskild typmall behövs alltså inte för grundläggande katalog- och detaljvisning.

## Derived views

Navigationssektioner i presentation contract använder de deklarerade derived views som läsmodell. Exempel:

- Produkt → IT-stöd visas som **Kan realisera IT-stöd**,
- Produkt → Plattformstjänst → Plattform visas som **Kan realisera Plattformstjänster**,
- Förmåga → Plattformstjänst → Plattform används för **Understöds av**.

Navigationsresultaten är alltid `source_of_truth: false`. De får inte skrivas tillbaka till den kanoniska modellen.

`scripts/generate_derived_views.py` använder från steg 26 de kanoniska relationsfälten `source`/`target` och kan använda repositoryts standardkatalog även när det analyserade projektet är ett separat scenario.

## Determinism

Samma modell, projektmetamodell, presentation contract och genereringsläge ska ge byte-stabil Markdown/Confluence-output. DOCX/PDF byggs från den genererade Markdown-strukturen och samma katalogmanifest.

## Legacy-kompatibilitet

- Legacy v1 behöver ingen `project-metamodel.yaml`.
- Befintliga legacy-relationer behåller sina läsaretiketter.
- Avsaknad av Product-fil i äldre projekt skapar inte en tom Produktkatalog.
- Native v2-projekt med Product aktivt eller `products.yaml` i ett enklare scenario får Produkt i exporten.

## Source of truth

Markdown, Confluence, `generation-manifest.json`, DOCX, PDF och derived navigation är alltid härledda artefakter. Ändringar ska göras i kanonisk YAML, projektmetamodell eller presentationskontrakt och därefter regenereras.


# KÄLLA: `docs/structural-validation-v2.md`

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
