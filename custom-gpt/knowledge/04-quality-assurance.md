<!-- GENERERAD FIL: ändra inte manuellt. -->
<!-- Källa: EA Stödjare-projektets kanoniska styrdokument. -->

# Builder Knowledge – Quality Assurance

Denna fil konsoliderar följande kanoniska källor:

- `docs/runtime-quality-contract-v2.md`
- `knowledge/quality-metamodel-aware.md`
- `knowledge/change-control.md`

---


# KÄLLA: `docs/runtime-quality-contract-v2.md`

# Runtimekontrakt – kvalitet v2

QA ska alltid resolveras mot projektets faktiska metamodell. Regler för avaktiverade typer ska inte skapa falska fel; aktiva extensions kan bidra med egna QA-regler.

Kontrollera minst:

- korrekt objekttyp och abstraktionsnivå,
- tydlig boundary och icke-överlappande identitet,
- evidens/proveniens,
- giltiga relationer och kvalificerare,
- epistemisk lagerseparation,
- Product/`can_realize` utan actual-use-felslut,
- `provided_by` som konceptuell hemvist,
- embedded Function utan globala referenser,
- retired IDs,
- derived views/presentation som `source_of_truth: false`,
- change-control vid kanoniska eller metamodellmässiga ändringar.

Strukturvalidatorn är den gemensamma maskinella grinden. Semantiska evaldefinitioner är ett separat LLM-beteendekontrakt och ska inte beskrivas som runtime-godkända förrän svar faktiskt har körts och poängsatts.


# KÄLLA: `knowledge/quality-metamodel-aware.md`

# Metamodellstyrd kvalitet

Innan objekt- eller modellkvalitet bedöms:

1. fastställ projektläge,
2. ladda projektets faktiska metamodell,
3. resolvera aktiva extensions,
4. begränsa QA till aktiva objekt- och relationstyper,
5. inkludera QA-bidrag från aktiva extensions,
6. använd fryst legacyprofil för v1.

Flagga aldrig en medvetet avaktiverad objekttyp som en modellucka. Utgå inte från att standardprofilens fulla lager finns i ett projekts scope.


# KÄLLA: `knowledge/change-control.md`

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
