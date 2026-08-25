# Revision log – EA Stödjare

Denna fil är den människoläsbara revisionshistoriken för projektets aktuella manifeststyrda struktur. Detaljerad utvecklingshistorik finns i Git och dupliceras inte här.

## Revision 23 – 2026-08-20

- Releasekandidat `v1.0.0-rc1` etablerad.
- EA-metamodell, relationer, proveniens, YAML-format och kvalitetsregler verifierade.
- Deterministisk Markdown-, Confluence-, DOCX- och PDF-kedja verifierad.
- Custom GPT Builder-instruktion och sex deterministiskt genererade Knowledge-filer etablerade.
- Semantisk eval-svit och realistiska regressionstest etablerade.
- CI/releasepaketering och dual distribution för Custom GPT/portable Chat etablerad.
- Historiska utvecklingsrapporter har därefter rensats ur working tree; Git är historikkälla.

### Nästa revisionshändelse

Skapa en ny revision när releasekandidaten ändras materiellt, runtime-acceptansen leder till en korrigering eller skarp `v1.0.0` publiceras.

## Revision 24 – 2026-08-25

- V2-utvecklingsspåret initierat; steg 1 av 32 genomfört.
- `docs/v2-design-principles.md` etablerar v2:s designbaslinje utan att ändra den kanoniska v1-metamodellen.
- `docs/backward-compatibility-contract.md` etablerar releasekrav för native v2, legacy v1 och extended legacy-projekt.
- `docs/v2-development-plan.md` har lagts in i projektpaketet så utvecklingen kan fortsätta från zip-filen utan separat planartefakt.
- `it-formagemodell-del3-rev80` är fastställt som obligatoriskt extended-legacy kompatibilitets- och migrationstest.
- Actual Platform Offering ska inte vara obligatoriskt kärnobjekt; Produkt planeras som generell stödjande objekttyp i senare v2-steg.
- Befintlig v1-metamodell, relationsmodell, Builder Instructions och Builder Knowledge är avsiktligt oförändrade i detta steg.

### Nästa revisionshändelse

Genomför v2 steg 2: skapa explicit maskinläsbar legacy-profil för EA Stödjare v1.

## Revision 25 – 2026-08-25

- V2 steg 2 av 32 genomfört.
- `compatibility/ea-stodjare-v1/profile.yaml` etablerat som maskinläsbar legacy-profil för EA Stödjare v1.
- V1:s objekttyper, relationer, proveniens, YAML-format och projektmanifest har frysts som självständiga snapshots under `compatibility/ea-stodjare-v1/schemas/`.
- Profilen dokumenterar v1:s ID-prefix, statusvärden, filstruktur, detektionsmarkörer och kända semantiska skyddsregler för `scope`, Plattformstjänst, Plattform, `realized_by`, Produkt och embedded Funktion.
- Legacy mode ska kunna fortsätta redigera v1 enligt snapshotens semantik utan att v2-only-fält skrivs in automatiskt.
- Regressionstest verifierar att kompatibilitetsprofilens snapshots och kärnsemantik är internt konsistenta.
- Den kanoniska v1-metamodellen i repositoryts huvudschemas är fortsatt oförändrad i detta steg.

### Nästa revisionshändelse

Genomför v2 steg 3: inventera `it-formagemodell-del3-rev80` som extended legacy project och rekonstruera dess faktiskt använda metamodell maskinläsbart.

## Revision 26 – 2026-08-25

