# Semantiska evals för EA Stödjare

Den här katalogen innehåller version 1 av den semantiska eval-sviten. Den testar sådant som inte kan avgöras enbart med strukturell validering: korrekt EA-klassificering, evidensdisciplin, researchbeteende, modellanalys, osäkerhet och scopekontroll.

## Princip

Varje evalfall beskriver:

- ett användarscenario,
- relevant kontext/underlag,
- vilka förmågor som testas,
- förväntade beteenden,
- oacceptabla beteenden,
- bedömningskriterier och kritiska fel.

Evalfallen är avsedda att köras mot den faktiska Custom GPT-konfigurationen. De är inte facitsvar som ska memoreras; flera sakligt rimliga svar kan få full poäng om de uppfyller kriterierna.

## Struktur

- `eval-suite.yaml` – suite-metadata och gemensamma trösklar.
- `cases/*.yaml` – enskilda evalfall.
- `rubrics/semantic-grading.md` – manuell/LLM-baserad bedömningsrubrik.
- `rubrics/research-grading.md` – särskilda kriterier för externa källor och research.

## Resultatnivåer

- **PASS** – inga kritiska fel och totalpoäng minst 80 %.
- **PASS_WITH_WARNINGS** – inga kritiska fel och totalpoäng 65–79 %.
- **FAIL** – kritiskt fel eller totalpoäng under 65 %.

För releasekandidat ska samtliga blockerande evalfall vara `PASS` och hela sviten nå minst 85 % viktad poäng.
