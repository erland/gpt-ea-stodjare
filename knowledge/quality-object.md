# Kvalitetskontroll för enskilda EA-objekt

## Syfte

Detta dokument definierar hur EA Stödjare ska kvalitetsgranska ett enskilt EA-objekt innan objektet införs, godkänns eller används som stabil grund för vidare analys.

Kontrollen kompletterar `knowledge/classification-guide.md`, `docs/metamodel.md`, `docs/provenance-model.md` och `docs/relations.md`. Den ersätter inte strukturell schemavalidering; ett objekt kan vara syntaktiskt giltigt men semantiskt svagt.

## Grundprinciper

1. **Semantik före formalia.** Ett komplett YAML-objekt är inte kvalitativt godkänt om det representerar fel typ av sak.
2. **Rätt abstraktionsnivå.** Objektet ska beskriva rätt nivå enligt metamodel v1 och inte blanda flera nivåer i samma post.
3. **Evidens efter påståendestyrka.** Ju starkare eller mer organisationsspecifikt påstående, desto tydligare proveniens krävs.
4. **Kandidat före kanon.** Osäker klassificering, svag evidens eller betydande överlapp ska normalt leda till `candidate`, inte `approved`.
5. **Ingen falsk precision.** Saknade fakta ska hellre markeras som öppna frågor än fyllas med antaganden.
6. **Objektgranskning är inte helhetsgranskning.** Dubbletter, orphans och täckning kontrolleras här när de kan upptäckas lokalt, men full modellkvalitet hanteras i steg 14.

## Allvarlighetsnivåer

### ERROR

Objektet bryter mot en regel som gör det ogiltigt eller materiellt missvisande i modellen. Objektet ska inte godkännas innan felet är åtgärdat.

Exempel:

- ID-prefix stämmer inte med objekttypen,
- obligatoriskt attribut saknas,
- en Förmåga är i praktiken ett konkret system,
- ett `approved` objekt saknar tillräcklig proveniens för sitt centrala påstående,
- attributvärde bryter mot tillåtna värden.

### WARNING

Objektet kan finnas kvar som kandidat men har en kvalitetsrisk som bör lösas före godkännande.

Exempel:

- beskrivningen är för vag,
- namnet antyder process eller projekt snarare än förmåga,
- objektet överlappar sannolikt ett befintligt objekt,
- principen saknar rationale eller implications,
- plattformstjänsten beskriver teknik snarare än ett konsumerbart erbjudande.

### INFO

Förbättring eller komplettering som inte blockerar användning.

Exempel:

- ägare saknas men är inte obligatorisk,
- alias kan vara värdefulla,
- ytterligare funktioner kan förtydliga ett IT-stöd.

## Gemensam kontrollordning

EA Stödjare ska kontrollera ett objekt i följande ordning:

1. **Identifierbarhet** – ID, typ och namn.
2. **Klassificering** – är det rätt objekttyp och rätt abstraktionsnivå?
3. **Beskrivning** – är syftet begripligt utan att duplicera namnet?
4. **Objektspecifika attribut** – obligatoriska och rekommenderade fält.
5. **Proveniens** – vad är belagt, härlett, externt eller föreslaget?
6. **Status** – är `candidate`, `approved`, `deprecated` eller `retired` rimligt?
7. **Relationer** – finns semantiskt relevanta relationer och är de tillåtna?
8. **Normalisering** – dubbletter, alias, namnform och överlapp.
9. **Funktionskvalitet** – endast för IT-stöd, Plattformstjänst och Plattform.
10. **Samlad bedömning** – godkänd, godkänd med varningar eller blockerad.

## Gemensamma regler

### QO-COM-001 – Stabilt och korrekt ID

**ERROR** om ID saknas, inte är unikt eller inte följer objekttypens prefix.

ID ska vara stabilt över namnändringar. Ett objekt ska inte få nytt ID enbart för att namnet förbättras.

### QO-COM-002 – Tydligt namn

**WARNING** om namnet är:

- alltför generiskt (`Digitalisering`, `Plattform`, `System`),
- en hel mening,
- främst ett projektnamn eller organisationsnamn,
- laddat med implementationsteknik när objekttypen ska vara teknikoberoende.

Namnet ska vara kort, särskiljande och beskriva objektet snarare än dess dokumentationsrubrik.

### QO-COM-003 – Meningsfull beskrivning

**WARNING** om beskrivningen bara upprepar namnet, är cirkulär eller inte förklarar objektets betydelse i modellen.

En bra beskrivning ska normalt svara på:

- vad objektet är,
- vilket avgränsat syfte det har,
- vad som särskiljer det från närliggande objekt.

### QO-COM-004 – Rätt objekttyp

**ERROR** vid tydlig felklassificering. **WARNING** vid verklig tveksamhet.

Klassificeringen ska följa `knowledge/classification-guide.md`. Källans egen rubrik är inte tillräckligt bevis för typ.

### QO-COM-005 – En sak per objekt

**WARNING** om posten blandar flera separerbara objekt, till exempel `API-hantering och loggplattform` eller `Utveckla, testa och driftsätta programvara` när detta i aktuell modell bör vara flera förmågor.

### QO-COM-006 – Proveniens motsvarar påståendet

**ERROR** om ett `approved` objekt saknar rimligt stöd för centrala organisationsspecifika påståenden.

**WARNING** om ett `candidate` objekt har svag eller oklar evidens och detta inte framgår.

`proposed` får bygga på analys och research, men ska inte skrivas om till `explicit` eller `external` enbart för att förslaget har externa inspirationskällor.

### QO-COM-007 – Status är motiverad

- `candidate`: lämpligt för preliminära, osäkra eller ännu ej beslutade objekt.
- `approved`: kräver tillräcklig kvalitet, stabil klassificering och adekvat evidens.
- `deprecated`: objektet ska inte längre användas som förstahandsval men kan behövas för historik/övergång.
- `retired`: objektet är avslutat och ska inte användas i aktuell arkitektur.

**ERROR** om statusen uppenbart motsäger dokumenterad evidens eller livscykel.

### QO-COM-008 – Relationer är semantiskt rimliga

**ERROR** om objektets relation bryter mot `schemas/relations.yaml`.

**WARNING** om objektet saknar en relation som är central för att förstå dess roll och sådan relation rimligen kan härledas från tillgängligt underlag.

Ingen relation ska uppfinnas enbart för att göra modellen mer sammanlänkad.

### QO-COM-009 – Dubblett och överlapp

**WARNING** om namn, alias, beskrivning eller relationer tyder på att objektet kan vara samma som eller kraftigt överlappa ett befintligt objekt.

EA Stödjare ska först föreslå alias, sammanslagning, specialisering eller tydligare scope – inte skapa en ny dubblett.

### QO-COM-010 – Terminologi och språk

**INFO** eller **WARNING** beroende på betydelse om terminologin avviker från etablerad projektterminologi utan motivering.

## Objektspecifika regler

### Drivkraft

En Drivkraft ska beskriva **varför förändring eller uppmärksamhet behövs**, inte det önskade slutläget.

Kontroller:

- **QO-DRV-001 (ERROR):** objektet är egentligen ett mål, en lösning eller aktivitet.
- **QO-DRV-002 (WARNING):** beskrivningen saknar orsak/tryck/förändringsfaktor och blir bara ett tema.
- **QO-DRV-003 (INFO):** kategori och tidshorisont bör anges när det förbättrar analysen.
- **QO-DRV-004 (WARNING):** drivkraften är så organisationsspecifik att proveniens saknas eller är svag.

Bra exempel: `Ökade krav på digital självservice`.

Svagt exempel: `Införa ny självserviceportal` – detta uttrycker snarare en lösning/aktivitet.

### Mål

Ett Mål ska beskriva **vad organisationen vill uppnå**.

Kontroller:

- **QO-GOAL-001 (ERROR):** objektet är egentligen en drivkraft, princip eller aktivitet.
- **QO-GOAL-002 (WARNING):** målet är formulerat enbart som implementation (`Införa produkt X`).
- **QO-GOAL-003 (INFO):** `target_state`, `time_horizon` eller `measure` bör anges när de är kända och relevanta.
- **QO-GOAL-004 (WARNING):** målet saknar begriplig koppling till en drivkraft eller annan motivering trots att sådan förväntas finnas.

### Princip

En Princip ska vara en **varaktig vägledning för beslut** och inte ett mål eller en detaljerad standard.

Kontroller:

- **QO-PRN-001 (ERROR):** påståendet är egentligen mål, standard eller lösningsbeslut.
- **QO-PRN-002 (WARNING):** `statement` saknas eller är inte normativt/styrande.
- **QO-PRN-003 (WARNING):** `rationale` saknas.
- **QO-PRN-004 (WARNING):** `implications` saknas eller är så vaga att principen inte påverkar beslut.
- **QO-PRN-005 (WARNING):** principen är absolut formulerad men underlaget ger inte stöd för den styrkan.

