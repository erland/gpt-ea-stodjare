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
- `scripts/validate_runtime_parity.py` – GPT Byggaren 1.5.1 runtime/parity-grind för Chat, Custom GPT och OpenAI Plugin.

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
