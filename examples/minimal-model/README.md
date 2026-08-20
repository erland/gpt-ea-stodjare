# Minimal EA-modell

Detta är syntetisk testdata för EA Stödjare och inte en rekommendation för någon verklig organisation.

Modellen demonstrerar samtliga primära och sekundära objekttyper, verksamhets- och IT-förmåga, funktioner på de tre tillåtna objekttyperna, interna och externa källor, evidenskategorierna samt samtliga relationstyper i v1.

Filerna under `model/` kan senare användas som fixtures för validerings- och genereringstester.


## Projektformat

Exempelprojektet är från steg 7 även en komplett projektinstans med `project-manifest.json` och `revision-log.md`. Manifestet inventerar de kanoniska modellfilerna och skyddar dem med SHA-256.


## Genererad Markdown

Steg 16 använder detta projekt som end-to-end-fixture. `docs/generated/` är deterministiskt genererad `working`-output från YAML-modellen och kan återskapas med:

```bash
python ../../scripts/generate_markdown.py --project-root . --mode working
```

Outputen är ett derivat och inte source of truth.


## DOCX/PDF

Generera distributionsdokument från projektroten:

```bash
python scripts/export_documents.py --project-root examples/minimal-model --mode published --output-dir exports/document --basename ea-dokumentation-published
```

Referensfiler finns i `exports/document/`.
