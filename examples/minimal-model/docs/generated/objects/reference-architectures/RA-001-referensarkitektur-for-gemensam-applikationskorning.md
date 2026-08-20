# Referensarkitektur för gemensam applikationskörning

- **ID:** `RA-001`
- **Objekttyp:** `reference_architecture`
- **Status:** `candidate`

## Beskrivning

Vägledande referensarkitektur för hur IT-stöd kan använda gemensamma plattformstjänster för applikationskörning.

## Omfattning och tillämpbarhet

- **scope:** Gemensam applikationskörning
- **applicability:** IT-stöd som lämpar sig för containeriserad körning

## Byggblock

- IT-stöd
- Containerplattformstjänst
- Containerplattform

## Vägledning

- Konsumera tjänsten framför att koppla direkt mot plattformens interna implementation.

## Relationer

### Realiseras av (`realized_by`)
- [Standardiserad applikationskörning](../solution-patterns/PAT-001-standardiserad-applikationskorning.md) (`PAT-001`)

### Relaterar till (`related_to`)
- [Driftsätta och köra applikationer](../capabilities/CAP-002-driftsatta-och-kora-applikationer.md) (`CAP-002`)

## Proveniens
- **proposed** — confidence: medium
  - Motiv: Referensarkitekturen sammanför exempelmodellens återanvändbara styrning och realisering.
  - Härledd från: PAT-001, PRN-001
