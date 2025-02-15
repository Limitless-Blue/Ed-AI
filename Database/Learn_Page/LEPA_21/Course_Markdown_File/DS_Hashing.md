# Hashing

## Table of Contents
1. [Handling Collisions](#handling-collisions)
   - [Chaining Method](#chaining-method)
   - [Open Addressing Techniques](#open-addressing-techniques)
     - [Linear Probing](#linear-probing)
     - [Quadratic Probing](#quadratic-probing)
     - [Double Hashing](#double-hashing)
2. [Basic Hash Table Operations](#basic-hash-table-operations)
   - [Insertion](#insertion)
   - [Deletion](#deletion)
   - [Searching](#searching)

---

## 1. Handling Collisions

Collisions occur in hash tables when two different keys hash to the same index. There are several strategies to handle these collisions effectively. The two primary methods are **chaining** and **open addressing**.

### Chaining Method

Chaining involves storing multiple elements that hash to the same index in a linked list. Each index of the hash table points to the head of a linked list, which contains all the elements that hash to that index.

#### Example of Chaining

Assume we have a hash table of size 5 and a simple hash function that computes the index as `key % table_size`. If we insert the keys `10`, `15`, `20`, and `25`, we would get the following:

```plaintext
Index: 0 -> [ ]
Index: 1 -> [ ]
Index: 2 -> [ ]
Index: 3 -> [10] -> [15] -> [20] -> [25]
Index: 4 -> [ ]
```

Here, keys `10`, `15`, `20`, and `25` all hash to index `0` (`10 % 5`, `15 % 5`, `20 % 5`, `25 % 5`), so they are stored in a linked list at that index.

### Open Addressing Techniques

Open addressing is another method of collision resolution that involves finding the next available slot in the hash table when a collision occurs. There are several strategies for open addressing, including linear probing, quadratic probing, and double hashing.

#### Linear Probing

In linear probing, if a collision occurs at an index, the algorithm checks the next index (index + 1) and continues checking sequentially until an empty slot is found.

##### Example of Linear Probing

Suppose we have a hash table of size 5 and we insert the keys `10`, `11`, and `12` using a hash function `key % table_size`. The insertion would proceed as follows:

```plaintext
Insert 10: Hash(10) -> 0
Index: 0 -> [10]

Insert 11: Hash(11) -> 1
Index: 1 -> [11]

Insert 12: Hash(12) -> 2
Index: 2 -> [12]
```

Now, if we attempt to insert `13`, which hashes to index `3`, we find it's occupied, so we continue to index `4`, which is also occupied. Finally, we find an empty slot at index `0`:

```plaintext
Insert 13: Hash(13) -> 3 (occupied) -> check index 4 (occupied) -> check index 0 (occupied) -> check index 1 (occupied)
```

Thus, `13` would be inserted in the next available slot.

#### Quadratic Probing

Quadratic probing improves upon linear probing by searching for an empty slot using a quadratic function to calculate the offset. The first probe checks the index, the second probe checks index + 1^2, the third probe checks index + 2^2, and so on.

##### Example of Quadratic Probing

Using the same example with a hash table of size 5, inserting the keys `10`, `11`, `12`, and attempting to insert `13` would yield:

```plaintext
Insert 10: Hash(10) -> 0
Index: 0 -> [10]

Insert 11: Hash(11) -> 1
Index: 1 -> [11]

Insert 12: Hash(12) -> 2
Index: 2 -> [12]

Insert 13: Hash(13) -> 3 (occupied) -> check index 4 (occupied) -> check index 0 (occupied) -> check index 1 (occupied) -> check index 4 (occupied) -> check index 1 (occupied) -> check index 0 (occupied) 
```

In this case, the search might circle around before finding a free slot.

#### Double Hashing

Double hashing is another form of open addressing that uses a second hash function to calculate the step size for probing. This helps spread out the probing sequence more uniformly.

##### Example of Double Hashing

Let's assume we have a hash table of size 5 and two hash functions:

1. \( h_1(key) = key \% 5 \)
2. \( h_2(key) = 1 + (key \% 4) \)  (to avoid 0 step size)

Inserting keys `10`, `11`, and attempting to insert `12` would work as follows:

```plaintext
Insert 10: Hash(10) -> 0
Index: 0 -> [10]

Insert 11: Hash(11) -> 1
Index: 1 -> [11]

Insert 12: Hash(12) -> 2
Index: 2 -> [12]

Insert 13: Hash(13) -> 3 (occupied) 
    Step size: h_2(13) = 1 + (13 % 4) = 2
Check index 0 + 2 = 2 (occupied) 
Check index 2 + 2 = 4 (empty)
```

So `13` would be inserted at index `4`.

---

## 2. Basic Hash Table Operations

Basic operations in a hash table include insertion, deletion, and searching for elements. These operations leverage the hash function to determine the appropriate index for each key.

### Insertion

To insert a key-value pair into a hash table:

1. Compute the hash value of the key.
2. If the index is empty, insert the key-value pair.
3. If the index is occupied, handle the collision using chaining or open addressing.

##### Example of Insertion

For a hash table with size 5 and the key-value pair `("apple", 10)`:

```plaintext
Hash("apple") -> 1 (using a hash function)
Insert at index 1:
Index: 0 -> [ ]
Index: 1 -> [("apple", 10)]
Index: 2 -> [ ]
Index: 3 -> [ ]
Index: 4 -> [ ]
```

### Deletion

To delete a key-value pair:

1. Compute the hash value to find the index.
2. If the key is found, remove it from the hash table.
3. If using chaining, remove the node from the linked list. If using open addressing, mark the slot as deleted.

##### Example of Deletion

Continuing from the previous example, if we want to delete `"apple"`:

```plaintext
Hash("apple") -> 1
Remove from index 1:
Index: 0 -> [ ]
Index: 1 -> [ ]
Index: 2 -> [ ]
Index: 3 -> [ ]
Index: 4 -> [ ]
```

### Searching

To search for a key in a hash table:

1. Compute the hash value.
2. Check the corresponding index.
3. If the key is found, return the value; if not, handle the collision method accordingly.

##### Example of Searching

To search for the key `"apple"`:

```plaintext
Hash("apple") -> 1
Check index 1:
Found key: "apple" with value: 10
```

---

Hashing and hash tables are essential in optimizing data retrieval operations. By handling collisions effectively and understanding basic operations, hash tables can provide efficient storage and access for various applications.
```