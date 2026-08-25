# Runtimekontrakt – arbetsflöden v2

## Projektöppning

1. Detektera profil.
2. Resolvera faktisk metamodell för native v2.
3. Läs projektstatus/change-control.
4. Tillämpa först därefter objekts- och relationssemantik.

V1 och extended legacy får redigeras vidare utan implicit migration. Migration är separat, icke-destruktiv och rapporterad.

## Modellarbete

Arbeta boundary-first: fastställ identitet, in/out scope och konsument innan produktmatchning. Använd boundary review, decomposition review, merge review, singleton sanity, product stress test och composition sanity när relevant. Review-resultat är diagnostiska och får inte själva skriva om kanonisk modell.

## Migration

Planera före apply. Bevara stabila ID:n när semantiken är densamma. Vid tvetydighet: bevara + markera för review i stället för att gissa. Originalprojekt skrivs aldrig över.

## Uppdatering och change-control

Skilj redaktion/evidensuppdatering från controlled model change, breaking model change och metamodel change. Fryst baseline får endast ändras enligt freeze-policy. Pensionerade ID:n återanvänds aldrig.

## Output

Derived views och presentation är regenererbara konsumentlager och aldrig source of truth. Dokumentgeneratorer använder projektets effektiva metamodell och presentation contract.
