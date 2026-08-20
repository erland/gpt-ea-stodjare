# Arbetsflöde för extraktion ur underlag

## 1. Syfte

Detta arbetsflöde styr hur EA Stödjare analyserar dokument, tabeller, presentationer, befintliga modeller och andra underlag för att identifiera kandidater till EA-objekt och relationer.

Målet är inte att maximera antalet objekt. Målet är att skapa en **spårbar, normaliserad och semantiskt hållbar modell** där användaren kan se vad underlaget faktiskt säger, vad som har härletts och vad EA Stödjare själv föreslår.

Arbetsflödet ska användas innan organisationsspecifikt innehåll förs in i den kanoniska YAML-modellen.

## 2. Grundprinciper

1. **Underlag före tolkning.** Börja med vad källan faktiskt uttrycker.
2. **Kandidat före kanon.** Identifierade begrepp behandlas först som kandidater.
3. **Klassificera semantiskt.** Rubrik eller ordval i källan avgör inte objekttypen ensam.
4. **Separera evidensnivåer.** `explicit`, `derived`, `proposed` och `external` får inte blandas ihop.
5. **Normalisera utan att radera betydelse.** Bevara källans formulering i evidensen även när objektets namn normaliseras.
6. **Skapa inte objekt för varje substantiv.** Ett begrepp blir EA-objekt först när det uppfyller metamodelens definition och fyller en meningsfull roll i modellen.
7. **Osäkerhet ska synas.** Tvinga inte fram klassificering eller relation när underlaget är otillräckligt.
8. **Relationer kräver eget belägg.** Att två objekt förekommer nära varandra innebär inte automatiskt en relation.
9. **Modellen är source of truth först efter införande.** Analysanteckningar och kandidater är arbetsmaterial.
10. **Minsta nödvändiga ändring.** Vid uppdatering av en befintlig modell ska endast motiverade objekt och relationer ändras.

## 3. Indata

Arbetsflödet kan användas på exempelvis:

- strategi och verksamhetsplan,
- styrande dokument,
- arkitekturprinciper,
- förmågekataloger,
- system- och applikationslistor,
- plattformsbeskrivningar,
- standardkataloger,
- organisationsbeskrivningar,
- beslutsunderlag,
- rapporter och utredningar,
- kalkylblad och tabeller,
- tidigare arkitekturdokumentation.

För varje källa bör så långt möjligt följande registreras innan extraktion:

- titel eller identifierare,
- version/datum,
- källa/ägare,
- typ av dokument,
- analysens omfattning,
- om källan är intern eller extern,
- eventuell avgränsning eller känd osäkerhet.

## 4. Arbetsfaser

### Fas 0 – Förbered analysen

Fastställ:

- vilket underlag som ska analyseras,
- vilket modellområde analysen gäller,
- om en befintlig EA-modell finns,
- om uppgiften är ren extraktion eller även får innehålla härledning och förslag,
- vilka objekttyper som är relevanta för uppgiften.

Om användaren exempelvis endast ber om principer ska EA Stödjare inte automatiskt fylla hela modellen med förmågor, IT-stöd och plattformar.

### Fas 1 – Inventera underlaget

Skapa en mental eller explicit källinventering innan objekt extraheras.

Bedöm för varje källa:

- syfte,
- auktoritet,
- aktualitet,
- täckning,
- eventuell motsägelse mot andra källor,
- om innehållet beskriver nuläge, målläge, krav eller rekommendation.

Vid flera källor ska de inte slås ihop till en anonym gemensam textmassa. Proveniens måste kunna bibehållas.

### Fas 2 – Identifiera explicita kandidater

Leta först efter påståenden som direkt beskriver ett objekt enligt metamodelen.

Exempel:

> "Organisationen ska kunna dela information digitalt med externa aktörer."

Kan ge en explicit kandidat till en förmåga om formuleringen i sammanhanget uttrycker vad organisationen behöver kunna åstadkomma.

För varje kandidat noteras minst:

- arbets-ID eller kandidat-ID,
- källans formulering,
- källreferens,
- preliminär objekttyp,
- kort motivering.

Sätt provenienstyp `explicit` endast om själva objektpåståendet stöds direkt av källan. Att ordet "förmåga" förekommer är varken nödvändigt eller tillräckligt.

### Fas 3 – Klassificera kandidater

Klassificera mot `docs/metamodel.md` och `knowledge/classification-guide.md` när den senare finns.

Ställ framför allt följande frågor:

- Är detta något som **driver förändring**? → Drivkraft.
- Är detta ett **önskat resultat/tillstånd**? → Mål.
- Är detta en **styrande regel för arkitekturbeslut**? → Princip.
- Är detta något organisationen eller IT **behöver kunna åstadkomma**? → Förmåga.
- Är detta ett **konkret informationssystem/applikationsstöd**? → IT-stöd.
- Är detta ett **konsumerbart tekniskt erbjudande**? → Plattformstjänst.
- Är detta den **tekniska grund/realisering** som tjänster eller IT-stöd bygger på? → Plattform.
- Är detta en **normativ teknisk eller arkitekturell regel/specifikation**? → Standard.
- Är detta ett **återanvändbart sätt att lösa en återkommande problemtyp**? → Lösningsmönster.
- Är detta en **generell arkitekturstruktur för ett område**? → Referensarkitektur.

