# Searching Basics

## Goal

Practice finding whether an item exists and where it is.

## What students should know first

* Know lists.
* Know loops.
* Know if statements.

## Questions

### Question 1: Find the Sticker

**Problem description:** Read n sticker numbers and a target. Print found if the target is in the list.

**Input format:** First line n, second line n integers, third line target.

**Output format:** found or missing.

**Example input:**

```text
5
2 4 6 8 10
6
```

**Example output:**

```text
found
```

**Hint:** Check each item or use in.

**Difficulty:** Easy

### Question 2: First Place

**Problem description:** Read words and a target. Print the first index or -1.

**Input format:** Words line, then target.

**Output format:** Index.

**Example input:**

```text
red blue red
red
```

**Example output:**

```text
0
```

**Hint:** Loop with indexes.

**Difficulty:** Easy

### Question 3: Last Place

**Problem description:** Read words and a target. Print the last index or -1.

**Input format:** Words line, then target.

**Output format:** Index.

**Example input:**

```text
red blue red
red
```

**Example output:**

```text
2
```

**Hint:** Keep updating the answer.

**Difficulty:** Easy

### Question 4: Count Target

**Problem description:** Read numbers and target. Print how many times target appears.

**Input format:** n, numbers, target.

**Output format:** Count.

**Example input:**

```text
6
1 2 2 3 2 4
2
```

**Example output:**

```text
3
```

**Hint:** Count while searching.

**Difficulty:** Medium

### Question 5: First Bigger

**Problem description:** Read numbers and x. Print the first number bigger than x, or none.

**Input format:** n, numbers, x.

**Output format:** Number or none.

**Example input:**

```text
5
1 4 8 3 9
5
```

**Example output:**

```text
8
```

**Hint:** Stop when found.

**Difficulty:** Medium

### Question 6: Binary Search Door

**Problem description:** Read a sorted list and target. Use binary search idea and print found or missing.

**Input format:** n, sorted numbers, target.

**Output format:** found or missing.

**Example input:**

```text
5
1 3 5 7 9
7
```

**Example output:**

```text
found
```

**Hint:** Check the middle item.

**Difficulty:** Medium

### Question 7: Find Word Prefix

**Problem description:** Read words and a prefix. Print first word that starts with the prefix.

**Input format:** Words line, then prefix.

**Output format:** Word or none.

**Example input:**

```text
sun star moon
st
```

**Example output:**

```text
star
```

**Hint:** Use startswith().

**Difficulty:** Medium

### Question 8: Search Grid

**Problem description:** Read a small grid and target. Print row and column of first match, or -1 -1.

**Input format:** Rows cols, grid rows, target.

**Output format:** Position.

**Example input:**

```text
2 3
1 2 3
4 5 6
5
```

**Example output:**

```text
1 1
```

**Hint:** Use nested loops.

**Difficulty:** Hard

### Question 9: Missing Number

**Problem description:** Numbers from 1 to n have one missing. Find it.

**Input format:** n, then n-1 numbers.

**Output format:** Missing number.

**Example input:**

```text
5
1 2 4 5
```

**Example output:**

```text
3
```

**Hint:** Use expected sum or search.

**Difficulty:** Hard

### Question 10: Two Sum Search

**Problem description:** Read numbers and target. Print yes if two different numbers add to target.

**Input format:** n, numbers, target.

**Output format:** yes or no.

**Example input:**

```text
5
2 4 7 1 9
8
```

**Example output:**

```text
yes
```

**Hint:** Remember numbers already seen.

**Difficulty:** Hard

