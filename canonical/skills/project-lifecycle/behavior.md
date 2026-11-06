## Projektöppning och legacy

När ett projekt tillhandahålls:

1. verifiera integritet när projektet stödjer det,
2. detektera profil: native v2, legacy v1, extended legacy eller unknown,
3. läs `PROJECT_STATUS.md` och relevant projektmetamodell/kompatibilitetsprofil,
4. resolva aktiva extensions och effektiv metamodell för native v2,
5. arbeta först därefter med modellens semantik.

En ogiltig explicit v2-metamodell får inte tyst falla tillbaka till legacy. Ett okänt projekt får inte ges v2-semantik på chans. Legacy v1 ska kunna fortsätta redigeras utan obligatorisk migration. Extended legacy ska behålla projektspecifika konstruktioner tills de kan migreras säkert.

## Migration och change-control

Migration är en explicit, granskningsbar operation – inte global sök/ersätt. Bevara originalet, stabila ID:n, proveniens och informationsinnehåll. Tvetydiga legacyfält/relationer ska bevaras eller markeras för review i stället för att normaliseras utan stöd. Följ projektets migration report och kompatibilitetsregler.

Skilj `editorial`, `evidence_update`, `controlled_model_change`, `breaking_model_change` och `metamodel_change`. Följ baseline/freeze-policy, separera modellchangelog från metamodellchangelog och återanvänd aldrig retired IDs.

## Projektändringar

Vid en sammanhållen projektändring: ändra kanoniska källor först, uppdatera relationer/evidens/governance, kör relevant QA/validering, regenerera derivat, öka projektrevisionen exakt en gång och skriv manifestets inventering/checksummor sist.

