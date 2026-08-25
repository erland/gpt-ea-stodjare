# EA Stödjare – utvecklingsplan för nästa version

## 1. Syfte

Den här planen beskriver hur nästa version av **EA Stödjare** bör tas fram stegvis utifrån:

- den nuvarande generella EA Stödjare-GPT:n,
- erfarenheterna från det praktiska referensprojektet `it-formagemodell-del3-rev80`,
- dokumentet `metamodell-tillagg-och-rekommendationer-rev80.md`,
- den efterföljande analysen kring Plattform, Plattformstjänst, Produkt, funktioner och projektanpassad metamodell.

Varje steg är avgränsat så att det ska kunna genomföras i en separat prompt, exempelvis:

> Gör steg 6 enligt utvecklingsplanen och ge mig en uppdaterad projekt-zip.

Planen är utformad för **evolution och migration**, inte för ett omtag från noll.

En central acceptansregel för hela arbetet är:

> Ett projekt som skapats med den tidigare EA Stödjare-versionen ska kunna öppnas, förstås och fortsätta utvecklas i den nya versionen utan att användaren först måste bygga om projektet manuellt.

Referensprojektet `it-formagemodell-del3-rev80` ska användas som ett explicit bakåtkompatibilitets- och migreringstest genom hela utvecklingen.

---

# 2. Övergripande målbild

Nästa version av EA Stödjare ska:

1. behålla en liten och användbar standardmetamodell,
2. göra projektets faktiska metamodell explicit och maskinläsbar,
3. tillåta enklare och mer avancerade projektmodeller,
4. kunna utöka standardmetamodellen med projektspecifika objekt, attribut och relationer,
5. tydligare skilja konceptuell arkitektur, marknadsreferens och faktisk organisationsinformation,
6. förbättra semantiken för Plattform och Plattformstjänst,
7. införa Produkt som generellt stödjande objekttyp,
8. behålla Funktion som ett strukturerat underobjekt i normalfallet,
9. förbättra relationer genom några få nya relationstyper och kvalificerande metadata,
10. införa härledda vyer som förstaklasskoncept,
11. stärka boundary-, decomposition-, merge- och singleton-granskning,
12. införa tydligare baseline- och change-control-stöd,
13. kunna migrera och fortsätta arbeta med v1-projekt utan informationsförlust.

---

# 3. Föreslagen standardmetamodell i nästa version

## 3.1 Kärnobjekt

Följande behålls som standardobjekt:

- Drivkraft
- Mål
- Princip
- Förmåga
- IT-stöd
- Plattformstjänst
- Plattform
- Standard
- Lösningsmönster
- Referensarkitektur

## 3.2 Förmåga

Förmåga behåller stöd för:

- verksamhetsförmåga,
- IT-förmåga.

Förmåga bör utökas med tydligare boundary:

```yaml
in_scope:
out_of_scope:
consumer_scope:
```

För IT-förmågor bör `in_scope` användarsynligt normalt presenteras som **Stödjer**.

## 3.3 Plattformstjänst

Plattformstjänst ska definieras realiseringsneutralt:

> Ett stabilt tekniskt erbjudande eller funktionalitetskontrakt som lösningar kan konsumera och som beskriver vad som ska kunna erbjudas utan att låsa hur eller var realiseringen sker.

Det innebär att en Plattformstjänst kan realiseras av exempelvis:

- produkt,
- produktfamilj,
- ramverk,
- bibliotek,
- SaaS,
- central plattform,
- distribuerad runtime,
- komposition av flera byggblock.

## 3.4 Plattform

Användarsynligt namn behålls som **Plattform**, men standardsemantiken ska vara konceptuell:

> En produktneutral konceptuell gruppering av Plattformstjänster som tillsammans utgör ett sammanhållet tekniskt och förvaltningsmässigt erbjudandeområde.

Den generella kärnan ska alltså inte behandla Plattform som synonymt med en viss produkt.

## 3.5 Produkt

Produkt införs som generell stödjande objekttyp.

Definition:

> Ett konkret marknadserbjudande – exempelvis applikationsprodukt, plattformsprodukt, infrastrukturprodukt, SaaS-tjänst, ramverk, bibliotek, verktyg, SDK eller appliance – som kan realisera eller bidra till realiseringen av ett IT-stöd eller en Plattformstjänst.

