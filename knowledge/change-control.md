# Change-control – arbetsregel

Vid ändring av ett v2-projekt:

1. Klassificera först ändringen som `editorial`, `evidence_update`, `controlled_model_change`, `breaking_model_change` eller `metamodel_change`.
2. Ändras objekttyper, fält, relationstyper, värdemängder eller constraints ska ändringen vara `metamodel_change`.
3. Kontrollera baseline och freeze-status innan kanonisk mutation.
4. På fryst baseline kräver kontrollerad, breaking eller metamodelländring reopen och ny baseline.
5. Pensionerade ID:n registreras och får aldrig återanvändas.
6. Modelländringar skrivs i modellchangelog; metamodelländringar i metamodellchangelog.
7. Changelog ersätter aldrig evidens/proveniens.
8. Automatisera inte split, merge, retire eller ID-byte enbart utifrån ett review-resultat.
