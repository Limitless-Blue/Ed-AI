# Queue

## Table of Contents
1. [Implementation of Queues](#implementation-of-queues)
   1. [Using Arrays](#using-arrays)
   2. [Using Linked Lists](#using-linked-lists)
2. [Queue Operations](#queue-operations)
   1. [Enqueue](#enqueue)
   2. [Dequeue](#dequeue)
   3. [Front/Rear Access](#frontrear-access)
   4. [IsEmpty](#isempty)

---

## Implementation of Queues

Queues can be implemented using different data structures such as arrays and linked lists. Each implementation has its advantages and disadvantages, which may influence the choice based on specific requirements.

### Using Arrays

An array-based queue uses a fixed-size array where elements are added at one end (rear) and removed from the other end (front). However, this implementation has certain limitations such as the need for resizing the array when it's full or inefficient memory use when elements are dequeued without shifting the elements.

#### Example:

```python
class ArrayQueue:
    def __init__(self, capacity):
        self.queue = [None] * capacity
        self.capacity = capacity
        self.front = 0
        self.rear = -1
        self.size = 0

    def enqueue(self, item):
        if self.size == self.capacity:
            raise OverflowError("Queue is full")
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = item
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return item

    def is_empty(self):
        return self.size == 0

    def front_element(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[self.front]

    def rear_element(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.queue[self.rear]

# Example Usage
queue = ArrayQueue(3)
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)
print(queue.dequeue())  # Output: 10
```

In this implementation:
- Enqueue adds an element to the rear, while dequeue removes an element from the front.
- The queue is circular to utilize space efficiently, meaning when the rear pointer reaches the end, it wraps around to the front.

### Using Linked Lists

A linked list-based queue uses dynamic memory allocation, allowing the queue to grow and shrink as needed. A linked list consists of nodes, where each node stores data and a reference to the next node. This implementation is more flexible than arrays but requires more memory to store node references.

#### Example:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return item

    def is_empty(self):
        return self.front is None

    def front_element(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.front.data

    def rear_element(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self.rear.data

# Example Usage
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)
print(queue.dequeue())  # Output: 10
```

In this implementation:
- Enqueue adds a node to the rear, and dequeue removes a node from the front.
- Memory usage is dynamic, so there’s no need to specify the size of the queue beforehand.

---

## Queue Operations

Queues operate based on the First-In, First-Out (FIFO) principle. The following are the basic operations on queues:

### Enqueue

**Enqueue** is the operation of adding an element to the rear of the queue. This ensures that new elements are always added after the last element currently in the queue.

#### Example (Using Array):

```python
queue = ArrayQueue(3)
queue.enqueue(10)  # Adds 10 to the queue
queue.enqueue(20)  # Adds 20 to the queue
```

#### Example (Using Linked List):

```python
queue = LinkedListQueue()
queue.enqueue(10)  # Adds 10 to the queue
queue.enqueue(20)  # Adds 20 to the queue
```

### Dequeue

**Dequeue** is the operation of removing an element from the front of the queue. This is the opposite of enqueue, where the first element that was added is the first one to be removed.

#### Example (Using Array):

```python
queue = ArrayQueue(3)
queue.enqueue(10)
queue.enqueue(20)
print(queue.dequeue())  # Removes 10 from the queue, Output: 10
```

#### Example (Using Linked List):

```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
print(queue.dequeue())  # Removes 10 from the queue, Output: 10
```

### Front/Rear Access

In queue operations, you may need to access the element at the front or rear of the queue without removing it. This can be done using the `front_element()` and `rear_element()` methods.

#### Example (Using Array):

```python
queue = ArrayQueue(3)
queue.enqueue(10)
queue.enqueue(20)
print(queue.front_element())  # Output: 10
print(queue.rear_element())   # Output: 20
```

#### Example (Using Linked List):

```python
queue = LinkedListQueue()
queue.enqueue(10)
queue.enqueue(20)
print(queue.front_element())  # Output: 10
print(queue.rear_element())   # Output: 20
```

### IsEmpty

**IsEmpty** checks whether the queue is empty. It returns `True` if the queue has no elements and `False` if there are elements in the queue.

#### Example (Using Array):

```python
queue = ArrayQueue(3)
print(queue.is_empty())  # Output: True
queue.enqueue(10)
print(queue.is_empty())  # Output: False
```

#### Example (Using Linked List):

```python
queue = LinkedListQueue()
print(queue.is_empty())  # Output: True
queue.enqueue(10)
print(queue.is_empty())  # Output: False
```

---

Queues are essential data structures in computing, used for scheduling tasks, managing processes, and maintaining order in various applications such as print jobs, process management in operating systems, and handling requests in web servers.