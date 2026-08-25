# End-to-end-verifiering av minimal v1 → v2-migration

## Syfte

Steg 23 verifierar migrationsmotorns normalfall mot det minimala v1-referensprojektet i `examples/minimal-model/`. Testet ska visa att migrationen är reproducerbar och att informations- och läsarseman­tik bevaras även när v2 behöver lägga ett legacy-lager runt en tvetydig relation.

## Verifieringskedja

1. Kör migrationsmotorn i `plan` och kontrollera determinism och icke-destruktivitet.
2. Kör `apply` till en ny katalog.
3. Validera den migrerade v2-kopian.
4. Jämför stabila objekt-, relations- och käll-ID:n.
5. Jämför samtliga objektposter och deras proveniens exakt.
6. Jämför källregistret exakt.
7. Jämför relationer exakt efter endast deklarerad legacy-normalisering (`legacy_realized_by` → v1-betydelsen `realized_by`).
8. Regenerera Markdown och Confluence från både v1-källan och v2-målet och jämför semantiskt efter normalisering av projektrevision och deklarerad legacy-kod.
9. Regenerera DOCX och PDF för både källa och mål.

## Avsiktlig skillnad

`REL-006` (`PLS-001 → PLT-001`) kan inte automatiskt avgöras vara native-v2 `provided_by`. Migrationen behåller därför relations-ID, endpoints, status och proveniens men använder den temporära typen `legacy_realized_by`. Dokumentgeneratorerna visar relationen med läsaretiketten **Realiseras av/Realiserar**, så den gamla läsarseman­tiken förloras inte under granskningsfasen.

`REL-011` är också `realized_by`, men mellan Referensarkitektur och Lösningsmönster. Den relationen är inte PLS→Plattform och lämnas därför oförändrad.

## Godkännandekriterium

Migrationen är godkänd när samtliga maskinläsbara checks i `scripts/verify_v1_v2_migration.py` är `true` och den migrerade kopian validerar utan strukturella fel.
