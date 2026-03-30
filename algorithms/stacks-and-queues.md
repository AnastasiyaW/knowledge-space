---
title: Stacks and Queues
category: data-structures
tags: [stack, queue, deque, monotonic-stack, lifo, fifo]
---

# Stacks and Queues

## Key Facts

- **Stack** - LIFO (Last In, First Out); push/pop/peek all O(1)
- **Queue** - FIFO (First In, First Out); enqueue/dequeue/peek all O(1)
- **Deque** (double-ended queue) - O(1) insert/remove at both ends; Python `collections.deque`
- **Monotonic stack** - maintains elements in sorted order; used for "next greater/smaller element" problems
- Stack implementations: array-based (Python list), linked list
- Queue implementations: linked list, circular array, `collections.deque`
- Related: [[linked-lists]], [[binary-tree-traversal]]

## Patterns

### Stack - Balanced Parentheses

```python
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
```

### Monotonic Stack - Next Greater Element

```python
def next_greater_element(nums):
    result = [-1] * len(nums)
    stack = []  # indices, decreasing values
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)
    return result
```

### Queue using Two Stacks

```python
class QueueWithStacks:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def enqueue(self, val):
        self.in_stack.append(val)

    def dequeue(self):
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())
        return self.out_stack.pop()
    # Amortized O(1) per operation
```

### Min Stack - O(1) getMin

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def get_min(self):
        return self.min_stack[-1]
```

```java
// Java: Queue using LinkedList
import java.util.LinkedList;
import java.util.Queue;

Queue<Integer> queue = new LinkedList<>();
queue.offer(1);     // enqueue
queue.poll();       // dequeue
queue.peek();       // front element

// Java: Stack
import java.util.Stack;
Stack<Integer> stack = new Stack<>();
stack.push(1);
stack.pop();
stack.peek();
// Prefer Deque<Integer> stack = new ArrayDeque<>(); in modern Java
```

## Gotchas

- **Python list as stack is fine** - `append()` and `pop()` are O(1); but `pop(0)` for queue is O(n) - use `deque`
- **Java Stack is legacy** - use `ArrayDeque` instead of `java.util.Stack` (which extends Vector)
- **Queue with two stacks** - amortized O(1) but individual dequeue can be O(n) when transferring
- **Monotonic stack direction** - decreasing stack for "next greater", increasing stack for "next smaller"
- **Stack overflow in recursion** - every recursive call uses implicit stack space; convert to iterative with explicit stack if depth is large
- **Empty stack/queue checks** - always check `isEmpty()` before `pop()`/`dequeue()` to avoid exceptions

## See Also

- [[binary-tree-traversal]] - iterative traversal uses explicit stack
- [[graph-bfs-dfs]] - BFS uses queue, DFS uses stack
- [[linked-lists]] - underlying implementation for queue
