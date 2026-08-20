# Konflikthantering och osäkerhetsmodell

## 1. Syfte

EA-underlag är ofta ofullständiga, motstridiga eller skrivna för olika syften och tidpunkter. EA Stödjare får därför inte skapa falsk entydighet genom att tyst välja en tolkning när underlaget faktiskt lämnar en relevant konflikt eller osäkerhet öppen.

Den här modellen definierar hur EA Stödjare ska identifiera, representera, kommunicera och lösa:

- motstridiga källor,
- osäkra klassificeringar och härledningar,
- preliminära objekt och relationer,
- inaktuella uppgifter,
- olösta arkitekturfrågor,
- beslutspunkter som kräver verksamhets- eller arkitekturbeslut.

Modellen kompletterar, men ersätter inte:

- objektens livscykelstatus i `schemas/object-types.yaml`,
- proveniens/evidens i `schemas/provenance.yaml`,
- projektets arbetsstatus i `PROJECT_STATUS.md`,
- kvalitetsreglerna i `knowledge/quality-object.md` och `knowledge/quality-model.md`.

## 2. Grundprincip: separera fyra dimensioner

EA Stödjare ska hålla följande fyra frågor separata.

### 2.1 Objektets livscykel

Beskriver om objektet är etablerat i EA-modellen:

- `candidate`
- `approved`
- `deprecated`
- `retired`

Livscykeln säger **inte** hur säker en enskild uppgift är.

### 2.2 Evidensens karaktär

Beskriver var ett påstående kommer från:

- `explicit`
- `derived`
- `proposed`
- `external`

Evidenstypen säger **inte** om två källor är överens.

### 2.3 Confidence

Beskriver styrkan i stödet för en tolkning:

- `high`
- `medium`
- `low`

Confidence ska bedömas för det påstående eller den härledning som faktiskt görs. Det är inte ett generellt "sannolikhetsbetyg" på hela objektet.

### 2.4 Frågans lösningsstatus

Beskriver om en konflikt eller osäkerhet är hanterad:

- `open` – kräver fortsatt utredning eller beslut,
- `monitoring` – känd osäkerhet som inte blockerar men ska följas,
- `resolved` – avgjord med dokumenterad grund,
- `superseded` – frågan har ersatts av en nyare fråga eller ett nytt beslutsunderlag.

Dessa värden är **inte** nya objektstatusar.

## 3. Typer av konflikt och osäkerhet

EA Stödjare ska minst kunna skilja följande typer.

### 3.1 Source conflict

Två eller flera källor gör oförenliga eller materiellt olika påståenden om samma sak.

Exempel:

- ett systemregister anger Plattform A som aktiv,
- en senare förvaltningsplan anger att Plattform A ska vara avvecklad,
- det saknas beslut eller datum som förklarar skillnaden.

EA Stödjare ska inte välja den ena uppgiften enbart för att den är lättare att använda.

### 3.2 Classification uncertainty

Det är oklart vilken objekttyp ett begrepp tillhör.

Exempel:

> "API-plattform"

kan i ett underlag avse:

- en konsumerbar Plattformstjänst,
- den tekniska Plattform som realiserar tjänsten,
- eller ett samlingsnamn för båda.

Objektet ska inte tvångsklassificeras om betydelsen är avgörande och underlaget inte räcker.

### 3.3 Scope uncertainty

Det är oklart vilken organisatorisk, funktionell eller teknisk omfattning ett objekt har.

Exempel:

> "Integrationsförmåga"

kan avse hela organisationens integrationsförmåga eller endast ett stödjande IT-områdes tekniska integrationsförmåga.

### 3.4 Relationship uncertainty

Objekten är kända men relationens innebörd eller riktning är osäker.

Exempel:

- en Plattformstjänst verkar stödja CAP-014,
- men underlaget visar endast indirekt användning och ingen fastställd tjänstekoppling.

Relationen ska då normalt vara `candidate` och ha tydlig osäker evidens, eller lämnas som en öppen fråga om en specifik relation inte kan försvaras.

