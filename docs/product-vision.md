# EA Stödjare – produktvision och scope

## 1. Dokumentets status

Detta dokument är den kanoniska produktbeskrivningen för **EA Stödjare v1** efter utvecklingsplanens steg 1.

Dokumentet ska användas som beslutspunkt vid senare utveckling: ett nytt önskemål hör till v1 om det ligger inom den produktvision och de avgränsningar som anges här. Ändringar av scope ska göras medvetet och dokumenteras, inte uppstå indirekt genom enskilda implementationer.

---

## 2. Produktvision

**EA Stödjare ska hjälpa användare att förstå, strukturera, analysera, utveckla och dokumentera enterprise architecture genom att kombinera organisationens eget underlag med generell arkitekturkunskap och, när det är relevant, aktuell och källredovisad omvärldsresearch.**

Produkten ska vara mer än en dokumentgenerator. Den ska kunna fungera som:

- **analysstöd** – förstå ostrukturerade eller fragmenterade underlag och identifiera arkitekturmässigt relevanta delar,
- **researchstöd** – komplettera underlaget med relevant extern kunskap, standarder, ramverk, praxis och jämförelseexempel,
- **modelleringsstöd** – föreslå, strukturera och kvalitetssäkra EA-objekt och relationer,
- **dokumentationsstöd** – generera konsistent dokumentation från en strukturerad och spårbar modell,
- **förvaltningsstöd** – hjälpa till att vidareutveckla och kvalitetssäkra modellen över tid.

EA Stödjare ska kunna hjälpa både när organisationen redan har en etablerad modell och när utgångsläget är ett ofullständigt underlag där en lämplig modell först behöver identifieras.

---

## 3. Produktens kärnproblem

Enterprise architecture-material finns ofta utspritt i strategier, riktlinjer, systemlistor, plattformsbeskrivningar, standarder, presentationer, tidigare arkitekturdokument och muntlig kunskap. Begrepp används dessutom ofta inkonsekvent och på olika abstraktionsnivåer.

Det leder bland annat till att:

- drivkrafter, mål och principer inte är tydligt spårbara till varandra,
- förmågor blandas ihop med processer, funktioner, system eller organisation,
- IT-stöd, plattformstjänster och plattformar blandas ihop,
- kataloger utvecklas separat och tappar konsistens,
- relationer mellan objekten endast finns i löptext eller i människors minne,
- modeller kan innehålla dubbletter, överlapp och luckor,
- externa rekommendationer blandas ihop med organisationens egna beslut,
- dokumentation snabbt blir inaktuell när samma information kopieras till flera format.

EA Stödjare ska angripa detta genom en gemensam strukturerad modell, tydlig proveniens och kontrollerade arbetsflöden för analys, research, modellering och dokumentgenerering.

---

## 4. Målgrupper

### 4.1 Primära målgrupper

#### Enterprise-arkitekter

Behöver stöd för att:

- ta fram och utveckla EA-modeller,
- analysera underlag,
- identifiera objekt och relationer,
- kvalitetssäkra terminologi och abstraktionsnivåer,
- identifiera luckor, dubbletter och överlapp,
- skapa spårbar dokumentation.

#### Verksamhetsarkitekter och närliggande arkitektroller

Behöver stöd för att koppla samman exempelvis:

- drivkrafter,
- mål,
- verksamhetsförmågor,
- IT-förmågor,
- principer,
- IT-stöd.

#### IT-arkitektur-/plattformsansvariga på enterprise-nivå

Behöver stöd för att beskriva och analysera:

- vilka IT-förmågor organisationen behöver,
- vilka plattformstjänster som erbjuds,
- vilka plattformar som realiserar tjänsterna,
- vilka standarder och principer som styr dem,
- vilka IT-stöd som använder erbjudandena.

### 4.2 Sekundära målgrupper

EA Stödjare ska även kunna vara användbar för:

- strategiskt ansvariga,
- portfölj- och verksamhetsutvecklingsroller,
- IT-ledning,
- domänarkitekter,
- förvaltnings- och produktansvariga,
- personer som behöver konsumera eller granska EA-dokumentation utan att själva vara enterprise-arkitekter.

