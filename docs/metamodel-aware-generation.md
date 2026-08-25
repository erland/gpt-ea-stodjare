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
