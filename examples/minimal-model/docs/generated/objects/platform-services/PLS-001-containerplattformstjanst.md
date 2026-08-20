# Containerplattformstjänst

- **ID:** `PLS-001`
- **Objekttyp:** `platform_service`
- **Status:** `candidate`

## Beskrivning

Gemensamt tjänsteerbjudande för att driftsätta och köra containeriserade applikationer.

## Tjänsteinformation

- **Konsumentomfång:** Operativa utvecklingsområden

## Funktioner

- Driftsätta containeriserade applikationer
- Skala applikationsworkloads
- Hantera applikationskonfiguration

## Relationer

### Används av (`uses`)
- [Ärendehanteringsstöd](../it-support/ITS-001-arendehanteringsstod.md) (`ITS-001`)

### Begränsas av (`constrains`)
- [Standard för paketering av applikationer](../standards/STD-001-standard-for-paketering-av-applikationer.md) (`STD-001`)

### Realiseras av (`realized_by`)
- [Containerplattform](../platforms/PLT-001-containerplattform.md) (`PLT-001`)

### Styrs av (`governed_by`)
- [Gemensamma behov realiseras som återanvändbara tjänster](../principles/PRN-001-gemensamma-behov-realiseras-som-ateranvandbara-tjanster.md) (`PRN-001`)

### Stödjer (`supports`)
- [Driftsätta och köra applikationer](../capabilities/CAP-002-driftsatta-och-kora-applikationer.md) (`CAP-002`)

## Proveniens
- **proposed** — confidence: medium
  - Motiv: Tjänsten föreslås som konsumtionsyta för IT-förmågan.
  - Härledd från: CAP-002
