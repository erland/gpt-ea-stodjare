<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Domain Model

Denna fil konsoliderar följande kanoniska källor:

- `docs/metamodel.md`
- `docs/relations.md`
- `knowledge/classification-guide.md`

---


# KÄLLA: `docs/metamodel.md`

# EA Stödjare – metamodel v1

## 1. Syfte och status

Detta dokument definierar **EA Stödjares metamodel v1** efter utvecklingsplanens steg 3. Modellen är avsiktligt pragmatisk: den ska vara tillräckligt uttrycksfull för centralt enterprise architecture-arbete, men inte försöka modellera hela TOGAF, ArchiMate eller detaljerad lösningsarkitektur.

Metamodellen definierar vilka typer av arkitekturobjekt som får ingå i den kanoniska modellen, vad de betyder, vad de inte betyder och vilka grundattribut de behöver. Relationerna mellan objekten formaliseras separat i steg 4.

## 2. Övergripande designprinciper

1. **Förmågor beskriver vad organisationen eller IT behöver kunna åstadkomma – inte hur.**
2. **Funktion är inte ett eget globalt EA-objekt i v1.** Funktioner beskriver vad ett IT-stöd, en plattformstjänst eller en plattform tillhandahåller.
3. **IT-stöd, plattformstjänst och plattform ska hållas isär.**
4. **Produktnamn är inte automatiskt samma sak som plattformar.** En plattform kan realiseras av en eller flera produkter, men produktmodellering är inte en egen kärndomän i v1.
5. **Princip och standard ska hållas isär.** Principen uttrycker styrande arkitekturriktning; standarden uttrycker en mer konkret norm, regel, specifikation eller beslutad standardisering.
6. **Sekundära objekt får inte användas som en bakväg till lösningsarkitektur.** Lösningsmönster och referensarkitekturer ska hållas på återanvändbar enterprise-/styrningsnivå.
7. **Objekt ska ha stabil identitet.** Namn kan ändras utan att objektets ID ändras.
8. **Proveniens är obligatorisk som koncept men specificeras tekniskt i steg 5.**

## 3. Gemensamma kärnattribut

Alla primära och sekundära EA-objekt ska i den slutliga YAML-modellen kunna bära följande gemensamma information.

| Attribut | Krav | Betydelse |
|---|---|---|
| `id` | obligatoriskt | Stabil unik identitet enligt objekttypens prefix |
| `type` | obligatoriskt | Maskinläsbar objekttyp |
| `name` | obligatoriskt | Kort, entydigt användarnamn |
| `description` | obligatoriskt | Beskriver objektets innebörd och avgränsning |
| `status` | obligatoriskt | Livscykel-/beslutsstatus |
| `aliases` | valfritt | Kända alternativa benämningar |
| `owner` | valfritt | Ansvarig funktion/roll/organisatorisk enhet när relevant |
| `tags` | valfritt | Icke-kanonisk kategorisering för sökning/vyer |
| `notes` | valfritt | Kompletterande anteckningar som inte hör hemma i definitionen |
| `provenance` | senare obligatorisk struktur | Källa, härledning eller förslag enligt steg 5 |

### 3.1 Statusvärden v1

Följande gemensamma värden används som grund:

- `candidate` – identifierat eller föreslaget men ännu inte accepterat,
- `approved` – accepterat som del av den aktuella arkitekturmodellen,
- `deprecated` – bör inte längre användas för nya sammanhang men finns kvar för spårbarhet,
- `retired` – inte längre aktivt/relevant i aktuell arkitektur.

Status ska inte användas för att uttrycka evidensstyrka. Proveniens och säkerhet hanteras separat.

## 4. Primära objekttyper

## 4.1 Drivkraft (`driver`)

**ID-prefix:** `DRV-`

### Definition

En omständighet, kraft eller förändring som skapar behov av att organisationen agerar, prioriterar eller förändras.

Drivkrafter svarar typiskt på frågan:

> Varför behöver något förändras eller uppmärksammas?

Exempel:

- förändrad lagstiftning,
- ökade krav på digital service,
- höga kostnader för fragmenterad teknik,
- ökad cyberhotbild,
- behov av snabbare förändringsförmåga.

### Är inte

- ett önskat framtida resultat – det är normalt ett **Mål**,
- en regel för hur arkitektur ska utformas – det är normalt en **Princip**,
- en organisatorisk förmåga.

### Typiska attribut utöver kärnan

- `category` – exempelvis legal, strategic, operational, technology, economic, societal,
- `time_horizon` – valfri tidsmässig relevans.

---

## 4.2 Mål (`goal`)

**ID-prefix:** `GOAL-`

### Definition

Ett önskat framtida resultat eller tillstånd som organisationen vill uppnå.

Mål svarar typiskt på frågan:

> Vad vill vi uppnå?

Exempel:

- minska ledtiden från behov till produktionssatt IT-stöd,
- minska onödigt leverantörsberoende,
- öka återanvändningen av gemensamma IT-tjänster.

### Är inte

- orsaken till att förändring behövs – **Drivkraft**,
- en styrregel för arkitekturbeslut – **Princip**,
- en aktivitet eller ett projekt.

