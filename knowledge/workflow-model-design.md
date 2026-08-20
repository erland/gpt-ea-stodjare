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
