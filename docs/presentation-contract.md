# Reader-oriented presentation contract

## Syfte

Presentationskontraktet separerar **modellens maskinläsbara semantik** från det språk och den struktur som möter en läsare. Kontraktet finns i `presentation/presentation-contract.yaml` och valideras mot `schemas/presentation-contract.schema.json`.

Kontraktet är uttryckligen `source_of_truth: false`. Det får ändra **etikett, ordning, rubrik och visningsmönster**, men aldrig modellens innebörd, proveniens, informationslager eller relationer.

## Standardvisning av objekt

Standardmönstret är:

```text
Namn (ID)
```

ID visas alltid i standardkontraktet. Ett projektspecifikt kontrakt får välja annan visningspolicy, men ett genererat dokument får inte låta ett presentationsnamn ersätta objektets stabila ID i modellen.

## Fältetiketter

Maskinfält kan få läsarorienterade etiketter. V2-standardkontraktet innehåller bland annat:

| Modellfält | Läsaretikett |
|---|---|
| `capability.in_scope` för IT-förmåga | **Stödjer** |
| `capability.in_scope` för verksamhetsförmåga | **Omfattar** |
| `capability.out_of_scope` | **Omfattar inte** |
| `consumer_scope` | **Avsedda konsumenter** |
| `product.product_kind` | **Produkttyp** |

Den kontextberoende etiketten för `in_scope` ändrar inte fältets semantik. Den gör endast presentationen mer naturlig för läsaren.

## Relationsetiketter

Relationstyper behåller stabila maskinnamn men får riktade läsaretiketter. Exempel:

- `Platform Service --provided_by--> Platform` visas från tjänstens perspektiv som **Tillhandahålls av** och från Plattformens perspektiv som **Tillhandahåller**.
- `Product --can_realize--> IT Support|Platform Service` visas som **Kan realisera** och omvänt **Kan realiseras av**.
- `supports` visas som **Stödjer** / **Stöds av**.

Presentationsetiketten får inte användas för att konvertera en relationstyp till en annan.

## Härledda navigationssektioner

Kontraktet kan deklarera navigationssektioner som bygger på `derived-views/views.yaml`. Dessa sektioner är alltid:

- `source_of_truth: false`,
- regenererbara,
- read-only i presentationslagret,
- förbjudna som underlag för write-back till den kanoniska modellen.

Exempel är **Understöds av** på en Förmåga och **Tillhandahåller** på en Plattform. För Produkt kan sektionerna **Kan realisera IT-stöd** och **Kan realisera Plattformstjänster** visas, men med epistemisk not om att potential inte betyder faktiskt val eller faktisk användning.

## Tomma sektioner

Standardpolicyn är `omit`: en tom sektion visas inte. Kontraktet kan sätta `show_placeholder` globalt eller per navigationssektion om ett projekt behöver synliggöra avsaknad av data.

## Projektanpassning

`project-metamodel.yaml` och extensions får tillföra presentationssemantik enligt de kontrakt som redan etablerats i steg 4 och 14. Projektanpassningar ska vara delta ovanpå ett valt presentationskontrakt, inte kopior av hela basmodellen.

Kontraktet är implementerat och används av den metamodellstyrda Markdown/Confluence/DOCX/PDF-genereringen. Projektanpassningar förblir presentationsdelta och ändrar inte kanonisk semantik.