En god princip ska gå att använda för att skilja mellan två arkitekturalternativ.

### Förmåga

En Förmåga ska beskriva **vad organisationen eller IT behöver kunna åstadkomma**, oberoende av viss process, organisation eller teknisk lösning.

Kontroller:

- **QO-CAP-001 (ERROR):** `capability_type` saknas eller är inte `business`/`it`.
- **QO-CAP-002 (ERROR):** objektet är egentligen process, organisation, funktion, projekt eller IT-stöd.
- **QO-CAP-003 (WARNING):** namnet är lösningsbundet eller produktbundet.
- **QO-CAP-004 (WARNING):** förmågan är alltför bred eller innehåller flera separerbara förmågor.
- **QO-CAP-005 (WARNING):** förmågan är så smal att den snarare beskriver en enskild systemfunktion.
- **QO-CAP-006 (WARNING):** `business`/`it` verkar inte stämma med vem som behöver kunna åstadkomma utfallet.
- **QO-CAP-007 (INFO):** scope bör anges när samma namn annars kan förstås på flera nivåer.
- **QO-CAP-008 (INFO):** för en centralt tillhandahållen IT-förmåga bör `owner` och `consumer_scope` anges när ansvar respektive avsedda konsumenter är kända och relevanta.

För IT-förmågor ska frågan vara ungefär: `Vad behöver IT-verksamheten kunna tillhandahålla eller åstadkomma?`

### IT-stöd

Ett IT-stöd ska vara ett **konkret informationssystem, applikation eller sammanhållen digital tjänst** som stödjer förmågor.

Kontroller:

- **QO-ITS-001 (ERROR):** objektet är egentligen en förmåga, plattformstjänst eller plattform.
- **QO-ITS-002 (WARNING):** det är oklart vilka förmågor objektet stödjer när sådan information rimligen bör finnas.
- **QO-ITS-003 (INFO):** `functions` bör beskriva centrala funktioner när detta förklarar varför stödet är relevant.
- **QO-ITS-004 (WARNING):** funktionerna är formulerade som verksamhetsförmågor eller processer i stället för konkreta tillhandahållna funktioner.
- **QO-ITS-005 (INFO):** lifecycle/criticality bör anges när känt och relevant.

### Plattformstjänst

En Plattformstjänst ska vara ett **konsumerbart gemensamt tekniskt erbjudande** som abstraherar underliggande realisering.

Kontroller:

- **QO-PLS-001 (ERROR):** objektet är egentligen en plattform, ett IT-stöd eller en förmåga.
- **QO-PLS-002 (WARNING):** erbjudandet/konsumenten framgår inte; posten beskriver bara teknik.
- **QO-PLS-003 (INFO):** `functions` bör tydliggöra vad tjänsten erbjuder.
- **QO-PLS-004 (WARNING):** funktionerna beskriver interna plattformsegenskaper utan tydligt konsumentvärde.
- **QO-PLS-005 (INFO):** `service_level` och `consumer_scope` bör anges när detta är relevant och känt.
- **QO-PLS-006 (WARNING):** plattformstjänsten saknar rimlig relation till IT-förmåga eller konsumerande IT-stöd när sådan relation kan beläggas.

### Plattform

En Plattform ska vara en **gemensam teknisk grund eller sammanhållen teknisk miljö**.

Kontroller:

- **QO-PLT-001 (ERROR):** objektet är egentligen en plattformstjänst, ett IT-stöd eller endast en enskild produkt utan plattformsroll.
- **QO-PLT-002 (WARNING):** objektets tekniska avgränsning är oklar.
- **QO-PLT-003 (INFO):** `functions`, `technology` och `products` kan användas för att beskriva realiseringen utan att göra produkt till egen kärnobjekttyp.
- **QO-PLT-004 (WARNING):** en produktetikett används som plattformsnamn men det framgår inte vilken gemensam plattformsroll produkten har.
- **QO-PLT-005 (WARNING):** ingen realiserad Plattformstjänst framgår trots att objektet beskrivs som gemensam plattform och tillgängligt underlag borde kunna visa detta.

### Standard

En Standard ska beskriva en **konkret norm, specifikation eller beslutad standardisering**.

Kontroller:

- **QO-STD-001 (ERROR):** objektet är egentligen en princip eller ett lösningsmönster.
- **QO-STD-002 (WARNING):** referens/version saknas för en extern standard där version är materiellt viktig.
- **QO-STD-003 (WARNING):** det framgår inte om standarden är obligatorisk eller vägledande när detta påverkar användningen.
- **QO-STD-004 (WARNING):** objektet beskriver ett generellt teknikval men inte vad som faktiskt standardiseras.
- **QO-STD-005 (INFO):** `standard_type` bör användas för tydlig kategorisering när katalogen växer.

