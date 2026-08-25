# Migration – Plattformstjänst v1 till v2

V2 gör Plattformstjänst realiseringsneutral. Ett legacy v1-objekt är fortfarande läsbart och får fortsätta användas utan migration.

Vid kontrollerad migration behålls stabilt ID och befintlig information när objektets semantiska identitet är densamma. Formuleringar som antyder att PLS **måste** vara en gemensam eller centralt driftad runtime ska granskas. De får bara justeras redaktionellt när avsikten kan fastställas utan ny arkitekturslutsats.

`realization_pattern` är valfritt och får inte fyllas genom gissning. Marknadskapacitet, faktisk produktanvändning och faktisk organisatorisk realisering är separata påståenden.