Produkten ska däremot inte optimeras för detaljerat lösningsdesignarbete i v1.

---

## 5. Primära användningsfall

### UC-01 – Extrahera EA-objekt ur underlag

Användaren lämnar ett eller flera dokument eller andra informationskällor. EA Stödjare identifierar kandidater till exempelvis drivkrafter, mål, principer, förmågor, IT-stöd, plattformstjänster, plattformar och standarder.

Resultatet ska skilja mellan:

- explicit information i underlaget,
- härledda slutsatser,
- egna förslag.

### UC-02 – Ta fram en modell när den inte redan finns

Användaren beskriver en organisation, domän eller frågeställning och lämnar tillgängligt underlag. EA Stödjare hjälper till att undersöka hur en lämplig modell skulle kunna se ut genom att kombinera:

- användarens underlag,
- generell EA-kunskap,
- relevant aktuell omvärldsresearch,
- tydligt redovisade antaganden.

GPT:n ska kunna jämföra alternativa modellstrukturer och motivera ett rekommenderat förslag i stället för att behandla första hypotesen som facit.

### UC-03 – Granska en befintlig modell

EA Stödjare analyserar en befintlig EA-modell och identifierar exempelvis:

- dubbletter,
- överlapp,
- fel abstraktionsnivå,
- felklassificeringar,
- saknade relationer,
- möjliga luckor,
- inkonsekvent terminologi,
- objekt som saknar tillräcklig proveniens.

### UC-04 – Identifiera drivkrafter, mål och principer

EA Stödjare ska kunna analysera strategiskt material och hjälpa till att skilja på:

- vad som driver förändring,
- vilket resultat organisationen vill nå,
- vilka arkitekturprinciper som kan behövas som styrning.

Härledda eller föreslagna principer ska inte framställas som om de uttryckligen fanns i källan.

### UC-05 – Utveckla förmågemodeller

EA Stödjare ska kunna hjälpa till att identifiera, strukturera och granska:

- verksamhetsförmågor,
- IT-förmågor.

Det ska bland annat vara möjligt att uttrycka vilka IT-förmågor ett stödjande utvecklingsområde behöver tillhandahålla för att operativa utvecklingsområden ska kunna utveckla och förvalta IT-stöd.

### UC-06 – Kartlägga IT-stöd

EA Stödjare ska kunna beskriva vilka IT-stöd som stödjer vilka förmågor samt vilka funktioner ett IT-stöd tillhandahåller.

Funktion är i v1 ett underordnat attribut till relevanta objekt, inte en obligatorisk separat modellnivå mellan Förmåga och IT-stöd.

### UC-07 – Modellera plattformstjänster och plattformar

EA Stödjare ska hjälpa till att skilja mellan:

- **Plattformstjänst** – det tekniska erbjudande som konsumeras av exempelvis ett IT-stöd eller ett utvecklingsteam,
- **Plattform** – den tekniska grund eller realisering som möjliggör en eller flera plattformstjänster.

Både plattformstjänster och plattformar ska kunna beskriva vilka funktioner de tillhandahåller.

### UC-08 – Arbeta med standarder

EA Stödjare ska kunna identifiera och dokumentera standarder samt analysera vilka andra EA-objekt de styr, begränsar eller påverkar.

### UC-09 – Research och omvärldsjämförelse

När användarens underlag inte räcker ska EA Stödjare kunna söka efter relevanta externa källor och exempel, exempelvis:

- normer och standarder,
- etablerade EA-ramverk,
- myndighets- och branschrekommendationer,
- dokumenterade modeller från jämförbara organisationer,
- relevant teknisk eller organisatorisk praxis.

Extern information ska bedömas utifrån bland annat relevans, aktualitet, auktoritet och överförbarhet till användarens sammanhang.

### UC-10 – Generera arkitekturdokumentation

EA Stödjare ska kunna generera konsekventa vyer och dokument från den strukturerade modellen, i första hand med planerat stöd för:

- Markdown,
- Confluence markup,
- DOCX,
- PDF.

YAML-modellen är planerad som source of truth. Genererade dokument ska inte utvecklas som parallella, manuellt synkroniserade sanningskällor.

---

## 6. V1-scope – informationsmodell

