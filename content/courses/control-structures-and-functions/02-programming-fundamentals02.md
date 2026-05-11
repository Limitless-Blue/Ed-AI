# Programming Fundamentals

## Table of Contents
1. [Functions and Scope](#24-functions-and-scope)
    - [Defining and Calling Functions](#defining-and-calling-functions)
    - [Function Parameters and Return Values](#function-parameters-and-return-values)
    - [Scope (Local vs. Global Variables)](#scope-local-vs-global-variables)
    - [Recursion Basics](#recursion-basics)
    - [Lambda Expressions](#lambda-expressions)

---

## 2.4 Functions and Scope

Functions are essential building blocks in programming that allow for code reusability, modularity, and better organization. Understanding how to define and use functions, manage scope, and leverage advanced concepts like recursion and lambda expressions is crucial for writing efficient and maintainable code.

### Defining and Calling Functions

Functions encapsulate reusable blocks of code that perform specific tasks. They help in reducing redundancy and improving code readability.

#### Defining a Function

**Definition:** A function is defined using a specific syntax depending on the programming language, specifying the function name, parameters (if any), and the block of code to execute.

- **Python Example:**
  ```python
  def greet(name):
      print(f"Hello, {name}!")
  ```

- **Java Example:**
  ```java
  public void greet(String name) {
      System.out.println("Hello, " + name + "!");
  }
  ```

#### Calling a Function

**Description:** Once defined, a function can be invoked or called by its name, passing necessary arguments.

- **Python Example:**
  ```python
  greet("Alice")  # Output: Hello, Alice!
  ```

- **Java Example:**
  ```java
  greet("Bob");  // Output: Hello, Bob!
  ```

**Usage Tips:**
- Ensure that the number and type of arguments match the function's parameters.
- Functions should have descriptive names that reflect their purpose.

### Function Parameters and Return Values

Functions can accept input through parameters and can return output using return values.

#### Function Parameters

**Description:** Parameters allow functions to accept inputs, making them more flexible and reusable.

- **Python Example:**
  ```python
  def add(a, b):
      return a + b
  ```

- **Java Example:**
  ```java
  public int add(int a, int b) {
      return a + b;
  }
  ```

**Default Parameters (Python):**
- Python allows setting default values for parameters.
  ```python
  def greet(name="Guest"):
      print(f"Hello, {name}!")
  
  greet()          # Output: Hello, Guest!
  greet("Charlie") # Output: Hello, Charlie!
  ```

#### Return Values

**Description:** Functions can return values using the `return` statement, allowing the caller to use the result.

- **Python Example:**
  ```python
  def multiply(a, b):
      return a * b

  result = multiply(3, 4)  # result is 12
  ```

- **Java Example:**
  ```java
  public int multiply(int a, int b) {
      return a * b;
  }

  int result = multiply(3, 4);  // result is 12
  ```

**Usage Tips:**
- Clearly define what the function returns to avoid confusion.
- Use return values to pass results back to the caller for further processing.

### Scope (Local vs. Global Variables)

Scope determines the accessibility of variables within different parts of a program.

#### Local Variables

**Description:** Variables declared within a function are local to that function and cannot be accessed outside of it.

- **Python Example:**
  ```python
  def foo():
      local_var = 10
      print(local_var)

  foo()          # Output: 10
  print(local_var)  # Error: NameError
  ```

- **Java Example:**
  ```java
  public void foo() {
      int localVar = 10;
      System.out.println(localVar);
  }

  foo();            // Output: 10
  System.out.println(localVar);  // Error: Cannot find symbol
  ```

#### Global Variables

**Description:** Variables declared outside of functions are global and can be accessed from anywhere in the program.

- **Python Example:**
  ```python
  global_var = 20

  def foo():
      print(global_var)

  foo()          # Output: 20
  print(global_var)  # Output: 20
  ```

- **Java Example:**
  ```java
  public class Example {
      static int globalVar = 20;

      public void foo() {
          System.out.println(globalVar);
      }

      public static void main(String[] args) {
          Example ex = new Example();
          ex.foo();            // Output: 20
          System.out.println(globalVar);  // Output: 20
      }
  }
  ```

**Best Practices:**
- Minimize the use of global variables to reduce potential side effects and improve code maintainability.
- Use local variables within functions to encapsulate data and functionality.

### Recursion Basics

Recursion is a programming technique where a function calls itself to solve smaller instances of a problem.

#### Defining Recursion

**Description:** A recursive function must have a base case to terminate the recursion and avoid infinite loops.

- **Python Example:**
  ```python
  def factorial(n):
      if n == 0:
          return 1
      else:
          return n * factorial(n - 1)

  print(factorial(5))  # Output: 120
  ```

- **Java Example:**
  ```java
  public int factorial(int n) {
      if (n == 0) {
          return 1;
      } else {
          return n * factorial(n - 1);
      }
  }

  System.out.println(factorial(5));  // Output: 120
  ```

**Advantages of Recursion:**
- Simplifies the code for problems that have a natural recursive structure, such as tree traversals and combinatorial problems.

**Disadvantages of Recursion:**
- Can lead to high memory usage due to multiple function calls.
- Risk of stack overflow if the recursion depth is too high.

**Usage Tips:**
- Always define a clear base case.
- Ensure that each recursive call progresses towards the base case.

### Lambda Expressions

Lambda expressions provide a concise way to define anonymous functions without a name.

#### Defining Lambda Expressions

**Description:** Lambda expressions are useful for short, throwaway functions that are used only once or a few times.

- **Python Example:**
  ```python
  add = lambda a, b: a + b
  print(add(2, 3))  # Output: 5
  ```

- **Java Example:**
  ```java
  // Using lambda to define a simple functional interface
  interface MathOperation {
      int operate(int a, int b);
  }

  MathOperation add = (a, b) -> a + b;
  System.out.println(add.operate(2, 3));  // Output: 5
  ```

**Use Cases:**
- Sorting or filtering collections with custom criteria.
- Passing functions as arguments to higher-order functions.
- Implementing simple callbacks or event handlers.

**Advantages of Lambda Expressions:**
- Reduces boilerplate code.
- Enhances readability for simple operations.

**Best Practices:**
- Use lambda expressions for simple, single-operation functions.
- Avoid complex logic within lambda expressions to maintain readability.

### Best Practices

- **Modular Design:** Break down complex problems into smaller, reusable functions.
- **Descriptive Naming:** Use clear and descriptive names for functions and parameters to improve code readability.
- **Avoid Deep Recursion:** Use iterative solutions when recursion depth could lead to stack overflow.
- **Limit Global Variables:** Prefer passing parameters to functions over relying on global variables to enhance modularity and reduce side effects.
- **Use Lambdas Judiciously:** Utilize lambda expressions for simple operations to keep code concise without sacrificing clarity.

### Summary

Functions and scope are fundamental concepts that enable developers to write organized, reusable, and maintainable code. By effectively defining and calling functions, managing variable scope, leveraging recursion, and utilizing lambda expressions, programmers can tackle complex problems with greater ease and efficiency. Adhering to best practices ensures that code remains clean, understandable, and robust.
