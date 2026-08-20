# Projektstatus – EA Stödjare

## Statusöversikt

- **Projekt:** EA Stödjare – utvecklings- och referensprojekt
- **Utvecklingsplan:** steg 28 av 28 genomfört
- **Projektrevision:** 22
- **Livscykelstatus:** review
- **Metamodell:** v1.0
- **Relationsmodell:** v1.0
- **Proveniensmodell:** v1.0
- **Modellformat:** v1.0
- **Senast uppdaterad:** 2026-08-20

## Syfte med denna statusfil

`PROJECT_STATUS.md` är projektets mänskligt läsbara återupptagningspunkt. Den ska göra det möjligt för en ny chat eller en ny arbetsomgång att förstå vad som är färdigt, vad som är preliminärt och vad som bör göras härnäst utan att behöva rekonstruera tidigare konversationer.

Statusfilen är **inte source of truth för EA-objekten**. Den kanoniska EA-modellen finns i `model/`. Statusfilen beskriver arbetsläget kring modellen och projektet.

## Genomförda utvecklingssteg

1. Produktvision och scope.
2. Återbruksanalys från Lärobokskaparen.
3. EA-metamodell v1.
4. Relationsmodell v1.
5. Proveniens- och evidensmodell v1.
6. Kanoniskt YAML-format v1.
7. Projektformat och manifest v1.
8. Projektstatus och arbetsläge.
9. Arbetsflöde för extraktion ur underlag.
10. Arbetsflöde för research och omvärldsanalys.
11. Arbetsflöde för modellförslag.
12. Normaliserings- och klassificeringsregler.
13. Kvalitetskontroll för enskilda objekt.
14. Kvalitetskontroll för hela modellen.
15. Markdown-dokumentationsprofiler.
16. Deterministisk Markdown-generering.
17. Deterministisk Confluence markup-export.
18. Reproducerbar DOCX- och PDF-export.
19. Ändrings- och uppdateringsarbetsflöde.
20. Konflikthantering och osäkerhetsmodell.
21. Builder-instruktion för Custom GPT.
22. Builder Knowledge för Custom GPT.
23. Conversation starters, normala användarflöden och användarhandledning.
24. Strukturell validering.
25. Semantiska evals.
26. Stresstest med realistiska EA-scenarier.
27. GitHub Actions, release och reproducerbar paketering.
28. Slutlig helhetsrevision och releasekandidat v1.0.0-rc1.

## Etablerade projektartefakter

- Produktvision och v1-avgränsning.
- Teknisk målbild och återbruksbeslut.
- Metamodell för primära och sekundära EA-objekt.
- Relationsmodell med begränsat relationsvokabulär.
- Proveniensmodell med `explicit`, `derived`, `proposed` och `external`.
- Kanoniskt YAML-format och minimal exempelmodell.
- Manifestformat med revisioner och SHA-256-integritet.
- Regler för projektstatus och återupptagning.
- Extraktionsarbetsflöde med kandidatfas, klassificering, proveniens, normalisering och kontrollerat införande i kanonisk modell.
- Fyra syntetiska regressionsexempel för centrala extraktionsbeteenden.
- Researcharbetsflöde och källpolicy.
- Modellförslagsarbetsflöde med alternativjämförelse, rekommendation, antaganden och kanonisering.
- Objektspecifik kvalitetskontroll med gemensamma regler, severity-nivåer och maskinläsbara regel-ID:n.
- Helhetskontroll för modellen med scopeprofiler, spårbarhet, orphans, dubbletter, konsistens, täckning, grafmönster, styrning och proveniens.
- Markdown-dokumentationsprofiler och mallkontrakt för katalog- och detaljvyer.
- Deterministisk Markdown-generator med `working`/`published`, relativa länkar, relationer, funktioner, proveniens och regressionstest.
- Deterministisk Confluence wiki markup-generator med samma statusfilter, objektuppsättning, relationer, funktioner och proveniens som Markdown.
- DOCX/PDF-exportkedja via genererad Markdown, Pandoc och LibreOffice med samma kanoniska YAML som ursprung.
- Regressionstest för `working`/`published`, kandidatfiltrering och parsbar DOCX/PDF.
- Säkert inkrementellt uppdateringsarbetsflöde med preflight, scope, stabil identitet, relations-/provenienssynk, revision, regenerering, validering och diffrapportering.
- Konflikt- och osäkerhetsmodell som separerar livscykel, evidens, confidence och issue-status samt definierar source conflicts, klassificerings-/scope-/relationsosäkerhet, tidskonflikter och beslutsbehov.
- Första kompletta Builder-instruktionen för Custom GPT med kompakt styrning av roll, scope, evidens, research, klassificering, modellhantering, kvalitet, filhantering, export och avgränsningar.
- Deterministiskt Builder Knowledge-paket med index och fem tematiska kunskapsfiler genererade från kanoniska styrdokument.
- Generator och regressionstest som förhindrar manuell drift mellan projektversionen och Custom GPT:s Knowledge.
- Builder-konfigurationsguide med fyra primära conversation starters och rekommenderade capabilities.
- Normala användarflöden för analys, modellförslag, granskning, uppdatering, research och dokumentation/export.
- Kort användarhandledning med konkreta promptmönster och vägledning för centrala EA-begrepp.
- Deterministisk strukturell validator för manifest, checksumma, YAML-format, ID:n, källor, proveniens, relationer och genererade artefakter.
- Regressionstest för både giltiga projekt och avsiktligt felaktiga strukturer.
- Semantisk eval-svit med 15 fall för klassificering, evidens, research, modellförslag, osäkerhet, konflikter, luckanalys och scopekontroll.
- Bedömningsrubriker för semantiskt EA-beteende och research/överförbarhet samt releasegrind med blockerande fall.
- GitHub Actions för CI, manuell artefaktbyggnad och taggbaserad release.
- Deterministisk releasepaketering med Git-taggen som normal versionskälla och SHA-256-metadata.
- Reproducerbarhetsregler som exkluderar cache-/byggartefakter och verifierar att release-zippen kan valideras efter uppackning.

