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
