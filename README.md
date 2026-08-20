# EA Stödjare

**Status:** Releasekandidat – v1.0.0-rc1, steg 28 av 28 genomfört

EA Stödjare är ett planerat AI-baserat stöd för arbete med **enterprise architecture (EA)**. Projektets första version ska hjälpa användare att analysera underlag, identifiera och strukturera centrala EA-objekt, komplettera analysen med relevant generell kunskap och aktuell omvärldsresearch samt generera konsistent arkitekturdokumentation från en strukturerad modell.

EA Stödjare ska vara ett **analys-, research-, modellerings- och dokumentationsstöd**. Den ska inte vara en generell lösningsarkitekt i version 1.

## Produktvision

Den kanoniska produktvisionen och v1-avgränsningen finns i:

- [`docs/product-vision.md`](docs/product-vision.md)

## Utvecklingsplan

Den stegvisa utvecklingsplanen finns i:

- [`docs/development-plan.md`](docs/development-plan.md)

Varje steg är utformat för att kunna genomföras i en separat prompt. Samtliga **28 av 28 steg är nu genomförda**. Slutrevisionen finns i [`docs/final-review.md`](docs/final-review.md) och projektet är paketerat som **v1.0.0-rc1** för praktisk Builder-import och acceptanstestning före sluttagg `v1.0.0`.

## V1 i korthet

### Primära EA-objekt

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

### Sekundära EA-objekt

- Lösningsmönster
- Referensarkitektur

### Övergripande arbetssätt

EA Stödjare ska kunna:

1. analysera användarens underlag,
2. identifiera och klassificera EA-objekt,
3. skilja mellan explicit information, härledning, externa uppgifter och egna förslag,
4. använda relevant extern research när uppgiften kräver det,
5. hjälpa till att föreslå hur en EA-modell för en organisation eller domän kan se ut,
6. förvalta en strukturerad modell med YAML som source of truth,
7. generera dokumentation från modellen.

## Uttryckligen utanför v1

Bland annat:

- detaljerad lösningsarkitektur,
- komponentdesign,
- API-design,
- detaljerade integrationskontrakt,
- databasdesign,
- deployment- och nätverksdesign,
- detaljerad säkerhetsdesign,
- full ArchiMate-modellering,
- automatisk diagramgenerering.

## Återbruk från Lärobokskaparen

Steg 2 fastställer vilka mekanismer från Lärobokskaparen som ska återanvändas och vilka som är bokdomänspecifika. Se:

- [`docs/reuse-analysis.md`](docs/reuse-analysis.md)
- [`docs/technical-target.md`](docs/technical-target.md)

Huvudprincipen är att återanvända projekt-, revisions-, integritets-, distributions- och kvalitetsmönster, men bygga EA Stödjares metamodel och arbetsflöden domänspecifikt.

## Metamodell v1

Den kanoniska definitionen av objekttyper och gränsdragningar finns i:

- [`docs/metamodel.md`](docs/metamodel.md)
- [`schemas/object-types.yaml`](schemas/object-types.yaml)

Metamodellen fastställer åtta primära objekttyper, två sekundära objekttyper samt Funktion som ett underordnat begrepp på IT-stöd, Plattformstjänst och Plattform.

## Relationsmodell v1

Den kanoniska relationssemantiken finns i:

- [`docs/relations.md`](docs/relations.md)
- [`schemas/relations.yaml`](schemas/relations.yaml)

Relationsmodellen använder nio avsiktligt begränsade relationstyper och definierar maskinläsbart vilka source/target-kombinationer som är tillåtna. Inversa formuleringar används endast vid presentation och lagras inte som separata relationer.

## Proveniens- och evidensmodell v1

Den kanoniska proveniens- och evidensmodellen finns i:

- [`docs/provenance-model.md`](docs/provenance-model.md)
- [`schemas/provenance.yaml`](schemas/provenance.yaml)

Modellen skiljer mellan `explicit`, `derived`, `proposed` och `external`, stödjer separata källregister, härledningskedjor, kvalitativ confidence och bedömning av extern informations överförbarhet. Samma modell gäller för både EA-objekt och relationer.

## Kanoniskt YAML-format v1

Serialiseringsformatet och den faktiska modellstrukturen finns i:

- [`docs/yaml-model-format.md`](docs/yaml-model-format.md)
- [`schemas/model-format.yaml`](schemas/model-format.yaml)
- [`model/`](model/)
- [`examples/minimal-model/`](examples/minimal-model/)

YAML-filerna under `model/` är nu definierade som EA-modellens source of truth. Relationer lagras i ett gemensamt register och källor i ett separat källregister. Funktioner ligger fortsatt inbäddade på IT-stöd, Plattformstjänst och Plattform.

