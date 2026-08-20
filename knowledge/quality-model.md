# Kvalitetskontroll för hela EA-modellen

## Syfte

Detta dokument definierar hur EA Stödjare ska kvalitetsgranska **hela den kanoniska EA-modellen som ett sammanhängande system**. Kontrollen kompletterar kvalitetskontrollen för enskilda objekt i `knowledge/quality-object.md`.

En modell kan bestå av individuellt välformulerade objekt och ändå vara svag som helhet. Helhetskontrollen ska därför hitta problem som endast blir synliga när objekt, relationer, proveniens och modellens täckning analyseras tillsammans.

Kontrollen ersätter inte strukturell schemavalidering och ska inte framtvinga relationer eller objekt som saknar evidens.

## Grundprinciper

1. **Helhet före mängd.** Fler objekt innebär inte automatiskt en bättre EA-modell.
2. **Evidens före grafkomplettering.** Saknade länkar får inte fyllas i endast för att göra modellen mer sammanhängande.
3. **Approved kräver högre sammanhang än candidate.** Preliminära kandidater får vara partiellt anslutna medan godkända objekt förväntas ha ett begripligt sammanhang.
4. **Täckning bedöms mot modellens uttalade scope.** En modell ska inte kritiseras för att inte beskriva sådant som ligger utanför dess avgränsning.
5. **Semantiska luckor skiljs från dataluckor.** En verklig arkitekturlucka är inte samma sak som att underlaget ännu inte dokumenterar relationen.
6. **Ingen falsk symmetri.** Alla objekttyper behöver inte förekomma i samma antal eller ha samma relationsgrad.
7. **Spårbarhet ska kunna förklaras, inte bara räknas.** En kedja är värdefull först när relationerna har relevant semantik och proveniens.
8. **Kvalitetskontroll är diagnostik.** Den ska identifiera risker, mönster och frågor – inte automatiskt fatta arkitekturbeslut.

## Allvarlighetsnivåer

### ERROR

Ett fel som gör modellen strukturellt eller semantiskt motsägelsefull, eller som innebär att centrala godkända delar inte kan användas tillförlitligt.

Exempel:

- relation refererar till ett objekt som inte finns,
- `derived_from` bildar en härledningscykel,
- två godkända objekt har samma ID,
- en lagrad relation bryter mot relationsmodellen,
- en godkänd relation har source/target som inte är tillgängliga i aktuell modell.

### WARNING

En tydlig kvalitetsrisk som bör granskas men som inte nödvändigtvis gör modellen ogiltig.

Exempel:

- godkända mål saknar koppling till drivkrafter eller förmågor trots att sådan spårbarhet förväntas,
- godkända IT-stöd saknar känd koppling till förmågor,
- plattformstjänster saknar känd konsument- eller realiseringskontext,
- flera objekt verkar överlappa kraftigt,
- en del av modellen är oproportionerligt tät eller isolerad.

### INFO

Observation som kan förbättra modellen eller hjälpa fortsatt analys utan att indikera ett direkt kvalitetsproblem.

Exempel:

- ett område har betydligt lägre dokumentationstäthet än andra,
- vissa candidates saknar relationer,
- fler tvärgående standardkopplingar kan vara värda att undersöka.

## Resultatnivåer

Helhetskontrollen rapporterar:

- **GODKÄND** – inga ERROR och inga materiella WARNING.
- **GODKÄND MED VARNINGAR** – inga ERROR men en eller flera WARNING.
- **BLOCKERAD** – minst ett ERROR.

Resultatet ändrar inte automatiskt objektstatus eller modellens livscykelstatus.

## Förutsättningar före semantisk granskning

Innan helhetskontrollen genomförs ska EA Stödjare säkerställa att:

1. projektmanifestet kan läsas,
2. modellfilerna kan parsas,
3. ID:n kan indexeras,
4. relationer kan läsas,
5. källreferenser kan lösas i den utsträckning modellen kräver.

Om dessa förutsättningar inte uppfylls ska relevanta strukturella fel rapporteras och beroende semantiska kontroller markeras som **ej bedömbara**, inte gissas.

# Kontrollområden

## 1. Referentiell och semantisk integritet

### QM-INT-001 – Unika objekt-ID:n

**ERROR** om samma objekt-ID förekommer mer än en gång i den samlade modellen.

### QM-INT-002 – Relationernas endpoints finns

