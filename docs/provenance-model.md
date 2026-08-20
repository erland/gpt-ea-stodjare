# EA Stödjare – proveniens- och evidensmodell v1

## 1. Syfte och status

Detta dokument definierar **EA Stödjares proveniens- och evidensmodell v1** efter utvecklingsplanens steg 5. Modellen ska göra det möjligt att förstå **varför ett EA-objekt eller en relation finns**, vilket underlag det bygger på och hur stark slutsatsen är.

Proveniensmodellen gäller både objekt och relationer. Den ska förhindra att EA Stödjare blandar ihop:

- vad användarens underlag uttryckligen säger,
- vad som har härletts från underlaget,
- vad externa källor tillför,
- vad GPT:n själv rekommenderar.

Den slutliga serialiseringen i projektets kanoniska YAML-modell fastställs i steg 6.

## 2. Grundprinciper

1. **Varje materiellt objekt och varje materiell relation ska kunna motiveras.**
2. **Evidenstyp är inte samma sak som livscykelstatus.** Ett objekt kan vara `approved` men fortfarande bygga på `derived` evidens.
3. **Confidence är inte samma sak som evidenstyp.** Ett `external` påstående kan ha hög eller låg confidence beroende på källa och överförbarhet.
4. **GPT-förslag ska aldrig presenteras som uttryckliga fakta i användarens underlag.**
5. **Extern research ska kunna särskiljas från organisationens interna beslut och beskrivningar.**
6. **Härledningar ska om möjligt peka tillbaka på de objekt eller källor de bygger på.**
7. **Flera evidensposter får stödja samma objekt eller relation.**
8. **Motstridiga källor ska inte döljas genom att endast en källa sparas.** Konflikthantering fördjupas i steg 20.

## 3. Evidenstyper

### 3.1 `explicit`

Informationen framgår uttryckligen av användarens underlag eller en intern källa som används som organisationsspecifik source of truth.

Exempel:

> Strategin anger uttryckligen att organisationen ska minska ledtiden från behov till produktionssatt IT-stöd.

Lämplig användning:

```yaml
provenance:
  - evidence_type: explicit
    source_id: SRC-001
    reference: "Avsnitt 3.2"
```

`explicit` betyder inte automatiskt att uppgiften är korrekt eller fortfarande aktuell. Det betyder att den uttryckligen förekommer i den angivna källan.

### 3.2 `derived`

Informationen är en strukturerad slutsats som rimligen kan härledas från ett eller flera underlag eller redan etablerade objekt, men uttrycks inte i exakt denna form i källan.

Exempel:

- flera strategiska mål antyder behov av en IT-förmåga för automatiserad leverans,
- en arkitekturprincip formuleras utifrån ett uttalat mål och en drivkraft,
- en relation mellan två objekt härleds från beskrivningen av hur de används.

En härledning ska när det är möjligt ange `derived_from`.

```yaml
provenance:
  - evidence_type: derived
    derived_from:
      - GOAL-003
      - DRV-002
    rationale: >-
      Målet om kortare ledtid och drivkraften om högre förändringstakt
      motiverar behov av denna IT-förmåga.
```

### 3.3 `proposed`

Informationen är ett aktivt förslag eller en rekommendation från EA Stödjare. Den ska inte behandlas som beslutad eller som belagd i underlaget.

Exempel:

- föreslagen ny förmåga för att täcka en identifierad lucka,
- rekommenderad princip,
- rekommenderad klassificering när underlaget är otydligt,
- föreslagen relation mellan två objekt.

```yaml
provenance:
  - evidence_type: proposed
    rationale: >-
      Förmågan föreslås för att täcka den identifierade luckan mellan
      utvecklingsbehov och befintliga plattformstjänster.
```

Ett `proposed` objekt bör normalt börja med livscykelstatus `candidate` tills användaren eller organisationen accepterat det.

### 3.4 `external`

Informationen baseras på en extern källa eller omvärldsresearch och används för att komplettera, jämföra eller utmana den organisationsspecifika modellen.

Exempel på externa källor:

- normativ standard,
- etablerat ramverk,
- myndighets- eller branschrekommendation,
- dokumenterad modell hos jämförbar organisation,
- produkt- eller leverantörsdokumentation,
- annan relevant publicerad källa.

```yaml
provenance:
  - evidence_type: external
    source_id: SRC-EXT-004
    reference: "Capability model, section 2"
    transferability: medium
    rationale: >-
      Modellen är relevant som jämförelse men organisationens uppdrag och
      ansvar skiljer sig delvis från källorganisationens.
```

