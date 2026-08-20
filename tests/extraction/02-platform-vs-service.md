# Test 02 – Plattformstjänst kontra Plattform

## Syntetiskt underlag

> Utvecklingsteamen beställer Containerplattform som tjänst via tjänstekatalogen. Tjänsten realiseras idag av organisationens OpenShift-kluster och omfattar bland annat körning av containrar, konfigurationshantering och autoskalning.

## Förväntat analysbeteende

- **Plattformstjänst**: Containerplattform som tjänst. Proveniens: `explicit`.
- **Plattform**: OpenShift-kluster. Proveniens: `explicit`.
- `realized_by` från Plattformstjänst till Plattform är rimlig och explicit belagd.
- Funktionerna "körning av containrar", "konfigurationshantering" och "autoskalning" kan dokumenteras på Plattformstjänsten och/eller Plattformen beroende på vad texten faktiskt tillskriver respektive nivå.
- OpenShift ska inte automatiskt slås ihop med tjänsten till ett enda objekt.
