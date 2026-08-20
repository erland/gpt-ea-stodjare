# EA Stödjare – steg-för-steg utvecklingsplan

## 1. Syfte med planen

Den här planen beskriver hur **EA Stödjare** kan tas fram stegvis som en Custom GPT och som ett versionshanterat projektpaket. Varje steg är avgränsat så att det kan genomföras i en separat prompt, exempelvis:

> Gör steg 7 enligt utvecklingsplanen och ge mig en uppdaterad projekt-zip.

Planen är avsiktligt uppbyggd så att varje steg lämnar projektet i ett konsistent och verifierbart läge innan nästa steg påbörjas.

EA Stödjare ska i första versionen fokusera på **enterprise architecture** och inte på detaljerad lösningsarkitektur.

---

# 2. Målbild för EA Stödjare

EA Stödjare ska hjälpa användaren att:

- analysera befintliga dokument, modeller och andra underlag,
- identifiera relevanta enterprise architecture-objekt,
- skilja på sådant som uttryckligen finns i underlaget, sådant som kan härledas och sådant som GPT:n själv föreslår,
- använda egen generell kunskap och aktuell omvärldsinformation för att komplettera analysen,
- undersöka hur en lämplig arkitekturmodell för en viss organisation eller domän skulle kunna se ut,
- jämföra med etablerade modeller, standarder, praxis och relevanta externa exempel,
- normalisera terminologi och identifiera överlapp, dubbletter och luckor,
- modellera relationer mellan arkitekturobjekt,
- förvalta en strukturerad och maskinläsbar EA-modell,
- generera konsistent dokumentation från modellen,
- kvalitetssäkra modellen och den genererade dokumentationen.

EA Stödjare ska alltså inte bara dokumentera vad användaren redan vet. Den ska också kunna agera som **analys- och researchstöd**.

Exempel:

> Analysera vårt strategidokument och identifiera möjliga drivkrafter, mål och arkitekturprinciper.

> Undersök hur en rimlig IT-förmågemodell för en stödjande IT-organisation skulle kunna se ut utifrån vårt underlag, generell EA-praxis och relevanta externa källor.

> Jämför vår befintliga plattformstjänstekatalog med hur liknande förmågor normalt realiseras och identifiera möjliga luckor.

> Bedöm om det här objektet bör klassificeras som förmåga, IT-stöd, plattformstjänst eller plattform.

---

# 3. Avgränsning för version 1

## Primära objekttyper

- Drivkraft
- Mål
- Princip
- Förmåga
  - verksamhetsförmåga
  - IT-förmåga
- IT-stöd
- Plattformstjänst
- Plattform
- Standard

## Sekundära objekttyper

- Lösningsmönster
- Referensarkitektur

Dessa ska stödjas av datamodellen men behöver inte ha samma djup eller arbetsflödesstöd som kärnobjekten i version 1.

## Underordnad information

Följande bör normalt vara attribut eller underobjekt snarare än egna globala objekttyper i v1:

- funktioner,
- beskrivning,
- status,
- ägare,
- taggar/kategorier,
- källor och proveniens,
- livscykelinformation.

Funktioner ska i v1 kunna beskrivas för:

- IT-stöd,
- Plattformstjänst,
- Plattform.

Funktion ska inte vara en obligatorisk mellanliggande nod mellan Förmåga och IT-stöd.

## Utanför scope för v1

- detaljerad lösningsarkitektur,
- komponentarkitektur,
- API-design,
- integrationskontrakt,
- databasdesign,
- deploymentdesign,
- nätverksdesign,
- detaljerad säkerhetsdesign,
- sekvensdiagram,
- implementationsinstruktioner,
- full ArchiMate-modellering,
- automatisk diagramgenerering.

---

# 4. Grundläggande designprinciper

## 4.1 YAML som source of truth

Den kanoniska EA-modellen ska i första hand lagras i YAML.

Exempel på struktur:

```text
model/
  drivers.yaml
  goals.yaml
  principles.yaml
  capabilities.yaml
  it-support.yaml
  platform-services.yaml
  platforms.yaml
  standards.yaml
  solution-patterns.yaml
  reference-architectures.yaml
  relations.yaml
```

## 4.2 Genererade format

