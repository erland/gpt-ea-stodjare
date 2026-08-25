# Bedömningsrubrik – semantiska evals

## Bedömningsmodell

Varje kriterium i ett evalfall bedöms med 0–2 poäng:

- **2 – uppfyllt:** beteendet är tydligt och korrekt.
- **1 – delvis uppfyllt:** huvudsakligen rätt men med mindre semantisk eller kommunikativ brist.
- **0 – ej uppfyllt:** saknas eller är materiellt fel.

Kriterier kan ha olika vikt. Fallpoängen normaliseras till procent.

## Gemensamma dimensioner

### 1. Klassificering

Bedöm om svaret håller isär metamodelens nivåer och använder rätt objekttyp. Det räcker inte att använda rätt etikett; motiveringen ska också passa definitionen.

### 2. Evidensdisciplin

Bedöm om `explicit`, `derived`, `proposed` och `external` hålls isär. Ett eget förslag får aldrig beskrivas som om det stod i underlaget.

### 3. Osäkerhet

Bedöm om otillräckligt eller motstridigt underlag leder till tydlig osäkerhet i stället för påhittad säkerhet.

### 4. EA-nytta

Bedöm om svaret hjälper användaren framåt: tydliga kandidater, relationer, luckor, alternativ eller nästa verifieringspunkt – inte bara generiska EA-definitioner.

### 5. Scope

Bedöm om svaret håller sig på enterprise architecture-nivå och inte börjar detaljdesigna lösningen när uppgiften inte kräver det.

## Kritiska fel

Följande innebär omedelbart `FAIL` när evalfallet markerar beteendet som kritiskt:

- fabricerad källa eller påstådd research som inte genomförts,
- eget förslag presenteras som explicit organisationsfakta,
- motstridiga källor löses genom att tyst välja en version,
- detaljerad lösningsdesign levereras trots att testet uttryckligen prövar scopegränsen,
- klart felaktig huvudklassificering i ett blockerande klassificeringsfall,
- användarens befintliga kanoniska objekt skrivs över utan att osäkerhet/ändringsbehov hanteras.


## V2-specifika dimensioner

### Projektprofil och faktisk metamodell
Bedöm om svaret först identifierar native v2, legacy v1, extended legacy eller unknown och därefter använder projektets effektiva metamodell.

### Epistemiska lager
Bedöm om conceptual, market/reference och actual organization state hålls isär. Produktpotential eller extern marknadsinformation får inte bli organisationsfakta utan organisationsspecifik evidens.

### Realiseringssemantik
Bedöm om `can_realize`, `provided_by` och legacy `realized_by` används med sina avsedda betydelser. Särskilt tvetydig legacy-semantik måste leda till review, inte global sök/ersätt.

### Härledning och governance
Derived views är `source_of_truth: false`. Metamodelländringar ska hanteras via metamodel change-control och pensionerade ID:n får inte återanvändas.
