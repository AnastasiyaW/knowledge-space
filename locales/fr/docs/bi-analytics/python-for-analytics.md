---
title: "Python pour l'analytique"
category: tools
tags: [bi-analytics, python, numpy, jupyter, basics, analytics]
level: 4
source_sha256: 8c8e5483551fd089c9572afc930521069c97108dc70ae393a7f706d2f90d8f60
translation: machine
translated_at: '2026-10-24'
---
# Python pour l'analytique {#python-for-analytics}

Notions fondamentales de Python pour les analystes de données, couvrant la syntaxe de base, NumPy pour les opérations numériques et le flux de travail avec Jupyter Notebook. Cela complète les compétences en SQL et permet une manipulation de données plus souple que les seuls outils de BI.

## Points clés {#key-facts}

- Python est à typage dynamique (contrairement à Kotlin/Java, qui sont à typage statique)
- NumPy fournit des opérations vectorisées qui sont des ordres de grandeur plus rapides que les boucles Python
- Jupyter Notebook est l'environnement standard pour le travail analytique en Python
- Bibliothèques principales : NumPy (numérique), pandas (données tabulaires), matplotlib/seaborn (visualisation)
- Les compréhensions de liste et de dictionnaire offrent une syntaxe concise pour la transformation de données

## Modèles {#patterns}

### Types de données et structures de base {#core-data-types-and-structures}

```python
# Basic types
x = 5           # int
y = 3.14        # float
name = "Alice"  # str
active = True   # bool
nothing = None  # NoneType

# Lists
items = [1, 2, 3, 4, 5]
items.append(6)
items[0]         # first
items[-1]        # last
items[1:3]       # slice [2, 3]
squares = [x**2 for x in range(10)]
evens = [x for x in items if x % 2 == 0]

# Dictionaries
user = {"id": 1, "name": "Alice", "age": 28}
user.get("email", "")  # safe access with default
word_counts = {word: len(word) for word in ["hello", "world"]}
```

### Fonctions {#functions}

```python
def calculate_ltv(avg_order, frequency, months):
    """Calculate customer lifetime value."""
    return avg_order * frequency * months

def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

min_val, max_val, avg = get_stats([1, 2, 3, 4, 5])
```

### NumPy {#numpy}

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
zeros = np.zeros(10)
ones = np.ones((3, 4))

# Vectorized operations (no loops needed)
arr * 2          # [2, 4, 6, 8, 10]
arr ** 2         # [1, 4, 9, 16, 25]
np.sqrt(arr)     # element-wise sqrt

# Statistics
np.mean(arr)
np.median(arr)
np.std(arr)
np.percentile(arr, [25, 50, 75])

# 2D arrays (matrices)
matrix = np.array([[1, 2], [3, 4]])
matrix.shape     # (2, 2)
matrix.T         # transpose
matrix @ matrix  # matrix multiplication

# Boolean masking
arr[arr > 3]     # [4, 5]
```

### Flux de travail avec Jupyter Notebook {#jupyter-notebook-workflow}

Raccourcis clés :
- `Shift+Enter` - exécuter la cellule, passer à la suivante
- `Ctrl+Enter` - exécuter la cellule, rester sur place
- `A` / `B` - insérer une cellule au-dessus/en dessous (mode commande)
- `DD` - supprimer la cellule
- `M` - convertir en Markdown ; `Y` - convertir en code

Bonnes pratiques :
- Redémarrer le noyau et exécuter toutes les cellules avant de partager
- Utiliser les cellules Markdown pour la documentation
- Garder les cellules ciblées (un concept par cellule)
- Donner des noms de variables descriptifs

## Pièges {#gotchas}

- Division entière en Python : `5 / 2 = 2.5` (flottant) mais `5 // 2 = 2` (entier) - ceci diffère de nombreux autres langages
- Les arguments par défaut mutables dans les fonctions sont un piège classique : `def f(lst=[])` partage la liste entre les appels
- Les tableaux NumPy ont un dtype fixe - mélanger les types provoque une conversion implicite silencieuse (les entiers deviennent des flottants dès qu'un flottant est présent)
- Les cellules Jupyter peuvent être exécutées dans le désordre, ce qui crée des bogues d'état caché - redémarrer le noyau régulièrement

## Voir aussi {#see-also}

- [[pandas-data-analysis]] - manipulation de données tabulaires avec pandas
- [[sql-for-analytics]] - SQL comme principal langage de requête analytique
- [[web-marketing-analytics]] - connecter Python aux données analytiques web
