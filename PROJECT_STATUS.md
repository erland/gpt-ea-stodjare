# Projektstatus – EA Stödjare

## Aktuell status

- **Projekt:** EA Stödjare – utvecklings- och referensprojekt
- **Version:** 1.0.0-rc1
- **Livscykelstatus:** release candidate / acceptanstest
- **Metamodell:** v1.0
- **Relationsmodell:** v1.0
- **Proveniensmodell:** v1.0
- **Modellformat:** v1.0
- **Senast strukturellt verifierad:** 2026-08-20

`PROJECT_STATUS.md` är projektets mänskligt läsbara återupptagningspunkt. Den är inte source of truth för EA-objekten; den kanoniska modellen finns i `model/`.

## Etablerat

EA Stödjare har aktuell och testad funktionalitet för:

- EA-metamodell och begränsad relationsmodell,
- evidens/proveniens med `explicit`, `derived`, `proposed` och `external`,
- research- och källpolicy,
- extraktion, modellförslag, uppdatering och konflikthantering,
- objekt- och modellkvalitetsregler,
- kanonisk YAML-modell,
- Markdown-, Confluence-, DOCX- och PDF-export,
- projektmanifest, revision och integritetskontroll,
- Custom GPT-instruktion och deterministiskt Builder Knowledge,
- semantiska evals och realistiska regressionsscenarier,
- CI, artefaktbyggnad och reproducerbar releasepaketering,
- Custom GPT- och portable Chat-distributioner.

## Modellstatus

- Den kanoniska modellen i detta repository är referens-/exempeldata för utveckling och validering.
- Ingen organisationsspecifik EA-modell är ännu etablerad i repositoryt.
- Primära och sekundära objekttyper, relationer och proveniens är definierade för v1.

## Kvarvarande acceptans före skarp v1.0.0

1. Importera releasekandidaten i Custom GPT Builder.
2. Kör semantiska evals mot den faktiska GPT-runtimeinstansen.
3. Verifiera beteendet med minst ett realistiskt organisationsspecifikt EA-underlag.
4. Publicera `v1.0.0` när releasegrinden är uppfylld.

## Medvetna framtidsfrågor

Följande är inte blockerande för v1:

- eventuell fördjupning av Lösningsmönster och Referensarkitektur,
- eventuell explicit organisationsmodellering om `owner` + `consumer_scope` blir otillräckligt,
- framtida visualisering/ArchiMate,
- ytterligare exportprofiler efter praktisk användning.

## Återuppta arbete

1. Läs denna `PROJECT_STATUS.md`.
2. Läs `custom-gpt/instructions.md` och relevant kanonisk dokumentation under `docs/`/`knowledge/`.
3. Läs `project-manifest.json` för aktuell projektstruktur och integritet.
4. Kör `python3 scripts/validate_project.py .` före och efter strukturella ändringar.
5. Regenerera Builder Knowledge med `python3 scripts/build_builder_knowledge.py` när kanoniska kunskapskällor ändras.
6. Uppdatera denna statusfil och `revision-log.md` när projektläget faktiskt förändras.