Produkten bör kunna kategoriseras med `product_kind`, exempelvis:

```yaml
product_kind:
  - application_product
  - platform_product
  - infrastructure_product
  - service_product
  - framework
  - library
  - component_library
  - data_access_framework
  - build_tool
  - testing_framework
  - developer_tool
  - sdk
  - appliance
  - other
  - unknown
```

Produkt ska aldrig automatiskt klassificeras som Plattform.

## 3.6 Funktion

Funktion ska fortsatt normalt vara ett strukturerat underobjekt, inte ett globalt EA-objekt.

Det ska kunna användas på minst:

- IT-stöd,
- Plattformstjänst,
- Plattform.

Vid behov ska ett projekt kunna ge funktioner lokala ID:n för exempelvis produktcoverage utan att göra Funktion till global objekttyp.

---

# 4. Föreslagen relationsmodell

Behåll i huvudsak den lilla relationskärnan:

- `influences`
- `supports`
- `uses`
- `governed_by`
- `constrains`
- `depends_on`
- `derived_from`
- `related_to`

Komplettera med:

- `provided_by`
- `can_realize`

Standardsemantik:

```text
Platform Service --provided_by--> Platform

Product --can_realize--> IT Support
Product --can_realize--> Platform Service
```

`realized_by` får endast behållas där den verkligen betyder konkret realisering, och får inte längre användas som synonym för konceptuell hemvist.

Relationer ska kunna kvalificeras med valfria attribut såsom:

```yaml
relation_role:
strength:
mandatory:
realization_role:
verification_status:
boundary_basis:
notes:
```

Inte alla attribut ska vara tillåtna på alla relationstyper.

---

# 5. Den viktigaste arkitekturförändringen: projektspecifik metamodell

EA Stödjare ska inte längre förutsätta att varje projekt använder exakt standardmetamodellen.

Varje projekt ska bära med sig en maskinläsbar beskrivning av den metamodell som faktiskt gäller.

Princip:

```text
EA Stödjare standardmodell
        ↓
projektets valda profil
        ↓
projektets extensions/avvikelser
        ↓
projektets faktiska metamodell
```

Projektet ska kunna uttrycka exempelvis:

```yaml
metamodel:
  base: ea-stodjare-v2
  project_model_version: 1.0

enabled_object_types:
  - capability
  - it_support
  - platform_service
  - platform
  - product

disabled_object_types:
  - driver
  - goal

extensions:
  - product_deployment
  - platform_maturity
```

GPT:n ska alltid läsa projektets metamodell innan den tolkar projektdata.

---

# 6. Bakåtkompatibilitetsprincip

Nästa version ska känna igen minst tre projektlägen:

## A. Native v2-project

Projekt som uttryckligen innehåller den nya metamodellbeskrivningen.

## B. Legacy v1-project

Projekt skapat med tidigare EA Stödjare och den fasta v1-metamodellen.

GPT:n ska då:

1. identifiera projektet som v1,
2. ladda en inbyggd kompatibilitetsprofil för v1,
3. tolka befintliga YAML-filer enligt v1-semantiken,
4. inte kräva omedelbar migration,
5. kunna fortsätta arbetet,
6. erbjuda kontrollerad migration när det ger nytta.

## C. Extended legacy project

Projekt som utgått från v1 men byggt projektspecifika supporting-modeller, som `it-formagemodell-del3-rev80`.

GPT:n ska:

1. läsa v1-kärnan,
2. inventera projektspecifika extensions,
3. rekonstruera den faktiska använda metamodellen,
4. dokumentera den,
5. kunna fortsätta arbeta utan att först tvinga fram full migration,
6. kunna skapa en v2-kompatibel projektmetamodell när användaren väljer att migrera.

Referensprojektet rev80 ska vara obligatoriskt testfall för detta läge.

---

# 7. Steg-för-steg-plan

## Steg 1 – Fastställ v2-designprinciper och kompatibilitetskontrakt

### Mål

Lås de övergripande designprinciperna innan schemas ändras.

### Genomför

Dokumentera:

- liten standardmetamodell,
- projektmetamodell som source of truth för modellsemantik,
- extensions framför ständig expansion av kärnan,
- bakåtkompatibilitet med v1,
- stöd för extended legacy projects,
- conceptual / market / actual separation,
- candidate-before-canon,
- minimum sufficient model.

### Leverabler

- `docs/v2-design-principles.md`
- `docs/backward-compatibility-contract.md`

### Klart när

Det finns entydiga regler för vad nästa version får bryta respektive måste kunna läsa.

### Prompt

> Genomför steg 1 i v2-planen för EA Stödjare. Fastställ och dokumentera designprinciper och bakåtkompatibilitetskontrakt. Ändra ännu inte den kanoniska metamodellen.

---

## Steg 2 – Inventera v1-projektformat och skapa legacy-profil

### Mål

Göra v1-formatet explicit maskinläsbart som kompatibilitetsprofil.

### Genomför

Samla den tidigare GPT:ns:

- objekttyper,
- attribut,
- relationer,
- proveniensregler,
- statusvärden,
- filstruktur,
- ID-prefix.

Skapa en versionerad profil, exempelvis:

```text
compatibility/
  ea-stodjare-v1/
```

### Leverabler

- `compatibility/ea-stodjare-v1/metamodel.yaml`
- dokumenterad v1-profil.

### Klart när

Ett v1-projekt kan tolkas utan att den nya standardmetamodellen behöver låtsas vara v1.

### Prompt

> Genomför steg 2 i v2-planen. Skapa en explicit legacy-kompatibilitetsprofil för EA Stödjare v1 baserat på den tidigare GPT-versionens faktiska schemas och regler.

---

## Steg 3 – Inventera rev80 som extended legacy project

### Mål

Dokumentera den faktiska metamodell som rev80-projektet använder.

### Genomför

Inventera:

- kärnobjekt,
- supporting-object models,
- produktmodell,
- product→PLS,
- deployment,
- openness,
- maturity,
- derived views,
- relation roles,
- change control,
- presentation contract,
- projektspecifika regler.

Skilj:

- aktiv projektspecifik metamodell,
- tillfälliga experiment,
- pensionerade koncept,
- rent härledda presentationer.

### Leverabler

- `compatibility/reference-projects/rev80/metamodel-reconstruction.md`
- maskinläsbar rekonstruerad metamodell.

### Klart när

Den nya GPT:n kan förklara exakt hur rev80 ska tolkas utan att enbart förlita sig på konversationshistorik.

### Prompt

> Genomför steg 3 i v2-planen. Inventera referensprojektet rev80 som ett extended legacy project och rekonstruera dess faktiskt använda metamodell maskinläsbart. Ändra inte projektets kanoniska modell.

---

## Steg 4 – Definiera v2-projektmetamodellformat

### Mål

Skapa formatet som varje framtida projekt använder för att beskriva sin faktiska metamodell.

### Genomför

Definiera stöd för:

- base profile,
- enabled/disabled object types,
- custom object types,
- custom attributes,
- custom relation types,
- relation constraints,
- enum extensions,
- embedded structures,
- derived views,
- presentation semantics,
- project metamodel version.

### Leverabler

- `schemas/project-metamodel.schema.*`
- `docs/project-metamodel-format.md`
- minimala exempel.

### Prompt

> Genomför steg 4 i v2-planen. Definiera ett maskinläsbart projektmetamodellformat som kan beskriva både enkla standardprojekt och avancerade projektspecifika extensions.

---

## Steg 5 – Inför metamodell-detektion vid projektöppning

### Mål

GPT:n ska alltid veta vilken modell ett projekt använder.

### Genomför

Definiera prioritet:

1. explicit v2 project metamodel,
2. explicit legacy marker,
3. v1 manifest/schema-detektion,
4. extended legacy reconstruction,
5. osäker/okänd modell.

GPT:n får inte tolka okända projekttyper med standardmodellen av bekvämlighet.

### Leverabler

- `knowledge/workflow-project-open.md`
- detektionsregler/tester.

### Prompt

> Genomför steg 5 i v2-planen. Implementera arbetsflöde och regler för att identifiera och ladda rätt metamodell när ett projekt öppnas.

---

## Steg 6 – Revidera Förmåga-boundary

### Mål

