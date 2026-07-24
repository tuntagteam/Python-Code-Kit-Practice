# Recursion Basics

## Goal

Practice functions that solve a problem by calling themselves on a smaller problem.

## What students should know first

* Know functions.
* Know if statements.
* Know smaller subproblems.

## Questions

### Question 1: Countdown Recursion

**Problem description:** Write a recursive function that prints n down to 1.

**Input format:** One integer.

**Output format:** Countdown.

**Example input:**

```text
3
```

**Example output:**

```text
3
2
1
```

**Hint:** Base case is n == 0.

**Difficulty:** Easy

### Question 2: Factorial Fun

**Problem description:** Use recursion to compute n factorial.

**Input format:** One integer.

**Output format:** Factorial.

**Example input:**

```text
5
```

**Example output:**

```text
120
```

**Hint:** n! = n * (n-1)!

**Difficulty:** Easy

### Question 3: Sum to N

**Problem description:** Use recursion to sum numbers from 1 to n.

**Input format:** One integer.

**Output format:** Sum.

**Example input:**

```text
4
```

**Example output:**

```text
10
```

**Hint:** sum(n) = n + sum(n-1).

**Difficulty:** Easy

### Question 4: Fibonacci Small

**Problem description:** Use recursion to find Fibonacci number n where fib(0)=0 and fib(1)=1.

**Input format:** One integer.

**Output format:** Fibonacci value.

**Example input:**

```text
6
```

**Example output:**

```text
8
```

**Hint:** Use two base cases.

**Difficulty:** Medium

### Question 5: String Reverse

**Problem description:** Use recursion to reverse a word.

**Input format:** One word.

**Output format:** Reversed word.

**Example input:**

```text
code
```

**Example output:**

```text
edoc
```

**Hint:** Reverse the smaller rest of the word.

**Difficulty:** Medium

### Question 6: Digit Sum

**Problem description:** Use recursion to sum digits of a positive integer.

**Input format:** One integer.

**Output format:** Digit sum.

**Example input:**

```text
1234
```

**Example output:**

```text
10
```

**Hint:** Last digit is n % 10.

**Difficulty:** Medium

### Question 7: Power Recursion

**Problem description:** Use recursion to calculate a to the power b.

**Input format:** Two integers.

**Output format:** Power.

**Example input:**

```text
2
5
```

**Example output:**

```text
32
```

**Hint:** a^b = a * a^(b-1).

**Difficulty:** Medium

### Question 8: List Sum Recursive

**Problem description:** Use recursion to sum a list of numbers.

**Input format:** n then n integers.

**Output format:** Sum.

**Example input:**

```text
4
1 2 3 4
```

**Example output:**

```text
10
```

**Hint:** Sum first item plus sum of rest.

**Difficulty:** Hard

### Question 9: Palindrome Recursive

**Problem description:** Use recursion to check if a word is a palindrome.

**Input format:** One word.

**Output format:** yes or no.

**Example input:**

```text
radar
```

**Example output:**

```text
yes
```

**Hint:** Compare first and last, then shrink.

**Difficulty:** Hard

### Question 10: Recursive Maze Steps

**Problem description:** A robot can climb 1 or 2 steps. Use recursion to count ways to climb n steps.

**Input format:** One integer.

**Output format:** Number of ways.

**Example input:**

```text
4
```

**Example output:**

```text
5
```

**Hint:** ways(n)=ways(n-1)+ways(n-2).

**Difficulty:** Hard

