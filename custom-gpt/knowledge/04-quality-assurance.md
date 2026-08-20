<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Quality Assurance

Denna fil konsoliderar följande kanoniska källor:

- `knowledge/quality-object.md`
- `knowledge/quality-model.md`

---


# KÄLLA: `knowledge/quality-object.md`

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


# KÄLLA: `knowledge/quality-model.md`

# Kvalitetskontroll för hela EA-modellen

## Syfte

Detta dokument definierar hur EA Stödjare ska kvalitetsgranska **hela den kanoniska EA-modellen som ett sammanhängande system**. Kontrollen kompletterar kvalitetskontrollen för enskilda objekt i `knowledge/quality-object.md`.

En modell kan bestå av individuellt välformulerade objekt och ändå vara svag som helhet. Helhetskontrollen ska därför hitta problem som endast blir synliga när objekt, relationer, proveniens och modellens täckning analyseras tillsammans.

Kontrollen ersätter inte strukturell schemavalidering och ska inte framtvinga relationer eller objekt som saknar evidens.

## Grundprinciper

1. **Helhet före mängd.** Fler objekt innebär inte automatiskt en bättre EA-modell.
2. **Evidens före grafkomplettering.** Saknade länkar får inte fyllas i endast för att göra modellen mer sammanhängande.
3. **Approved kräver högre sammanhang än candidate.** Preliminära kandidater får vara partiellt anslutna medan godkända objekt förväntas ha ett begripligt sammanhang.
4. **Täckning bedöms mot modellens uttalade scope.** En modell ska inte kritiseras för att inte beskriva sådant som ligger utanför dess avgränsning.
5. **Semantiska luckor skiljs från dataluckor.** En verklig arkitekturlucka är inte samma sak som att underlaget ännu inte dokumenterar relationen.
6. **Ingen falsk symmetri.** Alla objekttyper behöver inte förekomma i samma antal eller ha samma relationsgrad.
7. **Spårbarhet ska kunna förklaras, inte bara räknas.** En kedja är värdefull först när relationerna har relevant semantik och proveniens.
8. **Kvalitetskontroll är diagnostik.** Den ska identifiera risker, mönster och frågor – inte automatiskt fatta arkitekturbeslut.

## Allvarlighetsnivåer

### ERROR

Ett fel som gör modellen strukturellt eller semantiskt motsägelsefull, eller som innebär att centrala godkända delar inte kan användas tillförlitligt.

Exempel:

- relation refererar till ett objekt som inte finns,
- `derived_from` bildar en härledningscykel,
- två godkända objekt har samma ID,
- en lagrad relation bryter mot relationsmodellen,
- en godkänd relation har source/target som inte är tillgängliga i aktuell modell.

### WARNING

En tydlig kvalitetsrisk som bör granskas men som inte nödvändigtvis gör modellen ogiltig.

Exempel:

- godkända mål saknar koppling till drivkrafter eller förmågor trots att sådan spårbarhet förväntas,
- godkända IT-stöd saknar känd koppling till förmågor,
- plattformstjänster saknar känd konsument- eller realiseringskontext,
- flera objekt verkar överlappa kraftigt,
- en del av modellen är oproportionerligt tät eller isolerad.

### INFO

Observation som kan förbättra modellen eller hjälpa fortsatt analys utan att indikera ett direkt kvalitetsproblem.

Exempel:

- ett område har betydligt lägre dokumentationstäthet än andra,
- vissa candidates saknar relationer,
- fler tvärgående standardkopplingar kan vara värda att undersöka.

## Resultatnivåer

Helhetskontrollen rapporterar:

- **GODKÄND** – inga ERROR och inga materiella WARNING.
- **GODKÄND MED VARNINGAR** – inga ERROR men en eller flera WARNING.
- **BLOCKERAD** – minst ett ERROR.

Resultatet ändrar inte automatiskt objektstatus eller modellens livscykelstatus.

## Förutsättningar före semantisk granskning

Innan helhetskontrollen genomförs ska EA Stödjare säkerställa att:

1. projektmanifestet kan läsas,
2. modellfilerna kan parsas,
3. ID:n kan indexeras,
4. relationer kan läsas,
5. källreferenser kan lösas i den utsträckning modellen kräver.

Om dessa förutsättningar inte uppfylls ska relevanta strukturella fel rapporteras och beroende semantiska kontroller markeras som **ej bedömbara**, inte gissas.

# Kontrollområden

