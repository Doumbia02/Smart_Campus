"""
SMART CAMPUS MANAGEMENT SYSTEM
Data Structures & Algorithms Assignment
Language: Python 3

Run:
    python smart_campus.py

The application demonstrates:
1. Fixed Array and Dynamic Array
2. Singly and Doubly Linked Lists
3. Stack, Queue and Deque
4. Custom Hash Table with Separate Chaining
5. Binary Search Tree (BST)

Benchmark results are measurements from the current computer and Python runtime.
They are illustrative, not universal hardware-independent guarantees.
"""
from time import perf_counter
import random


# ---------------------------------------------------------------------------
# 1. ARRAY AND DYNAMIC ARRAY
# ---------------------------------------------------------------------------

class FixedArray:
    """A fixed-capacity array. Insertion/deletion in the middle shifts elements."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = [None] * capacity
        self.size = 0

    def insert(self, index, value):
        if self.size >= self.capacity:
            raise OverflowError("FixedArray is full")
        if index < 0 or index > self.size:
            raise IndexError("Invalid insertion index")
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.size += 1

    def append(self, value):
        self.insert(self.size, value)

    def delete(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Invalid deletion index")
        removed = self.data[index]
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
        self.data[self.size] = None
        return removed

    def search(self, value):
        for i in range(self.size):
            if self.data[i] == value:
                return i
        return -1

    def __len__(self):
        return self.size


class DynamicArray:
    """Resizable array. Capacity doubles when full and halves when sparsely used."""

    def __init__(self):
        self.capacity = 2
        self.size = 0
        self.data = [None] * self.capacity

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self.size):
            new_data[i] = self.data[i]
        self.data = new_data
        self.capacity = new_capacity

    def insert(self, index, value):
        if index < 0 or index > self.size:
            raise IndexError("Invalid insertion index")
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]
        self.data[index] = value
        self.size += 1

    def append(self, value):
        self.insert(self.size, value)

    def delete(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Invalid deletion index")
        removed = self.data[index]
        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]
        self.size -= 1
        self.data[self.size] = None
        if self.capacity > 2 and self.size <= self.capacity // 4:
            self._resize(max(2, self.capacity // 2))
        return removed

    def search(self, value):
        for i in range(self.size):
            if self.data[i] == value:
                return i
        return -1

    def __len__(self):
        return self.size


# ---------------------------------------------------------------------------
# 2. SINGLY AND DOUBLY LINKED LISTS
# ---------------------------------------------------------------------------

class SNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, value):
        node = SNode(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self.size += 1

    def prepend(self, value):
        node = SNode(value)
        node.next = self.head
        self.head = node
        self.size += 1

    def search(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def delete(self, value):
        previous = None
        current = self.head
        while current:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                self.size -= 1
                return True
            previous, current = current, current.next
        return False

    def values(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, value):
        node = DNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def prepend(self, value):
        node = DNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self.size += 1

    def search(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def delete(self, value):
        current = self.head
        while current and current.value != value:
            current = current.next
        if current is None:
            return False
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        self.size -= 1
        return True

    def values(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def reverse_values(self):
        result = []
        current = self.tail
        while current:
            result.append(current.value)
            current = current.prev
        return result


# ---------------------------------------------------------------------------
# 3. STACK, QUEUE AND DEQUE
# ---------------------------------------------------------------------------

class Stack:
    """Last-In, First-Out. Used for undo history."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.items:
            raise IndexError("Stack is empty")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    """First-In, First-Out. Uses a linked list to avoid front-shifting."""
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, item):
        node = SNode(item)
        if self.rear is None:
            self.front = self.rear = node
        else:
            self.rear.next = node
            self.rear = node

    def dequeue(self):
        if self.front is None:
            raise IndexError("Queue is empty")
        item = self.front.value
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return item

    def is_empty(self):
        return self.front is None