**ERROR** om `source` eller `target` i en relation inte motsvarar ett känt objekt.

### QM-INT-003 – Relationstyp och source/target är tillåtna

**ERROR** om en lagrad relation inte följer `schemas/relations.yaml`.

### QM-INT-004 – Inga dubbellagrade identiska relationer

**WARNING** om samma `(source, relation, target)` lagras flera gånger. Separat evidens ska i normalfallet samlas i samma relationspost i stället för att duplicera relationen.

### QM-INT-005 – Ingen lagrad invers dubblett

**WARNING** om två relationer endast uttrycker varandras presentationsinvers och därmed dubbellagrar samma semantik i strid med relationsmodellen.

### QM-INT-006 – Härledningsgraf utan cykler

**ERROR** om `derived_from` bildar en cykel. Ett objekt eller en relation får inte direkt eller indirekt härledas från sig självt.

### QM-INT-007 – Källreferenser kan lösas

**ERROR** för obligatorisk/kärnproveniens på godkända objekt eller relationer om refererad source-ID saknas.

**WARNING** för motsvarande brist på candidates när osäkerheten är tydligt deklarerad.

## 2. Orphans och kontextlösa objekt

Ett orphan definieras här som ett objekt utan relevanta in- eller utgående EA-relationer. Orphan är **inte automatiskt fel**.

### QM-ORP-001 – Godkänt mål utan arkitekturkontext

**WARNING** om ett `approved` Mål saknar relation till både motiverande Drivkraft och realiserande/stödjande arkitekturkontext trots att modellen är avsedd att beskriva strategi-till-arkitektur-spårbarhet.

### QM-ORP-002 – Godkänd förmåga utan relevant sammanhang

**WARNING** om en `approved` Förmåga saknar alla relevanta relationer till mål, andra förmågor, IT-stöd eller plattformstjänster och det inte finns dokumenterat skäl.

### QM-ORP-003 – Godkänt IT-stöd utan förmågekoppling

**WARNING** om ett `approved` IT-stöd saknar relation som visar vilken Förmåga det stödjer och modellens scope omfattar förmåge-/IT-stödsspårbarhet.

### QM-ORP-004 – Godkänd plattformstjänst utan erbjudande-/realiseringskontext

**WARNING** om en `approved` Plattformstjänst varken har känd koppling till IT-förmåga/IT-stöd eller till realiserande Plattform.

### QM-ORP-005 – Godkänd plattform utan tjänstekontext

**WARNING** om en `approved` Plattform saknar relation till Plattformstjänst eller annan relevant användnings-/realiseringskontext inom modellens scope.

### QM-ORP-006 – Candidate utan relationer

**INFO** om ett `candidate` objekt är orphan. Detta kan vara legitimt under analys men bör synliggöras inför fortsatt arbete.

### QM-ORP-007 – Styrande objekt utan faktisk styrkoppling

**WARNING** om en `approved` Princip eller Standard saknar någon relation som visar vad den styr eller begränsar, när modellens scope omfattar sådan spårbarhet.

## 3. Strategisk spårbarhet

Kontrollerna ska endast appliceras när modellens scope faktiskt inkluderar motsvarande nivåer.

### QM-TRC-001 – Drivkrafter till mål

**WARNING** om betydande `approved` Drivkrafter inte påverkar något Mål och ingen annan motiverad struktur för deras effekt finns.

### QM-TRC-002 – Mål till förmågor

**WARNING** om ett `approved` Mål saknar spårbar väg till någon Förmåga när modellen används för att förklara vilka förmågor som behöver utvecklas för att nå målen.

En spårbar väg får bestå av flera semantiskt relevanta relationer. Enbart `related_to` ska inte räknas som stark spårbarhet.

### QM-TRC-003 – Förmåga till IT-stöd

**INFO** eller **WARNING** beroende på scope om en verksamhetsförmåga saknar känt IT-stöd. Detta är inte automatiskt en arkitekturlucka; förmågan kan vara manuell eller underlaget ofullständigt.

### QM-TRC-004 – IT-förmåga till plattformstjänst

**WARNING** om en `approved` IT-förmåga som enligt modellens scope ska tillhandahållas av ett stödjande IT-område saknar känd realisering/möjliggörande Plattformstjänst och ingen annan realiseringsform dokumenterats.

### QM-TRC-005 – IT-stöd till plattformstjänster