### Typiska attribut utöver kärnan

- `target_state` – valfri precisering av önskat tillstånd,
- `time_horizon` – valfri tidshorisont,
- `measure` – valfri referens till hur målet kan följas upp utan att EA Stödjare blir ett KPI-system.

---

## 4.3 Princip (`principle`)

**ID-prefix:** `PRN-`

### Definition

En varaktig styrande regel eller vägledning som ska påverka arkitekturbeslut och utformning över flera initiativ eller lösningar.

Principer svarar typiskt på frågan:

> Vilken övergripande regel ska vägleda våra arkitekturbeslut?

En välformad princip bör normalt kunna beskrivas med:

- statement,
- rationale,
- implications.

Exempel:

- gemensamma förmågor ska återanvändas före lokal duplicering,
- integrationsgränssnitt ska vara tydligt definierade och löst kopplade,
- data ska ha ett tydligt informationsägarskap.

### Är inte

- ett önskat resultat – **Mål**,
- en detaljerad teknisk regel eller vald specifikation – ofta **Standard**,
- ett allmänt positivt påstående utan konsekvenser för beslut.

### Typiska attribut utöver kärnan

- `statement` – principens normativa kärna,
- `rationale` – varför principen finns,
- `implications` – vilka konsekvenser den får för arkitektur och beslut.

---

## 4.4 Förmåga (`capability`)

**ID-prefix:** `CAP-`

### Definition

En stabil beskrivning av **vad organisationen eller dess IT-verksamhet behöver kunna åstadkomma**, oberoende av exakt organisation, process, system eller teknisk realisering.

Förmågor svarar typiskt på frågan:

> Vad behöver vi kunna göra eller åstadkomma?

### Obligatorisk undertyp

`capability_type` ska vara en av:

- `business` – verksamhetsförmåga,
- `it` – IT-förmåga.

#### Verksamhetsförmåga

Vad verksamheten behöver kunna åstadkomma för att fullgöra uppdrag och mål.

Exempel:

- hantera ärenden,
- genomföra kontroll,
- kommunicera med externa aktörer.

#### IT-förmåga

Vad IT-organisationen behöver kunna tillhandahålla eller åstadkomma för att möjliggöra verksamhetens och utvecklingsområdenas IT-behov.

Exempel:

- utveckla och bygga programvara,
- driftsätta applikationer,
- möjliggöra systemintegration,
- övervaka applikationer och tjänster.

### Är inte

- en process – process beskriver **hur** arbete utförs,
- en organisation/enhet – organisation beskriver **vem** som ansvarar,
- ett IT-system – **IT-stöd**,
- en teknisk funktion som autentisering eller autoskalning – normalt `functions` på ett relevant realiserande objekt.

### Typiska attribut utöver kärnan

- `capability_type` – obligatoriskt: `business` eller `it`,
- `scope` – valfri precisering av avgränsning,
- `consumer_scope` – valfri lättviktig beskrivning av vilka målgrupper, utvecklingsområden eller organisatoriska delar som förmågan avses betjäna; särskilt relevant för IT-förmågor.

### Särskild regel

EA Stödjare ska kunna beskriva vilka IT-förmågor ett stödjande utvecklingsområde behöver erbjuda utan att själva utvecklingsområdet måste bli en egen kärnobjekttyp i v1. Organisatoriskt ansvar kan uttryckas med `owner` och avsedda konsumenter med `consumer_scope`. Dessa är kontextattribut, inte egna organisationsobjekt eller relationer. Senare relations-/organisationsstöd införs endast om behovet motiverar det.

---

## 4.5 IT-stöd (`it_support`)

**ID-prefix:** `ITS-`

### Definition

Ett informationssystem, en applikation eller en sammanhållen digital tjänst som används för att stödja en eller flera verksamhets- eller IT-förmågor.

IT-stöd svarar typiskt på frågan:

> Vilket konkret digitalt stöd använder verksamheten eller IT för att utföra sitt arbete?

Exempel:

- ärendehanteringssystem,
- tullklareringssystem,
- behörighetsadministrationssystem,
- utvecklarportal.

### Är inte

- servicedesk/IT-support som organisatorisk funktion,
- en förmåga,
- ett erbjudande av generell teknisk plattformsfunktion – **Plattformstjänst**,
- den underliggande tekniska plattformen – **Plattform**.

### Typiska attribut utöver kärnan

- `functions` – funktioner som IT-stödet tillhandahåller,
- `lifecycle` – valfri livscykelinformation,
- `criticality` – valfri enkel kategorisering om organisationen behöver den.

### Funktioner

Funktioner ska beskriva konkreta saker IT-stödet kan göra, exempelvis:

- registrera ärende,
- besluta i ärende,
- söka ärendehistorik.

Funktionerna är underordnad information i v1 och har inte egna globala ID:n.

---

## 4.6 Plattformstjänst (`platform_service`)

**ID-prefix:** `PLS-`

### Definition

