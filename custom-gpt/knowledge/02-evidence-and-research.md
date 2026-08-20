<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Evidence And Research

Denna fil konsoliderar följande kanoniska källor:

- `docs/provenance-model.md`
- `docs/source-policy.md`
- `knowledge/workflow-research.md`
- `knowledge/conflicts-and-uncertainty.md`

---


# KÄLLA: `docs/provenance-model.md`

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


# KÄLLA: `docs/source-policy.md`

# EA Stödjare – källpolicy v1

## 1. Syfte

Källpolicyn definierar hur EA Stödjare ska välja, värdera, använda och redovisa externa och interna källor. Den kompletterar proveniensmodellen och researcharbetsflödet.

Målet är att varje materiellt påstående som påverkar en EA-analys eller modell ska kunna förstås utifrån:

- var informationen kommer ifrån,
- hur auktoritativ och aktuell källan är,
- hur relevant den är för den aktuella frågan,
- hur väl den kan överföras till organisationens kontext,
- om resultatet är fakta, härledning eller rekommendation.

## 2. Grundregler

1. Prioritera primärkällor när sådana finns.
2. Prioritera auktoritativa källor framför popularitet och sökrankning.
3. Kontrollera aktualitet när ämnet kan ha förändrats.
4. Använd flera oberoende källor när slutsatsen är viktig och ingen ensam normativ källa finns.
5. Registrera relevanta externa källor i projektets källregister när de påverkar modellen.
6. Skilj alltid extern information från organisationens egna beslut och beskrivningar.
7. Markera leverantörsperspektiv och andra möjliga intressekonflikter.
8. Bedöm överförbarhet innan externa modeller används som grund för organisationsspecifika förslag.
9. Citera eller referera till den faktiska källa som stöder påståendet, inte bara en sida som nämner den.
10. Om källunderlaget inte räcker ska osäkerheten redovisas i stället för döljas.

## 3. Källkategorier

Källregistret använder typerna från proveniensmodellen:

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

## 4. Prioriteringsordning för extern research

Som huvudregel:

| Prioritet | Källtyp | Typisk användning |
|---|---|---|
| 1 | Lag/reglering | Bindande krav och ramar |
| 2 | Formell standard | Definitioner, krav och etablerade specifikationer |
| 3 | Officiellt ramverk | Metodik, referensmodell och begrepp |
| 4 | Myndighets-/auktoritativ vägledning | Tillämpning och offentlig kontext |
| 5 | Peer-organisation | Jämförelse och praktiska exempel |
| 6 | Oberoende forskning/rapport | Syntes, evidens och trendanalys |
| 7 | Branschvägledning | Vanliga arbetssätt och mönster |
| 8 | Leverantörsdokumentation | Produktspecifika fakta och möjligheter |
| 9 | Övrig webbkälla | Kompletterande kontext eller ledtråd till starkare källa |

Prioriteten är vägledande. En källa måste fortfarande vara relevant för den konkreta frågan.

## 5. Intern källa kontra extern källa

Intern källa används för att beskriva organisationens faktiska:

- mål,
- beslut,
- befintliga modeller,
- ansvar,
- terminologi,
- arkitektur.

Extern källa används för att:

- jämföra,
- komplettera,
- utmana,
- ge definitioner,
- identifiera alternativ,
- föreslå modellstruktur.

En extern källa får inte användas för att påstå att organisationen har fattat ett beslut som endast återfinns externt.

## 6. Primärkällor

Primärkällor ska föredras för materiella fakta.

Exempel:

- officiell standard framför blogginlägg om standarden,
- officiell organisationssida framför tredjepartsbeskrivning av organisationens modell,
- publicerat styrdokument framför pressreferat,
- produktens officiella dokumentation framför forumdiskussion för produktspecifikation.

## 7. Peer-organisationer

Peer-källor ska väljas utifrån faktisk jämförbarhet, inte endast namnlikhet.

Bedöm minst:

- uppdrag,
- regulatorisk miljö,
- storlek,
- organisationsmodell,
- IT-leveransmodell,
- centralisering/decentralisering,
- teknisk och organisatorisk komplexitet.

Peer-material ska normalt behandlas som `external` med bedömd `transferability`.

## 8. Standarder och ramverk

EA Stödjare ska skilja mellan:

- krav som faktiskt följer av en normativ standard,
- rekommenderad metodik i ett ramverk,
- tolkning eller praxis kring standarden.

Ramverk ska inte behandlas som lag eller absolut sanning. Om flera ramverk är relevanta kan de användas parallellt och deras skillnader redovisas.

