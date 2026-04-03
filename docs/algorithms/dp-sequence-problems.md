---
title: "DP: Sequence Problems"
category: algorithms
tags: [algorithms, dynamic-programming, LCS, edit-distance, LIS, subsequence, string-dp]
---

# DP: Sequence Problems

Dynamic programming on sequences and strings: Longest Common Subsequence (LCS), Edit Distance (Levenshtein), Longest Increasing Subsequence (LIS), Word Break, Interleaving Strings, and decode counting. These problems share the pattern of building solutions from character/element comparisons.

## Key Facts

- LCS: O(nm) time/space, space-optimizable to O(min(n,m))
- Edit Distance: O(nm) time/space, three operations: insert, delete, substitute
- LIS: O(n^2) naive DP, O(n log n) with patience sorting
- Word Break: O(n^2 * L) where L = average word length
- Shortest Common Supersequence length = len(s1) + len(s2) - LCS(s1, s2)

## Patterns

### Longest Common Subsequence (LCS) - O(nm)

Subsequence = characters in order but not necessarily contiguous.

**Recurrence:**
```
if s1[i-1] == s2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
else:                   dp[i][j] = max(dp[i-1][j], dp[i][j-1])
```

If last chars match, include both. Otherwise, skip one and take the best.

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

### Edit Distance (Levenshtein) - O(nm)

Minimum insertions, deletions, or substitutions to transform word1 into word2.

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

### Longest Increasing Subsequence (LIS)

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

**O(n log n) with Patience Sorting:**

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

`tails` is always sorted. For each element, binary search for its position. Append if extends all known subsequences, otherwise replace to keep tails small for future extensions.

### Word Break

Can string s be segmented into words from dictionary?

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

### Interleaving Strings

Can s3 be formed by interleaving s1 and s2?

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

### Ways to Decode

String of digits, 'A'=1 to 'Z'=26. Count distinct decodings.

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

## Gotchas

- LCS space can be reduced to O(min(n,m)) by keeping only two rows
- Edit distance base cases are critical: dp[i][0] = i (delete all), dp[0][j] = j (insert all)
- LIS O(n log n) `tails` array does NOT contain the actual LIS - just its length
- Word break: using a set for dictionary enables O(1) lookup vs O(L) for list
- Decoding '0' is invalid on its own - only valid as part of 10 or 20

## See Also

- [[dynamic-programming-fundamentals]] - DP concepts and top-down vs bottom-up
- [[dp-optimization-problems]] - knapsack, coin change variants
- [[searching-algorithms]] - binary search used in O(n log n) LIS
