# EA Stödjare – projektformat v1

## 1. Syfte

Detta dokument definierar **EA Stödjares projektformat v1**. Formatet gör ett EA-projekt självbeskrivande, versionsbart och integritetskontrollerbart så att en LLM eller ett verktyg kan läsa, verifiera och uppdatera projektet reproducerbart.

Projektformatet beskriver projektbehållaren. Själva EA-semantiken definieras separat av metamodel, relationsmodell, proveniensmodell och det kanoniska YAML-formatet.

---

## 2. Grundprinciper

1. `project-manifest.json` är projektets maskinläsbara ingångspunkt.
2. `model/` är den kanoniska EA-modellen och är source of truth för arkitekturinnehållet.
3. Projektets **revision** och modellformatens **versioner** är olika saker.
4. Alla sökvägar i manifestet är relativa till projektroten och använder `/` som separator.
5. SHA-256 används för att upptäcka oavsiktliga filändringar.
6. `project-manifest.json` hashas inte av sig självt.
7. Genererad dokumentation och export ska kunna återskapas från den kanoniska modellen och behöver därför inte vara del av den kanoniska integritetsmängden.
8. En uppdatering avslutas med att manifestet skrivs sist, efter att revision, revisionslogg och checksummor har uppdaterats.

---

## 3. Minsta projektstruktur

Ett EA-projekt enligt v1 bör minst ha:

```text
<project-root>/
  project-manifest.json
  revision-log.md
  model/
    drivers.yaml
    goals.yaml
    principles.yaml
    capabilities.yaml
    it-support.yaml
    platform-services.yaml
    platforms.yaml
    standards.yaml
    solution-patterns.yaml
    reference-architectures.yaml
    sources.yaml
    relations.yaml
```

Ett fullt projekt kan dessutom innehålla:

```text
  docs/                 # genererade eller stödjande dokument
  exports/              # Confluence/DOCX/PDF m.m.
  sources/              # lokala källfiler när det är lämpligt
  schemas/              # schemas som följer med projektet
  scripts/              # projektlokal generering/validering
  PROJECT_STATUS.md     # införs som arbetsstatus i steg 8
```

`PROJECT_STATUS.md` är avsiktligt inte obligatorisk i projektformat v1 ännu; arbetsstatusens semantik fastställs i steg 8.

---

## 4. `project-manifest.json`

Manifestet ska vara UTF-8-kodad JSON och följa `schemas/project-manifest.schema.json` när schemat finns tillgängligt.

### 4.1 Toppnivå

```json
{
  "format": "ea-stodjare-project",
  "format_version": "1.0",
  "project": {},
  "model": {},
  "integrity": {},
  "files": []
}
```

### 4.2 `format`

Fast värde:

```text
ea-stodjare-project
```

Det gör att en LLM eller validator kan skilja EA Stödjare-projekt från andra zip-/repositoryformat.

### 4.3 `format_version`

Version på själva projektbehållarens kontrakt.

V1 använder:

```text
1.0
```

Ändring av projektformatversion ska ske medvetet och får inte blandas ihop med en vanlig projektrevision.

---

## 5. Projektmetadata

`project` innehåller minst:

| Fält | Betydelse |
|---|---|
| `id` | Stabil maskinläsbar projektidentitet |
| `name` | Användarvänligt projektnamn |
| `kind` | Typ av projektinstans |
| `language` | Primärt språk enligt BCP 47, exempelvis `sv-SE` |
| `revision` | Monotont heltal för projektets innehållsrevision |
| `created_at` | Tidpunkt då manifeststyrd projektinstans skapades |
| `updated_at` | Tidpunkt för senaste manifeststyrda revision |
| `lifecycle_status` | Övergripande projektstatus |

### 5.1 Projekt-ID

Rekommenderat format:

```text
[a-z0-9][a-z0-9-]{2,63}
```

ID:t ska vara stabilt även om projektets visningsnamn ändras.

### 5.2 `kind`

V1 använder fria men dokumenterade värden. Rekommenderade värden är:

- `ea_model` – normalt EA-projekt,
- `ea_model_template` – återanvändbar tom/starter-modell,
- `ea_reference_example` – exempelprojekt.

### 5.3 `lifecycle_status`

Rekommenderade v1-värden:

- `draft`,
- `active`,
- `review`,
- `approved`,
- `archived`.

Detta är projektets övergripande livscykelstatus och ska inte förväxlas med den mer detaljerade arbetsstatus som införs i steg 8.

---

## 6. Revision

`project.revision` är ett monotont heltal som börjar på `1` när projektet tas under manifeststyrning.

En revision ska ökas när en bestående ändring görs i projektets integritetsskyddade innehåll, till exempel när:

- ett EA-objekt läggs till, ändras eller tas bort,
- en relation ändras,
- en källreferens ändras,
- projektstyrande dokument eller schemas som ingår i integritetsmängden ändras.

