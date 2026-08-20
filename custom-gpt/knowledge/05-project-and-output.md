<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Project And Output

Denna fil konsoliderar följande kanoniska källor:

- `docs/yaml-model-format.md`
- `docs/project-format.md`
- `knowledge/project-status-rules.md`
- `docs/documentation-profiles.md`
- `docs/markdown-generation.md`
- `docs/confluence-generation.md`
- `docs/document-export.md`
- `docs/structural-validation.md`

---


# KÄLLA: `docs/yaml-model-format.md`

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


# KÄLLA: `docs/project-format.md`

# EA Stödjare – projektformat v1

## 1. Syfte

Detta dokument definierar **EA Stödjares projektformat v1**. Formatet gör ett EA-projekt självbeskrivande, versionsbart och integritetskontrollerbart så att en LLM eller ett verktyg kan läsa, verifiera och uppdatera projektet reproducerbart.

Projektformatet beskriver projektbehållaren. Själva EA-semantiken definieras separat av metamodel, relationsmodell, proveniensmodell och det kanoniska YAML-formatet.

---

## 2. Grundprinciper

1. `project-manifest.json` är projektets maskinläsbara ingångspunkt.
2. `model/` är den kanoniska EA-modellen och är source of truth för arkitekturinnehållet.
3. Projektets **revision** och modellformatens **versioner** är olika saker.
4. Alla sökvägar i manifestet är relativa till projektroten och använder `/` som separator.
5. SHA-256 används för att upptäcka oavsiktliga filändringar.
6. `project-manifest.json` hashas inte av sig självt.
7. Genererad dokumentation och export ska kunna återskapas från den kanoniska modellen och behöver därför inte vara del av den kanoniska integritetsmängden.
8. En uppdatering avslutas med att manifestet skrivs sist, efter att revision, revisionslogg och checksummor har uppdaterats.

---

## 3. Minsta projektstruktur

Ett EA-projekt enligt v1 bör minst ha:

```text
<project-root>/
  project-manifest.json
  revision-log.md
  model/
    drivers.yaml
    goals.yaml
    principles.yaml
    capabilities.yaml
    it-support.yaml
    platform-services.yaml
    platforms.yaml
    standards.yaml
    solution-patterns.yaml
    reference-architectures.yaml
    sources.yaml
    relations.yaml
```

Ett fullt projekt kan dessutom innehålla:

```text
  docs/                 # genererade eller stödjande dokument
  exports/              # Confluence/DOCX/PDF m.m.
  sources/              # lokala källfiler när det är lämpligt
  schemas/              # schemas som följer med projektet
  scripts/              # projektlokal generering/validering
  PROJECT_STATUS.md     # införs som arbetsstatus i steg 8
```

`PROJECT_STATUS.md` är avsiktligt inte obligatorisk i projektformat v1 ännu; arbetsstatusens semantik fastställs i steg 8.

---

## 4. `project-manifest.json`

Manifestet ska vara UTF-8-kodad JSON och följa `schemas/project-manifest.schema.json` när schemat finns tillgängligt.

### 4.1 Toppnivå

```json
{
  "format": "ea-stodjare-project",
  "format_version": "1.0",
  "project": {},
  "model": {},
  "integrity": {},
  "files": []
}
```

### 4.2 `format`

Fast värde:

```text
ea-stodjare-project
```

Det gör att en LLM eller validator kan skilja EA Stödjare-projekt från andra zip-/repositoryformat.

### 4.3 `format_version`

Version på själva projektbehållarens kontrakt.

V1 använder:

```text
1.0
```

Ändring av projektformatversion ska ske medvetet och får inte blandas ihop med en vanlig projektrevision.

---

## 5. Projektmetadata

`project` innehåller minst:

| Fält | Betydelse |
|---|---|
| `id` | Stabil maskinläsbar projektidentitet |
| `name` | Användarvänligt projektnamn |
| `kind` | Typ av projektinstans |
| `language` | Primärt språk enligt BCP 47, exempelvis `sv-SE` |
| `revision` | Monotont heltal för projektets innehållsrevision |
| `created_at` | Tidpunkt då manifeststyrd projektinstans skapades |
| `updated_at` | Tidpunkt för senaste manifeststyrda revision |
| `lifecycle_status` | Övergripande projektstatus |

### 5.1 Projekt-ID

Rekommenderat format:

```text
[a-z0-9][a-z0-9-]{2,63}
```

ID:t ska vara stabilt även om projektets visningsnamn ändras.

### 5.2 `kind`

V1 använder fria men dokumenterade värden. Rekommenderade värden är:

- `ea_model` – normalt EA-projekt,
- `ea_model_template` – återanvändbar tom/starter-modell,
- `ea_reference_example` – exempelprojekt.

### 5.3 `lifecycle_status`

Rekommenderade v1-värden:

- `draft`,
- `active`,
- `review`,
- `approved`,
- `archived`.

