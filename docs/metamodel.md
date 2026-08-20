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