Dokumentation genereras från modellen:

```text
YAML-modell
    |
    +-- Markdown
    +-- Confluence markup
    +-- DOCX
    +-- PDF
```

Genererade dokument ska inte betraktas som parallella sanningskällor.

## 4.3 Stabil identitet

Varje EA-objekt ska ha ett stabilt ID.

Exempel:

- DRV-001
- GOAL-001
- PRN-001
- CAP-001
- ITS-001
- PLS-001
- PLT-001
- STD-001

## 4.4 Evidensdisciplin

EA Stödjare ska tydligt skilja mellan:

1. **explicit** – uttryckligen belagt i underlaget,
2. **derived** – härlett från underlaget,
3. **proposed** – rekommendation eller förslag från GPT:n,
4. **external** – baserat på externa källor eller omvärldsresearch.

GPT:n får inte presentera ett eget förslag som om det uttryckligen stod i användarens underlag.

## 4.5 Research som förstaklassfunktion

När uppgiften kräver det ska EA Stödjare kunna:

- använda webbsökning,
- prioritera primärkällor och auktoritativa källor,
- söka efter etablerad EA-praxis,
- jämföra relevanta organisationer och modeller,
- identifiera standarder och referensmodeller,
- komplettera användarens underlag med omvärldskunskap,
- redovisa vad som kommer från externa källor,
- separera fakta från rekommendationer.

---

# 5. Föreslagen utvecklingsplan

## Steg 1 – Fastställ produktvision och scope

### Mål
Skapa den kanoniska beskrivningen av vad EA Stödjare är, vem den är till för och vad den inte ska göra.

### Genomför
- definiera syfte,
- definiera målgrupper,
- definiera primära användningsfall,
- definiera v1-scope,
- definiera uttryckliga avgränsningar mot lösningsarkitektur,
- definiera relationen till Lärobokskaparen,
- definiera principen om analys + research + modellering + dokumentgenerering.

### Leverabler
- `docs/product-vision.md`
- initial `README.md`

### Klart när
Det går att avgöra om ett nytt önskemål hör till EA Stödjare v1 eller inte.

### Prompt för genomförande
> Genomför steg 1 i utvecklingsplanen för EA Stödjare. Fastställ produktvision, målgrupper, användningsfall, scope och uttryckliga avgränsningar. Utgå från den överenskomna inriktningen och skapa/uppdatera projektfilerna. Ge mig en uppdaterad projekt-zip och redovisa kort vilka filer som ändrats.

---

## Steg 2 – Inventera och återanvänd lämpliga delar från Lärobokskaparen

### Mål
Identifiera vilka tekniska och metodmässiga delar från Lärobokskaparen som bör återanvändas.

### Genomför
Inventera bland annat:
- projektmanifest,
- revisionshantering,
- integritetskontroll,
- projektstatus,
- Builder Knowledge-struktur,
- instruktionernas struktur,
- kvalitetsgrindar,
- test-/valideringsupplägg,
- exportmekanismer,
- GitHub Actions,
- versionshantering,
- zip-distribution.

Klassificera varje del som:
- återanvänd direkt,
- återanvänd efter anpassning,
- ej relevant.

### Leverabler
- `docs/reuse-analysis.md`
- reviderad teknisk målbild

### Klart när
Det finns ett medvetet beslut för varje viktig mekanism från Lärobokskaparen.

### Prompt
> Genomför steg 2 i utvecklingsplanen för EA Stödjare. Inventera bifogad/befintlig Lärobokskapare och dokumentera vilka mekanismer som ska återanvändas direkt, anpassas eller lämnas utanför. Implementera endast de grundläggande återanvändningsbeslut som behövs för projektstrukturen i detta steg.

---

## Steg 3 – Definiera EA-metamodell v1

### Mål
Fastställa objekttyper, attribut och centrala semantiska skillnader.

### Genomför
Definiera minst:
- Drivkraft,
- Mål,
- Princip,
- Förmåga,
- verksamhetsförmåga,
- IT-förmåga,
- IT-stöd,
- Plattformstjänst,
- Plattform,
- Standard,
- Lösningsmönster,
- Referensarkitektur.

