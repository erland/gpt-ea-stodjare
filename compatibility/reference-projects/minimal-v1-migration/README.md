# Minimal v1 → v2 migration reference

Detta är regressionsbaslinjen för v2 steg 23. Själva v1-källprojektet ligger kvar i `examples/minimal-model/`; någon statisk kopia av det migrerade projektet checkas inte in eftersom migrationsmotorn ska bevisa att resultatet kan reproduceras.

`verification-baseline.yaml` anger de stabila ID:n, antalen och den enda avsiktliga relationstransformationen i normalfallet. `REL-006` bevaras efter migration som `legacy_realized_by` tills dess innebörd har granskats. Vid semantisk ekvivalenskontroll normaliseras denna deklarerade legacy-kod tillbaka till v1-betydelsen `realized_by`; övriga modellposter ska vara oförändrade.

End-to-end-verifieringen körs av `scripts/verify_v1_v2_migration.py` och regressionstestet `tests/compatibility/test_minimal_v1_migration_e2e.py`.
