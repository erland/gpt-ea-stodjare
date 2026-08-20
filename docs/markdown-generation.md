# Deterministisk Markdown-generering

## Syfte

`scripts/generate_markdown.py` genererar katalog- och detaljvyer från den kanoniska YAML-modellen enligt `docs/documentation-profiles.md` och mallarna under `templates/markdown/`.

Generatorn ändrar aldrig YAML-modellen. `docs/generated/` är alltid ett derivat och kan regenereras från modellen.

## Användning

Från projektroten:

```bash
python scripts/generate_markdown.py --project-root . --mode working
```

För publiceringsvy:

```bash
python scripts/generate_markdown.py --project-root . --mode published
```

Alternativ outputkatalog kan anges med `--output-dir`.

## Lägen

- `working`: inkluderar `candidate`, `approved` och `deprecated` och visar mer proveniensinformation.
- `published`: inkluderar endast `approved` och reducerar arbetsintern proveniens.
- `retired` utelämnas i båda standardlägena.

## Determinism

Generatorn använder:

- stabil objektsortering,
- stabila ID-baserade filnamn,
- deterministiska sluggar,
- relationer endast från `model/relations.yaml`,
- källinformation endast från `model/sources.yaml`,
- stabil gruppering av relationer och listor.

Samma modell, mallar, projektrevision och presentationsläge ska därför ge byte-identisk Markdown.

## Interna länkar

Detaljsidor länkas med relativa länkar. Om ett relaterat objekt inte ingår i aktuell export visas namn/ID utan länk. YAML-modellen innehåller inga presentationslänkar.

## Test

`tests/generation/test_generate_markdown.py` kör generatorn två gånger och jämför hash av hela Markdown-trädet. Testet verifierar också att `published` filtrerar bort kandidater.

Exempel:

```bash
python tests/generation/test_generate_markdown.py
```

## Exempeloutput

`examples/minimal-model/docs/generated/` innehåller genererad `working`-output från den syntetiska minimalmodellen och fungerar som konkret referens för formatet.
