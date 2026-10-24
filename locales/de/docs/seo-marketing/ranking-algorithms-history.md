---
title: "Geschichte der Ranking-Algorithmen"
category: concepts
tags: [seo-marketing, algorithms, yandex, google, neural-networks, bert, yati]
level: 3
source_sha256: 88d9fc948e6601fe5439d13a68466b96fabe22efcb89164801ebb0f19ff833a0
translation: machine
translated_at: '2026-10-24'
---
Hmm, that's not right — I'm writing the response now, so let me produce the actual German translation.

---
title: Geschichte der Ranking-Algorithmen
category: concepts
tags: [seo-marketing, algorithms, yandex, google, neural-networks, bert, yati]
---

# Geschichte der Ranking-Algorithmen {#ranking-algorithms-history}

Zeitleiste der wichtigsten Algorithmus-Updates von Suchmaschinen für Yandex und Google, einschließlich der Entwicklung von heuristischem Ranking hin zu neuronalen Netzwerk-basierten Systemen.

## Yandex-Algorithmus-Zeitleiste {#yandex-algorithm-timeline}

| Algorithmus | Jahr | Bedeutung |
|-----------|------|-------------|
| Nepot-Filter | 2005 | Hob das Linkgewicht auf, wenn ein Link als kommerziell/bezahlt eingestuft wurde |
| Magadan | 2008 | Beginn der benannten Algorithmus-Ära; Geo-Abhängigkeit; Erkennung von Texteindeutigkeit |
| ACS-Filter | 2009 | Sanktionen für minderwertige, automatisch generierte Inhalte |
| Snozhinks | 2009 | Matrixnet-ML eingeführt; Texte mit Keyword-Stuffing abgewertet |
| Krasnodor | 2010 | Technologie „Spectrum“: klassifiziert Anfragen nach unterschiedlichen Intents |
| Baden-Baden | 2017 | Abwertung überoptimierter Inhalte mit übermäßiger Keyword-Dichte |
| YATI | 2020 | Transformer-basierte Textanalyse; bedeutende NLP-Verbesserung |
| Y1 | 2021 | Großes Update (+2000 Verbesserungen); Transformer-basiertes YaTI + YaLM |

## Entwicklung der neuronalen Netzwerke bei Yandex {#yandex-neural-network-evolution}

### Vor 2016: Heuristik-Ära {#pre-2016-heuristic-era}
Heuristische Algorithmen, tabellenbasierte Faktoren, ausschließlich inhaltsbasierte Signale.

### 2016–2018: Palekh und Korolev {#2016-2018-palekh-and-korolev}
- Basiert auf dem Deep Structured Semantic Model (DSSM)
- **Palekh**: vergleicht die Anfrage mit dem Dokumenttitel
- **Korolev**: erweitert auf den Vergleich mit dem gesamten Seiteninhalt; Bewertungen von Assessoren integriert

### 2019: Neuronale Netzwerke auf Basis von Expertenbewertungen {#2019-expert-assessment-neural-networks}
Trainingsziele auf Grundlage von Expertenbewertungen der Qualität.

### 2020+: YATI (Yandex Attention to Intent) {#2020-yati-yandex-attention-to-intent}
- Transformer-Architektur
- Mehrere Streams: Ankertext-Liste, klickbasierter URL-Index
- Größere Textbetrachtung: Texte mit bis zu 10 Sätzen werden vollständig verarbeitet
- Wortvektorraum für semantisches Verständnis

### Yandex Proxima (Qualitätsmetrik) {#yandex-proxima-quality-metric}
Kombiniert kommerzielle, Konversions- und Expertensignale:
- Komponenten kommerzieller Qualität
- Domänenspezifische Qualität (Medizin, Recht, Finanzen)
- Signale zum Nutzerwert: Expertise, Autorität, Vertrauenswürdigkeit

## Google-Algorithmus-Zeitleiste {#google-algorithm-timeline}

| Algorithmus | Jahr | Bedeutung |
|-----------|------|-------------|
| Panda | 2011 | Abwertung dünner/doppelter/minderwertiger Inhalte; betraf 12 % der Ergebnisse |
| Penguin | 2012 | Abwertung von Spam-Links, Linkfarmen, gekauften Linkschemata |
| Hummingbird | 2012 | Semantisches Verständnis von Anfragen; Kontext > einzelne Keywords |
| RankBrain | 2015 | ML-Komponente; relevante Seiten nach Bedeutung ohne exakte Übereinstimmung |
| Mobile-Friendly | 2015 | Mobiloptimierte Seiten erhalten Priorität in der mobilen Suche |
| Mobile-First Index | 2018 | Mobile Version wird als primäre Version für die Indexierung verwendet |
| BERT | 2019 | Bidirektionale Kontextanalyse; Präpositionen und Bedeutung des ganzen Satzes |
| Core Web Vitals | 2020 | LCP, FID/INP, CLS als Ranking-Signale |

## Google-E-E-A-T-Framework {#google-e-e-a-t-framework}

Ursprünglich E-A-T, erweitert zu E-E-A-T:
- **E (Experience)** - direkte Erfahrung aus erster Hand mit dem Thema
- **E (Expertise)** - Fachwissen auf Expertenniveau zum Thema
- **A (Authoritativeness)** - Autorität von Autor und Website in der Nische
- **T (Trustworthiness)** - Zuverlässigkeit der Website: qualitativ hochwertige Inhalte, vollständige Kontaktangaben, Zahlungs- und Lieferinformationen

YMYL-Websites (Gesundheit, Finanzen, Recht, Sicherheit) unterliegen seit 2018 den strengsten E-E-A-T-Anforderungen.

## Google BERT (2019) {#google-bert-2019}

Bidirectional Encoder Representations from Transformers: verarbeitet den Anfragekontext einschließlich Präpositionen und des gesamten Satzes, nicht nur einzelne Keywords. Markiert den Wandel vom Keyword-Matching hin zum semantischen Verständnis.

## Wichtige Fakten {#key-facts}
- Yandex verwendet mehr als 2000 Ranking-Faktoren
- Die Algorithmus-Updates von Google zielen zunehmend auf Inhaltsqualität und Nutzerintention ab
- Beide Suchmaschinen haben sich auf Transformer-basierte Architekturen für semantisches Verständnis konvergiert
- YMYL-Nischen unterliegen auf beiden Plattformen den strengsten Qualitätsanforderungen

## Fallstricke {#gotchas}
- **Algorithmennamen sind für die Diagnose wichtig** - wenn der Traffic einbricht, ist das zeitliche Abgleichen mit bekannten Algorithmus-Rollouts der schnellste Weg, die Ursache zu finden
- **YATI hat für Yandex alles verändert** - Empfehlungen zur Textoptimierung für Yandex aus der Zeit vor 2020 sind weitgehend veraltet
- **E-E-A-T ist kein direkter Ranking-Faktor** - es ist ein Qualitätsrahmen für menschliche Assessoren, deren Bewertungen die Algorithmen trainieren
- **Mobile-First bedeutet, dass Mobil DER Index ist** - Inhalte, die nur auf dem Desktop sichtbar sind und in der mobilen Version fehlen, werden möglicherweise gar nicht indexiert

## Siehe auch {#see-also}
- [[search-engine-mechanics]] - Gruppen der Ranking-Faktoren
- [[filters-and-penalties]] - Spezifische Penalty-Algorithmen
- [[commercial-ranking-factors]] - Details zu E-A-T und kommerziellen Faktoren
- [[text-optimization]] - Wie die Bewertung der Textrelevanz funktioniert
