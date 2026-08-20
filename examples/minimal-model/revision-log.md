# Revisionslogg – Minimal EA-modell

## Revision 1 – 2026-08-20

- Exempelprojektet sattes under EA Stödjares projektformat v1.
- Befintlig minimalmodell registrerades som första manifeststyrda revision.

## Revision 2 – 2026-08-20

- Projektstatusfil tillagd för att demonstrera återupptagningsformatet från steg 8.

## Revision 3 – steg 16 referensoutput

- Minimalmodellen används som fixture för deterministisk Markdown-generering.
- README kompletterades med instruktion för regenerering.
- Genererad `working`-output skapades under `docs/generated/`; outputen är ett derivat och inventeras inte som kanonisk modell.

## Revision 4 – steg 17 referensoutput

- Confluence wiki markup-referensoutput genererad under `exports/confluence/`.
- Exporten använder samma kanoniska YAML-modell och statusfiltrering som Markdown.
- Genererad export är derivat och inte source of truth.



## Revision 5 – steg 18 referensoutput

- DOCX- och PDF-referensexporter genererade i `working` och `published`.
- Exporterna är derivat av den kanoniska YAML-modellen och inventeras inte som kanonisk modell.
