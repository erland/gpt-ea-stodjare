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
