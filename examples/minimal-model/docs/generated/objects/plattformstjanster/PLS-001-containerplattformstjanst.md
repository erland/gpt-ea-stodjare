# Containerplattformstjänst (PLS-001)

> Genererad från kanonisk YAML · läge `working` · projektrevision `5` · presentationskontrakt `ea-reader-oriented-sv`

- **ID:** `PLS-001`
- **Objekttyp:** `platform_service`
- **Status:** `candidate`

## Beskrivning

Gemensamt tjänsteerbjudande för att driftsätta och köra containeriserade applikationer.

## Funktioner

- Driftsätta containeriserade applikationer
- Skala applikationsworkloads
- Hantera applikationskonfiguration

## Egenskaper

- **Avsedda konsumenter:** Operativa utvecklingsområden

## Relationer

### Används av (`uses`)
- [Ärendehanteringsstöd](../it-stod/ITS-001-arendehanteringsstod.md) (`ITS-001`)

### Begränsas av (`constrains`)
- [Standard för paketering av applikationer](../standarder/STD-001-standard-for-paketering-av-applikationer.md) (`STD-001`)

### Realiseras av (`realized_by`)
- [Containerplattform](../plattformar/PLT-001-containerplattform.md) (`PLT-001`)

### Styrs av (`governed_by`)
- [Gemensamma behov realiseras som återanvändbara tjänster](../principer/PRN-001-gemensamma-behov-realiseras-som-ateranvandbara-tjanster.md) (`PRN-001`)

### Stödjer (`supports`)
- [Driftsätta och köra applikationer](../formagor/CAP-002-driftsatta-och-kora-applikationer.md) (`CAP-002`)

## Proveniens

- **proposed** — confidence: medium
  - Motiv: Tjänsten föreslås som konsumtionsyta för IT-förmågan.
  - Härledd från: CAP-002
