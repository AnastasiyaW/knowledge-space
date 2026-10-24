---
title: "DP: Sequenzprobleme"
category: algorithms
tags: [algorithms, dynamic-programming, LCS, edit-distance, LIS, subsequence, string-dp]
level: 3
source_sha256: 017f7f811256caa5629c73c6bf1774bf2873f61b4d911ed9782b2ed07ae26960
translation: machine
translated_at: '2026-10-24'
---
# DP: Sequenzprobleme {#dp-sequence-problems}

Dynamische Programmierung auf Sequenzen und Zeichenketten: Longest Common Subsequence (LCS), Edit Distance (Levenshtein), Longest Increasing Subsequence (LIS), Word Break, Interleaving Strings und das Zählen von Dekodierungen. Diese Probleme folgen dem gemeinsamen Muster, Lösungen aus Vergleichen von Zeichen bzw. Elementen aufzubauen.

## Key Facts {#key-facts}

- LCS: O(nm) Zeit/Speicher, Speicher auf O(min(n,m)) optimierbar
- Edit Distance: O(nm) Zeit/Speicher, drei Operationen: Einfügen, Löschen, Ersetzen
- LIS: O(n^2) naives DP, O(n log n) mit Patience Sorting
- Word Break: O(n^2 * L), wobei L = durchschnittliche Wortlänge
- Länge der Shortest Common Supersequence = len(s1) + len(s2) - LCS(s1, s2)

## Patterns {#patterns}

### Longest Common Subsequence (LCS) - O(nm) {#longest-common-subsequence-lcs-onm}

Subsequenz = Zeichen in gleicher Reihenfolge, aber nicht notwendigerweise zusammenhängend.

**Rekurrenz:**
```yaml
if s1[i-1] == s2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
else:                   dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

Stimmen die letzten Zeichen überein, werden beide berücksichtigt. Andernfalls wird eines übersprungen und das bessere Ergebnis übernommen.

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

### Edit Distance (Levenshtein) - O(nm) {#edit-distance-levenshtein-onm}

Minimale Anzahl an Einfügungen, Löschungen oder Ersetzungen, um word1 in word2 zu überführen.

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

### Longest Increasing Subsequence (LIS) {#longest-increasing-subsequence-lis}

**O(n^2) DP:**

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

**O(n log n) mit Patience Sorting:**

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

`tails` ist stets sortiert. Für jedes Element wird per binärer Suche seine Position bestimmt. Ist das Element größer als alle bekannten Subsequenzen, wird es angehängt; andernfalls ersetzt es ein Element, damit `tails` für künftige Erweiterungen klein bleibt.

### Word Break {#word-break}

Lässt sich die Zeichenkette s aus Wörtern des Wörterbuchs zusammensetzen?

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

Kann s3 durch Verschränkung von s1 und s2 gebildet werden?

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

### Ways to Decode {#ways-to-decode}

Zeichenkette aus Ziffern, mit 'A'=1 bis 'Z'=26. Anzahl unterschiedlicher Dekodierungen zählen.

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

## Gotchas {#gotchas}

- Der Speicherbedarf für LCS lässt sich auf O(min(n,m)) reduzieren, indem nur zwei Zeilen gehalten werden
- Die Basisfälle der Edit Distance sind kritisch: dp[i][0] = i (alles löschen), dp[0][j] = j (alles einfügen)
- Das `tails`-Array der O(n log n) LIS enthält nicht die tatsächliche LIS, sondern nur deren Länge
- Word Break: Ein Set für das Wörterbuch ermöglicht Nachschlagen in O(1) statt O(L) bei einer Liste
- Die Ziffer '0' ist allein ungültig und nur als Teil von 10 oder 20 gültig

## Siehe auch {#see-also}

- [[dynamic-programming-fundamentals]] - DP-Konzepte sowie Top-down vs. Bottom-up
- [[dp-optimization-problems]] - Knapsack- und Coin-Change-Varianten
- [[searching-algorithms]] - binäre Suche in der O(n log n) LIS