Ett standardiserat tekniskt eller gemensamt IT-erbjudande som kan konsumeras av IT-stöd, utvecklingsteam eller andra interna konsumenter och som abstraherar delar av den underliggande tekniska realiseringen.

Plattformstjänster svarar typiskt på frågan:

> Vilken gemensam teknisk tjänst erbjuder vi som konsumenter kan använda?

Exempel:

- containerplattformstjänst,
- meddelandetjänst,
- central logghantering,
- objektlagringstjänst,
- identitets-/autentiseringstjänst.

### Är inte

- den tekniska produkten eller plattformen som realiserar tjänsten – **Plattform**,
- ett verksamhetsnära system med egen verksamhetsfunktionalitet – normalt **IT-stöd**,
- en abstrakt IT-förmåga.

### Typiska attribut utöver kärnan

- `functions` – vad tjänsten erbjuder konsumenten,
- `service_level` – valfri referens/beskrivning,
- `consumer_scope` – valfri målgrupp eller tillåten konsumenttyp.

### Viktig gränsdragning

En IT-förmåga beskriver **vad IT behöver kunna erbjuda/åstadkomma**. En plattformstjänst beskriver **det konkreta, konsumtionsbara erbjudandet** genom vilket delar av förmågan kan göras tillgänglig.

---

## 4.7 Plattform (`platform`)

**ID-prefix:** `PLT-`

### Definition

En gemensam teknisk grund eller sammanhållen teknisk miljö som realiserar eller möjliggör en eller flera plattformstjänster och/eller tekniska funktioner.

Plattformar svarar typiskt på frågan:

> Vilken teknisk grund realiserar våra gemensamma tekniska erbjudanden?

Exempel:

- OpenShift-baserad containerplattform,
- central integrationsplattform,
- identitetsplattform,
- dataplattform.

### Är inte

- automatiskt samma sak som en enskild produkt,
- själva tjänsteerbjudandet till konsumenten – **Plattformstjänst**,
- ett verksamhetsnära IT-stöd.

### Typiska attribut utöver kärnan

- `functions` – tekniska funktioner plattformen tillhandahåller,
- `technology` – valfri teknisk beskrivning,
- `products` – valfri lista över centrala produkter/tekniker som realiserar plattformen; dessa är attribut i v1, inte egna kärnobjekt.

### Produktregel

Exempelvis kan `OpenShift` vara produkt/teknik i en bredare plattform eller, om organisationen faktiskt förvaltar den som en sammanhållen plattform, förekomma i plattformens namn. GPT:n ska klassificera utifrån **arkitekturrollen i organisationens modell**, inte enbart produktnamnet.

---

## 4.8 Standard (`standard`)

**ID-prefix:** `STD-`

### Definition

En beslutad eller normativ specifikation, regel, teknikstandard, informationsstandard eller annan konkret standardisering som styr eller begränsar arkitekturens utformning.

Standarder svarar typiskt på frågan:

> Vilken konkret standard, norm eller specifikation ska följas?

Exempel:

- beslutad API-standard,
- en tillämpad ISO-standard,
- beslutad standard för loggformat,
- standardiserad teknikprofil.

### Är inte

- en övergripande varaktig arkitekturregel – normalt **Princip**,
- ett lösningsmönster,
- en produktlista utan normativ betydelse.

### Typiska attribut utöver kärnan

- `standard_type` – exempelvis internal, external, legal, technical, information,
- `reference` – referens till standardens auktoritativa källa,
- `version` – tillämplig version när relevant,
- `mandatory` – om standarden är bindande inom definierat scope.

---

## 5. Sekundära objekttyper

## 5.1 Lösningsmönster (`solution_pattern`)

**ID-prefix:** `PAT-`

### Definition

En återanvändbar och vägledande lösningsstruktur för en återkommande typ av arkitekturproblem, beskriven på en nivå som kan tillämpas i flera lösningar.

Exempel:

- asynkront meddelandeutbyte,
- API-medierad systemintegration,
- centraliserad logginsamling.

### Är inte

- en detaljerad design för ett specifikt system,
- en referensarkitektur för ett helt område,
- en standard, även om en standard kan styra hur mönstret används.

### Typiska attribut

- `problem` – vilket återkommande problem mönstret adresserar,
- `context` – när det är tillämpligt,
- `approach` – den övergripande lösningsidén,
- `consequences` – viktiga konsekvenser/avvägningar.

---

## 5.2 Referensarkitektur (`reference_architecture`)

**ID-prefix:** `RA-`

### Definition

En återanvändbar, vägledande arkitektur för ett definierat område som beskriver centrala byggblock, ansvar, principer och relationer utan att vara designen för en specifik implementation.

Exempel:

- referensarkitektur för integration,
- referensarkitektur för identitet och åtkomst,
- referensarkitektur för dataplattform.

### Är inte

- den detaljerade lösningsarkitekturen för ett enskilt system,
- enbart ett diagram,
- ett enskilt lösningsmönster.

### Typiska attribut

- `scope` – vilket område referensarkitekturen omfattar,
- `applicability` – när den ska användas,
- `building_blocks` – övergripande byggblock/koncept på referensnivå,
- `guidance` – central vägledning.

