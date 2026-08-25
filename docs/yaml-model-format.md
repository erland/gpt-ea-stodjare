# Kanoniskt YAML-format v1

## Syfte

Detta dokument fastställer serialiseringen av EA Stödjares kanoniska modell efter steg 6. Metamodellen beskriver **vilka begrepp som finns**, relationsmodellen beskriver **vilka kopplingar som är tillåtna**, proveniensmodellen beskriver **varför informationen finns**, och detta format beskriver **hur allt lagras i YAML**.

## Grundprincip

`model/` är source of truth för EA-modellens innehåll. Genererad Markdown, Confluence markup, DOCX och PDF ska senare byggas från denna modell och får inte utvecklas till parallella sanningskällor.

## Filstruktur

```text
model/
  sources.yaml
  drivers.yaml
  goals.yaml
  principles.yaml
  capabilities.yaml
  it-support.yaml
  platform-services.yaml
  platforms.yaml
  products.yaml
  standards.yaml
  solution-patterns.yaml
  reference-architectures.yaml
  relations.yaml
```

En objekttyp per fil gör modellen enkel att diffgranska, generera dokumentation från och validera. Källor och relationer är gemensamma register och ligger därför separat.

## Objektfil

Varje objektfil har ett litet envelope:

```yaml
schema_version: "1.0"
object_type: capability
objects:
  - id: CAP-001
    type: capability
    name: Utveckla IT-stöd
    description: Förmåga att utveckla och vidareutveckla IT-stöd.
    status: candidate
    capability_type: it
    provenance:
      - evidence_type: proposed
        rationale: Föreslagen som del av exempelmodellen.
        confidence: medium
```

`type` på varje objekt är avsiktligt kvar även om filen redan anger `object_type`. Redundansen gör fristående objekt begripliga och möjliggör enkel validering av att ett objekt ligger i rätt fil.

## Gemensamma objektfält

Obligatoriska fält är `id`, `type`, `name`, `description`, `status` och `provenance`. Valfria gemensamma fält är `aliases`, `owner`, `tags` och `notes`. Objekttypsspecifika fält definieras i `schemas/object-types.yaml`.

## Funktioner

Funktion är fortfarande ett underordnat begrepp i v1. Därför lagras funktioner inuti IT-stöd, Plattformstjänst och Plattform och får inga globala ID:n:

```yaml
functions:
  - name: Köra containeriserade applikationer
    description: Tillhandahåller exekveringsmiljö för containeriserade workloads.
```

Om funktioner senare behöver egna relationer eller livscykel kan de migreras till fullvärdiga objekt i en framtida schemaversion.

## Källregister och proveniens

`sources.yaml` registrerar varje källa en gång. Objekt och relationer refererar därefter till källan via `source_id`.

`provenance` är en lista, inte ett enskilt block. Ett objekt kan därmed ha flera belägg av olika slag. Ett organisationsspecifikt förslag som inspirerats av extern research ska fortfarande ha en `proposed`-post. Externa källor kan läggas som ytterligare evidensposter men gör inte förslaget till ett internt faktum.

## Relationer

Relationer lagras endast i `relations.yaml`:

```yaml
schema_version: "1.0"
relations:
  - id: REL-001
    type: supports
    source: ITS-001
    target: CAP-001
    status: candidate
    provenance:
      - evidence_type: proposed
        rationale: IT-stödet föreslås stödja förmågan.
        confidence: medium
```

Relationer dupliceras inte som `supports_capabilities`, `uses_platform_services` eller liknande fält på objekt. En enda kanonisk relationsrepresentation minskar synkproblem och gör grafanalys möjlig senare.

## Status och schema-version

Objekt använder `candidate`, `approved`, `deprecated` och `retired`. Relationer använder samma värden för att kunna skilja preliminära kopplingar från accepterade utan en separat livscykelmodell.

`schema_version` beskriver YAML-kontraktet. Projektets revision, manifest och filintegritet införs först i steg 7.

## Identifierare

Objekt-ID följer prefixen i metamodel v1. Relationer använder `REL-`. Källor använder `SRC-` eller `SRC-EXT-`. ID:n ska vara stabila över namnändringar.

## Medvetna förenklingar i v1

- Ingen generell `attributes`-påse; kända fält ska vara explicita.
- Inga relationer dupliceras inne i objekten.
- Funktioner saknar global identitet.
- Produkt och teknik är attribut där de behövs, inte egna kärnobjekt.
- Projektmanifest och revision väntar till steg 7.
- Exekverbar fullvalidering implementeras senare enligt utvecklingsplanen.

## Exempelmodell

`examples/minimal-model/` innehåller syntetisk testdata som demonstrerar samtliga primära och sekundära objekttyper, verksamhets- och IT-förmåga, funktioner, källor, evidenstyper och relationstyper. Den ska inte tolkas som rekommendation för en verklig organisation.


## Produkt i native v2

`model/products.yaml` innehåller stödjande Produkt-objekt (`PRD-*`). Produkt kräver `product_kind` och beskriver ett konkret marknadserbjudande. Produkt är inte automatiskt IT-stöd, Plattformstjänst, Plattform eller faktisk organisationsanvändning. Produktrelationer till IT-stöd/PLS införs i v2 steg 10.

## Embedded Funktion i native v2

`functions[]` får användas på IT-stöd, Plattformstjänst och Plattform. Varje post kräver `name` och kan ha `id`, `description` och `required`. Ett funktions-ID är **lokalt till moderobjektet** och skapar ingen global `FUN-*`-identitet.

```yaml
functions:
  - id: F01
    name: Spåra ändringar
    description: Visa och acceptera eller avvisa ändringar.
    required: true
```

Regler:

- lokalt ID måste vara unikt inom samma moderobjekt,
- samma lokala ID får förekomma under ett annat moderobjekt,
- lokala funktions-ID:n får inte användas som globala relationsmål,
- legacy v1-funktioner utan ID fortsätter vara giltiga,
- migration ska inte skapa lokala ID:n om projektet inte behöver dem.