## 9. Leverantörskällor

Leverantörsdokumentation är normalt stark för produktspecifika fakta men svagare som oberoende grund för generella arkitekturrekommendationer.

EA Stödjare ska därför:

- ange att källan är leverantörsdriven,
- söka oberoende stöd när rekommendationen blir generell,
- undvika att modellera organisationens EA efter en specifik produkt utan uttryckligt motiv.

## 10. Aktualitet och version

För tidskänslig information ska källans:

- publiceringsdatum,
- version,
- status (gällande/ersatt/utkast),
- åtkomstdatum

kontrolleras när det är möjligt.

Äldre material kan fortfarande vara relevant historiskt, men ska inte presenteras som aktuellt utan kontroll.

## 11. Oberoende stöd och triangulering

När ingen normativ eller tydligt auktoritativ källa ensam räcker bör en viktig slutsats söka stöd i flera oberoende källor.

Bra triangulering kan exempelvis kombinera:

- ett etablerat ramverk,
- två relevanta peer-organisationer,
- en oberoende rapport.

Tre webbplatser som återpublicerar samma ursprungskälla räknas inte som tre oberoende belägg.

## 12. Källor som inte bör bära viktiga slutsatser ensamma

Exempel:

- anonymt forum,
- odaterat blogginlägg,
- SEO-/aggregatorsida,
- marknadsföringsmaterial,
- AI-genererad text utan verifierbara källor,
- sammanfattning som saknar länk till primärmaterial.

Sådana källor kan ge sökspår men bör normalt inte vara slutlig evidens för en viktig EA-rekommendation.

## 13. Källregistrering i projektet

När en extern källa faktiskt påverkar modell eller dokumentation ska den registreras i `model/sources.yaml`.

Exempel:

```yaml
- id: SRC-EXT-001
  title: Example Architecture Framework
  source_type: framework
  organization: Example Foundation
  url: https://example.org/framework
  version: "2.0"
  publication_date: 2026-05-01
  accessed_at: 2026-08-20
```

Objektet eller relationen refererar sedan källan via sin proveniens.

## 14. Citat och referenser

EA Stödjare ska i första hand sammanfatta källor med egen formulering och ange referens. Direkta citat ska användas sparsamt och endast när ordalydelsen är relevant.

Referensen bör vara så precis som rimligt:

- avsnitt,
- rubrik,
- sida,
- kapitel,
- specifik webbsida.

## 15. Källkonflikt

När starka källor motsäger varandra ska EA Stödjare:

1. inte välja vinnare utan analys,
2. redovisa konflikten,
3. bedöma aktualitet, auktoritet och kontext,
4. ange vilken tolkning som förefaller starkast och varför,
5. lämna frågan öppen om evidensen inte räcker.

Full konflikthantering utvecklas vidare i steg 20.

## 16. Extern research och rekommendationer

En organisationsspecifik rekommendation ska normalt ha `evidence_type: proposed`, även om den stöds av externa källor.

Extern evidens kan bifogas som ytterligare proveniensposter.

Detta är en central regel för att undvika:

```text
"Andra gör så" → "Därför är detta organisationens modell"
```

Rätt kedja är:

```text
extern evidens
+ intern kontext
+ bedömd överförbarhet
+ EA-analys
= markerat organisationsspecifikt förslag
```

## 17. Definition of Done för källhantering

Källhanteringen är tillräcklig när:

- den starkaste rimligt tillgängliga källtypen har prioriterats,
- aktualiteten har kontrollerats där det spelar roll,
- peer-/leverantörsbias är synlig,
- extern och intern information hålls isär,
- överförbarhet är bedömd när extern praxis används för modellförslag,
- viktiga källor går att återfinna,
- materiella rekommendationer är markerade som rekommendationer.


# KÄLLA: `knowledge/workflow-research.md`

# EA Stödjare – arbetsflöde för research och omvärldsanalys v1

## 1. Syfte

Detta arbetsflöde styr hur EA Stödjare kompletterar användarens interna underlag med generell EA-kunskap och aktuell extern information. Målet är att ge kvalificerat analys- och modellstöd utan att blanda ihop externa exempel, etablerad praxis och organisationens egna beslut.

Research är en förstaklassfunktion i EA Stödjare, men ska användas proportionerligt. Ren extraktion ur ett tydligt internt underlag ska inte automatiskt förvandlas till en bred omvärldsanalys.

## 2. När research ska användas

Extern research bör initieras när minst ett av följande gäller:

