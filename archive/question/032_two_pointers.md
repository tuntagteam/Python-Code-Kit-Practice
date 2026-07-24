# Two Pointers

## Goal

Practice using two positions in a list or string to solve problems faster.

## What students should know first

* Know lists and strings.
* Know while loops.
* Know indexes.

## Questions

### Question 1: Pair Sum Sorted

**Problem description:** Read a sorted list and target. Print yes if two numbers add to target.

**Input format:** n, sorted numbers, target.

**Output format:** yes or no.

**Example input:**

```text
5
1 2 4 7 9
11
```

**Example output:**

```text
yes
```

**Hint:** Start one pointer at each end.

**Difficulty:** Easy

### Question 2: Reverse With Pointers

**Problem description:** Read a word and print it reversed by moving from both ends.

**Input format:** One word.

**Output format:** Reversed word.

**Example input:**

```text
robot
```

**Example output:**

```text
tobor
```

**Hint:** Move inward from the ends.

**Difficulty:** Easy

### Question 3: Palindrome Check

**Problem description:** Read a word and use two pointers to print yes if it is a palindrome.

**Input format:** One word.

**Output format:** yes or no.

**Example input:**

```text
level
```

**Example output:**

```text
yes
```

**Hint:** Compare left and right letters.

**Difficulty:** Easy

### Question 4: Closest Pair Sum

**Problem description:** Read sorted numbers and target. Print the pair sum closest to target.

**Input format:** n, sorted numbers, target.

**Output format:** Closest sum.

**Example input:**

```text
5
1 3 5 8 12
10
```

**Example output:**

```text
9
```

**Hint:** Move the pointer that helps the sum.

**Difficulty:** Medium

### Question 5: Count Pairs Under

**Problem description:** Read sorted numbers and x. Count pairs with sum less than x.

**Input format:** n, sorted numbers, x.

**Output format:** Pair count.

**Example input:**

```text
4
1 2 3 4
6
```

**Example output:**

```text
4
```

**Hint:** When left+right is small, many pairs work.

**Difficulty:** Medium

### Question 6: Move Zeros

**Problem description:** Read numbers and move all zeros to the end, keeping other order.

**Input format:** n then n integers.

**Output format:** Reordered numbers.

**Example input:**

```text
6
0 1 0 3 0 5
```

**Example output:**

```text
1 3 5 0 0 0
```

**Hint:** Use one pointer for next non-zero spot.

**Difficulty:** Medium

### Question 7: Container Water Junior

**Problem description:** Read heights and find the biggest area between two lines.

**Input format:** n then n integers.

**Output format:** Max area.

**Example input:**

```text
5
1 3 2 5 4
```

**Example output:**

```text
9
```

**Hint:** Move the shorter side inward.

**Difficulty:** Hard

### Question 8: Remove Duplicates Sorted

**Problem description:** Read sorted numbers and print each unique number once.

**Input format:** n then sorted integers.

**Output format:** Unique numbers.

**Example input:**

```text
7
1 1 2 2 2 3 4
```

**Example output:**

```text
1 2 3 4
```

**Hint:** Compare current with previous.

**Difficulty:** Medium

### Question 9: Three Sum Zero

**Problem description:** Read numbers and print yes if any three add to zero.

**Input format:** n then integers.

**Output format:** yes or no.

**Example input:**

```text
5
-3 1 2 4 -1
```

**Example output:**

```text
yes
```

**Hint:** Sort, then fix one number and use two pointers.

**Difficulty:** Hard

### Question 10: Merge Names

**Problem description:** Read two alphabetically sorted name lists and merge them.

**Input format:** Two lines of names.

**Output format:** Merged names.

**Example input:**

```text
Ana Kai
Ben Zoe
```

**Example output:**

```text
Ana Ben Kai Zoe
```

**Hint:** Use two pointers over the lists.

**Difficulty:** Hard

