# Revisionslogg – EA Stödjare utvecklings-/referensprojekt

## Revision 1 – 2026-08-20

- Manifeststyrt projektformat v1 infördes i utvecklings-/referensprojektet.
- `project-manifest.json`, `docs/project-format.md` och JSON Schema för manifestet infördes.
- Kanoniska modell-, schema- och styrande källfiler registrerades med SHA-256.
- Tidigare utvecklingssteg 1–6 mappas inte retroaktivt till projektrevisioner.

## Revision 2 – 2026-08-20

- Steg 8 genomfört: projektstatus och arbetsläge infördes.
- `PROJECT_STATUS.md` etablerades som mänskligt läsbar återupptagningspunkt.
- `knowledge/project-status-rules.md` infördes med regler för status, återupptagning, öppna frågor, konflikter och uppdateringsordning.
- Minimal exempelmodell kompletterades med egen statusfil.
- README uppdaterades till steg 8 av 28.

## Revision 3 – steg 9

- Infört `knowledge/workflow-extraction.md` som kanoniskt arbetsflöde för extraktion ur underlag.
- Etablerat principen kandidat före kanon samt separata faser för explicit extraktion, härledning, relationer, osäkerhet, normalisering, dubblettkontroll och förslag.
- Definierat riskbaserade regler för när modelländringar kan införas direkt respektive bör presenteras för granskning först.
- Lagt till fyra syntetiska testexempel under `tests/extraction/`.
- Uppdaterat README och projektstatus för steg 9.


## Revision 4 – steg 10

- Infört `knowledge/workflow-research.md` som kanoniskt arbetsflöde för research och omvärldsanalys.
- Infört `docs/source-policy.md` med källhierarki, primärkälleprincip, peer-/leverantörsbedömning, aktualitet och triangulering.
- Definierat när research ska initieras respektive undvikas.
- Etablerat research i tre lager: normativt/etablerat, jämförbara organisationer och bredare praxis.
- Fastställt att organisationsspecifika slutsatser som bygger på extern research normalt ska vara `proposed`, medan externa källor sparas som stödjande `external` evidens.
- Infört explicit bedömning av överförbarhet och regler för att skilja etablerad praxis från enskilda exempel.
- Uppdaterat README och projektstatus för steg 10.

## Revision 5 – steg 11

- Infört `knowledge/workflow-model-design.md` som kanoniskt arbetsflöde för modellförslag.
- Etablerat principerna kontext före struktur, kandidat före kanon och minsta tillräckliga modell.
- Definierat hur alternativa modellstrukturer tas fram och kvalitativt jämförs när verkliga strukturval finns.
- Definierat hur organisationskontext, internt underlag, generell EA-kunskap och extern research kombineras utan att externa exempel blir intern sanning.
- Infört tre outputnivåer: skiss, granskningsförslag och kanoniseringsförslag.
- Förtydligat modellering av IT-förmågor för stödjande utvecklingsområden.
- Uppdaterat README och projektstatus för steg 11.


## Revision 6 – steg 12

- Tillagt `knowledge/classification-guide.md`.
- Fastställt beslutsordning för klassificering och centrala semantiska gränsdragningar.
- Definierat normaliseringsregler, alias/dubblett/överlapp och hantering av osäker eller sammansatt klassificering.
- Uppdaterat README och projektstatus.

## Revision 7 – steg 13

- Infört `knowledge/quality-object.md` med gemensamma och objektspecifika kvalitetsregler för enskilda EA-objekt.
- Infört `schemas/object-quality-rules.yaml` med maskinläsbara regel-ID:n, severity och aggregeringsregler.
- Etablerat nivåerna ERROR, WARNING och INFO samt resultaten GODKÄND, GODKÄND MED VARNINGAR och BLOCKERAD.
- Definierat kontroller för ID, namn, beskrivning, klassificering, proveniens, status, relationer, dubbletter och terminologi.
- Definierat objektspecifika kontroller för samtliga primära och sekundära objekttyper samt `functions[]`.
- Fastställt att kvalitetsresultat inte automatiskt ändrar ett objekts livscykelstatus.
- Uppdaterat README och projektstatus för steg 13.

