# Migration – Plattform v1 till konceptuell Plattform v2

V2 definierar Plattform som en **produktneutral konceptuell gruppering av Plattformstjänster**. V1 definierade Plattform bredare som teknisk grund/realisering. Därför är detta en semantisk migration och inte ett mekaniskt namnbyte.

## Grundregel

Ett v1-Plattformobjekt får fortsätta användas med v1-semantik utan migration. Vid migration ska man avgöra om objektet faktiskt beskriver en konceptuell gruppering av stabila Plattformstjänster, en konkret runtime/teknisk grund, en produktnamngiven miljö eller en blandning av flera nivåer.

Stabilt ID får behållas när den konceptuella identiteten är densamma. Om objektets identitet i praktiken är en konkret produkt/realisering ska det inte tvingas in som v2-Plattform.

## Produktneutralitet

`technology` och `products` i legacy-data är kontext/evidens om realisering och får inte ensamma definiera v2-Plattformens boundary. Produktnärvaro eller marknadskapacitet är inte bevis för ett faktiskt organisatoriskt plattformserbjudande.

## Relationer

Legacy `PLS --realized_by--> PLT` skrivs **inte om i steg 8**. Den relationen migreras först när v2-relationsmodellen inför `provided_by`. Fram till dess bevaras legacy-relationens innebörd i v1-profilen.

## Boundary review

Vid migration bör minst följande granskas:

1. vilket stabilt tjänstelöfte Plattformen grupperar,
2. om ingående PLS delar rimlig livscykel, kompetens eller förvaltningslogik,
3. om Plattformen fortfarande är meningsfull om en produkt byts,
4. om en bred Plattform bör dekomponeras,
5. om en singleton är legitim genom självständigt tjänstelöfte/livscykel.
