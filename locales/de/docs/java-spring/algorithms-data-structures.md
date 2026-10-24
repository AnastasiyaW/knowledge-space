---
title: "Algorithmen und Datenstrukturen in Java"
category: concepts
tags: [java-spring, java, algorithms, sorting, searching, big-o, trees, interview]
level: 3
source_sha256: 47eac949edb0f3d962c952e6638e3647164c76f4e7ba52e61b21c23f4885b2f8
translation: machine
translated_at: '2026-10-24'
---
# Algorithmen und Datenstrukturen in Java {#algorithms-and-data-structures-in-java}

Kernalgorithmen (Sortieren, Suchen), grundlegende Datenstrukturen (Stack, Queue, Linked List, Tree, Hash Map), Komplexitätsanalyse und gängige Interview-Muster.

## Key Facts {#key-facts}

- Arrays haben eine feste Größe; `ArrayList` ist dynamisch. Der Zugriff auf ein Array ist O(1)
- Binäre Suche erfordert sortierte Eingabe und läuft in O(log n)
- HashMap: Array aus Buckets, Hash-Funktion bildet Schlüssel auf Index ab, Kollisionsbehandlung über Verkettung (Chaining), Load Factor 0,75 löst ein Resize aus
- BST: links < Elternknoten < rechts; In-Order-Traversierung liefert sortierte Ausgabe
- Merge Sort mit O(n log n) ist immer stabil; Quick Sort hat im Mittel O(n log n), im schlechtesten Fall jedoch O(n^2)

## Patterns {#patterns}

### Komplexität von Sortieralgorithmen {#sorting-complexity}
| Algorithmus | Bestfall | Durchschnitt | Schlechtester Fall | Stabil |
|-----------|------|---------|-------|--------|
| Bubble Sort | O(n) | O(n^2) | O(n^2) | Ja |
| Selection Sort | O(n^2) | O(n^2) | O(n^2) | Nein |
| Insertion Sort | O(n) | O(n^2) | O(n^2) | Ja |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | Ja |
| Quick Sort | O(n log n) | O(n log n) | O(n^2) | Nein |

### Binäre Suche {#binary-search}
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

### Stack und Queue {#stack-and-queue}
```java
// Stack (LIFO) - prefer ArrayDeque over Stack class
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.pop(); stack.peek();

// Queue (FIFO)
Queue<Integer> queue = new LinkedList<>();
queue.offer(1); queue.poll(); queue.peek();
```

### Binärer Suchbaum {#binary-search-tree}
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

### Baum-Traversierungen {#tree-traversals}
```java
void inOrder(TreeNode n)   { inOrder(n.left); visit(n); inOrder(n.right); }   // sorted
void preOrder(TreeNode n)  { visit(n); preOrder(n.left); preOrder(n.right); }
void postOrder(TreeNode n) { postOrder(n.left); postOrder(n.right); visit(n); }
// Level-order: BFS with queue
```

### Big-O-Referenz {#big-o-reference}
| O(1) | HashMap get/put, Array-Index |
| O(log n) | Binäre Suche, balancierter BST |
| O(n) | Lineare Suche, einfache Schleife |
| O(n log n) | Merge Sort, Quick Sort (Mittel) |
| O(n^2) | Bubble Sort, verschachtelte Schleifen |
| O(2^n) | Naives rekursives Fibonacci |

### Two-Pointers-Muster {#two-pointers-pattern}
```java
boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

### Sliding-Window-Muster {#sliding-window-pattern}
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

## Stolperfallen {#gotchas}

- `mid = (left + right) / 2` kann bei großen Arrays überlaufen – verwende `left + (right - left) / 2`
- Naives rekursives Fibonacci ist O(2^n) – verwende Memoization oder eine iterative Lösung für O(n)
- Die Klasse `Stack<>` ist veraltet (erbt von Vector) – verwende stattdessen `ArrayDeque`
- HashMap hat im Worst Case O(n) bei vielen Kollisionen, aber ab Java 8 wandelt sie lange Ketten in Bäume um (O(log n))

## Siehe auch {#see-also}

- [[java-collections-streams]] – Collection-Implementierungen und Stream-Operationen
- [[java-concurrency]] – Nebenläufige Datenstrukturen