## Revision 8 – steg 14

- Infört `knowledge/quality-model.md` med helhetskontroll för EA-modellen.
- Infört `schemas/model-quality-rules.yaml` med maskinläsbara `QM-*`-regler och severity.
- Definierat kontroller för referentiell integritet, orphans, strategisk spårbarhet, dubbletter/överlapp, konsistens, täckning, grafstruktur, styrning och proveniens.
- Infört täckningsprofilerna `catalog`, `strategy_to_capability`, `capability_to_it` och `full_ea_v1`.
- Fastställt att dokumentationsluckor, möjliga arkitekturluckor och bekräftade arkitekturluckor ska skiljas åt.
- Fastställt att deterministiska grafmått endast är signaler och inte ensamma får bli semantiska slutsatser.
- Uppdaterat README och projektstatus för steg 14.


## Revision 9 – steg 15

- Infört `docs/documentation-profiles.md` med Markdown-profiler för katalog- och detaljvyer.
- Infört `templates/markdown/` med 20 mallkontrakt: katalog och detalj för samtliga tio objekttyper.
- Definierat `working` och `published` som presentationslägen utan påverkan på kanonisk modellstatus.
- Fastställt sortering, filnamn, länkning, relationer, funktioner, proveniens och hantering av tomma sektioner.
- Fastställt att genererad Markdown alltid är derivat av YAML-modellen och inte får bli parallell source of truth.
- Uppdaterat README och projektstatus för steg 15.


## Revision 10 – steg 16

- Implementerat `scripts/generate_markdown.py` för deterministisk generering av Markdown från den kanoniska YAML-modellen.
- Implementerat katalog- och detaljrendering för samtliga tio objekttyper.
- Implementerat `working` och `published`, relativa interna länkar, relationsrendering, funktioner och proveniens.
- Lagt till `docs/markdown-generation.md` och genererad referensoutput i minimalmodellen.
- Lagt till regressionstest som verifierar byte-stabil omkörning och filtrering av kandidater i publiceringsläge.
- Uppdaterat README och projektstatus till steg 16.

## Revision 11 – steg 17

- Implementerat `scripts/generate_confluence.py` för deterministisk Confluence wiki markup-export från den kanoniska YAML-modellen.
- Implementerat katalog- och detaljrendering för samtliga tio objekttyper.
- Implementerat samma `working`/`published`-filtrering, relationer, funktioner och proveniens som Markdown-exporten.
- Lagt till `docs/confluence-generation.md` och genererad Confluence-referensoutput i minimalmodellen.
- Lagt till regressionstest som verifierar byte-stabil omkörning och semantisk objektsynk mellan Markdown och Confluence.
- Uppdaterat README och projektstatus till steg 17.



## Revision 12 – steg 18

- Implementerat `scripts/export_documents.py` för reproducerbar DOCX- och PDF-export från den kanoniska YAML-modellen via genererad Markdown.
- Infört Pandoc-baserad DOCX-generering med titel, metadata, innehållsförteckning, kataloger och detaljsektioner.
- Infört PDF-export genom LibreOffice från samma DOCX-layoutbas.
- Lagt till `docs/document-export.md` och regressionstest för `working`/`published`.
- Lagt till DOCX/PDF-referensexporter för minimalmodellen.
- Fastställt att DOCX/PDF är derivat och aldrig parallella sanningskällor.
- Uppdaterat README och projektstatus till steg 18.

## Revision 13 – steg 19

- Infört `knowledge/workflow-update.md` som kanoniskt arbetsflöde för inkrementella modelländringar.
- Definierat preflight-integritet, scopeklassificering och principen minsta nödvändiga ändring.
- Definierat säker hantering av nya/ändrade objekt, typbyte, sammanslagning, uppdelning, avveckling och fysisk borttagning.
- Fastställt explicit synk av relationer, källor och proveniens samt stabil ID-hantering.
- Fastställt en projektrevision per sammanhållen ändring, regenerering av derivat och konkret diffrapportering.
- Uppdaterat README och projektstatus till steg 19.

