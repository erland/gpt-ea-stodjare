# Gemensamma behov realiseras som återanvändbara tjänster

- **ID:** `PRN-001`
- **Objekttyp:** `principle`
- **Status:** `candidate`

## Beskrivning

Återkommande tekniska behov bör erbjudas gemensamt när det ger tydlig nytta och minskar duplicering.

## Principformulering

Gemensamma tekniska behov ska i första hand mötas genom återanvändbara plattformstjänster.

## Motiv

Minskar dubbelarbete och ger en enhetlig konsumtionsmodell.

## Implikationer

- Plattformstjänster behöver tydliga erbjudanden och ansvar.
- Operativa IT-stöd bör återanvända gemensamma tjänster där de passar.

## Relationer

### Ligger till grund för (`derived_from`)
- [Standardiserad applikationskörning](../solution-patterns/PAT-001-standardiserad-applikationskorning.md) (`PAT-001`)

### Påverkas av (`influences`)
- [Snabbare och mer självständig utveckling](../goals/GOAL-001-snabbare-och-mer-sjalvstandig-utveckling.md) (`GOAL-001`)

### Styr (`governed_by`)
- [Containerplattformstjänst](../platform-services/PLS-001-containerplattformstjanst.md) (`PLS-001`)

## Proveniens
- **proposed** — confidence: medium
  - Motiv: Föreslagen styrning för att stödja målet om snabbare utveckling.
  - Härledd från: GOAL-001
- **external** — källa: Extern referens för standardiserade plattformstjänster (`SRC-EXT-001`); referens: Exempel på standardiserade interna plattformserbjudanden; confidence: medium; överförbarhet: medium
