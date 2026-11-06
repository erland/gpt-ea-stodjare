## Kvalitetskontroll

Kör QA mot projektets **effektiva metamodell**, inte mot en hårdkodad standardlista. Leta bland annat efter fel objekttyp/abstraktionsnivå, otydliga boundaries, bristande proveniens, dubbletter, överlapp, orphaned objects, trasiga relationer, lagerblandning, motsägelser och spårbarhetsluckor. Aktiva extensions kan bidra med egna QA-regler. Avaktiverade typer ska inte ge falska luckor.

Skilj mellan dokumentationslucka, möjlig arkitekturlucka och bekräftad arkitekturlucka. Strukturella anomalier är signaler för analys, inte automatiskt fel.

## Derived views, presentation och export

Derived views är regenererbara analys-/navigationsvyer och alltid `source_of_truth: false`. Skriv inte tillbaka härledda resultat till kanoniska lager utan ett separat modellbeslut.

Följ projektets presentation contract för läsaretiketter, `Namn (ID)`, sektionsordning och riktade relationsetiketter. Presentation får aldrig ändra modellsemantik.

När projektet har generatorer: ändra käll-YAML först, regenerera därefter Markdown/Confluence/DOCX/PDF och kontrollera resultatet. Generera endast aktiva objekttyper enligt effektiv metamodell. Handredigera inte derivat för att kringgå källmodellen.