**INFO** om ett IT-stöd saknar kända använda Plattformstjänster. **WARNING** endast om modellens scope uttryckligen ska beskriva sådan plattformsanvändning och objektet är `approved`.

### QM-TRC-006 – Plattformstjänst till plattform

**WARNING** om en `approved` Plattformstjänst saknar känd realisering av Plattform när modellens scope omfattar teknisk realisering.

### QM-TRC-007 – Svaga spårbarhetskedjor

**WARNING** om en kritisk spårbarhetskedja huvudsakligen består av `related_to` trots att mer precisa relationer borde kunna fastställas från tillgängligt underlag.

## 4. Dubbletter, alias och överlapp

### QM-DUP-001 – Sannolik dubblett

**WARNING** om två objekt av samma eller närliggande typ har mycket liknande namn/alias och beskrivningar och förefaller representera samma sak.

### QM-DUP-002 – Semantiskt överlapp

**WARNING** om två objekt överlappar så starkt att deras scope inte går att skilja på ett meningsfullt sätt.

EA Stödjare ska föreslå möjliga åtgärder – exempelvis alias, sammanslagning, tydligare scope eller hierarkisk avgränsning – men inte automatiskt slå ihop objekten.

### QM-DUP-003 – Samma namn, olika semantik

**WARNING** om samma eller nästan samma namn används för olika objekttyper utan tydlig disambiguering.

Exempel: både en IT-förmåga och Plattformstjänst heter `Integration` utan tillräckligt särskiljande beskrivning.

### QM-DUP-004 – Dubbletter i funktioner

**INFO** eller **WARNING** om funktionslistor inom eller mellan närliggande IT-stöd/Plattformstjänster antyder oavsiktlig överlappning som bör analyseras.

Liknande funktioner på olika objekt är inte i sig fel.

## 5. Konsistens och motsägelser

### QM-CON-001 – Motstridig livscykel

**ERROR** om relationer behandlar ett `retired` objekt som aktuell obligatorisk realisering utan dokumenterad övergång eller historisk kontext.

**WARNING** vid `deprecated` objekt som fortfarande är centrala beroenden utan dokumenterad plan/kontext.

### QM-CON-002 – Motsägande klassificering

**WARNING** om relationer och beskrivningar systematiskt antyder en annan objekttyp än den lagrade typen, även om objektet individuellt inte redan fångats av objektkontrollen.

### QM-CON-003 – Motsägande proveniens

**WARNING** om olika evidensposter ger materiellt motstridiga påståenden och konflikten inte är markerad eller hanterad.

### QM-CON-004 – Approved byggt på olöst svag grund

**WARNING** eller **ERROR** beroende på betydelse om ett `approved` objekt eller en `approved` relation huvudsakligen bygger på osäkra `proposed`/svagt överförbara externa antaganden utan dokumenterad beslutspunkt.

### QM-CON-005 – Föräldralösa beroenden till borttagna objekt

**ERROR** om aktuell modell innehåller relationer till borttagna objekt. Historik ska hanteras via status/revisionshistorik, inte trasiga aktuella referenser.

## 6. Täckning och modellens scope

Täckning får bara bedömas mot dokumenterat scope. Avsaknad av en objekttyp i en avgränsad modell är inte ett fel i sig.

### QM-COV-001 – Scope saknas eller är oklart

**WARNING** om modellen granskas för täckning men projektets avgränsning inte är tillräckligt tydlig för att avgöra vad som förväntas ingå.

### QM-COV-002 – Uttalat scope saknar representerade kärnområden

**WARNING** om ett explicit scope säger att ett område ska omfattas men modellen saknar objekt eller relationer som rimligen krävs för att beskriva området.

### QM-COV-003 – Dokumentationslucka kontra arkitekturlucka

**INFO** när modellen indikerar en möjlig lucka men evidensen inte räcker för att avgöra om den är verklig. Rapporten ska uttryckligen ange `dokumentationslucka`, `möjlig arkitekturlucka` eller `bekräftad arkitekturlucka` – inte blanda begreppen.

### QM-COV-004 – Kritiska områden med låg evidenstäckning

**WARNING** om en central del av modellen har många `approved` påståenden men låg eller svag provenienstäckning.

### QM-COV-005 – Externa förslag dominerar intern modell

