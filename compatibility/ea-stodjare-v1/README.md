# EA Stödjare v1 – legacy-kompatibilitetsprofil

## Syfte

Den här katalogen är en **fryst kompatibilitetssnapshot** av den semantik och de formatkontrakt som användes av EA Stödjare v1. Den finns för att nästa GPT-version ska kunna öppna, förstå och fortsätta arbeta med äldre projekt även när huvudschemana i repositoryt utvecklas till v2.

Profilen är inte v2-standardmetamodellen och ska inte vidareutvecklas genom att följa framtida ändringar i `schemas/`. Om v1-tolkningen måste korrigeras ska det ske som en uttrycklig kompatibilitetsändring med revisionsnotering.

## Maskinläsbar ingång

`profile.yaml` är profilens ingångspunkt. Den innehåller:

- detektionsmarkörer för v1-projekt,
- v1:s fasta modellfilstruktur,
- ID-prefix,
- statusvärden,
- provenienssammanfattning,
- semantiska skyddsregler för kända v1→v2-skillnader,
- redigerings- och migrationspolicy,
- SHA-256 för de frysta schemasnapshottarna.

## Frysta schemas

Under `schemas/` finns kopior av de kontrakt som faktiskt styr v1:

- `object-types.yaml` – objekttyper, attribut, ID-prefix och v1-definitioner,
- `relations.yaml` – relationstyper och tillåtna source/target-kombinationer,
- `provenance.yaml` – evidens, confidence, transferability och källtyper,
- `model-format.yaml` – YAML-envelope, filstruktur, gemensamma fält och embedded Funktion,
- `project-manifest.schema.json` – v1-projektbehållarens manifestkontrakt.

Dessa snapshots ska användas vid legacy-tolkning även när motsvarande filer i repositoryts huvudkatalog senare har v2-semantik.

## Viktiga legacy-skillnader

### Förmåga

V1 tillåter `scope`. Det får inte automatiskt tolkas som v2:s `in_scope` eller `out_of_scope`.

### Plattformstjänst

V1:s definition innehåller formuleringen standardiserat/gemensamt tekniskt erbjudande. Ett omigrerat v1-projekt ska läsas enligt denna definition, inte enligt den senare realiseringsneutrala v2-definitionen.

### Plattform

V1:s Plattform är en gemensam teknisk grund eller sammanhållen teknisk miljö som realiserar eller möjliggör tjänster/funktioner. Den får inte automatiskt tolkas som v2:s konceptuella produktneutrala Plattform.

### `realized_by`

V1 tillåter `Platform Service --realized_by--> Platform`. Den relationen får inte mekaniskt bytas till `provided_by`; semantiken måste granskas vid migration.

### Produkt

Produkt och teknik är uttryckligen utanför v1-kärnan. Ett v1-baserat projekt med en egen produktmodell är därför ett **extended legacy project** och ska inventeras innan v2-semantik appliceras.

### Funktion

Funktion är embedded i IT-stöd, Plattformstjänst och Plattform och har ingen global identitet i v1.

## Arbete utan migration

En v2-GPT ska kunna fortsätta redigera ett v1-projekt i legacy mode. Då ska den:

1. ladda denna profil,
2. respektera v1:s schemas och semantik,
3. inte skriva v2-only-fält i kanoniska v1-filer,
4. bevara stabila ID:n och proveniens,
5. endast föreslå migration när användaren behöver en v2-funktion eller väljer att migrera.

## Extended legacy

Om projektet innehåller supporting-schemas eller egna modellager som inte ingår här ska de **inte** ignoreras. Projektet ska då klassificeras som extended legacy och dess faktiskt använda metamodell rekonstrueras. `it-formagemodell-del3-rev80` är obligatoriskt referenstest för det arbetsläget i v2-planen.
