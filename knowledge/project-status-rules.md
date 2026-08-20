# Regler för projektstatus och arbetsläge

## 1. Syfte

EA Stödjare ska kunna återuppta ett projekt säkert efter en ny chat, en paus eller en överlämning. `PROJECT_STATUS.md` är den mänskligt läsbara sammanfattningen av arbetsläget och kompletterar `project-manifest.json`.

Manifestet svarar främst på **vad projektet är och vilka filer/revisioner som är giltiga**. Statusfilen svarar främst på **var arbetet befinner sig och vad som återstår**.

## 2. Source-of-truth-regel

`PROJECT_STATUS.md` får aldrig ersätta den kanoniska YAML-modellen.

- EA-objekt och relationer hör hemma i `model/`.
- Källor/proveniens hör hemma i den kanoniska modellen.
- Projektets tekniska identitet/revision hör hemma i `project-manifest.json`.
- Arbetsläge, öppna frågor och nästa steg hör hemma i `PROJECT_STATUS.md`.

Om statusfilen och den kanoniska modellen motsäger varandra gäller den kanoniska modellen för EA-innehåll. Motsägelsen ska då rapporteras och statusfilen korrigeras.

## 3. Obligatoriska statusområden

Statusfilen ska minst kunna beskriva:

- aktuell utvecklings-/arbetsstatus,
- genomförda steg eller analyser,
- analyserat underlag,
- modellstatus,
- preliminära delar,
- öppna frågor,
- kända konflikter,
- senaste kvalitetskontroll,
- rekommenderat nästa steg,
- återupptagningsinstruktion.

Tomma områden ska uttryckligen säga att inget finns registrerat, inte bara utelämnas när frånvaron är viktig för återupptagningen.

## 4. Analyserat underlag

För konkreta EA-projekt bör statusen per relevant källa kunna sammanfatta:

- käll-ID eller tydlig referens,
- dokument/version/datum,
- analysstatus: `not_started`, `partial`, `complete`, `superseded`,
- berörda modellområden,
- viktiga begränsningar.

Den detaljerade evidensen ska fortfarande ligga i modellens proveniensstruktur.

## 5. Preliminära objekt och modelldelar

Statusfilen får sammanfatta preliminära områden men ska normalt referera till objekt-ID eller modellområde i stället för att duplicera fullständiga objekt.

Exempel:

> CAP-014–CAP-018 är kandidater och behöver verksamhetsvalideras.

Inte:

> Kopiera hela definitionerna av CAP-014–CAP-018 in i statusfilen.

## 6. Öppna frågor

En öppen fråga ska vara konkret och handlingsbar. Ange när möjligt:

- berört objekt/område,
- varför frågan är öppen,
- vad som krävs för att lösa den,
- om den blockerar fortsatt arbete.

GPT:n ska inte ställa om samma fråga i en ny chat om svaret redan framgår av projektets status eller kanoniska filer.

## 7. Konflikter

Statusfilen ska sammanfatta materiella öppna konflikter och osäkerheter enligt `knowledge/conflicts-and-uncertainty.md`.

En konflikt ska inte lösas genom att tyst välja en källa. Om befintligt underlag, en styrande källa eller ett dokumenterat beslut inte löser konflikten ska den stå kvar med egen lösningsstatus.

Vid många eller komplexa frågor bör ett separat strukturerat issue-register användas enligt `schemas/conflicts-and-uncertainty.yaml`; `PROJECT_STATUS.md` ska då endast sammanfatta de viktigaste aktiva frågorna.

## 8. Senaste kvalitetskontroll

Statusen ska ange:

- datum eller projektrevision,
- vilken kontrollnivå som genomfördes,
- viktiga resultat,
- kända begränsningar.

En gammal kvalitetskontroll får inte framställas som om den täcker senare modelländringar.

## 9. Rekommenderat nästa steg

EA Stödjare ska normalt ange ett tydligt rekommenderat nästa steg efter avslutad arbetsomgång.

Det ska bygga på:

1. användarens uttryckliga mål,
2. utvecklings-/arbetsplanen,
3. blockerande öppna frågor,
4. modellens faktiska status.

I ett utvecklingsprojekt med sekventiell plan är nästa ej genomförda steg normalt rekommendationen om inget blockerar.

## 10. Uppdateringsregler

När en arbetsomgång faktiskt ändrar projektet ska EA Stödjare:

1. verifiera befintlig projektintegritet,
2. utföra den avgränsade ändringen,
3. uppdatera statusfilen,
4. öka projektrevisionen exakt en gång,
5. uppdatera revisionsloggen,
6. uppdatera manifestets tidsstämpel och filinventering,
7. beräkna checksummor sist,
8. verifiera resultatet.

## 11. Återupptagning i ny chat

När ett befintligt EA Stödjare-projekt bifogas ska GPT:n normalt läsa i denna ordning:

1. `project-manifest.json`,
2. `PROJECT_STATUS.md`,
3. relevant utvecklings-/arbetsplan,
4. endast de kanoniska modell- och styrfiler som behövs för uppgiften.

Syftet är att minimera risken att historiskt konversationsminne får högre auktoritet än det bifogade projektet.

## 12. Status är en sammanfattning, inte ett loggarkiv

`PROJECT_STATUS.md` ska hållas aktuell och kompakt. Historiska revisioner hör hemma i `revision-log.md` och Git-historik. Avslutade öppna frågor och gamla nästa-steg-punkter behöver inte ackumuleras i statusfilen.