Detta är projektets övergripande livscykelstatus och ska inte förväxlas med den mer detaljerade arbetsstatus som införs i steg 8.

---

## 6. Revision

`project.revision` är ett monotont heltal som börjar på `1` när projektet tas under manifeststyrning.

En revision ska ökas när en bestående ändring görs i projektets integritetsskyddade innehåll, till exempel när:

- ett EA-objekt läggs till, ändras eller tas bort,
- en relation ändras,
- en källreferens ändras,
- projektstyrande dokument eller schemas som ingår i integritetsmängden ändras.

Revisionen ska **inte** återställas när exempelvis en ny DOCX exporteras från oförändrad modell.

Införandet av manifestet i EA Stödjares utvecklingsprojekt startar revision `1`; tidigare utvecklingssteg 1–6 mappas inte retroaktivt till projektrevisioner.

---

## 7. Modellmetadata

`model` anger vilka semantiska kontrakt projektet följer.

Exempel:

```json
{
  "root": "model",
  "serialization": "YAML",
  "model_format_version": "1.0",
  "metamodel_version": "1.0",
  "relation_model_version": "1.0",
  "provenance_model_version": "1.0"
}
```

Detta möjliggör många projektrevisioner utan att metamodelversionen behöver ändras.

Om EA Stödjare möter en format-/modellversion som den inte stöder ska den inte gissa. Den ska rapportera versionskonflikten och kräva migration eller ett kompatibelt arbetsläge.

---

## 8. Filinventering

`files` är en deterministiskt sorterad lista över integritetsskyddade projektfiler.

Varje post har:

| Fält | Betydelse |
|---|---|
| `path` | Relativ POSIX-sökväg |
| `role` | Filens funktion i projektet |
| `required` | Om filen krävs för den aktuella projektprofilen |
| `sha256` | SHA-256 över filens exakta bytes |

Tillåtna/rekommenderade roller i v1:

- `canonical_model`
- `schema`
- `governance`
- `documentation_source`
- `support`

Källmaterial som kan vara känsligt eller stort behöver inte kopieras in i projektpaketet bara för att det finns en proveniensreferens. `model/sources.yaml` kan referera till externa eller organisatoriska källor utan att källfilen ingår i integritetsinventeringen.

---

## 9. Integritet

V1 använder:

```json
{
  "algorithm": "sha256",
  "manifest_self_hash": false,
  "inventory_order": "path-ascending",
  "canonical_model_required": true
}
```

### 9.1 Hashning

SHA-256 beräknas över filens råa bytes och skrivs som 64 gemena hexadecimala tecken.

Exempel:

```text
sha256(file_bytes).hexdigest()
```

### 9.2 Manifestet hashar inte sig självt

Det undviker rekursiv självreferens. Manifestets konsistens verifieras i stället genom schema, filinventering och att manifestet skrivs sist i varje revision.

### 9.3 Genererade filer

Genererad Markdown, Confluence markup, DOCX och PDF ska normalt inte vara del av den kanoniska integritetsmängden. Senare generatorsteg kan ha egna outputmanifest/checksummor.

---

## 10. Revisionslogg

`revision-log.md` är den människoläsbara historiken över projektets manifeststyrda revisioner.

Minimikrav per revision:

- revision,
- datum/tid,
- kort ändringssammanfattning,
- ändrade fil-/modellområden,
- eventuell kommentar om migration eller särskild risk.

Manifestet är maskinläsbar aktuell status; revisionsloggen är historisk förklaring.

---

## 11. Reproducerbart uppdateringsförfarande

EA Stödjare eller annat verktyg ska vid uppdatering följa denna ordning:

1. Läs `project-manifest.json`.
2. Kontrollera `format` och stödd `format_version`.
3. Kontrollera modellversionerna.
4. Verifiera att integritetsskyddade filer finns och matchar registrerade SHA-256.
5. Läs den kanoniska YAML-modellen.
6. Tillämpa endast beställda/avsedda ändringar.
7. Uppdatera berörda modell- och projektfiler.
8. Lägg till post i `revision-log.md`.
9. Öka `project.revision` exakt en gång för revisionen.
10. Uppdatera `project.updated_at`.
11. Bygg om den deterministiskt sorterade filinventeringen och dess SHA-256.
12. Skriv `project-manifest.json` sist.
13. Verifiera att manifestet nu motsvarar projektets faktiska filer.

Om SHA-256 inte matchar **innan** ändringen ska EA Stödjare inte tyst skriva över avvikelsen. Avvikelsen ska först redovisas och hanteras som en potentiell extern/okänd ändring.

---

## 12. Datum och tid

Manifestets tidsfält använder ISO 8601 med explicit tidszon, exempelvis:

```text
2026-08-20T17:50:00+02:00
```

Det gör tidpunkten entydig utan att kräva UTC-konvertering i människoläsbara projekt.

---

