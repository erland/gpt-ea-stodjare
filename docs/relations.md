# EA Stödjare – relationsmodell v1 med v2-utökningar

## 1. Syfte och status

Detta dokument definierar **relationsmodell v1** efter utvecklingsplanens steg 4. Syftet är att ge EA Stödjare ett litet, tydligt och maskinvaliderbart vokabulär för hur arkitekturobjekt får kopplas samman.

Relationsmodellen är medvetet restriktiv. En ny relationstyp ska bara införas när den uttrycker en återkommande och arkitekturellt viktig betydelse som inte kan uttryckas tydligt med befintliga relationer.

Proveniens för relationer specificeras i steg 5 och det slutliga instanceschemat i steg 6.

## 2. Grundprinciper

1. **Relationer har riktning och semantik.** `source`, `relation` och `target` ska kunna läsas som en begriplig sats.
2. **Relationen ska beskriva arkitekturell betydelse, inte bara association.** `related_to` används endast när en mer precis relation ännu inte kan fastställas.
3. **Samma sak ska inte modelleras dubbelt i både objektattribut och relationer.** Globala kopplingar mellan EA-objekt uttrycks i relationsmodellen. Underordnade `functions` förblir attribut.
4. **Förmågor realiseras inte automatiskt av IT-stöd.** Ett IT-stöd `supports` en förmåga. Förmågan är organisatorisk/IT-mässig förmåga och är inte samma sak som systemets funktionalitet.
5. **Plattformstjänst och Plattform hålls isär.** I native v2 använder Plattformstjänsten `provided_by` för konceptuell hemvist i en Plattform; ett IT-stöd kan `uses` en Plattformstjänst. Legacy v1 kan fortsatt använda `realized_by` enligt den frysta v1-profilen.
6. **Strategiska relationer får vara många-till-många.** En Drivkraft kan påverka flera Mål och ett Mål kan påverkas av flera Drivkrafter.
7. **Relationer ska kunna ha egen proveniens.** Det kan vara belagt att två objekt finns men endast härlett att de har en viss relation.
8. **Avsaknad av relation är inte automatiskt ett fel.** Kvalitetsregler för förväntade relationer definieras senare.

## 3. Kanoniskt relationsformat

Relationsinstanser ska i steg 6 kunna uttryckas ungefär så här:

```yaml
- id: REL-0001
  source: DRV-001
  relation: influences
  target: GOAL-001
```

`id` blir stabil identitet för relationen. Proveniens och övrig metadata läggs till i senare steg.

## 4. Relationstyper v1

### 4.1 `influences` – påverkar

**Betydelse:** Källobjektet är en bidragande orsak eller påverkansfaktor för målobjektet, utan att ensamt realisera eller styra det.

**Primära användningar:**

- Drivkraft → Mål
- Drivkraft → Princip
- Mål → Princip
- Mål → Förmåga

**Exempel:**

> Ökad cyberhotbild **påverkar** målet att öka motståndskraften.

Använd inte `influences` när en mer precis styr-, stöd- eller realiseringsrelation finns.

---

### 4.2 `supports` – stödjer

**Betydelse:** Källobjektet bidrar konkret till att målobjektet kan utövas eller uppnås, men är inte liktydigt med målobjektet.

**Primära användningar:**

- IT-stöd → Förmåga
- Plattformstjänst → IT-förmåga
- Lösningsmönster → Förmåga
- Referensarkitektur → Förmåga

**Exempel:**

> Ärendehanteringssystemet **stödjer** förmågan Hantera ärenden.

> Containerplattformstjänsten **stödjer** IT-förmågan Driftsätta applikationer.

Det rekommenderade läsriktningen är alltså från det stödjande objektet till det som stöds. Användargränssnitt och dokumentation får naturligt visa den inversa formuleringen ”Förmåga stöds av …”.

---

### 4.3 `uses` – använder

**Betydelse:** Källobjektet konsumerar eller använder målobjektet som en del av sin funktion eller realisering.

**Primära användningar:**

- IT-stöd → Plattformstjänst
- Plattformstjänst → Plattformstjänst
- Plattform → Plattformstjänst, endast när en plattform själv konsumerar en separat plattformstjänst

**Exempel:**

> Tullklareringssystemet **använder** den gemensamma meddelandetjänsten.

`uses` ska inte användas för att beskriva Plattformstjänstens konceptuella hemvist; använd i native v2 `provided_by`. `realized_by` reserveras för konkret realiseringssemantik där projektmetamodellen uttryckligen stödjer den.

---

