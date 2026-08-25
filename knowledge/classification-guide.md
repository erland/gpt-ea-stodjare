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
6. Beskriver den **ett stabilt tekniskt erbjudande eller funktionalitetskontrakt som kan konsumeras, oberoende av hur eller var det realiseras**? → Plattformstjänst.
7. Beskriver den **den sammanhållna plattformsnivån** snarare än själva konsumtionskontraktet? → Plattform (v2-semantiken revideras fullt i steg 8).
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

## 6.1 Förmågeboundary i v2

Native v2 använder `in_scope`, `out_of_scope` och `consumer_scope` i stället för det äldre generella `scope`.

- `in_scope` beskriver den positiva boundaryn. För IT-förmågor ska den uttrycka **vilket tekniskt möjliggörande** konsumenten får.
- `out_of_scope` anger närliggande ansvar eller beteenden som uttryckligen inte ingår.
- `consumer_scope` anger vilka konsumentgrupper förmågan avses betjäna när det är relevant.

För IT-förmågor får `in_scope` inte bli en lista över produkter eller Plattformstjänster och inte heller beskriva verksamhetsfunktionalitet som om IT själv utförde den. Användarsynligt bör `in_scope` normalt rubriceras **Stödjer** och `out_of_scope` **Omfattar inte**.

Legacy v1-fältet `scope` tolkas enligt v1-profilen. Det får inte automatiskt omvandlas till positiv eller negativ boundary när ordalydelsen är tvetydig.

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

Beskriver **det konsumerbara tekniska erbjudandet eller funktionalitetskontraktet**: vad en lösning eller teknisk konsument behöver kunna få tillgång till utan att låsa realisering.

### Plattform

Beskriver **den produktneutrala konceptuella hemvisten** för ett sammanhållet kluster av Plattformstjänster.

Exempel:

- Plattformstjänst: Köra containeriserade workloads
- Plattform: Containerplattform

- Plattformstjänst: Meddelandetjänst
- Plattform: Integrationsplattform, om meddelandeområdet faktiskt ingår i ett sammanhållet integrationsnära erbjudandeområde

### Test

Fråga först:

> Är detta det tekniska erbjudande som konsumenten behöver, eller en konceptuell gruppering av flera sådana erbjudanden?

Om det är konsumtionslöftet: **Plattformstjänst**. Om det är den produktneutrala sammanhållningen/hemvisten: **Plattform**.

En Plattform behöver inte motsvara en viss runtime, produkt eller faktisk organisatorisk serviceinstans. En singleton-plattform kan vara legitim när tjänstelöfte, livscykel, kompetens eller förvaltning motiverar självständighet.

Legacy v1 använder en bredare Plattform-semantik som teknisk grund/realisering. Tillämpa därför inte denna v2-gränsdragning retroaktivt utan kontrollerad migration.

---

## 12. Produkt kontra IT-stöd, Plattformstjänst och Plattform

Native v2 har **Produkt** som generell stödjande objekttyp.

### Produkt kontra IT-stöd

- **IT-stöd** beskriver det produktoberoende digitala stöd organisationen behöver eller använder som stöd för förmågor, exempelvis **Ordbehandling**.
- **Produkt** beskriver ett konkret marknadserbjudande som kan bedömas som möjlig realisering, exempelvis en viss ordbehandlingsprodukt.

Testfråga: *Skulle behovet fortfarande finnas om den nuvarande produkten byttes ut?* Om ja är behovsobjektet normalt IT-stöd och produktnamnet Produkt.

### Produkt kontra Plattformstjänst

- **Plattformstjänst** beskriver vilket stabilt tekniskt erbjudande/funktionalitetskontrakt som behöver kunna konsumeras.
- **Produkt** är en möjlig marknadsrealisering eller del av realisering.

### Produkt kontra Plattform

- **Plattform** är produktneutral konceptuell gruppering av Plattformstjänster.
- **Produkt** är ett konkret marknadserbjudande.

Exempel:

- Kubernetes – Produkt/tekniskt byggblock om det modelleras som konkret marknads-/realiseringsreferens, inte automatiskt Plattform.
- Red Hat OpenShift – Produkt, inte automatiskt Plattform.
- Containerplattform – kan vara konceptuell Plattform när den grupperar ett stabilt tjänsteerbjudande oberoende av produkt.

### Kvalitetsfrågor

- Beskriver objektet **vad organisationen behöver** eller **vad marknaden erbjuder**?
- Skulle IT-stödet eller Plattformens syfte fortfarande vara meningsfullt om produkten byttes?
- Finns evidens för faktisk organisationsanvändning, eller endast marknadskapacitet?
- Är ett produktnamn felaktigt på väg att bli Plattform bara därför att produkten har bred funktionalitet?

EA Stödjare får inte skapa eller slå ihop Plattformar enbart utifrån produktöverlapp. Samma Produkt kan senare visa sig bidra till flera IT-stöd eller Plattformstjänster utan att dessa därför är samma arkitekturobjekt.

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

## Funktion med lokal identitet i v2

Funktion är fortsatt **inte en global EA-objekttyp**. Native v2 tillåter ett valfritt lokalt funktions-ID under IT-stöd, Plattformstjänst eller Plattform när projektet behöver stabil referens inom moderobjektet, exempelvis för produktjämförelse eller coverage. Lokal identitet får inte tolkas som att Funktionen kan få globala relationer.

