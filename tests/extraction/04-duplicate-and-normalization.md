# Test 04 – dubblett och normalisering

## Syntetiskt underlag

Källa A:

> Den centrala identitetstjänsten används av samtliga interna webbapplikationer för autentisering.

Källa B:

> IAM Service tillhandahåller gemensam autentisering till interna applikationer.

## Befintlig modell

- `PLS-004` – "Gemensam identitetstjänst"

## Förväntat analysbeteende

- Båda formuleringarna är kandidater till Plattformstjänst.
- De ska jämföras med `PLS-004` innan nya objekt skapas.
- Resultatet bör vara `match`, `update` eller `possible_duplicate` beroende på ytterligare evidens.
- EA Stödjare får inte anta att "central identitetstjänst", "IAM Service" och `PLS-004` är samma objekt enbart på språklig likhet.
- Om de verifieras som samma objekt bör källornas alias/originalformuleringar kunna bevaras i evidensen medan modellnamnet normaliseras.
