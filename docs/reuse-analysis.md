# EA Stödjare – återbruksanalys av Lärobokskaparen

## 1. Syfte och status

Detta dokument är resultatet av utvecklingsplanens **steg 2**. Syftet är att identifiera vilka mekanismer i Lärobokskaparen som bör återanvändas när EA Stödjare byggs vidare, vilka som kräver domänanpassning och vilka som inte hör hemma i produkten.

Analysen avser Lärobokskaparens repositorystruktur, GPT-instruktion, Knowledge-upplägg, projektmall, revisions- och integritetsmekanismer, exportstöd, distributionsbygge och validering.

Huvudslutsats:

> EA Stödjare bör återanvända Lärobokskaparens robusta **projekt-, kvalitets-, distributions- och förvaltningsmönster**, men inte dess bokcentrerade informationsmodell eller publiceringslogik.

EA Stödjare ska alltså vara en systerprodukt med samma ingenjörsmässiga grundprinciper, inte en variant av ett bokprojekt.

---

## 2. Sammanfattande beslut

| Mekanism i Lärobokskaparen | Beslut för EA Stödjare | Kommentar |
|---|---|---|
| Git-release som versionskälla | Återanvänd direkt | Undviker parallella versionskällor |
| Separat Custom GPT- och portabel chat-distribution | Återanvänd efter anpassning | Mycket relevant när EA Stödjare är mogen för distribution |
| `START-HERE.md` i portabel distribution | Återanvänd efter anpassning | Bra bootstrap för användning av zip i vanlig chat |
| Builder Instructions + separata Knowledge-filer | Återanvänd direkt som arkitekturprincip | Innehållet blir EA-specifikt |
| Maxgräns-/distributionsvalidering | Återanvänd efter anpassning | Kontroller ska spegla EA Stödjares filer och centrala termer |
| Kanonisk projektmall som single source of truth | Återanvänd direkt som princip | Ny mall blir `templates/ea-project/` eller motsvarande |
| `project-manifest.json` | Återanvänd efter anpassning | Införs formellt i steg 7 |
| `revision-log.md` | Återanvänd efter anpassning | Revisionsdisciplinen är direkt relevant |
| SHA-256/integritetskontroll | Återanvänd efter anpassning | Ska skydda modellfiler och projektartefakter |
| Regel: verifiera före och efter filändring | Återanvänd direkt | Viktigt för iterativ zip-baserad utveckling |
| Regel: ändra endast beställda filer | Återanvänd direkt | Minskar oavsiktlig modelldrift |
| Projektstatus | Återanvänd efter anpassning | EA-status behöver öppna frågor, preliminära objekt, konflikter m.m. |
| Canon/terminologi | Återanvänd och förstärk | EA behöver strukturerad modell som främsta canon samt terminologiregler |
| Källpolicy/faktakontroll | Återanvänd och förstärk | Utvecklas till proveniens-, evidens- och researchmodell |
| Kvalitetschecklista | Återanvänd mönstret | Kontrollerna blir semantiska EA-kontroller i stället för bokkvalitet |
| Canonical Markdown-kontrakt | Återanvänd efter anpassning | Markdown är genererad output, inte primär source of truth |
| Lokal Pandoc-baserad export | Återanvänd efter anpassning | DOCX/PDF relevanta; EPUB tas bort |
| GitHub Actions Validate/Preview/Release | Återanvänd efter anpassning | Införs senare enligt planen |
| Reproducerbar build | Återanvänd direkt som princip | Genererade artefakter ska kunna återskapas från modellen |
| Bokprofiler `textbook`/`factbook` | Ej relevant | EA får egen metamodel och arbetslägen |
| `book.yaml` och kapitelordning | Ej relevant | Ersätts av EA-modelldata och relationsmodell |
| Kapitelmallar och pedagogisk progression | Ej relevant | Bokdomänspecifikt |
| Läroboksintervju/bokplan | Ej relevant i formen | Mönstret med plan före större förändring kan återkomma i EA-arbetsflöden |
| Övningar/exempel/kodmappar | Ej relevant som standard | Kan förekomma som källmaterial men är inte projektets kärnstruktur |
| Omslags-/illustrationsflöde | Ej relevant för v1 | Visualisering ligger uttryckligen senare |
| EPUB-export | Ej relevant | EA v1 prioriterar Markdown, Confluence, DOCX och PDF |
| Boktypmönster | Ej relevant | Ersätts av EA-objekttyper och dokumentationsprofiler |

---

# 3. Delar som bör återanvändas direkt som princip

## 3.1 En enda auktoritativ versionskälla

Lärobokskaparen använder en GitHub Release-tagg `v<SemVer>` som auktoritativ distributionsversion och undviker en separat incheckad versionsfil.

Detta bör EA Stödjare återanvända när releaseflödet införs. Fördelarna är:

- ingen versionsdrift mellan filer och release,
- reproducerbara distributioner,
- tydlig koppling mellan Git-historik och paketerad GPT,
- enklare CI-validering.