## 13. Exempelmanifest

Det minimala exempelprojektet under `examples/minimal-model/` innehåller ett konkret `project-manifest.json` och `revision-log.md` som följer detta format.

---

## 14. Medvetna avgränsningar i steg 7

Steg 7 definierar **projektbehållaren**, inte:

- detaljerad arbetsstatus och öppna frågor (`PROJECT_STATUS.md`) – steg 8,
- semantisk innehållsextraktion – steg 9,
- valideringsscript – steg 24,
- generatorversioner/outputmanifest – senare generator- och release-steg.

Detta håller projektformatet stabilt utan att föregripa senare arbetsflöden.


# KÄLLA: `knowledge/project-status-rules.md`

# Regler för projektstatus och arbetsläge

## 1. Syfte

EA Stödjare ska kunna återuppta ett projekt säkert efter en ny chat, en paus eller en överlämning. `PROJECT_STATUS.md` är den mänskligt läsbara sammanfattningen av arbetsläget och kompletterar `project-manifest.json`.

Manifestet svarar främst på **vad projektet är och vilka filer/revisioner som är giltiga**. Statusfilen svarar främst på **var arbetet befinner sig och vad som återstår**.

## 2. Source-of-truth-regel

`PROJECT_STATUS.md` får aldrig ersätta den kanoniska YAML-modellen.

- EA-objekt och relationer hör hemma i `model/`.
- Källor/proveniens hör hemma i den kanoniska modellen.
- Projektets tekniska identitet/revision hör hemma i `project-manifest.json`.
- Arbetsläge, öppna frågor och nästa steg hör hemma i `PROJECT_STATUS.md`.

Om statusfilen och den kanoniska modellen motsäger varandra gäller den kanoniska modellen för EA-innehåll. Motsägelsen ska då rapporteras och statusfilen korrigeras.

## 3. Obligatoriska statusområden

Statusfilen ska minst kunna beskriva:

- aktuell utvecklings-/arbetsstatus,
- genomförda steg eller analyser,
- analyserat underlag,
- modellstatus,
- preliminära delar,
- öppna frågor,
- kända konflikter,
- senaste kvalitetskontroll,
- rekommenderat nästa steg,
- återupptagningsinstruktion.

Tomma områden ska uttryckligen säga att inget finns registrerat, inte bara utelämnas när frånvaron är viktig för återupptagningen.

## 4. Analyserat underlag

För konkreta EA-projekt bör statusen per relevant källa kunna sammanfatta:

- käll-ID eller tydlig referens,
- dokument/version/datum,
- analysstatus: `not_started`, `partial`, `complete`, `superseded`,
- berörda modellområden,
- viktiga begränsningar.

Den detaljerade evidensen ska fortfarande ligga i modellens proveniensstruktur.

## 5. Preliminära objekt och modelldelar

Statusfilen får sammanfatta preliminära områden men ska normalt referera till objekt-ID eller modellområde i stället för att duplicera fullständiga objekt.

Exempel:

> CAP-014–CAP-018 är kandidater och behöver verksamhetsvalideras.

Inte:

> Kopiera hela definitionerna av CAP-014–CAP-018 in i statusfilen.

## 6. Öppna frågor

En öppen fråga ska vara konkret och handlingsbar. Ange när möjligt:

- berört objekt/område,
- varför frågan är öppen,
- vad som krävs för att lösa den,
- om den blockerar fortsatt arbete.

GPT:n ska inte ställa om samma fråga i en ny chat om svaret redan framgår av projektets status eller kanoniska filer.

## 7. Konflikter

Statusfilen ska sammanfatta materiella öppna konflikter och osäkerheter enligt `knowledge/conflicts-and-uncertainty.md`.

En konflikt ska inte lösas genom att tyst välja en källa. Om befintligt underlag, en styrande källa eller ett dokumenterat beslut inte löser konflikten ska den stå kvar med egen lösningsstatus.

Vid många eller komplexa frågor bör ett separat strukturerat issue-register användas enligt `schemas/conflicts-and-uncertainty.yaml`; `PROJECT_STATUS.md` ska då endast sammanfatta de viktigaste aktiva frågorna.

## 8. Senaste kvalitetskontroll

Statusen ska ange:

- datum eller projektrevision,
- vilken kontrollnivå som genomfördes,
- viktiga resultat,
- kända begränsningar.

En gammal kvalitetskontroll får inte framställas som om den täcker senare modelländringar.

## 9. Rekommenderat nästa steg

EA Stödjare ska normalt ange ett tydligt rekommenderat nästa steg efter avslutad arbetsomgång.

Det ska bygga på:

1. användarens uttryckliga mål,
2. utvecklings-/arbetsplanen,
3. blockerande öppna frågor,
4. modellens faktiska status.

I ett utvecklingsprojekt med sekventiell plan är nästa ej genomförda steg normalt rekommendationen om inget blockerar.