Revisionen ska **inte** återställas när exempelvis en ny DOCX exporteras från oförändrad modell.

Införandet av manifestet i EA Stödjares utvecklingsprojekt startar revision `1`; tidigare utvecklingssteg 1–6 mappas inte retroaktivt till projektrevisioner.

---

## 7. Modellmetadata

`model` anger vilka semantiska kontrakt projektet följer.

Exempel:

```json
{
  "root": "model",
  "serialization": "YAML",
  "model_format_version": "1.0",
  "metamodel_version": "1.0",
  "relation_model_version": "1.0",
  "provenance_model_version": "1.0"
}
```

Detta möjliggör många projektrevisioner utan att metamodelversionen behöver ändras.

Om EA Stödjare möter en format-/modellversion som den inte stöder ska den inte gissa. Den ska rapportera versionskonflikten och kräva migration eller ett kompatibelt arbetsläge.

---

## 8. Filinventering

`files` är en deterministiskt sorterad lista över integritetsskyddade projektfiler.

Varje post har:

| Fält | Betydelse |
|---|---|
| `path` | Relativ POSIX-sökväg |
| `role` | Filens funktion i projektet |
| `required` | Om filen krävs för den aktuella projektprofilen |
| `sha256` | SHA-256 över filens exakta bytes |

Tillåtna/rekommenderade roller i v1:

- `canonical_model`
- `schema`
- `governance`
- `documentation_source`
- `support`

Källmaterial som kan vara känsligt eller stort behöver inte kopieras in i projektpaketet bara för att det finns en proveniensreferens. `model/sources.yaml` kan referera till externa eller organisatoriska källor utan att källfilen ingår i integritetsinventeringen.

---

## 9. Integritet

V1 använder:

```json
{
  "algorithm": "sha256",
  "manifest_self_hash": false,
  "inventory_order": "path-ascending",
  "canonical_model_required": true
}
```

### 9.1 Hashning

SHA-256 beräknas över filens råa bytes och skrivs som 64 gemena hexadecimala tecken.

Exempel:

```text
sha256(file_bytes).hexdigest()
```

### 9.2 Manifestet hashar inte sig självt

Det undviker rekursiv självreferens. Manifestets konsistens verifieras i stället genom schema, filinventering och att manifestet skrivs sist i varje revision.

### 9.3 Genererade filer

Genererad Markdown, Confluence markup, DOCX och PDF ska normalt inte vara del av den kanoniska integritetsmängden. Senare generatorsteg kan ha egna outputmanifest/checksummor.

---

## 10. Revisionslogg

`revision-log.md` är den människoläsbara historiken över projektets manifeststyrda revisioner.

Minimikrav per revision:

- revision,
- datum/tid,
- kort ändringssammanfattning,
- ändrade fil-/modellområden,
- eventuell kommentar om migration eller särskild risk.

Manifestet är maskinläsbar aktuell status; revisionsloggen är historisk förklaring.

---

## 11. Reproducerbart uppdateringsförfarande

EA Stödjare eller annat verktyg ska vid uppdatering följa denna ordning:

1. Läs `project-manifest.json`.
2. Kontrollera `format` och stödd `format_version`.
3. Kontrollera modellversionerna.
4. Verifiera att integritetsskyddade filer finns och matchar registrerade SHA-256.
5. Läs den kanoniska YAML-modellen.
6. Tillämpa endast beställda/avsedda ändringar.
7. Uppdatera berörda modell- och projektfiler.
8. Lägg till post i `revision-log.md`.
9. Öka `project.revision` exakt en gång för revisionen.
10. Uppdatera `project.updated_at`.
11. Bygg om den deterministiskt sorterade filinventeringen och dess SHA-256.
12. Skriv `project-manifest.json` sist.
13. Verifiera att manifestet nu motsvarar projektets faktiska filer.

Om SHA-256 inte matchar **innan** ändringen ska EA Stödjare inte tyst skriva över avvikelsen. Avvikelsen ska först redovisas och hanteras som en potentiell extern/okänd ändring.

---

## 12. Datum och tid

Manifestets tidsfält använder ISO 8601 med explicit tidszon, exempelvis:

```text
2026-08-20T17:50:00+02:00
```

Det gör tidpunkten entydig utan att kräva UTC-konvertering i människoläsbara projekt.

---

## 13. Exempelmanifest

Det minimala exempelprojektet under `examples/minimal-model/` innehåller ett konkret `project-manifest.json` och `revision-log.md` som följer detta format.

---

## 14. Medvetna avgränsningar i steg 7

Steg 7 definierar **projektbehållaren**, inte:

- detaljerad arbetsstatus och öppna frågor (`PROJECT_STATUS.md`) – steg 8,
- semantisk innehållsextraktion – steg 9,
- valideringsscript – steg 24,
- generatorversioner/outputmanifest – senare generator- och release-steg.

Detta håller projektformatet stabilt utan att föregripa senare arbetsflöden.
