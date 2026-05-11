# Hashing

## Table of Contents
1. [Introduction to Hashing](#introduction-to-hashing)
   - [What is Hashing?](#what-is-hashing)
   - [Benefits of Using Hash Tables](#benefits-of-using-hash-tables)
2. [Hash Functions](#hash-functions)
   - [Simple Hash Function Examples](#simple-hash-function-examples)
   - [Understanding Hash Collisions](#understanding-hash-collisions)

---

## 1. Introduction to Hashing

### What is Hashing?

Hashing is a process used in computing to map data of arbitrary size to fixed-size values. This process is achieved by using a **hash function** that converts the input data (also known as the key) into a hash value, typically represented as an integer. This value is often used as an index in a hash table, which is a data structure that stores key-value pairs.

For example, let's say we want to store and quickly retrieve the information associated with different people using their names. Instead of searching through an unsorted list of names, hashing allows us to compute a unique "hash code" for each name and store it in a specific location in a hash table, ensuring faster lookups.

```plaintext
Input Key: "John Doe"
Hash Function: Hash("John Doe") -> 112
Store "John Doe" at index 112 of the hash table.
```

### Benefits of Using Hash Tables

Hash tables are a highly efficient data structure when it comes to retrieving, inserting, and deleting data. Here are some of the key benefits:

1. **Fast Lookup Time**: Hash tables provide average O(1) time complexity for search, insert, and delete operations, which means operations are constant time and independent of the number of elements.
   
2. **Efficient Memory Use**: Hashing typically uses less memory compared to other structures like arrays or linked lists, as only the relevant keys are stored.

3. **Widely Used in Various Applications**: Hash tables are used in various applications such as databases (indexing), caching, password storage (with hashing algorithms), and in compilers to store identifiers.

---

## 2. Hash Functions

A **hash function** is a function that takes an input (or "key") and returns a fixed-size string of bytes. The output, known as the "hash value" or "hash code," typically looks like a seemingly random string of numbers and letters, but it always corresponds to the input.

### Simple Hash Function Examples

Let's look at a few simple examples of hash functions. For simplicity, we'll use basic numeric hash functions.

#### Example 1: Modulo Hash Function

A simple hash function might take the key and apply the modulo operator to it, returning the remainder when divided by a certain number (e.g., the size of the hash table).

```python
def simple_modulo_hash(key, table_size):
    return key % table_size
```

For example, if the table size is 10 and the key is 123:

```plaintext
Key = 123
Hash Function = 123 % 10 = 3
```

In this case, the key 123 would be mapped to index 3 in the hash table.

#### Example 2: Hashing Strings

When dealing with strings, we can convert characters to their ASCII values, sum them up, and then apply a modulo operation. Here's an example hash function for strings:

```python
def string_hash(s, table_size):
    total = 0
    for char in s:
        total += ord(char)  # ord() gives ASCII value of character
    return total % table_size
```

For the string `"hello"` and a table size of 10:

```plaintext
h -> 104
e -> 101
l -> 108
l -> 108
o -> 111
Total = 104 + 101 + 108 + 108 + 111 = 532
Hash value = 532 % 10 = 2
```

The string `"hello"` would be mapped to index 2 in the hash table.

### Understanding Hash Collisions

Hash collisions occur when two different keys produce the same hash value, meaning they are mapped to the same index in the hash table. Hash collisions are inevitable due to the "pigeonhole principle," especially when the number of keys exceeds the number of available slots in the hash table.

#### Example of a Collision

Consider two keys, `23` and `33`, with the following hash function:

```python
def simple_modulo_hash(key, table_size):
    return key % table_size
```

Using a table size of 10:

```plaintext
Hash(23) = 23 % 10 = 3
Hash(33) = 33 % 10 = 3
```

Both keys, `23` and `33`, are mapped to the same index (`3`), causing a collision.

#### Handling Collisions

There are several strategies to handle collisions, including:

1. **Chaining**: This involves storing multiple elements at the same index in a linked list.
   ```plaintext
   Table index 3 -> [23] -> [33]
   ```
   Each index in the table points to a linked list, and any colliding elements are added to the list.

2. **Open Addressing**: This method looks for the next available slot in the hash table using a probing sequence (e.g., linear probing or quadratic probing).

   - **Linear Probing**: If index `i` is occupied, check `i+1`, `i+2`, and so on.
   
   - **Quadratic Probing**: Check indices using a quadratic formula (e.g., `i + 1^2`, `i + 2^2`, etc.).

---

Hashing is a fundamental concept in computer science with applications across many domains. Hash functions must be designed to minimize collisions and distribute keys uniformly across the table. By handling collisions efficiently, hash tables can maintain their performance, providing fast lookups, insertions, and deletions.
```

---