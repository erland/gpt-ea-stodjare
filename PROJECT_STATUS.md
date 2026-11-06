# Projektstatus – EA Stödjare

## Aktuell status

- **Release:** 2.0.0
- **Revision:** 60
- **Livscykelstatus:** released / frozen
- **Standardmetamodell:** v2.0
- **Relationsmodell:** v2.0
- **Legacy-baslinje:** v1.0.0-rc1, fryst under `compatibility/ea-stodjare-v1/`
- **Senast strukturellt verifierad:** 2026-10-06

`PROJECT_STATUS.md` är projektets mänskligt läsbara återupptagningspunkt. Kanonisk EA-modell finns i `model/`; projektets effektiva metamodell deklareras genom `project-metamodel.yaml` och resolveras mot basprofil och aktiva extensions.

## Releasebaslinje 2.0.0

V2 är färdigutvecklad och fryst. Revision 60 lägger till GPT Byggaren 1.5.1 OpenAI Plugin som runtime/distributionsstöd utan att ändra modell- eller metamodellsemantik. Historiska RC1/RC2-artefakter som inte längre användes har tagits bort, medan permanenta regressionsgrindar har fått funktionsbaserade namn.

V2 omfattar bland annat:

- projektspecifik metamodell enligt base profile + delta,
- native v2 för Förmåga, Plattformstjänst, Plattform och Produkt,
- `Product --can_realize--> IT Support|Platform Service`,
- `Platform Service --provided_by--> Platform`,
- extensions och projektspecifika objekttyper/attribut/relationer,
- conceptual / market-reference / actual-state,
- derived views och presentation contract,
- metamodellstyrd QA och change-control,
- icke-destruktiv v1→v2-migration,
- extended-legacy/rev80-kompatibilitet,
- Markdown/Confluence/DOCX/PDF-generering,
- Builder Instructions, Builder Knowledge, portable-chat- och OpenAI Plugin-distribution,
- 29 semantiska evaldefinitioner med fail-closed runtime-evalprotokoll.

## Permanent verifiering

Följande är aktiva release- och regressionsgrindar:

- `scripts/validate_project.py` – strukturell och profil-/metamodellstyrd validering.
- `scripts/run_workflow_conformance.py` – fem centrala workflow-conformance-fall.
- `scripts/run_full_e2e_regression.py` – tolv sammanhållna E2E-scenarier.
- `scripts/run_v2_ci_gate.py` – central CI/release-grind.
- `scripts/run_generation_smoke.py` – dokumentgeneratorer.
- `scripts/build_builder_knowledge.py` / Builder-tester – distributionskonsistens.
- `scripts/package_release.py` – deterministisk releasepaketering och efterföljande unpack/revalidate via CI-grinden.
- `scripts/validate_runtime_parity.py` – deklarativ runtime/paritetsgrind för Chat ZIP, OpenAI Plugin, Claude Project, Claude Skills och OpenCode.

Permanenta baslinjer finns i:

- `compatibility/reports/v2-e2e-baseline.yaml`
- `compatibility/reports/workflow-conformance-baseline.json`

## Legacy och migration

Legacy-material under `compatibility/` är aktiv regressions- och migrationsdata och ska inte betraktas som historiskt skräp. Det används för att verifiera att:

- v1 kan öppnas och redigeras utan implicit migration,
- v1→v2-migration är icke-destruktiv,
- rev80 kan tolkas som extended legacy och migreras kontrollerat,
- äldre semantik inte normaliseras tyst.

## Runtime-evals

De 29 semantiska evalfallen är definierade och runtimeprotokollet är implementerat. Extern körning mot separat installerad Custom GPT/portable-chat-runtime är inte genomförd och ska fortsatt redovisas som `not_executed_external_runtime_required`. För 2.0.0 är detta en uttryckligen accepterad residualrisk, inte en passerad testgrind.

## Vid nästa förändring

1. Läs `README.md`, denna statusfil och relevant styrande dokument under `docs/`.
2. Identifiera projektprofil och effektiv projektmetamodell före modelländring.
3. Ändra inte fryst v2-semantik utan explicit change-control-beslut.
4. Kör relevant regression samt `scripts/run_v2_ci_gate.py` före release.
5. Höj revision och uppdatera manifest/integritet för varje paketerad ändring.
6. För OpenAI Plugin: bevara project-files som state authority och paketera endast deklarerade runtime-scripts, aldrig CI/releaseverktyg.

## Distributionsmigration till GPT Byggaren 1.6.33 (arbetskopia, 2026-11-06)

- EA Stödjares frysta v2.0-domänmodell och kompatibilitetsprofiler är oförändrade.
- Migrerad projektkonfiguration finns i `gpt-project.yaml`; tidigare 1.5.1-konfiguration bevaras i `migration/gpt-project-1.5.1.yaml`.
- En enda Skill (`ea-stodjare`) används för att inte genomföra en ogranskad uppdelning av det ursprungliga beteendet. Den ursprungliga kanoniska instruktionen finns kvar i `custom-gpt/instructions.md`.
- Canonical Engine 1.6.33 har installerats efter godkänt självtest. Fem runtime-ZIP har byggts och motorns distributionsvalidering passerade.
- Äldre Custom GPT-distribution har avaktiverats enligt aktuellt byggkontrakt; legacy-underlag finns kvar.
- GitHub Actions CI #42164185604 (inklusive `--full-pytest`) och distributionsbygge #42164185577 har passerat på PR #8, commit `11856798f8c9df655eb53660b1cb4ed00a4f5a66`.
- Externa funktionella värdtester för Chat, Plugin, Claude och OpenCode är inte utförda. Byggresultat bevisar inte funktionell runtimeparitet.
- CI- och release-workflows använder den versionslåsta motorn 1.6.33. Slutlig releasegranskning ska skilja passerad CI från externa hosttester och redovisa kvarstående begränsningar.

## Modulära Skills (2026-11-06)

- Tre Skills med gemensam kärna och separat ansvar har aktiverats.
- Samtliga avsnitt i ursprunglig instruktion är bevarade och spårade i `canonical/assembly.json`.
- Fem distributioner har byggts och validerats lokalt. GitHub-kontroll efter denna förändring och externa värdtester återstår.

## Runtime-Skill-beroenden och separat Engine (2.2.1, PR under granskning)

- `quality-and-publication` deklarerar nu `detect_project_profile.py` och `resolve_project_metamodel.py` utöver tidigare skript.
- `project-lifecycle` deklarerar nu `validate_project.py`, som används vid v1-migration.
- `engine.enabled: true` aktiverar en separat EA Stödjare Engine ZIP med endast explicit deklarerade runtimeverktyg och ett exekverbart självtest.
- Obligatorisk CI-grind provar isolerade Python-importer inuti paketerade Skills och Engine ZIP:ens integritet/självtest.
- Full GitHub Actions-verifiering på denna PR återstår. Hostparitet i verklig ChatGPT Plugin/Claude/OpenCode är inte verifierad.

## Konsoliderad projektleverans (2.2.1, PR #10)

- Endast `ea-stodjare-project-<version>.zip` publiceras automatiskt som komplett projektpaket.
- Extra `ea-stodjare-<version>.zip` och `ea-stodjare-<version>.release.json` tas bort från automatisk release.
- Kanoniskt projektarkiv packas upp och körs genom `validate_project.py` i obligatorisk CI/release-gate.
- `scripts/package_release.py` bevaras för historisk kompatibilitet men anropas inte automatiskt. Externa konsumenter av äldre format behöver vid behov migrera.
- Fullständig GitHub CI för ändringen måste verifieras på PR #10.
