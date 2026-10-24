---
title: "DP : problèmes de séquences"
category: algorithms
tags: [algorithms, dynamic-programming, LCS, edit-distance, LIS, subsequence, string-dp]
level: 3
source_sha256: 017f7f811256caa5629c73c6bf1774bf2873f61b4d911ed9782b2ed07ae26960
translation: machine
translated_at: '2026-10-24'
---
# DP : problèmes de séquences {#dp-sequence-problems}

Programmation dynamique sur les séquences et les chaînes de caractères : plus longue sous-séquence commune (LCS), distance d'édition (Levenshtein), plus longue sous-séquence croissante (LIS), Word Break, Interleaving Strings, et comptage de décodages. Ces problèmes partagent le schéma consistant à construire les solutions à partir de comparaisons de caractères ou d'éléments.

## Points clés {#key-facts}

- LCS : O(nm) en temps et en espace, réductible à O(min(n,m)) en espace
- Distance d'édition : O(nm) en temps et en espace, trois opérations : insertion, suppression, substitution
- LIS : DP naïve en O(n^2), O(n log n) avec le tri par paquets (patience sorting)
- Word Break : O(n^2 * L) où L = longueur moyenne d'un mot
- Longueur de la plus courte super-séquence commune = len(s1) + len(s2) - LCS(s1, s2)

## Schémas {#patterns}

### Plus longue sous-séquence commune (LCS) - O(nm) {#longest-common-subsequence-lcs-onm}

Sous-séquence = caractères dans l'ordre mais pas nécessairement contigus.

**Récurrence :**
```yaml
if s1[i-1] == s2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
else:                   dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

Si les derniers caractères correspondent, on les inclut tous les deux. Sinon, on en ignore un et on prend le meilleur résultat.

```python
def lcs(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]
```

### Distance d'édition (Levenshtein) - O(nm) {#edit-distance-levenshtein-onm}

Nombre minimal d'insertions, de suppressions ou de substitutions nécessaires pour transformer word1 en word2.

```python
def min_distance(word1, word2):
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i  # delete i chars
    for j in range(m + 1):
        dp[0][j] = j  # insert j chars
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete from word1
                    dp[i][j - 1],      # insert into word1
                    dp[i - 1][j - 1]   # substitute
                )
    return dp[n][m]
```

### Plus longue sous-séquence croissante (LIS) {#longest-increasing-subsequence-lis}

**DP en O(n^2) :**

```python
def lis(arr):
    n = len(arr)
    dp = [1] * n  # dp[i] = LIS ending at arr[i]
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**O(n log n) avec le tri par paquets (patience sorting) :**

```python
import bisect

def lis_nlogn(arr):
    tails = []  # tails[i] = smallest tail of increasing subseqs of length i+1
    for x in arr:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)
        else:
            tails[pos] = x  # replace with smaller tail
    return len(tails)
```

`tails` est toujours trié. Pour chaque élément, on effectue une recherche dichotomique pour trouver sa position. On l'ajoute en fin si il prolonge toutes les sous-séquences connues, sinon on le remplace afin de garder `tails` petit pour les extensions futures.

### Word Break {#word-break}

La chaîne s peut-elle être segmentée en mots issus du dictionnaire ?

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

### Interleaving Strings {#interleaving-strings}

s3 peut-elle être formée en entrelaçant s1 et s2 ?

```python
def is_interleave(s1, s2, s3):
    n, m = len(s1), len(s2)
    if n + m != len(s3):
        return False
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = ((dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or
                        (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]))
    return dp[n][m]
```

### Nombre de décodages {#ways-to-decode}

Chaîne de chiffres, 'A'=1 à 'Z'=26. Compter le nombre de décodages distincts.

```python
def num_decodings(s):
    n = len(s)
    if not s or s[0] == '0':
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1 if s[0] != '0' else 0
    for i in range(2, n + 1):
        one = int(s[i - 1])
        two = int(s[i - 2:i])
        if 1 <= one <= 9:
            dp[i] += dp[i - 1]
        if 10 <= two <= 26:
            dp[i] += dp[i - 2]
    return dp[n]
```

## Pièges {#gotchas}

- L'espace de la LCS peut être réduit à O(min(n,m)) en ne conservant que deux lignes
- Les cas de base de la distance d'édition sont critiques : dp[i][0] = i (tout supprimer), dp[0][j] = j (tout insérer)
- Le tableau `tails` de la LIS en O(n log n) ne contient PAS la LIS réelle, seulement sa longueur
- Word break : utiliser un set pour le dictionnaire permet une recherche en O(1) contre O(L) pour une liste
- Décoder '0' seul est invalide : il n'est valide que dans 10 ou 20

## Voir aussi {#see-also}

- [[dynamic-programming-fundamentals]] - concepts de la DP et approches top-down vs bottom-up
- [[dp-optimization-problems]] - variantes du sac à dos et du rendu de monnaie
- [[searching-algorithms]] - recherche dichotomique utilisée dans la LIS en O(n log n)
