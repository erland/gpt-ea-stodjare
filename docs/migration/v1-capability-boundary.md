# Migreringsregel – Förmågeboundary v1 → v2

V1 tillåter det generella attributet `scope`. Native v2 använder i stället `in_scope`, `out_of_scope` och `consumer_scope`.

`scope` får **inte** rutinmässigt byta namn till `in_scope`: källtexten kan innehålla positiv boundary, negativ boundary eller båda.

- Entydigt positiv text kan föreslås som `in_scope`.
- Entydigt negativ text kan föreslås som `out_of_scope`.
- Blandad eller tvetydig text bevaras som legacy tills kontrollerad migration.
- `consumer_scope` bevaras oförändrat när semantiken är densamma.
- Stabilt CAP-ID bevaras när semantisk identitet är oförändrad.

För `capability_type: it` ska migrerat `in_scope` dessutom granskas så att det uttrycker tekniskt möjliggörande och inte produktinventering, Plattformstjänstlista eller verksamhetsfunktionalitet som IT sägs utföra.

Maskinläsbar regel: `compatibility/migration-rules/v1-to-v2-capability-boundary.yaml`.
