---
title: "Mehrsprachige Auffindbarkeit für rein englischsprachige Websites"
category: reference
tags: [seo-marketing, multilingual, hreflang, i18n, llms-txt, schema-org, yandex, baidu, mkdocs, ai-search]
level: 3
source_sha256: 10a42961c5b0bf93fb34746e09bcd7180a8779133ce328cf9af4825afb90ff74
translation: machine
translated_at: '2026-10-24'
---
# Mehrsprachige Auffindbarkeit für rein englischsprachige Websites {#multilingual-discovery-for-english-only-sites}

Eine rein englischsprachige statische Website (MkDocs, Hugo, Jekyll auf GitHub Pages) in mehreren Sprachen auffindbar machen, ohne vollständige Übersetzung. Die Strategie: Hub- und Landingpages pro Sprache übersetzen, Artikel auf Englisch belassen und Metadaten sowie strukturierte Daten nutzen, um die mehrsprachige Verfügbarkeit zu signalisieren.

## Kernfakten {#key-facts}

- Übersetzte Websites erhalten 24 % mehr Zitierungen insgesamt und eine 327 % höhere sprachübergreifende Sichtbarkeit in der KI-Suche
- ChatGPT nutzt englische Quellen in 43 % der nicht-englischen Recherchschritte; 78 % enthalten zusätzliche englische Suche
- Google AI Overviews übersetzen englische Inhalte automatisch, wenn lokale Quellen spärlich sind (7,9 % bei polnischen Suchanfragen)
- Vollständige Übersetzung ist nicht notwendig: Hub-Seiten und saubere Metadaten erschließen den größten Teil des Auffindbarkeitsnutzens
- 67 % der Hreflang-Implementierungen enthalten Fehler. Halte es einfach und übertechnisiere nicht

## Strategie: Hub-Seiten und englische Artikel {#strategy-hub-pages-english-articles}

```text
docs/
  index.md              # English hub (default)
  index.ru.md           # Russian hub page (translated)
  index.zh.md           # Chinese hub page (translated)
  kafka/
    consumer-groups.md  # English article (stays English)
    index.md            # English domain index
    index.ru.md         # Russian domain index (translated)
```

Hub-Seiten sind 10–20 pro Sprache (Domain-Indexseiten und Hauptlandingpage). Artikel bleiben englisch. So wird der Auffindbarkeitsnutzen zu etwa 5 % der Kosten einer vollständigen Übersetzung erreicht.

## mkdocs-static-i18n-Plugin {#mkdocs-static-i18n-plugin}

```yaml
# mkdocs.yml
plugins:
  - i18n:
      default_language: en
      languages:
        - locale: en
          name: English
          default: true
        - locale: ru
          name: Russian
          build: true
        - locale: zh
          name: Chinese
          build: true
      fallback_to_default: true  # untranslated pages fall back to English
```

**Suffixbasiert** (`index.ru.md`) vs. **ordnerbasiert** (`/ru/index.md`):

| Ansatz | Vorteile | Nachteile |
|--------|----------|-----------|
| Suffix | Dateien liegen beieinander, einfach zu bearbeiten | URLs sehen aus wie `/index.ru/` |
| Ordner | Saubere URLs `/ru/`, vertraute Struktur | Dateien sind über Ordner verteilt |

Mit dem Material-Theme werden Sprachauswahl und Hreflang-Tags automatisch erzeugt.

## Hreflang-Tags {#hreflang-tags}

Nur gültig für Seiten, die tatsächlich Übersetzungen haben. Die Verknüpfung muss bidirektional sein:

```html
<!-- On English hub page -->
<link rel="alternate" hreflang="en" href="https://site.com/" />
<link rel="alternate" hreflang="ru" href="https://site.com/ru/" />
<link rel="alternate" hreflang="x-default" href="https://site.com/" />

<!-- On Russian hub page -->
<link rel="alternate" hreflang="en" href="https://site.com/" />
<link rel="alternate" hreflang="ru" href="https://site.com/ru/" />
<link rel="alternate" hreflang="x-default" href="https://site.com/" />
```

**Füge hreflang NICHT zu rein englischen Artikelseiten hinzu.** Hreflang setzt eine entsprechende Seite in der Zielsprache voraus. Auf die englische Version von der eigenen Seite aus zu verweisen, ist bedeutungslos.

**Unterstützung durch Suchmaschinen:**

| Suchmaschine | Hreflang | Hinweise |
|--------------|----------|----------|
| Google | Ja | HTML-Head + HTTP-Header + Sitemap |
| Yandex | Ja | Nur HTML-Head (Sitemap-Methode entfernt) |
| Baidu | Nein | Verwendet stattdessen das `<meta>`-Sprach-Tag |
| Bing | Ja | Wie Google |

## Mehrsprachige llms.txt {#multilingual-llmstxt}

Für mehrsprachige llms.txt gibt es noch keine formale Spezifikation. Etablierte Praxis:

```text
/llms.txt           # English (default), serves as index
/ru/llms.txt        # Russian language version
/zh/llms.txt        # Chinese language version
```

```markdown
# Knowledge Base (Russian Index)

> Техническая база знаний: Kafka, Python, Rust, SQL, DevOps

## Основные темы
- [Kafka Consumer Groups](https://site.com/kafka/consumer-groups/): Партиции, оффсеты, ребалансировка
- [Python Async](https://site.com/python/async/): asyncio, aiohttp, паттерны

## О базе знаний
Статьи на английском языке. Эта страница помогает найти нужный контент.
```

