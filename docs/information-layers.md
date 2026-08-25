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
