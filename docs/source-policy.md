# EA Stödjare – källpolicy v1

## 1. Syfte

Källpolicyn definierar hur EA Stödjare ska välja, värdera, använda och redovisa externa och interna källor. Den kompletterar proveniensmodellen och researcharbetsflödet.

Målet är att varje materiellt påstående som påverkar en EA-analys eller modell ska kunna förstås utifrån:

- var informationen kommer ifrån,
- hur auktoritativ och aktuell källan är,
- hur relevant den är för den aktuella frågan,
- hur väl den kan överföras till organisationens kontext,
- om resultatet är fakta, härledning eller rekommendation.

## 2. Grundregler

1. Prioritera primärkällor när sådana finns.
2. Prioritera auktoritativa källor framför popularitet och sökrankning.
3. Kontrollera aktualitet när ämnet kan ha förändrats.
4. Använd flera oberoende källor när slutsatsen är viktig och ingen ensam normativ källa finns.
5. Registrera relevanta externa källor i projektets källregister när de påverkar modellen.
6. Skilj alltid extern information från organisationens egna beslut och beskrivningar.
7. Markera leverantörsperspektiv och andra möjliga intressekonflikter.
8. Bedöm överförbarhet innan externa modeller används som grund för organisationsspecifika förslag.
9. Citera eller referera till den faktiska källa som stöder påståendet, inte bara en sida som nämner den.
10. Om källunderlaget inte räcker ska osäkerheten redovisas i stället för döljas.

## 3. Källkategorier

Källregistret använder typerna från proveniensmodellen:

- `internal_document`
- `internal_model`
- `internal_decision`
- `law_or_regulation`
- `standard`
- `framework`
- `authority_guidance`
- `industry_guidance`
- `peer_organization`
- `vendor_documentation`
- `research_or_report`
- `web_source`
- `user_statement`
- `other`

## 4. Prioriteringsordning för extern research

Som huvudregel:

| Prioritet | Källtyp | Typisk användning |
|---|---|---|
| 1 | Lag/reglering | Bindande krav och ramar |
| 2 | Formell standard | Definitioner, krav och etablerade specifikationer |
| 3 | Officiellt ramverk | Metodik, referensmodell och begrepp |
| 4 | Myndighets-/auktoritativ vägledning | Tillämpning och offentlig kontext |
| 5 | Peer-organisation | Jämförelse och praktiska exempel |
| 6 | Oberoende forskning/rapport | Syntes, evidens och trendanalys |
| 7 | Branschvägledning | Vanliga arbetssätt och mönster |
| 8 | Leverantörsdokumentation | Produktspecifika fakta och möjligheter |
| 9 | Övrig webbkälla | Kompletterande kontext eller ledtråd till starkare källa |

Prioriteten är vägledande. En källa måste fortfarande vara relevant för den konkreta frågan.

## 5. Intern källa kontra extern källa

Intern källa används för att beskriva organisationens faktiska:

- mål,
- beslut,
- befintliga modeller,
- ansvar,
- terminologi,
- arkitektur.

Extern källa används för att:

- jämföra,
- komplettera,
- utmana,
- ge definitioner,
- identifiera alternativ,
- föreslå modellstruktur.

En extern källa får inte användas för att påstå att organisationen har fattat ett beslut som endast återfinns externt.

## 6. Primärkällor

Primärkällor ska föredras för materiella fakta.

Exempel:

- officiell standard framför blogginlägg om standarden,
- officiell organisationssida framför tredjepartsbeskrivning av organisationens modell,
- publicerat styrdokument framför pressreferat,
- produktens officiella dokumentation framför forumdiskussion för produktspecifikation.

## 7. Peer-organisationer

Peer-källor ska väljas utifrån faktisk jämförbarhet, inte endast namnlikhet.

Bedöm minst:

- uppdrag,
- regulatorisk miljö,
- storlek,
- organisationsmodell,
- IT-leveransmodell,
- centralisering/decentralisering,
- teknisk och organisatorisk komplexitet.

Peer-material ska normalt behandlas som `external` med bedömd `transferability`.

## 8. Standarder och ramverk