Om två klassificeringar är rimliga ska kandidaten markeras som osäker i stället för att döljas bakom ett tvärsäkert val.

### Fas 4 – Identifiera härledda kandidater

Efter de explicita kandidaterna får EA Stödjare identifiera sådant som kan **härledas** från en eller flera explicit belagda uppgifter.

Exempel:

- Källa A säger att organisationen ska erbjuda självbetjäning dygnet runt.
- Källa B säger att manuella handläggningsmoment ska minska.
- En möjlig härledd drivkraft eller förmåga kan då identifieras, men ska inte märkas `explicit` om den inte själv uttrycks i underlaget.

För en `derived` kandidat krävs:

- minst ett konkret `derived_from`,
- en begriplig härledningsmotivering,
- confidence enligt proveniensmodellen,
- ingen extern källa som enda grund. Om slutsatsen huvudsakligen bygger på omvärldsresearch är den normalt `proposed`, med extern evidens som stöd.

### Fas 5 – Identifiera relationer

Relationer extraheras efter att objekten har fått preliminär identitet.

För varje relation:

1. välj relationstyp enligt `docs/relations.md`,
2. kontrollera tillåten source/target-kombination,
3. dokumentera relationens eget evidens,
4. undvik att lagra en implicit invers relation separat,
5. använd `related_to` endast när en mer precis relation inte kan beläggas.

Exempel:

> "Ärendehanteringssystemet använder den centrala identitetstjänsten för autentisering."

kan ge en explicit `uses`-relation mellan IT-stödet och plattformstjänsten om båda objekten är korrekt klassificerade.

### Fas 6 – Markera osäkerhet och konflikter

Markera bland annat:

- tveksam objekttyp,
- oklar avgränsning,
- oklar relation,
- motsägande källor,
- för gammalt underlag,
- begrepp som används olika i olika dokument,
- möjlig dubblett.

EA Stödjare ska hellre rapportera "behöver verifieras" än skapa falsk precision.

Fullständig konflikthantering införs i steg 20, men arbetsflödet ska redan nu bevara konflikten.

### Fas 7 – Normalisera

Normalisering sker **efter** identifiering och klassificering.

Kontrollera:

- singular/plural,
- konsekvent språk,
- förkortningar och alias,
- om flera källor avser samma objekt,
- om ett namn beskriver organisation, process, teknik eller faktisk objekttyp,
- om namnet ligger på rätt abstraktionsnivå.

Normalisering får ändra modellnamnet men inte skriva om historien. Ursprunglig formulering behålls via källreferens/evidens.

Exempel:

- "IAM", "Identitetshantering" och "Identity Management" kan efter analys visa sig vara samma objekt eller tre olika nivåer. De får inte slås ihop enbart på språklig likhet.

### Fas 8 – Dubblett- och överlappskontroll

Innan nya objekt föreslås ska kandidater jämföras med:

- befintliga objekt i modellen,
- andra kandidater i samma analys,
- kända alias.

Resultatet för varje kandidat bör vara ett av:

- `new` – nytt objekt,
- `match` – motsvarar befintligt objekt,
- `update` – befintligt objekt bör kompletteras,
- `possible_duplicate` – kräver bedömning,
- `discard` – bör inte bli eget objekt.

### Fas 9 – Föreslå kompletterande objekt

Först efter extraktion och härledning får EA Stödjare föreslå objekt som inte följer direkt ur underlaget.

Sådana objekt ska:

- märkas `proposed`,
- ha en tydlig motivering,
- ange vilket problem eller vilken lucka de adresserar,
- vid behov stödjas av extern research,
- inte beskrivas som fastställda organisationsobjekt.

Extern research som krävs för kvalificerade modellförslag styrs närmare av steg 10.

### Fas 10 – Presentera analysresultat

Vid större analyser bör resultatet presenteras innan införande i kanonisk modell.

Lämplig struktur:

1. analyserade källor,
2. explicita kandidater,
3. härledda kandidater,
4. föreslagna kompletteringar,
5. nya eller ändrade relationer,
6. möjliga dubbletter/överlapp,
7. osäkerheter och konflikter,
8. föreslagna modelländringar.

För små, entydiga ändringar i ett redan etablerat projekt kan uppdatering ske direkt om användarens instruktion tydligt innebär att modellen ska ändras och inga riskfaktorer finns.

## 5. När ändringar får bli kanoniska

### Direkt införande kan vara rimligt när

- objektet är tydligt explicit belagt,
- klassificeringen är entydig,
- ingen befintlig modellkonflikt finns,
- ändringen ligger inom användarens uttryckliga uppdrag,
- relationerna följer relationsmodellen.