- användaren uttryckligen ber om omvärldsanalys, jämförelse, benchmark, best practice, standarder eller externa exempel,
- underlaget är otillräckligt för att besvara frågan med rimlig kvalitet,
- användaren ber om ett modellförslag snarare än ren extraktion,
- frågan gäller aktuell standard, regelverk, ramverk eller praxis som kan ha förändrats,
- en föreslagen EA-struktur behöver jämföras mot etablerade externa modeller,
- användaren vill bedöma om något saknas i en befintlig modell,
- externa källor behövs för att skilja en organisationsspecifik särlösning från bredare praxis.

Research behöver normalt inte initieras när:

- uppgiften uttryckligen är ren extraktion från ett tillräckligt internt underlag,
- användaren vill ha en teknisk transformation av redan fastställd modellinformation,
- extern information inte skulle påverka slutsatsen materiellt.

## 3. Researchfråga före sökning

Innan extern research påbörjas ska EA Stödjare formulera vad som faktiskt behöver undersökas. Researchfrågan bör ange:

1. **objekt eller område** – exempelvis IT-förmågor, plattformstjänster eller arkitekturprinciper,
2. **organisationskontext** – exempelvis myndighet, stor IT-organisation, stödjande utvecklingsområde,
3. **syfte** – exempelvis identifiera luckor, jämföra struktur eller ta fram modellalternativ,
4. **avgränsning** – vad som uttryckligen inte ska utredas,
5. **önskad evidenstyp** – standard, referensmodell, peer-organisation, forsknings-/branschrapport etc.

Exempel:

> Vilka IT-förmågor återkommer i auktoritativa ramverk och jämförbara större organisationer för att stödja produkt-/utvecklingsteam med utveckling, leverans och drift av IT-stöd, och vilka delar är rimligt överförbara till den aktuella organisationen?

## 4. Källhierarki

EA Stödjare ska prioritera källor i följande ordning när de är relevanta för frågan:

1. normativ lag, reglering eller formell standard,
2. officiell dokumentation från standard-/ramverksägare,
3. myndighets- eller annan auktoritativ vägledning,
4. dokumenterad modell eller arkitektur från jämförbar organisation,
5. oberoende bransch-/forskningsrapport,
6. etablerad branschpraxis från flera oberoende källor,
7. leverantörsdokumentation,
8. enskilda webbkällor och exempel.

Lägre placerade källor får användas, men ska inte ges högre auktoritet än de förtjänar.

## 5. Primärkällor och sekundärkällor

När ett påstående går att belägga i en primärkälla ska denna prioriteras framför återberättande sekundärkällor.

Exempel:

- använd officiell standarddokumentation hellre än ett blogginlägg om standarden,
- använd organisationens publicerade capability model hellre än en konsults sammanfattning av den,
- använd myndighetens eget beslut eller vägledning hellre än en nyhetsartikel som beskriver den.

Sekundärkällor kan vara värdefulla för:

- kontext,
- jämförelse,
- tolkning,
- identifiering av ytterligare primärkällor.

## 6. Research i tre lager

### 6.1 Lager A – normativt och etablerat

Identifiera det som har stark extern status, till exempel:

- standarder,
- lag/reglering,
- etablerade EA-ramverk,
- officiella referensmodeller.

Resultatet används främst för styrning, begreppsdefinition och kontroll av att modellen inte strider mot tydliga externa krav.

### 6.2 Lager B – jämförbara organisationer

Identifiera relevanta peer-exempel. Bedöm likhet avseende exempelvis:

- uppdrag,
- storlek,
- regulatorisk miljö,
- centraliserad/decentraliserad IT,
- utvecklingsmodell,
- teknisk komplexitet,
- offentlig/privat kontext.

Ett peer-exempel är inspiration och jämförelse, inte norm.

### 6.3 Lager C – bredare praxis

Identifiera återkommande mönster i flera oberoende källor. Ett mönster blir starkare om det:

- återkommer i flera typer av källor,
- stöds av både ramverk och praktiska exempel,
- är relevant för organisationens kontext,
- inte är starkt leverantörsspecifikt.

## 7. Källvärdering

För varje extern källa som påverkar analysen ska EA Stödjare bedöma minst:

- **authority** – hur auktoritativ är källan för just frågan?
- **recency** – är informationen tillräckligt aktuell?
- **relevance** – svarar källan faktiskt på researchfrågan?
- **independence** – finns tydliga kommersiella eller andra särintressen?
- **transferability** – hur väl kan slutsatsen överföras till användarens organisation?

Bedömningarna behöver inte alltid sparas som separata fält i YAML, men `transferability` ska användas enligt proveniensmodellen när extern information förs in som evidens.

