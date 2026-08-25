<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Domain Model

Denna fil konsoliderar följande kanoniska källor:

- `docs/v2-design-principles.md`
- `docs/runtime-domain-contract-v2.md`
- `docs/information-layers.md`

---


# KÄLLA: `docs/v2-design-principles.md`

# EA Stödjare v2 – designprinciper

## 1. Syfte

Detta dokument fastställer de övergripande designprinciperna för nästa version av EA Stödjare. Steg 1 ändrar **inte** den kanoniska v1-metamodellen, relationsmodellen eller projektdataformatet. Dokumentet fungerar som styrande kontrakt för de efterföljande v2-stegen.

V2 är en evolution av v1, inte ett omtag från noll.

## 2. Grundprincip: standardmodell, inte universell modell

EA Stödjare ska tillhandahålla en liten, vältestad och begriplig standardmetamodell. Den ska vara en bra utgångspunkt för många EA-projekt, men får inte behandlas som den enda tillåtna modellen.

Varje projekt ska i v2 kunna beskriva sin **faktiskt använda metamodell** maskinläsbart. Det innebär att ett projekt ska kunna:

- använda standardmodellen utan ändringar,
- använda endast en delmängd av standardmodellens objekttyper,
- aktivera generella extensions,
- lägga till projektspecifika attribut,
- lägga till projektspecifika objekttyper och relationer när ett verkligt behov finns,
- dokumentera avvikelser från standardmodellen.

GPT:n ska alltid tolka projektet utifrån projektets deklarerade metamodell, inte utifrån antagandet att alla projekt använder samma struktur.

## 3. Minimum sufficient model

EA Stödjare ska fortsatt följa principen om **minsta tillräckliga modell**.

Nya objekttyper eller relationer ska inte införas bara för att de förekommer i ett ramverk eller skulle kunna vara användbara i något framtida fall. Ett koncept bör göras till global objekttyp först när det behöver egen identitet, egna relationer eller egen livscykel i det aktuella modelleringsbehovet.

Exempel:

- Funktion är fortsatt normalt embedded.
- Organisation ska inte bli kärnobjekt enbart för att `owner` eller `consumer_scope` förekommer.
- Actual Platform Offering ska inte införas som obligatorisk standardobjekttyp.

## 4. Standardmetamodellens kärna

V2 ska tills vidare utgå från följande standardobjekt:

- Drivkraft
- Mål
- Princip
- Förmåga
- IT-stöd
- Plattformstjänst
- Plattform
- Standard
- Lösningsmönster
- Referensarkitektur

Funktion är fortsatt normalt ett strukturerat underobjekt på relevanta objekt.

Produkt införs i senare v2-steg som en generell **stödjande objekttyp/extension** för marknads- och realiseringsanalys, inte som ersättning för IT-stöd eller Plattform.

## 5. Förmåga beskriver stabilt behov

Förmåga ska uttrycka vad organisationen eller IT behöver kunna åstadkomma eller möjliggöra, inte hur detta implementeras.

V2 ska införa tydligare boundary-stöd:

```yaml
in_scope:
out_of_scope:
consumer_scope:
```

För `capability_type: it` ska positiv boundary normalt presenteras som **Stödjer**. Den får inte bli en förtäckt lista över produkter, Plattformstjänster eller verksamhetsfunktionalitet som IT själv utför.

## 6. Plattformstjänst är realiseringsneutral

Plattformstjänst ska i v2 beskriva ett stabilt tekniskt erbjudande eller funktionalitetskontrakt som lösningar kan konsumera.

Den ska beskriva **vad** som ska kunna erbjudas, inte låsa **hur** eller **var** realiseringen sker.

En Plattformstjänst kan därför realiseras av exempelvis:

- produkt,
- produktfamilj,
- ramverk,
- bibliotek/SDK,
- SaaS,
- distribuerad runtime,
- central plattform,
- komposition av flera byggblock.

Begreppet får inte normativt innebära central shared runtime eller centralt driftad tjänsteinstans.

## 7. Plattform är konceptuell i standardmodellen

Användarsynligt namn behålls som **Plattform**, men v2-standardsemantiken ska vara konceptuell och produktneutral.

En Plattform ska beskriva en sammanhållen gruppering av Plattformstjänster med gemensam teknisk och/eller förvaltningsmässig logik.

Det innebär bland annat:

