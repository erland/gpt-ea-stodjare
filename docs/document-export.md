# DOCX- och PDF-export

## Syfte

`scripts/export_documents.py` skapar distributionsformat från den kanoniska EA-modellen utan att införa en parallell sanningskälla.

Exportkedjan är:

```text
YAML-modell
  -> deterministisk Markdown-generering
  -> sammansatt distributionsdokument
  -> Pandoc DOCX
  -> LibreOffice PDF
```

DOCX och PDF är alltså alltid derivat. Ändringar ska göras i `model/*.yaml` och därefter regenereras.

## Förutsättningar

- Python 3
- Pandoc
- LibreOffice (`libreoffice` eller `soffice`)

## Användning

Från projektroten:

```bash
python scripts/export_documents.py --project-root . --mode published
```

Arbetsmaterial inklusive kandidater:

```bash
python scripts/export_documents.py --project-root . --mode working
```

Annan outputkatalog och filbas:

```bash
python scripts/export_documents.py \
  --project-root . \
  --mode published \
  --output-dir exports/document \
  --basename arkitekturdokumentation
```

## Innehåll och struktur

Exporten innehåller:

- dokumenttitel från projektmanifestet,
- presentationsläge och projektrevision,
- innehållsförteckning,
- katalogavsnitt för samtliga objekttyper som ingår i aktuellt läge,
- detaljsektioner för objekten,
- relationer, funktioner och proveniens enligt Markdown-profilerna.

Katalogerna följer den ordning som definierats för EA Stödjare v1: drivkrafter, mål, principer, förmågor, IT-stöd, plattformstjänster, plattformar, standarder, lösningsmönster och referensarkitekturer.

## Layoutprinciper

Version 1 använder avsiktligt en enkel och robust dokumentlayout:

- Pandocs DOCX-standardformat,
- rubrikhierarki som ger navigerbar innehållsförteckning,
- Pandocs tabellrendering för katalogtabeller,
- varje övergripande katalogavsnitt börjar på ny sida i DOCX/PDF,
- tomma kataloger utelämnas i `published` men behålls i `working`,
- DOCX som grund även för PDF-export så att formaten hålls nära varandra,
- inga presentationsspecifika data lagras i YAML-modellen.

Mer avancerad grafisk profil kan senare införas genom ett versionshanterat Pandoc-reference-DOCX utan att ändra informationsmodellen.

## Determinism

Samma:

- YAML-modell,
- projektrevision,
- Markdown-generator,
- presentationsläge,
- Pandoc/LibreOffice-versioner

ska ge semantiskt samma dokument. Binär DOCX/PDF kan innehålla verktygsspecifik metadata och betraktas därför inte som byte-deterministisk på samma sätt som Markdown/Confluence-exporten.

## Verifiering

`tests/generation/test_export_documents.py` verifierar att:

- DOCX och PDF skapas,
- båda filerna är icke-tomma,
- DOCX innehåller projektets titel och förväntade EA-sektioner,
- PDF kan parsas och innehåller förväntad text,
- `published` inte tar med objekt med status `candidate`.

Visuell QA av referensexporten görs dessutom genom rendering av både DOCX och PDF till sidbilder.