Inför lärdomarna från rev80 utan att bryta v1.

### Genomför

V2-standard för Förmåga:

```yaml
in_scope:
out_of_scope:
consumer_scope:
```

Stöd legacy `scope` via kompatibilitetsprofil/migration.

Definiera presentation:

- IT-förmåga `in_scope` → **Stödjer**
- `out_of_scope` → **Omfattar inte**

### Leverabler

- uppdaterad metamodel,
- schemas,
- migrationsregel,
- QA-regler.

### Prompt

> Genomför steg 6 i v2-planen. Utöka Förmåga med in_scope/out_of_scope/consumer_scope och inför kompatibilitet med legacy scope.

---

## Steg 7 – Revidera Plattformstjänst-semantiken

### Mål

Ta bort antagandet om central/gemensam runtime.

### Genomför

Inför realiseringsneutral definition och klassificeringsguide.

Lägg eventuellt till optional:

```yaml
realization_pattern:
```

utan att göra fältet obligatoriskt.

### Leverabler

- metamodel,
- classification guide,
- quality rules,
- migration notes.

### Prompt

> Genomför steg 7 i v2-planen. Revidera Plattformstjänst till ett realiseringsneutralt tekniskt erbjudande/funktionalitetskontrakt och uppdatera klassificering och QA.

---

## Steg 8 – Revidera Plattform till konceptuell standardsemantik

### Mål

Gör standardtypen Plattform produktneutral och konceptuell.

### Genomför

Fastställ:

- Plattform grupperar PLS,
- Plattform är produktneutral,
- Plattform behöver inte vara faktisk organisationstjänst,
- singleton-plattform kan vara legitim,
- kompositionsrealisering är legitim.

Skapa v1-kompatibilitetsregler för äldre `platform`.

### Prompt

> Genomför steg 8 i v2-planen. Revidera standardsemantiken för Plattform till konceptuell plattform och säkerställ att legacy v1-projekt fortfarande kan tolkas korrekt.

---

## Steg 9 – Inför Produkt som generell stödjande objekttyp

### Mål

Ge GPT:n en generell marknads-/realiseringsmodell som fungerar både för IT-stöd och Plattformstjänster.

### Genomför

Definiera:

- Produkt,
- ID-prefix,
- `product_kind`,
- kärnattribut,
- proveniens,
- source layer / market reference.

Produkten ska kunna representera exempelvis:

- ordbehandlingsprodukt,
- SaaS,
- OpenShift,
- IBM MQ,
- ramverk,
- bibliotek,
- utvecklingsverktyg.

### Leverabler

- produkt-schema,
- metamodel,
- QA,
- exempel.

### Prompt

> Genomför steg 9 i v2-planen. Inför Produkt som generell stödjande objekttyp och definiera product_kind, proveniens och regler för att hålla Produkt skild från IT-stöd och Plattform.

---

## Steg 10 – Generalisera Produkt→behov-realisering

### Mål

Stöd både ordbehandlingsexemplet och plattformsreferensprojektet.

### Genomför

Inför:

```text
Product --can_realize--> IT Support
Product --can_realize--> Platform Service
```

Definiera generella roller, exempelvis:

```yaml
realization_role:
  - primary
  - partial
  - supporting
```

Tillåt projektextensions för mer detaljerade roller såsom `native_primary`, `integrated` osv.

Kräv proveniens för positiva marknadspåståenden.

### Prompt

> Genomför steg 10 i v2-planen. Inför generaliserad Product can_realize-relation till IT-stöd och Plattformstjänst med evidens och extensibla realization roles.

---

## Steg 11 – Revidera PLS→Plattform-relationen

### Mål

Separera konceptuell hemvist från konkret realisering.

### Genomför

Inför:

```text
Platform Service --provided_by--> Platform
```

Migrera inte automatiskt gamla `realized_by`; skapa semantisk migreringsregel som bedömer legacy-relationens faktiska betydelse.

Behåll `realized_by` endast för projekt som uttryckligen behöver konkret realiseringssemantik.

### Prompt

> Genomför steg 11 i v2-planen. Inför provided_by mellan Plattformstjänst och Plattform och skapa säker kompatibilitets-/migrationshantering för legacy realized_by.

---