---

## 6. Funktion som underordnat begrepp

`Function` införs **inte** som en egen objekttyp i v1.

I stället kan följande objekt ha `functions`:

| Objekttyp | `functions` | Exempel |
|---|---:|---|
| IT-stöd | Ja | registrera ärende, autentisera användare |
| Plattformstjänst | Ja | köra containeriserade applikationer, tillhandahålla meddelandekö |
| Plattform | Ja | orkestrera workloads, hantera secrets |
| Förmåga | Nej | själva objektet beskriver redan vad organisationen behöver kunna |

En funktion ska vara konkretare än en förmåga men behöver inte ha egen identitet, proveniens eller relationsgraf i v1.

### När Function kan behöva lyftas till eget objekt senare

Det kan bli motiverat om funktioner behöver:

- stabila globala ID:n,
- återanvändas mellan många objekt,
- ha egna relationer,
- ha egen livscykel/ägare,
- dokumenteras eller analyseras som en självständig katalog.

Det behovet finns inte tillräckligt tydligt för v1.

## 7. Centrala gränsdragningar

| Om frågan är… | Trolig objekttyp |
|---|---|
| Varför måste vi förändras? | Drivkraft |
| Vad vill vi uppnå? | Mål |
| Vilken övergripande regel ska styra beslut? | Princip |
| Vad behöver verksamheten eller IT kunna? | Förmåga |
| Vilket digitalt system/tjänst stödjer arbetet? | IT-stöd |
| Vilket standardiserat tekniskt erbjudande konsumeras? | Plattformstjänst |
| Vilken teknisk grund realiserar erbjudandet? | Plattform |
| Vilken konkret norm/specifikation ska följas? | Standard |
| Vilket återanvändbart sätt löser en återkommande problemtyp? | Lösningsmönster |
| Vilken generell arkitektur vägleder ett helt område? | Referensarkitektur |

## 8. Exempel på klassificering

### Exempel A – identitet

- `CAP-IT-...` eller CAP med `capability_type: it`: **Hantera digital identitet och åtkomst** – IT-förmåga.
- **Central autentiseringstjänst** – Plattformstjänst.
- **IAM-plattform** – Plattform.
- **Autentisera användare** – Funktion på tjänsten/plattformen.
- **Entra ID / Keycloak** – produkt/teknik om den används för att realisera plattformen, inte automatiskt en separat objekttyp.

### Exempel B – programvaruleverans

- **Driftsätta applikationer** – IT-förmåga.
- **Containerplattformstjänst** – Plattformstjänst som gör förmågan konsumtionsbar.
- **OpenShift-baserad applikationsplattform** – Plattform.
- **Automatisk skalning** – Funktion.

### Exempel C – verksamhetsstöd

- **Hantera ärenden** – Verksamhetsförmåga.
- **Ärendehanteringssystem** – IT-stöd.
- **Registrera ärende** – Funktion på IT-stödet.

## 9. Medvetet ej modellerat i v1

Följande är inte egna kärnobjekt i metamodel v1:

- organisation/enhet,
- stakeholder,
- process,
- aktivitet,
- informationsobjekt/datadomän,
- produkt/teknik,
- projekt/initiativ,
- roadmap/transitionsarkitektur,
- KPI/mätetal,
- risk,
- requirement/constraint som separata globala objekt,
- fysisk komponent,
- API/integrationskontrakt.

Information kan förekomma som attribut eller källkontext där det behövs. Om återkommande use case visar att någon av dessa behöver stabil identitet och egna relationer kan den introduceras i en senare metamodelversion.

## 10. Metamodellens v1-kontrakt

Efter steg 3 är följande beslut styrande inför relationsmodell och YAML-schema:

1. Åtta primära objekttyper används: Driver, Goal, Principle, Capability, IT Support, Platform Service, Platform och Standard.
2. Capability har undertyperna Business och IT.
3. Solution Pattern och Reference Architecture stöds som sekundära objekt.
4. Function är underordnad information på IT Support, Platform Service och Platform.
5. Produkt/teknik är inte en egen kärnobjekttyp.
6. Relationer mellan objekten definieras först i steg 4.
7. Proveniensens struktur definieras först i steg 5.
8. Exakt serialisering/YAML-schema fastställs först i steg 6; `schemas/object-types.yaml` i detta steg är en maskinläsbar domänspecifikation, inte det slutliga instanceschemat.


# KÄLLA: `docs/relations.md`

# EA Stödjare – relationsmodell v1

## 1. Syfte och status

Detta dokument definierar **relationsmodell v1** efter utvecklingsplanens steg 4. Syftet är att ge EA Stödjare ett litet, tydligt och maskinvaliderbart vokabulär för hur arkitekturobjekt får kopplas samman.

Relationsmodellen är medvetet restriktiv. En ny relationstyp ska bara införas när den uttrycker en återkommande och arkitekturellt viktig betydelse som inte kan uttryckas tydligt med befintliga relationer.

Proveniens för relationer specificeras i steg 5 och det slutliga instanceschemat i steg 6.

## 2. Grundprinciper

