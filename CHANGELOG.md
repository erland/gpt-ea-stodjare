# Changelog

Alla betydande förändringar i EA Stödjare dokumenteras här.

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