## 10. Uppdateringsregler

När en arbetsomgång faktiskt ändrar projektet ska EA Stödjare:

1. verifiera befintlig projektintegritet,
2. utföra den avgränsade ändringen,
3. uppdatera statusfilen,
4. öka projektrevisionen exakt en gång,
5. uppdatera revisionsloggen,
6. uppdatera manifestets tidsstämpel och filinventering,
7. beräkna checksummor sist,
8. verifiera resultatet.

## 11. Återupptagning i ny chat

När ett befintligt EA Stödjare-projekt bifogas ska GPT:n normalt läsa i denna ordning:

1. `project-manifest.json`,
2. `PROJECT_STATUS.md`,
3. relevant utvecklings-/arbetsplan,
4. endast de kanoniska modell- och styrfiler som behövs för uppgiften.

Syftet är att minimera risken att historiskt konversationsminne får högre auktoritet än det bifogade projektet.

## 12. Status är en sammanfattning, inte ett loggarkiv

`PROJECT_STATUS.md` ska hållas aktuell och kompakt. Historiska revisioner hör hemma i `revision-log.md` och Git-historik. Avslutade öppna frågor och gamla nästa-steg-punkter behöver inte ackumuleras i statusfilen.


# KÄLLA: `docs/documentation-profiles.md`

# Markdown-dokumentationsprofiler v1

## Syfte

Detta dokument definierar hur EA Stödjares kanoniska YAML-modell ska presenteras som Markdown. Profilerna är ett **presentationskontrakt**, inte en ny informationsmodell. All sakinformation ska hämtas från `model/`; genererade Markdown-filer får inte bli en parallell source of truth.

## Grundprinciper

1. **YAML före Markdown.** Sakuppgifter ändras i modellen och därefter regenereras dokumentationen.
2. **Determinism.** Samma modell och samma profilinställningar ska ge semantiskt och textuellt stabil output.
3. **Stabila ID:n visas.** ID används för spårbarhet även när läsaren främst arbetar med namn.
4. **Relationer härleds från `relations.yaml`.** De får inte återskapas genom tolkning av löptext.
5. **Proveniens visas proportionerligt.** Arbetsdokument visar mer evidens än publiceringsvyer.
6. **Tomma sektioner utelämnas.** En rubrik ska inte genereras bara för att mallen har stöd för fältet.
7. **Ingen hallucinerad utfyllnad.** Saknade värden återges inte som antagna fakta.
8. **Sekundära objekttyper hålls tydligt sekundära.** Lösningsmönster och Referensarkitekturer stöds, men får inte dra v1 mot detaljerad lösningsarkitektur.

## Två presentationsnivåer

### Katalogprofil

Katalogen ger en kompakt översikt över en objekttyp. Varje objekttyp får en egen katalogfil.

Rekommenderade outputvägar:

```text
docs/generated/
  drivkrafter.md
  mal.md
  principer.md
  formagor.md
  it-stod.md
  plattformstjanster.md
  plattformar.md
  standarder.md
  losningsmonster.md
  referensarkitekturer.md
```

### Detaljprofil

Detaljprofilen visar ett objekt med relevanta attribut, funktioner, relationer och proveniens.

Rekommenderade outputvägar:

```text
docs/generated/objects/<object-type>/<ID>-<slug>.md
```

Exempel:

```text
docs/generated/objects/capabilities/CAP-001-utveckla-it-stod.md
```

## Arbetsvy och publiceringsvy

Generatorn i steg 16 bör stödja minst två lägen:

- `working`: visar `candidate`, `approved` och `deprecated`; visar confidence, evidenstyp och arbetsnoteringar när de finns.
- `published`: visar som standard endast `approved`; utelämnar interna arbetsnoteringar och tekniska proveniensdetaljer som inte behövs för läsaren.

`retired` ska normalt utelämnas från båda vyerna om inte historik uttryckligen efterfrågas.

Detta är en presentationsregel och ändrar inte objektens status i modellen.

## Gemensam katalogstruktur

Varje katalog ska innehålla:

1. H1 med objekttypens svenska pluralnamn.
2. Kort genererad ingress om vad katalogen visar.
3. Metadata med genereringsläge och modell-/projektrevision när informationen finns tillgänglig.
4. En deterministiskt sorterad tabell.
5. Vid behov kort sektion för relaterade kataloger.

### Sortering

Standard är:

1. `name` normaliserat för alfabetisk sortering,
2. `id` som stabil tie-breaker.

För Förmågor grupperas först på `capability_type` (`business`, `it`) och därefter på namn. En framtida explicit ordningsnyckel får ersätta detta, men introduceras inte i steg 15.

### Katalogkolumner