KI-Bots fragen tatsächlich Unterverzeichnis-llms.txt-Dateien ab. Kein KI-Unternehmen liest llms.txt nachweislich offiziell zur Crawl-Zeit, dennoch haben über 844.000 Websites sie übernommen.

## Schema.org für mehrsprachige Websites {#schemaorg-for-multilingual-sites}

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "url": "https://site.com",
  "inLanguage": "en",
  "availableLanguage": ["en", "ru", "zh"],
  "name": "Knowledge Base"
}
```

Für übersetzte Hub-Seiten verlinke auf die Originale:

```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "url": "https://site.com/ru/",
  "inLanguage": "ru",
  "translationOfWork": {
    "@type": "WebPage",
    "url": "https://site.com/"
  }
}
```

**Kritisch:** Unvollständiges Schema bedeutet einen Zitierungsabzug von 18 %. Füge `translationOfWork` / `workTranslation` nur hinzu, wenn beide Seiten existieren und korrekt verlinkt sind. `availableLanguage` im WebSite-Schema kann dagegen immer ergänzt werden.

## Besonderheiten einzelner Suchmaschinen {#search-engine-specifics}

### Yandex {#yandex}

- Unterstützt Hreflang (nur HTML-Head)
- IndexNow für schnelle Indexierung neuer Seiten
- Russische Meta-Description auf russischen Seiten erforderlich
- Registrierung in Yandex Webmaster (kostenlos, ca. 1 Stunde Einrichtung)
- Separate Sitemap mit russischen Seiten hilft

### Baidu {#baidu}

- Unterstützt Hreflang NICHT
- Verwendet das Tag `<meta name="language" content="zh">`
- Starke Bevorzugung chinesisch gehosteter Inhalte
- 1–3 Monate Indexierungsverzögerung für nicht-chinesische Websites
- Auf GitHub Pages unzuverlässig. Überspringen, außer der chinesische Markt ist primär

### Sprachübergreifendes Verhalten in der KI-Suche {#ai-search-cross-language-behavior}

- **ChatGPT**: 43 % der nicht-englischen Recherchschritte nutzen englische Quellen, 78 % ergänzen mit Englisch
- **Perplexity**: liefert englische URLs, auch wenn in anderen Sprachen geantwortet wird
- **Google AI Overviews**: normalerweise 96 % sprachpassende Zitierungen, übersetzt aber Englisch, wenn lokale Inhalte spärlich sind

Englische Inhalte haben in der KI-Suche einen strukturellen Vorteil, denn sie sind der Fallback für alle Sprachen.

## Googles Richtlinie für gemischtsprachige Websites {#google-mixed-language-policy}

- Keine Strafe dafür, dass einige Seiten übersetzt und andere nicht sind, SOFERN jede Seite genau eine Sprache hat
- Warnt davor, nur Navigation oder Boilerplate zu übersetzen
- Hub-Seiten brauchen substanziellen übersetzten Text, nicht nur Menüpunkte
- Für die Spracherkennung wird der sichtbare Inhalt verwendet, nicht das HTML-Attribut `lang`
- Jede URL muss durchgehend in einer Sprache sein

## Kosten-Nutzen-Rangfolge {#cost-benefit-ranking}

| Maßnahme | Aufwand | Wirkung | Priorität |
|----------|---------|---------|-----------|
| Mehrsprachige llms.txt | 4 h + 2 h Prüfung pro Sprache | Mittel | 1 |
| Schema.org `availableLanguage` | 30 Min. | Mittel | 2 |
| Übersetzte Hub-Seiten (pro Sprache) | 2–3 Tage | Sehr hoch | 3 |
| Registrierung bei Yandex Webmaster | 1 Stunde | Hoch (russischer Markt) | 4 |
| HTML-Meta-Descriptions pro Sprache | 2 h pro Sprache | Mittel | 5 |
| Baidu-Optimierung | Tage | Gering (GitHub Pages) | Überspringen |

## Gotchas {#gotchas}

- **Maschinell übersetzte Hub-Seiten werden markiert.** Google stuft maschinell übersetzte Inhalte ohne menschliche Prüfung als automatisch erzeugten Spam ein. Hub-Seiten müssen vor der Veröffentlichung von Muttersprachlern geprüft werden. Nutze KI für den ersten Entwurf und Menschen für die finale Prüfung
- **Hreflang ohne passende Seiten versagt stillschweigend.** Wenn `hreflang="ru"` auf eine Seite verweist, die tatsächlich auf Englisch ist, verwirrt das Suchmaschinen. Google ignoriert es, Yandex kann bestrafen. Füge hreflang nur hinzu, wenn unter dieser URL tatsächlich eine übersetzte Seite existiert
- **`inLanguage` muss dem tatsächlichen Inhalt entsprechen.** Die Angabe `inLanguage: "ru"` bei einem englischen Artikel, weil er eine russische Meta-Description hat, ist falsch. Die Eigenschaft bezieht sich auf die primäre Inhaltssprache, nicht auf die Metadatensprache

## Siehe auch {#see-also}

- [[seo-marketing/llm-discoverability-ai-search]] - Grundlagen der Optimierung für die KI-Suche
- [[seo-marketing/regional-seo]] - regionale Suchmaschinenoptimierung
- [[seo-marketing/robots-txt-sitemaps-indexation]] - Crawl-Steuerung und Sitemap-Konfiguration
- [[seo-marketing/technical-content-seo-strategy]] - Content-Architektur für Auffindbarkeit
