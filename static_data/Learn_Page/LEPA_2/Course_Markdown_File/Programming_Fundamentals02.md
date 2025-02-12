# Programming Fundamentals

## Table of Contents
1. [Variables and Data Types](#21-variables-and-data-types)
    - [Introduction to Variables](#introduction-to-variables)
    - [Common Data Types (Integers, Floats, Characters, Booleans)](#common-data-types-integers-floats-characters-booleans)
    - [Type Conversion and Casting](#type-conversion-and-casting)

2. [Operators and Expressions](#22-operators-and-expressions)
    - [Arithmetic Operators](#arithmetic-operators)
    - [Logical Operators](#logical-operators)
    - [Relational Operators](#relational-operators)
    - [Bitwise Operators](#bitwise-operators)
    - [Operator Precedence and Associativity](#operator-precedence-and-associativity)

---

## 2.2 Operators and Expressions

Operators and expressions are fundamental concepts in programming that allow developers to perform computations, make decisions, and manipulate data. Understanding the various types of operators and how they interact within expressions is crucial for writing effective and efficient code.

### Arithmetic Operators

**Arithmetic Operators** perform mathematical calculations between numeric operands. They are essential for tasks such as computations, data analysis, and algorithm implementation.

- **Addition (`+`)**
  - **Description:** Adds two operands.
  - **Example:**
    ```python
    a = 10
    b = 5
    result = a + b  # result is 15
    ```
  
- **Subtraction (`-`)**
  - **Description:** Subtracts the second operand from the first.
  - **Example:**
    ```java
    int a = 10;
    int b = 5;
    int result = a - b;  // result is 5
    ```
  
- **Multiplication (`*`)**
  - **Description:** Multiplies two operands.
  - **Example:**
    ```python
    a = 10
    b = 5
    result = a * b  # result is 50
    ```
  
- **Division (`/`)**
  - **Description:** Divides the first operand by the second.
  - **Example:**
    ```python
    a = 10
    b = 5
    result = a / b  # result is 2.0
    ```
  
- **Modulus (`%`)**
  - **Description:** Returns the remainder of division between two operands.
  - **Example:**
    ```java
    int a = 10;
    int b = 3;
    int result = a % b;  // result is 1
    ```
  
- **Exponentiation (`**` or `^`)**
  - **Description:** Raises the first operand to the power of the second.
  - **Example:**
    ```python
    a = 2
    b = 3
    result = a ** b  # result is 8
    ```

**Operator Precedence in Arithmetic Operations:**

Operators have a specific order in which they are evaluated, known as precedence. Parentheses can be used to override the default precedence.

```python
# Without parentheses
result = 10 + 5 * 2  # result is 20

# With parentheses
result = (10 + 5) * 2  # result is 30
```

### Logical Operators

**Logical Operators** are used to combine multiple boolean expressions or conditions. They are essential for controlling the flow of a program based on multiple criteria.

- **AND (`&&` or `and`)**
  - **Description:** Returns `True` if both operands are `True`.
  - **Example:**
    ```python
    a = True
    b = False
    result = a and b  # result is False
    ```
  
- **OR (`||` or `or`)**
  - **Description:** Returns `True` if at least one operand is `True`.
  - **Example:**
    ```java
    boolean a = true;
    boolean b = false;
    boolean result = a || b;  // result is true
    ```
  
- **NOT (`!` or `not`)**
  - **Description:** Inverts the boolean value of the operand.
  - **Example:**
    ```python
    a = True
    result = not a  # result is False
    ```

**Short-Circuit Evaluation:**

Logical operators often use short-circuit evaluation, where the second operand is evaluated only if necessary.

```python
# AND operator
result = (a == 10) and (b == 5)
# If a != 10, b == 5 is not evaluated.

# OR operator
result = (a == 10) or (b == 5)
# If a == 10, b == 5 is not evaluated.
```

### Relational Operators

**Relational Operators** compare two operands and return a boolean result based on the relationship between them. They are commonly used in conditional statements and loops.

- **Equal to (`==`)**
  - **Description:** Checks if two operands are equal.
  - **Example:**
    ```python
    a = 5
    b = 5
    result = (a == b)  # result is True
    ```
  
- **Not Equal to (`!=`)**
  - **Description:** Checks if two operands are not equal.
  - **Example:**
    ```java
    int a = 5;
    int b = 10;
    boolean result = (a != b);  // result is true
    ```
  
- **Greater than (`>`)**
  - **Description:** Checks if the first operand is greater than the second.
  - **Example:**
    ```python
    a = 10
    b = 5
    result = (a > b)  # result is True
    ```
  
- **Less than (`<`)**
  - **Description:** Checks if the first operand is less than the second.
  - **Example:**
    ```java
    int a = 5;
    int b = 10;
    boolean result = (a < b);  // result is true
    ```
  
- **Greater than or Equal to (`>=`)**
  - **Description:** Checks if the first operand is greater than or equal to the second.
  - **Example:**
    ```python
    a = 10
    b = 10
    result = (a >= b)  # result is True
    ```
  
- **Less than or Equal to (`<=`)**
  - **Description:** Checks if the first operand is less than or equal to the second.
  - **Example:**
    ```java
    int a = 5;
    int b = 10;
    boolean result = (a <= b);  // result is true
    ```

### Bitwise Operators

**Bitwise Operators** perform operations on the binary representations of integers. They are useful for low-level programming, such as manipulating individual bits within data.

- **AND (`&`)**
  - **Description:** Performs a bitwise AND operation.
  - **Example:**
    ```python
    a = 5  # 0101
    b = 3  # 0011
    result = a & b  # result is 1 (0001)
    ```
  
- **OR (`|`)**
  - **Description:** Performs a bitwise OR operation.
  - **Example:**
    ```java
    int a = 5;  // 0101
    int b = 3;  // 0011
    int result = a | b;  // result is 7 (0111)
    ```
  
- **XOR (`^`)**
  - **Description:** Performs a bitwise XOR operation.
  - **Example:**
    ```python
    a = 5  # 0101
    b = 3  # 0011
    result = a ^ b  # result is 6 (0110)
    ```
  
- **NOT (`~`)**
  - **Description:** Performs a bitwise NOT operation (inversion).
  - **Example:**
    ```java
    int a = 5;  // 0101
    int result = ~a;  // result is -6 (in two's complement)
    ```
  
- **Left Shift (`<<`)**
  - **Description:** Shifts the bits of the first operand to the left by the number of positions specified by the second operand.
  - **Example:**
    ```python
    a = 5  # 0101
    result = a << 1  # result is 10 (1010)
    ```
  
- **Right Shift (`>>`)**
  - **Description:** Shifts the bits of the first operand to the right by the number of positions specified by the second operand.
  - **Example:**
    ```java
    int a = 5;  // 0101
    int result = a >> 1;  // result is 2 (0010)
    ```

**Use Cases for Bitwise Operators:**

- **Performance Optimization:** Bitwise operations are faster and can be used for optimizing performance-critical sections of code.
- **Cryptography:** Manipulating bits is fundamental in encryption and decryption algorithms.
- **Networking:** Handling IP addresses and subnet masks often requires bitwise operations.
- **Embedded Systems:** Controlling hardware at the bit level is essential in embedded programming.

### Operator Precedence and Associativity

**Operator Precedence** determines the order in which operators are evaluated in an expression. **Associativity** defines the order in which operators of the same precedence are processed. Understanding precedence and associativity is vital to avoid unexpected results in expressions.

#### Precedence Rules

Operators with higher precedence are evaluated before those with lower precedence. Parentheses can be used to override the default precedence.

**Common Precedence Order (from highest to lowest):**

1. **Parentheses (`()`)**
2. **Exponentiation (`**`)**
3. **Unary Operators (`+`, `-`, `!`)**
4. **Multiplicative Operators (`*`, `/`, `%`)**
5. **Additive Operators (`+`, `-`)**
6. **Relational Operators (`<`, `<=`, `>`, `>=`)**
7. **Equality Operators (`==`, `!=`)**
8. **Logical AND (`&&`, `and`)**
9. **Logical OR (`||`, `or`)**

**Example:**

```python
result = 10 + 5 * 2  # Multiplication has higher precedence
# Equivalent to 10 + (5 * 2) = 20

result = (10 + 5) * 2  # Parentheses override precedence
# Equivalent to 15 * 2 = 30
```

#### Associativity Rules

**Associativity** defines the direction in which an expression is parsed when multiple operators of the same precedence appear in an expression.

- **Left-to-Right Associativity:** Operators are evaluated from left to right.
  - **Example:** `a - b - c` is evaluated as `(a - b) - c`.
  
- **Right-to-Left Associativity:** Operators are evaluated from right to left.
  - **Example:** `a ** b ** c` is evaluated as `a ** (b ** c)`.

**Example:**

```python
result = 10 - 5 - 2  # Left-to-right associativity
# Equivalent to (10 - 5) - 2 = 3

result = 2 ** 3 ** 2  # Right-to-left associativity
# Equivalent to 2 ** (3 ** 2) = 2 ** 9 = 512
```

**Challenging Operator Precedence:**

Certain operators can lead to confusion due to their precedence and associativity. It's important to use parentheses to make the intended order of operations explicit.

```java
int a = 5;
int b = 10;
int c = 15;

int result = a + b * c;  // Multiplication has higher precedence: 5 + (10 * 15) = 155
int result = (a + b) * c;  // Parentheses change the order: (5 + 10) * 15 = 225
```

### Best Practices

- **Use Parentheses for Clarity:** Even if you know the precedence, using parentheses can make your code more readable and maintainable.
  
  ```python
  result = (a + b) * c  # Clear and explicit
  ```
  
- **Understand Language-Specific Precedence:** Different programming languages might have slight variations in operator precedence and associativity. Always refer to the language documentation.
  
- **Avoid Complex Expressions:** Break down complex expressions into simpler statements to enhance readability and reduce the risk of errors.
  
  ```java
  // Instead of
  int result = a + b * c - d / e;
  
  // Use
  int multiplication = b * c;
  int division = d / e;
  int result = a + multiplication - division;
  ```

- **Consistent Formatting:** Maintain consistent formatting and indentation to make the order of operations clear.
  
  ```python
  # Clear formatting
  result = (a + b) * (c - d) / e
  ```

### Summary

Operators and expressions form the foundation of writing meaningful and functional code. By understanding the different types of operators, their precedence, and associativity, programmers can construct accurate and efficient expressions. Utilizing best practices, such as using parentheses for clarity and avoiding overly complex expressions, ensures that code remains readable and maintainable.