Extern evidens ska aldrig automatiskt göras om till intern sanning. Om extern information används för att skapa ett organisationsspecifikt förslag bör det nya objektet normalt vara `proposed`, med den externa källan som stödjande evidens.

## 4. Källmodell

Källor ska kunna registreras en gång och refereras från flera objekt och relationer.

Minsta källinformation:

| Fält | Krav | Betydelse |
|---|---|---|
| `id` | obligatoriskt | Stabil källidentitet |
| `title` | obligatoriskt | Dokumentets/källans titel |
| `source_type` | obligatoriskt | Typ av källa |
| `organization` | valfritt | Utgivare/ansvarig organisation |
| `url` | valfritt | URL för extern eller digital källa |
| `publication_date` | valfritt | Publiceringsdatum när känt |
| `accessed_at` | valfritt | När extern källa hämtades |
| `version` | valfritt | Versionsbeteckning |
| `notes` | valfritt | Källspecifika kommentarer |

Föreslagna `source_type` i v1:

- `internal_document`
- `internal_model`
- `internal_decision`
- `law_or_regulation`
- `standard`
- `framework`
- `authority_guidance`
- `industry_guidance`
- `peer_organization`
- `vendor_documentation`
- `research_or_report`
- `web_source`
- `user_statement`
- `other`

## 5. Provenienspost

Varje provenienspost ska kunna innehålla:

| Fält | Krav | Betydelse |
|---|---|---|
| `evidence_type` | obligatoriskt | `explicit`, `derived`, `proposed` eller `external` |
| `source_id` | beroende på typ | Referens till registrerad källa |
| `reference` | valfritt | Sida, avsnitt, rubrik eller annan locator |
| `quote` | valfritt | Kort stödjande citat när lämpligt och tillåtet |
| `derived_from` | beroende på typ | Objekt-/relations-ID:n som härledningen bygger på |
| `rationale` | ofta obligatoriskt | Motivering för härledning/förslag/överförbarhet |
| `confidence` | valfritt | `high`, `medium`, `low` |
| `transferability` | extern evidens | Hur väl extern praxis bedöms kunna överföras |
| `recorded_at` | valfritt | När evidensen registrerades |
| `notes` | valfritt | Kompletterande kommentar |

## 6. Regler per evidenstyp

### Explicit

Ska normalt ha:

- `source_id`,
- `reference` när källan är större än ett enkelt användaruttalande.

`rationale` behövs normalt inte när kopplingen är självklar.

### Derived

Ska ha minst ett av:

- `source_id`,
- `derived_from`.

Ska normalt ha `rationale`.

### Proposed

Ska normalt ha:

- `rationale`,
- `confidence` när osäkerheten är relevant.

Kan dessutom ha stödjande `source_id` och/eller `derived_from`.

### External

Ska ha:

- `source_id`,
- `reference` när relevant,
- `transferability` när informationen används som jämförelse eller modellunderlag för organisationen.

## 7. Confidence

`confidence` uttrycker hur säker EA Stödjare bedömer den aktuella tolkningen, härledningen eller rekommendationen.

Tillåtna värden i v1:

- `high` – starkt och entydigt stöd,
- `medium` – rimligt stöd men alternativa tolkningar finns,
- `low` – svagt eller ofullständigt stöd; bör valideras innan användning.

Confidence ska inte användas som en falsk matematisk sannolikhet.

### Grundregler

- `explicit` behöver inte automatiskt `high`; källan kan vara motsägelsefull eller gammal.
- `derived` bör normalt få confidence när härledningen är viktig för beslut.
- `proposed` bör få confidence när flera rimliga alternativ finns.
- `external` ska bedömas både utifrån källans kvalitet och överförbarhet.

## 8. Överförbarhet för externa källor

När en extern modell eller praxis används för att föreslå hur användarens organisation bör modelleras ska `transferability` kunna anges:

- `high` – kontext, uppdrag och användningsfall är nära jämförbara,
- `medium` – relevant inspiration men vissa viktiga skillnader finns,
- `low` – endast ett begränsat jämförelseexempel.

Bedömningen bör motiveras när den påverkar rekommendationen.

## 9. Proveniens på relationer

Relationer är lika viktiga att evidenssätta som objekten själva.

Exempel:

```yaml
- id: REL-014
  source: ITS-004
  relation: uses
  target: PLS-002
  provenance:
    - evidence_type: explicit
      source_id: SRC-008
      reference: "Systembeskrivning, avsnitt Integrationer"
```

