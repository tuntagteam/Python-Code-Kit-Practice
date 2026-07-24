# Dynamic Programming Basics

## Goal

Practice saving answers to smaller problems so bigger problems are easier.

## What students should know first

* Know lists.
* Know recursion or loops.
* Know saving repeated answers.

## Questions

### Question 1: Fibonacci Saved

**Problem description:** Compute Fibonacci n using a list to save earlier answers.

**Input format:** One integer.

**Output format:** Fibonacci value.

**Example input:**

```text
7
```

**Example output:**

```text
13
```

**Hint:** Build answers from 0 up to n.

**Difficulty:** Easy

### Question 2: Climb Stairs

**Problem description:** A robot climbs 1 or 2 steps. Count ways to climb n steps.

**Input format:** One integer.

**Output format:** Number of ways.

**Example input:**

```text
5
```

**Example output:**

```text
8
```

**Hint:** Same pattern as Fibonacci.

**Difficulty:** Easy

### Question 3: Coin Ways Small

**Problem description:** Using coins 1 and 2, count ways to make n.

**Input format:** One integer.

**Output format:** Ways.

**Example input:**

```text
4
```

**Example output:**

```text
3
```

**Hint:** Ways are 1+1+1+1, 1+1+2, 2+2.

**Difficulty:** Medium

### Question 4: Max Candy Path

**Problem description:** Read candy amounts in boxes in a line. You may not take neighboring boxes. Print max candy.

**Input format:** n then n integers.

**Output format:** Max candy.

**Example input:**

```text
5
2 7 9 3 1
```

**Example output:**

```text
12
```

**Hint:** Best at i is max(skip, take).

**Difficulty:** Medium

### Question 5: Min Jump Cost

**Problem description:** Read step costs. You can move 1 or 2 steps. Print minimum cost to reach the last step.

**Input format:** n then n integers.

**Output format:** Minimum cost.

**Example input:**

```text
4
1 100 1 1
```

**Example output:**

```text
2
```

**Hint:** Save best cost for each step.

**Difficulty:** Medium

### Question 6: Longest Increasing Easy

**Problem description:** Read numbers and print length of longest increasing subsequence.

**Input format:** n then n integers.

**Output format:** Length.

**Example input:**

```text
5
3 1 2 5 4
```

**Example output:**

```text
3
```

**Hint:** dp[i] stores best ending at i.

**Difficulty:** Medium

### Question 7: Grid Paths

**Problem description:** Read rows and columns. Count paths from top-left to bottom-right moving only right or down.

**Input format:** Two integers.

**Output format:** Path count.

**Example input:**

```text
2
3
```

**Example output:**

```text
3
```

**Hint:** Each cell gets paths from top plus left.

**Difficulty:** Medium

### Question 8: Subset Sum Small

**Problem description:** Read numbers and target. Print yes if some numbers can add to target.

**Input format:** n, numbers, target.

**Output format:** yes or no.

**Example input:**

```text
4
2 4 6 9
10
```

**Example output:**

```text
yes
```

**Hint:** Track possible sums.

**Difficulty:** Hard

### Question 9: Longest Common Subsequence

**Problem description:** Read two short words and print the LCS length.

**Input format:** Two words.

**Output format:** Length.

**Example input:**

```text
abcde
ace
```

**Example output:**

```text
3
```

**Hint:** Use a 2D table.

**Difficulty:** Hard

### Question 10: Coin Change Minimum

**Problem description:** Read coin values and amount. Print the fewest coins needed, or -1.

**Input format:** n, coin values, amount.

**Output format:** Minimum coins.

**Example input:**

```text
3
1 3 4
6
```

**Example output:**

```text
2
```

**Hint:** dp[amount] stores best answer.

**Difficulty:** Hard

