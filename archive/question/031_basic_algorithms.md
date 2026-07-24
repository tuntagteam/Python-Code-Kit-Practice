# Basic Algorithms

## Goal

Practice classic step-by-step methods for solving problems.

## What students should know first

* Know loops.
* Know functions.
* Know lists.

## Questions

### Question 1: Fizz Buzz Junior

**Problem description:** Read n. For numbers 1 to n, print Fizz if divisible by 3, Buzz if divisible by 5, FizzBuzz if both, otherwise the number.

**Input format:** One integer.

**Output format:** One result per line.

**Example input:**

```text
5
```

**Example output:**

```text
1
2
Fizz
4
Buzz
```

**Hint:** Check both first.

**Difficulty:** Easy

### Question 2: Prime Check

**Problem description:** Read n and print prime if it has exactly two factors.

**Input format:** One integer.

**Output format:** prime or not prime.

**Example input:**

```text
7
```

**Example output:**

```text
prime
```

**Hint:** Try divisors from 2 to n-1.

**Difficulty:** Easy

### Question 3: Greatest Common Divisor

**Problem description:** Read two numbers and print their greatest common divisor.

**Input format:** Two integers.

**Output format:** GCD.

**Example input:**

```text
12
18
```

**Example output:**

```text
6
```

**Hint:** Try Euclid's algorithm or all divisors.

**Difficulty:** Medium

### Question 4: Reverse Digits

**Problem description:** Read a positive integer and print its digits reversed.

**Input format:** One integer.

**Output format:** Reversed number.

**Example input:**

```text
1234
```

**Example output:**

```text
4321
```

**Hint:** Use string reverse or math loop.

**Difficulty:** Medium

### Question 5: Anagram Check

**Problem description:** Read two words and print yes if they have the same letters.

**Input format:** Two words.

**Output format:** yes or no.

**Example input:**

```text
listen
silent
```

**Example output:**

```text
yes
```

**Hint:** Sort both words.

**Difficulty:** Medium

### Question 6: Remove Duplicates

**Problem description:** Read numbers and print them keeping only first appearances.

**Input format:** n then n integers.

**Output format:** Unique sequence.

**Example input:**

```text
7
1 2 1 3 2 4 1
```

**Example output:**

```text
1 2 3 4
```

**Hint:** Use a set for seen numbers.

**Difficulty:** Medium

### Question 7: Sieve Starter

**Problem description:** Read n and print all prime numbers up to n.

**Input format:** One integer.

**Output format:** Prime numbers.

**Example input:**

```text
10
```

**Example output:**

```text
2 3 5 7
```

**Hint:** Mark multiples as not prime.

**Difficulty:** Hard

### Question 8: Run Length Encode

**Problem description:** Read a word and print each letter with its run count.

**Input format:** One word.

**Output format:** Encoded runs.

**Example input:**

```text
aaabbc
```

**Example output:**

```text
a3 b2 c1
```

**Hint:** Count same neighboring letters.

**Difficulty:** Hard

### Question 9: Merge Sorted Lists

**Problem description:** Read two sorted lists and print one sorted merged list.

**Input format:** Two lines of sorted integers.

**Output format:** Merged sorted list.

**Example input:**

```text
1 3 5
2 4 6
```

**Example output:**

```text
1 2 3 4 5 6
```

**Hint:** Use two positions.

**Difficulty:** Hard

### Question 10: Majority Vote

**Problem description:** Read values and print the value that appears more than half the time, or none.

**Input format:** n then n values.

**Output format:** Majority value or none.

**Example input:**

```text
5
A B A A C
```

**Example output:**

```text
A
```

**Hint:** Count frequencies.

**Difficulty:** Hard

