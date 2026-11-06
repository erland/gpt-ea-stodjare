# EA Stödjare – CI-/release-migrering till GPT Byggaren 1.6.33

## Genomfört

- Alla fyra GitHub Actions-workflows använder en lokal composite action för att ladda ned den versionslåsta motorn (`v1.6.33`), verifiera SHA-256, köra motorns oförändrade självtest och installera dess kanoniska byggare/validatorer.
- Release kör den obligatoriska EA v2-grinden före paketering och publicering. Taggen styr projektversionen, oberoende av den låsta motorversionen.
- Distributionsflödet publicerar inte längre ytterligare en release från händelsen `release.published`. Release-workflow är ensam publicerare vid tagg.
- `scripts/run_v2_ci_gate.py` använder distributionsvalidatorns stödda `--project-root`-argument.
- Runtime-paritet deklarerar nu de fem stödda målen; historisk Custom GPT är inte en aktiv distribution. Värdspecifik funktionell paritet återstår att testa.
- Uppdaterat EA-filmanifest med ändrade filers faktiska SHA-256.

## Verifierat i lokal miljö

- Originalmotorns självtest: PASS vid föregående migrationssteg.
- Projektvalidering: 0 fel, 0 varningar efter ändringarna.
- Runtime-paritetskontrakt: PASS (deklarativ kontroll, inte funktionellt värdtest).
- Distributionsbygge: 6 arkiv inklusive projektpaket; distributionsvalidering: PASS.
- Riktad pytest för release/CI och v1→v2-migrering: 10 passed.
- Generatorsmoke: Markdown, Confluence, DOCX och PDF: PASS.
- Omfattande EA CI-gate kördes, men exekveringen nådde miljöns tidsgräns efter sju godkända delsteg. Den ska därför **inte** betraktas som genomförd eller godkänd.

## Kända kvarstående kontroller

1. Kör GitHub Actions för en PR och kontrollera att den publicerade engine-ZIP-filen motsvarar SHA-256 `9638ce2b9300423ace6c055ef824284154788d9d8e6e54459f875fe56ff69885`. Självtest och installering körs före grinden.
2. Låt komplett `run_v2_ci_gate.py --full-pytest` slutföras i CI, inklusive full E2E, releasesmoke och regressionstester.
3. Provkör respektive distribution i Chat, Plugin, Claude Project, Claude Skills och OpenCode och verifiera projektfiler, verktygsbehörigheter samt att EA-modellens beteende behålls.
4. Skapa release-tagg först när alla blockerande kontroller är gröna. Ingen GitHub-release skapades i detta arbete.

## Återstående risk

Detta steg bedömer inte funktionell språkmodell-paritet och har inte kört Github-hostade workflows. Projektets egen omfattande regressionsgrind är fortfarande inte slutverifierad.
