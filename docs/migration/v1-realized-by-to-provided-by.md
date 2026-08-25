# Migration: legacy `realized_by` till native v2 `provided_by`

## Syfte

Native v2 använder `Platform Service --provided_by--> Platform` för konceptuell hemvist. V1 tillät `Platform Service --realized_by--> Platform` med bredare realiseringssemantik.

## Regel

Ingen global sök/ersätt-migration är tillåten. Varje legacy-relation klassificeras först som:

1. **conceptual_home** – relationen betyder att PLS hör hemma i/tillhandahålls inom Plattformen. Den kan konverteras till `provided_by`.
2. **concrete_realization** – relationen uttrycker konkret teknisk realisering. Den ska inte konverteras till `provided_by`.
3. **ambiguous** – underlaget räcker inte. Bevara relationen i legacy-semantik och flagga för granskning.

## Rev80

I rev80-referensprofilen är PLS→PLT `realized_by` dokumenterad som konceptuell hemvist. Dessa relationer är därför kandidater för kontrollerad konvertering till `provided_by`, men själva referensprojektet ändras inte i steg 11.

## Invarianter

- proveniens bevaras,
- stabilt relations-ID bör bevaras när semantiken är ekvivalent och migrationspolicyn tillåter det,
- migration får inte inferera faktisk produktanvändning eller organisatoriskt erbjudande.
