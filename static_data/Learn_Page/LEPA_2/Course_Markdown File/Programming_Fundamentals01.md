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

## 2.1 Variables and Data Types

Programming Fundamentals form the backbone of writing effective and efficient code. Understanding variables and data types is essential for any programming language and is the first step towards developing robust applications.

### Introduction to Variables

**Variables** are fundamental building blocks in programming that store data values. They act as containers that hold information which can be referenced and manipulated throughout a program.

- **Declaration:** Defining a variable involves specifying its name and, in some languages, its data type.
  
  ```python
  # Example in Python
  age = 25
  ```

  ```java
  // Example in Java
  int age = 25;
  ```

- **Naming Conventions:**
  - Use meaningful and descriptive names.
  - Avoid using reserved keywords.
  - Follow language-specific naming conventions (e.g., camelCase in Java, snake_case in Python).

- **Scope:** The context in which a variable is accessible, such as global or local scope.
  
  - **Global Variables:** Accessible throughout the entire program.
  - **Local Variables:** Accessible only within a specific block or function.

- **Lifetime:** The duration for which a variable exists in memory.
  
  - **Static Variables:** Exist for the lifetime of the program.
  - **Dynamic Variables:** Exist until they go out of scope or are explicitly destroyed.

**Example:**

```python
# Python Example
def greet():
    message = "Hello, World!"  # Local variable
    print(message)

greet()
# print(message)  # This would raise an error because 'message' is not accessible here
```

### Common Data Types (Integers, Floats, Characters, Booleans)

Data types define the kind of data that can be stored and manipulated within a program. Understanding the various data types is crucial for selecting the appropriate type based on the requirements of your application.

#### 1. Integers (`int`)
- **Description:** Whole numbers without a fractional component.
- **Range:** Varies based on the language and system (e.g., `-2,147,483,648` to `2,147,483,647` in a 32-bit system).
- **Usage:** Counting, indexing, and scenarios requiring exact values.
  
  ```python
  age = 30
  ```

#### 2. Floats (`float`)
- **Description:** Numbers with fractional parts.
- **Precision:** Typically 32 or 64 bits, allowing for a wide range of decimal values.
- **Usage:** Scientific calculations, measurements, and scenarios requiring precision.
  
  ```python
  temperature = 98.6
  ```

#### 3. Characters (`char`)
- **Description:** Single letters, digits, or symbols.
- **Representation:** Enclosed in single quotes (e.g., `'A'`, `'3'`, `'$'`).
- **Usage:** Storing individual characters in strings, handling user input, and representing symbolic data.
  
  ```java
  char grade = 'A';
  ```

#### 4. Booleans (`bool`)
- **Description:** Represents truth values.
- **Possible Values:** `True` or `False` (or `true`/`false` depending on the language).
- **Usage:** Conditional statements, loops, and flags to control program flow.
  
  ```python
  is_active = True
  ```

**Composite Data Types:**
- **Strings (`str`):** Sequences of characters used to represent text.
  
  ```python
  name = "Alice"
  ```

- **Arrays and Lists:** Collections of elements, typically of the same data type.
  
  ```python
  numbers = [1, 2, 3, 4, 5]
  ```

- **Objects:** Complex data types that can contain multiple properties and methods.
  
  ```java
  class Person {
      String name;
      int age;
  }
  ```

### Type Conversion and Casting

**Type Conversion** and **Casting** are processes used to convert data from one type to another. Proper understanding of these concepts ensures data integrity and prevents errors during program execution.

#### Implicit Conversion
- **Description:** Automatic conversion performed by the compiler or interpreter.
- **Example:** Converting an integer to a float during arithmetic operations.
  
  ```python
  num_int = 10
  num_float = num_int + 5.5  # num_int is implicitly converted to float
  ```

#### Explicit Conversion (Casting)
- **Description:** Manual conversion initiated by the programmer.
- **Syntax:** Varies by language; often involves using casting functions or operators.
  
  ```java
  // Java Example
  double numDouble = 9.78;
  int numInt = (int) numDouble;  // Explicit casting from double to int
  ```

  ```python
  # Python Example
  num_str = "123"
  num_int = int(num_str)  # Explicit conversion from string to integer
  ```

#### Rules and Best Practices
- **Compatibility:** Ensure that the source and target types are compatible to avoid data loss or errors.
  
  ```python
  # Potential Data Loss
  num_float = 9.99
  num_int = int(num_float)  # Results in 9, losing the decimal part
  ```

- **Exception Handling:** Handle potential exceptions that may arise during type conversion.
  
  ```python
  try:
      num = int("abc")  # This will raise a ValueError
  except ValueError:
      print("Invalid input for conversion")
  ```

- **Use Cases:**
  - **Parsing User Input:** Converting string input to numeric types for calculations.
  - **Data Formatting:** Ensuring data is in the correct format for storage or transmission.
  - **Interoperability:** Facilitating communication between different systems or components that use different data types.

**Example:**

```python
# Python Example of Type Conversion
height_str = "175.5"
height_float = float(height_str)  # Converts string to float
height_int = int(height_float)    # Converts float to int, resulting in 175
```

**Caveats:**
- **Data Loss:** Converting from a type with higher precision to lower precision (e.g., float to int) can result in data loss.
- **Invalid Conversions:** Attempting to convert incompatible types (e.g., string to int when the string does not represent a valid number) can cause errors.

**Best Practices:**
- **Validate Data:** Always validate data before performing type conversions to ensure compatibility.
- **Use Built-In Functions:** Utilize language-specific functions or methods designed for safe and efficient type conversions.
- **Minimize Unnecessary Conversions:** Avoid excessive type casting to maintain code readability and performance.

By mastering variables, data types, and type conversion, programmers can write more efficient, error-free, and maintainable code. These fundamentals are crucial for solving complex problems and building scalable applications.