Definiera också:
- vad varje objekttyp är,
- vad den inte är,
- obligatoriska attribut,
- valfria attribut,
- tillåtna statusvärden,
- ID-format,
- namnregler,
- funktioner som underordnat attribut.

### Leverabler
- `docs/metamodel.md`
- `schemas/object-types.yaml`

### Klart när
Två olika användare rimligen skulle klassificera samma objekt på ungefär samma sätt.

### Prompt
> Genomför steg 3 i utvecklingsplanen för EA Stödjare. Definiera och dokumentera metamodel v1 med tydliga definitioner, gränsdragningar, attribut och exempel för samtliga överenskomna objekttyper.

---

## Steg 4 – Definiera relationsmodell v1

### Mål
Fastställa vilka relationer som får uttryckas mellan objekten.

### Genomför
Ta fram ett begränsat, semantiskt tydligt relationsvokabulär, exempelvis:
- influences,
- realizes,
- supports,
- uses,
- enabled_by,
- realized_by,
- governed_by,
- constrains,
- depends_on,
- derived_from,
- related_to.

Definiera:
- tillåtna source/target-kombinationer,
- riktning,
- betydelse,
- när relationen ska respektive inte ska användas.

### Leverabler
- `docs/relations.md`
- `schemas/relations.yaml`

### Klart när
Det går att validera om en relation är semantiskt tillåten.

### Prompt
> Genomför steg 4 i utvecklingsplanen för EA Stödjare. Definiera en begränsad och tydlig relationsmodell v1 och dokumentera tillåtna relationer mellan objekttyperna.

---

## Steg 5 – Definiera proveniens- och evidensmodell

### Mål
Göra det möjligt att spåra varför ett objekt eller en relation finns.

### Genomför
Definiera stöd för:
- explicit,
- derived,
- proposed,
- external,
- källa,
- dokumentreferens,
- URL,
- datum,
- derived_from,
- confidence,
- kommentar/motivering.

Definiera också regler för när GPT:n får hävda respektive föreslå något.

### Leverabler
- `docs/provenance-model.md`
- `schemas/provenance.yaml`

### Klart när
Alla viktiga slutsatser kan spåras till underlag eller markeras som GPT-förslag.

### Prompt
> Genomför steg 5 i utvecklingsplanen för EA Stödjare. Definiera proveniens- och evidensmodellen så att explicit information, härledningar, externa fakta och GPT-förslag alltid går att skilja åt.

---

## Steg 6 – Skapa kanoniskt YAML-schema

### Mål
Omsätta metamodel och relationsmodell till ett praktiskt YAML-format.

### Genomför
Skapa:
- filstruktur,
- schemas,
- exempelobjekt,
- relationsformat,
- källreferenser,
- funktioner,
- kategorisering,
- versionsfält.

Undvik övermodellering.

### Leverabler
- `model/*.yaml`
- `schemas/*.yaml`
- `examples/minimal-model/`

### Klart när
En liten men komplett EA-modell kan representeras utan Markdown.

### Prompt
> Genomför steg 6 i utvecklingsplanen för EA Stödjare. Skapa den kanoniska YAML-strukturen och ett minimalt exempelprojekt som demonstrerar alla centrala objekttyper och relationer.

---

## Steg 7 – Definiera projektformat och manifest

### Mål
Skapa ett robust projektformat inspirerat av Lärobokskaparen.

### Genomför
Definiera bland annat:
- projektmanifest,
- revision,
- projektnamn,
- modellversion,
- språk,
- skapad/uppdaterad,
- filinventering,
- integritetsinformation,
- projektstatus.

### Leverabler
- `project-manifest.json`
- `docs/project-format.md`
- exempelmanifest

### Klart när
EA Stödjare kan identifiera, läsa och uppdatera ett EA-projekt på ett reproducerbart sätt.

### Prompt
> Genomför steg 7 i utvecklingsplanen för EA Stödjare. Definiera projektformat, manifest, revision och filintegritet baserat på de bästa delarna från Lärobokskaparen men anpassat till EA-modellen.

---

## Steg 8 – Definiera projektstatus och arbetsläge

### Mål
Göra långvarigt iterativt arbete robust.

### Genomför
Projektet ska kunna registrera:
- vad som analyserats,
- vilka modeller som skapats,
- vilka delar som är preliminära,
- öppna frågor,
- konflikter,
- rekommenderade nästa steg,
- senaste genomförda kvalitetskontroll.