En relation som GPT:n endast tror är rimlig ska i stället markeras som exempelvis:

```yaml
provenance:
  - evidence_type: proposed
    confidence: medium
    rationale: >-
      IT-stödets beskrivna funktion kräver sannolikt den aktuella
      plattformstjänsten, men underlaget anger inte beroendet explicit.
```

## 10. Kombination av evidens

Samma objekt eller relation kan ha flera proveniensposter.

Exempel:

```yaml
provenance:
  - evidence_type: explicit
    source_id: SRC-001
    reference: "Avsnitt 4"
  - evidence_type: external
    source_id: SRC-EXT-002
    reference: "Section 3"
    transferability: medium
```

Det gör det möjligt att uttrycka att ett internt behov både är belagt internt och stöds av extern praxis.

## 11. Rekommenderat mönster för organisationsspecifika modellförslag

När EA Stödjare använder research för att föreslå en ny modell bör arbetskedjan vara:

```text
Internt underlag
     +
Extern research
     +
EA-kunskap
     ↓
Analys / härledning
     ↓
Proposed objekt/relationer
```

Det föreslagna objektet ska alltså inte märkas enbart `external` bara för att externa källor inspirerat det. Själva organisationsspecifika slutsatsen är ett `proposed` objekt, medan de externa källorna sparas som stödjande evidens.

## 12. Presentationsregler för GPT:n

När EA Stödjare presenterar analys utanför själva YAML-modellen ska den använda ett språk som speglar evidensen.

### Explicit

Lämpligt:

> Underlaget anger att ...

Undvik:

> Jag bedömer att ...

när det faktiskt är explicit belagt.

### Derived

Lämpligt:

> Detta kan härledas till ...

> Sammantaget talar underlaget för ...

### Proposed

Lämpligt:

> Jag rekommenderar att ...

> Ett rimligt modellförslag är ...

### External

Lämpligt:

> Externa källor visar att ...

> Som jämförelse använder ...

När extern praxis används normativt ska GPT:n förklara varför den är relevant för den aktuella organisationen.

## 13. Valideringsregler v1

Minst följande regler ska senare kunna valideras maskinellt:

- varje provenienspost har en definierad `evidence_type`,
- `source_id` refererar till en existerande källa,
- `derived_from` refererar till existerande objekt/relationer,
- `derived` har motivering när kopplingen inte är självklar,
- `proposed` har motivering,
- `external` har extern källa,
- `transferability` används endast där det är relevant,
- confidence använder tillåtna värden,
- ett materialt objekt eller en material relation saknar inte proveniens,
- externa källor görs inte om till implicit interna beslut.

## 14. Exempel – från strategi till föreslagen princip

### Källa

```yaml
- id: SRC-001
  title: IT-strategi 2026
  source_type: internal_document
  organization: Exempelmyndigheten
```

### Mål

```yaml
- id: GOAL-004
  type: goal
  name: Minska strategiskt leverantörsberoende
  status: approved
  provenance:
    - evidence_type: explicit
      source_id: SRC-001
      reference: "Avsnitt 4.2"
```

### Principförslag

```yaml
- id: PRN-007
  type: principle
  name: Utbytbara lösningskomponenter
  status: candidate
  provenance:
    - evidence_type: proposed
      derived_from:
        - GOAL-004
      confidence: high
      rationale: >-
        Principen operationaliserar det uttryckliga målet genom att styra
        arkitekturbeslut mot lösare koppling och utbytbarhet.
```

Detta bevarar skillnaden mellan organisationens beslutade mål och GPT:ns rekommenderade princip.

## 15. Avgränsningar i v1

Proveniensmodellen är inte avsedd att vara:

- ett fullständigt records-management-system,
- ett juridiskt bevisregister,
- ett formellt beslutsdiarium,
- en vetenskaplig referensdatabas,
- en sannolikhetsmodell.

Syftet är praktisk och transparent EA-spårbarhet.

## 16. Beslut efter steg 5

Följande är nu fastställt inför steg 6:

- fyra evidenstyper används: `explicit`, `derived`, `proposed`, `external`,
- objekt och relationer kan ha flera proveniensposter,
- källor registreras separat och refereras med stabila ID:n,
- härledningar kan peka på andra EA-objekt eller relationer,
- `confidence` används som kvalitativ bedömning,
- extern research ska bedömas för överförbarhet,
- organisationsspecifika slutsatser baserade på extern research är normalt `proposed`, inte `external`,
- GPT:n ska språkligt skilja fakta, härledning, extern information och rekommendationer.
