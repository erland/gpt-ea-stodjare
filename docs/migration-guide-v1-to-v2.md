# Migreringsguide – EA Stödjare v1 till v2

Den här guiden beskriver hur ett befintligt EA Stödjare-projekt ska hanteras i v2. Grundregeln är att **migration är valfri**: ett legitimt v1-projekt kan fortsätta användas under den frysta v1-semantiken.

## 1. Bör jag migrera?

Migrera när projektet behöver v2-funktioner som explicit projektmetamodell, Product/`can_realize`, informationslager, extensions, v2-Plattform/Plattformstjänst, metamodellstyrd QA eller presentation.

Migrera inte enbart för att kunna öppna eller fortsätta redigera ett v1-projekt. V2 har explicit legacy-stöd.

## 2. Säkerhetsprinciper

Migrationen är utformad för att vara:

- **icke-destruktiv** – källprojektet skrivs aldrig över,
- **reproducerbar** – samma källa och regler ger samma semantiska resultat,
- **granskningsbar** – en maskinläsbar migreringsrapport skapas,
- **konservativ** – tvetydig semantik bevaras hellre än gissas,
- **ID-stabil** – stabila ID:n bevaras när objektets betydelse är densamma.

## 3. Fastställ projektprofil först

Kör:

```bash
python3 scripts/detect_project_profile.py --project-root /path/till/projekt
```

Möjliga huvudresultat:

- `native_v2`
- `legacy_v1`
- `extended_legacy`
- `unknown`

Ett `unknown`-projekt ska inte migreras genom antaganden. Projektets struktur/metamodell behöver först rekonstrueras eller deklareras.

## 4. Vanligt v1-projekt

### 4.1 Planera utan att ändra filer

```bash
python3 scripts/migrate_v1_to_v2.py plan \
  --source /path/till/v1-projekt
```

Planen identifierar säkra transformationer och sådant som kräver semantisk review.

### 4.2 Materialisera en separat v2-kopia

```bash
python3 scripts/migrate_v1_to_v2.py apply \
  --source /path/till/v1-projekt \
  --target /path/till/ny-v2-kopia
```

Målkatalogen får inte redan finnas. Källan lämnas orörd.

### 4.3 Validera resultatet

```bash
python3 scripts/validate_project.py \
  --project-root /path/till/ny-v2-kopia \
  --repo-root /path/till/ea-stodjare
```

Granska även `migration/migration-report.yaml`.

## 5. Viktiga semantiska skillnader

### Förmåga: `scope`

V1:s `scope` får **inte** mekaniskt döpas om till `in_scope`. Ett äldre scope kan innehålla både positiv och negativ avgränsning. Tvetydiga fall bevaras och markeras för review.

### Plattformstjänst

V2 definierar Plattformstjänst realiseringsneutralt. Ett v1-objekt behåller sitt ID men dess boundary/definition kan behöva granskas innan man påstår full v2-semantic equivalence.

### Plattform

V2-Plattform är konceptuell och produktneutral. En v1-Plattform ska inte automatiskt bli v2-Plattform om objektet i praktiken beskriver en konkret produkt/runtime.

### `realized_by`

PLS→Plattform `realized_by` får inte globalt sök/ersättas till `provided_by`. Den generella migreringsmotorn bevarar tvetydiga fall som `legacy_realized_by` tills betydelsen verifierats.

### Product och actual state

Marknadsproduktinformation får inte automatiskt bli faktisk organisationsstatus. Product/`can_realize` och `actual-state` är separata informationspåståenden.

## 6. Rev80 / extended legacy

Rev80 föregår det standardiserade v1-manifestet och hanteras med den särskilda extended-legacy-adaptern:

```bash
python3 scripts/migrate_rev80_to_v2.py \
  --source /path/till/rev80 \
  --target /path/till/rev80-v2
```

För den frysta rev80-signaturen är de 92 PLS→PLT-relationerna verifierade som konceptuell hemvist och kan därför migreras till `provided_by`. Supporting-YAML bevaras byte-identiskt där native v2-materialisering annars skulle riskera informationsförlust eller epistemisk omklassificering.

## 7. Efter migration

1. Läs migreringsrapporten.
2. Lös alla poster som kräver semantic review innan de normaliseras.
3. Kontrollera conceptual/market/actual-lager.
4. Kör metamodellstyrd QA.
5. Generera derived views på nytt.
6. Generera Markdown/Confluence/DOCX/PDF från den migrerade modellen.
7. Frys ny baseline först när granskningspunkterna är lösta.

## 8. Rollback

Rollback är normalt trivial eftersom källprojektet aldrig ändras. Om den migrerade kopian inte accepteras kan den tas bort och migrationen köras om med uppdaterade regler eller manuella klassificeringsbeslut.

## 9. Referenser i paketet

- `docs/backward-compatibility-contract.md`
- `docs/v1-to-v2-migration-engine.md`
- `docs/v2-migration-notes.md`
- `docs/minimal-v1-migration-verification.md`
- `docs/rev80-migration-verification.md`
- `compatibility/migration-rules/`