### 4.4 `provided_by` – tillhandahålls av

**Semantik:** Plattformstjänsten har sin konceptuella hemvist i och tillhandahålls inom Plattformen. Relationen beskriver gruppering/hemvist, inte konkret implementation.

Tillåten native v2-kombination:

- Plattformstjänst → Plattform

`provided_by` innebär inte att Plattformen är en produkt, att en enda produkt realiserar hela tjänsten eller att organisationen faktiskt erbjuder en viss produktbaserad runtime.

### 4.4b `realized_by` – realiseras av

**Semantik:** konkret realisering. I native v2 används `realized_by` inte för Plattformstjänst → Plattform. Relationstypen kan fortsatt användas där den definierade projektmetamodellen verkligen behöver konkret realiseringssemantik, exempelvis Referensarkitektur → Lösningsmönster. Legacy v1 `PLS --realized_by--> PLT` tolkas genom den frysta v1-profilen tills kontrollerad migration görs.

### 4.5 `governed_by` – styrs av

**Betydelse:** Källobjektets utformning, användning eller utveckling ska följa ett styrande målobjekt.

**Tillåtna målobjekt:** Princip eller Standard.

**Primära källobjekt:**

- Förmåga
- IT-stöd
- Plattformstjänst
- Plattform
- Lösningsmönster
- Referensarkitektur

**Exempel:**

> Plattformstjänsten **styrs av** principen Återanvänd gemensamma tjänster.

> API-mönstret **styrs av** organisationens API-standard.

I användarvänlig framställning kan inversen visas som ”Principen styr …”. Den kanoniska lagringen använder `governed_by` för att relationens mål ska vara det styrande objektet.

---

### 4.6 `constrains` – begränsar

**Betydelse:** Källobjektet sätter en uttrycklig begränsning på vilka val eller utformningar som är tillåtna för målobjektet.

**Primära användningar:**

- Standard → IT-stöd
- Standard → Plattformstjänst
- Standard → Plattform
- Standard → Lösningsmönster
- Standard → Referensarkitektur

**Exempel:**

> Krypteringsstandarden **begränsar** vilka algoritmer plattformen får använda.

Skillnad mot `governed_by`: `governed_by` beskriver att ett objekt omfattas av styrningen; `constrains` används när det är relevant att explicit modellera att styrningen begränsar handlingsutrymmet. De två ska inte rutinmässigt dubbleras för samma sak.

---

### 4.7 `depends_on` – beror på

**Betydelse:** Källobjektet är beroende av att målobjektet finns eller fungerar för att självt kunna fungera eller vara relevant.

**Primära användningar:**

- Förmåga → Förmåga
- IT-stöd → IT-stöd
- Plattformstjänst → Plattformstjänst
- Plattform → Plattform
- Lösningsmönster → Lösningsmönster
- Referensarkitektur → Referensarkitektur

**Exempel:**

> IT-förmågan Automatiserad driftsättning **beror på** IT-förmågan Hantera byggartefakter.

Använd inte `depends_on` som ersättning för `uses` eller `realized_by` när den mer specifika relationen är känd.

---

### 4.8 `derived_from` – härledd från

**Betydelse:** Källobjektets existens, formulering eller innehåll har härletts från målobjektet.

**Primära användningar:**

- Mål → Drivkraft
- Princip → Drivkraft
- Princip → Mål
- Förmåga → Mål
- Lösningsmönster → Princip
- Referensarkitektur → Princip
- Referensarkitektur → Standard

**Exempel:**

> Principen Minimera leverantörslåsning **är härledd från** målet Minska strategiskt leverantörsberoende.

`derived_from` uttrycker härledning/spårbarhet och är därför inte samma sak som `influences`. Båda kan i undantagsfall finnas mellan samma objekt, men endast om de uttrycker två faktiskt olika påståenden.

---

### 4.9 `related_to` – relaterar till

**Betydelse:** Det finns en relevant arkitekturell koppling mellan objekten men underlaget räcker ännu inte för en mer precis relation.

**Tillåtelse:** Mellan alla EA-objekttyper.

**Regel:** Ska användas sparsamt och normalt endast för `candidate`-relationer eller ofullständigt underlag. När relationens betydelse har klarlagts ska den ersättas av en mer specifik relationstyp.

---

## 5. Tillåtna source/target-kombinationer

Tabellen sammanfattar den kanoniska riktningen.

