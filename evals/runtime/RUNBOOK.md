# Runbook – faktisk runtime-eval inför EA Stödjare 2.0.0

Detta flöde används för att skapa **LLM-runtime-evidens**. Det ersätter inte de deterministiska repository-testerna och får inte markeras som genomfört förrän svar faktiskt har producerats av den distributionskonfiguration som ska släppas.

## 1. Frys målkonfigurationen

Bygg/installer den Custom GPT- eller portable-chat-konfiguration som ska bedömas från denna revision. Ändra inte instruktioner eller Knowledge under en pågående evalrun. Om målkonfigurationen ändras ska en ny run skapas.

## 2. Skapa en run

```bash
python3 scripts/prepare_runtime_eval_run.py \
  --target "EA Stödjare 2.0.0" \
  --run-dir evals/runtime/runs/rc2-runtime
```

Run-manifestet innehåller ett SHA-256-fingeravtryck av `custom-gpt/instructions.md` och samtliga genererade Builder Knowledge-filer. Det gör det möjligt att visa vilken konfiguration svaren avser.

## 3. Kör 29 isolerade konversationer

För varje fil i `prompts/`:

1. Starta en **ny separat konversation** mot exakt samma målkonfiguration.
2. Skicka endast texten under rubriken `Prompt`.
3. Lägg inte in grading criteria, expected behaviors eller forbidden behaviors i modellen.
4. Spara hela assistentsvaret oförändrat i motsvarande `responses/EVAL-xxx.md`.
5. Använd inte svar från tidigare evalfall som kontext.

Detta minskar risken för cross-case contamination och för att modellen optimerar mot bedömningsrubriken.

## 4. Bedöm varje svar

Öppna motsvarande YAML-fil i `assessments/` och sätt varje kriterium till `true` eller `false`. Lämna det inte som `null`.

`critical_failures` ska endast innehålla faktiskt observerade kritiska fel. `notes` används för kort evidens/motivering, gärna med citatfragment eller referens till relevant del av svaret.

Bedömningen ska göras mot respektive evaldefinition under `evals/cases/`, inte mot ett önskat facitsvar.

## 5. Sammanställ resultatet

```bash
python3 scripts/assemble_runtime_eval_results.py \
  --run-dir evals/runtime/runs/rc2-runtime
```

Assemblern vägrar skapa ett runtime-resultat om något svar saknas eller något kriterium fortfarande är obestämt.

## 6. Poängsätt releasegrinden

```bash
python3 scripts/score_runtime_eval_results.py \
  --results evals/runtime/runs/rc2-runtime/runtime-eval-results.json \
  --report evals/runtime/runs/rc2-runtime/runtime-eval-score.json
```

För slutlig `2.0.0` gäller eval-svitens release gate: samtliga blockerande fall ska vara `PASS` och den viktade totalsumman ska nå minst 85 procent.

## 7. Spara releaseevidens

Spara minst följande tillsammans med releaseunderlaget:

- `run-manifest.json`
- alla `responses/EVAL-xxx.md`
- alla `assessments/EVAL-xxx.yaml`
- `runtime-eval-results.json`
- `runtime-eval-score.json`

Om målkonfigurationen ändras efter körningen är evidensen inte längre tillräcklig för den nya konfigurationen; skapa då en ny run.