- V2 steg 3 av 32 genomfört.
- `it-formagemodell-del3-rev80` har inventerats som ett extended legacy project utan ändring av referensprojektets kanoniska data.
- `compatibility/reference-projects/rev80/metamodel.yaml` rekonstruerar den faktiskt använda modellsemantiken maskinläsbart.
- Rekonstruktionen dokumenterar 13 IT-förmågor, 10 IT-stöd, 92 Plattformstjänster, 35 konceptuella Plattformar, 385 kanoniska relationer, 14 källor och 295 marknadsprodukter i referenssnapshoten.
- `extension-inventory.yaml` inventerar samtliga 92 supporting-YAML-filer med metadata och kategori.
- Capability boundary, realiseringsneutral Plattformstjänst, konceptuell Plattform, marknadsproduktreferens, produkt→PLS, deployment/openness, relation roles, plattformsmognad, derived views, presentation contract och model freeze/change control är dokumenterade som projektextensions.
- Actual-platform-lagrets 10 tidigare kandidater är markerade som pensionerat experiment; 0 aktiva actual-platform-objekt ingår i rekonstruerad aktiv metamodell.
- Centrala rev80-källfiler har fingerprintats för framtida kompatibilitets-/migrationstest.
- Regressionstest verifierar rekonstruktionens kärnfakta och att actual-platform-lagret inte är aktivt.
- Den kanoniska v1-metamodellen i repositoryts huvudschemas är fortsatt oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 4: definiera det maskinläsbara projektmetamodellformat som ska kunna uttrycka både standardprojekt och rev80-liknande extensions.

## Revision 27 – 2026-08-25

- V2 steg 4 av 32 genomfört.
- `schemas/project-metamodel.schema.json` etablerat som maskinläsbart kontrakt för native v2-projekts faktiska metamodell.
- `docs/project-metamodel-format.md` definierar basprofil + delta, enabled/disabled object types, custom object types, attribute extensions, custom relations, relation qualifiers, value sets, extension references, derived views, presentation semantics och enkel governance.
- `examples/project-metamodel/minimal.yaml` visar att ett projekt kan använda en mindre modell än standardprofilen.
- `examples/project-metamodel/extended.yaml` visar projektspecifika objekt/attribut/relationer samt extensions och derived views inspirerade av rev80 utan att vara en migration av referensprojektet.
- Derived views kräver uttryckligen `source_of_truth: false`.
- Fristående regressionstest validerar båda exemplen mot JSON Schema och kontrollerar grundläggande konsistens.
- V1-kärnmetamodell, relationer, Builder Instructions/Knowledge och strukturvalidatorns v1-semantik är fortsatt oförändrade.

### Nästa revisionshändelse

Genomför v2 steg 5: inför metamodell-detektion vid projektöppning för native v2, legacy v1, extended legacy och okänd modell.


## Revision 28 – 2026-08-25

- V2 steg 5 genomfört: metamodell-detektion vid projektöppning.
- Lagt till strikt detektionsordning för native v2, explicit legacy, legacy v1, extended legacy och unknown.
- Lagt till `project-compatibility.yaml`-kontrakt, maskinläsbara detektionsregler och CLI-stöd.
- Okänd/ogiltig explicit modell får inte falla tillbaka till standardsemantik.
- Regressionstester täcker native v2, invalid explicit model, explicit legacy, v1, generic extended legacy, rev80 och unknown.


## Revision 29 – 2026-08-25

- V2 steg 6 av 32 genomfört.
- Native v2 Förmåga använder `in_scope`, `out_of_scope` och `consumer_scope`; legacy `scope` är borttaget från huvudschemats native v2-attribut men ligger kvar i fryst v1-snapshot.
- För IT-förmågor definieras positiv boundary som tekniskt möjliggörande och presenteras normalt som **Stödjer**; negativ boundary som **Omfattar inte**.
- `schemas/model-format.yaml` har fått ett explicit v2-kontrakt för capability-instance utan att serialiseringsformatet i övrigt bryts.
- Objekt-QA har kompletterats med boundary-kontroller och skydd mot produkt-/PLS-listor i IT-förmåga `in_scope`.
- Konservativ maskinläsbar migreringsregel har lagts till; tvetydigt v1 `scope` får inte automatiskt splittras/renamas.
- Legacy v1-profilens schemasnapshots är oförändrade.