### Presentera före införande när

- många objekt tillkommer samtidigt,
- modellen omstruktureras,
- befintliga objekt föreslås slås ihop eller tas bort,
- klassificeringen är osäker,
- flera källor motsäger varandra,
- slutsatsen är huvudsakligen `derived` eller `proposed`,
- externa exempel riskerar att förändra organisationens modellprinciper.

När projektet i en senare version får mer detaljerade godkännandestatusar ska dessa regler integreras med dem.

## 6. Proveniensregler vid extraktion

### Explicit

Använd `explicit` när påståendet kan återfinnas direkt i en identifierad källa.

Minimikrav:

- `source_id`,
- så exakt locator som källtypen medger,
- kort evidenssammanfattning.

### Derived

Använd `derived` när slutsatsen följer genom analys av ett eller flera belagda objekt/påståenden.

Minimikrav:

- `derived_from`,
- `reasoning_summary`,
- `confidence`.

### Proposed

Använd `proposed` när EA Stödjare rekommenderar något som inte kan behandlas som en slutsats ur organisationens underlag.

Minimikrav:

- `reasoning_summary`,
- vilket gap eller behov förslaget adresserar,
- `confidence` där det är meningsfullt.

### External

Använd `external` för fakta eller objekt som faktiskt beskriver den externa källans värld, exempelvis en extern standard eller referensmodell.

Använd **inte** `external` för ett organisationsspecifikt förslag bara för att förslaget inspirerats av externa källor. Det organisationsspecifika objektet är då normalt `proposed`, med de externa källorna som stödjande evidens.

## 7. Klassificeringssäkerhet

Använd kvalitativ confidence från proveniensmodellen:

- `high` – starkt belägg och liten rimlig klassificeringsosäkerhet,
- `medium` – rimlig tolkning men alternativ finns,
- `low` – betydande osäkerhet eller bristande underlag.

Confidence är inte en matematisk sannolikhet och ska inte användas för att dölja en konkret konflikt.

## 8. Extraktionsjournal i arbetsmaterial

Vid komplex analys är följande arbetsformat lämpligt innan YAML uppdateras:

| Kandidat | Föreslagen typ | Evidens | Proveniens | Modellutfall | Kommentar |
|---|---|---|---|---|---|
| K-001 | Förmåga/IT | SRC-001 §4 | explicit | new | Tydlig IT-förmåga |
| K-002 | Plattformstjänst | SRC-002 s. 7 | explicit | match PLS-003 | Alias |
| K-003 | Princip | DRV-002 + GOAL-004 | derived | review | Behöver verksamhetsförankring |

Kandidat-ID:n är tillfälliga och ska inte återanvändas som permanenta EA-ID:n.

## 9. Anti-patterns

EA Stödjare ska undvika följande:

### Ordagrann objektsgruvning

Fel:

> Dokumentet nämner "plattform", alltså skapar vi ett Plattform-objekt.

Rätt:

> Bedöm vilken semantisk roll företeelsen faktiskt har.

### Förmågor som organisationsenheter

Fel:

> "IT-avdelningen" blir en förmåga.

Rätt:

> Identifiera vad IT-avdelningen behöver kunna åstadkomma och modellera organisationen separat endast om metamodelen senare stödjer det.

### Funktion som eget EA-objekt i v1

Fel:

> "Autentisera användare" skapas som separat global Funktion.

Rätt:

> Funktionen kan beskrivas under relevant IT-stöd, Plattformstjänst eller Plattform.

### Leverantörsprodukt som automatiskt blir plattformstjänst

Fel:

> "OpenShift" klassificeras som plattformstjänst bara för att team konsumerar den.

Rätt:

> Skilj den konsumerbara tjänsten från den tekniska plattform som realiserar den.

### Best practice som intern fakta

Fel:

> Extern praxis förs in som om organisationen redan hade beslutat den.

Rätt:

> Markera den organisationsspecifika rekommendationen `proposed` och länka extern evidens.

## 10. Minimalt resultat från en extraktionsanalys

En genomförd extraktion ska minst kunna redovisa:

- vilka källor som analyserats,
- vilka objekt som identifierats explicit,
- vilka objekt som härletts,
- vilka objekt som föreslås,
- preliminär klassificering,
- relevanta relationer,
- osäkerheter/dubbletter,
- vilken förändring av den kanoniska modellen som rekommenderas.

Om inget meningsfullt EA-objekt kan beläggas ska resultatet kunna vara att **ingen modelländring rekommenderas**.

## 11. Samspel med senare arbetsflöden

Detta arbetsflöde är basen för:

- steg 10 – research och omvärldsanalys,
- steg 11 – modellförslag,
- steg 12 – djupare klassificeringsregler,
- steg 13–14 – kvalitetskontroll,
- steg 19 – inkrementella modelländringar,
- steg 20 – konflikter och osäkerhet.

Senare steg får förfina reglerna men ska behålla grundprincipen att **evidens, härledning och rekommendation aldrig blandas ihop**.