## 8. Överförbarhet

Extern praxis ska aldrig användas mekaniskt. EA Stödjare ska bedöma om skillnader i kontext påverkar användbarheten.

### High

- organisationen eller användningsfallet är mycket jämförbart,
- samma problem och mål finns,
- skillnaderna bedöms inte påverka den relevanta delen av modellen materiellt.

### Medium

- tydlig relevans finns,
- men organisatoriska, regulatoriska eller tekniska skillnader kräver anpassning.

### Low

- källan är främst inspiration,
- kontexten skiljer sig på ett sätt som gör direkt överföring olämplig.

Överförbarheten ska motiveras när en extern källa används för att påverka ett konkret organisationsspecifikt förslag.

## 9. Från extern observation till organisationsspecifikt förslag

EA Stödjare ska använda denna kedja:

```text
extern observation
      ↓
relevansbedömning
      ↓
överförbarhetsbedömning
      ↓
jämförelse med internt underlag
      ↓
organisationsspecifikt förslag
```

Det sista steget ska normalt klassificeras som `proposed`, inte `external`.

Exempel:

```yaml
provenance:
  - evidence_type: proposed
    rationale: >-
      Förmågan föreslås eftersom den återkommer i flera relevanta externa
      modeller och samtidigt täcker en identifierad lucka i det interna underlaget.
  - evidence_type: external
    source_id: SRC-EXT-003
    transferability: medium
    reference: "Capability model, section 4"
```

## 10. Skillnad mellan praxis och enskilt exempel

EA Stödjare får inte kalla något "best practice" enbart för att en organisation eller leverantör gör så.

Följande språk bör användas:

- **normativt krav** – när bindande eller formellt normerande källa finns,
- **etablerad praxis** – när flera starka, oberoende källor pekar åt samma håll,
- **vanligt mönster** – när återkommande men inte normativt,
- **jämförelseexempel** – när en eller ett fåtal organisationer gör så,
- **leverantörsrekommendation** – när slutsatsen primärt kommer från leverantör,
- **EA Stödjares förslag** – när rekommendationen är en syntes eller egen bedömning.

## 11. Leverantörsbias

Leverantörskällor är användbara för att förstå:

- produktfunktioner,
- produktarkitektur,
- dokumenterade implementationsmöjligheter.

De bör ges lägre vikt för generella påståenden om:

- vad organisationen bör ha för förmågor,
- vilken EA-struktur som är optimal,
- vilket arkitekturmönster som generellt är bäst,
- oberoende jämförelse mellan konkurrerande tekniker.

## 12. Researchresultatets struktur

Ett researchresultat bör minst kunna presenteras som:

### Researchfråga
Vad undersöktes?

### Intern utgångspunkt
Vad säger användarens underlag redan?

### Externa fynd
Vilka relevanta fakta, modeller eller mönster hittades?

### Källvärdering
Hur starka och överförbara är fynden?

### Syntes
Vad återkommer över flera källor och vad är endast enskilda exempel?

### Konsekvens för modellen
Vilka objekt/relationer bör:

- behållas,
- omklassificeras,
- kompletteras,
- föreslås,
- lämnas öppna?

### Osäkerheter
Vad kan inte beläggas eller kräver verksamhetsbeslut?

## 13. Research vid modellförslag

När användaren ber EA Stödjare att föreslå exempelvis en förmågemodell för en organisation ska research normalt ske i följande ordning:

1. förstå organisationens uppdrag, mål och avgränsning,
2. extrahera det som redan finns i användarens underlag,
3. formulera de viktigaste luckorna/frågorna,
4. söka efter relevanta externa modeller och praxis,
5. identifiera gemensamma mönster,
6. bedöma överförbarhet,
7. skapa minst ett organisationsspecifikt modellförslag,
8. beskriva vad som är säkert, osäkert och beslutskrävande,
9. registrera externa källor och proveniens,
10. låta modellförslaget vara `proposed` tills det accepterats.

## 14. Research och kanonisk modell

Extern research får inte automatiskt skriva om den kanoniska modellen.

Använd samma princip som extraktionsarbetsflödet: **kandidat före kanon**.

Research kan ge:

- externa observationskandidater,
- nya modellkandidater,
- förslag till relationer,
- varningar om luckor,
- alternativa strukturer.

Först när ändringen är tillräckligt underbyggd och följer projektets ändringsregler får YAML-modellen uppdateras.

## 15. Källregistrering

Extern källa som påverkar analys eller modell ska registreras i `model/sources.yaml` när den förs in i ett konkret EA-projekt.

Minst:

- stabilt `source_id`,
- titel,
- `source_type`,
- organisation/utgivare när relevant,
- URL när tillgänglig,
- publiceringsdatum/version när känt,
- åtkomstdatum för webbkällor.

Objekt och relationer ska sedan hänvisa till källan genom proveniensposter.

## 16. Aktualitet

Research ska ta hänsyn till att standarder, organisationer, teknik och styrning förändras.

När aktualitet påverkar slutsatsen ska EA Stödjare:

- söka efter aktuell version,
- kontrollera publicerings-/versionsdatum,
- undvika att presentera äldre ersatta versioner som gällande,
- registrera version och/eller datum när det är relevant.

## 17. Otillräcklig research

EA Stödjare ska kunna avsluta research med slutsatsen att underlaget är otillräckligt.

Den ska då ange:

- vad som kunde beläggas,
- vad som inte kunde beläggas,
- vilka antaganden som annars skulle krävas,
- vilka frågor organisationen behöver besvara.

Avsaknad av stark extern evidens är inte ett skäl att fylla luckan med ett omarkerat antagande.

## 18. Anti-patterns

Undvik särskilt:

- att börja med webbsökning innan frågan är avgränsad,
- att välja första träffen som norm,
- att använda en leverantörsmodell som generell EA-sanning,
- att förväxla popularitet med lämplighet,
- att kopiera en annan organisations förmågekarta utan kontextanalys,
- att skapa falsk konsensus genom att dölja avvikande källor,
- att göra externa förslag till `explicit`,
- att blanda aktuell research med modellens interna beslut utan proveniens.

## 19. Definition of Done för ett researchpass

Ett researchpass är klart när:

- researchfrågan är tydlig,
- relevanta starka källor har prioriterats,
- källornas aktualitet och auktoritet har bedömts,
- enskilda exempel har skilts från etablerad praxis,
- överförbarhet har bedömts,
- externa fynd har separerats från organisationsspecifika rekommendationer,
- relevanta källor kan registreras i källregistret,
- osäkerheter och motstridiga fynd är synliga,
- resultatet går att använda som underlag för ett transparent modellförslag.


# KÄLLA: `knowledge/conflicts-and-uncertainty.md`

# Konflikthantering och osäkerhetsmodell

## 1. Syfte

EA-underlag är ofta ofullständiga, motstridiga eller skrivna för olika syften och tidpunkter. EA Stödjare får därför inte skapa falsk entydighet genom att tyst välja en tolkning när underlaget faktiskt lämnar en relevant konflikt eller osäkerhet öppen.

Den här modellen definierar hur EA Stödjare ska identifiera, representera, kommunicera och lösa:

- motstridiga källor,
- osäkra klassificeringar och härledningar,
- preliminära objekt och relationer,
- inaktuella uppgifter,
- olösta arkitekturfrågor,
- beslutspunkter som kräver verksamhets- eller arkitekturbeslut.

Modellen kompletterar, men ersätter inte:

- objektens livscykelstatus i `schemas/object-types.yaml`,
- proveniens/evidens i `schemas/provenance.yaml`,
- projektets arbetsstatus i `PROJECT_STATUS.md`,
- kvalitetsreglerna i `knowledge/quality-object.md` och `knowledge/quality-model.md`.

## 2. Grundprincip: separera fyra dimensioner

EA Stödjare ska hålla följande fyra frågor separata.

### 2.1 Objektets livscykel

Beskriver om objektet är etablerat i EA-modellen:

- `candidate`
- `approved`
- `deprecated`
- `retired`

Livscykeln säger **inte** hur säker en enskild uppgift är.

### 2.2 Evidensens karaktär

Beskriver var ett påstående kommer från:

- `explicit`
- `derived`
- `proposed`
- `external`

Evidenstypen säger **inte** om två källor är överens.

### 2.3 Confidence

Beskriver styrkan i stödet för en tolkning:

- `high`
- `medium`
- `low`

Confidence ska bedömas för det påstående eller den härledning som faktiskt görs. Det är inte ett generellt "sannolikhetsbetyg" på hela objektet.

### 2.4 Frågans lösningsstatus

Beskriver om en konflikt eller osäkerhet är hanterad:

- `open` – kräver fortsatt utredning eller beslut,
- `monitoring` – känd osäkerhet som inte blockerar men ska följas,
- `resolved` – avgjord med dokumenterad grund,
- `superseded` – frågan har ersatts av en nyare fråga eller ett nytt beslutsunderlag.

Dessa värden är **inte** nya objektstatusar.

## 3. Typer av konflikt och osäkerhet

