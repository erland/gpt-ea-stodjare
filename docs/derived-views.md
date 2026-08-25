# Derived views i EA Stödjare v2

Derived views är maskinläsbara fråge-/presentationsdefinitioner som **återskapas från kanonisk data**. De är aldrig source of truth för arkitektur-, marknads- eller actual-state-påståenden.

## Grundregler

1. `source_of_truth` ska alltid vara `false`.
2. En vy får endast läsa aktiva objekt, relationer och informationslager; den får inte skriva tillbaka till dem.
3. En vy ska kunna regenereras deterministiskt från samma input.
4. Saknad rad i en vy betyder inte automatiskt att kanonisk data ska tas bort eller läggas till.
5. Marknadssemantik behålls i presentationen. Exempelvis betyder Product `can_realize` inte faktisk användning.
6. Generated output ska betraktas som cache/presentation och kan tas bort och byggas om.

## Katalog

Standarddefinitionerna finns i `derived-views/views.yaml` och valideras mot `schemas/derived-view.schema.json`.

Varje vy anger:

- `id`
- `source_of_truth: false`
- startpunkt (`anchor`)
- `join_path` med relation, riktning och alias
- valfria `filters`
- valfri `aggregation`
- `sort`
- `presentation_semantics`
- `regeneration_policy`

## Standardvyer i steg 17

- Förmåga → Plattformstjänst → Plattform
- Plattform → Plattformstjänst → Förmåga
- Produkt → IT-stöd
- Produkt → Plattformstjänst → Plattform
- härledda plattformsberoenden
- shared realization
- product coverage

## Regenerering

`scripts/generate_derived_views.py` materialiserar vyerna som YAML i vald outputkatalog. Outputen innehåller input-fingeravtryck och `source_of_truth: false` och ska inte behandlas som kanonisk modell.

Exempel:

```bash
python3 scripts/generate_derived_views.py --project-root . --output-dir build/derived-views
```

`on_source_change` betyder att en konsument får cacha resultatet men måste regenerera när relevant kanonisk input ändras. `always` regenereras varje gång. `manual_rebuild` tillåter explicit körning men ändrar inte vyers icke-kanoniska status.