## 1. Referentiell och semantisk integritet

### QM-INT-001 – Unika objekt-ID:n

**ERROR** om samma objekt-ID förekommer mer än en gång i den samlade modellen.

### QM-INT-002 – Relationernas endpoints finns

**ERROR** om `source` eller `target` i en relation inte motsvarar ett känt objekt.

### QM-INT-003 – Relationstyp och source/target är tillåtna

**ERROR** om en lagrad relation inte följer `schemas/relations.yaml`.

### QM-INT-004 – Inga dubbellagrade identiska relationer

**WARNING** om samma `(source, relation, target)` lagras flera gånger. Separat evidens ska i normalfallet samlas i samma relationspost i stället för att duplicera relationen.

### QM-INT-005 – Ingen lagrad invers dubblett

**WARNING** om två relationer endast uttrycker varandras presentationsinvers och därmed dubbellagrar samma semantik i strid med relationsmodellen.

### QM-INT-006 – Härledningsgraf utan cykler

**ERROR** om `derived_from` bildar en cykel. Ett objekt eller en relation får inte direkt eller indirekt härledas från sig självt.

### QM-INT-007 – Källreferenser kan lösas

**ERROR** för obligatorisk/kärnproveniens på godkända objekt eller relationer om refererad source-ID saknas.

**WARNING** för motsvarande brist på candidates när osäkerheten är tydligt deklarerad.

## 2. Orphans och kontextlösa objekt

Ett orphan definieras här som ett objekt utan relevanta in- eller utgående EA-relationer. Orphan är **inte automatiskt fel**.

### QM-ORP-001 – Godkänt mål utan arkitekturkontext

**WARNING** om ett `approved` Mål saknar relation till både motiverande Drivkraft och realiserande/stödjande arkitekturkontext trots att modellen är avsedd att beskriva strategi-till-arkitektur-spårbarhet.

### QM-ORP-002 – Godkänd förmåga utan relevant sammanhang

**WARNING** om en `approved` Förmåga saknar alla relevanta relationer till mål, andra förmågor, IT-stöd eller plattformstjänster och det inte finns dokumenterat skäl.

### QM-ORP-003 – Godkänt IT-stöd utan förmågekoppling

**WARNING** om ett `approved` IT-stöd saknar relation som visar vilken Förmåga det stödjer och modellens scope omfattar förmåge-/IT-stödsspårbarhet.

### QM-ORP-004 – Godkänd plattformstjänst utan erbjudande-/realiseringskontext

**WARNING** om en `approved` Plattformstjänst varken har känd koppling till IT-förmåga/IT-stöd eller till realiserande Plattform.

### QM-ORP-005 – Godkänd plattform utan tjänstekontext

**WARNING** om en `approved` Plattform saknar relation till Plattformstjänst eller annan relevant användnings-/realiseringskontext inom modellens scope.

### QM-ORP-006 – Candidate utan relationer

**INFO** om ett `candidate` objekt är orphan. Detta kan vara legitimt under analys men bör synliggöras inför fortsatt arbete.

### QM-ORP-007 – Styrande objekt utan faktisk styrkoppling

**WARNING** om en `approved` Princip eller Standard saknar någon relation som visar vad den styr eller begränsar, när modellens scope omfattar sådan spårbarhet.

## 3. Strategisk spårbarhet

Kontrollerna ska endast appliceras när modellens scope faktiskt inkluderar motsvarande nivåer.

### QM-TRC-001 – Drivkrafter till mål

**WARNING** om betydande `approved` Drivkrafter inte påverkar något Mål och ingen annan motiverad struktur för deras effekt finns.

### QM-TRC-002 – Mål till förmågor

**WARNING** om ett `approved` Mål saknar spårbar väg till någon Förmåga när modellen används för att förklara vilka förmågor som behöver utvecklas för att nå målen.

En spårbar väg får bestå av flera semantiskt relevanta relationer. Enbart `related_to` ska inte räknas som stark spårbarhet.

### QM-TRC-003 – Förmåga till IT-stöd

**INFO** eller **WARNING** beroende på scope om en verksamhetsförmåga saknar känt IT-stöd. Detta är inte automatiskt en arkitekturlucka; förmågan kan vara manuell eller underlaget ofullständigt.

### QM-TRC-004 – IT-förmåga till plattformstjänst

