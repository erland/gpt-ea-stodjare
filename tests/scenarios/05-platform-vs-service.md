# Scenario 5: Plattform kontra Plattformstjänst

## Syfte

Stresstesta plattform kontra plattformstjänst mot EA Stödjare v1.

## Syntetiskt underlag

Underlaget använder “plattform” för både OpenShift-miljön, det interna erbjudandet “Containerplattform”, Kubernetes och en katalogpost med SLA/anslutningsvillkor.

## Förväntat beteende

Separera konsumtionsbart erbjudande (Plattformstjänst) från teknisk realiseringsgrund (Plattform). Produkt/teknik kan vara attribut på Plattform. Om underlaget är tvetydigt ska kandidaten hållas osäker.

## Primär risk

Risk för dubbla objekt med samma namn men olika semantik.

## Bedömning steg 26

**PASS efter designgranskning.** Nuvarande metamodel och arbetsflöden räcker för scenariot. Scenariot ska återanvändas vid runtime-test av den faktiska Custom GPT:n före v1.0.0.