- Plattform ska inte automatiskt vara synonym med en produkt.
- En Plattform får realiseras kompositionellt.
- Samma produkt får bidra till flera Plattformar utan att dessa automatiskt ska slås ihop.
- En Plattform med endast en Plattformstjänst är inte automatiskt fel.

## 8. Actual Platform Offering är inte kärnobjekt

V2 ska **inte** göra `actual_platform_offering` till obligatorisk standardobjekttyp.

Skälen är:

- produktnärvaro är inte tillräcklig evidens för ett verkligt organisatoriskt plattformserbjudande,
- praktisk användning visade stark tendens till 1–1-koppling mellan faktisk plattform och produkt,
- behovet kan ofta uttryckas bättre genom Produkt + actual-state/projektspecifika attribut,
- projekt som verkligen behöver ett separat organisatoriskt erbjudandeobjekt ska kunna lägga till detta som extension.

## 9. Produkt är ett generellt realiserings- och marknadskoncept

Produkt ska i v2 kunna representera ett konkret marknadserbjudande, till exempel:

- applikationsprodukt,
- plattformsprodukt,
- infrastrukturprodukt,
- SaaS-tjänst,
- ramverk,
- bibliotek,
- utvecklingsverktyg,
- SDK,
- appliance.

Produkt ska kunna analyseras mot både:

```text
Produkt --can_realize--> IT-stöd
Produkt --can_realize--> Plattformstjänst
```

Det möjliggör exempelvis både produktanalys för `IT-stöd: Ordbehandling` och produktanalys för en teknisk Plattformstjänst.

Produkt ska aldrig automatiskt klassificeras som IT-stöd eller Plattform.

## 10. Funktion förblir normalt embedded

Funktion ska fortsatt kunna beskriva vad ett IT-stöd, en Plattformstjänst eller Plattform tillhandahåller.

V2 ska kunna ge embedded funktioner lokala ID:n när ett projekt behöver spåra exempelvis produktcoverage, men detta gör inte Funktion till global objekttyp.

Exempel:

```yaml
functions:
  - id: F01
    name: Samredigering
  - id: F02
    name: Spåra ändringar
```

Lokala funktions-ID:n är scoped till moderobjektet.

## 11. Liten relationskärna med kvalificerande metadata

V2 ska undvika en explosion av generiska relationstyper.

Kärnan ska i huvudsak bygga vidare på:

- `influences`
- `supports`
- `uses`
- `governed_by`
- `constrains`
- `depends_on`
- `derived_from`
- `related_to`

samt kompletteras med några semantiskt nödvändiga relationer, främst:

- `provided_by`
- `can_realize`

`provided_by` ska användas för konceptuell hemvist:

```text
Platform Service --provided_by--> Platform
```

`realized_by` får inte längre överlastas för denna betydelse.

Relationer ska i v2 kunna kvalificeras med valfria attribut, exempelvis:

```yaml
relation_role:
strength:
mandatory:
realization_role:
verification_status:
boundary_basis:
notes:
```

Tillåtna kvalificerare ska styras av relationsschemat.

## 12. Konceptuell arkitektur, marknad och faktisk organisation är olika lager

EA Stödjare ska uttryckligen hålla isär:

1. **konceptuell arkitektur** – vad organisationen behöver kunna erbjuda eller stödja,
2. **marknadsreferens** – vad produkter och tekniska byggblock kan realisera enligt evidens,
3. **faktiskt tillstånd** – vad organisationen faktiskt använder, äger eller erbjuder.

Följande påståenden får inte infereras från varandra utan evidens:

- en produkt kan realisera ett behov,
- produkten används i organisationen,
- organisationen erbjuder ett faktisk förvaltat tjänste-/plattformserbjudande byggt på produkten.

## 13. Candidate before canon

V1-principen `candidate before canon` behålls och stärks.

Normal utvecklingskedja:

```text
identifiera
  ↓
kandidat
  ↓
boundary/evidence/stress review
  ↓
approved
  ↓
baseline/freeze vid tillräcklig mognad
```

GPT:n får inte göra externa exempel, marknadskapacitet eller egna rekommendationer till organisationsspecifik sanning genom att bara skriva in dem i kanonisk modell.

## 14. Boundary-first modeling

När nya Förmågor, IT-stöd, Plattformstjänster eller Plattformar övervägs ska GPT:n prioritera boundary-frågor framför produktmatchning.

Typiska frågor:

- Vilket stabilt behov eller konsumentlöfte beskriver objektet?
- Vad ligger uttryckligen utanför?
- Är detta samma semantik som ett befintligt objekt?
- Har objektet egen livscykel, kompetens eller förvaltningslogik?
- Är en eventuell produktöverlappning verklig semantisk överlappning eller endast shared realization?

Produkter används för stresstest och realiseringsanalys, inte för att automatiskt definiera arkitekturens gränser.

## 15. Derived views är inte source of truth

V2 ska kunna beskriva reproducerbara härledda vyer som exempelvis:

- Förmåga → Plattformstjänst → Plattform,
- Plattform → Plattformstjänst → Förmåga,
- Produkt → IT-stöd,
- Produkt → Plattformstjänst → Plattform,
- härledda plattformsberoenden,
- shared realization,
- produktcoverage.

En derived view:

- ska kunna regenereras,
- ska deklarera att den inte är source of truth,
- får aldrig korrigera kanonisk data bakvägen.

## 16. Presentation är separat från metamodell

Kanoniska fältnamn och användarsynliga rubriker ska hållas isär.

Exempel:

```text
in_scope      → Stödjer
out_of_scope  → Omfattar inte
PLS linkage   → Understöds av
Platform→PLS  → Tillhandahåller
```

Standardpresentation för objekt bör vara:

```text
Namn (ID)
```

inte `ID Namn` när ID:t bara är spårbarhetsinformation.

## 17. Extension före kärnexpansion

När ett verkligt projekt behöver något utanför standardmodellen ska EA Stödjare först bedöma om behovet bör lösas som project extension.

V2 ska därför stödja projektspecifika:

- objekttyper,
- attribut,
- relationer,
- enum-värden,
- QA-regler,
- presentationssemantik,
- derived views.

En extension får inte tyst ändra betydelsen av befintliga kärnobjekt.

## 18. Change control omfattar även metamodellen

När projektets metamodell kan förändras måste v2 skilja mellan minst:

- `editorial`
- `evidence_update`
- `controlled_model_change`
- `breaking_model_change`
- `metamodel_change`

Ändring av projektets objekttyper, relationer eller semantik ska registreras som `metamodel_change` och vara spårbar.

## 19. Bakåtkompatibilitet är en release-egenskap

En ny EA Stödjare-version är inte godkänd enbart för att nya v2-projekt fungerar.

Releasekandidaten måste även kunna:

- öppna ett v1-projekt,
- förstå v1-semantiken,
- fortsätta arbeta med projektet utan obligatorisk migration,
- migrera kontrollerat när användaren vill,
- förstå ett utökat legacy-projekt som referensprojektet rev80,
- dokumentera den faktiska metamodellen i ett sådant projekt.

Se `docs/backward-compatibility-contract.md`.

## 20. Designregel för kommande steg

Om ett kommande v2-steg föreslår en lösning som strider mot dessa principer ska motsättningen dokumenteras uttryckligen innan ändringen implementeras.

Steg 1 ska därför betraktas som designbaslinjen för v2-arbetet.


# KÄLLA: `docs/runtime-domain-contract-v2.md`

# Runtimekontrakt – domänmodell v2

Detta dokument är den aktuella läsmodellen för EA Stödjare 2.x. Det ersätter historiska stegvisa utvecklingsnoter i Builder Knowledge; äldre designbeslut finns kvar i repositoryt som spårbar historik men ska inte tolkas som framtida arbete.

## Projektprofil före semantik

Fastställ alltid projektprofil innan objekt eller relationer tolkas: `native_v2`, `legacy_v1`, `extended_legacy` eller `unknown`. Native v2 använder `project-metamodel.yaml` + basprofil + aktiva extensions. Legacy-profiler använder sin frysta semantik. `unknown` får inte tyst behandlas som v2.

## Standardobjekt

V2:s standardmodell är avsiktligt liten: Drivkraft, Mål, Princip, Förmåga, IT-stöd, Plattformstjänst, Plattform, Standard och Produkt. Lösningsmönster och Referensarkitektur stöds som sekundära typer. Funktion är embedded på IT-stöd, Plattformstjänst och Plattform och kan ha lokalt ID, men är inte global objekttyp.

## Centrala v2-semantiker