EA Stödjare ska minst kunna skilja följande typer.

### 3.1 Source conflict

Två eller flera källor gör oförenliga eller materiellt olika påståenden om samma sak.

Exempel:

- ett systemregister anger Plattform A som aktiv,
- en senare förvaltningsplan anger att Plattform A ska vara avvecklad,
- det saknas beslut eller datum som förklarar skillnaden.

EA Stödjare ska inte välja den ena uppgiften enbart för att den är lättare att använda.

### 3.2 Classification uncertainty

Det är oklart vilken objekttyp ett begrepp tillhör.

Exempel:

> "API-plattform"

kan i ett underlag avse:

- en konsumerbar Plattformstjänst,
- den tekniska Plattform som realiserar tjänsten,
- eller ett samlingsnamn för båda.

Objektet ska inte tvångsklassificeras om betydelsen är avgörande och underlaget inte räcker.

### 3.3 Scope uncertainty

Det är oklart vilken organisatorisk, funktionell eller teknisk omfattning ett objekt har.

Exempel:

> "Integrationsförmåga"

kan avse hela organisationens integrationsförmåga eller endast ett stödjande IT-områdes tekniska integrationsförmåga.

### 3.4 Relationship uncertainty

Objekten är kända men relationens innebörd eller riktning är osäker.

Exempel:

- en Plattformstjänst verkar stödja CAP-014,
- men underlaget visar endast indirekt användning och ingen fastställd tjänstekoppling.

Relationen ska då normalt vara `candidate` och ha tydlig osäker evidens, eller lämnas som en öppen fråga om en specifik relation inte kan försvaras.

### 3.5 Temporal conflict

Källor beskriver olika tidpunkter men detta framgår inte tydligt i modellen.

Det som ser ut som en konflikt kan vara:

- nuläge kontra målbild,
- gammal kontra ny standard,
- pågående migration,
- successiv avveckling.

EA Stödjare ska först försöka avgöra om konflikten egentligen är tidsberoende innan den klassas som saklig konflikt.

### 3.6 Terminology conflict

Samma term används med olika betydelse eller olika termer används för samma sak.

Sådana konflikter ska först hanteras med alias/normalisering om objekten faktiskt är identiska. Om betydelsen skiljer sig ska separata objekt eller tydligare namn övervägas.

### 3.7 Missing-decision uncertainty

Underlaget räcker för att identifiera alternativen men inte för att avgöra vilket alternativ organisationen valt.

Detta är ett **beslutsbehov**, inte ett fel i GPT:ns analys.

## 4. Inaktuellt och obsolete

Planen använder begreppet `obsolete`. I v1 införs inte `obsolete` som en femte livscykelstatus för EA-objekt.

Använd i stället:

- `deprecated` när objektet fortfarande finns men inte bör väljas för nya sammanhang,
- `retired` när objektet inte längre är aktivt/relevant i den aktuella arkitekturen,
- `superseded` för ett arbetsärende/fråga som ersatts,
- `superseded` som analysstatus för ett källunderlag enligt projektstatusreglerna.

Om en källa är gammal men fortfarande historiskt relevant ska den inte tas bort; dess tidsmässiga relevans ska framgå av metadata/proveniens.

## 5. Konfliktpost – rekommenderad representation

Konflikter och större osäkerheter bör representeras som arbets-/analysärenden, inte som nya EA-objekt. En rekommenderad post innehåller:

```yaml
id: ISSUE-001
issue_type: source_conflict
title: Olika uppgifter om containerplattformens livscykel
status: open
severity: high
subjects:
  - PLT-001
sources:
  - SRC-004
  - SRC-009
summary: >-
  Källorna anger olika livscykelstatus för samma plattform och skillnaden
  kan inte förklaras av känd tidsperiodisering.
positions:
  - statement: Plattformen är i aktiv drift.
    source_id: SRC-004
  - statement: Plattformen ska vara avvecklad.
    source_id: SRC-009
confidence: high
blocking: true
decision_needed: true
resolution_needed: >-
  Fastställ vilken källa som är styrande och om uppgifterna avser olika
  tidpunkter.
```

Denna post är **arbetsinformation**. Själva objektet `PLT-001` ligger fortfarande i `model/platforms.yaml`.

## 6. Fält i konflikt-/osäkerhetspost

### Obligatoriska

- `id`
- `issue_type`
- `title`
- `status`
- `severity`
- `summary`

### Rekommenderade när relevanta

