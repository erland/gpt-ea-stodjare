# Stresstestrapport – EA Stödjare steg 26

## Sammanfattning

EA Stödjare v1 har designstresstestats mot tio realistiska, syntetiska EA-scenarier. Testet avser **koncept, metamodel, klassificeringsregler, evidensdisciplin, research- och modelleringsflöden**. Det är inte ett runtime-resultat från en publicerad Custom GPT; scenarierna ska därför återanvändas i slutlig end-to-end-verifiering.

Resultat: **10/10 scenarier bedöms stödjas efter en mindre metamodelkomplettering.** Ingen ny kärnobjekttyp behövde införas och v1-scope mot detaljerad lösningsarkitektur kunde behållas.

## Scenarioresultat

| # | Scenario | Resultat | Huvudobservation |
|---:|---|---|---|
| 1 | Strategi → drivkrafter/mål | PASS | Evidensmodellen förhindrar att härledda principer blir explicit fakta. |
| 2 | Ostrukturerat IT-underlag → förmågor | PASS | Klassificeringsguiden räcker för process/roll/produkt kontra förmåga. |
| 3 | Stödjande IT-område → IT-förmågor | PASS efter korrigering | Förmågor behöver lättviktig konsumentkontext utan Organisation som objekt. |
| 4 | Inventering av IT-stöd | PASS | Kandidat före kanon och produktavgränsning är tillräckliga. |
| 5 | Plattform kontra Plattformstjänst | PASS | Erbjudande kontra realiseringsgrund är en robust huvudregel. |
| 6 | Standarder och principer | PASS | Beslutad konkret norm skiljs från generell styrande riktning. |
| 7 | Fragmenterat/motsägelsefullt underlag | PASS | Konfliktmodellen hindrar tyst källval. |
| 8 | Researchbaserat modellförslag | PASS | Research + transferability + `proposed` ger rätt evidensdisciplin. |
| 9 | Dubbletter och fel nivåer | PASS | Normalisering kan föreslås utan aggressiv automatisk omskrivning. |
| 10 | Otillräckligt underlag | PASS | Confidence, kandidatfas och scopekontroll stödjer återhållsamhet. |

## Korrigering 1 – konsumentkontext för IT-förmåga

### Problem

Scenario 3 visade att `owner` svarar på **vem som ansvarar för förmågan**, men inte på **vilka organisatoriska målgrupper eller utvecklingsområden som förmågan ska betjäna**. Att införa Organisation som ny kärnobjekttyp vore för stort för v1.

### Beslut

Förmåga får det valfria attributet `consumer_scope`. Det är framför allt relevant för `capability_type: it` och används för lättviktig kontext, exempelvis:

```yaml
id: CAP-042
type: capability
name: Driftsätta applikationer
capability_type: it
owner: Stödjande utvecklingsområde
consumer_scope:
  - Operativa utvecklingsområden
  - Produktteam
```

`consumer_scope` skapar **inte** egna organisationsobjekt eller relationer. Om explicit organisationsmodellering senare behövs ska det behandlas som en framtida metamodelutökning.

## Bekräftade designbeslut

Stresstestet ger stöd för att behålla följande v1-beslut:

1. **Funktion förblir underordnat attribut**, inte egen nod mellan Förmåga och IT-stöd.
2. **Organisation förblir utanför kärnmodellen**; `owner` och `consumer_scope` räcker för nuvarande use case.
3. **Lösningsmönster och Referensarkitektur kan förbli sekundära**; inget scenario kräver separata specialarbetsflöden före v1.
4. **Constraint behöver inte bli egen objekttyp i v1**. Regulatoriskt tryck kan modelleras som Drivkraft, konkret norm som Standard och övrig kontext bevaras som evidens/anteckning när den inte passar kärnmodellen.
5. **Produkt/teknik behöver inte bli egen kärnobjekttyp**. Inventeringar kan behålla teknik som attribut på Plattform eller analyskontext.
6. **Ingen grafisk visualisering krävs för v1**. Relationerna är tillräckligt strukturerade för framtida visualisering.
7. **Detaljerad lösningsarkitektur ska fortsatt ligga utanför scope**. Inget stresstest kräver att gränsen flyttas.

## Risker som ska bevakas i runtime-test

- LLM:n kan fortfarande överklassificera teknikord som Standard eller Plattform.
- LLM:n kan ge researchförslag större säkerhet än källornas överförbarhet medger.
- Modellförslag kan bli för detaljerade om “minsta tillräckliga modell” inte följs.
- Dubblettanalys måste vara konservativ när två liknande namn faktiskt representerar olika scope.
- `consumer_scope` är avsiktligt lättviktigt; om användarna börjar behöva relationer till organisatoriska enheter är det signal för framtida modellutökning.

## Bedömning inför steg 27

Ingen blockerande metamodelbrist återstår efter korrigeringen. Projektet kan gå vidare till GitHub Actions, release och reproducerbar paketering. De tio scenarierna bör köras igen mot den faktiska Custom GPT-konfigurationen i steg 28 tillsammans med eval-sviten.
