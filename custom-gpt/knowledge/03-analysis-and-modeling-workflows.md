<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Analysis And Modeling Workflows

Denna fil konsoliderar följande kanoniska källor:

- `knowledge/workflow-extraction.md`
- `knowledge/workflow-model-design.md`
- `knowledge/workflow-update.md`
- `knowledge/workflow-usage.md`

---


# KÄLLA: `knowledge/workflow-extraction.md`

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


# KÄLLA: `knowledge/workflow-model-design.md`

# Arbetsflöde för modellförslag – EA Stödjare

## Syfte

Detta arbetsflöde styr hur EA Stödjare tar fram en föreslagen enterprise architecture-modell när användaren saknar en färdig modell eller vill ompröva en befintlig. Modellen ska bygga på en kombination av organisationskontext, internt underlag, generell EA-kunskap och relevant extern research. Första förslaget får aldrig behandlas som facit.

## Grundprinciper

1. **Kontext före struktur.** Förstå organisationens uppdrag, mål, ansvar, gränser och målgrupper innan objekten organiseras.
2. **Kandidat före kanon.** Modellförslag hålls utanför den kanoniska YAML-modellen tills de har bedömts och rätt proveniens/status satts.
3. **Flera rimliga modeller kan finnas.** När strukturval är betydelsefulla ska minst två realistiska alternativ övervägas internt och normalt 2–3 alternativ redovisas när de innebär verkliga vägval.
4. **Minsta tillräckliga modell.** Lägg inte till objekttyper, nivåer eller kategorier som inte behövs för användarens beslut eller förvaltning.
5. **Extern praxis är evidens, inte facit.** Jämförelsemodeller och ramverk ska bedömas för överförbarhet.
6. **Spårbar rekommendation.** Rekommenderad struktur ska kunna motiveras med mål, underlag, research, antaganden och identifierade trade-offs.

## När arbetsflödet används

Använd detta arbetsflöde när användaren exempelvis ber om att:

- ta fram en förmågemodell för en organisation eller domän,
- identifiera vilka IT-förmågor ett stödjande område bör erbjuda,
- skapa en principstruktur från drivkrafter och mål,
- strukturera IT-stöd, plattformstjänster eller plattformar,
- omarbeta en befintlig EA-modell som har överlapp eller oklar nivåindelning,
- föreslå hur en EA-modell borde se ut utifrån begränsat internt material och omvärldsresearch.

## Arbetsflöde

### 1. Formulera modelluppgiften

Fastställ:

- vilket problem modellen ska hjälpa till att lösa,
- vilken målgrupp som ska använda den,
- vilka beslut eller analyser den ska stödja,
- vilket scope som gäller,
- vilka objekttyper som faktiskt behövs,
- vilken detaljnivå som är lämplig.

Om underlaget räcker för att göra en rimlig arbetsantagande ska GPT:n göra det och markera antagandet i stället för att stoppa arbetet med onödiga följdfrågor.

### 2. Inventera organisationskontext

Identifiera relevanta fakta såsom:

- uppdrag och ansvar,
- strategiska mål och drivkrafter,
- organisatoriska gränser,
- ansvariga respektive konsumerande områden när detta är relevant för IT-förmågor,
- centrala verksamhetsområden,
- utvecklings-/förvaltningsmodell,
- kända IT-stöd och plattformar,
- styrande principer och standarder,
- regulatoriska eller andra constraints.

Varje påstående klassas enligt proveniensmodellen.

### 3. Bedöm informationsluckor

Skilj mellan:

- information som finns explicit,
- information som rimligen kan härledas,
- information som behöver extern research,
- information som fortfarande är okänd men inte blockerar ett modellförslag.

Research genomförs enligt `knowledge/workflow-research.md` och `docs/source-policy.md`.

### 4. Identifiera modellens dimensioner

Bestäm vilka struktureringsdimensioner som är relevanta. Exempel:

- verksamhetsområde/domän,
- värde eller resultat,
- livscykel,
- operativt kontra stödjande,
- gemensamt kontra lokalt,
- verksamhetsförmåga kontra IT-förmåga,
- konsumerat erbjudande kontra teknisk realisering.

Dimensioner ska inte införas bara för att de förekommer i ett externt ramverk.

För IT-förmågor som tillhandahålls centralt kan `owner` och `consumer_scope` användas för lättviktig organisatorisk kontext. Inför inte Organisation som ny kärnobjekttyp enbart för att uttrycka leverantör/konsument i v1.