### Leverabler
- `PROJECT_STATUS.md`
- statusregler i instruktion/knowledge

### Klart när
En ny chat kan fortsätta arbetet från projektpaketet utan att behöva rekonstruera historiken.

### Prompt
> Genomför steg 8 i utvecklingsplanen för EA Stödjare. Definiera och implementera projektstatus så att projektet kan fortsätta säkert mellan separata chattar och revisioner.

---

## Steg 9 – Skapa arbetsflöde för extraktion ur underlag

### Mål
Lära GPT:n att systematiskt identifiera EA-objekt i dokument och annat underlag.

### Genomför
Definiera arbetsflöde:
1. inventera underlaget,
2. identifiera explicita kandidater,
3. klassificera,
4. identifiera härledda kandidater,
5. markera osäkerheter,
6. normalisera,
7. föreslå nya objekt vid behov,
8. presentera ändringar innan de blir kanoniska när risken kräver det.

### Leverabler
- `knowledge/workflow-extraction.md`
- testexempel

### Klart när
GPT:n konsekvent skiljer mellan identifierat, härlett och föreslaget.

### Prompt
> Genomför steg 9 i utvecklingsplanen för EA Stödjare. Skapa arbetsflödet för att analysera underlag och extrahera EA-objekt med korrekt proveniens och klassificering.

---

## Steg 10 – Skapa arbetsflöde för research och omvärldsanalys

### Mål
Göra EA Stödjare kapabel att komplettera användarens material med kvalificerad extern research.

### Genomför
Definiera hur GPT:n ska:
- avgöra när extern research behövs,
- formulera researchfrågor,
- söka efter primärkällor,
- använda standarder och auktoritativa källor,
- använda relevant branschpraxis,
- hitta jämförbara organisationsmodeller,
- skilja etablerad praxis från enskilda exempel,
- bedöma överförbarhet till användarens organisation,
- dokumentera externa källor,
- markera rekommendationer som rekommendationer.

### Viktig användning
GPT:n ska kunna få ett begränsat internt underlag och ändå hjälpa till med frågan:

> Hur skulle en rimlig modell kunna se ut?

via kombinationen:

```text
användarens underlag
+ EA-kunskap
+ aktuell omvärldsresearch
+ tydligt markerade antaganden
= kvalificerat modellförslag
```

### Leverabler
- `knowledge/workflow-research.md`
- `docs/source-policy.md`

### Klart när
Research är reproducerbar, transparent och inte blandas ihop med organisationens egna beslut.

### Prompt
> Genomför steg 10 i utvecklingsplanen för EA Stödjare. Definiera ett robust research- och omvärldsarbetsflöde som gör att GPT:n kan komplettera ett underlag med generell kunskap och aktuella externa källor och därefter föreslå hur en relevant EA-modell skulle kunna se ut.

---

## Steg 11 – Skapa arbetsflöde för modellförslag

### Mål
Göra GPT:n bra på att ta fram en ny modell när användaren inte redan har en.

### Genomför
Arbetsflödet ska stödja:
- problemformulering,
- organisationskontext,
- målgrupper,
- befintliga artefakter,
- research,
- hypoteser,
- modellalternativ,
- rekommenderad modell,
- motivering,
- osäkerheter,
- valideringsfrågor.

GPT:n ska undvika att behandla första förslaget som facit.

### Leverabler
- `knowledge/workflow-model-design.md`

### Klart när
GPT:n kan ta fram och motivera en modell snarare än att bara inventera befintliga objekt.

### Prompt
> Genomför steg 11 i utvecklingsplanen för EA Stödjare. Skapa arbetsflödet för att utifrån begränsat underlag, EA-kunskap och research ta fram och jämföra alternativa modellstrukturer och rekommendera en lämplig modell.

---

## Steg 12 – Skapa normaliserings- och klassificeringsregler

### Mål
Förhindra att modellens nivåer blandas ihop.

### Genomför
Skapa regler och heuristik för att skilja exempelvis:
- drivkraft från mål,
- mål från princip,
- princip från standard,
- förmåga från process,
- förmåga från funktion,
- funktion från IT-stöd,
- IT-stöd från plattformstjänst,
- plattformstjänst från plattform,
- plattform från produkt,
- lösningsmönster från referensarkitektur.

