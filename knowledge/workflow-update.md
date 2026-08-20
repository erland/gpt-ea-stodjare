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