| Relation | Source | Target |
|---|---|---|
| `influences` | Drivkraft | Mål, Princip |
| `influences` | Mål | Princip, Förmåga |
| `supports` | IT-stöd | Förmåga |
| `supports` | Plattformstjänst | IT-förmåga |
| `supports` | Lösningsmönster | Förmåga |
| `supports` | Referensarkitektur | Förmåga |
| `uses` | IT-stöd | Plattformstjänst |
| `uses` | Plattformstjänst | Plattformstjänst |
| `uses` | Plattform | Plattformstjänst |
| `provided_by` | Plattformstjänst | Plattform |
| `realized_by` | Referensarkitektur | Lösningsmönster |
| `governed_by` | Förmåga, IT-stöd, Plattformstjänst, Plattform, Lösningsmönster, Referensarkitektur | Princip, Standard |
| `constrains` | Standard | IT-stöd, Plattformstjänst, Plattform, Lösningsmönster, Referensarkitektur |
| `depends_on` | Förmåga | Förmåga |
| `depends_on` | IT-stöd | IT-stöd |
| `depends_on` | Plattformstjänst | Plattformstjänst |
| `depends_on` | Plattform | Plattform |
| `depends_on` | Lösningsmönster | Lösningsmönster |
| `depends_on` | Referensarkitektur | Referensarkitektur |
| `derived_from` | Mål | Drivkraft |
| `derived_from` | Princip | Drivkraft, Mål |
| `derived_from` | Förmåga | Mål |
| `derived_from` | Lösningsmönster | Princip |
| `derived_from` | Referensarkitektur | Princip, Standard |
| `related_to` | valfri EA-objekttyp | valfri EA-objekttyp |

### Undertypregel för `supports`

`Plattformstjänst → Förmåga` är endast tillåten när målobjektets `capability_type` är `it`. Plattformstjänster ska inte direkt användas för att påstå att de stödjer en verksamhetsförmåga när länken egentligen går via IT-stöd eller IT-förmåga.

## 6. Inversa läsningar

För att hålla det maskinläsbara vokabuläret litet lagras inte separata inversrelationer. Presentationer får däremot använda naturligt språk.

| Kanonisk relation | Tillåten presentationsform |
|---|---|
| `IT-stöd supports Förmåga` | Förmågan **stöds av** IT-stödet |
| `Plattformstjänst provided_by Plattform` | Plattformen **tillhandahåller/grupperar** plattformstjänsten konceptuellt |
| `Objekt governed_by Princip` | Principen **styr** objektet |
| `Objekt uses Plattformstjänst` | Plattformstjänsten **används av** objektet |

Det ska alltså inte skapas en extra relation bara för att kunna skriva inversen.

## 7. Relationer som medvetet inte införs i v1

Följande relationer kan verka naturliga men tas inte in ännu:

- `owns` – organisation är inte kärnobjekt i v1; `owner` är attribut,
- `provides`/`consumes` – ansvar och konsumentorganisationer är ännu inte fullvärdiga objekt,
- `implements` – för tvetydigt mellan system, plattform och standard,
- `contains`/`part_of` – hierarkier behöver först ett separat designbeslut,
- `enables` – överlappar lätt med `supports`,
- `complies_with` – `governed_by` och `constrains` räcker i v1; faktisk compliance kräver mer evidens,
- `replaces` – livscykel och transitionsarkitektur ligger utanför kärnan i v1.

Om framtida användningsfall visar ett tydligt återkommande behov kan dessa införas versionsstyrt.

## 8. Exempel på sammanhängande modell

```text
DRV-001 Ökad förändringstakt
    └─ influences → GOAL-001 Kortare ledtid från behov till produktion

GOAL-001 Kortare ledtid från behov till produktion
    ├─ influences → CAP-IT-001 Driftsätta applikationer
    └─ derived-from-läsning från CAP-IT-001 tillbaka till GOAL-001

PLS-001 Containerplattformstjänst
    ├─ supports → CAP-IT-001 Driftsätta applikationer
    └─ provided_by → PLT-001 Containerplattform

ITS-001 Ärendehanteringssystem
    ├─ supports → CAP-001 Hantera ärenden
    └─ uses → PLS-001 Containerplattformstjänst
```

I den faktiska YAML-modellen används alltid de definierade maskinrelationerna, inte textetiketten i diagrammet.

## 9. Kvalitetsregler för relationer

Redan i v1 gäller följande semantiska grundregler:

- source och target får inte vara samma objekt,
- source och target måste existera,
- relationstypen måste vara definierad,
- source/target-kombinationen måste vara tillåten,
- exakta dubbletter ska inte förekomma,
- `related_to` ska inte användas om en mer specifik relation är känd,
- relationens formulering ska kunna motiveras med underlag, härledning eller uttryckligt förslag,
- en relation ska inte skapas enbart för att två objekt nämns i samma dokument.

