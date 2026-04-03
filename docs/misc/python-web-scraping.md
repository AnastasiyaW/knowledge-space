---
title: Python Web Scraping with BeautifulSoup
category: concepts
tags: [misc, python, web-scraping, beautifulsoup, requests, html-parsing]
---

# Python Web Scraping with BeautifulSoup

BeautifulSoup web scraping patterns - element search methods, data extraction, pagination, table scraping, and anti-bot countermeasures.

## Key Facts

- Three parsers: `html.parser` (stdlib), `lxml` (faster), `html5lib` (most lenient)
- `find()` returns first match; `find_all()` returns all; `select()` uses CSS selectors
- `tag.text` gets all text recursively; `tag.string` only if tag has exactly one string child
- `tag['href']` raises KeyError if missing; `tag.get('href')` returns None
- For JavaScript-rendered pages, use `selenium` or `playwright` instead
- Always use `requests.Session()` to maintain cookies across requests

## Patterns

### Setup

```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')
```

### Finding Elements

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

### Extracting Data

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

### Table Scraping

```python
table = soup.find('table')
headers = [th.text.strip() for th in table.find_all('th')]
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = [td.text.strip() for td in tr.find_all('td')]
    rows.append(dict(zip(headers, cells)))
```

### Paginated Scraping

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

### URL Resolution

```python
from urllib.parse import urljoin
links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
```

### Anti-Bot Countermeasures

| Technique | Implementation |
|-----------|---------------|
| User-Agent | `headers={'User-Agent': 'Mozilla/5.0'}` |
| Rate limiting | `time.sleep(random.uniform(1, 3))` between requests |
| Session cookies | `requests.Session()` |
| Rotating proxies | Proxy services for serious scraping |
| JS rendering | `selenium` or `playwright` |

## Gotchas

- `tag.string` returns None if tag contains multiple elements, even if they all contain text
- `next_sibling` may return whitespace (NavigableString) - use `find_next_sibling()` instead
- `find_all(class_='product')` uses `class_` with underscore because `class` is a Python keyword
- Some sites serve different content to different User-Agents - check what you receive
- `requests.get()` follows redirects by default; check `response.url` to verify final destination

## See Also

- [[python-stdlib-patterns]] - collections, itertools for processing scraped data
- [[sql-advanced-patterns]] - SQL for analyzing scraped datasets
- [[browser-test-automation]] - Selenium/Geb for JS-rendered pages
