# Strukturell validering

## Syfte

Steg 24 inför deterministisk strukturell validering av ett EA Stödjare-projekt. Valideringen ska hitta tekniska och referentiella fel innan semantisk LLM-granskning görs.

Huvudverktyget är:

```bash
python scripts/validate_project.py --project-root .
```

Ett annat EA-projekt kan valideras mot denna repos schemas och generatorer:

```bash
python scripts/validate_project.py \
  --project-root /sokvag/till/projekt \
  --repo-root /sokvag/till/ea-stodjare
```

Exit code `0` betyder att inga blockerande strukturella fel hittades. Exit code `1` betyder att minst ett fel hittades.

## Kontroller

Validatorn kontrollerar följande lager.

### Manifest och filintegritet

- `project-manifest.json` finns och är giltig JSON.
- manifestet följer `schemas/project-manifest.schema.json`.
- filinventeringen är unik och deterministiskt sorterad.
- obligatoriska registrerade filer finns.
- SHA-256 stämmer för registrerade filer.
- den kanoniska modellkatalog som manifestet pekar på finns.

### Kanonisk YAML-modell

- samtliga obligatoriska modellfiler finns,
- YAML kan parsas,
- filernas envelope följer modellformat v1,
- `schema_version` och `object_type` är korrekta,
- obligatoriska objektfält finns,
- objekttyp matchar filen,
- ID-prefix matchar objekttypen,
- objekt-ID:n är globala och unika,
- statusvärden är tillåtna,
- `capability_type` är `business` eller `it`,
- `functions[]` används endast där metamodel v1 tillåter det och har inget globalt ID.

### Källor och proveniens

- käll-ID följer formatet och är unika,
- `source_type` är definierad,
- refererade källor finns,
- `derived_from` refererar befintliga objekt,
- evidenstyper följer de obligatoriska reglerna för source/rationale,
- confidence och transferability har tillåtna värden,
- external-evidens använder en extern källtyp.

### Relationer

- relations-ID följer formatet och är unika,
- source och target finns,
- relationstypen är definierad,
- source/target-kombinationen är tillåten enligt `schemas/relations.yaml`,
- target constraints, exempelvis IT-förmåga för plattformstjänstens `supports`, följs,
- förbjudna självrelationer upptäcks,
- exakta dubblettrelationer upptäcks,
- relationens proveniens valideras.

### Genererade artefakter

När lagrade genererade artefakter finns kontrolleras de som derivat:

- Markdown regenereras i `working` och jämförs byte-för-byte med `docs/generated/`.
- Confluence markup regenereras i `working` och jämförs byte-för-byte med `exports/confluence/`.
- lagrade PDF-filer kontrolleras för PDF-signatur.
- lagrade DOCX-filer kontrolleras för OOXML/ZIP-signatur.

DOCX/PDF:s fullständiga reproducerbarhet och innehållskvalitet fortsätter att testas av de dedikerade exporttesterna eftersom binär metadata kan göra direkt byte-jämförelse olämplig.

## Fel och varningar

Validatorn använder stabila kodprefix:

- `STR-MAN-*` – manifest/integritet,
- `STR-MODEL-*` – modellformat,
- `STR-ID-*` – identitet,
- `STR-SRC-*` – källregister,
- `STR-PROV-*` – proveniens,
- `STR-REL-*` – relationer,
- `STR-GEN-*` – genererade artefakter.

Fel blockerar godkänd strukturell validering. Varningar rapporteras men ger exit code `0`.

Maskinläsbart resultat fås med:

```bash
python scripts/validate_project.py --project-root . --json
```

## Avgränsning

Steg 24 validerar sådant som kan avgöras deterministiskt. Den försöker inte ersätta:

- objektspecifik semantisk kvalitet i `knowledge/quality-object.md`,
- modellens helhetskvalitet i `knowledge/quality-model.md`,
- bedömning av om en förmåga är välformulerad,
- relevans/överförbarhet i research utöver formella proveniensregler,
- om en arkitekturmodell är ändamålsenlig för organisationen.

Dessa delar hör hemma i kvalitetsarbetsflödena och senare semantiska evals.

## Regressionstest

Kör:

```bash
python tests/validation/test_validate_project.py
```

Testsviten verifierar både giltiga projekt och avsiktligt trasiga varianter, bland annat dubblett-ID, saknad relationsreferens, otillåten relation, hash-avvikelse och stale Markdown.