| Typ | Standardkolumner |
|---|---|
| Drivkraft | ID, Namn, Beskrivning, Kategori, Status |
| Mål | ID, Namn, Beskrivning, Tidshorisont, Status |
| Princip | ID, Namn, Principformulering, Status |
| Förmåga | ID, Namn, Typ, Beskrivning, Status |
| IT-stöd | ID, Namn, Beskrivning, Funktioner, Status |
| Plattformstjänst | ID, Namn, Beskrivning, Konsumentomfång, Funktioner, Status |
| Plattform | ID, Namn, Beskrivning, Teknik/produkter, Funktioner, Status |
| Standard | ID, Namn, Typ, Referens/version, Obligatorisk, Status |
| Lösningsmönster | ID, Namn, Problem/kontext, Status |
| Referensarkitektur | ID, Namn, Scope/tillämpbarhet, Status |

Långa listor i tabellceller ska komprimeras till korta kommaseparerade sammanfattningar. Fullständig information hör hemma på detaljsidan.

## Gemensam detaljstruktur

Alla detaljsidor använder följande ordning när informationen finns:

1. `# <Namn>`
2. identitet och status,
3. beskrivning,
4. objekttypsspecifika attribut,
5. funktioner (endast IT-stöd, Plattformstjänst och Plattform),
6. relationer,
7. proveniens/källor,
8. alias, taggar och ägare,
9. notes endast i `working`-läge.

### Identitetsblock

Detaljsidan ska alltid visa minst:

- ID,
- objekttyp,
- status.

### Relationer

Relationer grupperas efter semantisk relation och riktning. Presentationen får använda naturliga svenska etiketter, men den kanoniska relationstypen ska finnas tillgänglig, exempelvis i parentes eller metadata.

Exempel:

```markdown
## Relationer

### Stöds av

- [Identitets- och behörighetssystem](../it-support/ITS-001-identitets-och-behorighetssystem.md) (`ITS-001`)

### Styr

- [Containerplattformstjänst](../platform-services/PLS-001-containerplattformstjanst.md) (`PLS-001`)
```

Om en relaterad detaljsida inte ingår i aktuell export ska namnet och ID:t ändå visas utan bruten länk.

## Proveniens i Markdown

### Working

Visa per evidenspost när tillgängligt:

- evidenstyp (`explicit`, `derived`, `proposed`, `external`),
- källa och referens,
- confidence,
- rationale,
- `derived_from`,
- transferability för extern evidens.

### Published

Visa i första hand källor/referenser som är relevanta för läsaren. `proposed` ska fortfarande framgå som förslag om objektet publiceras i en granskningsleverans. Tekniska interna fält kan döljas, men får aldrig presenteras som starkare evidens än modellen anger.

## Objekttypsprofiler

### Drivkraft

Detaljsidan prioriterar kategori, tidshorisont och evidens för varför drivkraften är relevant. Den ska inte omformulera drivkraften till ett mål.

### Mål

Detaljsidan prioriterar måltillstånd, tidshorisont och mått. Relationer till drivkrafter och förmågor är särskilt relevanta.

### Princip

Detaljsidan prioriterar `statement`, `rationale` och `implications`. Om `statement` saknas används inte beskrivningen automatiskt som en beslutad principformulering; saknaden synliggörs i arbetsvy.

### Förmåga

Detaljsidan visar `capability_type` tydligt och får inte lägga in process-, organisations- eller systembeskrivningar som om de vore förmågeattribut. Relevanta relationer till mål, IT-stöd och Plattformstjänster visas.

### IT-stöd

Detaljsidan prioriterar funktioner, livscykel och criticality när de finns. Förmågor som stöds och Plattformstjänster som används ska kunna visas via relationsregistret.

### Plattformstjänst

Detaljsidan prioriterar erbjudandet till konsumenten: funktioner, service level och consumer scope. Underliggande Plattformar visas genom `realized_by`.

### Plattform

Detaljsidan prioriterar teknisk grund, funktioner, teknik och produkter. Den ska tydligt skiljas från den konsumtionsorienterade Plattformstjänsten.

### Standard

Detaljsidan prioriterar standardtyp, referens, version och om den är obligatorisk. Relationen till styrda/begränsade objekt ska synliggöras.

### Lösningsmönster

Detaljsidan prioriterar problem, kontext, angreppssätt och konsekvenser. Den ska förbli generell och återanvändbar och inte fyllas med specifik lösningsdesign.

### Referensarkitektur

Detaljsidan prioriterar scope, applicability, building blocks och guidance. Den beskriver återanvändbar vägledning, inte en specifik implementationsarkitektur.

## Mallkontrakt

Mallarna under `templates/markdown/` använder enkla dubbla klamrar som **designmarkörer** i steg 15, exempelvis `{{name}}` och `{{catalog_rows}}`. De är ännu inte bundna till ett särskilt template-bibliotek. Steg 16 ska implementera renderingen deterministiskt och får vid behov ersätta markörerna med en intern representationsmodell så länge outputkontraktet består.

Gemensamma markörer:

