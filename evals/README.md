# Semantiska evals för EA Stödjare

Den här katalogen innehåller **version 2** av den semantiska eval-sviten. Sviten behåller samtliga 15 v1-fall som bakåtkompatibilitetsregression och lägger till 14 blockerande v2-fall.

## V2-risker som måste täckas

- legacy v1 project open utan implicit migration
- extended legacy
- project metamodel override
- Produkt vs IT-stöd och Produkt vs Plattform
- `can_realize` mot IT-stöd och Plattformstjänst
- `provided_by`
- tvetydig legacy `realized_by`
- embedded Funktion och coverage
- conceptual / market / actual
- derived views är aldrig source of truth
- projektspecifika extensions
- metamodell-change-control

## Princip

Varje evalfall beskriver scenario, förväntade beteenden, förbjudna beteenden, poängkriterier och kritiska fel. Evalfallen är avsedda att köras mot faktisk Custom GPT-/portable-chat-konfiguration. De är semantiska kontrakt, inte facitsvar som ska memoreras.

## Resultatnivåer

- **PASS** – inga kritiska fel och minst 80 %.
- **PASS_WITH_WARNINGS** – inga kritiska fel och 65–79 %.
- **FAIL** – kritiskt fel eller under 65 %.

Releasekandidat kräver att samtliga blockerande fall passerar och att hela sviten når minst 85 % viktad poäng.

## Maskinläsbar coverage

`v2-risk-coverage.yaml` mappar utvecklingsplanens 14 obligatoriska v2-riskområden en-till-en till EVAL-016–EVAL-029. Testsviten verifierar att kartan och suite-filerna är kompletta och konsekventa.
