---
title: "Découvrabilité multilingue pour les sites en anglais uniquement"
category: reference
tags: [seo-marketing, multilingual, hreflang, i18n, llms-txt, schema-org, yandex, baidu, mkdocs, ai-search]
level: 3
source_sha256: 10a42961c5b0bf93fb34746e09bcd7180a8779133ce328cf9af4825afb90ff74
translation: machine
translated_at: '2026-10-24'
---
# Découvrabilité multilingue pour les sites en anglais uniquement {#multilingual-discovery-for-english-only-sites}

Rendre un site statique en anglais uniquement (MkDocs, Hugo, Jekyll sur GitHub Pages) découvrable dans plusieurs langues sans traduction complète. La stratégie consiste à traduire les pages hub et d'accueil pour chaque langue, à conserver les articles en anglais, et à utiliser les métadonnées et les données structurées pour signaler la disponibilité multilingue.

## Chiffres clés {#key-facts}

- Les sites traduits obtiennent 24 % de citations totales en plus et une hausse de visibilité de 327 % inter-langues dans la recherche IA
- ChatGPT utilise des sources anglaises dans 43 % des étapes de recherche non anglophones ; 78 % incluent une recherche complémentaire en anglais
- Les AI Overviews de Google traduisent automatiquement le contenu anglais lorsque les sources locales sont rares (7,9 % pour les requêtes en polonais)
- La traduction complète n'est pas nécessaire : les pages hub et des métadonnées correctes capturent la plus grande part du bénéfice de découvrabilité
- 67 % des implémentations hreflang comportent des erreurs : faites simple, ne sur-ingénierisez pas

## Stratégie : pages hub et articles en anglais {#strategy-hub-pages-english-articles}

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

