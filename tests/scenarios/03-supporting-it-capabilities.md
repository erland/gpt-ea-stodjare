# Scenario 3: Stödjande IT-område och IT-förmågor

## Syfte

Stresstesta stödjande it-område och it-förmågor mot EA Stödjare v1.

## Syntetiskt underlag

Ett centralt utvecklingsstöd ska möjliggöra att flera operativa utvecklingsområden själva bygger, testar, driftsätter och observerar sina IT-stöd. Underlaget nämner både centralt ansvar och lokala team.

## Förväntat beteende

Modellera stabila behov som IT-förmågor. Använd `owner` för ansvar och `consumer_scope` för vilka utvecklingsområden/målgrupper som förmågan avses betjäna. Introducera inte Organisation som egen kärnobjekttyp. Plattformstjänster kan senare stödja IT-förmågorna.

## Primär risk

Utan konsumentkontext blir det svårt att skilja central IT-förmåga från intern teamaktivitet.

## Bedömning steg 26

**PASS efter designgranskning.** Nuvarande metamodel och arbetsflöden räcker för scenariot; komplettering med `consumer_scope` på Förmåga krävs och är införd i steg 26. Scenariot ska återanvändas vid runtime-test av den faktiska Custom GPT:n före v1.0.0.
