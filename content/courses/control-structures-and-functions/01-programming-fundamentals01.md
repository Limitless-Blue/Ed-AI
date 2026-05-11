# Programming Fundamentals

## Table of Contents
1. [Control Structures](#23-control-structures)
    - [Conditionals](#conditionals)
        - [`if`, `else if`, `else` Statements](#if-else-if-else-statements)
        - [Switch Case](#switch-case)
    - [Loops](#loops)
        - [`for` Loop](#for-loop)
        - [`while` Loop](#while-loop)
        - [`do-while` Loop](#do-while-loop)
        - [Nested Loops](#nested-loops)
        - [Loop Control Statements (`break`, `continue`)](#loop-control-statements-break-continue)

---

## 2.3 Control Structures

Control structures are fundamental in programming as they determine the flow of execution within a program. They allow developers to dictate how and when certain blocks of code are executed based on specific conditions or repetitive tasks.

### Conditionals

Conditionals enable programs to make decisions and execute different code blocks based on whether certain conditions are met.

#### `if`, `else if`, `else` Statements

**`if`, `else if`, and `else` statements** allow for branching logic in programs. They execute specific code blocks based on boolean conditions.

- **`if` Statement**
  - **Description:** Executes a block of code if a specified condition is `True`.
  - **Example:**
    ```python
    age = 18
    if age >= 18:
        print("You are eligible to vote.")
    ```

- **`else if` / `elif` Statement**
  - **Description:** Checks another condition if the previous `if` condition is `False`.
  - **Example:**
    ```java
    int score = 85;
    if (score >= 90) {
        System.out.println("Grade: A");
    } else if (score >= 80) {
        System.out.println("Grade: B");
    }
    ```

- **`else` Statement**
  - **Description:** Executes a block of code if all preceding `if` and `else if` conditions are `False`.
  - **Example:**
    ```python
    score = 75
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    else:
        grade = 'C'
    print(f"Grade: {grade}")
    ```

**Usage Tips:**
- Only one `else` block is allowed per `if`-`elif` chain.
- Conditions are evaluated in order; once a `True` condition is found, subsequent conditions are skipped.

#### Switch Case

**Switch case** statements provide a way to execute different parts of code based on the value of a variable. They are often used as an alternative to multiple `if-else` statements for better readability.

- **Description:** Selects one of many code blocks to execute based on the value of an expression.
- **Example:**
  ```java
  char grade = 'B';
  switch (grade) {
      case 'A':
          System.out.println("Excellent!");
          break;
      case 'B':
      case 'C':
          System.out.println("Well done");
          break;
      case 'D':
          System.out.println("You passed");
          break;
      case 'F':
          System.out.println("Better try again");
          break;
      default:
          System.out.println("Invalid grade");
  }
  ```

**Advantages of Switch Case:**
- Improves code readability when dealing with multiple discrete values.
- Can be more efficient than multiple `if-else` statements in some languages.

### Loops

Loops allow for the repeated execution of a block of code as long as a specified condition is met. They are essential for tasks that require iteration, such as processing items in a list or performing calculations multiple times.

#### `for` Loop

**`for` loops** are used for iterating over a sequence (like a list, array, or range) a specific number of times.

- **Description:** Repeats a block of code a predetermined number of times.
- **Example:**
  ```python
  for i in range(5):
      print(f"Iteration {i}")
  ```

  ```java
  for (int i = 0; i < 5; i++) {
      System.out.println("Iteration " + i);
  }
  ```

**Use Cases:**
- Iterating over elements in a collection.
- Executing a block of code a specific number of times.

#### `while` Loop

**`while` loops** execute a block of code as long as a specified condition remains `True`.

- **Description:** Continues to execute as long as the condition is `True`.
- **Example:**
  ```python
  count = 0
  while count < 5:
      print(f"Count is {count}")
      count += 1
  ```

  ```java
  int count = 0;
  while (count < 5) {
      System.out.println("Count is " + count);
      count++;
  }
  ```

**Use Cases:**
- When the number of iterations is not known beforehand.
- Waiting for a certain condition to be met before proceeding.

#### `do-while` Loop

**`do-while` loops** are similar to `while` loops but guarantee that the block of code is executed at least once.

- **Description:** Executes the block once before checking the condition.
- **Example:**
  ```java
  int count = 0;
  do {
      System.out.println("Count is " + count);
      count++;
  } while (count < 5);
  ```

**Use Cases:**
- When the code block needs to run at least once regardless of the condition.
- Menu-driven programs where the menu should display at least once.

#### Nested Loops

**Nested loops** are loops within loops. They are used when dealing with multi-dimensional data structures or when multiple iterations are required.

- **Description:** A loop inside another loop.
- **Example:**
  ```python
  for i in range(3):
      for j in range(2):
          print(f"i={i}, j={j}")
  ```

  ```java
  for (int i = 0; i < 3; i++) {
      for (int j = 0; j < 2; j++) {
          System.out.println("i=" + i + ", j=" + j);
      }
  }
  ```

**Use Cases:**
- Iterating over multi-dimensional arrays or matrices.
- Generating combinations or permutations.

#### Loop Control Statements (`break`, `continue`)

**Loop control statements** alter the flow of loops by exiting them prematurely or skipping certain iterations.

- **`break` Statement**
  - **Description:** Terminates the closest enclosing loop immediately.
  - **Example:**
    ```python
    for i in range(10):
        if i == 5:
            break
        print(i)
    # Output: 0 1 2 3 4
    ```

    ```java
    for (int i = 0; i < 10; i++) {
        if (i == 5) {
            break;
        }
        System.out.println(i);
    }
    ```

- **`continue` Statement**
  - **Description:** Skips the current iteration and proceeds to the next one.
  - **Example:**
    ```python
    for i in range(5):
        if i == 2:
            continue
        print(i)
    # Output: 0 1 3 4
    ```

    ```java
    for (int i = 0; i < 5; i++) {
        if (i == 2) {
            continue;
        }
        System.out.println(i);
    }
    ```

**Use Cases:**
- `break`: Exiting a loop when a certain condition is met.
- `continue`: Skipping over unwanted iterations without terminating the loop.

### Best Practices

- **Avoid Infinite Loops:** Ensure that loop conditions will eventually be met to prevent the program from running indefinitely.
  
  ```python
  # Risk of infinite loop
  while True:
      # Missing condition to break the loop
      pass
  ```

- **Use Meaningful Loop Conditions:** Conditions should clearly reflect the purpose of the loop for better readability and maintenance.
  
  ```java
  // Clear loop condition
  while (userInput != 'q') {
      // Process input
  }
  ```

- **Limit Nesting Depth:** Excessive nesting can make code hard to read and maintain. Consider refactoring nested loops into separate functions if necessary.

- **Use Loop Control Statements Sparingly:** Overusing `break` and `continue` can make the flow of the loop hard to follow. Use them judiciously.

### Summary

Control structures are essential for directing the flow of a program. By effectively utilizing conditionals and loops, developers can create dynamic and responsive applications that handle a variety of scenarios and tasks. Understanding how to implement and manage these structures is crucial for writing efficient and maintainable code.