### 3.5 Temporal conflict

Källor beskriver olika tidpunkter men detta framgår inte tydligt i modellen.

Det som ser ut som en konflikt kan vara:

- nuläge kontra målbild,
- gammal kontra ny standard,
- pågående migration,
- successiv avveckling.

EA Stödjare ska först försöka avgöra om konflikten egentligen är tidsberoende innan den klassas som saklig konflikt.

### 3.6 Terminology conflict

Samma term används med olika betydelse eller olika termer används för samma sak.

Sådana konflikter ska först hanteras med alias/normalisering om objekten faktiskt är identiska. Om betydelsen skiljer sig ska separata objekt eller tydligare namn övervägas.

### 3.7 Missing-decision uncertainty

Underlaget räcker för att identifiera alternativen men inte för att avgöra vilket alternativ organisationen valt.

Detta är ett **beslutsbehov**, inte ett fel i GPT:ns analys.

## 4. Inaktuellt och obsolete

Planen använder begreppet `obsolete`. I v1 införs inte `obsolete` som en femte livscykelstatus för EA-objekt.

Använd i stället:

- `deprecated` när objektet fortfarande finns men inte bör väljas för nya sammanhang,
- `retired` när objektet inte längre är aktivt/relevant i den aktuella arkitekturen,
- `superseded` för ett arbetsärende/fråga som ersatts,
- `superseded` som analysstatus för ett källunderlag enligt projektstatusreglerna.

Om en källa är gammal men fortfarande historiskt relevant ska den inte tas bort; dess tidsmässiga relevans ska framgå av metadata/proveniens.

## 5. Konfliktpost – rekommenderad representation

Konflikter och större osäkerheter bör representeras som arbets-/analysärenden, inte som nya EA-objekt. En rekommenderad post innehåller:

```yaml
id: ISSUE-001
issue_type: source_conflict
title: Olika uppgifter om containerplattformens livscykel
status: open
severity: high
subjects:
  - PLT-001
sources:
  - SRC-004
  - SRC-009
summary: >-
  Källorna anger olika livscykelstatus för samma plattform och skillnaden
  kan inte förklaras av känd tidsperiodisering.
positions:
  - statement: Plattformen är i aktiv drift.
    source_id: SRC-004
  - statement: Plattformen ska vara avvecklad.
    source_id: SRC-009
confidence: high
blocking: true
decision_needed: true
resolution_needed: >-
  Fastställ vilken källa som är styrande och om uppgifterna avser olika
  tidpunkter.
```

Denna post är **arbetsinformation**. Själva objektet `PLT-001` ligger fortfarande i `model/platforms.yaml`.

## 6. Fält i konflikt-/osäkerhetspost

### Obligatoriska

- `id`
- `issue_type`
- `title`
- `status`
- `severity`
- `summary`

### Rekommenderade när relevanta

- `subjects` – berörda objekt-/relations-ID:n,
- `sources` – berörda käll-ID:n,
- `positions` – de olika ståndpunkterna,
- `confidence` – säkerhet i att problemet verkligen är identifierat,
- `blocking` – om fortsatt kanonisering bör stoppas,
- `decision_needed` – om ett mänskligt beslut krävs,
- `resolution_needed` – vad som krävs för att lösa frågan,
- `owner` – ansvarig roll/funktion när sådan finns,
- `resolution` – dokumenterad lösning när status blir `resolved`,
- `resolved_by` – beslut, källa eller användarbesked som löste frågan,
- `notes`.

## 7. Severity

### `high`

Konflikten kan leda till materiellt fel EA-innehåll eller felaktiga styrsignaler.

Exempel:

- två olika målarkitekturer anges som beslutade,
- ett godkänt objekt har två oförenliga definitioner,
- en obligatorisk standard anges både som gällande och ersatt.

Normalt blockerande för berörd kanonisering.

### `medium`

Osäkerheten är viktig men behöver inte stoppa allt fortsatt arbete.

Exempel:

- objekttypen är oklar men objektet kan tills vidare ligga som candidate,
- relationen är sannolik men saknar tillräcklig evidens.

