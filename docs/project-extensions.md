# Projektextensions i EA Stödjare v2

## Syfte

Extension-mekanismen gör det möjligt att utöka ett projekts faktiska metamodell utan att ändra eller forka standardprofilen. En extension är ett versionssatt, maskinläsbart paket som kan bidra med objekttyper, attribut, relationer, värdemängder, QA-regler och presentationssemantik.

Extensioner ändrar inte automatiskt legacy v1-semantik. De används av native v2-projekt eller av ett projekt som uttryckligen deklarerat en kompatibel egen basprofil.

## Namnrymder

Kärnprofilens etablerade namn är reserverade. Återanvändbara extensions måste ha:

- ett globalt kvalificerat `extension.id`, exempelvis `ea-stodjare.product-deployment` eller `example.ownership`,
- ett kvalificerat `namespace`, normalt samma som extensionens ID när inga särskilda skäl finns,
- unikt par `(id, version)` i extension-registret.

Bidragens lokala namn får vara korta i extensionfilen (`ownership_domain`, `stewarded_by`). Resolvern behandlar dem som ägda av extensionens namespace och vägrar ladda paketet om ett lokalt namn kolliderar med kärnan, projektets inline-definitioner eller ett annat aktivt extensionpaket.

Inline-definitioner direkt i `project-metamodel.yaml` är projektlokala och behåller steg-4-formatets korta namn. De får inte skugga kärn- eller extensiondefinitioner.

## Extensionpaket

Varje extension följer `schemas/project-extension.schema.json` och deklarerar:

- identitet, version och namespace,
- kompatibla basprofiler,
- beroenden (`requires`) och konflikter (`conflicts_with`),
- bidrag (`contributions`).

Stödda bidrag i steg 14:

- `object_types`
- `attribute_extensions`
- `relations`
- `relation_qualifiers`
- `value_sets`
- `value_set_extensions`
- `qa_rules`
- `presentation`

## Aktivering

Projektet aktiverar en extension under `project_metamodel.extensions`:

```yaml
extensions:
  - id: example.ownership
    version: "1.0"
    enabled: true
```

En aktiv extension måste finnas i `extensions/registry.yaml`, matcha begärd version och vara kompatibel med projektets basprofil. Avstängda extensioner påverkar inte den resolverade metamodellen.

## Konfliktregler

Resolveringen ska avbrytas vid minst följande fall:

1. två aktiva extensions använder samma namespace,
2. två bidrag definierar samma nya objekttyp eller relation,
3. en extension försöker definiera om en kärnobjekttyp eller kärnrelation,
4. ett attribut med samma namn redan finns på samma objekttyp,
5. två nya value sets har samma ID,
6. ett `value_set_extension` riktar sig mot en värdemängd som inte finns,
7. ett tillagt enumvärde redan finns i mål-värdemängden,
8. ett deklarerat beroende saknas eller har fel version,
9. aktiva extensions deklarerar konflikt med varandra,
10. extensionens basprofil är inkompatibel med projektets.

Extensioner får alltså **utöka**, inte tyst omdefiniera, etablerad semantik.

## Resolverad metamodell

`scripts/resolve_project_metamodel.py` sammanför:

1. projektets deklarerade v2-metamodell,
2. aktiverade extensionpaket,
3. extensionernas värdemängdstillägg,
4. QA- och presentationsbidrag.

Resultatet är en deterministisk resolverad representation av projektets faktiska metamodell. Den är en härledd artefakt och är inte source of truth. Source of truth är fortsatt `project-metamodel.yaml` plus de versionssatta extensionpaket som det refererar till.

## Avgränsning i steg 14

Extension-mekanismen är etablerad och testad, men den nuvarande EA-modellvalidatorn är ännu inte fullständigt metamodellstyrd. Det kommer i steg 20. Steg 15 använder mekanismen för att paketera generella optional extensions från rev80.

## Standardiserade valfria extensions från praktiska referensprojekt

Från och med v2 steg 15 finns tre generella, valfria extensionpaket som härletts från praktiskt använda modeller i referensprojektet rev80:

- `ea.product-deployment`
- `ea.product-openness`
- `ea.platform-maturity`

De är uttryckligen **inte kärnmetamodell** och har inga beroenden till varandra. Se `docs/optional-rev80-extensions.md` för semantik, värdemängder och epistemiska skyddsregler.