## Revision 14 – steg 20

- Infört `knowledge/conflicts-and-uncertainty.md` med fullständig modell för konflikter, osäkerhet, confidence, blockeringsgrad och beslutsbehov.
- Infört `schemas/conflicts-and-uncertainty.yaml` med maskinläsbar semantik och valideringsregler för issue-poster.
- Fastställt separation mellan objektlivscykel (`candidate`, `approved`, `deprecated`, `retired`), evidenstyp, confidence och frågans lösningsstatus (`open`, `monitoring`, `resolved`, `superseded`).
- Fastställt att `obsolete` inte införs som ny objektstatus i v1 utan hanteras via `deprecated`/`retired` respektive `superseded` beroende på betydelse.
- Definierat source conflict, classification uncertainty, scope uncertainty, relationship uncertainty, temporal conflict, terminology conflict och missing decision.
- Uppdaterat projektstatusregler, README och PROJECT_STATUS för steg 20.

## Revision 15 – steg 21

- Infört `custom-gpt/instructions.md` som första kompletta Builder-instruktion för Custom GPT-versionen av EA Stödjare.
- Samlat roll, scope, arbetsprinciper, evidensdisciplin, research, klassificering, modellarbete, konflikt-/osäkerhetshantering, kvalitet, projekt-/filhantering, export och avgränsningar i en kompakt huvudinstruktion.
- Fastställt att detaljerade metamodel-, relations-, proveniens-, kvalitets- och arbetsflödesregler fortsatt ska ligga i Builder Knowledge.
- Verifierat att Builder-instruktionen är under 8 000 tecken.
- Uppdaterat README och PROJECT_STATUS till steg 21.

## Revision 16 – steg 22

- Infört `custom-gpt/knowledge/` med ett Knowledge-index och fem tematiska Builder Knowledge-paket.
- Konsoliderat domänmodell/klassificering, evidens/research, analys-/modelleringsflöden, kvalitet samt projekt/output utan intern onödig duplicering.
- Infört `scripts/build_builder_knowledge.py` så Builder Knowledge genereras deterministiskt från kanoniska styrdokument.
- Infört `tests/builder/test_builder_knowledge.py` som verifierar filuppsättning och byte-stabil generering.
- Fastställt att Builder Knowledge är distributionsartefakt och inte en parallell source of truth.
- Uppdaterat README och PROJECT_STATUS till steg 22.

## Revision 17 – steg 23

- Infört `custom-gpt/builder-config.md` som praktisk konfigurationsguide för Custom GPT Builder.
- Fastställt fyra primära conversation starters som täcker underlagsanalys, modellframtagning, modellgranskning och omvärldsjämförelse.
- Infört `knowledge/workflow-usage.md` med sex normala användarflöden och regler för hur rätt flöde väljs/kombineras.
- Infört `docs/user-guide.md` med kort svensk användarhandledning och konkreta promptmönster.
- Utökat deterministiskt Builder Knowledge så normala användarflöden ingår i analys-/modelleringspaketet.
- Uppdaterat README och PROJECT_STATUS till steg 23.

## Revision 18 – steg 24

- Infört `scripts/validate_project.py` för deterministisk strukturell validering av EA Stödjare-projekt.
- Valideringen omfattar manifest/JSON Schema, SHA-256, obligatorisk filstruktur, YAML-envelope, objekttyper, stabila och unika ID:n, statusvärden, funktioner, källregister och proveniens.
- Implementerat referentiell och semantisk relationsvalidering mot `schemas/relations.yaml`, inklusive source/target constraints och dubblettrelationer.
- Infört kontroll av lagrade genererade Markdown- och Confluence-artefakter genom deterministisk regenerering samt grundläggande signaturkontroll för DOCX/PDF.
- Infört `tests/validation/test_validate_project.py` med både giltiga projekt och avsiktligt trasiga fall.
- Lagt till `docs/structural-validation.md` och inkluderat den i genererat Builder Knowledge.
- Uppdaterat README och PROJECT_STATUS till steg 24.

