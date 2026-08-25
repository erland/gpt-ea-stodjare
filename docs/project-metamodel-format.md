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