Det implementeras först i det senare release-steget; steg 2 fastställer endast designbeslutet.

## 3.2 Single source of truth för projektmall

Lärobokskaparen har en faktisk projektmall i repositoryt och genererar portabelt mallinnehåll från den. Det är ett starkt mönster som bör behållas.

För EA Stödjare ska den framtida kanoniska projektmallen innehålla den verkliga EA-projektstrukturen. Dokumentation eller Knowledge som återger mallen ska genereras från denna, inte underhållas parallellt.

Princip:

```text
kanonisk EA-projektmall
        |
        +-- portabel distribution
        +-- Builder Knowledge vid behov
        +-- exempel/dokumentation
```

## 3.3 Kontrollerad filändring

Lärobokskaparens arbetsregel att:

1. välja exakt en projektversion som indata,
2. verifiera den före ändring,
3. arbeta i en ny arbetskatalog,
4. ändra endast filer som uppgiften kräver,
5. skapa nästa revision,
6. paketera hela projektet,
7. verifiera igen,

är direkt relevant för EA Stödjare.

För EA-modeller är detta om möjligt ännu viktigare, eftersom en liten terminologi- eller relationsändring annars kan få stora följdeffekter.

## 3.4 Separera Instructions från detaljerad Knowledge

Lärobokskaparen håller den centrala GPT-instruktionen relativt kompakt och placerar detaljerade regler i Knowledge-filer.

EA Stödjare bör följa samma princip:

- Instructions: roll, prioriteringar, arbetsdisciplin, scope och styrande regler,
- Knowledge: metamodel, klassificeringsguide, relationer, proveniens, research, kvalitet, projektformat, outputprofiler.

Det minskar duplication och gör kunskapsregler enklare att utveckla separat.

## 3.5 Reproducerbarhet före manuellt formaterade artefakter

Lärobokskaparen bygger exportfiler reproducerbart från kanoniskt innehåll. EA Stödjare bör gå längre och låta den strukturerade YAML-modellen vara primär source of truth.

Genererade Markdown-, Confluence-, DOCX- och PDF-filer ska kunna återskapas från modellen och ska inte bli alternativa manuellt underhållna sanningskällor.

---

# 4. Delar som ska återanvändas efter EA-anpassning

## 4.1 Projektmanifest

Lärobokskaparens `project-manifest.json` och integritetsmodell är relevant, men bokfält och kapitelantaganden får inte kopieras.

EA-manifestet bör senare kunna beskriva exempelvis:

- projektnamn och projekt-ID,
- projektformatversion,
- modellversion/metamodel-version,
- revision,
- språk,
- filer som ingår i integritetskontroll,
- SHA-256,
- genereringsstatus,
- eventuella generatorversioner.

Detaljer fastställs i steg 7.

## 4.2 Revision och integritet

SHA-256-skyddet ska återanvändas konceptuellt, men EA-integritetskontrollen behöver förstå andra saker än kapitelnummer.

Framtida EA-validering bör bland annat kunna kontrollera:

- unika objekt-ID:n,
- giltiga referenser,
- inga saknade relationsmål,
- filinventering,
- schemaöverensstämmelse,
- om genererade artefakter är aktuella,
- att en revision inte oavsiktligt ändrat filer utanför beställt scope.

## 4.3 Projektstatus

Lärobokskaparens projektstatus är ett bra mönster för att göra ett zip-projekt självförklarande i en ny chat.

EA-versionen behöver dessutom kunna bära:

- analyserade källor,
- modellens mognadsgrad,
- preliminära objekt,
- öppna klassificeringsfrågor,
- konflikter mellan underlag,
- identifierade luckor,
- rekommenderade nästa steg,
- senaste kvalitetskontroll.

Detta implementeras i steg 8.

## 4.4 Canon och terminologi

Lärobokskaparens `innehalls-canon.md` och `terminologi.md` visar värdet av konsekventa begrepp över ett långt projekt.

För EA Stödjare ska själva YAML-modellen bli den primära informationscanonen. Därutöver behövs regler för:

- auktoritativa namn,
- alias,
- begreppsdefinitioner,
- förkortningar,
- klassificeringsbeslut,
- förbjudna eller utfasade termer.

Terminologin ska inte duplicera själva objektkatalogerna.

## 4.5 Källpolicy och faktakontroll → proveniens och research

Lärobokskaparens källpolicy/faktakontroll bör inte kopieras ordagrant. Den ska utvecklas till en mer strikt EA-modell där varje viktig slutsats kan klassificeras som:

- explicit,
- derived,
- proposed,
- external.

Extern research ska dessutom bedömas utifrån auktoritet, aktualitet, relevans, överförbarhet och potentiell bias.

Detta specificeras i steg 5 och 10.

## 4.6 Kvalitetsgrindar

Mönstret med explicit kvalitetschecklista ska behållas men innehållet bytas ut helt.

EA Stödjare behöver två nivåer:

1. kvalitet för enskilda objekt,
2. kvalitet för modellen som helhet.

Exempel på framtida kontroller är fel abstraktionsnivå, dubbletter, orphaned objects, inkonsekventa relationer och otillräcklig proveniens.