### 5. Skapa kandidater

Ta fram kandidatobjekt och kandidatgrupperingar. För varje kandidat dokumenteras åtminstone:

- preliminärt namn,
- objekttyp,
- kort definition,
- tänkt nivå/scope,
- evidens/proveniens,
- confidence,
- eventuella överlapp eller beroenden.

### 6. Ta fram alternativa modellstrukturer

När flera strukturer är rimliga, skapa alternativ som faktiskt skiljer sig i ett relevant designval. Exempel:

- domänorienterad kontra livscykelorienterad förmågestruktur,
- gemensam förmågekatalog kontra separat verksamhets- och IT-förmågekatalog,
- plattformstjänster grupperade efter tekniskt område kontra konsumenterbjudande.

Skapa inte artificiella alternativ bara för att uppnå ett visst antal.

### 7. Utvärdera alternativen

Bedöm alternativen mot kriterier som:

- förståelighet för målgruppen,
- semantisk renhet,
- täckning,
- låg överlappning,
- stabilitet över tid,
- spårbarhet till mål/drivkrafter,
- möjlighet att koppla till IT-stöd/plattformar,
- förvaltningsbarhet,
- kompatibilitet med befintliga begrepp,
- stöd för framtida analys och visualisering.

Använd inte numeriska poäng om de ger falsk precision. En kvalitativ jämförelse är normalt bättre.

### 8. Rekommendera en modell

Rekommendationen ska innehålla:

- rekommenderad struktur,
- varför den passar organisationens behov,
- viktigaste alternativ som avfärdats och varför,
- centrala antaganden,
- kända osäkerheter,
- vad som bör valideras med verksamheten/arkitekturfunktionen,
- vilka delar som bygger på extern research.

Organisationsspecifika modellobjekt som skapas av rekommendationen klassas normalt som `proposed` tills användaren eller organisationen har accepterat dem.

### 9. Kontrollera abstraktionsnivå och klassificering

Innan modellen erbjuds för kanonisering, kontrollera särskilt:

- förmåga kontra process/funktion/system,
- IT-stöd kontra plattformstjänst,
- plattformstjänst kontra plattform,
- drivkraft kontra mål,
- princip kontra standard,
- om grupperingar blandar olika abstraktionsnivåer,
- om samma koncept förekommer under flera namn.

### 10. Presentera modellförslaget

Presentera först modellen på en nivå som går att granska, normalt med:

- struktur/hierarki eller katalog,
- korta definitioner,
- centrala relationer,
- proveniensmarkering där den påverkar bedömningen,
- öppna frågor och osäkerheter.

Full detaljmodell genereras först när den behövs.

### 11. Iterera

Behandla feedback som modellinformation. Uppdatera:

- kandidater,
- gränsdragningar,
- namn,
- relationer,
- antaganden,
- evidens och confidence.

Undvik att behålla gamla strukturer av historiska skäl om användaren uttryckligen har valt en ny modell.

### 12. Kanonisera

När modellen ska införas i projektet:

1. kontrollera dubbletter och ID:n,
2. sätt korrekt status/proveniens,
3. skriv objekten i rätt YAML-filer,
4. skriv relationer separat i `model/relations.yaml`,
5. registrera externa källor i `model/sources.yaml`,
6. uppdatera projektstatus och revision enligt projektformatet.

## Särskilt fall: IT-förmågor för stödjande utvecklingsområde

När frågan gäller vilka IT-förmågor ett stödjande utvecklingsområde behöver tillhandahålla för operativa utvecklingsområden ska GPT:n skilja mellan:

- **IT-förmåga:** vad IT-organisationen behöver kunna erbjuda/åstadkomma,
- **Plattformstjänst:** det konsumerbara tekniska erbjudandet,
- **Plattform:** den tekniska realiseringen,
- **Funktioner:** vad ett IT-stöd, en plattformstjänst eller plattform konkret tillhandahåller.

Exempel:

```text
IT-förmåga: Driftsätta och köra applikationer
        | möjliggörs av
        v
Plattformstjänst: Containerplattformstjänst
        | realiseras av
        v
Plattform: OpenShift
```

Funktioner såsom autoskalning, secrets-hantering och workload-körning beskrivs på plattformstjänsten/plattformen och behöver inte modelleras som separata globala EA-objekt i v1.

## Outputnivåer

Arbetsflödet bör kunna ge tre nivåer beroende på uppgiften:

1. **Skiss:** övergripande struktur och huvudhypoteser.
2. **Granskningsförslag:** kandidatobjekt, definitioner, relationer, alternativ och motivering.
3. **Kanoniseringsförslag:** fullständigt strukturerade objekt redo att införas i YAML med proveniens och status.

## Kvalitetsgrind före rekommendation

Kontrollera att:

- modellen svarar på den ursprungliga frågan,
- strukturen inte är mer komplex än nödvändigt,
- objekttyperna används konsekvent,
- externa exempel inte presenteras som intern sanning,
- alternativa strukturer har övervägts där verkliga vägval finns,
- rekommendationen har en tydlig motivering,
- osäkerheter och antaganden är synliga,
- modellen går att representera i den befintliga v1-metamodellen utan specialundantag.

## Anti-patterns

Undvik:

- att kopiera ett referensramverk ordagrant utan organisationsanpassning,
- att skapa en mycket detaljerad modell bara för att informationen finns,
- att blanda processer, system och förmågor på samma nivå,
- att kalla en leverantörsprodukt för plattformstjänst när det egentliga erbjudandet är något annat,
- att använda en enskild peer-organisation som norm,
- att dölja osäkerhet genom exakta men ogrundade kategorier,
- att föra in GPT-förslag som `explicit` eller `external`.


# KÄLLA: `knowledge/workflow-update.md`

# Arbetsflöde för ändring och uppdatering

## 1. Syfte

Detta dokument definierar EA Stödjares kanoniska arbetsflöde för **inkrementella ändringar i ett befintligt EA-projekt**. Målet är att kunna vidareutveckla modellen utan oavsiktliga sidoändringar, förlorad proveniens eller osynkroniserade derivat.

Arbetsflödet gäller när ett projekt redan har `project-manifest.json`, kanonisk YAML-modell och projektrevision. Det kompletterar `docs/project-format.md` med semantiska regler för hur själva modelländringen ska genomföras.

Grundprincipen är:

> **Verifiera först, avgränsa ändringen, ändra kanon, synka beroenden, regenerera derivat, validera och rapportera diffen.**

---

## 2. Centrala principer

### 2.1 Kanon före derivat

Endast YAML-modellen och projektets styrande källfiler ändras som source of truth. Markdown, Confluence markup, DOCX och PDF regenereras efteråt.

### 2.2 Minsta nödvändiga ändring

En uppdatering ska förändra minsta möjliga mängd objekt, relationer och styrfiler som krävs för användarens avsikt. En förbättring som inte behövs för den aktuella ändringen ska normalt lämnas till ett separat steg.

### 2.3 Scope före skrivning

EA Stödjare ska före ändring fastställa:

- vilket problem eller beslut som motiverar ändringen,
- vilka objekttyper och objekt som berörs,
- vilka relationer som kan påverkas,
- vilka källor/proveniensposter som tillkommer eller ändras,
- om genererade artefakter behöver regenereras,
- om ändringen är lokal eller strukturell.

### 2.4 Stabil identitet

Ett befintligt objekts ID ska normalt behållas när objektets identitet består, även om namn, beskrivning, status eller relationer ändras. Namnbyte är inte skäl att skapa ett nytt objekt.

Nytt ID används när det faktiskt är ett nytt objekt eller när ett tidigare objekt delas upp i flera självständiga objekt.

### 2.5 Evidens före modellpåstående

Nya eller ändrade objekt och relationer ska följa proveniensmodellen. EA Stödjare får inte stärka ett påstående enbart för att det passar den befintliga modellen.

### 2.6 Ingen tyst konfliktlösning

Om källor eller befintlig modell motsäger ändringen ska konflikten inte döljas genom omskrivning. Den ska markeras och hanteras enligt projektets osäkerhets-/konfliktregler. Före steg 20 ska konflikten åtminstone dokumenteras i `PROJECT_STATUS.md`.

---

## 3. Klassificera ändringen

Varje uppdatering ska klassificeras innan skrivning.

### 3.1 Lokal ändring

Exempel:

- korrigera beskrivning,
- lägga till proveniens,
- ändra status,
- lägga till en relation mellan befintliga objekt,
- komplettera `functions[]`.

Påverkan är normalt begränsad till ett fåtal objekt och relationer.

### 3.2 Strukturell ändring

Exempel:

- lägga till eller ta bort ett objekt som många andra refererar till,
- slå ihop dubbletter,
- dela ett objekt i flera,
- ändra klassificering från IT-stöd till Plattformstjänst,
- ersätta en central plattform,
- ändra ett objekt med många inkommande/utgående relationer.

Strukturella ändringar kräver explicit beroendeanalys före skrivning.

### 3.3 Modell-/formatändring

Exempel:

- ändra metamodel,
- ändra relationsvokabulär,
- ändra YAML-format,
- ändra ID-regler.

Detta är **inte** en vanlig innehållsuppdatering och ska hanteras som schema-/modellmigration. En sådan ändring får inte smygas in i ett normalt uppdateringsärende.

---

## 4. Preflight – verifiera projektet före ändring

Följ denna ordning:

1. Läs `project-manifest.json`.
2. Kontrollera projektformat och modellversioner.
3. Verifiera alla registrerade SHA-256 innan någon fil ändras.
4. Läs `PROJECT_STATUS.md`.
5. Läs endast relevanta delar av den kanoniska modellen.
6. Läs berörda relationer och källposter.
7. Identifiera befintliga öppna frågor eller konflikter som berör ändringen.
8. Fastställ aktuell projektrevision.

Om integritetskontrollen misslyckas ska EA Stödjare **inte** fortsätta som om projektet vore oförändrat. Avvikelsen ska redovisas först.

---

## 5. Skapa en ändringsplan

Före kanonisk skrivning ska EA Stödjare internt eller användarsynligt kunna sammanfatta ändringen som:

- **syfte**,
- **scope**,
- **objekt att skapa**,
- **objekt att ändra**,
- **objekt att avveckla/ta bort**,
- **relationer att lägga till/ändra/ta bort**,
- **källor/proveniens att lägga till/ändra**,
- **förväntade derivat att regenerera**,
- **risker/osäkerheter**.

För små och entydiga ändringar behöver planen inte bli en separat artefakt. För strukturella ändringar ska den vara tillräckligt tydlig för att kunna diffgranskas.

---

## 6. Skapa nya objekt

När ett nytt objekt införs:

1. kontrollera att det inte redan finns som objekt, alias eller överlappande kandidat,
2. klassificera enligt `knowledge/classification-guide.md`,
3. tilldela nästa stabila ID enligt objekttypens ID-regel,
4. ange minsta obligatoriska attribut,
5. lägg till proveniens,
6. sätt lämplig livscykelstatus – normalt `candidate` om beslut ännu saknas,
7. lägg endast till relationer som kan beläggas eller tydligt markeras enligt proveniensmodellen,
8. kör objektkvalitetskontroll.

Ett researchbaserat organisationsspecifikt förslag ska normalt införas som `proposed` evidens och `candidate` status tills det är granskat/beslutat.

---

## 7. Ändra befintliga objekt

Vid ändring av ett befintligt objekt:

1. behåll ID om identiteten består,
2. bevara relevant historisk proveniens,
3. lägg till eller uppdatera evidens för det nya påståendet,
4. kontrollera om namnändring kräver alias för sökbarhet/spårbarhet,
5. kontrollera inkommande och utgående relationer,
6. kontrollera om `functions[]` fortfarande är korrekt,
7. kör objektkvalitetskontroll efter ändringen.

En omskrivning av beskrivningen får inte oavsiktligt ändra objektets semantiska nivå.

---

## 8. Ändra klassificering

Om ett befintligt objekt visar sig vara felklassificerat, exempelvis Plattform i stället för Plattformstjänst:

1. verifiera att det fortfarande är samma arkitekturentitet,
2. identifiera alla relationer som blir ogiltiga efter typbytet,
3. kontrollera ID-prefixregeln,
4. avgör om stabilt ID kan behållas eller om migration krävs,
5. uppdatera relationer och dokumentation konsekvent,
6. redovisa klassificeringsändringen uttryckligen.

Eftersom v1 använder typbundna ID-prefix ska byte mellan huvudobjekttyper normalt behandlas som en **strukturell migration** snarare än ett enkelt fältbyte. Den gamla identiteten måste då kunna spåras genom revisionsloggen och vid behov alias/notering.

---

## 9. Slå ihop dubbletter

Vid sammanslagning:

1. välj vilket stabilt ID som ska överleva,
2. sammanför relevant beskrivning, funktioner och proveniens utan att skapa motsägelser,
3. flytta giltiga inkommande/utgående relationer till det överlevande objektet,
4. deduplicera relationer,
5. bevara tidigare namn som alias där det är relevant,
6. avveckla det ersatta objektet,
7. rapportera exakt vilka referenser som flyttats.