**WARNING** om en `approved` IT-förmåga som enligt modellens scope ska tillhandahållas av ett stödjande IT-område saknar känd realisering/möjliggörande Plattformstjänst och ingen annan realiseringsform dokumenterats.

### QM-TRC-005 – IT-stöd till plattformstjänster

**INFO** om ett IT-stöd saknar kända använda Plattformstjänster. **WARNING** endast om modellens scope uttryckligen ska beskriva sådan plattformsanvändning och objektet är `approved`.

### QM-TRC-006 – Plattformstjänst till plattform

**WARNING** om en `approved` Plattformstjänst saknar känd realisering av Plattform när modellens scope omfattar teknisk realisering.

### QM-TRC-007 – Svaga spårbarhetskedjor

**WARNING** om en kritisk spårbarhetskedja huvudsakligen består av `related_to` trots att mer precisa relationer borde kunna fastställas från tillgängligt underlag.

## 4. Dubbletter, alias och överlapp

### QM-DUP-001 – Sannolik dubblett

**WARNING** om två objekt av samma eller närliggande typ har mycket liknande namn/alias och beskrivningar och förefaller representera samma sak.

### QM-DUP-002 – Semantiskt överlapp

**WARNING** om två objekt överlappar så starkt att deras scope inte går att skilja på ett meningsfullt sätt.

EA Stödjare ska föreslå möjliga åtgärder – exempelvis alias, sammanslagning, tydligare scope eller hierarkisk avgränsning – men inte automatiskt slå ihop objekten.

### QM-DUP-003 – Samma namn, olika semantik

**WARNING** om samma eller nästan samma namn används för olika objekttyper utan tydlig disambiguering.

Exempel: både en IT-förmåga och Plattformstjänst heter `Integration` utan tillräckligt särskiljande beskrivning.

### QM-DUP-004 – Dubbletter i funktioner

**INFO** eller **WARNING** om funktionslistor inom eller mellan närliggande IT-stöd/Plattformstjänster antyder oavsiktlig överlappning som bör analyseras.

Liknande funktioner på olika objekt är inte i sig fel.

## 5. Konsistens och motsägelser

### QM-CON-001 – Motstridig livscykel

**ERROR** om relationer behandlar ett `retired` objekt som aktuell obligatorisk realisering utan dokumenterad övergång eller historisk kontext.

**WARNING** vid `deprecated` objekt som fortfarande är centrala beroenden utan dokumenterad plan/kontext.

### QM-CON-002 – Motsägande klassificering

**WARNING** om relationer och beskrivningar systematiskt antyder en annan objekttyp än den lagrade typen, även om objektet individuellt inte redan fångats av objektkontrollen.

### QM-CON-003 – Motsägande proveniens

**WARNING** om olika evidensposter ger materiellt motstridiga påståenden och konflikten inte är markerad eller hanterad.

### QM-CON-004 – Approved byggt på olöst svag grund

**WARNING** eller **ERROR** beroende på betydelse om ett `approved` objekt eller en `approved` relation huvudsakligen bygger på osäkra `proposed`/svagt överförbara externa antaganden utan dokumenterad beslutspunkt.

### QM-CON-005 – Föräldralösa beroenden till borttagna objekt

**ERROR** om aktuell modell innehåller relationer till borttagna objekt. Historik ska hanteras via status/revisionshistorik, inte trasiga aktuella referenser.

## 6. Täckning och modellens scope

Täckning får bara bedömas mot dokumenterat scope. Avsaknad av en objekttyp i en avgränsad modell är inte ett fel i sig.

### QM-COV-001 – Scope saknas eller är oklart

**WARNING** om modellen granskas för täckning men projektets avgränsning inte är tillräckligt tydlig för att avgöra vad som förväntas ingå.

### QM-COV-002 – Uttalat scope saknar representerade kärnområden

**WARNING** om ett explicit scope säger att ett område ska omfattas men modellen saknar objekt eller relationer som rimligen krävs för att beskriva området.

### QM-COV-003 – Dokumentationslucka kontra arkitekturlucka

**INFO** när modellen indikerar en möjlig lucka men evidensen inte räcker för att avgöra om den är verklig. Rapporten ska uttryckligen ange `dokumentationslucka`, `möjlig arkitekturlucka` eller `bekräftad arkitekturlucka` – inte blanda begreppen.

### QM-COV-004 – Kritiska områden med låg evidenstäckning

**WARNING** om en central del av modellen har många `approved` påståenden men låg eller svag provenienstäckning.

