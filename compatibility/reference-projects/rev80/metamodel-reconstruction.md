# Rev80 – rekonstruktion av faktiskt använd metamodell

## Syfte

Denna fil dokumenterar `it-formagemodell-del3-rev80` som ett **extended legacy project** för EA Stödjare v2. Rekonstruktionen beskriver modellsemantik och extensions; den kopierar inte projektets kanoniska EA-data och ändrar inte referensprojektet.

Maskinläsbar huvudkälla: `metamodel.yaml`.

## Detekterat utgångsläge

- Basprofil: **EA Stödjare v1**.
- Referensrevision: **80**.
- Manifestet anger 245 filer.
- Kanonisk kärna: **13 IT-förmågor, 10 IT-stöd, 92 Plattformstjänster, 35 Plattformar, 385 relationer och 14 källor**.
- Marknadsreferensen innehåller **295 produkter/tekniska byggblock** i deployment-/produktlagret.

## Vad som är kanoniskt

Den organisationsspecifika konceptuella kärnan ligger fortsatt under `model/`:

- `capabilities.yaml`
- `it-support.yaml`
- `platform-services.yaml`
- `platforms.yaml`
- `relations.yaml`
- `sources.yaml`

Rev80 har däremot utökat semantiken jämfört med ren v1:

- Förmåga använder `in_scope`, `out_of_scope` och `consumer_scope`.
- Plattformstjänst är realiseringsneutral.
- Aktiva Plattformar är konceptuella och produktneutrala.
- `PLS --realized_by--> PLT` betyder i rev80 konceptuell hemvist snarare än konkret produktrealisering.

## Projektspecifika extensions

De viktigaste aktiva extensionerna är:

1. **Capability boundary** – `in_scope`, `out_of_scope`, `consumer_scope`.
2. **Marknadsproduktreferens** – produktkatalog och product kind.
3. **Produkt→PLS-realisering** med roller och evidens.
4. **Deployment/on-prem-modell**.
5. **Openness-modell**.
6. **Relation roles** ovanpå kanoniska relationer.
7. **Plattformsmognad** och boundary/decomposition/merge/singleton-analyser.
8. **Baseline/freeze/change control**.
9. **Derived query views** som uttryckligen inte är source of truth.
10. **Documentation/presentation contract**.

`extension-inventory.yaml` innehåller en fullständig inventering av supporting-YAML-filer och deras metadata.

## Relationer i den aktiva kärnan

| Relation | Antal |
|---|---:|
| `realized_by` | 92 |
| `related_to` | 71 |
| `supports` | 119 |
| `uses` | 103 |

Relation roles används som en separat projektextension. De aktiva rollerna omfattar responsibility boundary, cross-capability support samt informations-, livscykel- och operationella beroenden.

## Actual platform-lagret

Actual-platform-lagret är **inte aktiv metamodell i rev80**.

Tio produktbaserade kandidater sanity-granskades och pensionerades. Projektets uttryckliga lärdom är att produkt-/teknikevidens inte är tillräckligt för att hävda ett separat organisatoriskt plattformserbjudande. Rekonstruktionen markerar därför lagret som `retired_or_noncanonical_experiments`, inte som aktiv objekttyp.

## Epistemiska lager

Rev80 skiljer i praktiken mellan:

1. **Konceptuell organisationsmodell** – `model/`, kanonisk.
2. **Marknadsreferens** – produkt-, deployment-, openness- och realiseringsdata i `supporting/`; inte organisationsfakta.
3. **Faktisk organisationsinformation** – inte fullständigt modellerad och får inte härledas från marknadsreferensen.
4. **Härledda vyer/presentationer** – regenererbara och icke-kanoniska.

## Kompatibilitetsregel

När en ny EA Stödjare-version öppnar rev80 ska den först ladda v1-basprofilen och därefter denna rekonstruerade extensionprofil. Den får inte:

- konvertera `realized_by` till ny v2-semantik implicit,
- göra marknadsprodukt till faktisk organisationsprodukt,
- återaktivera pensionerade actual-platform-kandidater,
- skriva tillbaka derived views till kanonisk modell,
- ignorera baseline/freeze/change-control.

## Framtida migration

Denna rekonstruktion är underlag för senare migrationssteg. Den är **inte själv en migration**. Särskilt följande transformationer måste ske explicit och rapporteras:

- rev80 `PLS realized_by PLT` → möjlig v2 `provided_by`,
- marknadsprodukter → v2 `Product`,
- deployment/openness/maturity → valfria v2-extensions,
- relation roles och derived views → explicita v2-extension-/reportingkontrakt.