## Revision 19 – steg 25

- Infört `evals/eval-suite.yaml` med 15 semantiska evalfall som täcker de riskområden som definierats i utvecklingsplanen.
- Markerat 12 högriskfall som blockerande för release.
- Infört bedömningsrubrik för klassificering, evidensdisciplin, osäkerhet, EA-nytta och scope.
- Infört separat researchrubrik för källval, aktualitet, överförbarhet, leverantörsbias och extern proveniens.
- Infört kritiska fel för bland annat fabricerade källor, påhittade interna fakta, tyst konfliktlösning och detaljerad lösningsdesign vid scope-test.
- Infört `schemas/semantic-eval.schema.json` och `tests/evals/test_eval_suite.py` för maskinell validering av eval-svitens definitioner och täckning.
- Fastställt releasegrind: alla blockerande fall ska vara PASS och viktad totalpoäng ska vara minst 85 %.
- Uppdaterat README och PROJECT_STATUS till steg 25.



## Revision 20 – steg 26

- Infört `tests/scenarios/` med tio realistiska syntetiska EA-stresstestscenarier.
- Infört `docs/stress-test-report.md` med scenarioresultat, designfynd, kvarvarande risker och bedömning inför steg 27.
- Stresstestat strategi→mål, förmågeextraktion, stödjande IT-förmågor, IT-stödsinventering, Plattform/Plattformstjänst, Princip/Standard, källkonflikter, researchbaserat modellförslag, dubbletter/fel nivåer och otillräckligt underlag.
- Kompletterat Förmåga med valfritt `consumer_scope` för lättviktig konsumentkontext utan att införa Organisation som kärnobjekttyp.
- Bekräftat att Funktion kan förbli underordnat attribut och att Lösningsmönster/Referensarkitektur kan förbli sekundära i v1.
- Bekräftat att detaljerad lösningsarkitektur fortsatt ska ligga utanför v1-scope.
- Korrigerat README:s utvecklingsstatus och uppdaterat PROJECT_STATUS till steg 26.

## Revision 21 – steg 27

- Infört `.github/workflows/ci.yml` för strukturell validering, hela testsuiten, reproducerbar Builder Knowledge och DOCX/PDF-smoketest.
- Infört `.github/workflows/build-artifacts.yml` för manuell generering av Markdown-, Confluence-, DOCX- och PDF-referensartefakter.
- Infört `.github/workflows/release.yml` som på semantiska Git-taggar validerar, testar, paketerar, återvaliderar uppackad release och skapar GitHub Release.
- Infört `scripts/package_release.py` för deterministisk, versionsmärkt release-zip med Git-taggen som normal versionskälla.
- Infört `tests/release/test_package_release.py` för determinism, exkluderingsregler och semvervalidering.
- Infört `.gitignore`, `requirements-dev.txt` och `docs/release-and-ci.md`.
- Rensat runtime-cachefiler från projektets distributions-/integritetsmodell så att releaser inte påverkas av lokala pytest-/Python-cacher.
- Uppdaterat README och PROJECT_STATUS till steg 27.

## Revision 22 – steg 28

- Genomfört slutlig helhetsrevision mot produktvision och utvecklingsplan steg 1–28.
- Infört `docs/final-review.md` med releasebeslut, verifieringsresultat, kända kvarvarande risker och acceptansvillkor.
- Infört `CHANGELOG.md` för releasekandidat v1.0.0-rc1.
- Infört `tests/release/test_end_to_end_release.py` som bygger, packar upp och validerar en komplett releasekandidat.
- Uppdaterat README och PROJECT_STATUS till steg 28 av 28 och releasekandidatstatus.
- Fastställt att faktisk semantisk runtime-eval i Custom GPT Builder är sista acceptanskontroll före sluttagg v1.0.0.

