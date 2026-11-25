---
title: "Python-Web-Scraping mit BeautifulSoup"
category: concepts
tags: [python, web-scraping, beautifulsoup, requests, html-parsing]
level: 3
source_sha256: 0a27c77dc450471ea3618c66d8450c959c1ae937905f248564d1839d8542bdfb
translation: machine
translated_at: '2026-10-24'
---
# Python-Web-Scraping mit BeautifulSoup {#python-web-scraping-with-beautifulsoup}

BeautifulSoup-Muster für Web-Scraping: Methoden zur Elementsuche, Datenextraktion, Paginierung, Tabellen-Scraping und Gegenmaßnahmen gegen Bots.

## Wichtige Fakten {#key-facts}

- Drei Parser: `html.parser` (Standardbibliothek), `lxml` (schneller), `html5lib` (am tolerantesten)
- `find()` liefert den ersten Treffer, `find_all()` alle Treffer; `select()` verwendet CSS-Selektoren
- `tag.text` liefert rekursiv den gesamten Text; `tag.string` nur, wenn das Tag genau einen Textknoten als Kind hat
- `tag['href']` löst einen KeyError aus, wenn das Attribut fehlt; `tag.get('href')` liefert None
- Für JavaScript-gerenderte Seiten stattdessen `selenium` oder `playwright` verwenden
- Immer `requests.Session()` verwenden, um Cookies über mehrere Anfragen hinweg beizubehalten

## Muster {#patterns}

### Einrichtung {#setup}

```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')
```

### Elemente finden {#finding-elements}

```python
# By tag and attributes
tag = soup.find('div', class_='product')
tag = soup.find('a', attrs={'href': True})
tag = soup.find('span', id='price')

# Find all with multiple tag names
tags = soup.find_all(['h1', 'h2', 'h3'])
tags = soup.find_all('a', limit=10)

# CSS selectors (often cleaner)
tags = soup.select('div.product > span.price')
tag  = soup.select_one('table#results tbody tr')
```

### Daten extrahieren {#extracting-data}

```python
tag.text               # all text content (recursive)
tag.get_text()         # same, with optional separator
tag.string             # only if exactly one string child
tag.strings            # generator of all strings
tag.stripped_strings   # stripped, no empty strings

tag['href']            # attribute (KeyError if missing)
tag.get('href')        # safe (None if missing)
tag.attrs              # dict of all attributes

# Navigation
tag.parent
tag.children           # direct children (generator)
tag.descendants        # all descendants (generator)
tag.find_next_sibling('tr')
```

### Tabellen-Scraping {#table-scraping}

```python
table = soup.find('table')
headers = [th.text.strip() for th in table.find_all('th')]
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = [td.text.strip() for td in tr.find_all('td')]
    rows.append(dict(zip(headers, cells)))
```

### Scraping mit Paginierung {#paginated-scraping}

```python
page = 1
while True:
    soup = get_page(base_url, page)
    items = soup.find_all('div', class_='item')
    if not items:
        break
    process(items)
    page += 1
```

### URL-Auflösung {#url-resolution}

```python
from urllib.parse import urljoin
links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
```

### Gegenmaßnahmen gegen Bots {#anti-bot-countermeasures}

| Technik | Implementierung |
|-----------|---------------|
| User-Agent | `headers={'User-Agent': 'Mozilla/5.0'}` |
| Rate-Limiting | `time.sleep(random.uniform(1, 3))` zwischen den Anfragen |
| Session-Cookies | `requests.Session()` |
| Rotierende Proxys | Proxy-Dienste für umfangreiches Scraping |
| JS-Rendering | `selenium` oder `playwright` |

## Fallstricke {#gotchas}

- `tag.string` liefert None, wenn das Tag mehrere Elemente enthält, auch wenn alle Text enthalten
- `next_sibling` kann Leerraum (NavigableString) liefern; stattdessen `find_next_sibling()` verwenden
- `find_all(class_='product')` verwendet `class_` mit Unterstrich, weil `class` ein Schlüsselwort in Python ist
- Manche Seiten liefern je nach User-Agent unterschiedliche Inhalte; prüfen, was tatsächlich ankommt
- `requests.get()` folgt standardmäßig Weiterleitungen; `response.url` prüfen, um das tatsächliche Ziel zu verifizieren

## Siehe auch {#see-also}

- [[stdlib-patterns]] - collections, itertools zur Verarbeitung gescrapter Daten
- [[sql-databases/advanced-patterns]] - SQL zur Analyse gescrapter Datensätze
- [[browser-test-automation]] - Selenium/Geb für JavaScript-gerenderte Seiten
