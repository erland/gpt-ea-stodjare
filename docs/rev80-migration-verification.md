# Rev80 migration och kompatibilitetsverifiering

Steg 24 använder rev80 som extended-legacy stresstest. Projektet föregår det standardiserade `ea-stodjare-project`-manifestet och öppnas därför via en explicit adapter i stället för att låtsas vara ett ordinärt v1-projekt.

## Verifierat normalfall

Källan innehåller 13 IT-förmågor, 10 IT-stöd, 92 Plattformstjänster, 35 konceptuella Plattformar, 385 kanoniska relationer och 14 källor. De 92 `PLS -> PLT realized_by` är enligt rev80-rekonstruktionen entydigt konceptuell hemvist och migreras därför till `provided_by` med oförändrade relations-ID:n och endpoints.

De 55 analytiska relation roles från `supporting/relation-roles.yaml` förs in som relationskvalificerare. Samtliga 92 supporting-YAML bevaras byte-identiskt. Där ingår 295 marknadsprodukter, 295 deploymentposter, 295 opennessposter, produkt–PLS-analyser, maturity-bedömning, derived/query-vyer samt freeze/change-control.

## Epistemisk säkerhet

Marknadsproduktdata flyttas inte automatiskt till faktisk organisationsstatus. Produkt–PLS-realiseringsanalysen är fortsatt marknadspotential, inte bevis på faktisk användning. De tio tidigare Actual Platform-kandidaterna (`PLT-101`–`PLT-110`) förblir pensionerade och får inte återanvändas. Rev80 har fortsatt noll aktiva actual-platform-objekt.

## Extended legacy efter migration

Målet får ett giltigt v2 `project-metamodel.yaml` med `compatibility_mode: extended_legacy`. Det gör att v2 kan använda säker, redan verifierad semantik (`in_scope/out_of_scope`, realiseringsneutral PLS, konceptuell Plattform, `provided_by`) utan att tvinga äldre rev80-konventioner för ID och proveniens genom native-v2-validering.

Följande normalisering skjuts uttryckligen upp: materialisering av marknadsprodukter som native Product-objekt, `can_realize`, deployment/openness/maturity som native extension-attribut, regenerering av derived views och full governance-loggkonvertering. Detta är synligt i migreringsrapporten och räknas inte som dold informationsförlust.
