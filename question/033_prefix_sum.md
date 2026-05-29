# Prefix Sum

## Goal

Practice using saved running totals to answer sum questions quickly.

## What students should know first

* Know lists.
* Know loops.
* Know sums.

## Questions

### Question 1: Running Sum List

**Problem description:** Read numbers and print their prefix sums.

**Input format:** n then n integers.

**Output format:** Prefix sums.

**Example input:**

```text
4
2 3 5 1
```

**Example output:**

```text
2 5 10 11
```

**Hint:** Each prefix is previous prefix plus current.

**Difficulty:** Easy

### Question 2: Quick Range Sum

**Problem description:** Read numbers and one range l r. Print sum from l to r inclusive using 0-based indexes.

**Input format:** n, numbers, l r.

**Output format:** Range sum.

**Example input:**

```text
5
1 2 3 4 5
1 3
```

**Example output:**

```text
9
```

**Hint:** Build prefix sums first.

**Difficulty:** Easy

### Question 3: Many Range Sums

**Problem description:** Read numbers and q ranges. Print each range sum.

**Input format:** n, numbers, q, then q lines l r.

**Output format:** One sum per line.

**Example input:**

```text
5
1 2 3 4 5
2
0 2
2 4
```

**Example output:**

```text
6
12
```

**Hint:** prefix[r+1] - prefix[l].

**Difficulty:** Medium

### Question 4: Candy Before

**Problem description:** Read candy counts and index k. Print candies before index k.

**Input format:** n, counts, k.

**Output format:** Sum before k.

**Example input:**

```text
5
2 4 6 8 10
3
```

**Example output:**

```text
12
```

**Hint:** Use prefix[k].

**Difficulty:** Medium

### Question 5: Balanced Split

**Problem description:** Read numbers. Print yes if there is a place where left sum equals right sum.

**Input format:** n then n integers.

**Output format:** yes or no.

**Example input:**

```text
5
1 2 3 3 3
```

**Example output:**

```text
yes
```

**Hint:** Track left sum and total sum.

**Difficulty:** Medium

### Question 6: Max Subarray Fixed Size

**Problem description:** Read numbers and k. Print the biggest sum of any k neighboring numbers.

**Input format:** n, numbers, k.

**Output format:** Max window sum.

**Example input:**

```text
6
1 3 2 5 4 1
3
```

**Example output:**

```text
11
```

**Hint:** Use prefix sums for each window.

**Difficulty:** Medium

### Question 7: Prefix Average

**Problem description:** Read scores and print the average after each score.

**Input format:** n then n integers.

**Output format:** Prefix averages.

**Example input:**

```text
3
3 6 9
```

**Example output:**

```text
3.0
4.5
6.0
```

**Hint:** Use running total divided by count.

**Difficulty:** Medium

### Question 8: Zero Sum Range

**Problem description:** Read numbers. Print yes if any continuous part has sum 0.

**Input format:** n then n integers.

**Output format:** yes or no.

**Example input:**

```text
5
2 -2 3 1 -4
```

**Example output:**

```text
yes
```

**Hint:** If a prefix sum repeats, the middle sum is 0.

**Difficulty:** Hard

### Question 9: Difference Array Starter

**Problem description:** Read n and updates l r value. Add value to each range and print final list.

**Input format:** n, q, then updates.

**Output format:** Final list.

**Example input:**

```text
5
2
1 3 2
0 1 1
```

**Example output:**

```text
1 3 2 2 0
```

**Hint:** Use difference array then prefix sum.

**Difficulty:** Hard

### Question 10: 2D Row Prefix

**Problem description:** Read a grid and a row range. Print the sum in that row from c1 to c2.

**Input format:** rows cols, grid, row c1 c2.

**Output format:** Range sum.

**Example input:**

```text
2 4
1 2 3 4
5 6 7 8
1 1 3
```

**Example output:**

```text
21
```

**Hint:** Build prefix sums for each row.

**Difficulty:** Hard