## Projektformat och manifest v1

Projektbehållaren och manifestkontraktet finns i:

- [`docs/project-format.md`](docs/project-format.md)
- [`schemas/project-manifest.schema.json`](schemas/project-manifest.schema.json)
- [`project-manifest.json`](project-manifest.json)
- [`revision-log.md`](revision-log.md)

Formatet skiljer projektets monotona revision från metamodel-/relations-/proveniensversionerna. Integritetsskyddade filer inventeras deterministiskt och får SHA-256; manifestet hashar inte sig självt och skrivs sist i en revision. `examples/minimal-model/` innehåller ett konkret exempelmanifest.

## Nytt i steg 12

- `knowledge/classification-guide.md` definierar beslutsregler, exempel och motexempel för centrala EA-gränsdragningar.
- Klassificering ska baseras på semantik snarare än källans etikett.
- Guiden hanterar bland annat Drivkraft/Mål, Mål/Princip, Princip/Standard, Förmåga/Process/Funktion, IT-stöd/Plattformstjänst/Plattform samt Lösningsmönster/Referensarkitektur.
- Osäkra eller sammansatta kandidater ska inte tvångsklassificeras.

## Nytt i steg 13

- `knowledge/quality-object.md` definierar kvalitetskontroll för varje enskilt EA-objekt.
- `schemas/object-quality-rules.yaml` gör kontrollreglerna maskinläsbara med stabila regel-ID:n.
- Kontrollerna skiljer strukturell/formell kvalitet från semantisk EA-kvalitet.
- Gemensamma regler täcker bland annat ID, namn, beskrivning, klassificering, proveniens, status, relationer och dubblettrisk.
- Objektspecifika regler finns för samtliga tio objekttyper samt för inbäddade `functions[]`.
- Resultat rapporteras som `GODKÄND`, `GODKÄND MED VARNINGAR` eller `BLOCKERAD`; kvalitetsresultat ändrar inte automatiskt objektets livscykelstatus.


## Nytt i steg 14

- `knowledge/quality-model.md` definierar kvalitetskontroll för hela EA-modellen.
- `schemas/model-quality-rules.yaml` gör helhetsreglerna maskinläsbara med stabila `QM-*`-regel-ID:n.
- Kontrollen omfattar referentiell integritet, orphans, strategi-till-arkitektur-spårbarhet, dubbletter/överlapp, motsägelser, scope/täckning, grafmönster, styrning och proveniens.
- Fyra täckningsprofiler (`catalog`, `strategy_to_capability`, `capability_to_it`, `full_ea_v1`) förhindrar att modellen bedöms mot irrelevanta lager.
- Luckor ska skiljas mellan **dokumentationslucka**, **möjlig arkitekturlucka** och **bekräftad arkitekturlucka**.
- Deterministiska grafmått används som signaler; semantiska slutsatser kräver fortsatt EA-bedömning.


## Nytt i steg 15

- `docs/documentation-profiles.md` definierar katalog- och detaljprofiler för samtliga tio EA-objekttyper.
- `templates/markdown/` innehåller separata mallkontrakt för kataloger och objektdetaljer.
- Profilerna skiljer `working` från `published` utan att förändra modellens livscykelstatus.
- Relationer, funktioner och proveniens hämtas alltid från den kanoniska YAML-modellen; genererad Markdown får inte bli parallell source of truth.
- Filnamn, sortering, tomma sektioner, interna länkar och Markdown-konventioner är definierade inför steg 16.


## Nytt i steg 16

- `scripts/generate_markdown.py` implementerar deterministisk Markdown-generering från den kanoniska YAML-modellen.
- Generatorn stödjer `working` och `published` och renderar kataloger, detaljsidor, relationer, funktioner och proveniens.
- `docs/markdown-generation.md` dokumenterar användning och determinism.
- `tests/generation/test_generate_markdown.py` verifierar byte-stabil omkörning och publiceringsfiltrering.
- `examples/minimal-model/docs/generated/` innehåller referensoutput från den syntetiska modellen.

## Nytt i steg 17

- `scripts/generate_confluence.py` implementerar deterministisk Confluence wiki markup-export direkt från den kanoniska YAML-modellen.
- Exporten stödjer `working` och `published` med samma statusfiltrering som Markdown-generatorn.
- `docs/confluence-generation.md` dokumenterar syntax, outputstruktur, länkar och semantisk konsistens.
- `tests/generation/test_generate_confluence.py` verifierar byte-stabil omkörning och att Markdown/Confluence genererar samma uppsättning EA-objekt.
- `examples/minimal-model/exports/confluence/` innehåller referensoutput från den syntetiska modellen.

## Nytt i steg 18

