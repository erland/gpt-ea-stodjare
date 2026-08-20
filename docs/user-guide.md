# EA Stödjare – kort användarhandledning

## Vad EA Stödjare hjälper till med

EA Stödjare är utvecklad för enterprise architecture-arbete. Den är särskilt användbar när du vill gå från ostrukturerat underlag till en tydligare EA-modell, granska en befintlig modell eller komplettera den med kvalificerad research.

Kärnobjekten i v1 är:

- Drivkraft
- Mål
- Princip
- Förmåga (verksamhetsförmåga eller IT-förmåga)
- IT-stöd
- Plattformstjänst
- Plattform
- Standard

Lösningsmönster och Referensarkitektur stöds som sekundära objekttyper.

Detaljerad lösningsarkitektur ligger utanför v1.

## Tre huvudsätt att börja

### 1. Börja med ett underlag

Bifoga exempelvis strategi, verksamhetsplan, arkitekturdokument, systemförteckning eller plattformsbeskrivning och skriv:

> Analysera underlaget och identifiera relevanta EA-objekt. Skilj på sådant som uttryckligen står i underlaget, sådant du härleder och sådant du själv föreslår.

EA Stödjare ska då först analysera och klassificera kandidater. Den ska inte automatiskt behandla sina egna slutsatser som organisationens beslut.

### 2. Börja med en fråga om hur modellen borde se ut

Exempel:

> Hjälp mig ta fram en modell över vilka IT-förmågor ett stödjande utvecklingsområde behöver tillhandahålla för operativa utvecklingsområden. Använd vårt underlag, din EA-kunskap och relevant aktuell omvärldsresearch.

I detta läge kan EA Stödjare kombinera:

- organisationens underlag,
- generell EA-kunskap,
- aktuell extern research,
- tydligt markerade antaganden och rekommendationer.

Resultatet bör betraktas som ett kvalificerat modellförslag tills organisationen har validerat och accepterat det.

### 3. Börja med en befintlig EA Stödjare-zip

Bifoga projektpaketet och be exempelvis:

> Granska vår befintliga förmågekatalog och identifiera dubbletter, överlapp, fel abstraktionsnivå och möjliga luckor.

eller:

> Lägg in de här godkända principerna och ge mig en uppdaterad projekt-zip.

När projektet ska ändras ska EA Stödjare bevara stabila ID:n, uppdatera relationer/proveniens, regenerera derivat och revisionshantera projektet.

## Skillnaden mellan några centrala begrepp

### Förmåga och funktion

**Förmåga** beskriver vad verksamheten eller IT behöver kunna åstadkomma.

**Funktion** beskriver vad ett IT-stöd, en plattformstjänst eller en plattform konkret tillhandahåller. Funktion är därför inte en separat global EA-objekttyp i v1.

### IT-stöd, Plattformstjänst och Plattform

- **IT-stöd** – ett informationssystem, en applikation eller motsvarande stöd som hjälper till att realisera en förmåga.
- **Plattformstjänst** – ett återanvändbart tekniskt erbjudande som kan konsumeras av IT-stöd eller utvecklingsteam.
- **Plattform** – den tekniska grund som realiserar eller möjliggör plattformstjänster.

## Hur källor och rekommendationer hanteras

EA Stödjare skiljer mellan:

- `explicit` – står uttryckligen i organisationens underlag,
- `derived` – härlett från underlag eller modell,
- `proposed` – EA Stödjares rekommendation/förslag,
- `external` – fakta eller observation från extern källa.

Extern research gör inte automatiskt ett förslag till intern sanning. Ett organisationsspecifikt förslag som bygger på research ska normalt fortfarande vara `proposed` tills organisationen accepterar det.

## När research är lämplig

Be gärna EA Stödjare använda omvärlden när du vill:

- jämföra med etablerade EA-modeller,
- hitta relevanta standarder eller ramverk,
- undersöka hur jämförbara organisationer strukturerar ett område,
- bedöma om er modell verkar ha tydliga luckor,
- ta fram en modell när det interna underlaget är begränsat.

Ett bra exempel är:

> Jämför vår struktur för plattformstjänster med relevant aktuell praxis och jämförbara organisationer. Bedöm vad som faktiskt är överförbart till vår kontext.

## Dokumentation och export

YAML är projektets source of truth. Därifrån kan projektversionen generera:

- Markdown,
- Confluence markup,
- DOCX,
- PDF.

Använd `working` när arbetsmaterial och kandidater ska synas och `published` när endast publicerbart innehåll ska tas med enligt projektets regler.

## Bra promptmönster

För analys:

> Analysera [underlag] med fokus på [objekttyper/scope]. Redovisa explicit, derived och proposed separat och peka ut osäkerheter.

För modellförslag:

> Ta fram ett förslag på [modelltyp] för [organisation/domän]. Utgå från [underlag], komplettera med relevant aktuell research och motivera struktur, nivåer och avgränsningar.

För granskning:

> Granska [modell/katalog] med fokus på klassificering, abstraktionsnivå, dubbletter, överlapp, relationer och möjliga luckor. Ändra inte modellen ännu.

För projektändring:

> Genomför följande godkända ändringar i EA Stödjare-projektet: [...]. Bevara stabila ID:n där det går, regenerera derivat, validera och ge mig en uppdaterad zip.

## Vad EA Stödjare inte ska göra i v1

EA Stödjare ska inte glida över i detaljerad komponent-, API-, integrations-, databas-, nätverks-, deployment- eller säkerhetsdesign. Den kan beskriva relevanta EA-objekt och relationer på enterprise-nivå, men detaljerad lösningsarkitektur kräver ett annat stöd och andra arbetsflöden.
