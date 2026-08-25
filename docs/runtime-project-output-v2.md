# Runtimekontrakt – projekt, output och kompatibilitet v2

## Projektmetamodell

Native v2 deklarerar sin faktiska modell i `project-metamodel.yaml`: basprofil, aktiva/inaktiva standardtyper, custom types, attribut, relationer, värdemängder, extensions, derived views och presentationsdelta. Resolverad metamodell är härledd och inte source of truth.

## Kompatibilitet

- legacy v1 använder fryst v1-profil,
- extended legacy använder rekonstruerad/projektspecifik profil,
- native v2 använder aktuell projektmetamodell,
- unknown stoppas för semantisk automatiktolkning.

## Derived views och presentation

Derived views är deterministiska, regenererbara och `source_of_truth: false`. Presentation contract styr läsaretiketter, ordning, rubriker och visning men får inte ändra semantik eller proveniens.

## Dokumentgenerering

Markdown, Confluence, DOCX och PDF genereras från projektets effektiva metamodell och presentation contract. Generation manifest beskriver vilka kataloger som skapats. Product, custom types och extensions ska följa med när de är aktiva; avaktiverade typer utelämnas.

## Validering och release

`scripts/validate_project.py` är gemensam strukturell grind och kan skriva maskinläsbar valideringsrapport. CI/release ska även kontrollera legacy v1, extended legacy/rev80, migration, Builder-distributioner, dokumentexport och release unpack-and-validate.
