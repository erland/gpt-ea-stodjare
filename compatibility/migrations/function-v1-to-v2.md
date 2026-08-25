# Migration av embedded Funktion från v1 till v2

Legacy v1-funktioner kan fortsätta användas utan förändring. Native v2 tillför endast valfria lokala ID:n och `required`. Migration ska därför normalt bevara befintliga `name`/`description` och **inte** skapa nya ID:n eller kravmarkeringar automatiskt.

Lokala funktions-ID:n är scoped till moderobjektet och får inte användas som globala EA-ID:n eller relationsmål.
