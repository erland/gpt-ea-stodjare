# Release notes – EA Stödjare 2.0.0

EA Stödjare 2.0.0 är den första slutliga v2-releasen. Den bygger på `2.0.0-rc2` revision 57 och ändrar inte modell- eller metamodellsemantik.

## Viktigaste innehållet

- Projektspecifik metamodell baserad på base profile + delta.
- Native v2-semantik för Förmåga, Plattformstjänst, Plattform och Produkt.
- `Product --can_realize--> IT Support|Platform Service` och `Platform Service --provided_by--> Platform`.
- Extensions, informationslagren conceptual/market-reference/actual-state och derived views.
- Metamodellstyrd QA, presentation contract och change-control.
- Icke-destruktiv v1→v2-migration samt verifierad extended-legacy/rev80-hantering.
- Metamodellstyrd Markdown-, Confluence-, DOCX- och PDF-generering.
- Builder Instructions, Builder Knowledge och portable-chat-distribution för v2.
- 29 semantiska evaldefinitioner samt ett reproducerbart, fail-closed runtime-evalprotokoll.
- Deterministiska workflow-E2E- och releasegrindar.

## Releaseevidens

Revision 59 ska verifieras med repositoryts automatiserade validator, regressions-/kompatibilitetstester, generatorer, Builder/distributionstester och releasepaketets unpack/revalidate.

Extern LLM-runtime-eval är inte exekverad och redovisas fortsatt som sådan. Detta är en medvetet accepterad residualrisk i 2.0.0, inte en passerad testgrind.

## Revision 59 – post-release cleanup

- Tar bort superseded RC1/RC2-reviewer, RC-notes och engångsrapporter som inte längre används av releasekedjan.
- Tar bort duplicerade `working`-DOCX/PDF från minimal-exemplet.
- Byter utvecklingsstegs-/RC-namn på permanenta E2E- och workflow-conformance-grindar till funktionsbaserade namn.
- Behåller v1/rev80 och migrationsdata eftersom de är aktiv regressionsevidens.
- Ingen ändring av modell- eller metamodellsemantik.