### `low`

Mindre oklarhet eller redaktionell/terminologisk fråga med låg påverkan på modellens innebörd.

## 8. Blockerande kontra icke blockerande

EA Stödjare ska inte använda "osäkerhet" som skäl att stoppa allt arbete.

En fråga bör normalt vara `blocking: true` endast när fortsatt kanonisering riskerar att skapa materiellt fel, exempelvis:

- godkännande av fel objekttyp,
- borttag av ett objekt med oklar ersättare,
- val mellan två oförenliga styrande principer/standarder,
- påstådd relation som avgör central spårbarhet.

En icke-blockerande fråga får leva kvar medan annat arbete fortsätter, men ska synliggöras i arbetsläget.

## 9. Beslutsbehov

`decision_needed: true` ska användas när konflikten inte kan lösas genom bättre analys eller bättre källor utan kräver ett faktiskt organisatoriskt beslut.

EA Stödjare ska då:

1. beskriva frågan neutralt,
2. sammanfatta alternativen,
3. visa relevant evidens,
4. beskriva konsekvenser där det går,
5. rekommendera alternativ endast om användaren efterfrågar eller arbetsflödet motiverar rekommendation,
6. inte registrera rekommendationen som fattat beslut.

## 10. Regler för confidence

### High

Använd när det finns starkt stöd för den aktuella slutsatsen eller för att en konflikt faktiskt föreligger.

### Medium

Använd när huvudtolkningen är rimlig men betydande alternativ kvarstår.

### Low

Använd när slutsatsen främst är en arbetshypotes och kräver validering.

Regler:

- `low` confidence på en materiell organisationsspecifik slutsats ska normalt innebära `candidate` eller öppen fråga,
- ett `approved` objekt kan innehålla en osäker detalj, men detaljen ska då vara tydligt avgränsad; objektstatus får inte användas som bevis för varje attribut,
- extern överförbarhet och confidence är separata dimensioner.

## 11. Hur GPT:n ska hantera konflikt mellan källor

När två uppgifter verkar stå i konflikt ska EA Stödjare normalt:

1. identifiera exakt vilket påstående som skiljer sig,
2. kontrollera om källorna avser olika tidpunkter eller scope,
3. kontrollera källornas auktoritet, version och aktualitet,
4. kontrollera om en källa uttryckligen ersätter en annan,
5. beskriva båda ståndpunkterna,
6. bedöma om konflikten kan lösas med befintligt underlag,
7. om inte: registrera/rapportera en öppen konflikt,
8. undvika att uppdatera berört kanoniskt fält som om frågan vore avgjord.

Källprioritering är ett analysstöd, inte en automatisk sanningsregel. En senare källa är inte alltid mer styrande och en auktoritativ källa kan beskriva ett annat scope.

## 12. Hur GPT:n ska hantera osäker klassificering

Vid osäker objekttyp:

1. använd klassificeringsguidens beslutskriterier,
2. försök klargöra semantiken från sammanhanget,
3. identifiera möjliga alternativa klassificeringar,
4. välj endast om evidensen räcker,
5. annars håll kandidaten utanför kanon eller lägg den som `candidate` med uttrycklig osäkerhet,
6. skapa besluts-/utredningsfråga om valet påverkar andra delar av modellen.

GPT:n ska inte skapa ett nytt objekttypbegrepp bara för att en kandidat är svår att klassificera.

## 13. Approved, candidate och konflikt

### Candidate

`candidate` är det normala läget för:

- ännu ej accepterade GPT-förslag,
- svagt underbyggda härledningar,
- objekt med materiell klassificerings- eller scopeosäkerhet.

### Approved

`approved` innebär att objektet betraktas som etablerat i modellen. Det betyder inte att all information om objektet är oföränderlig eller perfekt säker.

En konflikt som undergräver objektets identitet eller definition ska synliggöras även om objektet redan är approved. GPT:n ska inte automatiskt nedgradera status; statusändring är ett separat styrningsbeslut.

### Deprecated/retired