### Nästa revisionshändelse

Genomför v2 steg 7: revidera Plattformstjänst till realiseringsneutral standardsemantik med legacy-kompatibilitet.


## Revision 30 – 2026-08-25

- V2 steg 7 av 32 genomfört.
- Native v2 Plattformstjänst definieras som realiseringsneutralt tekniskt erbjudande/funktionalitetskontrakt; gemensam/central runtime är inte ett krav.
- `realization_pattern` har lagts till som valfritt attribut med kontrollerad värdemängd för single product, product family, composition, framework/library, managed service, SaaS, mixed och unknown.
- Klassificeringsguide, objekt-QA och modellformat har uppdaterats med den nya semantiken.
- Konservativ migreringsregel och migreringsdokumentation har lagts till; legacy v1-PLS behåller identitet och äldre semantik tills kontrollerad migration sker.
- Fryst v1-snapshot är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 8: revidera Plattform till konceptuell och produktneutral standardsemantik med legacy-kompatibilitet.


## Revision 31 – 2026-08-25

- V2 steg 8 av 32 genomfört.
- Native v2 Plattform definieras som en produktneutral konceptuell gruppering av Plattformstjänster med sammanhållen teknisk/förvaltningsmässig logik.
- Plattform är inte automatiskt produkt, konkret runtime eller faktiskt organisatoriskt plattformserbjudande.
- Singleton-plattform och kompositionsrealisering är uttryckligen legitima när boundaryn motiverar det.
- Klassificeringsguide, modellformat och objekt-QA har uppdaterats med konceptuell Plattform-semantik.
- Konservativ v1→v2-migreringsregel och migrationsdokumentation har lagts till. Legacy `realized_by` lämnas oförändrad till steg 11.
- Fryst v1-snapshot är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 9: inför Produkt som generell stödjande objekttyp.


## Revision 32 – v2 steg 9

- Infört Produkt som generell stödjande v2-objekttyp (`PRD-*`).
- Infört `product_kind` och maskinläsbar produktmodell.
- Lagt till `model/products.yaml`, QA-, klassificerings- och migreringsregler.
- V1 legacy-snapshot är oförändrad; produktdata i legacy migreras inte automatiskt.

## Revision 33

- V2 steg 10: generaliserad `Product --can_realize--> IT Support|Platform Service`.
- Obligatorisk `realization_role`: primary/partial/supporting, projektextensibel.
- Källstödd evidens krävs; proposed-only räcker inte.
- Legacy v1-snapshot oförändrad.

## Revision 34

- V2 steg 11: infört `Platform Service --provided_by--> Platform` för konceptuell hemvist.
- PLS→Platform har tagits bort från native v2 `realized_by`; `realized_by` reserveras för konkret realiseringssemantik.
- Lagt till konservativ legacy-migreringsregel och migrationsdokumentation; ingen global automatisk konvertering tillåts.
- Rev80 dokumenteras som känt conceptual-home-fall men referensprojektets data ändras inte.
- Fryst v1 relationssnapshot är oförändrad.


## Revision 35

- V2 steg 12: infört generella relationskvalificerare och relationsspecifik tillämpbarhet.
- Lagt till global kvalificerarkatalog för `relation_role`, `strength`, `mandatory`, `realization_role`, `verification_status`, `boundary_basis` och `notes`.
- Validatorn kontrollerar nu att kvalificeraren är tillåten för relationstypen samt rätt datatyp/värdemängd.
- `realization_role` är fortsatt obligatorisk för `can_realize`; övriga kvalificerare är valfria enligt relationsschemat.
- Legacy v1-snapshot är oförändrad och behöver inga v2-kvalificerare.

### Nästa revisionshändelse

Genomför v2 steg 13: förstärk embedded Funktion med valfria lokala ID:n och metadata.

## Revision 36