**WARNING** om ett område i hög grad består av organisationsspecifika `proposed` objekt som främst stöds av externa exempel och ännu saknar intern validering.

## 7. Struktur, täthet och beroendemönster

Dessa kontroller är heuristiska och får inte användas som absoluta arkitekturregler.

### QM-GRF-001 – Extremt tätt objekt

**INFO** eller **WARNING** om ett objekt har avsevärt fler relationer än liknande objekt och därmed kan vara för brett, fungera som ospecificerad hubb eller ha överanvänt `related_to`.

### QM-GRF-002 – Isolerad delgraf

**INFO** om modellen innehåller en sammanhängande delgraf som saknar relation till övrig modell. **WARNING** om delgrafen enligt scope borde vara integrerad med resten.

### QM-GRF-003 – Överanvändning av `related_to`

**WARNING** om `related_to` används i sådan omfattning att relationssemantiken blir otydlig och mer precisa relationer borde kunna användas.

### QM-GRF-004 – Beroendecykel som kräver granskning

**INFO** eller **WARNING** om `depends_on` bildar cykler. Till skillnad från `derived_from` är detta inte automatiskt fel, men kan indikera stark koppling eller svår förändringsbarhet.

### QM-GRF-005 – Flaskhals-/single-point-of-dependency-kandidat

**INFO** om ett IT-stöd, en Plattformstjänst eller Plattform är central beroendepunkt för många andra objekt. Rapporten ska beskriva detta som analyskandidat, inte som risk utan ytterligare underlag.

## 8. Principer och standarder som faktisk styrning

### QM-GOV-001 – Princip utan tillämpning

**WARNING** om en `approved` Princip inte styr någon relevant del av modellen och detta inte är medvetet dokumenterat.

### QM-GOV-002 – Standard utan tillämpning

**WARNING** om en `approved` Standard inte styr eller begränsar något relevant objekt inom aktuellt scope.

### QM-GOV-003 – Styrning utan motivering

**WARNING** om omfattande `governed_by`/`constrains`-relationer saknar proveniens eller motivering när de representerar organisationsspecifika krav.

### QM-GOV-004 – Överlappande eller motstridiga styrsignaler

**WARNING** om flera Principer/Standarder verkar ge motstridiga krav på samma objekt och konflikten inte är dokumenterad.

## 9. Proveniens på modellnivå

### QM-PRV-001 – Approved utan tillräcklig evidenstäckning

**WARNING** eller **ERROR** enligt objekt-/relationsregler om centrala godkända objekt eller relationer saknar adekvat proveniens.

### QM-PRV-002 – Externa källor utan överförbarhetsbedömning

**WARNING** när externa källor används för organisationsspecifika modellförslag men deras relevans/överförbarhet inte har bedömts där detta är materiellt.

### QM-PRV-003 – Förslag har blivit omarkerad intern sanning

**ERROR** om material som endast kan spåras till GPT-förslag eller externa jämförelseexempel har klassats som `explicit` intern evidens.

### QM-PRV-004 – Härledningskedja går inte att följa

**WARNING** om `derived` objekt eller relationer har `derived_from`-referenser som är så ofullständiga att härledningen inte går att förklara.

## 10. Sekundära objekttyper

Lösningsmönster och Referensarkitekturer är sekundära i v1 och ska inte krävas för att modellen ska vara komplett.

### QM-SEC-001 – Lösningsmönster utan relevanskoppling

**INFO** eller **WARNING** om ett `approved` Lösningsmönster saknar relation till det område som det ska vägleda inom modellens scope.

### QM-SEC-002 – Referensarkitektur utan relevanskoppling

**INFO** eller **WARNING** om en `approved` Referensarkitektur saknar relation till relevanta förmågor, plattformstjänster, standarder eller mönster när sådana samband ingår i scope.

# Täckningsprofiler

Helhetskontrollen bör använda en **täckningsprofil** för att undvika generiska krav som inte passar modellens syfte.

V1 definierar fyra logiska profiler:

## `catalog`

Fokus på katalogkvalitet, dubbletter, normalisering, proveniens och objektens interna kvalitet. Relationstäckning är huvudsakligen INFO om den inte uttryckligen ingår i scope.

## `strategy_to_capability`

Fokus på:

- Drivkraft → Mål,
- Mål → Förmåga,
- relevanta Principer.

IT-stöd och plattformslager behöver inte finnas.

## `capability_to_it`

Fokus på:

- Förmåga → IT-stöd,
- IT-förmåga → Plattformstjänst,
- IT-stöd → Plattformstjänst där relevant.

## `full_ea_v1`

Fokus på sammanhängande spårbarhet över alla primära v1-objekttyper som faktiskt ligger inom projektets scope.

En kontrollrapport ska alltid ange vald profil och eventuella scopeundantag.

# Heuristik för dubbletter och överlapp

EA Stödjare får använda följande signaler tillsammans:

- normaliserat namn,
- alias,
- beskrivningens semantiska likhet,
- samma capability_type eller objekttyp,
- liknande relationer,
- liknande funktioner,
- samma scope/ägare/domän,
- gemensam proveniens.

Ingen enskild signal räcker för automatisk sammanslagning.

# Granskningens arbetsordning

EA Stödjare ska normalt granska modellen i följande ordning:

1. välj scope och täckningsprofil,
2. verifiera referentiell integritet,
3. sammanställ objekt- och relationsstatistik,
4. hitta orphans och isolerade delgrafer,
5. analysera strategisk spårbarhet,
6. analysera dubbletter och överlapp,
7. analysera motsägelser och livscykel,
8. analysera styrning via Principer/Standarder,
9. analysera proveniens på modellnivå,
10. analysera grafmönster och beroenden heuristiskt,
11. skilj dokumentationsluckor från möjliga/verifierade arkitekturluckor,
12. prioritera åtgärder.

# Rapportformat

En helhetsrapport bör minst innehålla:

```text
Modell: <namn/revision>
Profil: <catalog | strategy_to_capability | capability_to_it | full_ea_v1>
Scope: <kort sammanfattning>
Resultat: GODKÄND | GODKÄND MED VARNINGAR | BLOCKERAD

Sammanfattning
- Objekt: N
- Relationer: N
- ERROR: N
- WARNING: N
- INFO: N

Blockerande fel
- [QM-...] ...

Viktigaste kvalitetsrisker
- [QM-...] ...

Spårbarhet
- ...

Möjliga dubbletter/överlapp
- ...

Luckor
- Dokumentationsluckor: ...
- Möjliga arkitekturluckor: ...
- Bekräftade arkitekturluckor: ...

Proveniens/evidens
- ...

Prioriterade åtgärder
1. ...
2. ...

Ej bedömbart
- ...
```

## Prioritering

Rapporten ska prioritera:

1. ERROR,
2. WARNING som påverkar centrala spårbarhetskedjor eller många objekt,
3. möjliga dubbletter/överlappar som påverkar modellens begriplighet,
4. evidensproblem,
5. INFO/strukturförbättringar.

EA Stödjare ska undvika att lämna en lång osorterad lista med alla tänkbara observationer.

# Automatiserbart kontra LLM-bedömt

## Lämpligt för deterministisk validering

- unika ID:n,
- brutna referenser,
- tillåtna relationstyper/source-target,
- identiska relationsdubbletter,
- `derived_from`-cykler,
- saknade source-ID:n,
- orphan-statistik,
- relationsgrad,
- isolerade delgrafer,
- `depends_on`-cykler,
- andel `related_to`.

## Kräver normalt semantisk LLM-bedömning

- verklig dubblett kontra legitimt närliggande objekt,
- för bred/smal modellering,
- motsägande betydelse,
- om ett mål rimligen borde ha en förmågekoppling,
- om extern praxis är överförbar,
- om en lucka är dokumentationslucka eller verklig arkitekturlucka,
- om principer/standarder faktiskt påverkar beslut,
- om grafens täthet tyder på fel abstraktionsnivå.

Deterministiska mätvärden får inte ensamma översättas till semantiska slutsatser.

# Definition of Done för helhetsgranskning

En helhetsgranskning är komplett när:

- scope och profil är explicit angivna,
- alla ERROR-kontroller som är möjliga att köra har körts,
- relevanta WARNING-kontroller har bedömts,
- orphans och dubblettkandidater har analyserats,
- relevanta spårbarhetskedjor har bedömts,
- proveniens har bedömts på modellnivå,
- luckor har klassificerats som dokumentationslucka/möjlig/bekräftad arkitekturlucka,
- ej bedömbara områden redovisas,
- prioriterade nästa åtgärder ges,
- ingen modelländring görs automatiskt enbart på grund av kvalitetsrapporten.