- `scripts/export_documents.py` implementerar reproducerbar DOCX- och PDF-export via genererad Markdown, Pandoc och LibreOffice.
- `docs/document-export.md` dokumenterar exportkedja, beroenden, struktur, layoutprinciper och verifiering.
- `tests/generation/test_export_documents.py` verifierar DOCX/PDF i både `working` och `published` samt kandidatfiltrering.
- `examples/minimal-model/exports/document/` innehåller referensexporter i båda presentationslägena.
- DOCX och PDF är uttryckligen derivat av YAML-modellen och får aldrig användas som parallell source of truth.


## Nytt i steg 22

- `custom-gpt/knowledge/00-knowledge-index.md` beskriver läsordning och styrhierarki.
- Fem tematiska Knowledge-paket täcker domänmodell, evidens/research, analys-/modelleringsflöden, kvalitet samt projekt/output.
- `scripts/build_builder_knowledge.py` bygger paketet deterministiskt från kanoniska `docs/`- och `knowledge/`-filer.
- `tests/builder/test_builder_knowledge.py` verifierar komplett filuppsättning och byte-stabil generering.
- Builder Knowledge ska inte handredigeras; ändringar görs i kanoniska källor och regenereras.

## Nytt i steg 23

- `custom-gpt/builder-config.md` beskriver hur Custom GPT Builder ska konfigureras med namn, beskrivning, Instructions, Knowledge, capabilities och fyra primära conversation starters.
- `knowledge/workflow-usage.md` definierar sex normala användarflöden: underlagsanalys, modellförslag, modellgranskning, projektuppdatering, research/jämförelse och dokumentation/export.
- `docs/user-guide.md` ger en kort svensk användarhandledning med konkreta promptmönster och förklaring av centrala begrepp.
- Builder Knowledge-paketet inkluderar nu de normala användarflödena och genereras fortsatt deterministiskt.
- Conversation starters täcker underlagsanalys, modellframtagning, modellgranskning och omvärldsjämförelse utan att överbelasta startsidan.

## Projektstatus och arbetsläge

Den aktuella återupptagningsstatusen finns i:

- [`PROJECT_STATUS.md`](PROJECT_STATUS.md)
- [`knowledge/project-status-rules.md`](knowledge/project-status-rules.md)

Statusfilen sammanfattar analyserat underlag, modellstatus, preliminära delar, öppna frågor, konflikter, senaste kvalitetskontroll och rekommenderat nästa steg utan att duplicera YAML-modellen som source of truth.

## Extraktion ur underlag

Det kanoniska extraktionsarbetsflödet finns i:

- [`knowledge/workflow-extraction.md`](knowledge/workflow-extraction.md)
- [`tests/extraction/`](tests/extraction/)

Arbetsflödet använder principen **kandidat före kanon** och skiljer konsekvent mellan `explicit`, `derived`, `proposed` och `external`. Testfallen täcker bland annat härledning, Plattformstjänst kontra Plattform, utebliven modelländring och dubblett/normalisering.


## Research och omvärldsanalys

Det kanoniska researcharbetsflödet och källpolicyn finns i:

- [`knowledge/workflow-research.md`](knowledge/workflow-research.md)
- [`docs/source-policy.md`](docs/source-policy.md)

Research används proportionerligt och ska särskilt stödja modellförslag, gap-analys och jämförelse mot standarder, ramverk och relevanta peer-organisationer. Externa fynd blir inte automatiskt intern sanning; organisationsspecifika rekommendationer förblir `proposed` och externa källor registreras som stödjande evidens.


## Modellförslag

Det kanoniska arbetsflödet för modellförslag finns i:

- [`knowledge/workflow-model-design.md`](knowledge/workflow-model-design.md)

Arbetsflödet använder kontext före struktur, kandidat före kanon och minsta tillräckliga modell. Det stödjer alternativa modellstrukturer, kvalitativ jämförelse, researchdriven komplettering och tydlig markering av antaganden och organisationsspecifika GPT-förslag.

## Ändring och uppdatering

Det kanoniska arbetsflödet för inkrementell förvaltning av ett befintligt EA-projekt finns i:

- [`knowledge/workflow-update.md`](knowledge/workflow-update.md)

Arbetsflödet bygger på preflight-integritet, minsta nödvändiga ändring, stabila ID:n, explicit hantering av relationer/proveniens, en projektrevision per sammanhållen ändring, regenerering från YAML och konkret diffrapportering.



## Custom GPT – Builder-instruktion

Den första kompletta Builder-instruktionen finns i:

- [`custom-gpt/instructions.md`](custom-gpt/instructions.md)

