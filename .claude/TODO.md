# Happyin Knowledge Space - TODO

## Срочно (верифицировать после деплоя)

- [ ] **robots.txt на проде** - проверить что отдаётся НАШ файл, а не Cloudflare дефолт. Если нет - добавить `_headers` или Cloudflare Pages redirect rule
- [ ] **llms.txt на проде** - должен отдавать plain text, не HTML
- [ ] **Gradient border** - snippet card рамочка с анимацией, проверить визуально
- [ ] **Contributor cards** - LinkedIn иконки рядом с именами, не развалены
- [ ] **For LLM Agents** - страница в сайдбаре, перед Algorithms

## SEO - состояние

### Готово
- [x] `sitemap.xml` - генерируется MkDocs, содержит все 560+ страниц
- [x] `robots.txt` - разрешает поисковые + AI-краулеры, блокирует training (GPTBot, Google-Extended, CCBot)
- [x] `llms.txt` на 6 языках (EN/ZH/KO/ES/DE/FR) - для LLM discoverability
- [x] JSON-LD: WebSite schema на главной + TechArticle на статьях с description
- [x] OG tags: og:type, og:title, og:description, og:url, og:site_name
- [x] Twitter Card: summary_large_image
- [x] `availableLanguage` в WebSite schema (6 языков)
- [x] `privacy` plugin - внешние ресурсы (шрифты) скачиваются локально
- [x] `minify` plugin - HTML минификация
- [x] IndexNow workflow - уведомляет поисковики при пуше

### Не готово
- [ ] **Google Search Console** - нужна регистрация вручную
- [ ] **Bing Webmaster Tools** - нужна регистрация
- [ ] **IndexNow key** - сгенерировать на bing.com/indexnow, добавить `INDEXNOW_KEY` secret
- [ ] **Description frontmatter** - у 10 sample-статей нет `description` → TechArticle JSON-LD не рендерится
- [ ] **Favicon** - дефолтный MkDocs, нужен кастомный
- [ ] **OG image** - нет og:image для шаринга в соцсетях
- [ ] **About page** - E-E-A-T сигнал (автор + Person schema)
- [ ] **Кастомный домен** - обсудить (happyin.space уже работает через Cloudflare)

## Контент

- [ ] **370 validation warnings** - code blocks без language tag (`hooks/validate.py`)
- [ ] **76 incoming research files** - `skill-generator/state/incoming-research/`
- [ ] **Таблица доменов** - цифры в index.md hardcoded (85, 43, 40...), расходятся с реальными
- [ ] **Domain index pages** - 22 hub-страницы (overview + links) для каждого домена
- [ ] **Внутренняя перелинковка** - 5-10 ссылок на 2000 слов (SEO requirement)

## Инфраструктура

- [ ] **CI strict mode warnings** - сейчас 370 warnings проходят. Когда < 50, включить strict
- [ ] **Автообновление таблицы доменов** - расширить stats.py или JS inject
- [ ] **404 page** - кастомная (сейчас дефолтная Cloudflare)
- [ ] **Cloudflare cache** - проверить TTL, purge при деплое

## Улучшения

- [ ] **Dark mode graph** - проверить контрастность в светлой теме
- [ ] **Mobile graph** - touch events на мобильных
- [ ] **Contributor avatars** - фото вместо иконок

## Архитектура сайта

```
docs/                      # 560 статей, 22 домена
  {domain}/                # Доменные папки (algorithms, python, kafka, etc.)
  for-llm-agents.md        # Гайд для агентов-контрибьюторов
  contributing/index.md     # Contributing guide
  index.md                  # Главная
  robots.txt                # SEO (копируется в site/ хуком)
  llms.txt + llms-*.txt     # LLM discoverability (6 языков)
  javascripts/              # graph.js, stats.js (auto-generated)
  stylesheets/graph.css     # Snippet card, graph, contributors CSS
hooks/
  stats.py                  # Подсчёт статей, генерация stats.js
  validate.py               # Валидация статей (H1, code blocks, forbidden)
  wikilinks.py              # [[wiki-links]] → relative markdown links
  copy_extras.py            # Копирует .txt файлы в site root
overrides/main.html         # JSON-LD, OG tags, Twitter Card
mkdocs.yml                  # Конфигурация (theme, plugins, hooks)
.github/workflows/
  deploy-cloudflare.yml     # CI: build --strict + deploy to Cloudflare Pages
  indexnow.yml              # Уведомление поисковиков
  validate-article.yml      # PR validation
```