### Leverabler
- `knowledge/classification-guide.md`

### Klart när
GPT:n aktivt ifrågasätter felklassificeringar.

### Prompt
> Genomför steg 12 i utvecklingsplanen för EA Stödjare. Ta fram tydliga klassificerings- och normaliseringsregler med exempel och motexempel för samtliga centrala gränsdragningar i metamodel v1.

---

## Steg 13 – Skapa kvalitetskontroll för enskilda objekt

### Mål
Göra varje objekt granskningsbart.

### Genomför
Kontroller per objekttyp, exempelvis:
- tydligt namn,
- rätt abstraktionsnivå,
- begriplig beskrivning,
- korrekt objekttyp,
- tillräcklig proveniens,
- korrekt status,
- rimliga relationer,
- inga dubbletter.

### Leverabler
- `knowledge/quality-object.md`
- maskinläsbara kontrollregler där lämpligt.

### Prompt
> Genomför steg 13 i utvecklingsplanen för EA Stödjare. Skapa kvalitetsregler för varje objekttyp och definiera hur GPT:n ska rapportera fel, varningar och förbättringsförslag.

---

## Steg 14 – Skapa kvalitetskontroll för hela modellen

### Mål
Kunna bedöma modellens sammanhang och täckning.

### Genomför
Kontrollera bland annat:
- orphaned objects,
- dubbletter,
- överlapp,
- motsägelser,
- saknade relationer,
- onormalt täta/glesa delar,
- förmågor utan stöd,
- plattformstjänster utan tydligt syfte,
- plattformar utan tjänster,
- principer utan faktisk styrande betydelse,
- mål utan koppling till förmågor,
- externa rekommendationer som blivit omarkerade som intern sanning.

### Leverabler
- `knowledge/quality-model.md`

### Prompt
> Genomför steg 14 i utvecklingsplanen för EA Stödjare. Skapa en helhetskontroll för EA-modellen med kontroller för konsistens, täckning, överlapp, spårbarhet och semantisk kvalitet.

---

## Steg 15 – Definiera Markdown-dokumentationsprofiler

### Mål
Bestämma hur varje objekttyp ska dokumenteras.

### Genomför
Skapa mallar för exempelvis:
- drivkraftskatalog,
- målkatalog,
- principkatalog,
- förmågekatalog,
- IT-stödskatalog,
- plattformstjänstekatalog,
- plattformskatalog,
- standardkatalog,
- detaljsida per objekt där relevant.

### Leverabler
- `templates/markdown/*.md`
- `docs/documentation-profiles.md`

### Prompt
> Genomför steg 15 i utvecklingsplanen för EA Stödjare. Definiera Markdown-profiler och mallar för kataloger och objektdokumentation för samtliga centrala objekttyper.

---

## Steg 16 – Implementera deterministisk Markdown-generering

### Mål
Generera Markdown från YAML utan att handredigera den genererade informationen.

### Genomför
Skapa generator/script och verifiera:
- stabil ordning,
- stabil formattering,
- interna länkar,
- relationslistor,
- proveniens,
- funktioner,
- metadata.

### Leverabler
- `scripts/generate_markdown.py`
- genererad `docs/`

### Prompt
> Genomför steg 16 i utvecklingsplanen för EA Stödjare. Implementera och testa deterministisk Markdown-generering från den kanoniska YAML-modellen.

---

## Steg 17 – Implementera Confluence markup-export

### Mål
Göra modellen praktiskt användbar i Confluence.

### Genomför
Skapa export från samma modell/mellanrepresentation.

Stöd minst:
- rubriker,
- tabeller,
- listor,
- länkar/referenser,
- objektdetaljer.

### Leverabler
- `scripts/generate_confluence.py`
- `exports/confluence/`

### Prompt
> Genomför steg 17 i utvecklingsplanen för EA Stödjare. Implementera Confluence markup-export från samma kanoniska EA-modell och verifiera att innehållet är semantiskt konsistent med Markdown-exporten.

---

## Steg 18 – Implementera DOCX- och PDF-export

