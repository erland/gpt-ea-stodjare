# Scenario 9: Befintlig modell med dubbletter och fel nivåer

## Syfte

Stresstesta befintlig modell med dubbletter och fel nivåer mot EA Stödjare v1.

## Syntetiskt underlag

En capability-katalog innehåller “CI/CD”, “Jenkins”, “Bygga kod”, “Programvaruutveckling”, “OpenShift” och “Driftsätta applikationer” som jämbördiga förmågor.

## Förväntat beteende

Identifiera Jenkins/OpenShift som produkt/plattformsrelaterade kandidater snarare än förmågor, bedöm CI/CD som sammansatt/oklar term, normalisera capability-nivå och föreslå merge/split utan att automatiskt skriva om godkända objekt.

## Primär risk

Risk för överaggressiv normalisering och förlorad historik.

## Bedömning steg 26

**PASS efter designgranskning.** Nuvarande metamodel och arbetsflöden räcker för scenariot. Scenariot ska återanvändas vid runtime-test av den faktiska Custom GPT:n före v1.0.0.
