# CI och release för EA Stödjare v2

## Syfte

Steg 30 gör v2:s kompatibilitets- och releasekontrakt obligatoriskt i GitHub Actions. Den centrala grinden är `scripts/run_v2_ci_gate.py`. Workflows ska inte upprätthålla egna divergerande listor av tester.

## Obligatorisk coverage

Grinden verifierar minst:

1. repositoryts native v2/reference project,
2. den frysta v1-fixturen `examples/minimal-model`,
3. rev80 som extended legacy via rekonstruktions- och migrationstest,
4. v1→v2-migrationsmotorn och minimal end-to-end-migration,
5. semantiska eval-definitioner och v2-riskkarta,
6. Builder Knowledge,
7. Markdown/Confluence/DOCX/PDF-generatorregression,
8. Custom GPT- och portable-chat-distributioner,
9. deterministiskt releasepaket som packas upp och valideras på nytt.

I CI och release körs dessutom hela pytest-sviten med `--full-pytest`.

## Maskinläsbar rapport

`--report-file` skapar JSON med körläge, version, obligatorisk coverage, varje steg, exitstatus och slutstatus. Rapporten laddas upp som GitHub Actions-artifact även när grinden misslyckas.

Exempel:

```bash
python scripts/run_v2_ci_gate.py \
  --project-root . \
  --mode ci \
  --full-pytest \
  --report-file build/v2-ci-gate.json
```

## Release

Taggrelease använder taggens semver som enda releaseversion. Innan GitHub Release skapas måste samma v2-grind passera i `release`-läge. Därefter skapas det faktiska releasepaketet, packas upp och valideras ännu en gång av workflowet.

`package_release.py` är fortsatt deterministisk. Build-/testcache, `dist/` och `build/` inkluderas inte i releasezippen.

## Distributioner

Custom GPT- och portable-chat-zippar byggs och valideras av grinden. Workflowet `build-distributions.yml` kör därför grinden innan distributionsartefakter publiceras eller bifogas en GitHub Release.

## Blockerande princip

Ingen release får skapas om någon del av v2-grinden är röd. Det gäller även fel som endast påverkar legacy-kompatibilitet eller migration.