- V2 steg 13: förstärkt embedded Funktion utan global objekttyp.
- Native v2 Funktion kan ha valfritt lokalt `id`, `description` och `required`.
- Lokala funktions-ID:n är scoped till moderobjektet och valideras för format och unikhet inom moderobjektet.
- Legacy v1 Funktion förblir oförändrad och förbjuder fortsatt ID; migration skapar inga ID:n eller `required`-värden automatiskt.
- Lagt till QA-, migrerings- och kompatibilitetstest för den starkare funktionsstrukturen.

### Nästa revisionshändelse

Genomför v2 steg 14: inför extension-mekanism.


## Revision 37

- V2 steg 14: infört kontrollerad extension-mekanism för projektspecifika metamodelltillägg.
- Lagt till versionssatta extensionpaket med obligatoriskt namespace, registry, beroenden och konflikter.
- Extensioner kan bidra med object types, attributes, relations, value sets/value-set extensions, QA rules och presentation semantics.
- Lagt till deterministisk resolver som producerar en härledd, icke-kanonisk resolverad projektmetamodell.
- Lagt till konfliktregler och regressionstester för kärnkollisioner, enumkollisioner, saknade beroenden och okända extensions.
- Fryst v1-profil är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 15: paketera deployment-, openness- och platform-maturity-modellerna som generella optional extensions.

## Revision 38

- V2 steg 15: paketerat tre generella optional extensions från rev80.
- `ea.product-deployment` utökar Product med separata dimensioner för control plane, data plane och deployment posture.
- `ea.product-openness` utökar Product med källstödd openness-klassificering.
- `ea.platform-maturity` utökar konceptuell Platform med strukturell maturity class.
- Alla tre extensioner är oberoende, valfria och registrerade i extension-registret.
- Epistemiska skyddsregler förhindrar att marknads-/produktinformation tolkas som faktisk organisationsstatus.
- Rev80:s actual-platform-experiment förblir pensionerat och ingår inte.

### Nästa revisionshändelse

Genomför v2 steg 16: inför conceptual / market / actual informationslager.


## Revision 39

- V2 steg 16: infört explicit epistemisk separation mellan conceptual, market reference och actual state.
- Lagt till `schemas/information-layers.yaml`, `market-reference/` och `actual-state/` med separata assertion-format.
- `actual-state` kan referera Product direkt; inget obligatoriskt `actual_platform_offering`-objekt införs.
- Validatorn stoppar verifierad actual state som endast stöds av extern marknadsevidens.
- Manifestet deklarerar nu informationslagrens sökvägar.
- Fryst v1-profil är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 17: inför derived views som förstaklasskoncept.


## Revision 40

- V2 steg 17: infört derived views som förstaklasskoncept.
- Lagt till separat JSON Schema och standardkatalog med sju reproducerbara navigations-/analysvyer.
- Lagt till deterministisk generator som materialiserar vyer med input-fingeravtryck och `source_of_truth: false`.
- Validatorn kontrollerar schema, unika view-ID:n samt referenser till kända objekt- och relationstyper.
- Lagt till QA-regler som förbjuder write-back från derived views till kanoniska informationslager.
- Fryst v1-profil är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 18: inför reader-oriented presentation contract.

## Revision 41

- V2 steg 18: infört separat reader-oriented presentation contract.
- Lagt till JSON Schema och svensk standardkonfiguration med `source_of_truth: false`.
- Standardiserat objektvisning som `Namn (ID)`, kontextberoende fältetiketter och riktade relationsetiketter.
- Lagt till derived-view-baserade navigationssektioner som uttryckligen är icke-kanoniska och read-only.
- Validatorn kontrollerar presentationskontraktets schema, relationsreferenser och derived-view-referenser.
- Lagt till återanvändbar helper/CLI för att slå upp läsaretiketter och visningsmönster.
- Fryst v1-profil är oförändrad.

### Nästa revisionshändelse

Genomför v2 steg 19: förstärk boundary-first modeling.


