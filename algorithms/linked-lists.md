---
title: Linked Lists
category: data-structures
tags: [linked-list, singly-linked, doubly-linked, fast-slow-pointer, cycle-detection]
---

# Linked Lists

## Key Facts

- **Singly linked list** - each node has `data` + `next` pointer; O(1) insert/delete at head, O(n) access by index
- **Doubly linked list** - each node has `data` + `next` + `prev`; O(1) insert/delete at both ends
- No random access (unlike arrays) - must traverse from head
- Access: O(n), Search: O(n), Insert at head: O(1), Insert at position: O(n), Delete: O(1) if node reference known
- Merge sort is the preferred sort for linked lists - O(n log n) time, O(log n) space (no extra array needed)
- Related: [[arrays-and-strings]], [[stacks-and-queues]]

## Patterns

### Node Definition

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

### Reverse a Linked List (Iterative)

```python
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev  # new head
```

### Fast and Slow Pointers (Floyd's Algorithm)

```python
# Find middle of linked list
def find_middle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow  # middle node

# Detect cycle
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start
def detect_cycle_start(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow
    return None
```

### Merge Two Sorted Lists

```python
def merge_sorted(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    tail.next = l1 or l2
    return dummy.next
```

### Merge Sort on Linked List

```python
def sort_list(head):
    if not head or not head.next:
        return head
    # Find middle using slow/fast pointers
    slow, fast = head, head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    mid = slow.next
    slow.next = None  # split
    left = sort_list(head)
    right = sort_list(mid)
    return merge_sorted(left, right)
# Time: O(n log n), Space: O(log n) - stack only, no extra array
```

```java
// Java: reverse linked list
public ListNode reverseList(ListNode head) {
    ListNode prev = null, curr = head;
    while (curr != null) {
        ListNode next = curr.next;
        curr.next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}
```

## Gotchas

- **No random access** - `list[i]` is O(n), not O(1). Cannot use binary search on linked lists
- **Dummy head node** simplifies edge cases (empty list, insert at head) - return `dummy.next` at the end
- **Losing references** - save `curr.next` before modifying pointers in reversal
- **Merge sort space** - O(log n) for linked lists (stack only), vs O(n) for arrays (needs auxiliary array)
- **Fast pointer null check** - always check `fast and fast.next` before advancing, not just `fast.next`
- **Cycle detection** - Floyd's cycle detection uses O(1) space vs O(n) for hash set approach

## See Also

- [[stacks-and-queues]] - can be implemented with linked lists
- [[sorting-algorithms]] - merge sort is optimal for linked lists
- [[arrays-and-strings]] - compare trade-offs: access vs insertion