1. **Relationer har riktning och semantik.** `source`, `relation` och `target` ska kunna läsas som en begriplig sats.
2. **Relationen ska beskriva arkitekturell betydelse, inte bara association.** `related_to` används endast när en mer precis relation ännu inte kan fastställas.
3. **Samma sak ska inte modelleras dubbelt i både objektattribut och relationer.** Globala kopplingar mellan EA-objekt uttrycks i relationsmodellen. Underordnade `functions` förblir attribut.
4. **Förmågor realiseras inte automatiskt av IT-stöd.** Ett IT-stöd `supports` en förmåga. Förmågan är organisatorisk/IT-mässig förmåga och är inte samma sak som systemets funktionalitet.
5. **Plattformstjänst och Plattform hålls isär.** Plattformstjänsten kan `realized_by` en Plattform; ett IT-stöd kan `uses` en Plattformstjänst.
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

`uses` ska inte användas för att beskriva att en Plattformstjänst tekniskt implementeras av en Plattform; använd då `realized_by`.

---

### 4.4 `realized_by` – realiseras av

**Betydelse:** Källobjektet får sin konkreta realisering genom målobjektet.

**Primära användningar:**

- Plattformstjänst → Plattform
- Referensarkitektur → Lösningsmönster, när referensarkitekturen konkretiseras genom återanvändbara mönster

**Exempel:**

> Containerplattformstjänsten **realiseras av** OpenShift-plattformen.

Relationen ska inte användas mellan Förmåga och IT-stöd i v1; där används `supports` i motsatt riktning.