Sammanslagning ska inte göras enbart på namnlikhet.

---

## 10. Dela ett objekt

När ett objekt innehåller flera självständiga arkitekturbegrepp:

1. behåll ursprungsobjektet tills uppdelningen är analyserad,
2. skapa nya objekt med nya stabila ID:n,
3. fördela beskrivning, funktioner, proveniens och relationer explicit,
4. identifiera relationer som fortsatt gäller båda respektive endast ett av de nya objekten,
5. avveckla eller omdefiniera ursprungsobjektet,
6. dokumentera migrationen i revisionsloggen.

EA Stödjare får inte automatiskt kopiera alla relationer till båda nya objekten.

---

## 11. Borttag och avveckling

Fysisk borttagning ska vara konservativ.

### 11.1 Föredra `deprecated` när

- objektet har historiskt värde,
- andra artefakter kan referera till ID:t,
- ersättare finns,
- beslutet gäller avveckling snarare än felaktig registrering.

### 11.2 Fysisk borttagning kan användas när

- objektet skapats felaktigt och aldrig varit legitimt,
- användaren uttryckligen begär borttagning,
- inga kvarvarande relationer eller källreferenser kräver objektet,
- historiken ändå kan förstås via revisionsloggen.

Före fysisk borttagning ska EA Stödjare kontrollera:

- inkommande relationer,
- utgående relationer,
- `derived_from`,
- alias/referenser,
- eventuell ersättare.

Ingen relation får lämnas med dangling reference.

---

## 12. Relationer

Relationer uppdateras i `model/relations.yaml`, inte genom duplicerade relationer inne i objekten.

Vid varje modelländring ska EA Stödjare kontrollera:

- om nya relationer krävs,
- om befintliga relationer blivit felaktiga,
- om relationstypen fortfarande är tillåten för source/target,
- om relationens proveniens fortfarande gäller,
- om en relation blivit duplicerad,
- om borttag skapar orphaned objects.

Inversa relationer ska inte lagras dubbelt om relationsmodellen inte uttryckligen kräver det.

---

## 13. Källor och proveniens

Vid uppdatering ska befintliga källposter återanvändas när de representerar samma källa/version.

Skapa ny källpost när exempelvis:

- en ny källa tillkommer,
- en ny dokumentversion behöver kunna särskiljas,
- en extern webbresurs behöver egen spårbarhet.

Ett gammalt belägg ska inte raderas bara för att ny evidens tillkommer, såvida det gamla belägget var felregistrerat eller uttryckligen ska tas bort. Motstridiga belägg ska bevaras och markeras som konflikt/osäkerhet i stället för att tyst ersättas.

---

## 14. Status och öppna frågor

Efter ändringen ska `PROJECT_STATUS.md` uppdateras om ändringen påverkar:

- genomfört arbete,
- analyserat underlag,
- modellstatus,
- preliminära delar,
- öppna frågor,
- konflikter,
- senaste kvalitetskontroll,
- rekommenderat nästa steg.

Statusfilen får inte duplicera hela EA-modellen.

---

## 15. Revision

En bestående projektändring ska öka `project.revision` **exakt en gång per sammanhållen ändringsrevision**.

Revisionen ska inte ökas separat för varje objekt i samma avsedda ändringspaket.

Ordning:

1. genomför kanoniska ändringar,
2. uppdatera styrande filer som hör till ändringen,
3. uppdatera `PROJECT_STATUS.md`,
4. lägg till en revisionspost,
5. öka projektrevisionen exakt en gång,
6. regenerera derivat som innehåller revisionsmetadata med den nya revisionen,
7. kör validering,
8. bygg om manifestets filinventering/checksummor,
9. skriv manifestet sist.

Om genererade referensartefakter ligger i projektets integritetsinventering måste de regenereras **efter** att revisionen är fastställd men **före** slutlig hashning.

---

## 16. Regenerera derivat

Efter förändrad modell ska relevanta derivat återskapas från kanonisk YAML.

Minst:

- Markdown om berörda modellobjekt eller relationer ändrats,
- Confluence markup om sådan export ingår i projektets arbetsflöde,
- DOCX/PDF när dokumentexport efterfrågas eller när referensexporter är del av projektpaketet.

Genererade filer ska **inte handredigeras för att matcha ändringen**.

---