- `{{name}}`
- `{{id}}`
- `{{status}}`
- `{{description}}`
- `{{metadata}}`
- `{{relations}}`
- `{{provenance}}`
- `{{catalog_rows}}`

Objekttypsspecifika markörer dokumenteras direkt i respektive mall.

## Filnamn och länkar

- Filnamn använder objektets stabila ID följt av en slug av namnet.
- Slug ska vara gemener, ASCII där praktiskt möjligt och bindestrecksseparerad.
- ID:t gör att en namnändring är spårbar även om filnamnet ändras.
- Interna länkar ska beräknas från outputstrukturen, inte lagras i YAML-modellen.

## Markdown-konventioner

- ATX-rubriker (`#`, `##`, `###`).
- Pipe-tabeller för kataloger.
- Vanliga punktlistor för funktioner och relationer.
- Inga HTML-tabeller i standardprofilen.
- Ingen presentationsspecifik färgsättning eller layoutmetadata i YAML.
- Svenska rubriker i svensk output; intern schema-/relationssemantik får fortsatt använda engelska nycklar.
- Escape av `|`, radbrytningar och andra Markdown-känsliga tecken ska ske i generatorn.

## Source of truth och ändringsregel

Om en användare vill ändra innehållet i en genererad Markdown-fil ska EA Stödjare:

1. identifiera motsvarande objekt/relationsdata i YAML,
2. föreslå eller genomföra ändringen där,
3. regenerera Markdown,
4. inte handredigera den genererade filen som primär metod.

Manuellt redaktionellt innehåll som inte hör hemma i EA-modellen ska i framtiden kunna hanteras som separat dokumentationskälla, men ett sådant system introduceras inte i v1 steg 15.

## Profiler som medvetet inte införs nu

- diagramprofiler,
- ArchiMate-vyer,
- presentationsslides,
- dashboards/heatmaps,
- lösningsarkitekturprofiler,
- organisations- och processvyer.

Dessa kan senare byggas ovanpå samma modell och relationsregister.


# KÄLLA: `docs/markdown-generation.md`

# Deterministisk Markdown-generering

## Syfte

`scripts/generate_markdown.py` genererar katalog- och detaljvyer från den kanoniska YAML-modellen enligt `docs/documentation-profiles.md` och mallarna under `templates/markdown/`.

Generatorn ändrar aldrig YAML-modellen. `docs/generated/` är alltid ett derivat och kan regenereras från modellen.

## Användning

Från projektroten:

```bash
python scripts/generate_markdown.py --project-root . --mode working
```

För publiceringsvy:

```bash
python scripts/generate_markdown.py --project-root . --mode published
```

Alternativ outputkatalog kan anges med `--output-dir`.

## Lägen

- `working`: inkluderar `candidate`, `approved` och `deprecated` och visar mer proveniensinformation.
- `published`: inkluderar endast `approved` och reducerar arbetsintern proveniens.
- `retired` utelämnas i båda standardlägena.

## Determinism

Generatorn använder:

- stabil objektsortering,
- stabila ID-baserade filnamn,
- deterministiska sluggar,
- relationer endast från `model/relations.yaml`,
- källinformation endast från `model/sources.yaml`,
- stabil gruppering av relationer och listor.

Samma modell, mallar, projektrevision och presentationsläge ska därför ge byte-identisk Markdown.

## Interna länkar

Detaljsidor länkas med relativa länkar. Om ett relaterat objekt inte ingår i aktuell export visas namn/ID utan länk. YAML-modellen innehåller inga presentationslänkar.

## Test

`tests/generation/test_generate_markdown.py` kör generatorn två gånger och jämför hash av hela Markdown-trädet. Testet verifierar också att `published` filtrerar bort kandidater.

Exempel:

```bash
python tests/generation/test_generate_markdown.py
```

## Exempeloutput

`examples/minimal-model/docs/generated/` innehåller genererad `working`-output från den syntetiska minimalmodellen och fungerar som konkret referens för formatet.


# KÄLLA: `docs/confluence-generation.md`

# Confluence markup-generering

## Syfte

EA Stödjare kan från steg 17 generera **Confluence wiki markup** från samma kanoniska YAML-modell som används för Markdown-exporten. Confluence-exporten är ett presentationsderivat och får inte redigeras som en parallell source of truth.

## Källa

Generatorn läser endast projektets kanoniska modell och styrmetadata:

- `model/*.yaml`
- `model/relations.yaml`
- `model/sources.yaml`
- `project-manifest.json` för projektrevision

Den läser inte genererad Markdown som informationskälla. Markdown och Confluence är därmed två deterministiska vyer av samma EA-modell.

## Kommando

Från projektroten:

```bash
python3 scripts/generate_confluence.py --project-root . --mode working
```

Standardkatalog är:

```text
exports/confluence/
```

Publiceringsläge:

```bash
python3 scripts/generate_confluence.py --project-root . --mode published
```

