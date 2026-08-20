# Testexempel – extraktion ur underlag

Dessa testexempel hör till steg 9 och är avsedda som semantiska regressionsexempel. De är ännu inte en automatiserad eval-svit; det införs i steg 25.

Varje fall innehåller ett syntetiskt underlag och ett förväntat analysutfall. Syftet är att kontrollera arbetsflödets viktigaste beteenden utan att låsa exakt ordalydelse.

## Fall

1. `01-explicit-and-derived.md` – skiljer explicit objekt från härledd princip.
2. `02-platform-vs-service.md` – skiljer Plattformstjänst från Plattform.
3. `03-no-object.md` – visar att varje textstycke inte ska generera ett EA-objekt.
4. `04-duplicate-and-normalization.md` – identifierar möjlig dubblett/alias utan att slå ihop automatiskt.

## Godkänt beteende

Ett test betraktas konceptuellt som godkänt när EA Stödjare:

- inte flyttar `derived` eller `proposed` till `explicit`,
- använder metamodelens semantik framför källans etiketter,
- bevarar osäkerhet där underlaget inte räcker,
- inte skapar onödiga objekt,
- inte skriver in testresultatet i den kanoniska modellen utan ett uttryckligt införandesteg.