### Mål
Skapa läsbara dokumentpaket för distribution.

### Genomför
Utgå från genererad Markdown och använd reproducerbar export, exempelvis via Pandoc.

Definiera:
- titel,
- metadata,
- innehållsförteckning,
- tabellformat,
- sidbrytningar,
- enkel professionell layout.

### Leverabler
- exportscript,
- DOCX,
- PDF,
- exportdokumentation.

### Prompt
> Genomför steg 18 i utvecklingsplanen för EA Stödjare. Implementera reproducerbar DOCX- och PDF-export från genererad dokumentation och verifiera att inga parallella sanningskällor introduceras.

---

## Steg 19 – Skapa ändrings- och uppdateringsarbetsflöde

### Mål
Göra det säkert att vidareutveckla en befintlig modell.

### Genomför
Definiera hur GPT:n ska:
- läsa befintlig modell,
- förstå scope för ändringen,
- undvika oavsiktliga sidoändringar,
- uppdatera objekt,
- hantera borttag,
- uppdatera relationer,
- öka revision,
- regenerera output,
- rapportera ändringar.

### Leverabler
- `knowledge/workflow-update.md`

### Prompt
> Genomför steg 19 i utvecklingsplanen för EA Stödjare. Skapa ett säkert arbetsflöde för inkrementella modelländringar, revisioner och regenerering av dokumentation.

---

## Steg 20 – Skapa konflikthantering och osäkerhetsmodell

### Mål
Hantera att EA-underlag ofta motsäger varandra.

### Genomför
Definiera stöd för:
- conflicting sources,
- unresolved,
- obsolete,
- candidate,
- approved,
- deprecated,
- confidence,
- beslutsbehov.

GPT:n ska inte tvinga fram falsk entydighet.

### Leverabler
- `knowledge/conflicts-and-uncertainty.md`

### Prompt
> Genomför steg 20 i utvecklingsplanen för EA Stödjare. Definiera hur motstridiga källor, osäkerheter, preliminära objekt och olösta arkitekturfrågor ska representeras och hanteras.

---

## Steg 21 – Skapa Builder-instruktionen för Custom GPT

### Mål
Samla beteendet i en kompakt och robust systeminstruktion.

### Genomför
Instruktionen ska täcka:
- roll,
- scope,
- arbetsprinciper,
- evidensdisciplin,
- research,
- klassificering,
- modellhantering,
- filhantering,
- kvalitetskontroll,
- export,
- avgränsningar.

Håll huvudinstruktionen kompakt och flytta detaljer till Knowledge.

### Leverabler
- `custom-gpt/instructions.md`

### Prompt
> Genomför steg 21 i utvecklingsplanen för EA Stödjare. Skapa den första kompletta Builder-instruktionen för Custom GPT och säkerställ att detaljer som lämpar sig bättre som Knowledge inte dupliceras i onödan.

---

## Steg 22 – Bygg Builder Knowledge

### Mål
Skapa den knowledge-bas GPT:n behöver för stabilt beteende.

### Genomför
Konsolidera lämpliga filer för Builder Knowledge, exempelvis:
- metamodel,
- relationsmodell,
- klassificeringsguide,
- researcharbetsflöde,
- extraktionsarbetsflöde,
- kvalitetsregler,
- projektformat,
- outputregler.

### Leverabler
- `custom-gpt/knowledge/`

### Prompt
> Genomför steg 22 i utvecklingsplanen för EA Stödjare. Bygg och optimera Builder Knowledge så att Custom GPT-versionen får samma semantik och arbetsregler som projektversionen utan onödig duplicering.

---

## Steg 23 – Skapa conversation starters och normala arbetsflöden

### Mål
Göra GPT:n lätt att förstå och använda.

### Exempel
- Analysera detta underlag och identifiera EA-objekt.
- Hjälp mig ta fram en förmågemodell för organisationen.
- Granska vår befintliga förmågekatalog.
- Identifiera vilka IT-förmågor en stödjande IT-organisation bör erbjuda.
- Analysera våra plattformstjänster och identifiera luckor.
- Ta fram arkitekturprinciper från strategiska mål och drivkrafter.
- Jämför vår modell med relevant omvärldspraxis.

### Leverabler
- Builder-konfiguration,
- användarhandledning.