---

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
| `realized_by` | Plattformstjänst | Plattform |
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
| `Plattformstjänst realized_by Plattform` | Plattformen **realiserar** plattformstjänsten |
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
    └─ realized_by → PLT-001 OpenShift-plattform

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
realized_by
governed_by
constrains
depends_on
derived_from
related_to
```

Detta är avsiktligt färre relationstyper än vad ett fullskaligt EA-språk kan erbjuda. Målet är en modell som är lätt att förstå, lätt att validera och tillräckligt uttrycksfull för EA Stödjares v1-scope.


# KÄLLA: `knowledge/classification-guide.md`

# EA Stödjare – klassificerings- och normaliseringsguide v1

## 1. Syfte

Denna guide styr hur EA Stödjare klassificerar och normaliserar kandidater till enterprise architecture-objekt. Målet är att samma företeelse ska hamna på samma semantiska nivå oavsett om den upptäcks i ett strategidokument, en systemlista, ett plattformsunderlag eller genom extern research.

Guiden kompletterar `docs/metamodel.md`, `docs/relations.md`, `knowledge/workflow-extraction.md` och `knowledge/workflow-model-design.md`.

Grundregeln är:

> Klassificera efter vad objektet **är i modellen**, inte efter vilket ord källan råkar använda.

Ett dokument kan exempelvis kalla något "förmåga" trots att innehållet egentligen beskriver ett system, en aktivitet eller en tjänst. Källans terminologi är evidens, inte facit för klassificeringen.

---

## 2. Beslutsordning

När en kandidat identifieras ska EA Stödjare pröva frågorna i ungefär denna ordning:

1. Beskriver kandidaten **varför förändring behövs**? → Drivkraft.
2. Beskriver den **vilket resultat eller tillstånd som ska uppnås**? → Mål.
3. Beskriver den **en varaktig styrande regel för hur arkitekturbeslut ska fattas**? → Princip.
4. Beskriver den **vad organisationen eller IT behöver kunna åstadkomma**, oberoende av specifik organisation, process eller lösning? → Förmåga.
5. Beskriver den **ett konkret informationssystem, applikationsstöd eller digitalt stöd**? → IT-stöd.
6. Beskriver den **ett konsumtionsbart tekniskt erbjudande till IT-stöd eller utvecklingsteam**? → Plattformstjänst.
7. Beskriver den **den tekniska grund/miljö som realiserar tjänsterna**? → Plattform.
8. Beskriver den **ett normerande tekniskt eller metodmässigt krav/regelverk**? → Standard.
9. Beskriver den **ett återanvändbart sätt att lösa ett återkommande arkitekturproblem**? → Lösningsmönster.
10. Beskriver den **en generell rekommenderad arkitekturstruktur för ett område**? → Referensarkitektur.
11. Om inget passar: behåll kandidaten i analysarbetsytan och klassificera inte genom tvång.

---

## 3. Drivkraft kontra mål

### Drivkraft

En drivkraft beskriver ett förhållande, tryck, behov eller förändringsmotiv som gör att organisationen behöver agera.

Typiska former:

- ökade regulatoriska krav,
- förändrad hotbild,
- ökande kostnader,
- behov av snabbare förändringsförmåga,
- teknisk skuld,
- förändrade användarbehov.

### Mål

Ett mål beskriver ett önskat resultat eller tillstånd som organisationen vill uppnå.

Typiska former:

- minska ledtiden för driftsättning,
- öka graden av återanvändning,
- säkerställa spårbar åtkomst,
- minska beroendet av enskilda leverantörer.

### Test

Fråga:

> Är detta något som **driver oss**, eller något vi **vill uppnå**?

Exempel:

| Kandidat | Klassificering |
|---|---|
| Nya EU-krav på informationsutbyte | Drivkraft |
| Uppfylla nya EU-krav senast 2028 | Mål |
| Bristande skalbarhet i nuvarande lösningar | Drivkraft |
| Kunna skala kritiska tjänster utan manuell kapacitetsökning | Mål |

Vanligt fel: formulera om en drivkraft till mål utan att markera det som en härledning.

---

## 4. Mål kontra princip

### Princip

En princip är en varaktig styrande regel som ska vägleda flera framtida arkitekturbeslut. Den ska normalt innehålla eller kunna kompletteras med rationale och implikationer.

Exempel:

- "API:er ska utformas kontraktsdrivet och versionshanteras."
- "Gemensamma förmågor ska i första hand realiseras som återanvändbara tjänster."

### Test

Fråga:

> Beskriver detta **vad vi vill uppnå** eller **hur vi återkommande ska fatta arkitekturbeslut**?

"Minska leverantörsberoendet" är ett mål. "Lösningskomponenter ska kunna ersättas genom dokumenterade standardiserade gränssnitt" kan vara en princip som härletts ur målet.

EA Stödjare får inte göra den senare till `explicit` bara för att målet är explicit.

---

## 5. Princip kontra standard

### Princip

Styr beslutsriktningen och uttrycker varför/hur arkitekturen bör utformas.

### Standard

Anger en fastställd norm, specifikation, teknikregel eller annan mer konkret styrning som ska följas inom ett definierat scope.

Exempel:

| Kandidat | Typ |
|---|---|
| Öppna standarder ska prioriteras | Princip |
| HTTP Semantics RFC 9110 ska följas för HTTP-baserade API:er | Standard |
| All extern trafik ska använda TLS 1.3 | Standard, om detta är ett beslutat normerande krav |

En standard kan vara extern eller intern. Ett produktval är inte automatiskt en standard.

---

## 6. Förmåga kontra process

### Förmåga

Beskriver **vad organisationen behöver kunna göra**, relativt stabilt över tid och utan att ange exakt arbetsflöde eller organisatoriskt ansvar.

Bra namn är ofta substantiverade verbfraser, exempelvis:

- Hantera digitala identiteter
- Integrera informationssystem
- Utveckla och bygga programvara
- Hantera tullärenden

### Process

Beskriver **hur arbete utförs i en sekvens av aktiviteter**.

Exempel:

- Förmåga: Hantera behörigheter
- Process: Beställa, godkänna, tilldela och avsluta behörighet

Process är inte en kärnobjekttyp i v1. Processinformation får behållas i underlaget eller som kontext men ska inte felaktigt läggas i `capabilities.yaml`.

### Test

Fråga:

> Skulle behovet av detta kvarstå även om organisation, processflöde och system förändrades?

Om ja talar det för förmåga.

---

## 7. Förmåga kontra funktion

Detta är en central gränsdragning i EA Stödjare v1.

### Förmåga

Beskriver vad verksamheten eller IT behöver kunna åstadkomma.

### Funktion

Beskriver vad ett konkret IT-stöd, en Plattformstjänst eller en Plattform tillhandahåller.

Exempel:

- IT-förmåga: Driftsätta applikationer
- Plattformstjänst: Containerplattformstjänst
- Funktioner: driftsätta container-workloads, autoskalning, secrets-hantering

Funktion är **inte ett globalt EA-objekt i v1**. Den lagras som underordnad information på IT-stöd, Plattformstjänst eller Plattform.

### Test

Fråga:

> Är detta något organisationen behöver kunna, eller något ett konkret tekniskt objekt erbjuder?

Förmåga får inte reduceras till en produktfunktionslista.

---

## 8. Verksamhetsförmåga kontra IT-förmåga

Båda representeras som `capability`, med `capability_type`.

### Verksamhetsförmåga (`business`)

Beskriver vad verksamheten behöver kunna åstadkomma för att fullgöra sitt uppdrag eller skapa verksamhetsvärde.

Exempel:

- Genomföra riskbaserade kontroller
- Hantera tillstånd
- Hantera kundärenden

### IT-förmåga (`it`)

Beskriver vad IT-funktionen behöver kunna erbjuda eller åstadkomma för att möjliggöra verksamhetens och utvecklingsområdenas digitala leverans.

Exempel:

- Bygga programvara
- Driftsätta applikationer
- Tillhandahålla observability
- Integrera informationssystem

### Test

Fråga:

> Är primär mottagare av förmågan verksamhetens uppdrag/resultat eller IT-leveransen som möjliggör digital utveckling?

Om klassificeringen beror på organisationskontext ska den motiveras och osäkerheten behållas.

För IT-förmågor kan `owner` ange ansvarigt område och `consumer_scope` ange vilka utvecklingsområden, team eller andra målgrupper som förmågan är avsedd att betjäna. Detta ska inte tolkas som att Organisation blivit en egen objekttyp i v1.

---

## 9. Funktion kontra IT-stöd

### Funktion

En avgränsad sak som ett tekniskt objekt kan göra.

### IT-stöd

Ett konkret informationssystem, applikationsstöd eller digitalt stöd som används för att stödja en eller flera förmågor.

Exempel:

- Funktion: Registrera ett ärende
- IT-stöd: Ärendehanteringssystem

- Funktion: Kontrollera behörighet
- IT-stöd: Identitets- och behörighetssystem

Ett verb uttryckt som en funktion får inte automatiskt göras till ett IT-stöd. Ett produktnamn eller systemnamn får inte automatiskt göras till en funktion.

---

## 10. IT-stöd kontra Plattformstjänst

### IT-stöd

Stödjer verksamhets- eller IT-förmågor genom ett informationssystem eller applikationsnära stöd. Användarvärdet eller verksamhetsstödet är centralt.

### Plattformstjänst

Ett standardiserat tekniskt erbjudande som konsumeras av IT-stöd, utvecklingsteam eller andra tekniska tjänster.

Exempel:

| Kandidat | Typ |
|---|---|
| Ärendehanteringssystem | IT-stöd |
| Tullklareringssystem | IT-stöd |
| Containerplattform som tjänst | Plattformstjänst |
| Central logghantering | Plattformstjänst |
| Meddelandetjänst | Plattformstjänst |

### Test

Fråga:

> Är den primära konsumenten verksamhetsanvändaren/verksamhetsflödet, eller andra IT-stöd och utvecklingsteam?

Detta är en heuristik, inte en absolut regel. En tjänst kan ha flera konsumenttyper.

---

## 11. Plattformstjänst kontra Plattform

### Plattformstjänst

Beskriver **erbjudandet** och hur en teknisk förmåga görs konsumtionsbar.

### Plattform

Beskriver **den tekniska realiseringsgrunden** bakom erbjudandet.

Exempel:

- Plattformstjänst: Containerplattformstjänst
- Plattform: OpenShift-baserad containerplattform

- Plattformstjänst: Meddelandetjänst
- Plattform: IBM MQ-plattform

### Test

Fråga:

> Skulle vi fortfarande behöva beskriva erbjudandet även om den underliggande tekniska produkten byttes?

Om ja är erbjudandet sannolikt en Plattformstjänst och realiseringen en Plattform.

En Plattform kan tillhandahålla funktioner direkt, men det gör den inte automatiskt till en Plattformstjänst.

---

## 12. Plattform kontra produkt/teknik

Produkt/teknik är inte en egen kärnobjekttyp i v1.

En Plattform är en organisationellt relevant teknisk realiseringsmiljö eller sammanhållen teknisk grund. Den kan bestå av en eller flera produkter/tekniker.

Exempel:

- Kubernetes är en teknik.
- Red Hat OpenShift är en produkt/plattformsteknik.
- Organisationens "Containerplattform Produktion" kan vara ett EA-objekt av typen Plattform som använder OpenShift.

EA Stödjare ska inte automatiskt skapa ett Plattform-objekt för varje namngiven produkt i en inventering. Kandidaten måste ha relevant identitet och betydelse i organisationens arkitekturmodell.

Produktinformation kan i v1 beskrivas som attribut, exempelvis `technology` eller i beskrivning/taggar om schemat medger det.

---

## 13. Lösningsmönster kontra referensarkitektur

### Lösningsmönster

Ett återanvändbart sätt att lösa ett återkommande arkitekturproblem. Har normalt ett avgränsat problem, kontext, rekommenderad struktur och konsekvenser.

Exempel:

- Händelsedriven integration
- API gateway som kontrollerad exponeringspunkt

### Referensarkitektur

En mer sammanhållen generell arkitektur för ett område med rekommenderade byggblock, ansvar och relationer.

Exempel:

- Referensarkitektur för API-baserad integration
- Referensarkitektur för containerbaserad applikationsdrift

### Test

Fråga:

> Är detta ett återanvändbart svar på ett specifikt återkommande problem, eller en sammanhängande modell för ett helt arkitekturområde?

Första fallet talar för Lösningsmönster, andra för Referensarkitektur.

---

## 14. Objekt kontra attribut

All information ska inte bli objekt.

Skapa normalt ett självständigt objekt när företeelsen behöver minst något av följande:

- stabil egen identitet,
- egna relationer,
- egen livscykel/status,
- återanvändning från flera andra objekt,
- separat proveniens,
- separat dokumentation eller styrning.

Behåll som attribut/underobjekt när informationen främst beskriver ett annat objekt.

Exempel:

- Funktioner på ett IT-stöd → attribut/underobjekt i v1.
- Produktversion för en Plattform → attribut.
- Ett återanvändbart normerande dokument som styr flera plattformar → Standard-objekt.

---

## 15. Normalisering av namn

Normalisering får aldrig ändra betydelsen utan evidens.

### 15.1 Grundregler

- använd ett kort, begripligt och stabilt kanoniskt namn,
- undvik organisationsnamn i förmågor om de inte är semantiskt nödvändiga,
- undvik produktnamn i förmågor,
- använd singular/plural konsekvent inom en objekttyp,
- undvik namn som enbart består av interna förkortningar,
- behåll väl etablerade akronymer som alias vid behov,
- normalisera stavning och kapitalisering utan att skapa nya semantiska antaganden.

### 15.2 Förmågenamn

Förmågor bör normalt uttrycka vad man kan åstadkomma och vara relativt teknik- och organisationsneutrala.

Bra:

- Hantera digitala identiteter
- Integrera informationssystem
- Driftsätta applikationer

Svagare:

- IAM-teamet
- OpenShift
- API-processen

### 15.3 Tjänste- och plattformsnamn

Namn ska göra nivåskillnaden synlig när det behövs.

Exempel:

- `Containerplattformstjänst` – erbjudandet
- `Containerplattform Produktion` – teknisk plattform

Undvik att kalla både tjänst och plattform exakt `OpenShift` om de ska vara separata objekt.

---

## 16. Alias, dubbletter och överlapp

### Alias

Två namn för samma objekt ska normalt bli ett kanoniskt objekt med alias, inte två objekt.

Exempel:

- "IAM"
- "Identitets- och åtkomsthantering"

kan vara samma objekt om underlaget visar att de avser samma sak.

### Dubblett

Skapa inte nytt ID förrän befintliga objekt kontrollerats utifrån:

- namn,
- alias,
- definition,
- scope,
- relationer,
- källor.

### Överlapp

Två objekt kan vara olika men delvis överlappande. Då ska de inte slås ihop automatiskt. Markera överlappet och föreslå modellbeslut.

---

## 17. Blandade eller sammansatta kandidater

Källmaterial innehåller ofta uttryck som blandar flera nivåer, exempelvis:

> "Gemensam integrationsplattform och förmåga för säkert informationsutbyte"

Detta ska inte tvingas in som ett enda objekt. Dekomponera kandidaten när evidensen medger det, exempelvis:

- IT-förmåga: Integrera informationssystem
- Plattformstjänst: Integrationstjänst
- Plattform: Integrationsplattform

Varje nytt objekt får egen proveniens som visar att det härletts ur samma ursprungliga formulering.

---

## 18. Klassificering vid osäkerhet

EA Stödjare ska uttrycka osäkerhet hellre än skapa falsk precision.

När två klassificeringar är rimliga:

1. dokumentera kandidatens ursprungliga formulering,
2. ange primär föreslagen klassificering,
3. ange relevant alternativ,
4. förklara vilket kriterium som avgör,
5. använd `confidence` enligt proveniensmodellen,
6. kanonisera inte hög-risk-fall utan tillräcklig grund.

Exempel:

> "Logghantering" kan avse en IT-förmåga, en Plattformstjänst eller en teknisk funktion. Underlaget måste visa om det beskriver organisationens förmåga, erbjudandet eller plattformens funktion.

---

## 19. Klassificeringsanti-patterns

EA Stödjare ska särskilt reagera på:

- organisationsenheter modellerade som Förmågor,
- processsteg modellerade som Förmågor,
- produkter modellerade som Förmågor,
- en teknisk funktion modellerad som Plattformstjänst utan faktiskt erbjudande,
- Plattform och Plattformstjänst hopslagna enbart för att samma produktnamn används,
- mål formulerade som principer,
- principer som bara upprepar mål,
- interna beslut eller produktval presenterade som externa Standarder,
- Lösningsmönster som egentligen är detaljerad lösningsdesign,
- Referensarkitektur som egentligen beskriver en specifik produktionslösning.

---

## 20. Minimal klassificeringsrapport

Vid analys av en kandidat bör EA Stödjare kunna redovisa minst:

```text
Kandidat: "Central logghantering"
Föreslagen typ: Plattformstjänst
Confidence: medium
Motivering: Formuleringen beskriver ett gemensamt tekniskt erbjudande till flera IT-stöd.
Alternativ: IT-förmåga, om underlaget i stället beskriver vad IT-organisationen behöver kunna.
Behöver verifieras: vem som konsumerar erbjudandet och om det finns en separat teknisk plattform.
Proveniens: explicit kandidat; klassificeringen derived.
```

Denna rapport är analysinformation. Den behöver inte lagras som eget kanoniskt objektformat.

---

## 21. Sammanfattande tumregel

EA Stödjare ska försöka hålla följande semantiska nivåer isär:

```text
VARFÖR förändring behövs          → Drivkraft
VAD vi vill uppnå                 → Mål
HUR beslut ska styras             → Princip
VAD organisationen/IT behöver kunna → Förmåga
VAD ett system konkret stödjer med → IT-stöd + funktioner
VAD IT erbjuder konsumtionsbart   → Plattformstjänst + funktioner
VAD erbjudandet tekniskt bygger på → Plattform + funktioner
VAD som normativt ska följas      → Standard
HUR ett återkommande problem löses → Lösningsmönster
HUR ett område generellt struktureras → Referensarkitektur
```

När verkligheten inte passar modellen ska EA Stödjare markera modellfrågan i stället för att förvränga verkligheten för att få en klassificering.
