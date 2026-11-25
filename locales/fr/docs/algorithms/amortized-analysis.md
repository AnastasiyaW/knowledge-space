---
title: "Analyse amortie"
category: concepts
tags: [algorithms, complexity, amortized, dynamic-array]
level: 2
source_sha256: 1547f9a73a9a1cb72135ead4367c23d37aae2a754436459e29c15be551ccec8e
translation: machine
translated_at: '2026-10-24'
---
# Analyse amortie {#amortized-analysis}

L'analyse amortie calcule le coût moyen par opération sur une séquence d'opérations, en fournissant une borne garantie quelle que soit l'entrée. Contrairement à l'analyse en moyenne (qui dépend de la distribution des entrées), le coût amorti s'applique à toutes les séquences d'opérations possibles.

## Points clés {#key-facts}

- Coût amorti = coût total de n opérations / n
- Ne dépend PAS de la probabilité des entrées : borne garantie sur toutes les séquences
- Certaines opérations individuelles peuvent être coûteuses, mais la moyenne reste faible
- Exemple le plus courant : l'ajout (`append`) dans un tableau dynamique (liste Python)

## Patrons {#patterns}

### Insertion dans un tableau dynamique (liste Python) {#dynamic-array-python-list-insertion}

Lorsque le tableau est plein, on double sa capacité et on recopie tous les éléments. Le redimensionnement a lieu aux tailles 1, 2, 4, 8, 16, 32, ...

```text
Cost of n insertions without resize: n
Cost of resize operations: 1 + 2 + 4 + 8 + ... + n = 2n - 1

Total cost of n insertions = n + (2n - 1) ~ 3n
Amortized cost per insertion = 3n / n = O(1)
```

Bien qu'un seul redimensionnement coûte O(n), il se produit si rarement que le coût amorti par `append()` est O(1).

### Distinction essentielle {#key-distinction}

| Concept | Dépend de | Garantie |
|---------|-----------|----------|
| Pire cas | Unique entrée la plus défavorable | Par opération |
| Cas moyen | Distribution de probabilité des entrées | Espérance sur des entrées aléatoires |
| Amorti | Séquence d'opérations | Moyenne par opération, pour toute séquence |

## Pièges à éviter {#gotchas}

- Un coût amorti O(1) ne signifie PAS que chaque opération est en O(1) : des opérations individuelles peuvent coûter O(n)
- Peu adapté aux systèmes temps réel, où chaque opération doit être rapide
- La garantie porte sur l'ensemble de la séquence, et non sur chaque opération
- `list.append()` de Python est en O(1) amorti, mais un seul `append` peut déclencher une copie en O(n)

## Voir aussi {#see-also}

- [[complexity-analysis|concepts fondamentaux de complexité]] - notions fondamentales de complexité
- [[data-structures|fonctionnement interne des listes Python]] - structures de données
