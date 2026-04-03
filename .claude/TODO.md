# Knowledge Space - TODO

## Срочно (блокирует качество сайта)

- [ ] **Push и деплой** - commit graph fix + hooks + wikilinks, проверить на happyin.space
- [ ] **Проверить wiki-links рендеринг** - открыть статью (напр. kafka/event-sourcing), убедиться что `[[cqrs-pattern]]` стал кликабельной ссылкой
- [ ] **Граф: визуальная проверка** - убедиться что граф рендерится с fallback данными после деплоя

## Контент

- [ ] **370 validation warnings** - в основном code blocks без language tag (`validate.py`). Нужен batch fix или агент для прохода
- [ ] **76 incoming research files** - `skill-generator/state/incoming-research/` ждут обработки в статьи
- [ ] **Таблица доменов в index.md** - цифры (85, 43, 40...) hardcoded, расходятся с реальными (38, 30, 30...). Либо обновить вручную, либо генерировать хуком из KS_STATS
- [ ] **Stage 3 article generation** - оставшиеся домены (ios-mobile, testing-qa, rust, php, nodejs, misc, image-generation и др.)

## Инфраструктура

- [ ] **IndexNow key** - сгенерировать на bing.com/indexnow, добавить `INDEXNOW_KEY` secret в GitHub
- [ ] **CI strict mode** - сейчас `validate.py` не блокирует билд. Когда warnings < 50, включить strict
- [ ] **Автообновление таблицы доменов** - расширить `hooks/stats.py` чтобы генерировал HTML таблицу или inject через JS

## Улучшения сайта

- [ ] **Snippet card текст** - финальный вариант текста для "Copy for Claude" блока
- [ ] **404 page** - кастомная страница (сейчас дефолтная Cloudflare)
- [ ] **Favicon** - добавить (сейчас дефолтный MkDocs)
- [ ] **Open Graph image** - для шаринга ссылок в соцсетях/мессенджерах

## Низкий приоритет

- [ ] **Contributor avatars** - добавить фото/аватары к карточкам контрибуторов
- [ ] **Dark mode graph colors** - проверить контрастность в светлой теме
- [ ] **Mobile graph** - проверить что touch events работают на мобильных
