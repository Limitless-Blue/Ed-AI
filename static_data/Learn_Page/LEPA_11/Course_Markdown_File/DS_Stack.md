# Table of Contents
1. [Introduction to Stacks](#introduction-to-stacks)
   1. [Definition and Properties](#definition-and-properties)
   2. [LIFO Principle Explained](#lifo-principle-explained)
2. [Implementation](#implementation)
   1. [Using Arrays](#using-arrays)
   2. [Using Linked Lists](#using-linked-lists)

---

## Introduction to Stacks

### Definition and Properties

A **stack** is a linear data structure that follows a particular order in which operations are performed. The order may be **Last In First Out (LIFO)** or **First In Last Out (FILO)**. Stacks are used to store a collection of elements, with two main operations:

1. **Push**: Adding an element to the top of the stack.
2. **Pop**: Removing the topmost element from the stack.

Stacks are commonly used in various applications such as:
- Expression evaluation and syntax parsing (e.g., in calculators, compilers).
- Backtracking algorithms (e.g., depth-first search).
- Undo mechanisms in text editors.
  
#### Key properties of a stack:
- **Last In First Out (LIFO)**: The most recent element added is the first one to be removed.
- **Size**: A stack has a finite capacity, though it may grow dynamically.
- **Top Element**: The only accessible element in the stack is the one at the top.

```text
Example:
Imagine a stack of plates. The last plate added to the stack is the first one to be taken off.
```

### LIFO Principle Explained

The LIFO principle stands for **Last In, First Out**, which means the last element pushed onto the stack will be the first one to be popped off.

Consider an example:
- You start with an empty stack.
- You push `A`, `B`, and `C` onto the stack.
- The stack now looks like: `C` (top), `B`, `A`.
- When you pop an element, `C` is removed first, followed by `B`, and finally `A`.

```text
Illustration:
Push A -> Push B -> Push C
Stack: [A, B, C]

Pop -> C is removed
Stack: [A, B]

Pop -> B is removed
Stack: [A]

Pop -> A is removed
Stack: []
```

---

## Implementation

Stacks can be implemented using various data structures, including arrays and linked lists. Both implementations have their own advantages and limitations.

### Using Arrays

An array-based stack uses a fixed-size array, which makes it efficient in terms of memory access but requires careful management of the stack's size. If the stack grows beyond the array's capacity, you must resize the array.

#### Example: Stack Implementation using Arrays in Python

```python
class StackArray:
    def __init__(self, size):
        self.stack = [None] * size  # Initialize the array with a fixed size
        self.top = -1  # Top points to the last element added; -1 means stack is empty
        self.size = size

    def push(self, item):
        if self.top >= self.size - 1:
            raise OverflowError("Stack overflow!")
        self.top += 1
        self.stack[self.top] = item

    def pop(self):
        if self.top == -1:
            raise IndexError("Stack underflow!")
        item = self.stack[self.top]
        self.stack[self.top] = None  # Clear the value
        self.top -= 1
        return item

    def peek(self):
        if self.top == -1:
            return None
        return self.stack[self.top]

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == self.size - 1

# Usage Example
stack = StackArray(3)
stack.push(10)
stack.push(20)
stack.push(30)

print(stack.pop())  # Output: 30
print(stack.pop())  # Output: 20
```

#### Advantages of Array-based Stack:
- Constant time complexity **O(1)** for both push and pop operations (except during resizing if necessary).
- Simple and easy to implement.

#### Disadvantages:
- Fixed size (though dynamic arrays can mitigate this).
- Resizing an array can be costly in terms of performance.

### Using Linked Lists

A stack can also be implemented using a linked list. In this case, each element in the stack is represented by a node that points to the next node. This allows the stack to grow dynamically without the need for resizing.

#### Example: Stack Implementation using Linked Lists in Python

```python
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class StackLinkedList:
    def __init__(self):
        self.top = None  # Initially, the stack is empty

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top  # Link the new node to the previous top
        self.top = new_node  # Update the top pointer

    def pop(self):
        if self.top is None:
            raise IndexError("Stack underflow!")
        item = self.top.value
        self.top = self.top.next  # Move the top pointer down
        return item

    def peek(self):
        if self.top is None:
            return None
        return self.top.value

    def is_empty(self):
        return self.top is None

# Usage Example
stack = StackLinkedList()
stack.push(10)
stack.push(20)
stack.push(30)

print(stack.pop())  # Output: 30
print(stack.pop())  # Output: 20
```

#### Advantages of Linked List-based Stack:
- Dynamic size: The stack can grow and shrink as needed without predefining its size.
- Efficient memory usage: No need for resizing arrays or allocating memory in advance.

#### Disadvantages:
- Each node requires extra memory for the pointer to the next node.
- Slightly slower than arrays because of pointer manipulation.

---

In summary, stacks are a versatile data structure that can be implemented using either arrays or linked lists depending on the specific requirements of the problem. Arrays offer quick access and simple memory management, while linked lists provide more flexibility in terms of dynamic resizing at the cost of extra memory and processing overhead.