Precis som Markdown-generatorn innebär:

- `working`: `candidate`, `approved` och `deprecated` får visas,
- `published`: endast `approved` visas.

## Outputstruktur

```text
exports/confluence/
  drivkrafter.txt
  mal.txt
  principer.txt
  formagor.txt
  it-stod.txt
  plattformstjanster.txt
  plattformar.txt
  standarder.txt
  losningsmonster.txt
  referensarkitekturer.txt
  objects/
    drivers/
    goals/
    principles/
    capabilities/
    it-support/
    platform-services/
    platforms/
    standards/
    solution-patterns/
    reference-architectures/
```

Varje `.txt`-fil innehåller Confluence wiki markup som kan kopieras till en Confluence-sida eller användas som underlag för senare publiceringsautomation.

## Renderingsregler

- Rubriker använder `h1.`, `h2.` och `h3.`.
- Katalogtabeller använder Confluence-formatet `|| header ||` och `| cell |`.
- Listor använder `*`.
- Genereringsmetadata visas i en `{info}`-panel.
- Objektreferenser använder Confluence-sidlänkar med sidtiteln `ID – Namn`.
- Relationer renderas i båda läsriktningarna men lagras fortsatt endast en gång i `relations.yaml`.
- Funktioner hämtas från respektive objekts `functions[]`.
- Proveniens och källreferenser hämtas från den kanoniska modellen.
- `working` visar mer evidensmetadata än `published`.

## Semantisk konsistens med Markdown

Markdown och Confluence använder samma:

- statusfiltrering,
- objektsortering,
- objekttyper,
- relationer,
- funktioner,
- proveniens,
- projektmetadata.

De kan skilja sig i presentation och länksyntax men får inte skilja sig i EA-innehåll. Regressionstestet `tests/generation/test_generate_confluence.py` verifierar bland annat att båda formaten genererar samma uppsättning objektsidor och att publiceringsläget filtrerar kandidater på samma sätt.

## Determinism

Generatorn rensar tidigare `.txt`-output i målkatalogen före renderingen och skriver filer i deterministisk ordning. Två körningar mot oförändrad modell och samma projektrevision ska ge identiskt hashat outputträd.


# KÄLLA: `docs/document-export.md`

# DOCX- och PDF-export

## Syfte

`scripts/export_documents.py` skapar distributionsformat från den kanoniska EA-modellen utan att införa en parallell sanningskälla.

Exportkedjan är:

```text
YAML-modell
  -> deterministisk Markdown-generering
  -> sammansatt distributionsdokument
  -> Pandoc DOCX
  -> LibreOffice PDF
```

DOCX och PDF är alltså alltid derivat. Ändringar ska göras i `model/*.yaml` och därefter regenereras.

## Förutsättningar

- Python 3
- Pandoc
- LibreOffice (`libreoffice` eller `soffice`)

## Användning

Från projektroten:

```bash
python scripts/export_documents.py --project-root . --mode published
```

Arbetsmaterial inklusive kandidater:

```bash
python scripts/export_documents.py --project-root . --mode working
```

Annan outputkatalog och filbas:

```bash
python scripts/export_documents.py \
  --project-root . \
  --mode published \
  --output-dir exports/document \
  --basename arkitekturdokumentation
```

## Innehåll och struktur

Exporten innehåller:

- dokumenttitel från projektmanifestet,
- presentationsläge och projektrevision,
- innehållsförteckning,
- katalogavsnitt för samtliga objekttyper som ingår i aktuellt läge,
- detaljsektioner för objekten,
- relationer, funktioner och proveniens enligt Markdown-profilerna.

Katalogerna följer den ordning som definierats för EA Stödjare v1: drivkrafter, mål, principer, förmågor, IT-stöd, plattformstjänster, plattformar, standarder, lösningsmönster och referensarkitekturer.

## Layoutprinciper

Version 1 använder avsiktligt en enkel och robust dokumentlayout:

- Pandocs DOCX-standardformat,
- rubrikhierarki som ger navigerbar innehållsförteckning,
- Pandocs tabellrendering för katalogtabeller,
- varje övergripande katalogavsnitt börjar på ny sida i DOCX/PDF,
- tomma kataloger utelämnas i `published` men behålls i `working`,
- DOCX som grund även för PDF-export så att formaten hålls nära varandra,
- inga presentationsspecifika data lagras i YAML-modellen.

Mer avancerad grafisk profil kan senare införas genom ett versionshanterat Pandoc-reference-DOCX utan att ändra informationsmodellen.

## Determinism

Samma:

- YAML-modell,
- projektrevision,
- Markdown-generator,
- presentationsläge,
- Pandoc/LibreOffice-versioner

ska ge semantiskt samma dokument. Binär DOCX/PDF kan innehålla verktygsspecifik metadata och betraktas därför inte som byte-deterministisk på samma sätt som Markdown/Confluence-exporten.