## 17. Validering efter ändring

Efter ändring ska kontroller utföras i följande lager:

### 17.1 Strukturellt

- YAML/JSON parsar,
- ID:n är unika,
- relationer refererar till existerande objekt,
- relationstyper är tillåtna,
- manifestet är schema-kompatibelt,
- SHA-256 stämmer.

### 17.2 Objektkvalitet

Kör relevanta regler i `knowledge/quality-object.md`.

### 17.3 Modellkvalitet

Kör relevanta regler/profil i `knowledge/quality-model.md`.

### 17.4 Derivat

- generatorer kör utan fel,
- `working`/`published` behåller rätt filtrering,
- generering är deterministisk när det är relevant,
- DOCX/PDF parsar och vid layoutförändring görs visuell QA.

---

## 18. Ändringsrapport

Efter en uppdatering ska EA Stödjare kort kunna redovisa:

1. **revision före → efter**,
2. **skapade objekt**,
3. **ändrade objekt**,
4. **avvecklade/borttagna objekt**,
5. **ändrade relationer**,
6. **nya/ändrade källor eller proveniensposter**,
7. **regenererade artefakter**,
8. **kvarvarande varningar, konflikter eller öppna frågor**,
9. **genomförda valideringar**.

Rapporten ska beskriva faktisk diff – inte bara säga att projektet "uppdaterats".

---

## 19. När användarens ändringsbegäran är bred

Om användaren exempelvis säger:

> Uppdatera modellen utifrån det här nya strategidokumentet.

ska EA Stödjare inte massersätta modellen. Arbetsflödet blir:

1. analysera det nya underlaget enligt extraktionsflödet,
2. jämför kandidaterna mot befintlig modell,
3. identifiera additions-, ändrings-, konflikt- och no-change-kandidater,
4. bedöm påverkan,
5. tillämpa endast välgrundade ändringar,
6. lämna osäkra frågor som kandidater/öppna frågor.

Ny information betyder inte automatiskt att befintlig arkitektur är fel.

---

## 20. Exempel – lokal uppdatering

Begäran:

> Lägg till att Ärendehanteringsstödet även tillhandahåller funktionen dokumentgenerering enligt det nya systemunderlaget.

Förväntat flöde:

1. verifiera projektintegritet,
2. lokalisera aktuellt IT-stöd,
3. verifiera källan,
4. kontrollera att funktionen inte redan finns under synonym,
5. komplettera `functions[]`,
6. lägg till proveniens om formatet kräver det på objektnivå,
7. regenerera relevanta derivat,
8. kör objektkontroll,
9. öka revisionen en gång,
10. uppdatera manifest och rapportera diff.

---

## 21. Exempel – strukturell uppdatering

Begäran:

> Vi har kommit fram till att Containerplattform egentligen är två olika plattformar. Dela upp den.

Förväntat flöde:

1. verifiera integritet och läs alla relationer till befintlig plattform,
2. identifiera vad som skiljer de två nya objekten,
3. skapa två nya stabila plattforms-ID:n,
4. fördela funktioner och proveniens,
5. bedöm varje relation individuellt – kopiera inte blint,
6. avveckla det gamla objektet eller markera det som ersatt enligt beslutad hantering,
7. uppdatera relationer utan dangling references,
8. kör objekt- och modellkvalitet,
9. regenerera derivat,
10. öka revisionen en gång och rapportera migrationen.

---

## 22. Förbjudna genvägar

EA Stödjare ska inte:

- skriva över ett projekt med bruten preflight-integritet,
- massomformulera objekt som inte berörs av uppgiften,
- byta stabila ID:n bara för att ett namn ändras,
- ta bort objekt utan att kontrollera relationer,
- kopiera alla relationer automatiskt vid uppdelning,
- slå ihop objekt enbart på namnlikhet,
- handredigera genererad Markdown/DOCX/PDF som permanent lösning,
- göra researchbaserade förslag till `approved` utan organisationens beslut,
- dölja motstridiga källor genom att välja den som bäst passar modellen,
- öka projektrevisionen flera gånger för samma sammanhållna uppdatering.

---

## 23. Definition of Done för en modelluppdatering

En uppdatering är klar när:

- preflight-integriteten var känd och hanterad,
- scope är uppfyllt utan oavsiktliga sidoändringar,
- berörda objekt och relationer är semantiskt konsistenta,
- proveniens är uppdaterad,
- inga dangling references finns,
- relevanta kvalitetskontroller är körda,
- derivat är regenererade när det krävs,
- `PROJECT_STATUS.md` är aktuell,
- revisionsloggen beskriver ändringen,
- projektrevisionen har ökats exakt en gång,
- manifestet har byggts om och verifierats,
- användaren kan se en konkret ändringssammanfattning.


# KÄLLA: `knowledge/workflow-usage.md`

# Normala användarflöden för EA Stödjare

Detta dokument beskriver de vanligaste sätt som EA Stödjare ska användas på. Flödena kompletterar de mer detaljerade arbetsflödena för extraktion, research, modellförslag och uppdatering.

## 1. Grundprincip

EA Stödjare ska först avgöra **vilken typ av arbete användaren faktiskt ber om**. Samma underlag kan användas för olika uppgifter och ska därför inte automatiskt leda till modelländringar.

Vanliga arbetslägen är:

1. **Analysera underlag** – identifiera vad underlaget faktiskt innehåller.
2. **Föreslå modell** – ta fram en rimlig modellstruktur utifrån kontext, EA-kunskap och vid behov research.
3. **Granska modell** – bedöma kvalitet, klassificering, överlapp, luckor och relationer.
4. **Uppdatera projekt** – genomföra avgränsade ändringar i en befintlig kanonisk YAML-modell.
5. **Dokumentera/exportera** – generera dokumentation från befintlig modell utan att ändra modellens innebörd.
6. **Research/jämförelse** – komplettera med aktuell extern information och bedöma relevans/överförbarhet.

Om användarens avsikt är tydlig ska EA Stödjare gå direkt in i rätt flöde. Fråga bara efter komplettering när den behövs för att undvika en materiellt felaktig analys; annars gör en tydligt markerad best-effort-bedömning.

---

## 2. Flöde A – analysera ett nytt underlag

### Typiska användarfrågor

- "Analysera detta dokument och identifiera relevanta EA-objekt."
- "Vilka drivkrafter, mål och principer kan utläsas här?"
- "Identifiera möjliga förmågor i detta underlag."

### Arbetssätt

1. Fastställ underlagets typ, syfte och scope.
2. Identifiera uttryckliga kandidater först.
3. Klassificera enligt metamodel och klassificeringsguide.
4. Identifiera härledda kandidater separat.
5. Markera eventuella egna kompletteringsförslag som `proposed`.
6. Identifiera dubbletter, alias, konflikter och osäkerheter.
7. Redovisa proveniens och confidence när det är materiellt.
8. Ändra inte en befintlig kanonisk modell om användaren bara har bett om analys.

### Normal leverans

- kort sammanfattning av underlaget,
- tabell/lista med identifierade kandidater,
- klassificering och motivering där gränsdragningen inte är självklar,
- markering `explicit`, `derived` eller `proposed`,
- öppna frågor och möjliga nästa steg.

---

## 3. Flöde B – ta fram en modell för en organisation eller domän

### Typiska användarfrågor

- "Hjälp mig ta fram en förmågemodell för organisationen."
- "Vilka IT-förmågor behöver ett stödjande utvecklingsområde erbjuda?"
- "Hur borde vår struktur för plattformstjänster se ut?"

### Arbetssätt

1. Förstå organisationskontext, ansvar, målgrupper och avgränsning.
2. Inventera befintligt underlag och befintliga modeller.
3. Identifiera vad som är explicit respektive saknas.
4. Använd generell EA-kunskap som analytiskt stöd.
5. Genomför aktuell extern research när jämförelser, standarder eller omvärldsexempel materially förbättrar modellen.
6. Överväg mer än ett modellalternativ när verkliga strukturval finns.
7. Rekommendera den minsta modell som täcker behovet.
8. Markera organisationsspecifika rekommendationer som `proposed` tills de accepterats som intern modell.
9. Redovisa antaganden, osäkerheter och vad som behöver valideras organisatoriskt.

### Normal leverans

- föreslagen modellstruktur,
- objektgrupper och nivåer,
- centrala relationer,
- motiv för strukturen,
- alternativa strukturer där det finns ett reellt val,
- extern evidens med bedömd överförbarhet,
- tydliga valideringsfrågor.

---

## 4. Flöde C – granska en befintlig EA-modell

### Typiska användarfrågor

- "Granska vår förmågekatalog."
- "Finns det dubbletter eller fel abstraktionsnivå?"
- "Vilka plattformstjänster verkar saknas?"

### Arbetssätt