## Revision 42 – v2 steg 19

- Infört sex boundary-first modeling-workflows: boundary, decomposition, merge, singleton sanity, product stress test och composition sanity.
- Kopplat workflows till nya modell-QA-regler `QM-BND-001`–`QM-BND-008`.
- Lagt till dokumentation, Knowledge-workflow och regressionstester.
- Legacy v1-profilen är fortsatt oförändrad.


## Revision 43 – v2 steg 20

- Infört metamodellstyrd QA-resolver för objekt-, modell- och extension-regler.
- Coverage-profiler skärs mot projektets aktiva objekttyper.
- Validatorn overlayar native v2 project metamodel och aktiva extensions innan strukturell objekt-/relationsvalidering.
- Avaktiverade standardobjekttyper behöver inte ha kanoniska modellfiler.
- Legacy v1 fortsätter valideras mot fryst v1-profil.
- Lagt till regressionstester för default v2, minimal profil, extension on/off, legacy v1 och disabled-file-beteende.


## Revision 44 – v2 steg 21

- Infört maskinläsbar change-control med baseline ID/version och freeze-status.
- Infört ändringsklasserna `editorial`, `evidence_update`, `controlled_model_change`, `breaking_model_change` och `metamodel_change`.
- Infört `governance/retired-ids.yaml` med policyn `retire_never_reuse`.
- Infört separata `model-changelog.yaml` och `metamodel-changelog.yaml`.
- Validatorn kontrollerar baseline mot manifest, freeze-policy, loggseparation och att pensionerade ID:n inte återanvänds.
- Legacy v1 kräver inte v2-governancefiler före migration.

### Nästa revisionshändelse

Genomför v2 steg 22: skapa migrationsmotor v1 → v2.


## Revision 45 – v2 steg 22

- Infört reproducerbar tvåfasig v1→v2-migrationsmotor (`plan`/`apply`).
- Originalprojekt skrivs aldrig över och befintlig målkatalog avvisas.
- Migration skapar explicit v2-projektmetamodell och schema-validerad migreringsrapport.
- Stabila objekt- och relations-ID:n bevaras när semantisk identitet är oförändrad.
- Tvetydigt legacy `capability.scope` bevaras via deklarerad attributextension i stället för mekanisk split.
- PLS→PLT `realized_by` bevaras med oförändrat relations-ID som `legacy_realized_by` tills konceptuell hemvist kan verifieras.
- Projektspecifika legacy-objekttyper i den kanoniska modellen deklareras inline i projektmetamodellen.
- Genererade derivat tas bort ur migrationskopian och ska regenereras; kanoniskt innehåll raderas inte.

### Nästa revisionshändelse

Genomför v2 steg 23: migrera och verifiera minimal v1-modell end-to-end.

## Revision 46 – v2 steg 23

- Migrerat den minimala v1-referensmodellen end-to-end som reproducerbart regressionstest.
- Lagt till maskinläsbar baslinje och verifieringsresultat för 11 objekt, 12 relationer och 3 källor.
- Lagt till generell `scripts/verify_v1_v2_migration.py` för stable-ID-, proveniens-, relations- och dokumentekvivalens.
- Verifierat exakt bevarande av objekt, källregister och proveniens samt deklarerad semantisk normalisering av `legacy_realized_by`.
- Justerat Markdown- och Confluence-generatorerna så temporär `legacy_realized_by` behåller läsaretiketten Realiseras av/Realiserar.
- Verifierat semantiskt ekvivalent Markdown/Confluence och regenerering av DOCX/PDF för både v1-källa och migrerat v2-mål.

### Nästa revisionshändelse

Genomför v2 steg 24: full migration/kompatibilitetsverifiering mot rev80-referensprojektet.


## Revision 47 – v2 steg 24