class Deque:
    """Double-ended queue: insertion/removal are supported at both ends."""
    def __init__(self):
        self.items = []

    def add_front(self, item):
        self.items.insert(0, item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if not self.items:
            raise IndexError("Deque is empty")
        return self.items.pop(0)

    def remove_rear(self):
        if not self.items:
            raise IndexError("Deque is empty")
        return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0


# ---------------------------------------------------------------------------
# 4. CUSTOM HASH TABLE USING SEPARATE CHAINING
# ---------------------------------------------------------------------------

class HashTable:
    """Each bucket stores a list (chain) of key-value pairs."""

    def __init__(self, capacity=11):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _index(self, key):
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._index(key)
        chain = self.buckets[index]
        for i, (existing_key, _) in enumerate(chain):
            if existing_key == key:
                chain[i] = (key, value)
                return
        chain.append((key, value))
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._rehash()

    def get(self, key):
        for existing_key, value in self.buckets[self._index(key)]:
            if existing_key == key:
                return value
        return None

    def delete(self, key):
        chain = self.buckets[self._index(key)]
        for i, (existing_key, _) in enumerate(chain):
            if existing_key == key:
                del chain[i]
                self.size -= 1
                return True
        return False

    def _rehash(self):
        old_items = []
        for chain in self.buckets:
            old_items.extend(chain)
        self.capacity = self.capacity * 2 + 1
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        for key, value in old_items:
            self.put(key, value)

    def show_chains(self):
        for i, chain in enumerate(self.buckets):
            if chain:
                print(f"Bucket {i}: {chain}")


# ---------------------------------------------------------------------------
# 5. BINARY SEARCH TREE
# ---------------------------------------------------------------------------

class BSTNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Unbalanced BST. Smaller keys go left; larger keys go right."""

    def __init__(self):
        self.root = None

    def insert(self, key, value=None):
        if self.root is None:
            self.root = BSTNode(key, value)
            return
        current = self.root
        while True:
            if key == current.key:
                current.value = value
                return
            if key < current.key:
                if current.left is None:
                    current.left = BSTNode(key, value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(key, value)
                    return
                current = current.right

    def search(self, key):
        current = self.root
        while current:
            if key == current.key:
                return current.value
            current = current.left if key < current.key else current.right
        return None

    def _delete_node(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_node(node.left, key)
        elif key > node.key:
            node.right = self._delete_node(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = node.right
            while successor.left:
                successor = successor.left
            node.key, node.value = successor.key, successor.value
            node.right = self._delete_node(node.right, successor.key)
        return node

    def delete(self, key):
        existed = self.search(key) is not None
        self.root = self._delete_node(self.root, key)
        return existed

    def inorder(self):
        result = []
        def walk(node):
            if node:
                walk(node.left)
                result.append((node.key, node.value))
                walk(node.right)
        walk(self.root)
        return result

    def height(self):
        def get_height(node):
            if node is None:
                return 0
            return 1 + max(get_height(node.left), get_height(node.right))
        return get_height(self.root)


# ---------------------------------------------------------------------------
# APPLICATION LAYER
# ---------------------------------------------------------------------------

class SmartCampusApp:
    def __init__(self):
        self.students = {}  # primary application records: ID -> name
        self.student_ids = DynamicArray()
        self.student_history = DoublyLinkedList()
        self.student_index = HashTable()
        self.student_tree = BinarySearchTree()
        self.undo_stack = Stack()
        self.service_queue = Queue()
        self.priority_deque = Deque()

    def add_student(self):
        student_id = input("Student ID: ").strip()
        name = input("Student name: ").strip()
        if not student_id or not name:
            print("ID and name are required.")
            return
        if self.student_index.get(student_id) is not None:
            print("That student ID already exists.")
            return
        self.students[student_id] = name
        self.student_ids.append(student_id)
        self.student_history.append(f"Added {student_id}: {name}")
        self.student_index.put(student_id, name)
        self.student_tree.insert(student_id, name)
        self.undo_stack.push(("add", student_id, name))
        print("Student added.")

    def find_student(self):
        student_id = input("Enter student ID: ").strip()
        name = self.student_index.get(student_id)
        if name is None:
            print("Student not found.")
        else:
            print(f"Found: {student_id} - {name}")

    def delete_student(self):
        student_id = input("Student ID to delete: ").strip()
        name = self.student_index.get(student_id)
        if name is None:
            print("Student not found.")
            return
        del self.students[student_id]
        self.student_index.delete(student_id)
        self.student_tree.delete(student_id)
        index = self.student_ids.search(student_id)
        if index != -1:
            self.student_ids.delete(index)
        self.student_history.append(f"Deleted {student_id}: {name}")
        self.undo_stack.push(("delete", student_id, name))
        print("Student deleted.")

    def undo(self):
        if self.undo_stack.is_empty():
            print("Nothing to undo.")
            return
        action, student_id, name = self.undo_stack.pop()
        if action == "add":
            self.students.pop(student_id, None)
            self.student_index.delete(student_id)
            self.student_tree.delete(student_id)
            index = self.student_ids.search(student_id)
            if index != -1:
                self.student_ids.delete(index)
            print("Last student addition undone.")
        else:
            self.students[student_id] = name
            self.student_ids.append(student_id)
            self.student_index.put(student_id, name)
            self.student_tree.insert(student_id, name)
            print("Last student deletion undone.")

    def show_students(self):
        if not self.students:
            print("No students registered.")
            return
        print("\nRegistered students:")
        for student_id, name in sorted(self.students.items()):
            print(f"  {student_id}: {name}")

    def add_service_request(self):
        request = input("Describe service request: ").strip()
        if request:
            self.service_queue.enqueue(request)
            print("Request added to the end of the queue.")

    def process_service_request(self):
        if self.service_queue.is_empty():
            print("No pending service requests.")
        else:
            print("Processing:", self.service_queue.dequeue())

    def add_priority_request(self):
        request = input("Describe priority request: ").strip()
        if request:
            side = input("Add to front (F) or rear (R)? ").strip().upper()
            if side == "F":
                self.priority_deque.add_front(request)
            else:
                self.priority_deque.add_rear(request)
            print("Priority request added.")

    def process_priority_request(self):
        if self.priority_deque.is_empty():
            print("No priority requests.")
            return
        side = input("Process front (F) or rear (R)? ").strip().upper()
        if side == "R":
            print("Processing:", self.priority_deque.remove_rear())
        else:
            print("Processing:", self.priority_deque.remove_front())

    def show_bst(self):
        print("BST inorder (student IDs in sorted order):")
        print(self.student_tree.inorder())
        print("Tree height:", self.student_tree.height())
        print("Note: sorted insertion can create a one-sided tree.")

    def list_demo(self):
        print("Activity history (oldest to newest):")
        print(self.student_history.values())
        print("Doubly linked history (newest to oldest):")
        print(self.student_history.reverse_values())

    def benchmark_menu(self):
        run_benchmarks()


# ---------------------------------------------------------------------------
# BENCHMARKING
# ---------------------------------------------------------------------------

def timed_average(function, repeats=3):
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        function()
        samples.append(perf_counter() - start)
    return sum(samples) / len(samples)


def benchmark_arrays(n):
    values = list(range(n))
    middle = n // 2

    def fixed_insert():
        a = FixedArray(n + 1)
        for value in values:
            a.append(value)
        a.insert(middle, -1)

    def dynamic_insert():
        a = DynamicArray()
        for value in values:
            a.append(value)
        a.insert(middle, -1)

    def fixed_delete():
        a = FixedArray(n)
        for value in values:
            a.append(value)
        a.delete(middle)

    def dynamic_delete():
        a = DynamicArray()
        for value in values:
            a.append(value)
        a.delete(middle)

    def fixed_search():
        a = FixedArray(n)
        for value in values:
            a.append(value)
        a.search(n - 1)

    def dynamic_search():
        a = DynamicArray()
        for value in values:
            a.append(value)
        a.search(n - 1)

    return {
        "Fixed Array": (
            timed_average(fixed_insert),
            timed_average(fixed_delete),
            timed_average(fixed_search),
        ),
        "Dynamic Array": (
            timed_average(dynamic_insert),
            timed_average(dynamic_delete),
            timed_average(dynamic_search),
        ),
    }


def benchmark_linked_lists(n):
    values = list(range(n))
    target = n - 1

    def sll_append():
        linked = SinglyLinkedList()
        for value in values:
            linked.append(value)

    def dll_append():
        linked = DoublyLinkedList()
        for value in values:
            linked.append(value)

    def sll_search():
        linked = SinglyLinkedList()
        for value in values:
            linked.append(value)
        linked.search(target)

    def dll_search():
        linked = DoublyLinkedList()
        for value in values:
            linked.append(value)
        linked.search(target)

    def sll_delete():
        linked = SinglyLinkedList()
        for value in values:
            linked.append(value)
        linked.delete(target)

    def dll_delete():
        linked = DoublyLinkedList()
        for value in values:
            linked.append(value)
        linked.delete(target)

    return {
        "Singly Linked List": (
            timed_average(sll_append), timed_average(sll_search), timed_average(sll_delete)
        ),
        "Doubly Linked List": (
            timed_average(dll_append), timed_average(dll_search), timed_average(dll_delete)
        ),
    }


def run_benchmarks():
    print("\nPERFORMANCE BENCHMARK")
    print("Times are seconds; each measurement is averaged over 3 runs.")
    print("\nARRAYS: insertion-at-middle / deletion-at-middle / search-last")
    for n in (100, 1000, 10000):
        results = benchmark_arrays(n)
        print(f"\nN = {n}")
        for name, times in results.items():
            print(f"{name:16} insert={times[0]:.6f} delete={times[1]:.6f} search={times[2]:.6f}")

    print("\nLINKED LISTS: append-all / search-last / delete-last")
    for n in (100, 1000, 5000):
        results = benchmark_linked_lists(n)
        print(f"\nN = {n}")
        for name, times in results.items():
            print(f"{name:20} append={times[0]:.6f} search={times[1]:.6f} delete={times[2]:.6f}")

    print("\nBST SHAPE EXPERIMENT")
    n = 15
    sorted_tree = BinarySearchTree()
    shuffled_tree = BinarySearchTree()
    for value in range(n):
        sorted_tree.insert(value, str(value))
    random_values = list(range(n))
    random.shuffle(random_values)
    for value in random_values:
        shuffled_tree.insert(value, str(value))
    print(f"Sorted insertion order 0..{n-1}: height = {sorted_tree.height()}")
    print(f"Shuffled insertion order: height = {shuffled_tree.height()}")
    print("A sorted sequence makes this unbalanced BST degenerate into a chain.")
    print("Search can approach O(n), instead of average O(log n) for a balanced tree.")


def self_test():
    # Basic checks to verify that the custom implementations work.
    a = FixedArray(3)
    a.append(1); a.insert(1, 9); assert a.search(9) == 1; assert a.delete(1) == 9

    d = DynamicArray()
    for x in range(20):
        d.append(x)
    assert d.search(19) == 19
    assert d.delete(10) == 10

    s = SinglyLinkedList()
    s.append(1); s.append(2); assert s.delete(1); assert s.search(2) == 0

    dl = DoublyLinkedList()
    dl.append(1); dl.append(2); assert dl.reverse_values() == [2, 1]
    assert dl.delete(1)

    st = Stack(); st.push("x"); assert st.pop() == "x"
    q = Queue(); q.enqueue("x"); assert q.dequeue() == "x"
    dq = Deque(); dq.add_front(1); dq.add_rear(2)
    assert dq.remove_front() == 1 and dq.remove_rear() == 2

    ht = HashTable(3)
    ht.put("A", "Alice"); ht.put("B", "Bob")
    assert ht.get("A") == "Alice"; assert ht.delete("B")

    bst = BinarySearchTree()
    for x in (8, 3, 10, 1, 6, 14, 4, 7, 13):
        bst.insert(x, str(x))
    assert bst.search(6) == "6"
    assert bst.delete(3)
    assert [key for key, _ in bst.inorder()] == [1, 4, 6, 7, 8, 10, 13, 14]
    print("All self-tests passed.")


def main():
    app = SmartCampusApp()
    self_test()

    while True:
        print("\n" + "=" * 48)
        print("       SMART CAMPUS MANAGEMENT SYSTEM")
        print("=" * 48)
        print("1. Add student")
        print("2. Find student (custom hash table)")
        print("3. Delete student")
        print("4. Undo last student change (stack)")
        print("5. Display students")
        print("6. Show activity history (doubly linked list)")
        print("7. Add service request (queue)")
        print("8. Process service request (queue)")
        print("9. Add priority request (deque)")
        print("10. Process priority request (deque)")
        print("11. Display BST")
        print("12. Run performance benchmarks")
        print("0. Exit")
        choice = input("Select an option: ").strip()

        actions = {
            "1": app.add_student,
            "2": app.find_student,
            "3": app.delete_student,
            "4": app.undo,
            "5": app.show_students,
            "6": app.list_demo,
            "7": app.add_service_request,
            "8": app.process_service_request,
            "9": app.add_priority_request,
            "10": app.process_priority_request,
            "11": app.show_bst,
            "12": app.benchmark_menu,
        }

        if choice == "0":
            print("Thank you for using Smart Campus Management System.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
