# EA Stödjare v2 – bakåtkompatibilitetskontrakt

## 1. Syfte

Detta dokument definierar vad nästa EA Stödjare-version måste kunna göra med projekt som skapats med tidigare versioner.

Kontraktet är styrande för v2-utvecklingen och ska användas som releasegrind.

Målet är inte att alla äldre projekt automatiskt ska konverteras till v2. Målet är att de ska kunna **öppnas, förstås, fortsätta användas och migreras kontrollerat**.

## 2. Grundprincip

> En ny GPT-version får inte göra ett äldre EA Stödjare-projekt oanvändbart enbart för att standardmetamodellen utvecklats.

Bakåtkompatibilitet innebär därför både **read compatibility**, **work compatibility** och **migration compatibility**.

## 3. Projektklasser som v2 måste känna igen

### 3.1 Native v2 project

Projekt som innehåller en explicit v2-kompatibel projektmetamodell.

GPT:n ska läsa denna metamodell före projektets objektdata.

### 3.2 Legacy v1 project

Projekt som följer den fasta v1-metamodellen och v1-projektformatet.

GPT:n ska kunna:

1. identifiera projektet som v1,
2. ladda en explicit v1-kompatibilitetsprofil,
3. tolka v1-objekt och relationer enligt v1-semantiken,
4. fortsätta arbeta med projektet utan obligatorisk migration,
5. erbjuda migration när en v2-funktion motiverar det.

### 3.3 Extended legacy project

Projekt som utgått från v1 men där verkligt arbete har lagt till supporting-modeller, projektspecifika schemas, härledda vyer eller andra extension-liknande koncept.

Referensprojektet `it-formagemodell-del3-rev80` är obligatoriskt testfall för denna klass.

GPT:n ska kunna:

1. identifiera v1-kärnan,
2. inventera projektspecifika utvidgningar,
3. skilja aktiv semantik från experiment/pensionerade koncept,
4. rekonstruera den faktiskt använda metamodellen,
5. dokumentera denna maskinläsbart,
6. fortsätta arbeta med projektet utan att först kräva full migration,
7. skapa en kontrollerad v2-migration när användaren väljer det.

### 3.4 Unknown or ambiguous project

Om GPT:n inte säkert kan identifiera projektets metamodell får den inte tyst anta v2-standardmodellen.

Den ska:

- inventera schemas, model-filer och manifest,
- ange vad som är säkert identifierat,
- markera osäkerheter,
- undvika destruktiva modelländringar tills projektsemantiken är tillräckligt förstådd.

## 4. Read compatibility

V2 ska kunna läsa v1-projekt utan att kräva att projektfiler först skrivs om.

Minimikrav:

- v1-ID-prefix ska förstås,
- v1-objekttyper ska förstås,
- v1-attribut ska förstås,
- v1-relationssemantik ska förstås,
- v1-proveniens ska förstås,
- v1-statusvärden ska förstås,
- v1-manifest och filstruktur ska förstås.

V2 ska inte automatiskt applicera ny v2-semantik på äldre data när detta kan ändra betydelsen.

## 5. Work compatibility

Ett legacy-projekt ska kunna fortsätta utvecklas i v2 utan omedelbar migration.

Det innebär att GPT:n vid arbete i legacy mode ska:

- respektera projektets befintliga semantik,
- skapa nya objekt enligt projektets legacy-profil om användaren inte valt migration,
- undvika att skriva v2-only-attribut in i v1-filer utan explicit formatändring,
- dokumentera om en önskad funktion kräver v2-migration eller project extension.

V2 får alltså fungera som **kompatibel redigerare** av v1-projekt.

## 6. Migration compatibility

Migration ska vara:

- explicit,
- reproducerbar,
- granskningsbar,
- icke-destruktiv,
- informationsbevarande så långt semantiken tillåter.

Migration får inte skriva över originalprojektet som standard.

Den ska skapa:

- ny projektkopia eller ny kontrollerad revision,
- explicit v2-projektmetamodell,
- migreringsrapport,
- lista över automatiskt transformerade objekt/relationer,
- lista över osäkra transformationer som kräver beslut,
- lista över legacy-koncept som bevarats som extensions.

## 7. Stabil ID-princip

Migration ska behålla ett objekts ID när objektets semantiska identitet är oförändrad.

Nytt ID krävs när:

- ett objekt semantiskt ersätts av ett annat,
- en uppdelning skapar flera självständiga objekt,
- ett sammanslaget objekt får ny semantisk identitet.

Pensionerade ID:n får inte återanvändas.

## 8. V1 → v2: kända semantiska skillnader

Följande skillnader får **inte** hanteras med blind textsök/ersätt.

### 8.1 Förmåga `scope`

V1 kan använda ett generellt `scope`.

V2 planerar:

```yaml
in_scope:
out_of_scope:
consumer_scope:
```

Migration måste avgöra om legacy `scope` motsvarar positiv boundary, blandad boundary eller behöver mänsklig granskning.

### 8.2 Plattformstjänst

V1-formuleringar kan implicera ett standardiserat/gemensamt tekniskt erbjudande.

V2-semantiken är realiseringsneutral.

Legacy-data behöver normalt inte skrivas om enbart för definitionens skull, men GPT:n ska tolka äldre objekt enligt v1-profil tills migration gjorts.

### 8.3 Plattform

V1 `platform` kan ha bredare betydelse än planerad v2-standardsemantik.

