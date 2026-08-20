# EA Stödjare – teknisk målbild efter steg 2

## 1. Syfte

Detta dokument beskriver den tekniska målbild som följer av produktvisionen och återbruksanalysen. Det är inte en komplett implementationsspecifikation; detaljer införs stegvis enligt utvecklingsplanen.

---

## 2. Två nivåer ska hållas isär

EA Stödjare består konceptuellt av två separata nivåer:

### A. GPT-/distributionsprojektet

Innehåller det som definierar själva EA Stödjare:

```text
ea-stodjare/
  README.md
  docs/
  gpt-configuration/          # införs senare
  knowledge-upload/           # införs senare
  templates/                  # införs senare
  scripts/                    # införs senare
  portable/                   # införs senare
  .github/workflows/          # införs senare
```

### B. EA-projekt skapade eller förvaltade av GPT:n

Framtida EA-projekt kommer principiellt att innehålla:

```text
<ea-projekt>/
  model/                      # kanonisk strukturerad EA-modell
  docs/                       # genererad/arbetsrelaterad dokumentation
  sources/                    # källmetadata/referenser vid behov
  exports/                    # genererade distributionsformat
  scripts/                    # lokal validering/generering
  project-manifest.json       # definierat i steg 7
  revision-log.md             # definierad i steg 7
  PROJECT_STATUS.md           # införs i steg 8
```

Den exakta strukturen får inte låsas förrän metamodel, relationsmodell och YAML-schema är definierade.

---

## 3. Källor och sanningshierarki

Den planerade sanningshierarkin är:

```text
1. Projektformat + schemas
2. Kanonisk YAML-modell
3. Proveniens/källreferenser
4. Genererade dokumentvyer
5. Exportformat
```

Genererad Markdown, Confluence markup, DOCX och PDF får inte användas som konkurrerande redigerbara masterdata.

---

## 4. GPT-arkitektur

När Custom GPT-delen införs ska strukturen följa:

```text
gpt-configuration/instructions.md
        |
        +-- kort roll/scope/styrande arbetsregler

knowledge-upload/
        |
        +-- metamodel
        +-- relationer
        +-- klassificering
        +-- proveniens
        +-- research
        +-- kvalitet
        +-- projektformat
        +-- outputregler
```

Samma källfiler ska där det är möjligt ligga bakom både Custom GPT- och portabel chat-distribution.

---

## 5. Planerad distributionsmodell

När projektet nått rätt mognad ska två distributioner kunna byggas från samma repository:

```text
ea-stodjare-custom-gpt-vX.Y.Z.zip

ea-stodjare-chat-vX.Y.Z.zip
```

Den portabla versionen ska minst kunna innehålla:

```text
START-HERE.md
VERSION                    # genererad vid build
MANIFEST.json              # distributionsmanifest
assistant/instructions.md
knowledge/
templates/ea-project/
examples/
```

En Git-release `v<SemVer>` ska vara auktoritativ versionskälla. En eventuell `VERSION` i distributionen är genererad output, inte källversion.

---

## 6. Planerade tekniska kontrollnivåer

### Nivå 1 – distributionsvalidering

Kontrollerar exempelvis:

- Builder Instructions-storlek,
- Knowledge-filantal,
- byte-identitet mellan källor och distribution,
- korrekt releaseversion,
- manifest och checksummor.

### Nivå 2 – EA-projektintegritet

Kontrollerar exempelvis:

- filinventering,
- SHA-256,
- revisionsdisciplin,
- projektformat.

### Nivå 3 – strukturell EA-validering

Kontrollerar exempelvis:

- YAML/schema,
- unika ID:n,
- giltiga relationer,
- giltiga referenser.

### Nivå 4 – semantisk EA-kvalitet

Bedöms av GPT/evals, exempelvis:

- abstraktionsnivå,
- klassificering,
- dubbletter,
- täckning,
- evidensdisciplin,
- kvalitet på research och modellförslag.

Det är viktigt att teknisk schema-validitet inte förväxlas med semantisk arkitekturkvalitet.

---

## 7. Reproducerbar generering

Målbilden är:

```text
YAML model
   |
   +--> Markdown
   +--> Confluence markup
   +--> sammansatt Markdown --> DOCX
                              --> PDF
```

Generatorerna ska vara deterministiska så långt det är rimligt: samma modell och generatorversion ska ge samma semantiska output.

---

## 8. Medvetet uppskjutna tekniska frågor

Följande ska inte avgöras i steg 2:

- exakt YAML-schema,
- exakt relationsvokabulär,
- om JSON Schema eller annan validator används för YAML,
- exakt Pandoc-template för DOCX/PDF,
- Confluence-exportens implementation,
- Builder Knowledge-filernas slutliga uppdelning,
- GitHub Actions-detaljer,
- visualiseringsformat.

De avgörs i de utvecklingssteg där tillräcklig semantisk grund finns.

---

## 9. Nästa arkitekturella beslut

Nästa steg är **steg 3 – definiera EA-metamodell v1**.

Det är den första punkt där EA Stödjares egen domänmodell formaliseras. Återbruksanalysen sätter därför en tydlig regel för nästa steg:

> Metamodellen ska utgå från enterprise architecture-semantik och den fastställda produktvisionen, inte från vilka filer eller mekanismer Lärobokskaparen råkar ha.
