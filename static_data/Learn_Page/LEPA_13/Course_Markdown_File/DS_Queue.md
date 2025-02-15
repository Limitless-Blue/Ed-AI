# Table of Contents
1. [Introduction to Queues](#introduction-to-queues)
   1. [Definition and Properties](#definition-and-properties)
   2. [FIFO Principle Explained](#fifo-principle-explained)
2. [Types of Queues](#types-of-queues)
   1. [Simple Queue](#simple-queue)
   2. [Circular Queue](#circular-queue)
   3. [Priority Queue](#priority-queue)

---

## Introduction to Queues

### Definition and Properties

A **queue** is a linear data structure that stores elements in a First In, First Out (FIFO) manner. This means that the first element added to the queue will be the first one to be removed. Queues are widely used in computing where data needs to be managed in a temporal order, such as in service requests, printer jobs, or tasks scheduling.

#### Key properties of a queue:
- **FIFO (First In First Out)**: The order of elements is preserved, with the oldest elements being processed first.
- **Enqueue**: The operation of adding an element to the back of the queue.
- **Dequeue**: The operation of removing an element from the front of the queue.
- **Front and Rear**: Terms used to describe the first and last elements of the queue, respectively.

### FIFO Principle Explained

The FIFO (First In, First Out) principle is fundamental to queue operations. It ensures that elements are processed in the exact sequence in which they are added.

#### Example:
Imagine a line of people waiting to buy tickets; the first person in the line is the first to get serviced.

```text
Queue operations:
Enqueue('Alice')
Enqueue('Bob')
Enqueue('Charlie')
```

When dequeue operations are performed:

```text
Dequeue() -> 'Alice'
Dequeue() -> 'Bob'
Dequeue() -> 'Charlie'
```

Alice, who was first in line, is served first, followed by Bob and Charlie, respectively.

---

## Types of Queues

### Simple Queue

A **simple queue** enforces the basic principles of FIFO without any variations. It's a straightforward implementation where elements are added at the rear and removed from the front.

#### Implementation Example in Python:
```python
class SimpleQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        raise IndexError("dequeue from empty queue")

    def is_empty(self):
        return len(self.queue) == 0

# Example usage:
queue = SimpleQueue()
queue.enqueue(1)
queue.enqueue(2)
queue.dequeue()  # returns 1
```

### Circular Queue

A **circular queue** is a more complex structure where the end of the queue wraps around to the front when there is available space. This setup helps in efficient utilization of storage by not wasting the space of removed elements.

#### Implementation Example in Python:
```python
class CircularQueue:
    def __init__(self, size):
        self.queue = [None] * size
        self.max_size = size
        self.head = 0
        self.tail = 0
        self.count = 0

    def enqueue(self, item):
        if self.count == self.max_size:
            raise IndexError("queue full")
        self.queue[self.tail] = item
        self.tail = (self.tail + 1) % self.max_size
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        item = self.queue[self.head]
        self.queue[self.head] = None
        self.head = (self.head + 1) % self.max_size
        self.count -= 1
        return item

    def is_empty(self):
        return self.count == 0

# Example usage:
c_queue = CircularQueue(3)
c_queue.enqueue(1)
c_queue.enqueue(2)
c_queue.dequeue()  # returns 1
```

### Priority Queue

A **priority queue** is a type of queue where each element is associated with a priority, and elements are dequeued based on their priority level. Higher priority elements are removed from the queue before lower priority ones.

#### Implementation Example in Python:
```python
import heapq

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def enqueue(self, item, priority):
        heapq.heappush(self.heap, (priority, item))

    def dequeue(self):
        if not self.is_empty():
            return heapq.heappop(self.heap)[1]
        raise IndexError("dequeue from empty queue")

    def is_empty(self):
        return len(self.heap) == 0

# Example usage:
p_queue = PriorityQueue()
p_queue.enqueue('task1', 1)
p_queue.enqueue('task2', 2)
p_queue.dequeue()  # returns 'task1' because it has a higher priority
```

---
Queues play a critical role in managing processes in operating systems, handling asynchronous data (like IO buffers), and prioritizing tasks in numerous algorithms. The type of queue implemented can significantly affect the efficiency and complexity of the solution.