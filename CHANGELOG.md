# Changelog

## [2.0.0] - 2026-08-25

Slutlig v2-release baserad på RC2/r57. Ingen modell- eller metamodellsemantik ändras i r58 eller post-release cleanup r59. Genererade artefakter och releaseevidens synkas och hela den lokalt körbara releasegrinden används som acceptansbas. Extern LLM-runtime-eval kvarstår uttryckligen som ej exekverad residualrisk. Builder Knowledge-bundlingen korrigeras samtidigt så projektmetamodellformatet ingår i den genererade Knowledge-distributionen som releasekontraktet kräver.

## [2.0.0-rc1] - 2026-08-25

Slutlig releasekandidat efter v2-utvecklingsplanens 32 steg.

### Added

- Maskinläsbar projektmetamodell med basprofil + projektspecifikt delta.
- Native v2, fryst legacy v1 och extended-legacy-profiler.
- Versionssatta project extensions med namespace, dependencies och conflicts.
- Product som generell stödjande objekttyp och `can_realize` mot IT-stöd/Plattformstjänst.
- Explicit conceptual/market/actual-separation.
- Deterministiska derived views och reader-oriented presentation contract.
- Boundary-first workflows, metamodellstyrd QA och change-control.
- Reproducerbar v1→v2-migration och verifierad rev80 extended-legacy-migration.
- Metamodellstyrd Markdown/Confluence/DOCX/PDF-generering.
- V2 Builder Instructions/Knowledge och portable-chat-distribution.
- 29 semantiska evalfall och central v2 CI/release-grind.
- 12-scenario full end-to-end-regression.

### Changed

- Förmåga använder native v2 `in_scope`/`out_of_scope`/`consumer_scope`.
- Plattformstjänst är realiseringsneutral.
- Plattform är konceptuell och produktneutral.
- PLS→Plattform använder `provided_by` för konceptuell hemvist.
- Embedded Funktion stödjer lokala ID:n utan global objekttyp.

### Compatibility

- Legacy v1 kan öppnas, valideras och fortsätta redigeras utan obligatorisk migration.
- Rev80 kan öppnas som extended legacy och migreras reproducerbart i separat kopia.
- Tvetydig äldre semantik bevaras och markeras för review i stället för att normaliseras tyst.

### Acceptance

- Definition of Done: 18/18.
- Full end-to-end regression: 12/12 scenarier.
- RC1 godkändes som historisk releasekandidat; superseded RC1-reviewfil distribueras inte längre efter cleanup r59.

## [1.0.0-rc1] - 2026-08-20

Första kompletta releasekandidaten efter utvecklingsplanens steg 1–28.

### Added

- Enterprise Architecture-metamodell med Drivkraft, Mål, Princip, Förmåga, IT-stöd, Plattformstjänst, Plattform och Standard.
- Sekundärt stöd för Lösningsmönster och Referensarkitektur.
- Förmågetyperna `business` och `it` samt lättviktigt `consumer_scope`.
- Begränsad maskinläsbar relationsmodell.
- Proveniens/evidens med `explicit`, `derived`, `proposed` och `external`.
- Research- och källpolicy med överförbarhetsbedömning.
- Arbetsflöden för extraktion, research, modellförslag, uppdatering och konflikthantering.
- Objekt- och modellkvalitetsregler.
- YAML som kanonisk source of truth.
- Deterministisk Markdown- och Confluence markup-generering.
- DOCX- och PDF-export.
- Projektmanifest, revision och SHA-256-integritet.
- Projektstatus och återupptagningsflöde.
- Custom GPT Builder-instruktion, Builder-konfiguration och deterministiskt Builder Knowledge.
- Semantisk eval-svit med 15 fall och releasegrind.
- 10 realistiska EA-stresstestscenarier.
- Strukturell validator.
- GitHub Actions för CI, artefaktbyggnad och release.
- Deterministisk taggbaserad releasepaketering.
- Slutlig helhetsrevision och releasebeslut för v1.0.0-rc1.

### Scope

Detaljerad lösningsarkitektur, full ArchiMate-modellering och automatisk diagramgenerering ingår inte i v1.

### Acceptance note

Semantiska evals är definierade och strukturellt validerade. Faktisk körning mot importerad Custom GPT-instans återstår som sista acceptanskontroll före sluttagg `v1.0.0`.

## v2 design revision 41

- Added reader-oriented presentation contract with contextual field labels, directional relation labels, object display pattern and non-canonical derived navigation sections.


### Revision 42
- Boundary-first modeling-workflows och QA-koppling för v2 steg 19.


### Revision 43
- V2 steg 20: metamodellstyrd objekt- och modell-QA.
- Lagt till `scripts/resolve_quality_rules.py` och dokumentation för effective-metamodel QA.
- Strukturell validator använder native v2 project metamodel + aktiva extensions för objektfiler, custom objekttyper och relationer.
- Avaktiverade standardtyper skapar inte falska luckor; extension-QA körs endast när extensionen är aktiv.
- Legacy v1 använder fortsatt fryst kompatibilitetsprofil.


## Revision 48 – v2 steg 25

- Added application-oriented IT-support product-analysis reference scenario (`Ordbehandling`).
- Verified Product/`can_realize` beyond the platform domain with primary/partial/supporting roles.
- Added explicit market-reference vs actual-state separation regression coverage.

## [2.0.0-rc2] - 2026-08-25

RC-hardening utan avsiktlig metamodelländring.

- Synkroniserat Builder Knowledge mot aktuella v2-runtimekontrakt.
- Lagt till spärr mot föråldrade utvecklingssteg i Builder Knowledge.
- Lagt till runtime-evalpaket, resultatformat och poängsättare för 29 semantiska evalfall.
- Korrigerat release assurance: definitionsvalidering är inte samma sak som faktisk LLM-runtime-verifiering.
- Lagt till femdelad deterministisk workflow-conformance-grind.

## 2.0.0-rc2 – revision 57, runtime-eval execution workflow

- Operationaliserar de 29 externa runtime-evalerna med separata prompt-, response- och assessment-filer.
- Fingeravtrycker Builder Instructions och Builder Knowledge så releaseevidens binds till exakt testad konfiguration.
- Lägger till fail-closed assembler som kräver samtliga svar och fullständiga kriteriebedömningar före resultatfil.
- Lägger till reproducerbar runbook för faktisk Custom GPT/portable-chat-körning.
- Ingen ändring av EA-modellens eller metamodellens semantik.
