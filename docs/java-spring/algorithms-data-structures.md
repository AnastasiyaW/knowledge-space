---
title: Algorithms and Data Structures in Java
category: concepts
tags: [java-spring, java, algorithms, sorting, searching, big-o, trees, interview]
---

# Algorithms and Data Structures in Java

Core algorithms (sorting, searching), fundamental data structures (stack, queue, linked list, tree, hash map), complexity analysis, and common interview patterns.

## Key Facts

- Arrays are fixed-size; `ArrayList` is dynamic. Array access is O(1)
- Binary search requires sorted input and runs in O(log n)
- HashMap: array of buckets, hash function maps key to index, collision handling via chaining, load factor 0.75 triggers resize
- BST: left < parent < right; in-order traversal gives sorted output
- Merge sort O(n log n) is always stable; Quick sort O(n log n) average but O(n^2) worst case

## Patterns

### Sorting Complexity
| Algorithm | Best | Average | Worst | Stable |
|-----------|------|---------|-------|--------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | Yes |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | No |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | Yes |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Yes |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | No |

### Binary Search
```java
int binarySearch(int[] arr, int target) {
    int left = 0, right = arr.length - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;  // avoids overflow
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

### Stack and Queue
```java
// Stack (LIFO) - prefer ArrayDeque over Stack class
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.pop(); stack.peek();

// Queue (FIFO)
Queue<Integer> queue = new LinkedList<>();
queue.offer(1); queue.poll(); queue.peek();
```

### Binary Search Tree
```java
class TreeNode {
    int value;
    TreeNode left, right;
}

void insert(TreeNode root, int value) {
    if (value < root.value) {
        if (root.left == null) root.left = new TreeNode(value);
        else insert(root.left, value);
    } else {
        if (root.right == null) root.right = new TreeNode(value);
        else insert(root.right, value);
    }
}
```

### Tree Traversals
```java
void inOrder(TreeNode n)   { inOrder(n.left); visit(n); inOrder(n.right); }   // sorted
void preOrder(TreeNode n)  { visit(n); preOrder(n.left); preOrder(n.right); }
void postOrder(TreeNode n) { postOrder(n.left); postOrder(n.right); visit(n); }
// Level-order: BFS with queue
```

### Big O Reference
| O(1) | HashMap get/put, array index |
| O(log n) | Binary search, balanced BST |
| O(n) | Linear search, single loop |
| O(n log n) | Merge sort, quick sort avg |
| O(n^2) | Bubble sort, nested loops |
| O(2^n) | Naive recursive Fibonacci |

### Two Pointers Pattern
```java
boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

### Sliding Window Pattern
```java
int maxSumSubarray(int[] arr, int k) {
    int windowSum = 0, maxSum = 0;
    for (int i = 0; i < k; i++) windowSum += arr[i];
    maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}
```

## Gotchas

- `mid = (left + right) / 2` can overflow for large arrays - use `left + (right - left) / 2`
- Naive recursive Fibonacci is O(2^n) - use memoization or iterative for O(n)
- `Stack<>` class is legacy (extends Vector) - use `ArrayDeque` instead
- HashMap worst case is O(n) with many collisions, but Java 8+ converts long chains to trees (O(log n))

## See Also

- [[java-collections-streams]] - Collection implementations and Stream operations
- [[java-concurrency]] - Concurrent data structures
