# Modulära Skills – EA Stödjare 1.6.33

Tre Skills använder en gemensam kanonisk kärna. `modeling-and-research` aktiveras vid boundary-analys, modellering och research; `project-lifecycle` vid projektöppning, ändringar och migration; `quality-and-publication` vid QA, derived views och dokumentexport. Varje Skill har egna beteenderegler och deklarerade resurser, medan `canonical/core.md` behåller gemensamma regler, v2-semantik och evidenslager.

`canonical/assembly.json` spårar alla ursprungliga instruktioners avsnitt till deras exklusiva ägare. Den tidigare `custom-gpt/instructions.md` är oförändrad och bevaras endast för spårbarhet. Samtliga tidigare 14 scripts ingår i de nya resursdeklarationerna; metamodell-/derived-view-skript delas som avsiktliga integrationspunkter.

GPT Byggarens lokala tester: fem ZIP-distributioner byggda, distributionsvalidering PASS, leveranskontroll PASS, modulär ZIP-innehållskontroll PASS. Funktionell paritet i värdmiljöerna är ännu inte testad.