Instruktionen styr roll, scope, arbetsdisciplin, evidens, research, klassificering, modellarbete, konflikthantering, kvalitet, projekt-/filhantering och export. Detaljerade definitioner och arbetsflöden ska fortsatt ligga i Builder Knowledge i stället för att dupliceras i instruktionen.

## Nytt i steg 24

- `scripts/validate_project.py` validerar projektformat, manifest, SHA-256, YAML-struktur, ID:n, källor, proveniens och relationer deterministiskt.
- Validatorn använder projektets befintliga maskinläsbara specs i `schemas/` i stället för att skapa en parallell modell av reglerna.
- Lagrade Markdown- och Confluence-artefakter regenereras och jämförs byte-för-byte när de finns. DOCX/PDF kontrolleras strukturellt och täcks fortsatt av dedikerade exporttester.
- `tests/validation/test_validate_project.py` innehåller positiva och negativa regressionstest, bland annat dubblett-ID, saknad referens, otillåten relation, hash-avvikelse och stale Markdown.
- `docs/structural-validation.md` dokumenterar CLI, felkoder och avgränsningen mellan deterministisk strukturkontroll och semantisk EA-kvalitet.

## Nytt i steg 25

- `evals/eval-suite.yaml` definierar den första kompletta semantiska eval-sviten för EA Stödjare.
- 15 evalfall testar klassificering, evidensdisciplin, research, dubbletter/luckor, modellförslag, otillräckligt underlag, källkonflikter och scopegränsen mot lösningsarkitektur.
- 12 fall är blockerande för release eftersom fel där riskerar att ge materiellt missvisande EA-stöd.
- `evals/rubrics/` innehåller gemensam semantisk bedömningsrubrik samt särskilda researchkriterier.
- `schemas/semantic-eval.schema.json` och `tests/evals/test_eval_suite.py` validerar att evaldefinitionerna är kompletta och konsistenta.
- Releasegrinden kräver att alla blockerande fall passerar och att den viktade totalpoängen är minst 85 %.


## Nytt i steg 26

- `tests/scenarios/` innehåller tio realistiska syntetiska EA-scenarier för strategi, förmågor, IT-stöd, plattformar, styrning, konflikter, research och otillräckligt underlag.
- `docs/stress-test-report.md` dokumenterar resultat, kvarvarande risker och designbeslut.
- Förmåga har kompletterats med valfritt `consumer_scope` för att beskriva vilka områden/målgrupper en framför allt IT-förmåga avses betjäna utan att införa Organisation som kärnobjekttyp.
- Funktion förblir underordnat attribut och detaljerad lösningsarkitektur ligger fortsatt utanför v1.

## Nytt i steg 27

- `.github/workflows/ci.yml` kör strukturell validering, tester, reproducerbarhetskontroll av Builder Knowledge och DOCX/PDF-smoketest på push och pull request.
- `.github/workflows/build-artifacts.yml` bygger manuellt referensartefakter i Markdown, Confluence markup, DOCX och PDF.
- `.github/workflows/release.yml` skapar releasepaket på semantiska Git-taggar (`vMAJOR.MINOR.PATCH`) och publicerar dem som GitHub Release.
- `scripts/package_release.py` bygger en deterministisk versionsmärkt zip där versionen normalt kommer från Git-taggen/releasen.
- `tests/release/test_package_release.py` verifierar byte-stabil releasepaketering, exkludering av cachefiler och semantisk versionsvalidering.
- `docs/release-and-ci.md` dokumenterar CI-, build- och releaseflödet.
- `.gitignore` och `requirements-dev.txt` gör lokala och CI-baserade körningar mer reproducerbara.


## Releasekandidat v1.0.0-rc1

- Slutlig helhetsrevision: [`docs/final-review.md`](docs/final-review.md)
- Ändringshistorik: [`CHANGELOG.md`](CHANGELOG.md)
- Samtliga steg 1–28 i utvecklingsplanen är genomförda.
- Inga kända blockerande strukturella projektfel finns.
- Faktisk semantisk runtime-eval mot importerad Custom GPT-instans återstår som sista acceptanskontroll före sluttagg `v1.0.0`.


## GPT-distributioner

Repositoryt kan även bygga två distributionsformat från samma aktuella Builder-konfiguration:

- `ea-stodjare-custom-gpt-vX.Y.Z.zip` för Custom GPT Builder.
- `ea-stodjare-chat-vX.Y.Z.zip` för att bifogas i en vanlig ChatGPT-konversation.

Kör lokalt med `python3 scripts/build_distributions.py` följt av `python3 scripts/validate_distributions.py`. Vanliga builds använder `VERSION`; vid publicerad GitHub Release används release-taggen som versionskälla. De sex genererade Builder Knowledge-filerna och huvudinstruktionen kopieras utan innehållsförändring.