Les pages hub représentent 10 à 20 pages par langue (index de domaine et page d'accueil principale). Les articles restent en anglais. Cette approche capte le bénéfice de découvrabilité pour environ 5 % du coût d'une traduction complète.

## Plugin mkdocs-static-i18n {#mkdocs-static-i18n-plugin}

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

**Basé sur le suffixe** (`index.ru.md`) contre **basé sur le dossier** (`/ru/index.md`) :

| Approche | Avantages | Inconvénients |
|----------|-----------|---------------|
| Suffixe | Fichiers colocalisés, édition facile | Les URL ressemblent à `/index.ru/` |
| Dossier | URL propres `/ru/`, structure familière | Fichiers dispersés dans plusieurs dossiers |

Avec le thème Material, le sélecteur de langue et les balises hreflang sont générés automatiquement.

## Balises hreflang {#hreflang-tags}

Valides uniquement pour les pages qui disposent réellement de traductions. Elles doivent être bidirectionnelles :

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

**NE PAS ajouter de hreflang aux pages d'articles uniquement en anglais.** Hreflang exige une page correspondante dans la langue cible. Pointer vers la version anglaise depuis elle-même n'a aucun sens.

**Prise en charge par les moteurs :**

| Moteur | Hreflang | Remarques |
|--------|----------|-----------|
| Google | Oui | En-tête HTML + en-tête HTTP + sitemap |
| Yandex | Oui | En-tête HTML uniquement (méthode sitemap abandonnée) |
| Baidu | Non | Utilise la balise `<meta>` de langue à la place |
| Bing | Oui | Identique à Google |

## llms.txt multilingue {#multilingual-llmstxt}

Il n'existe pas encore de spécification formelle pour le llms.txt multilingue. Pratique émergente :

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

Les robots d'IA demandent bien les fichiers llms.txt des sous-répertoires. Aucune entreprise d'IA n'a officiellement confirmé lire llms.txt au moment de l'exploration, mais plus de 844 000 sites l'ont adopté.

## Schema.org pour les sites multilingues {#schemaorg-for-multilingual-sites}

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

Pour les pages hub traduites, créez un lien vers les originaux :

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

**Critique :** un schéma partiel entraîne une pénalité de 18 % sur les citations. N'ajoutez `translationOfWork` / `workTranslation` que si les deux pages existent et sont correctement liées. `availableLanguage` dans le schéma WebSite peut toujours être ajouté sans risque.

## Spécificités des moteurs de recherche {#search-engine-specifics}

### Yandex {#yandex}

- Prend en charge hreflang (en-tête HTML uniquement)
- IndexNow pour une indexation rapide des nouvelles pages
- Meta description en russe obligatoire sur les pages russes
- Inscription dans Yandex Webmaster (gratuit, environ 1 heure de configuration)
- Un sitemap séparé contenant les pages russes aide

### Baidu {#baidu}

- Ne prend PAS en charge hreflang
- Utilise la balise `<meta name="language" content="zh">`
- Fort biais en faveur des contenus hébergés en Chine
- Délai d'indexation de 1 à 3 mois pour les sites non chinois
- Peu fiable pour GitHub Pages : à ignorer sauf si le marché chinois est prioritaire

### Comportement multilingue de la recherche IA {#ai-search-cross-language-behavior}

- **ChatGPT** : 43 % des étapes de recherche non anglophones utilisent des sources anglaises, 78 % les complètent avec de l'anglais
- **Perplexity** : renvoie des URL anglaises même lorsqu'il répond dans une autre langue
- **Google AI Overviews** : 96 % de citations dans la langue correspondante en temps normal, mais traduit l'anglais lorsque le contenu local est rare

Le contenu anglais bénéficie d'un avantage structurel dans la recherche IA : il sert de solution de repli pour toutes les langues.

## Politique de Google pour les contenus mixtes {#google-mixed-language-policy}

- Aucune pénalité pour certaines pages traduites et d'autres non, À CONDITION que chaque page soit dans une seule langue
- Déconseille de ne traduire que la navigation ou le contenu standard
- Les pages hub ont besoin d'un texte traduit substantiel, pas seulement d'éléments de menu
- Utilise le contenu visible (et non l'attribut HTML `lang`) pour détecter la langue
- Chaque URL doit être dans une seule langue cohérente

## Classement coût-bénéfice {#cost-benefit-ranking}

| Action | Effort | Impact | Priorité |
|--------|--------|--------|----------|
| llms.txt multilingue | 4 h + 2 h de relecture par langue | Moyen | 1 |
| Schema.org `availableLanguage` | 30 min | Moyen | 2 |
| Pages hub traduites (par langue) | 2 à 3 jours | Très élevé | 3 |
| Inscription Yandex Webmaster | 1 heure | Élevé (marché russe) | 4 |
| Meta descriptions HTML par langue | 2 h par langue | Moyen | 5 |
| Optimisation Baidu | Plusieurs jours | Faible (GitHub Pages) | Ignorer |

## Pièges à éviter {#gotchas}

- **Les pages hub traduites automatiquement sont signalées** : Google considère le contenu traduit automatiquement sans relecture humaine comme du spam généré automatiquement. Les pages hub doivent être relues par des locuteurs natifs avant publication. Utilisez l'IA pour le premier jet, et un humain pour la relecture finale
- **Un hreflang sans page correspondante échoue silencieusement** : ajouter `hreflang="ru"` vers une page en réalité en anglais brouille les moteurs de recherche. Google l'ignore ; Yandex peut pénaliser. N'ajoutez hreflang que lorsqu'une page traduite existe réellement à cette URL
- **`inLanguage` doit correspondre au contenu réel** : définir `inLanguage: "ru"` sur un article anglais parce qu'il possède une meta description en russe est incorrect. La propriété désigne la langue du contenu principal, et non la langue des métadonnées

## Voir aussi {#see-also}

- [[seo-marketing/llm-discoverability-ai-search]] - principes fondamentaux de l'optimisation pour la recherche IA
- [[seo-marketing/regional-seo]] - optimisation pour les moteurs de recherche régionaux
- [[seo-marketing/robots-txt-sitemaps-indexation]] - contrôle de l'exploration et configuration des sitemaps
- [[seo-marketing/technical-content-seo-strategy]] - architecture de contenu pour la découvrabilité
