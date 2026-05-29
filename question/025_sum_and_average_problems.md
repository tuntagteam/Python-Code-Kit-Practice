# Sum and Average Problems

## Goal

Practice adding numbers and finding averages.

## What students should know first

* Know loops.
* Know numbers.
* Know division.

## Questions

### Question 1: Class Point Sum

**Problem description:** Read n scores and print their total.

**Input format:** First line n, second line n integers.

**Output format:** Total score.

**Example input:**

```text
4
5 7 8 10
```

**Example output:**

```text
30
```

**Hint:** Use a running sum.

**Difficulty:** Easy

### Question 2: Average Stars

**Problem description:** Read star ratings and print the average.

**Input format:** n then n integers.

**Output format:** Average.

**Example input:**

```text
3
4 5 3
```

**Example output:**

```text
4.0
```

**Hint:** total / n.

**Difficulty:** Easy

### Question 3: Candy Bags

**Problem description:** Read candy counts in bags and print total candies.

**Input format:** One line integers.

**Output format:** Total.

**Example input:**

```text
2 3 5
```

**Example output:**

```text
10
```

**Hint:** sum() is okay.

**Difficulty:** Easy

### Question 4: Only Positive Sum

**Problem description:** Read numbers and sum only positive numbers.

**Input format:** n then n integers.

**Output format:** Positive sum.

**Example input:**

```text
5
-1 4 0 7 -2
```

**Example output:**

```text
11
```

**Hint:** Add only if number > 0.

**Difficulty:** Medium

### Question 5: Even Average

**Problem description:** Read numbers and print the average of even numbers.

**Input format:** n then n integers.

**Output format:** Average of evens.

**Example input:**

```text
5
2 3 4 7 8
```

**Example output:**

```text
4.666666666666667
```

**Hint:** Keep even total and even count.

**Difficulty:** Medium

### Question 6: Shop Receipt

**Problem description:** Read item prices and print total plus 5 coins delivery.

**Input format:** n then n prices.

**Output format:** Final total.

**Example input:**

```text
3
10 4 6
```

**Example output:**

```text
25
```

**Hint:** Add 5 after summing.

**Difficulty:** Medium

### Question 7: Score Drop Lowest

**Problem description:** Read scores, drop the lowest score, and print the sum of the rest.

**Input format:** n then n integers.

**Output format:** Sum without lowest.

**Example input:**

```text
4
8 5 10 7
```

**Example output:**

```text
25
```

**Hint:** Total minus min value.

**Difficulty:** Medium

### Question 8: Running Total

**Problem description:** Read numbers and print the running total after each number.

**Input format:** n then n integers.

**Output format:** Running totals.

**Example input:**

```text
4
1 3 2 5
```

**Example output:**

```text
1
4
6
11
```

**Hint:** Update total each step.

**Difficulty:** Hard

### Question 9: Weighted Gems

**Problem description:** Read gem counts and values. Print total value.

**Input format:** n, counts line, values line.

**Output format:** Total value.

**Example input:**

```text
3
2 1 4
5 10 3
```

**Example output:**

```text
32
```

**Hint:** Sum count[i] * value[i].

**Difficulty:** Hard

### Question 10: Average Without Zeros

**Problem description:** Read numbers and print the average ignoring zeros. If all are zero, print 0.

**Input format:** n then n integers.

**Output format:** Average or 0.

**Example input:**

```text
5
0 4 0 6 0
```

**Example output:**

```text
5.0
```

**Hint:** Count only non-zero values.

**Difficulty:** Hard