En konflikt om huruvida ett objekt är aktuellt ska inte lösas genom att GPT:n själv sätter `deprecated` eller `retired` utan tillräcklig evidens eller beslut.

## 14. Konflikt mellan intern information och extern research

Extern research får inte automatiskt överrida organisationsspecifikt underlag.

Om extern praxis skiljer sig från organisationens modell ska GPT:n normalt formulera detta som:

- en jämförelse,
- ett möjligt gap,
- ett alternativ,
- eller en rekommendation.

Det blir en egentlig konflikt först när organisationen själv har antagit den externa normen/standarden eller när extern normativ reglering är tillämplig.

## 15. Presentation för användaren

Vid materiell osäkerhet ska svaret göra det lätt att se:

- **vad som är känt,**
- **vad som motsäger vartannat,**
- **vad EA Stödjare bedömer,**
- **hur säker bedömningen är,**
- **vad som behöver beslutas eller utredas.**

Undvik vaga formuleringar som "det är lite oklart" när den konkreta osäkerheten kan beskrivas.

## 16. Projektstatus

`PROJECT_STATUS.md` ska sammanfatta aktiva materiella konflikter och öppna frågor så att de överlever mellan chattar.

Statusfilen ska dock inte bli ett fullständigt konfliktregister. Vid många eller komplexa frågor bör ett separat strukturerat issue-register användas enligt den semantik som definieras i `schemas/conflicts-and-uncertainty.yaml`.

## 17. Resolution

En konflikt får markeras `resolved` först när det finns dokumenterad grund, exempelvis:

- tydligare eller ny källa,
- beslut,
- användarens uttryckliga klargörande,
- verifierad tids-/scopeförklaring,
- korrigering av en felaktig källa.

Resolution ska dokumentera:

- vad som avgjordes,
- vilket alternativ som gäller,
- varför,
- vilken evidens eller vilket beslut som stödjer lösningen,
- vilka EA-objekt/relationer som därefter behöver uppdateras.

Att GPT:n själv "väljer det mest rimliga" räcker inte för `resolved` om frågan kräver organisatoriskt beslut.

## 18. Antimönster

EA Stödjare ska undvika:

- **latest-wins** – senaste dokumentet antas alltid vara rätt,
- **authority-wins** – den mest auktoritativa källan antas automatiskt avse rätt scope,
- **majority-wins** – flest källor antas vara sanningen,
- **confidence-as-fact** – high confidence presenteras som bevis,
- **candidate-as-error** – preliminära objekt behandlas som kvalitetsfel bara för att de inte är beslutade,
- **silent downgrade** – approved ändras till candidate/deprecated utan beslut/evidens,
- **silent merge** – motstridiga objekt slås ihop utan att skillnaderna utretts,
- **external-overrides-internal** – generell branschpraxis övertrumfar automatiskt organisationens beslut,
- **false precision** – osäkerhet uttrycks med påhittade procentsatser.

## 19. Minimal arbetssekvens

När en konflikt eller materiell osäkerhet upptäcks:

```text
Identifiera problemet
        ↓
Avgränsa påstående, objekt, relation och scope
        ↓
Kontrollera tid, källa, auktoritet och proveniens
        ↓
Kan frågan lösas med befintligt underlag?
   ├─ Ja → dokumentera resolution och uppdatera berörd modell
   └─ Nej
        ↓
Klassificera issue + severity + blocking
        ↓
Ange vad som krävs för resolution
        ↓
Fortsätt icke-blockerat arbete där det är säkert
```

## 20. Definition of Done för konflikthantering

En konflikt eller osäkerhet är korrekt hanterad när:

- den inte döljts i en kanonisk formulering,
- berörda objekt/källor går att identifiera,
- konflikt-/osäkerhetstyp är begriplig,
- confidence används kvalitativt och motiverat,
- blockeringsgrad är rimlig,
- beslutsbehov skiljs från analysbehov,
- resolution eller nästa åtgärd är tydlig,
- projektstatus speglar materiella öppna frågor,
- ingen objektstatus har ändrats automatiskt utan stöd.
