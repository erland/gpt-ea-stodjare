# Runtimekontrakt – domänmodell v2

Detta dokument är den aktuella läsmodellen för EA Stödjare 2.x. Det ersätter historiska stegvisa utvecklingsnoter i Builder Knowledge; äldre designbeslut finns kvar i repositoryt som spårbar historik men ska inte tolkas som framtida arbete.

## Projektprofil före semantik

Fastställ alltid projektprofil innan objekt eller relationer tolkas: `native_v2`, `legacy_v1`, `extended_legacy` eller `unknown`. Native v2 använder `project-metamodel.yaml` + basprofil + aktiva extensions. Legacy-profiler använder sin frysta semantik. `unknown` får inte tyst behandlas som v2.

## Standardobjekt

V2:s standardmodell är avsiktligt liten: Drivkraft, Mål, Princip, Förmåga, IT-stöd, Plattformstjänst, Plattform, Standard och Produkt. Lösningsmönster och Referensarkitektur stöds som sekundära typer. Funktion är embedded på IT-stöd, Plattformstjänst och Plattform och kan ha lokalt ID, men är inte global objekttyp.

## Centrala v2-semantiker

- **Förmåga:** native v2 använder `in_scope`, `out_of_scope` och vid behov `consumer_scope`. Legacy `scope` får inte mekaniskt döpas om.
- **Plattformstjänst:** ett realiseringsneutralt tekniskt erbjudande/funktionalitetskontrakt; inte automatiskt central drift, produkt eller faktisk organisationsstatus.
- **Plattform:** konceptuell, produktneutral gruppering/hemvist för Plattformstjänster. Singleton kan vara legitim när boundary är självständig.
- **Produkt:** konkret marknadserbjudande som kan bidra till eller realisera IT-stöd eller Plattformstjänst. Produkt är inte automatiskt IT-stöd, Plattform, Plattformstjänst eller faktisk användning.

## Relationer

- `provided_by`: Plattformstjänst → Plattform och betyder konceptuell hemvist.
- `can_realize`: Produkt → IT-stöd eller Plattformstjänst och betyder verifierbar realiseringspotential, inte produktval eller actual use. `realization_role` krävs.
- `realized_by`: reserveras för konkret realiseringssemantik där sådan uttrycks.
- Legacy `realized_by` migreras endast när betydelsen är verifierad; tvetydiga fall bevaras för review.

Relationskvalificerare används endast där relationstypen tillåter dem. Projektets effektiva metamodell är auktoritativ för tillåtna typer, attribut, relationer och värdemängder.

## Extensions

Projekt kan välja bort standardtyper och lägga till egna objekttyper, attribut, relationer, enumvärden, QA och presentationssemantik. Återanvändbara extensions har namespace och får inte kollidera med kärnan. Extensions ska användas före utvidgning av standardkärnan när behovet är projektspecifikt.
