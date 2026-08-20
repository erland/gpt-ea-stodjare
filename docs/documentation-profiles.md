# Markdown-dokumentationsprofiler v1

## Syfte

Detta dokument definierar hur EA Stödjares kanoniska YAML-modell ska presenteras som Markdown. Profilerna är ett **presentationskontrakt**, inte en ny informationsmodell. All sakinformation ska hämtas från `model/`; genererade Markdown-filer får inte bli en parallell source of truth.

## Grundprinciper

1. **YAML före Markdown.** Sakuppgifter ändras i modellen och därefter regenereras dokumentationen.
2. **Determinism.** Samma modell och samma profilinställningar ska ge semantiskt och textuellt stabil output.
3. **Stabila ID:n visas.** ID används för spårbarhet även när läsaren främst arbetar med namn.
4. **Relationer härleds från `relations.yaml`.** De får inte återskapas genom tolkning av löptext.
5. **Proveniens visas proportionerligt.** Arbetsdokument visar mer evidens än publiceringsvyer.
6. **Tomma sektioner utelämnas.** En rubrik ska inte genereras bara för att mallen har stöd för fältet.
7. **Ingen hallucinerad utfyllnad.** Saknade värden återges inte som antagna fakta.
8. **Sekundära objekttyper hålls tydligt sekundära.** Lösningsmönster och Referensarkitekturer stöds, men får inte dra v1 mot detaljerad lösningsarkitektur.

## Två presentationsnivåer

### Katalogprofil

Katalogen ger en kompakt översikt över en objekttyp. Varje objekttyp får en egen katalogfil.

Rekommenderade outputvägar:

```text
docs/generated/
  drivkrafter.md
  mal.md
  principer.md
  formagor.md
  it-stod.md
  plattformstjanster.md
  plattformar.md
  standarder.md
  losningsmonster.md
  referensarkitekturer.md
```

### Detaljprofil

Detaljprofilen visar ett objekt med relevanta attribut, funktioner, relationer och proveniens.

Rekommenderade outputvägar:

```text
docs/generated/objects/<object-type>/<ID>-<slug>.md
```

Exempel:

```text
docs/generated/objects/capabilities/CAP-001-utveckla-it-stod.md
```

## Arbetsvy och publiceringsvy

Generatorn i steg 16 bör stödja minst två lägen:

- `working`: visar `candidate`, `approved` och `deprecated`; visar confidence, evidenstyp och arbetsnoteringar när de finns.
- `published`: visar som standard endast `approved`; utelämnar interna arbetsnoteringar och tekniska proveniensdetaljer som inte behövs för läsaren.

`retired` ska normalt utelämnas från båda vyerna om inte historik uttryckligen efterfrågas.

Detta är en presentationsregel och ändrar inte objektens status i modellen.

## Gemensam katalogstruktur

Varje katalog ska innehålla:

1. H1 med objekttypens svenska pluralnamn.
2. Kort genererad ingress om vad katalogen visar.
3. Metadata med genereringsläge och modell-/projektrevision när informationen finns tillgänglig.
4. En deterministiskt sorterad tabell.
5. Vid behov kort sektion för relaterade kataloger.

### Sortering

Standard är:

1. `name` normaliserat för alfabetisk sortering,
2. `id` som stabil tie-breaker.

För Förmågor grupperas först på `capability_type` (`business`, `it`) och därefter på namn. En framtida explicit ordningsnyckel får ersätta detta, men introduceras inte i steg 15.

### Katalogkolumner

| Typ | Standardkolumner |
|---|---|
| Drivkraft | ID, Namn, Beskrivning, Kategori, Status |
| Mål | ID, Namn, Beskrivning, Tidshorisont, Status |
| Princip | ID, Namn, Principformulering, Status |
| Förmåga | ID, Namn, Typ, Beskrivning, Status |
| IT-stöd | ID, Namn, Beskrivning, Funktioner, Status |
| Plattformstjänst | ID, Namn, Beskrivning, Konsumentomfång, Funktioner, Status |
| Plattform | ID, Namn, Beskrivning, Teknik/produkter, Funktioner, Status |
| Standard | ID, Namn, Typ, Referens/version, Obligatorisk, Status |
| Lösningsmönster | ID, Namn, Problem/kontext, Status |
| Referensarkitektur | ID, Namn, Scope/tillämpbarhet, Status |

Långa listor i tabellceller ska komprimeras till korta kommaseparerade sammanfattningar. Fullständig information hör hemma på detaljsidan.

## Gemensam detaljstruktur

Alla detaljsidor använder följande ordning när informationen finns:

1. `# <Namn>`
2. identitet och status,
3. beskrivning,
4. objekttypsspecifika attribut,
5. funktioner (endast IT-stöd, Plattformstjänst och Plattform),
6. relationer,
7. proveniens/källor,
8. alias, taggar och ägare,
9. notes endast i `working`-läge.

### Identitetsblock

Detaljsidan ska alltid visa minst:

- ID,
- objekttyp,
- status.

### Relationer

Relationer grupperas efter semantisk relation och riktning. Presentationen får använda naturliga svenska etiketter, men den kanoniska relationstypen ska finnas tillgänglig, exempelvis i parentes eller metadata.

Exempel:

```markdown
## Relationer

### Stöds av

- [Identitets- och behörighetssystem](../it-support/ITS-001-identitets-och-behorighetssystem.md) (`ITS-001`)

### Styr

- [Containerplattformstjänst](../platform-services/PLS-001-containerplattformstjanst.md) (`PLS-001`)
```

Om en relaterad detaljsida inte ingår i aktuell export ska namnet och ID:t ändå visas utan bruten länk.

## Proveniens i Markdown

### Working

Visa per evidenspost när tillgängligt:

- evidenstyp (`explicit`, `derived`, `proposed`, `external`),
- källa och referens,
- confidence,
- rationale,
- `derived_from`,
- transferability för extern evidens.

### Published

Visa i första hand källor/referenser som är relevanta för läsaren. `proposed` ska fortfarande framgå som förslag om objektet publiceras i en granskningsleverans. Tekniska interna fält kan döljas, men får aldrig presenteras som starkare evidens än modellen anger.

## Objekttypsprofiler

### Drivkraft

Detaljsidan prioriterar kategori, tidshorisont och evidens för varför drivkraften är relevant. Den ska inte omformulera drivkraften till ett mål.

### Mål

Detaljsidan prioriterar måltillstånd, tidshorisont och mått. Relationer till drivkrafter och förmågor är särskilt relevanta.

### Princip

Detaljsidan prioriterar `statement`, `rationale` och `implications`. Om `statement` saknas används inte beskrivningen automatiskt som en beslutad principformulering; saknaden synliggörs i arbetsvy.

### Förmåga

Detaljsidan visar `capability_type` tydligt och får inte lägga in process-, organisations- eller systembeskrivningar som om de vore förmågeattribut. Relevanta relationer till mål, IT-stöd och Plattformstjänster visas.

### IT-stöd

Detaljsidan prioriterar funktioner, livscykel och criticality när de finns. Förmågor som stöds och Plattformstjänster som används ska kunna visas via relationsregistret.

### Plattformstjänst

Detaljsidan prioriterar erbjudandet till konsumenten: funktioner, service level och consumer scope. Underliggande Plattformar visas genom `realized_by`.

### Plattform

Detaljsidan prioriterar teknisk grund, funktioner, teknik och produkter. Den ska tydligt skiljas från den konsumtionsorienterade Plattformstjänsten.

### Standard

Detaljsidan prioriterar standardtyp, referens, version och om den är obligatorisk. Relationen till styrda/begränsade objekt ska synliggöras.

### Lösningsmönster

Detaljsidan prioriterar problem, kontext, angreppssätt och konsekvenser. Den ska förbli generell och återanvändbar och inte fyllas med specifik lösningsdesign.

### Referensarkitektur

Detaljsidan prioriterar scope, applicability, building blocks och guidance. Den beskriver återanvändbar vägledning, inte en specifik implementationsarkitektur.

## Mallkontrakt

Mallarna under `templates/markdown/` använder enkla dubbla klamrar som **designmarkörer** i steg 15, exempelvis `{{name}}` och `{{catalog_rows}}`. De är ännu inte bundna till ett särskilt template-bibliotek. Steg 16 ska implementera renderingen deterministiskt och får vid behov ersätta markörerna med en intern representationsmodell så länge outputkontraktet består.

Gemensamma markörer:

- `{{name}}`
- `{{id}}`
- `{{status}}`
- `{{description}}`
- `{{metadata}}`
- `{{relations}}`
- `{{provenance}}`
- `{{catalog_rows}}`

Objekttypsspecifika markörer dokumenteras direkt i respektive mall.

## Filnamn och länkar

- Filnamn använder objektets stabila ID följt av en slug av namnet.
- Slug ska vara gemener, ASCII där praktiskt möjligt och bindestrecksseparerad.
- ID:t gör att en namnändring är spårbar även om filnamnet ändras.
- Interna länkar ska beräknas från outputstrukturen, inte lagras i YAML-modellen.

## Markdown-konventioner

- ATX-rubriker (`#`, `##`, `###`).
- Pipe-tabeller för kataloger.
- Vanliga punktlistor för funktioner och relationer.
- Inga HTML-tabeller i standardprofilen.
- Ingen presentationsspecifik färgsättning eller layoutmetadata i YAML.
- Svenska rubriker i svensk output; intern schema-/relationssemantik får fortsatt använda engelska nycklar.
- Escape av `|`, radbrytningar och andra Markdown-känsliga tecken ska ske i generatorn.

## Source of truth och ändringsregel

Om en användare vill ändra innehållet i en genererad Markdown-fil ska EA Stödjare:

1. identifiera motsvarande objekt/relationsdata i YAML,
2. föreslå eller genomföra ändringen där,
3. regenerera Markdown,
4. inte handredigera den genererade filen som primär metod.

Manuellt redaktionellt innehåll som inte hör hemma i EA-modellen ska i framtiden kunna hanteras som separat dokumentationskälla, men ett sådant system introduceras inte i v1 steg 15.

## Profiler som medvetet inte införs nu

- diagramprofiler,
- ArchiMate-vyer,
- presentationsslides,
- dashboards/heatmaps,
- lösningsarkitekturprofiler,
- organisations- och processvyer.

Dessa kan senare byggas ovanpå samma modell och relationsregister.