### QM-COV-005 – Externa förslag dominerar intern modell

**WARNING** om ett område i hög grad består av organisationsspecifika `proposed` objekt som främst stöds av externa exempel och ännu saknar intern validering.

## 7. Struktur, täthet och beroendemönster

Dessa kontroller är heuristiska och får inte användas som absoluta arkitekturregler.

### QM-GRF-001 – Extremt tätt objekt

**INFO** eller **WARNING** om ett objekt har avsevärt fler relationer än liknande objekt och därmed kan vara för brett, fungera som ospecificerad hubb eller ha överanvänt `related_to`.

### QM-GRF-002 – Isolerad delgraf

**INFO** om modellen innehåller en sammanhängande delgraf som saknar relation till övrig modell. **WARNING** om delgrafen enligt scope borde vara integrerad med resten.

### QM-GRF-003 – Överanvändning av `related_to`

**WARNING** om `related_to` används i sådan omfattning att relationssemantiken blir otydlig och mer precisa relationer borde kunna användas.

### QM-GRF-004 – Beroendecykel som kräver granskning

**INFO** eller **WARNING** om `depends_on` bildar cykler. Till skillnad från `derived_from` är detta inte automatiskt fel, men kan indikera stark koppling eller svår förändringsbarhet.

### QM-GRF-005 – Flaskhals-/single-point-of-dependency-kandidat

**INFO** om ett IT-stöd, en Plattformstjänst eller Plattform är central beroendepunkt för många andra objekt. Rapporten ska beskriva detta som analyskandidat, inte som risk utan ytterligare underlag.

## 8. Principer och standarder som faktisk styrning

### QM-GOV-001 – Princip utan tillämpning

**WARNING** om en `approved` Princip inte styr någon relevant del av modellen och detta inte är medvetet dokumenterat.

### QM-GOV-002 – Standard utan tillämpning

**WARNING** om en `approved` Standard inte styr eller begränsar något relevant objekt inom aktuellt scope.

### QM-GOV-003 – Styrning utan motivering

**WARNING** om omfattande `governed_by`/`constrains`-relationer saknar proveniens eller motivering när de representerar organisationsspecifika krav.

### QM-GOV-004 – Överlappande eller motstridiga styrsignaler

**WARNING** om flera Principer/Standarder verkar ge motstridiga krav på samma objekt och konflikten inte är dokumenterad.

## 9. Proveniens på modellnivå

### QM-PRV-001 – Approved utan tillräcklig evidenstäckning

**WARNING** eller **ERROR** enligt objekt-/relationsregler om centrala godkända objekt eller relationer saknar adekvat proveniens.

### QM-PRV-002 – Externa källor utan överförbarhetsbedömning

**WARNING** när externa källor används för organisationsspecifika modellförslag men deras relevans/överförbarhet inte har bedömts där detta är materiellt.

### QM-PRV-003 – Förslag har blivit omarkerad intern sanning

**ERROR** om material som endast kan spåras till GPT-förslag eller externa jämförelseexempel har klassats som `explicit` intern evidens.

### QM-PRV-004 – Härledningskedja går inte att följa

**WARNING** om `derived` objekt eller relationer har `derived_from`-referenser som är så ofullständiga att härledningen inte går att förklara.

## 10. Sekundära objekttyper

Lösningsmönster och Referensarkitekturer är sekundära i v1 och ska inte krävas för att modellen ska vara komplett.

### QM-SEC-001 – Lösningsmönster utan relevanskoppling

**INFO** eller **WARNING** om ett `approved` Lösningsmönster saknar relation till det område som det ska vägleda inom modellens scope.

### QM-SEC-002 – Referensarkitektur utan relevanskoppling

**INFO** eller **WARNING** om en `approved` Referensarkitektur saknar relation till relevanta förmågor, plattformstjänster, standarder eller mönster när sådana samband ingår i scope.

# Täckningsprofiler

Helhetskontrollen bör använda en **täckningsprofil** för att undvika generiska krav som inte passar modellens syfte.

V1 definierar fyra logiska profiler:

## `catalog`

Fokus på katalogkvalitet, dubbletter, normalisering, proveniens och objektens interna kvalitet. Relationstäckning är huvudsakligen INFO om den inte uttryckligen ingår i scope.

## `strategy_to_capability`

Fokus på:

- Drivkraft → Mål,
- Mål → Förmåga,
- relevanta Principer.

IT-stöd och plattformslager behöver inte finnas.

