---
title: "Algorithmes et structures de données en Java"
category: concepts
tags: [java-spring, java, algorithms, sorting, searching, big-o, trees, interview]
level: 3
source_sha256: 47eac949edb0f3d962c952e6638e3647164c76f4e7ba52e61b21c23f4885b2f8
translation: machine
translated_at: '2026-10-24'
---
# Algorithmes et structures de données en Java {#algorithms-and-data-structures-in-java}

Algorithmes fondamentaux (tri, recherche), structures de données de base (pile, file, liste chaînée, arbre, table de hachage), analyse de la complexité et motifs courants en entretien technique.

## Points clés {#key-facts}

- Les tableaux ont une taille fixe ; `ArrayList` est dynamique. L'accès à un élément d'un tableau est en O(1)
- La recherche dichotomique exige une entrée triée et s'exécute en O(log n)
- HashMap : tableau de compartiments, la fonction de hachage associe une clé à un index, les collisions sont gérées par chaînage, un facteur de charge de 0,75 déclenche un redimensionnement
- ABR : gauche < parent < droite ; le parcours infixe (in-order) produit une sortie triée
- Le tri fusion en O(n log n) est toujours stable ; le tri rapide (Quick sort) est en O(n log n) en moyenne mais en O(n^2) au pire

## Motifs {#patterns}

### Complexité des tris {#sorting-complexity}
| Algorithme | Meilleur cas | Cas moyen | Pire cas | Stable |
|-----------|------|---------|-------|--------|
| Tri à bulles (Bubble Sort) | O(n) | O(n^2) | O(n^2) | Oui |
| Tri par sélection (Selection Sort) | O(n^2) | O(n^2) | O(n^2) | Non |
| Tri par insertion (Insertion Sort) | O(n) | O(n^2) | O(n^2) | Oui |
| Tri fusion (Merge Sort) | O(n log n) | O(n log n) | O(n log n) | Oui |
| Tri rapide (Quick Sort) | O(n log n) | O(n log n) | O(n^2) | Non |

### Recherche dichotomique {#binary-search}
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

### Pile et file {#stack-and-queue}
```java
// Stack (LIFO) - prefer ArrayDeque over Stack class
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); stack.pop(); stack.peek();

// Queue (FIFO)
Queue<Integer> queue = new LinkedList<>();
queue.offer(1); queue.poll(); queue.peek();
```

### Arbre binaire de recherche {#binary-search-tree}
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

### Parcours d'arbres {#tree-traversals}
```java
void inOrder(TreeNode n)   { inOrder(n.left); visit(n); inOrder(n.right); }   // sorted
void preOrder(TreeNode n)  { visit(n); preOrder(n.left); preOrder(n.right); }
void postOrder(TreeNode n) { postOrder(n.left); postOrder(n.right); visit(n); }
// Level-order: BFS with queue
```

### Référence Big O {#big-o-reference}
| O(1) | get/put de HashMap, accès par index de tableau |
| O(log n) | Recherche dichotomique, ABR équilibré |
| O(n) | Recherche linéaire, boucle simple |
| O(n log n) | Tri fusion, tri rapide en moyenne |
| O(n^2) | Tri à bulles, boucles imbriquées |
| O(2^n) | Fibonacci récursif naïf |

### Motif des deux pointeurs {#two-pointers-pattern}
```java
boolean isPalindrome(String s) {
    int left = 0, right = s.length() - 1;
    while (left < right) {
        if (s.charAt(left++) != s.charAt(right--)) return false;
    }
    return true;
}
```

### Motif de la fenêtre glissante {#sliding-window-pattern}
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

## Pièges {#gotchas}

- `mid = (left + right) / 2` peut provoquer un dépassement de capacité pour les grands tableaux - utiliser `left + (right - left) / 2`
- Le Fibonacci récursif naïf est en O(2^n) - utiliser la mémoïsation ou une version itérative pour obtenir O(n)
- La classe `Stack<>` est héritée (elle étend Vector) - utiliser `ArrayDeque` à la place
- Le pire cas de HashMap est en O(n) en présence de nombreuses collisions, mais depuis Java 8 les longues chaînes sont converties en arbres (O(log n))

## Voir aussi {#see-also}

- [[java-collections-streams]] - Implémentations des collections et opérations sur les Streams
- [[java-concurrency]] - Structures de données concurrentes