## Steg 12 – Inför generella relationskvalificerare

### Mål

Undvika explosion av relationstyper.

### Genomför

Stöd valfria:

- `relation_role`
- `strength`
- `mandatory`
- `realization_role`
- `verification_status`
- `boundary_basis`
- `notes`

Definiera tillämpbarhet per relationstyp.

### Prompt

> Genomför steg 12 i v2-planen. Inför generella relationskvalificerare och maskinläsbara regler för vilka metadata som är tillåtna på respektive relation.

---

## Steg 13 – Behåll Funktion embedded men gör strukturen starkare

### Mål

Stöd funktionsbeskrivning och framtida produktcoverage utan att globalisera Funktion.

### Genomför

Tillåt:

```yaml
functions:
  - id: optional-local-id
    name:
    description:
    required: optional
```

Lokala funktions-ID:n ska vara scoped till moderobjektet.

Stöd på:

- IT-stöd,
- Plattformstjänst,
- Plattform.

### Prompt

> Genomför steg 13 i v2-planen. Förstärk den embedded funktionsmodellen med valfria lokala ID:n och metadata, men behåll Funktion utanför den globala objekttypkärnan.

---

## Steg 14 – Inför extension-mekanism

### Mål

Göra EA Stödjare användbar när standardmodellen inte räcker.

### Genomför

Stöd projektspecifika:

- object types,
- attributes,
- relations,
- enum values,
- QA rules,
- presentation semantics.

Definiera namnrymd och konfliktregler.

### Prompt

> Genomför steg 14 i v2-planen. Implementera en kontrollerad extension-mekanism för projektspecifika objekttyper, attribut, relationer och värdemängder.

---

## Steg 15 – Skapa generella optional extensions från rev80

### Mål

Återanvänd praktiska koncept utan att göra dem obligatorisk kärna.

### Extensions

Skapa minst:

- `product-deployment`
- `product-openness`
- `platform-maturity`

Varje extension ska kunna aktiveras per projekt.

### Prompt

> Genomför steg 15 i v2-planen. Paketera deployment-, openness- och platform-maturity-modellerna som generella men valfria projekt-extensions.

---

## Steg 16 – Inför conceptual / market / actual informationslager

### Mål

Göra den epistemiska separationen explicit utan att kräva Actual Platform som kärnobjekt.

### Genomför

Definiera projektlager, exempelvis:

```text
model/
market-reference/
actual-state/
```

Regler:

- market capability ≠ actual use,
- actual use ≠ organizational offering,
- conceptual need ≠ product choice.

`actual-state` ska kunna använda Produkt direkt när det räcker.

### Prompt

> Genomför steg 16 i v2-planen. Inför explicit separation mellan konceptuell modell, marknadsreferens och faktisk organisationsinformation utan att göra actual_platform_offering till obligatorisk kärnobjekttyp.

---

## Steg 17 – Inför derived views som förstaklasskoncept

### Mål

Göra navigations-/analysvyer reproducerbara utan att duplicera kanonisk data.

### Genomför

Definiera exempelvis:

```yaml
view_id:
source_of_truth: false
join_path:
filters:
sort:
presentation_semantics:
regeneration_policy:
```

Standardvyer kan omfatta:

- Capability → PLS → Platform
- Platform → PLS → Capability
- Product → IT Support
- Product → PLS → Platform
- platform dependencies
- shared realization
- product coverage

### Prompt

> Genomför steg 17 i v2-planen. Inför derived views som maskinläsbara, regenererbara och icke-kanoniska vydefinitioner.

---

## Steg 18 – Inför reader-oriented presentation contract

### Mål

Separera modellens fältnamn från användarspråket.

### Genomför

Definiera exempelvis:

```text
in_scope      → Stödjer
out_of_scope  → Omfattar inte
PLS linkage   → Understöds av
Platform→PLS  → Tillhandahåller
```

Standardpresentation av objekt:

```text
Namn (ID)
```

### Prompt

> Genomför steg 18 i v2-planen. Inför ett separat presentationskontrakt för läsarorienterade rubriker, ID-format och härledda navigationssektioner.

---

## Steg 19 – Förstärk boundary-first modeling

### Mål

Göra rev80-arbetssätten generella.

### Genomför

Inför workflows för:

- boundary review,
- decomposition review,
- merge review,
- singleton sanity review,
- product stress test,
- composition sanity.

### Prompt

> Genomför steg 19 i v2-planen. Inför generella boundary-, decomposition-, merge-, singleton- och product-stress-test-arbetsflöden och koppla dem till QA.

---

## Steg 20 – Revidera modellkvalitetsregler för extensibla projekt

### Mål

QA ska validera projektets faktiska metamodell, inte bara standardmodellen.

### Genomför

Validator/QA ska:

1. ladda projektmetamodell,
2. ladda aktiverade extensions,
3. validera objekt/relationer därefter,
4. använda legacy-profil vid v1,
5. inte flagga avsiktligt inaktiverade objekttyper som luckor.

### Prompt

> Genomför steg 20 i v2-planen. Anpassa objekt- och modellkvalitetskontroller så att de styrs av projektets faktiska metamodell och aktiverade extensions.

---

## Steg 21 – Inför metamodell- och modell-change-control

### Mål

Skilja innehållsändring från ändring av själva modellen.

### Genomför

Stöd ändringsklasser:

- `editorial`
- `evidence_update`
- `controlled_model_change`
- `breaking_model_change`
- `metamodel_change`

Inför:

- baseline ID/version,
- freeze status,
- retired ID-registry,
- model/metamodel changelog.

### Prompt

> Genomför steg 21 i v2-planen. Inför baseline, freeze, retired-ID-registry och change-control som skiljer modelländringar från metamodelländringar.

---

## Steg 22 – Skapa migrationsmotor v1 → v2

### Mål

Göra migration reproducerbar och granskningsbar.

### Genomför

Migreringen ska:

- aldrig skriva över originalprojektet,
- skapa ny revision/kopia,
- generera migreringsrapport,
- bevara stabila ID:n där semantiken är oförändrad,
- markera osäkra relationstransformationer,
- skapa explicit v2 project metamodel,
- flytta projektspecifika extensions till deklarerad struktur.

### Prompt

> Genomför steg 22 i v2-planen. Implementera en säker och reproducerbar migrationsmotor för v1-projekt till v2-format med full migreringsrapport och utan informationsförlust.

---

## Steg 23 – Migreringstest mot minimal v1-modell

### Mål

Verifiera normalfallet först.

### Genomför

Använd v1:s minimala exempelprojekt.

Kontrollera:

- objekt,
- relationer,
- proveniens,
- genererade dokument,
- stable IDs,
- semantic equivalence.

### Prompt

> Genomför steg 23 i v2-planen. Migrera och verifiera det minimala v1-exempelprojektet end-to-end mot den nya modellen och åtgärda generella migreringsproblem.

---

## Steg 24 – Migreringstest mot rev80-referensprojektet

### Mål

Bevisa att ett verkligt extended legacy project kan fortsätta användas.

### Genomför

Migrera/re-konstruera rev80 i en separat kopia.

Verifiera särskilt:

- 13 IT-förmågor,
- IT-stöd,
- 92 PLS,
- 35 konceptuella plattformar,
- produktkatalog,
- produkt→PLS-relationer,
- deployment/openness,
- maturity,
- relation roles,
- derived views,
- model freeze/change control,
- pensionerade experiment.

Ingen informationsförlust får döljas.

### Prompt

> Genomför steg 24 i v2-planen. Testa full bakåtkompatibilitet och migration mot rev80-referensprojektet. Bevara originalet, dokumentera alla transformationer och åtgärda generella kompatibilitetsproblem.

---

## Steg 25 – Lägg till nytt produktanalys-scenario för IT-stöd

### Mål

Stresstesta att Produkt inte blivit plattformsspecifikt.

### Scenario

Exempel:

```text
Förmåga
  ↓
IT-stöd: Ordbehandling
  ├─ funktioner
  ↓
Marknadsprodukter
```

Testa:

- IT-stöd som produktoberoende behov,
- embedded functions,
- flera produkter,
- `can_realize`,
- partial/primary/supporting,
- external market evidence,
- actual usage separat.

### Prompt

> Genomför steg 25 i v2-planen. Lägg till och stresstesta ett komplett produktanalys-scenario för ett applikationsnära IT-stöd, exempelvis Ordbehandling, så att produktmodellen bevisligen fungerar utanför plattformsområdet.

