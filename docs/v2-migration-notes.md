# V2 migration notes


## Steg 12 – relationskvalificerare

Legacy v1-relationer förblir giltiga utan de nya v2-kvalificerarna. Migration får inte fabricera `relation_role`, `strength`, `mandatory`, `verification_status` eller `boundary_basis` när underlaget inte stödjer dem. Rev80:s projektspecifika `relation_role` kan vid kontrollerad migration mappas till v2-fältet när värdet och relationens semantik är förenliga. Kvalificerare kompletterar relationen; de får inte användas för att maskera att fel relationstyp valts.