Migration får inte automatiskt anta att varje v1-Plattform redan är en v2-konceptuell Plattform. Varje objekt måste kunna behållas som legacy-semantik tills en säker klassificering finns.

### 8.4 `realized_by`

V1 kan använda `realized_by` i en betydelse som senare behöver delas mellan konceptuell hemvist och konkret realisering.

Native v2 använder nu:

```text
Platform Service --provided_by--> Platform
```

för konceptuell hemvist. Migration får därför inte mekaniskt byta alla legacy-relationer:

```text
Platform Service --realized_by--> Platform
```

till `provided_by`. En relation får konverteras endast när legacybetydelsen faktiskt är konceptuell hemvist/tillhandahålls inom. Om relationen uttrycker eller kan uttrycka konkret realisering ska den bevaras för manuell semantisk granskning. Rev80 är ett känt fall där PLS→PLT `realized_by` betyder konceptuell hemvist och därmed är en stark kandidat för kontrollerad migration till `provided_by`.

### 8.5 Produkt

Produkt finns inte som standardobjekt i v1.

Legacy-projekt som själva infört produkter ska rekonstrueras som project extension eller migreras till v2:s Product-stöd först efter inventering av faktisk projektsyntax och semantik.

## 9. Referensprojekt rev80 – obligatoriskt kompatibilitetstest

`it-formagemodell-del3-rev80` ska användas som ett verkligt extended legacy-test.

V2-utvecklingen ska kunna verifiera minst:

- 13 IT-förmågor,
- befintliga IT-stöd,
- 92 Plattformstjänster,
- 35 konceptuella Plattformar,
- kanoniska relationer,
- produkt-/teknikreferenser,
- produkt→PLS-realiseringar,
- deploymentklassificering,
- opennessklassificering,
- plattformsmognad,
- relation roles,
- derived views,
- baseline/model freeze/change control,
- pensionerade actual-platform-experiment.

Dessa delar behöver inte alla bli standardfunktioner i v2-kärnan. Kompatibilitetskravet är att den nya GPT:n ska kunna **förstå vad projektet faktiskt använder** och fortsätta arbeta med det.

## 10. Extended legacy reconstruction

När ett projekt saknar explicit project metamodel men har egna supporting-filer ska GPT:n kunna skapa en rekonstruerad beskrivning med minst:

```yaml
base_profile:
detected_object_types:
detected_embedded_structures:
detected_relations:
custom_attributes:
custom_enums:
derived_views:
presentation_semantics:
governance_extensions:
uncertainties:
```

Rekonstruktionen är initialt en analysartefakt och får inte automatiskt bli kanonisk utan kontroll.

## 11. Ingen tyst informationsförlust

Om v2 inte kan representera ett legacy-koncept exakt måste GPT:n:

1. bevara originalinformationen,
2. dokumentera mismatchen,
3. representera konceptet som extension eller legacy payload om möjligt,
4. markera behov av beslut.

Det är inte tillåtet att utelämna information bara för att den inte passar standardmetamodellen.

## 12. Ingen tyst semantisk uppgradering

Följande får inte ske utan evidens eller explicit projektbeslut:

- Product → Actual Platform Offering,
- product capability → actual organizational use,
- actual product use → organizational platform offering,
- `related_to` → hårt `depends_on`,
- legacy `realized_by` → v2 `provided_by`,
- v1 Platform → v2 conceptual Platform.

## 13. Conceptual / market / actual vid migration

Legacy-projekt kan blanda dessa lager.

V2-migrationen ska, där det är möjligt, klassificera information i:

- conceptual,
- market_reference,
- actual_state.

Osäker klassificering ska markeras och bevaras, inte gissas bort.

## 14. Derived views

Legacy-rapporter och supporting-vyer som kan återskapas från kanonisk data ska i v2 kunna klassificeras som derived views.

Migration får inte göra en härledd presentation till ny source of truth.

## 15. Backward compatibility och validatorn

Den framtida v2-validatorn ska kunna arbeta i minst tre explicita lägen:

```text
native-v2
legacy-v1
extended-legacy
```

Valideringen ska använda rätt profil för respektive projekt och får inte rapportera v2-obligatoriska fält som fel i ett legitimt v1-projekt.

## 16. Backward compatibility och dokumentgeneratorer

När ett legacy-projekt öppnas utan migration ska befintlig dokumentgenerering kunna fortsätta använda legacy-semantiken.

När projektet migrerats ska generatorer i stället styras av den explicita v2-projektmetamodellen och presentation contract.

## 17. Releasegrind

En v2-releasekandidat får inte godkännas förrän följande fungerar end-to-end:

1. öppna ett minimalt v1-projekt,
2. analysera det med korrekt v1-semantik,
3. göra en avgränsad ändring utan migration,
4. validera projektet efter ändringen,
5. migrera projektet till v2 i separat kopia,
6. verifiera semantic equivalence där transformationen är säker,
7. öppna rev80 som extended legacy,
8. rekonstruera rev80:s projektmetamodell,
9. fortsätta arbeta med rev80 utan obligatorisk migration,
10. migrera rev80 i separat kopia utan dold informationsförlust.

## 18. Acceptanskriterium

Bakåtkompatibilitetskontraktet är uppfyllt när en användare kan ta en tidigare EA Stödjare-projektzip, öppna den i den nya GPT-versionen och fortsätta arbetet utan att behöva känna till intern v1/v2-migrationsmekanik för att undvika datatapp.
