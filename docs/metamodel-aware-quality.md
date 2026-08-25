# Metamodellstyrd QA i EA Stödjare v2

QA ska alltid utgå från **projektets effektiva metamodell**, inte från antagandet att hela standardmetamodellen används.

## Upplösningsordning

1. Legacy v1 använder den frysta profilen under `compatibility/ea-stodjare-v1/`.
2. Native v2 med `project-metamodel.yaml` resolverar basprofil + projektets enabled/disabled-val + aktiverade extensions.
3. Native v2 utan projektspecifik metamodell använder standardprofilen som fallback för repositoryts referensprojekt.

Den resolverade QA-konfigurationen är härledd (`source_of_truth: false`).

## Konsekvenser

- Objekt-QA körs bara för aktiva objekttyper.
- Modell-QA som uttryckligen avser en avaktiverad typ filtreras bort.
- Aktiverade extensions kan bidra med QA-regler och dessa körs bara när extensionen faktiskt är aktiv.
- Relationer valideras mot projektets aktiva relationsmängd.
- En avsiktligt avaktiverad objekttyp får inte rapporteras som en coverage-lucka eller saknad kanonisk modellfil.
- Legacy v1 ändrar inte semantik genom att öppnas i en v2-version av EA Stödjare.

## Verktyg

```bash
python3 scripts/resolve_quality_rules.py --project-root <projekt>
```

Output visar aktiv objekt-/relationsmängd, aktiva extensions och det QA-regelurval som gäller för projektet.

## Begränsning

QA-regler är diagnostiska. Resolvering eller QA får aldrig skapa, ändra, dela, slå ihop eller pensionera kanoniska modellobjekt automatiskt.
