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