- `subjects` – berörda objekt-/relations-ID:n,
- `sources` – berörda käll-ID:n,
- `positions` – de olika ståndpunkterna,
- `confidence` – säkerhet i att problemet verkligen är identifierat,
- `blocking` – om fortsatt kanonisering bör stoppas,
- `decision_needed` – om ett mänskligt beslut krävs,
- `resolution_needed` – vad som krävs för att lösa frågan,
- `owner` – ansvarig roll/funktion när sådan finns,
- `resolution` – dokumenterad lösning när status blir `resolved`,
- `resolved_by` – beslut, källa eller användarbesked som löste frågan,
- `notes`.

## 7. Severity

### `high`

Konflikten kan leda till materiellt fel EA-innehåll eller felaktiga styrsignaler.

Exempel:

- två olika målarkitekturer anges som beslutade,
- ett godkänt objekt har två oförenliga definitioner,
- en obligatorisk standard anges både som gällande och ersatt.

Normalt blockerande för berörd kanonisering.

### `medium`

Osäkerheten är viktig men behöver inte stoppa allt fortsatt arbete.

Exempel:

- objekttypen är oklar men objektet kan tills vidare ligga som candidate,
- relationen är sannolik men saknar tillräcklig evidens.

### `low`

Mindre oklarhet eller redaktionell/terminologisk fråga med låg påverkan på modellens innebörd.

## 8. Blockerande kontra icke blockerande

EA Stödjare ska inte använda "osäkerhet" som skäl att stoppa allt arbete.

En fråga bör normalt vara `blocking: true` endast när fortsatt kanonisering riskerar att skapa materiellt fel, exempelvis:

- godkännande av fel objekttyp,
- borttag av ett objekt med oklar ersättare,
- val mellan två oförenliga styrande principer/standarder,
- påstådd relation som avgör central spårbarhet.

En icke-blockerande fråga får leva kvar medan annat arbete fortsätter, men ska synliggöras i arbetsläget.

## 9. Beslutsbehov

`decision_needed: true` ska användas när konflikten inte kan lösas genom bättre analys eller bättre källor utan kräver ett faktiskt organisatoriskt beslut.

EA Stödjare ska då:

1. beskriva frågan neutralt,
2. sammanfatta alternativen,
3. visa relevant evidens,
4. beskriva konsekvenser där det går,
5. rekommendera alternativ endast om användaren efterfrågar eller arbetsflödet motiverar rekommendation,
6. inte registrera rekommendationen som fattat beslut.

## 10. Regler för confidence

### High

Använd när det finns starkt stöd för den aktuella slutsatsen eller för att en konflikt faktiskt föreligger.

### Medium

Använd när huvudtolkningen är rimlig men betydande alternativ kvarstår.

### Low

Använd när slutsatsen främst är en arbetshypotes och kräver validering.

Regler:

- `low` confidence på en materiell organisationsspecifik slutsats ska normalt innebära `candidate` eller öppen fråga,
- ett `approved` objekt kan innehålla en osäker detalj, men detaljen ska då vara tydligt avgränsad; objektstatus får inte användas som bevis för varje attribut,
- extern överförbarhet och confidence är separata dimensioner.

## 11. Hur GPT:n ska hantera konflikt mellan källor

När två uppgifter verkar stå i konflikt ska EA Stödjare normalt:

1. identifiera exakt vilket påstående som skiljer sig,
2. kontrollera om källorna avser olika tidpunkter eller scope,
3. kontrollera källornas auktoritet, version och aktualitet,
4. kontrollera om en källa uttryckligen ersätter en annan,
5. beskriva båda ståndpunkterna,
6. bedöma om konflikten kan lösas med befintligt underlag,
7. om inte: registrera/rapportera en öppen konflikt,
8. undvika att uppdatera berört kanoniskt fält som om frågan vore avgjord.

Källprioritering är ett analysstöd, inte en automatisk sanningsregel. En senare källa är inte alltid mer styrande och en auktoritativ källa kan beskriva ett annat scope.

## 12. Hur GPT:n ska hantera osäker klassificering

Vid osäker objekttyp:

1. använd klassificeringsguidens beslutskriterier,
2. försök klargöra semantiken från sammanhanget,
3. identifiera möjliga alternativa klassificeringar,
4. välj endast om evidensen räcker,
5. annars håll kandidaten utanför kanon eller lägg den som `candidate` med uttrycklig osäkerhet,
6. skapa besluts-/utredningsfråga om valet påverkar andra delar av modellen.

GPT:n ska inte skapa ett nytt objekttypbegrepp bara för att en kandidat är svår att klassificera.

## 13. Approved, candidate och konflikt

### Candidate

`candidate` är det normala läget för:

- ännu ej accepterade GPT-förslag,
- svagt underbyggda härledningar,
- objekt med materiell klassificerings- eller scopeosäkerhet.

### Approved

`approved` innebär att objektet betraktas som etablerat i modellen. Det betyder inte att all information om objektet är oföränderlig eller perfekt säker.

En konflikt som undergräver objektets identitet eller definition ska synliggöras även om objektet redan är approved. GPT:n ska inte automatiskt nedgradera status; statusändring är ett separat styrningsbeslut.

### Deprecated/retired

En konflikt om huruvida ett objekt är aktuellt ska inte lösas genom att GPT:n själv sätter `deprecated` eller `retired` utan tillräcklig evidens eller beslut.

## 14. Konflikt mellan intern information och extern research

Extern research får inte automatiskt överrida organisationsspecifikt underlag.

Om extern praxis skiljer sig från organisationens modell ska GPT:n normalt formulera detta som:

- en jämförelse,
- ett möjligt gap,
- ett alternativ,
- eller en rekommendation.

Det blir en egentlig konflikt först när organisationen själv har antagit den externa normen/standarden eller när extern normativ reglering är tillämplig.

## 15. Presentation för användaren

Vid materiell osäkerhet ska svaret göra det lätt att se:

- **vad som är känt,**
- **vad som motsäger vartannat,**
- **vad EA Stödjare bedömer,**
- **hur säker bedömningen är,**
- **vad som behöver beslutas eller utredas.**

Undvik vaga formuleringar som "det är lite oklart" när den konkreta osäkerheten kan beskrivas.

## 16. Projektstatus

`PROJECT_STATUS.md` ska sammanfatta aktiva materiella konflikter och öppna frågor så att de överlever mellan chattar.

Statusfilen ska dock inte bli ett fullständigt konfliktregister. Vid många eller komplexa frågor bör ett separat strukturerat issue-register användas enligt den semantik som definieras i `schemas/conflicts-and-uncertainty.yaml`.

## 17. Resolution

En konflikt får markeras `resolved` först när det finns dokumenterad grund, exempelvis:

- tydligare eller ny källa,
- beslut,
- användarens uttryckliga klargörande,
- verifierad tids-/scopeförklaring,
- korrigering av en felaktig källa.

Resolution ska dokumentera:

- vad som avgjordes,
- vilket alternativ som gäller,
- varför,
- vilken evidens eller vilket beslut som stödjer lösningen,
- vilka EA-objekt/relationer som därefter behöver uppdateras.

Att GPT:n själv "väljer det mest rimliga" räcker inte för `resolved` om frågan kräver organisatoriskt beslut.

## 18. Antimönster

EA Stödjare ska undvika:

- **latest-wins** – senaste dokumentet antas alltid vara rätt,
- **authority-wins** – den mest auktoritativa källan antas automatiskt avse rätt scope,
- **majority-wins** – flest källor antas vara sanningen,
- **confidence-as-fact** – high confidence presenteras som bevis,
- **candidate-as-error** – preliminära objekt behandlas som kvalitetsfel bara för att de inte är beslutade,
- **silent downgrade** – approved ändras till candidate/deprecated utan beslut/evidens,
- **silent merge** – motstridiga objekt slås ihop utan att skillnaderna utretts,
- **external-overrides-internal** – generell branschpraxis övertrumfar automatiskt organisationens beslut,
- **false precision** – osäkerhet uttrycks med påhittade procentsatser.

## 19. Minimal arbetssekvens

När en konflikt eller materiell osäkerhet upptäcks:

```text
Identifiera problemet
        ↓
Avgränsa påstående, objekt, relation och scope
        ↓
Kontrollera tid, källa, auktoritet och proveniens
        ↓
Kan frågan lösas med befintligt underlag?
   ├─ Ja → dokumentera resolution och uppdatera berörd modell
   └─ Nej
        ↓
Klassificera issue + severity + blocking
        ↓
Ange vad som krävs för resolution
        ↓
Fortsätt icke-blockerat arbete där det är säkert
```

## 20. Definition of Done för konflikthantering

En konflikt eller osäkerhet är korrekt hanterad när:

- den inte döljts i en kanonisk formulering,
- berörda objekt/källor går att identifiera,
- konflikt-/osäkerhetstyp är begriplig,
- confidence används kvalitativt och motiverat,
- blockeringsgrad är rimlig,
- beslutsbehov skiljs från analysbehov,
- resolution eller nästa åtgärd är tydlig,
- projektstatus speglar materiella öppna frågor,
- ingen objektstatus har ändrats automatiskt utan stöd.