## Analyserat underlag

Detta utvecklings-/referensprojekt innehåller ännu inget organisationsspecifikt analysunderlag. De modeller som finns under `model/` och `examples/` är syntetiska referens-/exempeldata för utveckling och validering.

När EA Stödjare används i ett konkret EA-projekt ska denna sektion sammanfatta vilka underlag som faktiskt har analyserats och deras status, exempelvis:

- källa/dokument,
- datum eller version,
- om analysen är komplett eller partiell,
- vilka modelldelar underlaget påverkat.

## Modellstatus

- **Kanonisk modell:** etablerad strukturellt men innehåller endast referens-/exempeldata.
- **Primära objekttyper:** definierade.
- **Sekundära objekttyper:** definierade på metamodelnivå.
- **Relationer:** definierade och exemplifierade.
- **Proveniens:** definierad och exemplifierad.
- **Organisationsspecifik modell:** ännu inte skapad.

## Preliminära delar

Efter stresstestet i steg 26 återstår följande som medvetet preliminärt inför framtida versioner:

- exakt djup för Lösningsmönster och Referensarkitektur i v1,
- om ytterligare capability-subtyper behövs utöver `business` och `it`,
- om lättviktigt `consumer_scope` på sikt behöver ersättas/kompletteras av explicit organisationsmodellering,
- om funktioner på sikt behöver egna stabila ID:n,
- detaljer kring framtida visualisering och eventuell ArchiMate-mappning.

Dessa frågor ska inte blockera steg 9–26 så länge nuvarande v1-format räcker.

## Öppna frågor

Inga blockerande öppna frågor finns efter steg 20.

Frågor som ska bevakas i kommande steg:

1. Behöver sekundära objekttyper egna särskilda arbetsflöden före v1.0.0?
2. Behöver `working`/`published` senare kompletteras med ytterligare exportprofiler efter praktiska tester?
3. Behöver viktning eller blockeringsgrad i eval-sviten justeras efter runtime-körning av scenarier/evals i steg 28?

## Kända konflikter

Inga kända semantiska eller strukturella konflikter är registrerade efter steg 20.

I konkreta EA-projekt ska materiella konflikter och osäkerheter hanteras enligt `knowledge/conflicts-and-uncertainty.md`. Statusfilen sammanfattar aktiva frågor; ett separat issue-register kan användas när antalet eller komplexiteten motiverar det.

## Senaste kvalitetskontroll

**Kontrollnivå:** CI-/release-, regression- och integritetskontroll för steg 27.

Kontrollerat:

- GitHub Actions-workflows kan YAML-parsas och använder explicit Python-/verktygskedja,
- strukturell validator och hela pytest-sviten körs i CI/release,
- Builder Knowledge kontrolleras byte-stabilt i CI,
- DOCX/PDF-export smoke-testas i CI,
- releaseversion hämtas normalt från Git-taggen och valideras som semver,
- två releasepaketeringar från identiskt källträd/version ger identisk SHA-256,
- cache-, bytecode- och buildkataloger exkluderas från releasepaketet,
- det uppackade releasepaketet valideras innan GitHub Release skapas.

## Slutlig kvalitetskontroll – steg 28

**Bedömning:** GODKÄND SOM RELEASEKANDIDAT v1.0.0-rc1.

Verifierat i slutrevisionen:

- strukturell validering: 0 fel, 0 varningar,
- Builder/eval/release/scenario-regressioner: gröna,
- validatorns positiva/negativa tester: gröna,
- Markdown och Confluence: deterministiska och semantiskt synkade,
- DOCX/PDF: exporterbara i `working` och `published`,
- releasepaket: deterministiskt, uppackningsbart och validerbart,
- Builder-instruktionen ligger under 8 000 tecken,
- inga nya kärnobjekt behövs efter helhetsrevisionen.

Se `docs/final-review.md` för fullständig releasebedömning.

## Rekommenderat nästa steg

Utvecklingsplanen 1–28 är slutförd. Nästa aktivitet är **praktisk acceptans av v1.0.0-rc1 i Custom GPT Builder**:

1. importera Builder-instruktion och Knowledge,
2. aktivera rekommenderade capabilities,
3. kör de 15 semantiska evalfallen mot den faktiska GPT-instansen,
4. verifiera minst ett realistiskt organisationsspecifikt EA-underlag,
5. publicera sluttagg `v1.0.0` om releasegrinden uppfylls.

## Återupptagningsinstruktion

Vid fortsatt arbete:

1. Läs `project-manifest.json` och verifiera integriteten innan ändringar.
2. Läs denna `PROJECT_STATUS.md`.
3. Läs relevant steg i `docs/development-plan.md`.
4. Läs endast de styrande dokument/schemafiler som behövs för det aktuella steget.
5. Ändra endast filer som steget kräver.
6. Uppdatera `PROJECT_STATUS.md` efter genomfört arbete.
7. Öka projektrevisionen exakt en gång när projektinnehållet ändras.
8. Uppdatera `revision-log.md`.
9. Uppdatera manifestets filinventering/checksummor sist.
