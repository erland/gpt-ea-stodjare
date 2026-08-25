# Arbetsflöde – boundary-first modeling

Använd detta arbetsflöde när nya eller befintliga Förmågor, IT-stöd, Plattformstjänster eller Plattformar behöver granskas, särskilt före produktmatchning eller större strukturförändringar.

## Körordning

1. **Boundary review** – definiera vad objektet är till för, vad som ingår och vad som inte ingår.
2. **Decomposition review** – kontrollera om objektet innehåller flera självständiga semantiska ansvar.
3. **Merge review** – kontrollera om närliggande objekt egentligen beskriver samma stabila ansvar/erbjudande.
4. **Singleton sanity review** – för Plattform med en Plattformstjänst, verifiera legitim konceptuell boundary.
5. **Product stress test** – byt tänkt produkt/realisering och kontrollera att arkitekturobjektets identitet består.
6. **Composition sanity review** – när realiseringen är sammansatt, kontrollera att kompositionen inte blivit arkitekturens definition.

## Beslutsregler

- Gör ingen automatisk split, merge eller omklassificering.
- Produktlikhet eller delad produkt är aldrig ensam tillräcklig grund för merge.
- En singleton-Plattform är inte ett fel; den måste bara ha en självständig konceptuell mening.
- Ett product stress test ska kunna genomföras utan att `can_realize` blandas ihop med faktisk organisationsanvändning.
- Förslag som förändrar kanonisk modell måste gå genom normal evidens-, QA- och change-control-process.
- Om boundaryn fortfarande är oklar: behåll objektet som kandidat eller markera review-behov i stället för att fylla luckan med antaganden.