### Prompt
> Genomför steg 23 i utvecklingsplanen för EA Stödjare. Ta fram conversation starters, normala användarflöden och en kort användarhandledning som speglar GPT:ns viktigaste arbetsuppgifter.

---

## Steg 24 – Skapa strukturell validering

### Mål
Automatiskt hitta tekniska fel i projektet.

### Genomför
Validera exempelvis:
- YAML-syntax,
- schema,
- unika ID:n,
- referensintegritet,
- tillåtna relationer,
- manifest,
- filstruktur,
- genererade artefakter.

### Leverabler
- `scripts/validate_project.py`
- tester.

### Prompt
> Genomför steg 24 i utvecklingsplanen för EA Stödjare. Implementera strukturell och referentiell projektvalidering med tydliga felmeddelanden och automatiserade tester.

---

## Steg 25 – Skapa semantiska evals

### Mål
Testa att GPT:n faktiskt resonerar korrekt som EA-stöd.

### Testområden
- klassificering,
- drivkraft vs mål,
- förmåga vs funktion,
- IT-stöd vs plattformstjänst,
- plattformstjänst vs plattform,
- explicit vs derived vs proposed,
- extern research,
- dubblettidentifiering,
- luckanalys,
- modellförslag,
- otillräckligt underlag,
- motstridiga källor,
- lösningsarkitektur utanför scope.

### Leverabler
- `evals/`
- bedömningskriterier.

### Prompt
> Genomför steg 25 i utvecklingsplanen för EA Stödjare. Skapa en första komplett eval-svit som testar GPT:ns semantiska EA-beteende, evidensdisciplin, research och scopekontroll.

---

## Steg 26 – Stresstesta med realistiska EA-scenarier

### Mål
Testa modellen mot verkligt svåra situationer.

### Scenarier
Minst:
1. från strategi till drivkrafter/mål,
2. från ostrukturerat IT-underlag till förmågekatalog,
3. stödjande IT-område som behöver identifiera IT-förmågor,
4. inventering av IT-stöd,
5. plattform vs plattformstjänst,
6. standarder och principer,
7. fragmenterat och motsägelsefullt underlag,
8. modellförslag som kräver omvärldsresearch,
9. befintlig modell med dubbletter och fel nivåer,
10. underlag där GPT:n bör avstå från att dra starka slutsatser.

### Leverabler
- `tests/scenarios/`
- stresstestrapport.

### Prompt
> Genomför steg 26 i utvecklingsplanen för EA Stödjare. Stresstesta GPT-konceptet och metamodel v1 mot realistiska enterprise architecture-scenarier och implementera nödvändiga korrigeringar.

---

## Steg 27 – GitHub Actions, release och reproducerbar paketering

### Mål
Göra projektet versionshanterat och reproducerbart.

### Genomför
Skapa Actions för:
- validate,
- tests,
- generering,
- export,
- releasepaket.

Versionsnummer bör komma från Git/release där det är lämpligt.

### Leverabler
- `.github/workflows/`
- releasepaket,
- dokumenterade releaseinstruktioner.

### Prompt
> Genomför steg 27 i utvecklingsplanen för EA Stödjare. Inför reproducerbar GitHub Actions-validering, export och releasepaketering med versionsinformation från Git där det är lämpligt.

---

## Steg 28 – Slutlig helhetsrevision och releasekandidat v1.0.0

### Mål
Avgöra om EA Stödjare är redo för praktisk användning.

### Genomför
Kontrollera:
- produktvision,
- scope,
- metamodel,
- relationer,
- YAML-schema,
- research,
- evidensdisciplin,
- modellförslag,
- dokumentgenerering,
- export,
- Builder-instruktion,
- Knowledge,
- evals,
- validering,
- dokumentation,
- releasepaket.

Genomför även några fullständiga end-to-end-tester.

### Leverabler
- slutrapport,
- CHANGELOG,
- release candidate,
- komplett projekt-zip.

### Prompt
> Genomför steg 28 i utvecklingsplanen för EA Stödjare. Gör en fullständig helhetsrevision mot produktvisionen och samtliga tidigare steg, åtgärda kvarvarande problem och ta fram releasekandidat v1.0.0.

---

