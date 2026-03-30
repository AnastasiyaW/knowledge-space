---
title: Bit Manipulation
category: algorithms
tags: [bitwise, xor, bitmask, bit-shift, powers-of-two]
---

# Bit Manipulation

## Key Facts

- Bitwise operations operate on individual bits: AND (`&`), OR (`|`), XOR (`^`), NOT (`~`), shifts (`<<`, `>>`)
- O(1) time for all bitwise operations (fixed-width integers)
- XOR properties: `a ^ a = 0`, `a ^ 0 = a`, commutative, associative
- Check if number is power of 2: `n > 0 and (n & (n - 1)) == 0`
- Count set bits (popcount): `bin(n).count('1')` or Brian Kernighan's algorithm
- Bitmask can represent subsets of a set with n elements (2^n possible masks)
- Related: [[arrays-and-strings]], [[dynamic-programming]]

## Patterns

### Common Bit Tricks

```python
# Check if bit at position i is set
def is_bit_set(n, i):
    return (n >> i) & 1 == 1

# Set bit at position i
def set_bit(n, i):
    return n | (1 << i)

# Clear bit at position i
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle bit at position i
def toggle_bit(n, i):
    return n ^ (1 << i)

# Get lowest set bit
def lowest_set_bit(n):
    return n & (-n)

# Clear lowest set bit
def clear_lowest_bit(n):
    return n & (n - 1)

# Check power of 2
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

### Single Number (XOR)

```python
# Every element appears twice except one - find it in O(n) time, O(1) space
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
# XOR cancels duplicates: a ^ a = 0, remaining = single number
```

### Count Set Bits (Brian Kernighan)

```python
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # clear lowest set bit
        count += 1
    return count
# O(k) where k = number of set bits
```

### Bitmask DP - Subsets with Bitmask

```python
# Generate all subsets of a set
def all_subsets(nums):
    n = len(nums)
    result = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    return result
```

### Swap Without Temp Variable

```python
def swap_xor(a, b):
    a ^= b
    b ^= a
    a ^= b
    return a, b
# Clever but less readable; prefer a, b = b, a in Python
```

```java
// Java: count bits
public int hammingWeight(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}

// Java: single number
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) result ^= num;
    return result;
}
```

## Gotchas

- **Python integers are arbitrary precision** - no overflow, but `~n` gives `-(n+1)` due to two's complement representation
- **Java/C++ signed integers** - right shift `>>` is arithmetic (preserves sign); `>>>` in Java is logical shift
- **XOR trick requires exactly paired elements** - single_number only works when all duplicates appear an even number of times
- **Bitmask DP limits** - practical for n <= 20 (2^20 = 1M states); beyond that, memory/time explodes
- **Operator precedence** - in most languages, `&` and `|` have lower precedence than `==`; use parentheses: `(n & 1) == 0`
- **Negative numbers** - bitwise operations on negative numbers behave differently across languages

## See Also

- [[dynamic-programming]] - bitmask DP for subset problems
- [[recursion-and-backtracking]] - alternative to bitmask for subset generation
- [[big-o-complexity-analysis]] - bitwise ops are O(1) for fixed-width integers
