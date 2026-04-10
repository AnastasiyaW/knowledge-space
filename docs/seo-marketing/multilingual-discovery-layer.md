---
title: Multilingual Discovery for English-Only Sites
category: reference
tags: [seo-marketing, multilingual, hreflang, i18n, llms-txt, schema-org, yandex, baidu, mkdocs, ai-search]
---

# Multilingual Discovery for English-Only Sites

Making an English-only static site (MkDocs, Hugo, Jekyll on GitHub Pages) discoverable in multiple languages without full translation. The strategy: translate hub/landing pages per language, keep articles in English, use metadata and structured data to signal multilingual availability.

## Key Facts

- Translated sites get 24% more total citations and 327% visibility boost cross-language in AI search
- ChatGPT uses English sources in 43% of non-English research steps; 78% include supplementary English search
- Google AI Overviews auto-translate English content when local sources are sparse (7.9% for Polish queries)
- Full translation is unnecessary - hub pages + proper metadata capture most of the discovery benefit
- 67% of hreflang implementations have errors - keep it simple, don't over-engineer

## Strategy: Hub Pages + English Articles

```
docs/
  index.md              # English hub (default)
  index.ru.md           # Russian hub page (translated)
  index.zh.md           # Chinese hub page (translated)
  kafka/
    consumer-groups.md  # English article (stays English)
    index.md            # English domain index
    index.ru.md         # Russian domain index (translated)
```

Hub pages are 10-20 per language (domain indexes + main landing). Articles stay English. This captures discovery benefit at ~5% of full translation cost.

## mkdocs-static-i18n Plugin

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

**Suffix-based** (`index.ru.md`) vs **folder-based** (`/ru/index.md`):

| Approach | Pros | Cons |
|----------|------|------|
| Suffix | Files colocated, easy editing | URLs look like `/index.ru/` |
| Folder | Clean URLs `/ru/`, familiar structure | Files scattered across folders |

With Material theme, the language selector and hreflang tags generate automatically.

## Hreflang Tags

Only valid for pages that actually have translations. Must be bidirectional:

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

**Do NOT add hreflang to English-only article pages.** Hreflang requires a corresponding page in the target language. Pointing to the English version from itself is meaningless.

**Engine support:**

| Engine | Hreflang | Notes |
|--------|----------|-------|
| Google | Yes | HTML head + HTTP header + sitemap |
| Yandex | Yes | HTML head only (dropped sitemap method) |
| Baidu | No | Uses `<meta>` language tag instead |
| Bing | Yes | Same as Google |

## Multilingual llms.txt

No formal spec for multilingual llms.txt yet. Emerging practice:

```
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

AI bots DO request subdirectory llms.txt files. No confirmed AI company officially reads llms.txt at crawl time, but 844K+ sites have adopted it.

## Schema.org for Multilingual Sites

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

For translated hub pages, link to originals:

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

**Critical:** partial schema = 18% citation penalty. Only add `translationOfWork` / `workTranslation` if both pages exist and are properly linked. `availableLanguage` on the WebSite schema is safe to add always.

## Search Engine Specifics

### Yandex

- Supports hreflang (HTML head only)
- IndexNow for fast indexing of new pages
- Russian meta description required on Russian pages
- Register in Yandex Webmaster (free, ~1 hour setup)
- Separate sitemap with Russian pages helps

### Baidu

- Does NOT support hreflang
- Uses `<meta name="language" content="zh">` tag
- Strong bias toward Chinese-hosted content
- 1-3 month indexing delay for non-Chinese sites
- Unreliable for GitHub Pages - skip unless Chinese market is primary

### AI Search Cross-Language Behavior

- **ChatGPT**: 43% of non-English research steps use English sources, 78% supplement with English
- **Perplexity**: returns English URLs even when answering in other languages
- **Google AI Overviews**: 96% language-matched citations normally, but auto-translates English when local content is sparse

English content has a structural advantage in AI search - it's the fallback for all languages.

## Google Mixed-Language Policy

- No penalty for having some pages translated and others not, IF each page is one language
- Warns against translating only navigation/boilerplate
- Hub pages need substantial translated text, not just menu items
- Uses visible content (not HTML `lang` attribute) for language detection
- Each URL must be one consistent language

## Cost-Benefit Ranking

| Action | Effort | Impact | Priority |
|--------|--------|--------|----------|
| Multilingual llms.txt | 4h + 2h review per language | Medium | 1 |
| Schema.org `availableLanguage` | 30 min | Medium | 2 |
| Translated hub pages (per language) | 2-3 days | Very high | 3 |
| Yandex Webmaster registration | 1 hour | High (RU market) | 4 |
| HTML meta descriptions per language | 2h per language | Medium | 5 |
| Baidu optimization | Days | Low (GitHub Pages) | Skip |

## Gotchas

- **Machine-translated hub pages get flagged** - Google flags machine-translated content without human review as auto-generated spam. Hub pages must be reviewed by native speakers before publishing. Use AI for first draft, human for final review
- **Hreflang without matching pages breaks silently** - adding `hreflang="ru"` pointing to a page that's actually in English confuses search engines. Google ignores it; Yandex may penalize. Only add hreflang when a real translated page exists at that URL
- **`inLanguage` must match actual content** - setting `inLanguage: "ru"` on an English article because it has a Russian meta description is incorrect. The property refers to the primary content language, not metadata language

## See Also

- [[seo-marketing/llm-discoverability-ai-search]] - AI search optimization fundamentals
- [[seo-marketing/regional-seo]] - regional search engine optimization
- [[seo-marketing/robots-txt-sitemaps-indexation]] - crawl control and sitemap configuration
- [[seo-marketing/technical-content-seo-strategy]] - content architecture for discovery