### 6.1 Primära objekttyper

Följande är kärnobjekt i v1:

1. **Drivkraft**
2. **Mål**
3. **Princip**
4. **Förmåga**
   - verksamhetsförmåga
   - IT-förmåga
5. **IT-stöd**
6. **Plattformstjänst**
7. **Plattform**
8. **Standard**

### 6.2 Sekundära objekttyper

Följande ska beaktas i datamodellen men behöver inte få lika omfattande stöd i v1:

- **Lösningsmönster**
- **Referensarkitektur**

De hör hemma på enterprise-/styrningsnivå när de beskriver återanvändbara eller vägledande strukturer. De ska inte användas som en bakväg till detaljerad lösningsdesign.

### 6.3 Underordnad information

Följande hanteras initialt som attribut eller underobjekt i stället för fristående globala objekttyper:

- funktioner,
- beskrivning,
- status,
- ägare,
- taggar/kategorier,
- proveniens och källor,
- livscykelinformation.

Funktioner ska kunna beskrivas för minst:

- IT-stöd,
- Plattformstjänst,
- Plattform.

### 6.4 Grundläggande begreppsskillnad för funktion

En **Förmåga** beskriver vad organisationen eller IT behöver kunna åstadkomma.

En **Funktion** beskriver vad ett konkret IT-stöd, en plattformstjänst eller en plattform tillhandahåller.

I v1 ska modellen därför kunna uttrycka direkt:

```text
Förmåga -- stöds av --> IT-stöd
```

och IT-stödet beskriver separat sina funktioner.

Det undviker en obligatorisk kedja:

```text
Förmåga -> Funktion -> IT-stöd
```

som bedöms ge onödig modellkomplexitet i första versionen.

---

## 7. Övergripande relationsbild

V1 ska inte tvinga in alla objekt i en enda linjär kedja. Följande är en konceptuell utgångspunkt, inte ett slutligt relationsschema:

```text
Drivkraft
    |
    v
   Mål
    |
    v
 Princip
    |
    v
 Förmåga
    |
    | stöds av
    v
 IT-stöd
    |
    | använder
    v
 Plattformstjänst
    |
    | realiseras av
    v
 Plattform
```

Standarder kan styra eller begränsa flera nivåer.

IT-förmågor kan möjliggöras av en eller flera plattformstjänster. Mål kan påverka förmågor direkt. Principer kan styra flera objekttyper. Det slutliga relationsvokabuläret fastställs i utvecklingsplanens steg 4.

---

## 8. Research som kärnfunktion

Research är en del av produktens kärna, inte en framtida extrafunktion.

EA Stödjare ska kunna arbeta i tre huvudsakliga lägen.

### Läge A – Extraktion

Fråga:

> Vad säger vårt befintliga material?

Användarens underlag är primär källa. GPT:n kompletterar inte i onödan utan fokuserar på korrekt identifiering, klassificering och proveniens.

### Läge B – Analys och komplettering

Fråga:

> Vad verkar saknas, överlappa eller vara fel i vår modell?

GPT:n får kombinera:

- den befintliga modellen,
- generell EA-kunskap,
- relevant extern research.

Externa slutsatser ska markeras som externa eller föreslagna, inte blandas ihop med organisationens egna beslut.

### Läge C – Modellförslag

Fråga:

> Hur skulle en rimlig modell för den här organisationen eller domänen kunna se ut?

GPT:n ska då kunna:

1. analysera organisationens kontext och underlag,
2. identifiera kända drivkrafter och mål,
3. formulera vad som är oklart,
4. göra relevant research,
5. jämföra möjliga modellstrukturer,
6. föreslå en modell,
7. motivera förslaget,
8. redovisa externa källor och antaganden,
9. ange osäkerheter och alternativa tolkningar.

Produkten ska inte använda begreppet "best practice" som om en modell automatiskt vore universellt rätt. Extern praxis ska alltid bedömas utifrån kontext och överförbarhet.

---

## 9. Evidensdisciplin

EA Stödjare ska i senare modellsteg stödja en tydlig skillnad mellan åtminstone:

- **explicit** – uttryckligen belagt i användarens underlag,
- **derived** – härlett från användarens underlag,
- **proposed** – GPT:ns rekommendation eller modellförslag,
- **external** – baserat på extern källa eller omvärldsresearch.

Detta är en central produktprincip.

Exempel:

Om strategin anger att organisationen ska minska strategiskt leverantörsberoende får GPT:n identifiera detta som en drivkraft eller ett mål beroende på formulering och kontext.

GPT:n kan därefter föreslå en arkitekturprincip om utbytbarhet, men principen ska då markeras som **härledd/föreslagen**, inte som explicit beslutad av organisationen.

---

## 10. Planerad source of truth och output

### 10.1 Source of truth

Planen för v1 är att använda **YAML** som kanoniskt, maskinläsbart format för EA-modellen.

Det slutliga schemat fastställs i senare utvecklingssteg.

### 10.2 Genererade vyer

Från modellen ska dokumentation kunna genereras i flera format:

```text
YAML
 |
 +-- Markdown
 +-- Confluence markup
 +-- DOCX
 +-- PDF
```

Genererad Markdown, Confluence markup, DOCX och PDF ska vara representationer av modellen, inte alternativa sources of truth.

### 10.3 Visualisering

Automatisk visualisering ingår inte i v1.

Datamodellen och relationsmodellen ska däremot utformas så att framtida stöd för exempelvis:

- draw.io,
- Gliffy,
- ArchiMate,
- beroendediagram,
- förmågekartor

kan införas utan att kärninformationen behöver modelleras om.

---

## 11. Relation till Lärobokskaparen

EA Stödjare ska utvecklas som en **separat GPT**, inte som ytterligare en boktyp eller generell dokumentprofil i Lärobokskaparen.

Skälen är främst:

- EA Stödjare utgår från en modell av arkitekturobjekt och relationer snarare än kapitel,
- kvalitetskriterierna är semantiska och strukturella snarare än pedagogiska,
- research och evidens behöver kopplas till modellobjekt,
- EA-dokumentation är olika vyer över en gemensam modell,
- detaljerad bokpublicering såsom EPUB är inte central här.

EA Stödjare ska däremot **återanvända goda mekanismer och designprinciper** från Lärobokskaparen där de är generella, exempelvis potentiellt:

- versions- och revisionshantering,
- projektmanifest,
- integritetskontroll,
- projektstatus,
- kvalitetsgrindar,
- reproducerbar export,
- Builder Knowledge-struktur,
- validering och tester,
- GitHub Actions,
- releasepaketering.

Vilka delar som faktiskt ska återanvändas beslutas i steg 2.

---

## 12. Uttrycklig avgränsning mot lösningsarkitektur

EA Stödjare v1 ska arbeta på enterprise-/styrningsnivå och får beskriva relationer mellan exempelvis:

- förmågor,
- IT-stöd,
- plattformstjänster,
- plattformar,
- standarder,
- principer.

Den får exempelvis uttrycka att ett IT-stöd använder en containerplattformstjänst som realiseras av en viss plattform.

Den ska däremot inte i v1 ta ansvar för att designa den konkreta lösningen i detalj.

### Utanför scope

- komponentarkitektur,
- detaljerade API-kontrakt,
- detaljerad integrationsdesign,
- datamodell/databasschema på lösningsnivå,
- deploymenttopologi,
- nätverkstopologi,
- detaljerad säkerhetsdesign,
- sekvensdiagram,
- kod- eller implementationsteknik,
- produktkonfiguration på detaljnivå.

Om ett användarbehov huvudsakligen handlar om **hur en specifik lösning ska konstrueras**, snarare än **hur enterprise-arkitekturen ska förstås, struktureras eller styras**, ligger det utanför v1.

---

## 13. Scopebeslut – tumregel

Ett nytt önskemål hör normalt till EA Stödjare v1 om huvudfrågan är någon av följande:

- Vad driver förändringen?
- Vad vill organisationen uppnå?
- Vilka principer bör styra?
- Vad behöver verksamheten eller IT kunna?
- Vilka IT-stöd stödjer dessa förmågor?
- Vilka plattformstjänster behöver erbjudas?
- Vilka plattformar realiserar dessa erbjudanden?
- Vilka standarder styr eller begränsar detta?
- Hur hänger objekten ihop?
- Vad säger vårt underlag?
- Vad saknas eller överlappar?
- Hur skulle en rimlig modell för organisationen/domänen kunna se ut?
- Vad visar relevant omvärldsresearch?
- Hur dokumenterar och kvalitetssäkrar vi modellen?

Ett önskemål hör normalt **inte** till v1 om huvudfrågan är:

- exakt hur en specifik applikation ska designas,
- vilket API-kontrakt som ska implementeras,
- hur komponenter ska kommunicera i runtime,
- hur en specifik databas ska modelleras,
- hur nätverk, deployment eller teknisk säkerhetslösning ska konfigureras.

---

## 14. Produktprinciper för v1

### P-01 – Modell före dokument

Arkitekturinformation ska så långt det är praktiskt lagras strukturerat och dokumentation genereras från modellen.

### P-02 – Proveniens före tvärsäkerhet

Det ska vara tydligt vad som kommer från användarens material, vad som är härlett, vad som kommer från externa källor och vad GPT:n föreslår.

### P-03 – Research ska vara kontextmedveten

Extern praxis är jämförelsematerial och evidens, inte automatiskt facit.

### P-04 – Minsta nödvändiga metamodel

V1 ska innehålla de objekt som behövs för att ge verkligt EA-värde, men undvika att modellera hela EA-domänen från början.

### P-05 – Tydliga abstraktionsnivåer

GPT:n ska aktivt hjälpa användaren att skilja exempelvis förmåga från funktion och IT-stöd från plattformstjänst.

### P-06 – Lösningsdesign är en separat disciplin

V1 ska inte växa mot detaljerad lösningsarkitektur genom att successivt lägga till lösningsdesignobjekt.

### P-07 – Reproducerbara artefakter

Samma kanoniska modell ska kunna generera konsekventa dokument i flera format.

### P-08 – Iterativ förvaltning

EA Stödjare ska kunna vidareutveckla befintliga modeller säkert över tid, inte bara skapa engångsrapporter.

---

## 15. Exempel på frågor som ligger inom v1

- "Analysera den här strategin och identifiera drivkrafter och mål."
- "Föreslå vilka arkitekturprinciper som följer av dessa mål och markera vad som är härlett."
- "Granska vår förmågekatalog och hitta överlapp eller saknade områden."
- "Vilka IT-förmågor behöver ett stödjande IT-område tillhandahålla för att operativa utvecklingsområden ska kunna utveckla IT-stöd?"
- "Utifrån vårt material och relevant omvärldsresearch, föreslå hur vår IT-förmågemodell skulle kunna struktureras."
- "Är detta en plattform, plattformstjänst eller ett IT-stöd? Motivera klassificeringen."
- "Vilka funktioner bör beskrivas för den här plattformstjänsten?"
- "Vilka standarder verkar saknas i vår modell?"
- "Generera en Markdown-katalog över våra principer från modellen."

---

## 16. Exempel på frågor som ligger utanför v1

- "Designa REST-API:t för den här tjänsten."
- "Skapa ett Kubernetes deployment manifest för systemet."
- "Ta fram exakt nätverkssegmentering och brandväggsregler."
- "Designa databasschemat för vår ordertjänst."
- "Ta fram sekvensdiagram för transaktionsflödet mellan mikrotjänsterna."

EA Stödjare kan i sådana fall hjälpa till att identifiera att behovet hör till lösningsarkitektur eller teknisk design, men själva detaljerade designarbetet ingår inte i v1.

---

## 17. Definition of Done för steg 1

Steg 1 är genomfört när följande är tydligt definierat:

- produktens syfte,
- målgrupper,
- huvudsakliga användningsfall,
- v1-scope,
- primära och sekundära EA-objekt,
- funktionen för research och modellförslag,
- planerad source of truth och dokumentgenerering,
- relationen till Lärobokskaparen,
- uttrycklig gräns mot lösningsarkitektur,
- en praktisk tumregel för att bedöma framtida scopeönskemål.

Detta dokument uppfyller dessa kriterier och utgör därför beslutspunkt för fortsatt utveckling i steg 2.
