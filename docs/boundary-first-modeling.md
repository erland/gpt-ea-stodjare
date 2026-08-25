# Boundary-first modeling i EA Stödjare v2

Steg 19 gör de granskningsmönster som visade sig användbara i rev80 generella. De är diagnostiska arbetsflöden och får aldrig automatiskt ändra kanoniska objekt, relationer eller informationslager.

## Grundordning

1. Fastställ objektets boundary och konsumentvärde.
2. Kontrollera om objektet bör delas upp eller slås samman.
3. Kontrollera specialfallen singleton och komposition.
4. Stressa modellen mot alternativa produkter/realiseringar.
5. Gör först därefter kanoniska ändringar, med evidens och normal change-control.

Denna ordning minskar risken att produktidentitet, historisk implementation eller organisatorisk vana används som ersättning för arkitektursemantik.

## Sex standardgranskningar

### Boundary review
Används på Förmåga, IT-stöd, Plattformstjänst och Plattform. Fokus ligger på positiv/negativ gräns, konsumentvärde, abstraktionsnivå och produktneutralitet.

### Decomposition review
Används när ett objekt misstänks innehålla flera självständiga ansvar, livscykler eller konsumenterbjudanden. Uppdelning är en kandidat, aldrig automatisk åtgärd.

### Merge review
Används när två eller flera objekt kan vara semantiskt samma objekt med olika namn, historik eller realisering. Delad produkt är inte i sig skäl för merge.

### Singleton sanity review
En Plattform med en enda Plattformstjänst är tillåten i v2. Reviewn avgör om boundaryn är legitim och produktneutral eller om Plattformen bara duplicerar tjänsten/produkten.

### Product stress test
Byt mentalt ut nuvarande produkt mot en eller flera alternativ. Om IT-stöd, Plattformstjänst eller Plattform då tappar identitet är modellen sannolikt för hårt kopplad till produkt/realisering.

### Composition sanity review
Används när en Plattformstjänst eller Plattform realiseras genom komposition. Kompositionen ska kunna förändras utan att det konceptuella konsumentlöftet måste ändras.

## Resultat

Varje workflow kan resultera i `pass`, `review` eller `blocked`. `review` betyder att modellbeslut kräver mänsklig/arkitekturell bedömning eller mer evidens. `blocked` används när ett känt semantiskt fel måste lösas innan objektet kan godkännas.

Reviews är `source_of_truth: false`. De får skapa granskningsanteckningar och kandidater men aldrig skriva tillbaka ändringar till `model/`, `market-reference/` eller `actual-state/` automatiskt.

Maskinläsbar definition finns i `schemas/modeling-review-workflows.yaml`.