- **Förmåga:** native v2 använder `in_scope`, `out_of_scope` och vid behov `consumer_scope`. Legacy `scope` får inte mekaniskt döpas om.
- **Plattformstjänst:** ett realiseringsneutralt tekniskt erbjudande/funktionalitetskontrakt; inte automatiskt central drift, produkt eller faktisk organisationsstatus.
- **Plattform:** konceptuell, produktneutral gruppering/hemvist för Plattformstjänster. Singleton kan vara legitim när boundary är självständig.
- **Produkt:** konkret marknadserbjudande som kan bidra till eller realisera IT-stöd eller Plattformstjänst. Produkt är inte automatiskt IT-stöd, Plattform, Plattformstjänst eller faktisk användning.

## Relationer

- `provided_by`: Plattformstjänst → Plattform och betyder konceptuell hemvist.
- `can_realize`: Produkt → IT-stöd eller Plattformstjänst och betyder verifierbar realiseringspotential, inte produktval eller actual use. `realization_role` krävs.
- `realized_by`: reserveras för konkret realiseringssemantik där sådan uttrycks.
- Legacy `realized_by` migreras endast när betydelsen är verifierad; tvetydiga fall bevaras för review.

Relationskvalificerare används endast där relationstypen tillåter dem. Projektets effektiva metamodell är auktoritativ för tillåtna typer, attribut, relationer och värdemängder.

## Extensions

Projekt kan välja bort standardtyper och lägga till egna objekttyper, attribut, relationer, enumvärden, QA och presentationssemantik. Återanvändbara extensions har namespace och får inte kollidera med kärnan. Extensions ska användas före utvidgning av standardkärnan när behovet är projektspecifikt.


# KÄLLA: `docs/information-layers.md`

# Informationslager i EA Stödjare v2

## Syfte

EA Stödjare skiljer från v2 steg 16 explicit mellan **konceptuell arkitektur**, **marknadsreferens** och **faktisk organisationsinformation**. Separationen är epistemisk: samma produktnamn kan förekomma i flera sammanhang, men påståendena betyder olika saker och får inte överföras mellan lagren utan evidens.

## 1. Conceptual – `model/`

`model/` är fortsatt source of truth för den konceptuella EA-modellen. Här finns exempelvis Förmåga, IT-stöd, Plattformstjänst, konceptuell Plattform och Produkt som stödjande marknads-/realiseringsobjekt.

Ett konceptuellt behov eller en `can_realize`-relation är aldrig i sig ett produktval eller bevis på faktisk användning.

## 2. Market reference – `market-reference/`

Detta lager innehåller verifierbara påståenden om marknaden: vad en produkt uppges kunna göra, produktegenskaper, livscykeluppgifter och leverantörserbjudanden. Lagret är inte kanoniskt för organisationens faktiska tillstånd.

**Regel:** market capability ≠ actual use.

## 3. Actual state – `actual-state/`

Detta lager innehåller organisationsspecifika påståenden om exempelvis vald, godkänd, använd eller avvecklad Produkt samt faktiska organisatoriska erbjudanden. En Produkt får refereras direkt. Det behövs därför inget obligatoriskt `actual_platform_offering`-objekt.

**Regel:** actual use ≠ organizational offering.

Ett verifierat actual-state-påstående måste ha organisationsspecifik explicit eller härledd evidens. Extern marknadsinformation ensam räcker inte.

## Assertions

Market reference använder `MKT-*` och actual state `ACT-*`. Assertions är separata från den konceptuella relationsmodellen; de beskriver kunskapsläge och verkligt tillstånd snarare än arkitekturell struktur.

Exempel faktisk produktanvändning:

```yaml
- id: ACT-001
  assertion_type: product_in_use
  subject: PRD-001
  statement: Produkten används i organisationen för det angivna sammanhanget.
  status: verified
  provenance:
    - evidence_type: explicit
      source_id: SRC-001
      reference: Förvaltningsregister
```

Exempel organisatoriskt erbjudande måste vara separat:

```yaml
- id: ACT-002
  assertion_type: organizational_offering
  subject: PLS-001
  statement: Plattformstjänsten erbjuds faktiskt till organisationens konsumenter.
  status: verified
  provenance:
    - evidence_type: explicit
      source_id: SRC-002
```

ACT-001 får inte användas som automatisk ersättning för ACT-002.

## Övergång mellan lager

Ingen automatisk "promotion" görs från marknad till actual state. En övergång kräver ett nytt påstående med ny organisationsspecifik evidens. På samma sätt innebär ett faktiskt produktval inte att den konceptuella modellen ska skrivas om till produktberoende semantik.