---

## Steg 26 – Revidera Markdown/Confluence/DOCX/PDF-generering

### Mål

Output ska styras av projektmetamodell och presentation contract.

### Genomför

Generatorerna ska:

- upptäcka aktiva objekttyper,
- generera endast relevanta kataloger,
- stödja custom object types där mall finns,
- använda derived views,
- använda reader contract,
- fortsatt vara deterministiska.

### Prompt

> Genomför steg 26 i v2-planen. Anpassa dokumentgeneratorerna till projektmetamodell, extensions, derived views och presentationskontrakt och verifiera determinism.

---

## Steg 27 – Revidera Builder Instructions och Knowledge

### Mål

Custom GPT:n ska förstå den nya modellarkitekturen utan att huvudinstruktionen blir överlastad.

### Genomför

Instruktionen ska särskilt styra:

- projektmetamodell först,
- legacy-kompatibilitet,
- extensibility,
- conceptual/market/actual,
- Produkt,
- boundary-first modeling,
- derived views,
- migration.

Detaljer flyttas till Knowledge.

### Prompt

> Genomför steg 27 i v2-planen. Revidera Builder Instructions och Knowledge för v2 och säkerställ att instruktionen hålls kompakt samt att legacy- och projektmetamodellregler är entydiga.

---

## Steg 28 – Revidera semantiska evals

### Mål

Testa nya risker och bakåtkompatibilitet.

### Lägg till evals för minst:

- v1-project open,
- extended legacy project,
- project metamodel override,
- Produkt vs IT-stöd,
- Produkt vs Plattform,
- can_realize IT-stöd,
- can_realize PLS,
- provided_by,
- legacy realized_by ambiguity,
- embedded function coverage,
- conceptual/market/actual separation,
- derived view is not source of truth,
- project-specific extension,
- metamodel change control.

### Prompt

> Genomför steg 28 i v2-planen. Revidera den semantiska eval-sviten med v2-funktioner och explicit bakåtkompatibilitet.

---

## Steg 29 – Revidera strukturell validator

### Mål

Göra valideringen metamodellstyrd.

### Genomför

Validatorn ska:

- validera project metamodel,
- ladda base profile,
- ladda extensions,
- validera custom schemas,
- känna igen legacy v1,
- kunna validera unmigrated rev80,
- kontrollera derived-view reproducibility,
- kontrollera retired IDs/change control.

### Prompt

> Genomför steg 29 i v2-planen. Gör strukturvalidatorn metamodellstyrd och bakåtkompatibel med både native v2, legacy v1 och extended legacy projects.

---

## Steg 30 – GitHub Actions och releasepaketering för v2

### Mål

Uppdatera CI/release för nya kompatibilitets- och migrationstester.

### Genomför

CI ska minst köra:

- standardprojekt,
- v1 legacy fixture,
- extended legacy fixture,
- migration,
- Builder Knowledge,
- eval definitions,
- generatorer,
- release unpack-and-validate.

### Prompt

> Genomför steg 30 i v2-planen. Uppdatera CI, release och reproducerbar paketering så att både v2- och legacy-kompatibilitet testas automatiskt.

---

## Steg 31 – Full end-to-end regression

### Mål

Verifiera hela arbetskedjan.

### Testa minst:

1. skapa enkelt v2-projekt,
2. skapa avancerat v2-projekt med extensions,
3. öppna v1-projekt utan migration,
4. fortsätta redigera v1-projekt,
5. migrera v1,
6. öppna rev80,
7. migrera rev80,
8. produktanalys för IT-stöd,
9. produktanalys för PLS,
10. researchbaserat modellförslag,
11. derived views,
12. export.

### Prompt

> Genomför steg 31 i v2-planen. Kör en full end-to-end regression över standardprojekt, extensions, v1-kompatibilitet, rev80, migration, produktanalys, research och export och åtgärda generella fel.

---

## Steg 32 – Slutlig helhetsrevision och releasekandidat

### Mål

Avgöra om nästa version är redo för release.

### Kontrollera

