# Valfria v2-extensions återanvända från rev80

## Syfte

Steg 15 paketerar tre praktiskt prövade begreppsmodeller från referensprojektet `it-formagemodell-del3-rev80` som **generella, valfria v2-extensions**. De är inte del av kärnmetamodellen och aktiveras endast i projekt som behöver dem.

De tre extensionerna är oberoende av varandra:

- `ea.product-deployment`
- `ea.product-openness`
- `ea.platform-maturity`

Rev80 är designkälla, inte semantisk specialregel. Extensionerna ska kunna användas i andra projekt utan att rev80:s övriga modell följer med.

## `ea.product-deployment`

Utökar `Product` med tre valfria dimensioner:

- `control_plane_location`
- `data_plane_location`
- `deployment_posture`

Dimensionerna är avsiktligt separata. Ett enda fält som "cloud/on-prem" tappar viktig information när kontrollplan och dataplan kan ligga på olika platser.

Extensionen beskriver **produktens dokumenterade driftsättningsmöjligheter eller karaktär**, inte var organisationen faktiskt kör produkten. Faktisk driftsättning kräver separat organisationsspecifik evidens/modellering.

## `ea.product-openness`

Utökar `Product` med `openness`:

- `open_source`
- `open_core`
- `source_available`
- `proprietary`
- `unknown`

Klassificeringen ska vara källstödd. `unknown` är ett legitimt värde när källorna inte räcker.

## `ea.platform-maturity`

Utökar den konceptuella `Platform` med `maturity_class`:

- `cohesive_platform`
- `composite_platform`
- `specialized_platform`
- `conditional_platform`
- `boundary_watch`

Detta är en bedömning av **plattformens konceptuella struktur/boundary**, inte ett mått på produktmognad, teammognad eller faktisk organisatorisk leveransförmåga.

## Aktivering

Extensionerna registreras i `extensions/registry.yaml` och aktiveras per projekt i `project-metamodel.yaml`:

```yaml
extensions:
  - id: ea.product-deployment
    version: "1.0"
    enabled: true
  - id: ea.product-openness
    version: "1.0"
    enabled: true
  - id: ea.platform-maturity
    version: "1.0"
    enabled: false
```

Ett komplett demonstratorprojekt finns i `examples/extensions/rev80-optional-extensions.yaml`.

## Epistemiska skyddsregler

1. Produktdeployment och openness är marknads-/produktinformation om inte ett projekt uttryckligen modellerar och evidensbelägger faktisk organisationsstatus.
2. `deployment_posture` får inte användas som synonym för "så här kör vi produkten".
3. Platform maturity gäller konceptuell modellstruktur och får inte användas för att inferera faktisk produkt- eller organisationsmognad.
4. Extensionerna får aktiveras och avaktiveras oberoende.
5. De får inte ändra betydelsen av kärnobjekten `Product` eller `Platform`.

## Relation till rev80

Värdemängderna är härledda från den rekonstruerade rev80-metamodellen i `compatibility/reference-projects/rev80/metamodel.yaml`. Ingen rev80-verksamhetsdata kopieras till extensionpaketen. Referensprojektets actual-platform-experiment är fortsatt pensionerat och ingår inte i dessa extensions.