- Infört explicit migrationsadapter för rev80 och äldre flat extended-legacy-manifest.
- Detektorn känner nu igen rev80-signaturen även när standardiserat v1-manifest saknas.
- Migreringen bevarar originalet, skapar separat v2-kopia och använder `compatibility_mode: extended_legacy`.
- Konverterar 92 PLS→PLT `realized_by` till `provided_by` utifrån rev80:s frysta semantiska rekonstruktion.
- Sammanför 55 relation roles till kanoniska relationsinstanser.
- Bevarar samtliga 92 supporting-YAML byte-identiskt och verifierar 295 produkter, deployment/openness, maturity, derived views och freeze/change-control utan att upphöja marknadsdata till actual state.
- Registrerar PLT-101–PLT-110 som pensionerade ID:n med `retire_never_reuse`.
- Lagt till rev80-specifik extended-legacy-validering, migrationsbaslinje, verifieringsresultat, dokumentation och regressionstester.

### Nästa revisionshändelse

Genomför v2 steg 25: lägg till produktanalys-scenario för IT-stöd (exempel Ordbehandling).


## Revision 48 – v2 steg 25

- Lagt till komplett native-v2-scenario för produktanalys av det produktneutrala IT-stödet `ITS-251 Ordbehandling`.
- Stresstestat embedded functions samt flera produkter mot samma IT-stöd.
- Verifierat `can_realize` med `primary`, `partial` och `supporting`.
- Hållit externa marknadspåståenden separata från organisationsspecifik actual state.
- Lagt till regressionstest som förhindrar att `can_realize` eller marknadskapacitet tolkas som faktisk användning.

### Nästa revisionshändelse

Genomför v2 steg 26: revidera Markdown/Confluence/DOCX/PDF-generering så output styrs av projektmetamodell och presentation contract.


## Revision 49 – v2 steg 26

- Infört gemensamt `scripts/generator_context.py` för metamodell- och presentationsstyrd dokumentgenerering.
- Markdown och Confluence genererar endast aktiva objekttyper och relationer enligt effektiv projektmetamodell; legacy-projekt använder bakåtkompatibel filupptäckt.
- Infört generiskt stöd för Product och custom object types, inklusive extension-/projektattribut och läsaretiketter.
- Presentation contract styr objektvisning, boundary-/fältetiketter och relationsetiketter.
- Derived-view-baserade navigationssektioner används som icke-kanoniska läsvyer.
- Varje generator skapar `generation-manifest.json`; DOCX/PDF använder manifestet i stället för hårdkodad kataloglista.
- Rättat derived-view-generatorn till kanoniska `source`/`target` och repository-fallback för view-katalogen.
- Lagt till regressionstest för enabled/disabled types, custom object type, Product och presentation overrides.
- Visuellt verifierat DOCX/PDF med applikationsnära Produkt-scenario.

### Nästa revisionshändelse

Genomför v2 steg 27: uppdatera Builder Instructions och Builder Knowledge för v2-semantiken.


## Revision 50 – v2 steg 27

- Reviderat `custom-gpt/instructions.md` till kompakt v2-semantik med project-metamodel-first, legacy/extended-legacy, extensions, informationslager, Product, boundary-first, derived views, migration och change-control.
- Hållit Builder Instructions inom 8 000 tecken och flyttat detaljregler till Builder Knowledge.
- Utökat `scripts/build_builder_knowledge.py` så samma sex Knowledge-filer konsoliderar hela v2:s styrande dokument och workflows.
- Uppdaterat Builder-konfiguration och portable chat-startpunkt till v2.
- Förstärkt Builder-regressionstest med v2-innehållskrav och explicit storleksgrind.

### Nästa revisionshändelse

Genomför v2 steg 28: revidera semantiska evals för nya v2-risker och bakåtkompatibilitet.


## Revision 51 – v2 steg 28