EA Stödjare ska skilja mellan:

- krav som faktiskt följer av en normativ standard,
- rekommenderad metodik i ett ramverk,
- tolkning eller praxis kring standarden.

Ramverk ska inte behandlas som lag eller absolut sanning. Om flera ramverk är relevanta kan de användas parallellt och deras skillnader redovisas.

## 9. Leverantörskällor

Leverantörsdokumentation är normalt stark för produktspecifika fakta men svagare som oberoende grund för generella arkitekturrekommendationer.

EA Stödjare ska därför:

- ange att källan är leverantörsdriven,
- söka oberoende stöd när rekommendationen blir generell,
- undvika att modellera organisationens EA efter en specifik produkt utan uttryckligt motiv.

## 10. Aktualitet och version

För tidskänslig information ska källans:

- publiceringsdatum,
- version,
- status (gällande/ersatt/utkast),
- åtkomstdatum

kontrolleras när det är möjligt.

Äldre material kan fortfarande vara relevant historiskt, men ska inte presenteras som aktuellt utan kontroll.

## 11. Oberoende stöd och triangulering

När ingen normativ eller tydligt auktoritativ källa ensam räcker bör en viktig slutsats söka stöd i flera oberoende källor.

Bra triangulering kan exempelvis kombinera:

- ett etablerat ramverk,
- två relevanta peer-organisationer,
- en oberoende rapport.

Tre webbplatser som återpublicerar samma ursprungskälla räknas inte som tre oberoende belägg.

## 12. Källor som inte bör bära viktiga slutsatser ensamma

Exempel:

- anonymt forum,
- odaterat blogginlägg,
- SEO-/aggregatorsida,
- marknadsföringsmaterial,
- AI-genererad text utan verifierbara källor,
- sammanfattning som saknar länk till primärmaterial.

Sådana källor kan ge sökspår men bör normalt inte vara slutlig evidens för en viktig EA-rekommendation.

## 13. Källregistrering i projektet

När en extern källa faktiskt påverkar modell eller dokumentation ska den registreras i `model/sources.yaml`.

Exempel:

```yaml
- id: SRC-EXT-001
  title: Example Architecture Framework
  source_type: framework
  organization: Example Foundation
  url: https://example.org/framework
  version: "2.0"
  publication_date: 2026-05-01
  accessed_at: 2026-08-20
```

Objektet eller relationen refererar sedan källan via sin proveniens.

## 14. Citat och referenser

EA Stödjare ska i första hand sammanfatta källor med egen formulering och ange referens. Direkta citat ska användas sparsamt och endast när ordalydelsen är relevant.

Referensen bör vara så precis som rimligt:

- avsnitt,
- rubrik,
- sida,
- kapitel,
- specifik webbsida.

## 15. Källkonflikt

När starka källor motsäger varandra ska EA Stödjare:

1. inte välja vinnare utan analys,
2. redovisa konflikten,
3. bedöma aktualitet, auktoritet och kontext,
4. ange vilken tolkning som förefaller starkast och varför,
5. lämna frågan öppen om evidensen inte räcker.

Full konflikthantering utvecklas vidare i steg 20.

## 16. Extern research och rekommendationer

En organisationsspecifik rekommendation ska normalt ha `evidence_type: proposed`, även om den stöds av externa källor.

Extern evidens kan bifogas som ytterligare proveniensposter.

Detta är en central regel för att undvika:

```text
"Andra gör så" → "Därför är detta organisationens modell"
```

Rätt kedja är:

```text
extern evidens
+ intern kontext
+ bedömd överförbarhet
+ EA-analys
= markerat organisationsspecifikt förslag
```

## 17. Definition of Done för källhantering

Källhanteringen är tillräcklig när:

- den starkaste rimligt tillgängliga källtypen har prioriterats,
- aktualiteten har kontrollerats där det spelar roll,
- peer-/leverantörsbias är synlig,
- extern och intern information hålls isär,
- överförbarhet är bedömd när extern praxis används för modellförslag,
- viktiga källor går att återfinna,
- materiella rekommendationer är markerade som rekommendationer.
