# Runtime-evals

Den strukturella eval-sviten under `evals/cases/` beskriver beteendekontrakt. Den är **inte** ett runtime-resultat.

För den faktiska releasekörningen används `evals/runtime/RUNBOOK.md`.

Kortflöde:

1. Kör `python3 scripts/prepare_runtime_eval_run.py --target <målkonfiguration> --run-dir <run-katalog>`.
2. Kör varje prompt i en separat konversation mot exakt den Custom GPT- eller portable-chat-konfiguration som ska släppas och spara hela svaret i run-katalogens `responses/`.
3. Bedöm kriterier och kritiska fel i motsvarande `assessments/`-fil.
4. Kör `python3 scripts/assemble_runtime_eval_results.py --run-dir <run-katalog>`; assemblern kräver 29 svar och fullständiga booleska kriteriebedömningar.
5. Kör `python3 scripts/score_runtime_eval_results.py --results <runtime-eval-results.json>`.

`prepare_runtime_eval_packet.py` finns kvar som ett kompakt maskinläsbart exportformat för integrationer. Runbook-flödet är rekommenderat för manuell Custom GPT-evaluering eftersom det separerar prompt, råsvar och bedömning samt fingeravtrycker den testade Builder-konfigurationen.

Release till slutlig `2.0.0` bör kräva att samtliga blockerande fall är PASS och att viktad totalpoäng når eval-svitens releasegräns. RC-paketet får inte beskriva evaldefinitioner som runtime-godkända om denna körning inte är genomförd.