- Reviderat semantisk eval-suite till version 2.
- Bevarat samtliga 15 v1-evalfall som regression.
- Lagt till 14 blockerande v2-fall (EVAL-016–EVAL-029) enligt utvecklingsplanens risklista.
- Förstärkt evaltestet med obligatoriska v2-tags och explicit coverage-grind.
- Utökat bedömningsrubriken med projektprofil/metamodell, epistemiska lager, realiseringssemantik, derived views och governance.
- Gjort derived-view-generatorns läsning bakåtkompatibel med både `source`/`target` och äldre `source_id`/`target_id`; kanonisk v2-output ändras inte.

### Nästa revisionshändelse

Genomför v2 steg 29: förstärk strukturell validator för slutlig v2-konsistens.


## Revision 52 – v2 steg 29

- Gjort `scripts/validate_project.py` profilmedveten före semantisk validering.
- Native v2 valideras mot effektiv projektmetamodell, base profile och aktiva extensions; legacy v1 använder fortsatt frysta snapshots.
- Infört separat valideringsgren för omigrerad rev80 med äldre flat-manifest och fryst rekonstruktionsprofil.
- Derived views och presentation contract valideras mot projektets effektiva objekt-/relationskatalog.
- Materialiserade `build/derived-views/` reproduceras och jämförs deterministiskt när katalogen finns.
- Samordnat change-control och retired-ID-kontroller i den gemensamma grinden.
- Lagt till schemavaliderad maskinläsbar valideringsrapport via `--report-file`.
- Lagt till dokumentation och fokuserade regressionstester för steg 29.

### Nästa revisionshändelse

Genomför v2 steg 30: GitHub Actions och releasepaketering för v2.


## Revision 53 – v2 steg 30

- Infört `scripts/run_v2_ci_gate.py` som central obligatorisk v2-grind för CI och release.
- Grinden verifierar standardprojekt, v1 legacy fixture, rev80 extended legacy, migration, semantiska evals, Builder Knowledge, generatorer, GPT-distributioner samt release unpack-and-validate.
- CI och taggrelease kör hela pytest-sviten utöver de explicit namngivna v2-grindarna.
- GitHub Actions-workflows använder den centrala grinden och laddar upp maskinläsbara JSON-rapporter.
- `package_release.py` gör strukturell v2-preflight även vid manuell paketering och redovisar projektets revision i release-metadata.
- Lagt till `docs/ci-release-v2.md` och regressionstest för workflow-/releasekontraktet.

### Nästa revisionshändelse

Genomför v2 steg 31: full end-to-end regression för native v2, legacy v1 och extended legacy.

## Revision 54 – v2 steg 31

- Infört `scripts/run_step31_e2e_regression.py` som explicit end-to-end-regression för planens tolv arbetskedjor.
- Lagt till reproducerbart scenario för Produkt→Plattformstjänst med realiseringsneutral PLS och separata market/actual-lager.
- Lagt till regression som bevisar att legacy v1 kan fortsätta redigeras utan migration.
- Förstärkt research-scenariot med v2:s epistemiska skyddsregler.
- Integrerat steg-31-grinden i `scripts/run_v2_ci_gate.py`.
- Dokumenterat RC-regressionen i `docs/full-end-to-end-regression.md`.

### Nästa revisionshändelse

Genomför v2 steg 32: slutlig helhetsrevision och releasekandidatbedömning.

## Revision 55 – v2 steg 32 / 2.0.0-rc1

- Genomfört slutlig helhetsrevision över designprinciper, backward compatibility, standard-/projektmetamodell, extensions, Product/Funktion, relationer, derived views, QA, change-control, migration, rev80, Builder, evals, CI och exports.
- Definition of Done verifierad **18/18**.
- Steg-31 end-to-end-baslinje verifierad **12/12 scenarier**.
- Lagt till slutrapport, migrationsguide och release notes för `2.0.0-rc1`.
- Fryst RC-baslinjen som `EA-STODJARE-V2-RC1@2.0.0-rc1-r55`.
- Uppdaterat produktversionen till `2.0.0-rc1`; v1.0.0-rc1 ligger kvar som fryst legacy-profil.
- Lagt till maskinläsbar release candidate-rapport och CI-test för RC-kontraktet.

