# Table of Contents
1. [Stack Operations](#stack-operations)
   1. [Push](#push)
   2. [Pop](#pop)
   3. [Peek/Top](#peektop)
   4. [IsEmpty](#isempty)

---

## Stack Operations

Stacks are dynamic data structures that follow the Last In, First Out (LIFO) principle. Here, we discuss the primary operations associated with stacks.

### Push

The **Push** operation adds an element to the top of the stack. This is the only way to insert new elements into a stack. 

#### Example:
Let's consider a stack of integers. Initially, the stack is empty. We push the numbers 1, 2, and 3 onto the stack in that order.

```text
Stack: []
Push(1)
Stack: [1]
Push(2)
Stack: [1, 2]
Push(3)
Stack: [1, 2, 3]
```

In Python, a simple implementation of push might look like this:

```python
def push(stack, item):
    stack.append(item)
```

### Pop

The **Pop** operation removes the top element from the stack and returns it. This operation modifies the stack, and if performed on an empty stack, it should indicate an underflow condition, typically through an error or exception.

#### Example:
Continuing from the previous stack, we now perform a pop operation:

```text
Current Stack: [1, 2, 3]
Pop()
Stack becomes: [1, 2]
```

In Python, a pop function could be implemented as follows:

```python
def pop(stack):
    if not stack:
        raise IndexError("pop from empty stack")
    return stack.pop()
```

### Peek/Top

The **Peek** or **Top** operation allows inspection of the top element of the stack without removing it. This is useful for checking the top value before deciding to perform a pop operation.

#### Example:
For the stack `[1, 2]`, a peek operation would return `2` without altering the stack.

```text
Current Stack: [1, 2]
Peek() -> 2
Stack remains: [1, 2]
```

Python implementation:

```python
def peek(stack):
    if not stack:
        return None
    return stack[-1]
```

### IsEmpty

The **IsEmpty** operation checks if the stack is empty. This is essential for preventing stack underflows caused by popping an empty stack.

#### Example:
We need to check if our current stack is empty or not.

```text
Stack: [1, 2]
IsEmpty() -> False

Stack: []
IsEmpty() -> True
```

Python function to check if a stack is empty:

```python
def is_empty(stack):
    return len(stack) == 0
```

---
Each of these operations plays a vital role in using and managing stacks effectively, whether in simple data management scenarios or more complex algorithmic contexts.
