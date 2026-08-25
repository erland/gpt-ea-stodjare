# Full end-to-end regression – v2

Den permanenta full-E2E-grinden verifierar de tolv centrala arbetskedjor som tillsammans täcker v2:s viktigaste användnings- och kompatibilitetsflöden.

Kör:

```bash
python3 scripts/run_full_e2e_regression.py --project-root . --report-file build/full-e2e-report.json
```

Grinden verifierar: enkelt native v2-projekt, avancerad v2-metamodell med extensions, öppning och fortsatt redigering av v1 utan migration, v1-migration, öppning och migration av rev80, produktanalys för både IT-stöd och Plattformstjänst, researchbaserat modellförslag, derived views och export till Markdown/Confluence/DOCX/PDF.

Regressionen är diagnostisk och muterar inte källprojektet. Produkt- och researchscenarierna använder syntetiska källor så testerna är reproducerbara och inte beroende av föränderliga externa tjänster.

Den permanenta releasebaslinjen finns i `compatibility/reports/v2-e2e-baseline.yaml`.
