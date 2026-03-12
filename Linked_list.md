# ─────────────────────────────────────────────
#  Linked List – complete reference & practice
# ─────────────────────────────────────────────

# ── Node definition ──────────────────────────
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ── Helper: build a list from a Python list ──
def build(values):
    """[1, 2, 3]  →  1 → 2 → 3"""
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


# ── Helper: convert back to a Python list ────
def to_list(head):
    """1 → 2 → 3  →  [1, 2, 3]"""
    result = []
    cur = head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result


# ── Helper: pretty-print ──────────────────────
def display(head):
    print(" → ".join(str(v) for v in to_list(head)) or "Empty list")


# ─────────────────────────────────────────────
#  Core operations
# ─────────────────────────────────────────────

def traverse(head):
    """Print every node value."""
    cur = head
    while cur:
        print(cur.val)
        cur = cur.next


def length(head):
    """Return the number of nodes."""
    count = 0
    cur = head
    while cur:
        count += 1
        cur = cur.next
    return count


def search(head, target):
    """Return True if target exists in the list."""
    cur = head
    while cur:
        if cur.val == target:
            return True
        cur = cur.next
    return False


# ── Insert ────────────────────────────────────

def insert_at_head(head, val):
    """O(1) – prepend a new node."""
    new_node = ListNode(val, head)
    return new_node          # new head


def insert_at_tail(head, val):
    """O(n) – append a new node."""
    new_node = ListNode(val)
    if not head:
        return new_node
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = new_node
    return head


def insert_at_position(head, val, pos):
    """Insert at 0-based position (0 = head)."""
    if pos == 0:
        return insert_at_head(head, val)
    new_node = ListNode(val)
    cur = head
    for _ in range(pos - 1):
        if not cur:
            raise IndexError("Position out of range")
        cur = cur.next
    new_node.next = cur.next
    cur.next = new_node
    return head


# ── Delete ────────────────────────────────────

def delete_by_value(head, val):
    """Remove the first node whose value equals val."""
    dummy = ListNode(0, head)
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
            break
        cur = cur.next
    return dummy.next


def delete_at_position(head, pos):
    """Remove the node at 0-based position."""
    dummy = ListNode(0, head)
    cur = dummy
    for _ in range(pos):
        if not cur.next:
            raise IndexError("Position out of range")
        cur = cur.next
    cur.next = cur.next.next if cur.next else None
    return dummy.next


# ─────────────────────────────────────────────
#  Classic interview problems
# ─────────────────────────────────────────────

# 1. Reverse ──────────────────────────────────
def reverse_list(head):
    """Iterative reversal – O(n) time, O(1) space."""
    prev = None
    cur = head
    while cur:
        next_node = cur.next
        cur.next = prev
        prev = cur
        cur = next_node
    return prev          # new head


def reverse_list_recursive(head):
    """Recursive reversal – O(n) time, O(n) stack space."""
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head


# 2. Detect cycle (Floyd's tortoise & hare) ───
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


# 3. Find middle node ─────────────────────────
def find_middle(head):
    """Returns the middle node (right-middle for even length)."""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow


# 4. Merge two sorted lists ───────────────────
def merge_sorted(l1, l2):
    dummy = ListNode(0)
    cur = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            cur.next, l1 = l1, l1.next
        else:
            cur.next, l2 = l2, l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next


# 5. Remove nth node from end ─────────────────
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next


# 6. Check if palindrome ──────────────────────
def is_palindrome(head):
    # Step 1: find middle
    mid = find_middle(head)
    # Step 2: reverse second half
    second = reverse_list(mid)
    # Step 3: compare
    p1, p2 = head, second
    result = True
    while p2:
        if p1.val != p2.val:
            result = False
            break
        p1, p2 = p1.next, p2.next
    # Step 4: restore (optional but good practice)
    reverse_list(second)
    return result


# 7. Intersection of two lists ────────────────
def get_intersection(headA, headB):
    """Returns the intersecting node, or None."""
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a


# ─────────────────────────────────────────────
#  collections.deque  (Python's built-in O(1) deque)
# ─────────────────────────────────────────────
from collections import deque

dq = deque([1, 2, 3])
dq.appendleft(0)   # O(1) prepend  → deque([0, 1, 2, 3])
dq.append(4)       # O(1) append   → deque([0, 1, 2, 3, 4])
dq.popleft()       # O(1) remove from front
dq.pop()           # O(1) remove from back


# ─────────────────────────────────────────────
#  Quick demo / smoke tests
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("BUILD & TRAVERSE")
    head = build([1, 2, 3, 4, 5])
    display(head)                          # 1 → 2 → 3 → 4 → 5

    print("\nINSERT at head (0), tail (6), position 2 (99)")
    head = insert_at_head(head, 0)
    head = insert_at_tail(head, 6)
    head = insert_at_position(head, 99, 2)
    display(head)                          # 0 → 1 → 99 → 2 → 3 → 4 → 5 → 6

    print("\nDELETE value 99, position 0")
    head = delete_by_value(head, 99)
    head = delete_at_position(head, 0)
    display(head)                          # 1 → 2 → 3 → 4 → 5 → 6

    print("\nLENGTH:", length(head))       # 6
    print("SEARCH 4:", search(head, 4))    # True
    print("SEARCH 9:", search(head, 9))    # False

    print("\nREVERSE (iterative)")
    head = reverse_list(head)
    display(head)                          # 6 → 5 → 4 → 3 → 2 → 1

    print("\nREVERSE (recursive)")
    head = reverse_list_recursive(head)
    display(head)                          # 1 → 2 → 3 → 4 → 5 → 6

    print("\nMIDDLE NODE:", find_middle(head).val)   # 4

    print("\nREMOVE 2nd from end")
    head = remove_nth_from_end(head, 2)
    display(head)                          # 1 → 2 → 3 → 4 → 6

    print("\nIS PALINDROME?")
    print(is_palindrome(build([1, 2, 3, 2, 1])))   # True
    print(is_palindrome(build([1, 2, 3])))          # False

    print("\nMERGE SORTED LISTS")
    l1 = build([1, 3, 5])
    l2 = build([2, 4, 6])
    display(merge_sorted(l1, l2))          # 1 → 2 → 3 → 4 → 5 → 6

    print("\nHAS CYCLE?")
    nc = build([1, 2, 3])
    print(has_cycle(nc))                   # False
    # create a cycle: tail → node at index 1
    tail = nc
    while tail.next:
        tail = tail.next
    tail.next = nc.next                    # cycle!
    print(has_cycle(nc))                   # True

    print("\ncollections.deque:", list(dq))
    print("=" * 45)
