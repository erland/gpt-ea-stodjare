# Referensarkitektur för gemensam applikationskörning (RA-001)

> Genererad från kanonisk YAML · läge `working` · projektrevision `5` · presentationskontrakt `ea-reader-oriented-sv`

- **ID:** `RA-001`
- **Objekttyp:** `reference_architecture`
- **Status:** `candidate`

## Beskrivning

Vägledande referensarkitektur för hur IT-stöd kan använda gemensamma plattformstjänster för applikationskörning.

## Egenskaper

- **Scope:** Gemensam applikationskörning
- **Tillämplighet:** IT-stöd som lämpar sig för containeriserad körning
- **Byggblock:** IT-stöd, Containerplattformstjänst, Containerplattform
- **Vägledning:** Konsumera tjänsten framför att koppla direkt mot plattformens interna implementation.

## Relationer

### Realiseras av (`realized_by`)
- [Standardiserad applikationskörning](../losningsmonster/PAT-001-standardiserad-applikationskorning.md) (`PAT-001`)

### Relaterar till (`related_to`)
- [Driftsätta och köra applikationer](../formagor/CAP-002-driftsatta-och-kora-applikationer.md) (`CAP-002`)

## Proveniens

- **proposed** — confidence: medium
  - Motiv: Referensarkitekturen sammanför exempelmodellens återanvändbara styrning och realisering.
  - Härledd från: PAT-001, PRN-001
