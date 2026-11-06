# GPT Byggaren 1.6.33 – migrationsrapport

## Mål och bevarande

Källprojekt: EA Stödjare 2.0.0 (revision 60), ursprungligen byggt för GPT Byggaren 1.5.1. Domänmetamodell, native v2, legacy-migrationer, YAML-modell, evidenslager och dokumentgeneratorer behålls.

## Genomförda sex steg

1. **Inventering – klar:** äldre projektkontrakt, instruktion, 6 Knowledge-filer, scripts, tester och CI dokumenterade.
2. **Projektmodell – klar med granskningsnotering:** fem peer-runtimes med separat OpenAI Plugin, avaktiverad Custom GPT, en enda Skill för att bevara ursprungligt beteende. 1.5.1-kontrakt arkiverat.
3. **Motor – klar:** bifogad kanonisk Engine 1.6.33 självtestad, integritetsverifierad och installerad.
4. **Fem distributioner – byggda:** Chat ZIP, Plugin, Claude Project, Claude Skills och OpenCode. Kanonisk distributionsvalidator: PASS.
5. **Dokumentation/hygien – delvis klar:** README och PROJECT_STATUS uppdaterade och gamla källfiler bevarade. CI- och release-workflows är migrerade till versionslåst engine 1.6.33. Inga osäkra automatiska borttagningar.
6. **Slutverifiering – öppen:** full EA-domän CI/E2E och distributionsbygge har passerat på GitHub PR #8; externa hosttester återstår. ZIP-build får inte likställas med funktionell runtimeparitet.

## Teknisk granskning före release

- Validera att Plugin/Claude Skills i respektive host kan komma åt de runtime-skript och den state-hantering som projektet kräver.
- Granska att 1.6.33-bygget och befintliga GitHub Actions ersätter äldre anrop utan förlust av semantik.
- Kontrollera att dokumentation, interna hänvisningar och projektmanifestets checksummor är korrekta.
- Kör `python scripts/run_v2_ci_gate.py --project-root . --mode ci` i en miljö med tillräcklig exekveringstid.
- Kör motorns validering med `python scripts/validate_distributions.py --project-root .` efter slutlig build.

## Nästa steg

Samordna CI/release-workflows med nya fem-distributionskontraktet, kör full regression och granska hostparitet innan release.

## Uppföljande modularisering

Tidigare beskrivningar av en enda Skill är historiska. `instructions.mode: modular_skills` är nu aktiverat med tre Skills och gemensam kärna. Se `canonical/SKILL-ARCHITECTURE.md`. Lokala distributions- och innehållskontroller har passerat; hostverifiering kvarstår.