- designprinciper,
- backward compatibility,
- v2 standardmetamodell,
- project metamodel,
- extensions,
- Produkt,
- Funktion,
- relationsmodell,
- derived views,
- QA,
- change control,
- migration,
- rev80-kompatibilitet,
- Builder,
- evals,
- CI,
- exports.

### Leverabler

- slutrapport,
- changelog,
- migration guide,
- release notes,
- release candidate zip.

### Prompt

> Genomför steg 32 i v2-planen. Gör en fullständig slutrevision, verifiera bakåtkompatibilitet mot v1 och rev80 och ta fram releasekandidat för nästa EA Stödjare-version.

---

# 8. Rekommenderade grindar

## Grind A – efter steg 5

Den nya versionen måste kunna identifiera:

- native v2,
- legacy v1,
- extended legacy.

Ingen metamodellmigration bör göras innan detta fungerar.

## Grind B – efter steg 14

Standardmetamodell + extensions måste vara stabila innan advanced extensions byggs.

## Grind C – efter steg 22

Migrationsmotorn ska vara generisk innan rev80 används som full migreringsövning.

## Grind D – efter steg 24

Rev80 måste kunna fortsätta användas utan informationsförlust innan Builder/evals/release färdigställs.

---

# 9. Viktiga icke-mål

Nästa version bör fortfarande inte försöka bli en komplett modell för all enterprise architecture.

Följande ska inte automatiskt bli kärnobjekt enbart på grund av v2-arbetet:

- Organisation
- Stakeholder
- Process
- Aktivitet
- Informationsobjekt
- Datadomän
- Projekt
- Initiativ
- Roadmap
- KPI
- Risk
- Requirement
- Constraint
- API contract
- Physical component
- Actual Platform Offering

De kan införas som project extensions när ett verkligt behov finns.

---

# 10. Särskilt om Actual Platform Offering

`actual_platform_offering` ska **inte** införas som obligatorisk standardobjekttyp.

Motivering:

- rev80 visade att produktnärvaro inte är samma sak som ett faktiskt organisatoriskt erbjudande,
- i praktiska fall tenderade den faktiska plattformen att få stark 1–1-koppling till produkt,
- informationsbehovet kan ofta uttryckas med Produkt + actual-state/projektspecifika attribut,
- projekt som verkligen behöver ett separat organisatoriskt tjänsteobjekt kan lägga till det som extension.

Detta bevarar den lilla kärnmodellen.

---

# 11. Definition of Done

Nästa version kan betraktas som klar när:

1. projektets faktiska metamodell alltid kan identifieras,
2. standardmodellen kan användas utan projektspecifika extensions,
3. projekt kan välja en enklare modell,
4. projekt kan utöka modellen kontrollerat,
5. v1-projekt kan öppnas och fortsätta redigeras,
6. rev80 kan öppnas och förstås fullt ut,
7. v1 och rev80 kan migreras reproducerbart,
8. migration bevarar information och stabila ID:n där semantiken är densamma,
9. Plattform och Plattformstjänst har den nya tydliga semantiken,
10. Produkt fungerar för både IT-stöd och Plattformstjänster,
11. Funktion kan användas strukturerat utan global objektexplosion,
12. derived views är reproducerbara och icke-kanoniska,
13. conceptual/market/actual hålls isär,
14. QA styrs av projektets metamodell,
15. dokumentgeneratorerna styrs av projektets metamodell,
16. Builder-versionen följer samma regler,
17. CI testar native v2, v1 legacy och extended legacy,
18. releasekandidaten klarar full end-to-end regression.

---

# 12. Sammanfattad rekommendation

Den viktigaste förändringen i nästa EA Stödjare-version är inte att göra kärnmetamodellen mycket större.

Den viktigaste förändringen är:

> **EA Stödjare ska ha en bra standardmetamodell, men varje projekt ska bära med sig en komplett och maskinläsbar beskrivning av den metamodell som faktiskt används.**

Det gör det möjligt att:

- använda en liten modell när det räcker,
- använda en rikare modell när behovet kräver det,
- införa projektspecifika extensions utan att forka GPT:n,
- fortsätta arbeta med äldre projekt,
- migrera när det ger verklig nytta,
- låta framtida verkliga projekt driva fram nya generella extensions i stället för att försöka förutse alla EA-behov i förväg.