## `capability_to_it`

Fokus på:

- Förmåga → IT-stöd,
- IT-förmåga → Plattformstjänst,
- IT-stöd → Plattformstjänst där relevant.

## `full_ea_v1`

Fokus på sammanhängande spårbarhet över alla primära v1-objekttyper som faktiskt ligger inom projektets scope.

En kontrollrapport ska alltid ange vald profil och eventuella scopeundantag.

# Heuristik för dubbletter och överlapp

EA Stödjare får använda följande signaler tillsammans:

- normaliserat namn,
- alias,
- beskrivningens semantiska likhet,
- samma capability_type eller objekttyp,
- liknande relationer,
- liknande funktioner,
- samma scope/ägare/domän,
- gemensam proveniens.

Ingen enskild signal räcker för automatisk sammanslagning.

# Granskningens arbetsordning

EA Stödjare ska normalt granska modellen i följande ordning:

1. välj scope och täckningsprofil,
2. verifiera referentiell integritet,
3. sammanställ objekt- och relationsstatistik,
4. hitta orphans och isolerade delgrafer,
5. analysera strategisk spårbarhet,
6. analysera dubbletter och överlapp,
7. analysera motsägelser och livscykel,
8. analysera styrning via Principer/Standarder,
9. analysera proveniens på modellnivå,
10. analysera grafmönster och beroenden heuristiskt,
11. skilj dokumentationsluckor från möjliga/verifierade arkitekturluckor,
12. prioritera åtgärder.

# Rapportformat

En helhetsrapport bör minst innehålla:

```text
Modell: <namn/revision>
Profil: <catalog | strategy_to_capability | capability_to_it | full_ea_v1>
Scope: <kort sammanfattning>
Resultat: GODKÄND | GODKÄND MED VARNINGAR | BLOCKERAD

Sammanfattning
- Objekt: N
- Relationer: N
- ERROR: N
- WARNING: N
- INFO: N

Blockerande fel
- [QM-...] ...

Viktigaste kvalitetsrisker
- [QM-...] ...

Spårbarhet
- ...

Möjliga dubbletter/överlapp
- ...

Luckor
- Dokumentationsluckor: ...
- Möjliga arkitekturluckor: ...
- Bekräftade arkitekturluckor: ...

Proveniens/evidens
- ...

Prioriterade åtgärder
1. ...
2. ...

Ej bedömbart
- ...
```

## Prioritering

Rapporten ska prioritera:

1. ERROR,
2. WARNING som påverkar centrala spårbarhetskedjor eller många objekt,
3. möjliga dubbletter/överlappar som påverkar modellens begriplighet,
4. evidensproblem,
5. INFO/strukturförbättringar.

EA Stödjare ska undvika att lämna en lång osorterad lista med alla tänkbara observationer.

# Automatiserbart kontra LLM-bedömt

## Lämpligt för deterministisk validering

- unika ID:n,
- brutna referenser,
- tillåtna relationstyper/source-target,
- identiska relationsdubbletter,
- `derived_from`-cykler,
- saknade source-ID:n,
- orphan-statistik,
- relationsgrad,
- isolerade delgrafer,
- `depends_on`-cykler,
- andel `related_to`.

## Kräver normalt semantisk LLM-bedömning

- verklig dubblett kontra legitimt närliggande objekt,
- för bred/smal modellering,
- motsägande betydelse,
- om ett mål rimligen borde ha en förmågekoppling,
- om extern praxis är överförbar,
- om en lucka är dokumentationslucka eller verklig arkitekturlucka,
- om principer/standarder faktiskt påverkar beslut,
- om grafens täthet tyder på fel abstraktionsnivå.

Deterministiska mätvärden får inte ensamma översättas till semantiska slutsatser.

# Definition of Done för helhetsgranskning

En helhetsgranskning är komplett när:

- scope och profil är explicit angivna,
- alla ERROR-kontroller som är möjliga att köra har körts,
- relevanta WARNING-kontroller har bedömts,
- orphans och dubblettkandidater har analyserats,
- relevanta spårbarhetskedjor har bedömts,
- proveniens har bedömts på modellnivå,
- luckor har klassificerats som dokumentationslucka/möjlig/bekräftad arkitekturlucka,
- ej bedömbara områden redovisas,
- prioriterade nästa åtgärder ges,
- ingen modelländring görs automatiskt enbart på grund av kvalitetsrapporten.
