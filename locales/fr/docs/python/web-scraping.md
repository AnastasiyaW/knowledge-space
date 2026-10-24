---
title: "Scraping web en Python avec BeautifulSoup"
category: concepts
tags: [python, web-scraping, beautifulsoup, requests, html-parsing]
level: 3
source_sha256: 0a27c77dc450471ea3618c66d8450c959c1ae937905f248564d1839d8542bdfb
translation: machine
translated_at: '2026-10-24'
---
# Scraping web en Python avec BeautifulSoup {#python-web-scraping-with-beautifulsoup}

Schémas de scraping avec BeautifulSoup : méthodes de recherche d'éléments, extraction de données, pagination, scraping de tableaux et contre-mesures anti-bot.

## Points clés {#key-facts}

- Trois parseurs : `html.parser` (bibliothèque standard), `lxml` (plus rapide), `html5lib` (le plus tolérant)
- `find()` renvoie la première correspondance ; `find_all()` renvoie toutes les correspondances ; `select()` utilise les sélecteurs CSS
- `tag.text` récupère tout le texte de manière récursive ; `tag.string` ne fonctionne que si la balise possède exactement un enfant textuel
- `tag['href']` lève une KeyError si l'attribut est absent ; `tag.get('href')` renvoie None
- Pour les pages rendues par JavaScript, utilisez plutôt `selenium` ou `playwright`
- Utilisez toujours `requests.Session()` pour conserver les cookies entre les requêtes

## Schémas {#patterns}

### Configuration {#setup}

```python
from bs4 import BeautifulSoup
import requests

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(response.text, 'html.parser')
```

### Recherche d'éléments {#finding-elements}

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

### Extraction de données {#extracting-data}

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

### Scraping de tableaux {#table-scraping}

```python
table = soup.find('table')
headers = [th.text.strip() for th in table.find_all('th')]
rows = []
for tr in table.find('tbody').find_all('tr'):
    cells = [td.text.strip() for td in tr.find_all('td')]
    rows.append(dict(zip(headers, cells)))
```

### Scraping paginé {#paginated-scraping}

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

### Résolution des URL {#url-resolution}

```python
from urllib.parse import urljoin
links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
```

### Contre-mesures anti-bot {#anti-bot-countermeasures}

| Technique | Mise en œuvre |
|-----------|---------------|
| User-Agent | `headers={'User-Agent': 'Mozilla/5.0'}` |
| Limitation de débit | `time.sleep(random.uniform(1, 3))` entre les requêtes |
| Cookies de session | `requests.Session()` |
| Proxys tournants | Services de proxy pour un scraping intensif |
| Rendu JS | `selenium` ou `playwright` |

## Pièges {#gotchas}

- `tag.string` renvoie None si la balise contient plusieurs éléments, même si tous contiennent du texte
- `next_sibling` peut renvoyer des espaces (NavigableString) : utilisez plutôt `find_next_sibling()`
- `find_all(class_='product')` utilise `class_` avec un tiret bas, car `class` est un mot-clé réservé de Python
- Certains sites servent un contenu différent selon le User-Agent : vérifiez ce que vous recevez
- `requests.get()` suit les redirections par défaut ; vérifiez `response.url` pour confirmer la destination finale

## Voir aussi {#see-also}

- [[stdlib-patterns]] - collections, itertools pour le traitement des données scrapées
- [[sql-databases/advanced-patterns]] - SQL pour l'analyse des jeux de données scrapés
- [[browser-test-automation]] - Selenium/Geb pour les pages rendues par JavaScript