## Verifiering

`tests/generation/test_export_documents.py` verifierar att:

- DOCX och PDF skapas,
- båda filerna är icke-tomma,
- DOCX innehåller projektets titel och förväntade EA-sektioner,
- PDF kan parsas och innehåller förväntad text,
- `published` inte tar med objekt med status `candidate`.

Visuell QA av referensexporten görs dessutom genom rendering av både DOCX och PDF till sidbilder.


# KÄLLA: `docs/structural-validation.md`

# Strukturell validering

## Syfte

Steg 24 inför deterministisk strukturell validering av ett EA Stödjare-projekt. Valideringen ska hitta tekniska och referentiella fel innan semantisk LLM-granskning görs.

Huvudverktyget är:

```bash
python scripts/validate_project.py --project-root .
```

Ett annat EA-projekt kan valideras mot denna repos schemas och generatorer:

```bash
python scripts/validate_project.py \
  --project-root /sokvag/till/projekt \
  --repo-root /sokvag/till/ea-stodjare
```

Exit code `0` betyder att inga blockerande strukturella fel hittades. Exit code `1` betyder att minst ett fel hittades.

## Kontroller

Validatorn kontrollerar följande lager.

### Manifest och filintegritet

- `project-manifest.json` finns och är giltig JSON.
- manifestet följer `schemas/project-manifest.schema.json`.
- filinventeringen är unik och deterministiskt sorterad.
- obligatoriska registrerade filer finns.
- SHA-256 stämmer för registrerade filer.
- den kanoniska modellkatalog som manifestet pekar på finns.

### Kanonisk YAML-modell

- samtliga obligatoriska modellfiler finns,
- YAML kan parsas,
- filernas envelope följer modellformat v1,
- `schema_version` och `object_type` är korrekta,
- obligatoriska objektfält finns,
- objekttyp matchar filen,
- ID-prefix matchar objekttypen,
- objekt-ID:n är globala och unika,
- statusvärden är tillåtna,
- `capability_type` är `business` eller `it`,
- `functions[]` används endast där metamodel v1 tillåter det och har inget globalt ID.

### Källor och proveniens

- käll-ID följer formatet och är unika,
- `source_type` är definierad,
- refererade källor finns,
- `derived_from` refererar befintliga objekt,
- evidenstyper följer de obligatoriska reglerna för source/rationale,
- confidence och transferability har tillåtna värden,
- external-evidens använder en extern källtyp.

### Relationer

- relations-ID följer formatet och är unika,
- source och target finns,
- relationstypen är definierad,
- source/target-kombinationen är tillåten enligt `schemas/relations.yaml`,
- target constraints, exempelvis IT-förmåga för plattformstjänstens `supports`, följs,
- förbjudna självrelationer upptäcks,
- exakta dubblettrelationer upptäcks,
- relationens proveniens valideras.

### Genererade artefakter

När lagrade genererade artefakter finns kontrolleras de som derivat:

- Markdown regenereras i `working` och jämförs byte-för-byte med `docs/generated/`.
- Confluence markup regenereras i `working` och jämförs byte-för-byte med `exports/confluence/`.
- lagrade PDF-filer kontrolleras för PDF-signatur.
- lagrade DOCX-filer kontrolleras för OOXML/ZIP-signatur.

DOCX/PDF:s fullständiga reproducerbarhet och innehållskvalitet fortsätter att testas av de dedikerade exporttesterna eftersom binär metadata kan göra direkt byte-jämförelse olämplig.

## Fel och varningar

Validatorn använder stabila kodprefix:

- `STR-MAN-*` – manifest/integritet,
- `STR-MODEL-*` – modellformat,
- `STR-ID-*` – identitet,
- `STR-SRC-*` – källregister,
- `STR-PROV-*` – proveniens,
- `STR-REL-*` – relationer,
- `STR-GEN-*` – genererade artefakter.

Fel blockerar godkänd strukturell validering. Varningar rapporteras men ger exit code `0`.

Maskinläsbart resultat fås med:

```bash
python scripts/validate_project.py --project-root . --json
```

## Avgränsning

Steg 24 validerar sådant som kan avgöras deterministiskt. Den försöker inte ersätta:

- objektspecifik semantisk kvalitet i `knowledge/quality-object.md`,
- modellens helhetskvalitet i `knowledge/quality-model.md`,
- bedömning av om en förmåga är välformulerad,
- relevans/överförbarhet i research utöver formella proveniensregler,
- om en arkitekturmodell är ändamålsenlig för organisationen.

Dessa delar hör hemma i kvalitetsarbetsflödena och senare semantiska evals.

## Regressionstest

Kör:

```bash
python tests/validation/test_validate_project.py
```

Testsviten verifierar både giltiga projekt och avsiktligt trasiga varianter, bland annat dubblett-ID, saknad relationsreferens, otillåten relation, hash-avvikelse och stale Markdown.
