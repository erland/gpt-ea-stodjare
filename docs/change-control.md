# Modell- och metamodell-change-control

## Syfte

Change-control skiljer ändringar i **modellinnehåll** från ändringar i **metamodellen**. Governance-artefakterna är styrande för ändringsprocessen men är inte EA-objekt och ersätter inte proveniens i den kanoniska modellen.

## Ändringsklasser

| Klass | Lager | Betydelse |
|---|---|---|
| `editorial` | modell | Form, språk eller presentation utan semantisk ändring. |
| `evidence_update` | modell | Evidens/proveniens ändras men modellpåståendet består. |
| `controlled_model_change` | modell | Kanoniskt innehåll ändras inom samma metamodell. |
| `breaking_model_change` | modell | Stabil modellsemantik, ID-kontrakt eller konsumentkontrakt bryts. |
| `metamodel_change` | metamodell | Objekttyper, attribut, relationstyper, värdemängder eller constraints ändras. |

En ändring som kräver ny objekttyp eller ny relationstyp är alltså **inte** en vanlig modelländring. Den måste först behandlas som `metamodel_change`; därefter kan modellinstanser skapas inom den nya baslinjen.

## Baseline och freeze

`governance/change-control.yaml` deklarerar baseline-ID, baseline-version, modellrevision, metamodellversion och `freeze_status`.

Tillåtna statusar är `draft`, `review`, `frozen`, `reopened`, `retired` och `not_applicable`.

För en `frozen` baseline gäller standardpolicyn:

- `editorial` och `evidence_update` kan registreras utan att baseline öppnas,
- `controlled_model_change`, `breaking_model_change` och `metamodel_change` kräver `reopened` och ny baseline efter godkänd ändring.

Freeze betyder alltså inte att filer aldrig får ändras; den beskriver vilka ändringsklasser som får passera utan explicit baseline-övergång.

## Retired ID-registry

`governance/retired-ids.yaml` använder policyn `retire_never_reuse`.

När ett stabilt ID pensioneras ska det registreras med:

- ID,
- entity kind,
- revision,
- orsak,
- eventuell ersättare,
- change reference.

Ett pensionerat ID får inte återinföras som aktivt kanoniskt ID. Detta gäller även om ett nytt objekt råkar få samma namn eller syfte.

## Två changeloggar

`governance/model-changelog.yaml` accepterar:

- `editorial`,
- `evidence_update`,
- `controlled_model_change`,
- `breaking_model_change`.

`governance/metamodel-changelog.yaml` accepterar endast `metamodel_change`.

Detta gör historiken granskningsbar: en ändring i exempelvis en capability-boundary blandas inte ihop med att Capability-typen får ett nytt fält.

## Epistemisk relation

Change-control ersätter inte source/provenance. En changeloggrad förklarar **att och varför modellen ändrades**; modellens proveniens förklarar **vilket underlag som stöder påståendet**.

## Legacy

Legacy v1-projekt behöver inte materialisera dessa v2-governancefiler för att fortsätta vara redigerbara. Vid migrering kan tidigare change-control rekonstrueras och mappas till v2-formatet. Rev80 används som referens eftersom projektet redan har baseline/freeze och retired-kandidater, men dess historiska filer ändras inte i steg 21.