# 6. Rekommenderad ordning och grindar

Planen bör genomföras sekventiellt.

Särskilt viktiga beslutspunkter är:

```text
Steg 1    Produktgräns
   ↓
Steg 3–6  Metamodel och kanoniskt format
   ↓
Steg 9–12 Analys-, research- och klassificeringsbeteende
   ↓
Steg 13–14 Kvalitetsmodell
   ↓
Steg 15–18 Output
   ↓
Steg 21–23 Custom GPT
   ↓
Steg 24–26 Validering och eval
   ↓
Steg 27–28 Release
```

Metamodel bör betraktas som preliminärt låst efter steg 6. Stresstest i steg 26 får fortfarande förändra modellen om verkliga problem identifieras, men förändringar ska då vara medvetna och migreras konsekvent.

---

# 7. Tre centrala arbetslägen

## Läge A – Extraktion

Utgångspunkt:

> Här är vår befintliga dokumentation. Vad säger den?

GPT:n prioriterar användarens underlag och identifierar explicit och härledd information.

## Läge B – Analys och komplettering

Utgångspunkt:

> Här är vår befintliga modell. Vad saknas eller verkar fel?

GPT:n kombinerar:
- användarens modell,
- generell EA-kunskap,
- relevant research.

## Läge C – Modellförslag

Utgångspunkt:

> Vi behöver en förmågemodell för den här typen av organisation. Hjälp oss ta fram en lämplig struktur.

GPT:n:
1. analyserar organisationskontexten,
2. inventerar kända drivkrafter och mål,
3. identifierar vad som kan härledas från underlaget,
4. genomför relevant research,
5. jämför flera möjliga modeller,
6. föreslår en struktur,
7. markerar vilka delar som är externa rekommendationer,
8. redovisar antaganden och osäkerheter,
9. hjälper användaren iterera modellen.

Detta läge är centralt för produktens värde och ska inte betraktas som en bonusfunktion.

---

# 8. Princip för användning av omvärldsinformation

EA Stödjare ska inte behandla "best practice" som universell sanning.

Extern information bör kategoriseras, exempelvis:

- normativ standard,
- etablerat ramverk,
- myndighets-/branschrekommendation,
- dokumenterad praxis hos jämförbar organisation,
- produkt-/leverantörsdokumentation,
- generell branschpraxis,
- enskilt exempel.

GPT:n ska också bedöma:
- relevans,
- aktualitet,
- överförbarhet,
- källans auktoritet,
- potentiell leverantörsbias.

Ett externt exempel ska därför kunna uttryckas ungefär:

> Detta är ett relevant jämförelseexempel, men det innebär inte i sig att samma modell är lämplig för er organisation.

---

# 9. Vad vi medvetet skjuter på framtiden

När v1 är stabil kan en senare utvecklingsplan omfatta:

- visualisering från relationsmodellen,
- draw.io,
- Gliffy,
- ArchiMate-export,
- grafdatabas/grafanalys,
- interaktiva beroendevyer,
- heatmaps,
- capability maturity,
- roadmap/transitionsarkitektur,
- applikationsportföljanalys,
- informationsdomäner,
- organisationsobjekt,
- mer avancerad strategi-till-arkitektur-spårbarhet,
- separat GPT för lösningsarkitektur.

Det viktiga i v1 är att datamodellen inte blockerar dessa möjligheter, utan att de behöver implementeras nu.

---

# 10. Definition of Done för EA Stödjare v1

Version 1 kan betraktas som färdig när GPT:n på ett stabilt sätt kan:

1. läsa och förstå ett EA-projekt,
2. analysera nya underlag,
3. identifiera och klassificera EA-objekt,
4. skilja fakta, härledning, externa uppgifter och egna förslag,
5. använda aktuell extern research när det är relevant,
6. hjälpa till att utforma en modell för en organisation eller domän,
7. skapa och uppdatera YAML-modellen,
8. hantera relationer och proveniens,
9. upptäcka vanliga modellproblem,
10. generera Markdown och Confluence markup,
11. generera DOCX och PDF,
12. validera projektet,
13. fortsätta arbetet över flera revisioner,
14. fungera som Custom GPT,
15. hålla detaljerad lösningsarkitektur utanför scope.