## 4.7 Export och renderingskontrakt

Lärobokskaparen använder canonical Markdown och Pandoc. EA Stödjare bör återanvända det reproducerbara exporttänket men med annan riktning:

```text
YAML -> genererad Markdown -> DOCX/PDF
     -> Confluence markup
```

PDF/Word är distributionsformat; de får inte innehålla unik information som saknas i modellen/genererad dokumentation.

## 4.8 Custom GPT och portabel chat-version

Det är värdefullt att på sikt kunna distribuera EA Stödjare både som:

- Custom GPT-paket,
- portabel chat-zip med `START-HERE.md`.

Den portabla versionen bör kunna användas i en vanlig chat på samma sätt som Lärobokskaparen, men med EA-specifik instruktion, Knowledge och projektmall.

Det införs först när Builder-instruktion och Knowledge har stabiliserats.

---

# 5. Delar som inte ska återanvändas

## 5.1 Bokdomänen

Följande koncept ska inte följa med:

- `book_kind`,
- `book_type`,
- `book.yaml`,
- kapitelnummer som strukturell identitet,
- kapitelordning som exportens kärna,
- läroboks- och faktaboksmallar,
- pedagogisk progression,
- lärandemål,
- övningar och quiz som projektmekanik.

EA Stödjare får i stället en uttrycklig metamodel och relationsmodell.

## 5.2 Bokpublicering

Följande är inte relevanta i v1:

- EPUB,
- EPUB-navigering,
- bokomslag,
- illustration workflow,
- boktypografi och bokunika sidbrytningsregler.

PDF och DOCX återkommer, men då som EA-dokumentexport och inte bokpublicering.

## 5.3 Bokcentrerad projektstruktur

Mappar som `chapters/`, `exercises/` och bokunika metadata ska inte kopieras av historiska skäl.

EA-projektets struktur ska härledas från EA-domänen och fastställs successivt genom steg 3–8.

---

# 6. Föreslagen teknisk arvslinje

EA Stödjare ska inte forka Lärobokskaparen som produktlogik. Den ska återanvända beprövade mönster på följande sätt:

```text
Lärobokskaparen
  |
  +-- versionsprincip -------------------+
  +-- manifest/integritet ---------------+
  +-- revisionsdisciplin ----------------+
  +-- projektstatus ---------------------+
  +-- Builder/Knowledge-separation ------+--> EA Stödjare
  +-- distributionsbygge ----------------+
  +-- CI-validering ---------------------+
  +-- reproducerbar export --------------+
                                          |
EA-specifik design -----------------------+
  +-- EA-metamodell
  +-- EA-relationsmodell
  +-- proveniens/evidens
  +-- researcharbetsflöde
  +-- YAML source of truth
  +-- EA-kvalitetsregler
  +-- EA-dokumentationsprofiler
```

Detta ger gemensamma engineering-principer utan att låsa EA Stödjare till en bokmodell.

---

# 7. Vad som införs redan i steg 2

Steg 2 är ett analys- och designsteg. För att inte föregripa senare steg införs **inte** ännu:

- `project-manifest.json`,
- revisionsscript,
- schemas,
- projektmall,
- Builder-instruktion,
- Knowledge-distribution,
- CI,
- exportscript.

Det som införs nu är i stället:

- denna kanoniska återbruksanalys,
- en teknisk målbild som binder framtida implementationssteg till återbruksbesluten,
- uppdaterad README/status.

Detta följer utvecklingsplanens princip att varje mekanism ska införas först när dess EA-semantik är definierad.

---

# 8. Beslut som senare steg ska respektera

1. **EA-metamodellen får inte formas efter bokprojektets filstruktur.**
2. **YAML blir den planerade informationsmässiga source of truth.**
3. **Git release ska senare vara distributionsversionens auktoritativa källa.**
4. **Projektversioner ska få revisions- och integritetsskydd motsvarande Lärobokskaparen, men EA-anpassat.**
5. **Custom GPT och portabel chat-version ska kunna byggas från samma källor.**
6. **Instructions ska vara kompakta; detaljer ska flyttas till Knowledge.**
7. **Genererade dokument är vyer av modellen och får inte bli parallella sanningskällor.**
8. **Research/proveniens är en starkare förstaklassmekanism i EA Stödjare än vanlig faktakontroll är i Lärobokskaparen.**
9. **EPUB, omslag, illustrationer och pedagogiska bokflöden ska inte följa med.**
10. **Återbruk ska ske medvetet och semantiskt, inte genom blind kopiering av filer.**

---

# 9. Slutsats

Lärobokskaparen är en lämplig teknisk och metodmässig referensimplementation för EA Stödjare. Den mest värdefulla delen är inte bokfunktionerna utan disciplinen kring långlivade AI-projekt: kanon, status, revision, integritet, reproducerbar generering, Builder/Knowledge-separation, validering och release.

EA Stödjare bör bygga vidare på dessa principer men få en helt egen EA-metamodell från steg 3 och framåt.