### Nästa revisionshändelse

Efter verklig RC-användning: klassificera eventuella korrigeringar enligt change-control och besluta därefter om slutlig `2.0.0`.

## Revision 56 – RC hardening / 2.0.0-rc2

- Synkroniserat Builder Knowledge mot aktuella v2-runtimekontrakt och avlägsnat kända föråldrade framtidssteg från distributionen.
- Lagt till regressionstest som blockerar återintroduktion av stale Builder Knowledge.
- Infört runtime-evalprotokoll: paketexport, resultat-schema, poängsättare och explicit status för extern runtime-körning.
- Lagt till fem deterministiska workflow-E2E-kedjor och maskinläsbar conformance-rapport.
- Reviderat release assurance så evaldefinitioner inte beskrivs som faktisk runtime-pass.
- Klassificerat kvarvarande gate före final 2.0.0: faktisk runtime-eval + verifierad GitHub CI/release-körning.


## Revision 57 – runtime-eval execution workflow

- Behållit produktversion `2.0.0-rc2` och modell-/metamodellsemantiken oförändrad; RC2-baslinjens tekniska revision höjs till r57 för spårbarhet av evalverktygen.
- Infört `scripts/prepare_runtime_eval_run.py` som skapar 29 isolerade prompt-/response-/assessment-fall för faktisk Custom GPT/portable-chat-körning.
- Infört SHA-256-fingeravtryck av Builder Instructions och genererad Builder Knowledge så runtime-evidensen kan knytas till exakt testad konfiguration.
- Infört `scripts/assemble_runtime_eval_results.py` som vägrar skapa ett runtime-resultat om svar saknas eller kriterier inte är fullständigt bedömda.
- Lagt till `evals/runtime/RUNBOOK.md` med reproducerbart operatörsflöde och regler mot cross-case contamination.
- Lagt till regressionstest för run-förberedelse, fingerprint och fail-closed assembler.

### Nästa revisionshändelse

Kör de 29 fallen mot den faktiska EA Stödjare-distributionen, importera/bedöm resultaten och avgör runtime-releasegrinden.


## Revision 58 – final 2.0.0

- Fryst EA Stödjare v2 som slutlig `2.0.0` utan ändrad modell- eller metamodellsemantik.
- Regenererat versionskänsliga/genererade artefakter från kanonisk source of truth före slutlig releasegrind.
- Rättat Builder Knowledge-bundlingen så `docs/project-metamodel-format.md` faktiskt ingår i projekt-/outputpaketet enligt den befintliga releasegrinden.
- Dokumenterat att extern 29-falls LLM-runtime-eval fortsatt är 0/29 exekverad och uttryckligen accepteras som residualrisk i releasebeslutet.
- Slutlig release kräver lokal validator, regressioner, migrations-/kompatibilitetsgrindar, generatorer, Builder/distributioner samt unpack/revalidate av releasepaketet.


## Revision 59 – post-release cleanup

- Rensat superseded RC1/RC2-reviewer, RC-release notes och engångsrapporter ur final distribution.
- Tagit bort duplicerade `working`-DOCX/PDF från minimal-exemplets dokumentexport.
- Bytt `step31`-namn på permanent full E2E-regression till `run_full_e2e_regression.py` och `v2-e2e-baseline.yaml`.
- Bytt RC-hardening-namn på permanent workflow-conformance till `run_workflow_conformance.py` och `workflow-conformance-baseline.json`.
- Ersatt historiskt Step32 release-candidate-test med permanent final release contract.
- Behållit v1-/rev80-/migrationsunderlag som aktiv regressionsevidens.
- Ingen modell- eller metamodellsemantik ändrad.