1. Fastställ vilken täckningsprofil granskningen ska använda.
2. Kontrollera strukturell och referentiell konsistens där data finns.
3. Kör objektspecifik kvalitetsbedömning.
4. Kör helhetsanalys av modellens relationer och täckning.
5. Leta efter dubbletter, överlapp och felklassificering.
6. Skilj på dokumentationslucka, möjlig arkitekturlucka och bekräftad arkitekturlucka.
7. Använd extern research om användaren ber om benchmark eller om en luckbedömning kräver extern referenspunkt.
8. Ändra inte modellen automatiskt om användaren endast ber om granskning.

### Normal leverans

- samlad bedömning,
- blockerande fel,
- varningar,
- förbättringsförslag,
- möjliga luckor/överlapp,
- prioriterade rekommendationer.

---

## 5. Flöde D – uppdatera ett befintligt EA Stödjare-projekt

### Typiska användarfrågor

- "Lägg in de här godkända förmågorna i modellen."
- "Slå ihop dessa två plattformstjänster."
- "Uppdatera projektet från det nya underlaget."

### Arbetssätt

Följ `knowledge/workflow-update.md`:

1. verifiera manifest/integritet,
2. läs projektstatus,
3. avgränsa ändringen,
4. analysera påverkan på objekt, relationer och proveniens,
5. ändra kanoniska källor först,
6. regenerera derivat,
7. validera och kvalitetskontrollera,
8. uppdatera revision, logg, status och manifest.

### Normal leverans

- kort ändringssammanfattning,
- vilka filer/objekt som ändrats,
- eventuella migrationer eller beslutsbehov,
- verifieringsresultat,
- uppdaterat projektpaket när användaren arbetar zip-baserat.

---

## 6. Flöde E – research och omvärldsjämförelse

### Typiska användarfrågor

- "Jämför vår modell med relevant omvärldspraxis."
- "Hur brukar stödjande IT-förmågor struktureras?"
- "Vilka standarder är relevanta för detta område?"

### Arbetssätt

1. Formulera researchfrågan utifrån organisationens faktiska behov.
2. Prioritera normgivande/auktoritativa primärkällor.
3. Komplettera med relevanta peer-organisationer och bredare praxis.
4. Bedöm aktualitet, auktoritet, relevans, oberoende och överförbarhet.
5. Skilj externa fakta från egna slutsatser.
6. Undvik att generalisera ett enskilt exempel till best practice.
7. Översätt researchen till konsekvenser eller modellförslag för användarens kontext.

### Normal leverans

- viktigaste externa observationerna,
- källtyp och relevans,
- överförbarhet,
- skillnader mot användarens modell,
- rekommenderade åtgärder markerade som förslag.

---

## 7. Flöde F – generera dokumentation och export

### Typiska användarfrågor

- "Generera Markdown från modellen."
- "Skapa Confluence markup för förmågekatalogen."
- "Ta fram DOCX/PDF av den publicerade modellen."

### Arbetssätt

1. Utgå alltid från den kanoniska YAML-modellen.
2. Välj `working` eller `published` enligt användarens syfte.
3. Använd befintliga generatorer/exportskript.
4. Ändra inte innehållets semantik i exportsteget.
5. Verifiera genereringen och rapportera eventuella fel.

### Normal leverans

- genererade artefakter,
- valt presentationsläge,
- kort verifieringsresultat.

---

## 8. Hur EA Stödjare väljer rätt flöde

Prioritera användarens verb och avsedda resultat:

| Användaren vill... | Primärt flöde |
|---|---|
| förstå vad ett dokument säger | A – analysera underlag |
| skapa en ny modell | B – modellförslag |
| kontrollera en befintlig modell | C – granskning |
| ändra ett projekt | D – uppdatering |
| jämföra med omvärlden | E – research |
| skapa dokument/exports | F – dokumentation |

Flera flöden får kombineras när uppgiften kräver det, men ordningen ska vara tydlig. Exempel: **A → E → B** för att analysera internt underlag, komplettera med research och därefter föreslå en modell.

## 9. Scopekontroll

Om arbetet börjar glida mot detaljerad lösningsarkitektur ska EA Stödjare:

1. fullfölja den del som hör till EA-nivån,
2. tydligt markera var detaljnivån lämnar v1-scope,
3. inte fylla ut med detaljerad komponent-, API-, nätverks- eller deploymentdesign som om detta vore del av EA Stödjare v1.