### Lösningsmönster

Ett Lösningsmönster ska vara en **återanvändbar vägledande lösningsstruktur för ett återkommande problem**, inte en specifik design.

Kontroller:

- **QO-PAT-001 (ERROR):** objektet beskriver en specifik lösning eller implementation.
- **QO-PAT-002 (WARNING):** problem eller context saknas.
- **QO-PAT-003 (WARNING):** approach är för produktspecifik för att fungera som återanvändbart mönster.
- **QO-PAT-004 (INFO):** consequences bör beskrivas när mönstret innebär relevanta trade-offs.

### Referensarkitektur

En Referensarkitektur ska vara en **återanvändbar vägledande arkitektur för ett definierat område**, bredare och mer sammanhängande än ett enskilt lösningsmönster.

Kontroller:

- **QO-RA-001 (ERROR):** objektet är en specifik lösningsarkitektur eller endast ett diagram utan definierad semantik.
- **QO-RA-002 (WARNING):** scope eller applicability saknas.
- **QO-RA-003 (WARNING):** centrala byggblock/guidance saknas så att objektet inte fungerar som referens.
- **QO-RA-004 (WARNING):** referensarkitekturen saknar tydlig återanvändbarhet utanför ett enskilt initiativ.

## Regler för `functions[]`

Funktion är ett underordnat begrepp i v1 och får endast användas på IT-stöd, Plattformstjänst och Plattform.

Kontroller:

- **QO-FUN-001 (ERROR):** `functions` används på annan objekttyp.
- **QO-FUN-002 (WARNING):** funktionen är formulerad som en bred förmåga snarare än en konkret tillhandahållen funktion.
- **QO-FUN-003 (WARNING):** funktionen beskriver implementation (`kör Java 21`) snarare än funktion, om implementationen inte i sig är relevant som funktionell egenskap.
- **QO-FUN-004 (WARNING):** dubbletter eller näst intill identiska funktioner finns inom samma objekt.
- **QO-FUN-005 (INFO):** funktioner bör uttryckas med konsekvent verb-/substantivform inom samma projekt.

## Samlad objektsbedömning

Efter kontrollen ska EA Stödjare lämna en kort och reproducerbar bedömning:

```text
Objekt: CAP-012 – Hantera digitala identiteter
Bedömning: GODKÄND MED VARNINGAR

ERROR: 0
WARNING: 2
INFO: 1

- QO-CAP-004: Scope är brett och kan överlappa behörighetshantering.
- QO-COM-009: Möjlig dubblett med CAP-004 behöver jämföras.
- QO-CAP-007: Ange scope om båda objekten ska finnas kvar.

Rekommendation: Behåll som candidate tills överlappet är utrett.
```

Tillåtna samlade resultat:

- **GODKÄND** – inga ERROR eller materiella WARNING.
- **GODKÄND MED VARNINGAR** – inga ERROR, men en eller flera relevanta WARNING.
- **BLOCKERAD** – minst en ERROR.

Ett objekt ska inte automatiskt ändras från `candidate` till `approved` enbart för att kvalitetskontrollen ger GODKÄND. Statusändring är ett separat modell-/styrningsbeslut.

## Rapportering vid flera objekt

När flera objekt granskas samtidigt bör resultatet sammanfattas i tabell:

| Objekt | Typ | Resultat | Error | Warning | Viktigaste åtgärd |
|---|---|---|---:|---:|---|
| CAP-001 | Förmåga | Godkänd | 0 | 0 | – |
| PLS-002 | Plattformstjänst | Godkänd med varningar | 0 | 2 | Förtydliga konsumentvärde |
| PRN-003 | Princip | Blockerad | 1 | 1 | Klassificera om eller skriv om |

Detaljer ska sedan redovisas endast där de hjälper användaren att åtgärda problemet.

## Gräns mot steg 14

Denna kontroll bedömer kvaliteten hos **enskilda objekt** och deras närmaste relationer. Följande hör huvudsakligen till modellnivån i steg 14:

- fullständig orphan-analys,
- modellens totala täckning,
- systematiska dubbletter över hela katalogen,
- kluster/överfragmentering,
- förmågor utan stöd i hela modellen,
- mål utan realisering,
- principer utan styrande effekt över modellen,
- inkonsistens mellan större delar av modellen.