Teknisk validering implementeras i steg 24; provenienskraven formaliseras i steg 5.

## 10. Designbeslut efter steg 4

Relationsmodell v1 består av nio relationstyper:

```text
influences
supports
uses
provided_by
realized_by
governed_by
constrains
depends_on
derived_from
related_to
```

Detta är avsiktligt färre relationstyper än vad ett fullskaligt EA-språk kan erbjuda. Målet är en modell som är lätt att förstå, lätt att validera och tillräckligt uttrycksfull för EA Stödjares v1-scope.


## 9. V2-utökning: `can_realize` – kan realisera

**Betydelse:** En Produkt har verifierade egenskaper som gör att den helt eller delvis kan realisera ett produktoberoende IT-stöd eller en Plattformstjänst. Relationens existens uttrycker marknads-/realiseringspotential och betyder **inte** att produkten används, är vald eller erbjuds av organisationen.

**Tillåtna riktningar:**

- Produkt → IT-stöd
- Produkt → Plattformstjänst

**Obligatorisk kvalificerare:** `realization_role`. Standardvärden i v2 är `primary`, `partial` och `supporting`. Projektmetamodellen får senare utöka värdemängden när en domän behöver mer detaljer, exempelvis `native_primary` eller `integrated`.

**Evidensregel:** Ett positivt `can_realize`-påstående ska ha källstödd proveniens. En relation som endast har `proposed`-evidens är inte tillräcklig som marknadspåstående. External, explicit eller härledd evidens med spårbar källa/underlag krävs.

Exempel:

```yaml
- id: REL-0901
  type: can_realize
  source: PRD-101
  target: ITS-020
  realization_role: primary
  status: candidate
  provenance:
    - evidence_type: external
      source_id: SRC-EXT-101
      reference: Produktdokumentation för dokumentredigering
      confidence: high
      transferability: high
```

Samma mönster kan användas för en plattformsprodukt mot en Plattformstjänst. Produktens närvaro i marknadsreferensen eller `can_realize` får aldrig infereras till faktisk organisationsanvändning.


## V2 steg 12 – generella relationskvalificerare

V2 behåller en liten relationskärna och använder **kvalificerare** när en relation behöver mer precision. Kvalificerare är metadata på relationen; de får aldrig användas för att ändra relationstypens grundbetydelse.

Standardkvalificerare:

| Kvalificerare | Typ | Standardvärden / semantik |
|---|---|---|
| `relation_role` | enum | `responsibility_boundary`, `cross_capability_support`, `information_dependency`, `lifecycle_dependency`, `operational_dependency`; projektextensibel |
| `strength` | enum | `structural`, `typical`, `optional`, `informational` |
| `mandatory` | boolean | Om relationen uttrycker ett obligatoriskt krav/beroende i aktuell kontext |
| `realization_role` | enum | `primary`, `partial`, `supporting`; projektextensibel och obligatorisk för `can_realize` |
| `verification_status` | enum | `verified`, `partially_verified`, `unverified`, `unknown` |
| `boundary_basis` | string | Kort motivering till boundary/klassificering |
| `notes` | string eller lista | Kompletterande kommentar |

Tillämpbarheten är **relationsspecifik** och definieras maskinläsbart i `schemas/relations.yaml`. Exempelvis är `realization_role` tillåten för `can_realize`, medan `relation_role` främst används på `related_to`, `supports`, `uses` och `depends_on`. En kvalificerare som inte är deklarerad för relationstypen är ogiltig.

`verification_status` ersätter aldrig relationens proveniens. `unknown` betyder att påståendet ännu inte är verifierat, inte att relationen är falsk. `mandatory` får inte användas för att göra en i grunden mjuk relationstyp semantiskt hårdare än vad relationstypens definition tillåter.

Exempel:

```yaml
- id: REL-1201
  type: related_to
  source: CAP-IT-001
  target: CAP-IT-002
  relation_role: responsibility_boundary
  strength: informational
  verification_status: verified
  boundary_basis: Ansvarsgränsen behöver synliggöras men är inte ett hårt beroende.
  status: approved
  provenance:
    - evidence_type: explicit
      source_id: SRC-001
```

```yaml
- id: REL-1202
  type: can_realize
  source: PRD-010
  target: ITS-004
  realization_role: partial
  strength: typical
  verification_status: verified
  status: candidate
  provenance:
    - evidence_type: external
      source_id: SRC-EXT-010
```
