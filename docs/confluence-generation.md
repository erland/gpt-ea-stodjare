# Confluence markup-generering

## Syfte

EA Stödjare kan från steg 17 generera **Confluence wiki markup** från samma kanoniska YAML-modell som används för Markdown-exporten. Confluence-exporten är ett presentationsderivat och får inte redigeras som en parallell source of truth.

## Källa

Generatorn läser endast projektets kanoniska modell och styrmetadata:

- `model/*.yaml`
- `model/relations.yaml`
- `model/sources.yaml`
- `project-manifest.json` för projektrevision

Den läser inte genererad Markdown som informationskälla. Markdown och Confluence är därmed två deterministiska vyer av samma EA-modell.

## Kommando

Från projektroten:

```bash
python3 scripts/generate_confluence.py --project-root . --mode working
```

Standardkatalog är:

```text
exports/confluence/
```

Publiceringsläge:

```bash
python3 scripts/generate_confluence.py --project-root . --mode published
```

Precis som Markdown-generatorn innebär:

- `working`: `candidate`, `approved` och `deprecated` får visas,
- `published`: endast `approved` visas.

## Outputstruktur

```text
exports/confluence/
  drivkrafter.txt
  mal.txt
  principer.txt
  formagor.txt
  it-stod.txt
  plattformstjanster.txt
  plattformar.txt
  standarder.txt
  losningsmonster.txt
  referensarkitekturer.txt
  objects/
    drivers/
    goals/
    principles/
    capabilities/
    it-support/
    platform-services/
    platforms/
    standards/
    solution-patterns/
    reference-architectures/
```

Varje `.txt`-fil innehåller Confluence wiki markup som kan kopieras till en Confluence-sida eller användas som underlag för senare publiceringsautomation.

## Renderingsregler

- Rubriker använder `h1.`, `h2.` och `h3.`.
- Katalogtabeller använder Confluence-formatet `|| header ||` och `| cell |`.
- Listor använder `*`.
- Genereringsmetadata visas i en `{info}`-panel.
- Objektreferenser använder Confluence-sidlänkar med sidtiteln `ID – Namn`.
- Relationer renderas i båda läsriktningarna men lagras fortsatt endast en gång i `relations.yaml`.
- Funktioner hämtas från respektive objekts `functions[]`.
- Proveniens och källreferenser hämtas från den kanoniska modellen.
- `working` visar mer evidensmetadata än `published`.

## Semantisk konsistens med Markdown

Markdown och Confluence använder samma:

- statusfiltrering,
- objektsortering,
- objekttyper,
- relationer,
- funktioner,
- proveniens,
- projektmetadata.

De kan skilja sig i presentation och länksyntax men får inte skilja sig i EA-innehåll. Regressionstestet `tests/generation/test_generate_confluence.py` verifierar bland annat att båda formaten genererar samma uppsättning objektsidor och att publiceringsläget filtrerar kandidater på samma sätt.

## Determinism

Generatorn rensar tidigare `.txt`-output i målkatalogen före renderingen och skriver filer i deterministisk ordning. Två körningar mot oförändrad modell och samma projektrevision ska ge identiskt hashat outputträd.
