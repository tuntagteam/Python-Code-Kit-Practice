# Sorting Basics

## Goal

Practice putting values into a useful order.

## What students should know first

* Know lists.
* Know comparisons.
* Know loops.

## Questions

### Question 1: Line Up Scores

**Problem description:** Read scores and print them from smallest to biggest.

**Input format:** First line n, second line n integers.

**Output format:** Sorted scores.

**Example input:**

```text
5
8 3 5 1 4
```

**Example output:**

```text
1 3 4 5 8
```

**Hint:** Use sorted() while learning the idea.

**Difficulty:** Easy

### Question 2: Alphabet Names

**Problem description:** Read names and print them alphabetically.

**Input format:** One line names.

**Output format:** Sorted names.

**Example input:**

```text
Zoe Ana Ben
```

**Example output:**

```text
Ana Ben Zoe
```

**Hint:** sorted() works with strings.

**Difficulty:** Easy

### Question 3: Big to Small

**Problem description:** Read numbers and print them from biggest to smallest.

**Input format:** n then n integers.

**Output format:** Descending numbers.

**Example input:**

```text
4
2 9 1 5
```

**Example output:**

```text
9 5 2 1
```

**Hint:** Use reverse=True.

**Difficulty:** Easy

### Question 4: Sort Word Letters

**Problem description:** Read a word and print its letters sorted.

**Input format:** One word.

**Output format:** Sorted letters.

**Example input:**

```text
banana
```

**Example output:**

```text
aaabnn
```

**Hint:** Sort the characters then join them.

**Difficulty:** Medium

### Question 5: Shortest to Longest

**Problem description:** Read words and print them by length.

**Input format:** One line words.

**Output format:** Words by length.

**Example input:**

```text
moon cat elephant
```

**Example output:**

```text
cat moon elephant
```

**Hint:** Use key=len.

**Difficulty:** Medium

### Question 6: Sort Scores With Names

**Problem description:** Read name score pairs and print names from lowest score to highest.

**Input format:** n then pairs.

**Output format:** Names in score order.

**Example input:**

```text
3
Ana 9
Ben 5
Cam 7
```

**Example output:**

```text
Ben Cam Ana
```

**Hint:** Sort pairs by score.

**Difficulty:** Medium

### Question 7: Find Median

**Problem description:** Read odd n numbers and print the middle value after sorting.

**Input format:** Odd n, then n integers.

**Output format:** Median.

**Example input:**

```text
5
9 1 5 3 7
```

**Example output:**

```text
5
```

**Hint:** Sort then use index n//2.

**Difficulty:** Medium

### Question 8: Keep Top Three

**Problem description:** Read scores and print the top three from highest to lowest.

**Input format:** n then n integers.

**Output format:** Top three.

**Example input:**

```text
5
4 10 8 2 9
```

**Example output:**

```text
10 9 8
```

**Hint:** Sort descending and slice.

**Difficulty:** Hard

### Question 9: Sort by Last Letter

**Problem description:** Read words and sort them by their last letter.

**Input format:** One line words.

**Output format:** Sorted words.

**Example input:**

```text
dog cat bee
```

**Example output:**

```text
bee dog cat
```

**Hint:** Use key that returns word[-1].

**Difficulty:** Hard

### Question 10: Stable Queue Sort

**Problem description:** Read arrival number and score pairs. Sort by score high to low, keeping arrival order for ties.

**Input format:** n then arrival score lines.

**Output format:** Arrival numbers.

**Example input:**

```text
4
1 10
2 8
3 10
4 7
```

**Example output:**

```text
1 3 2 4
```

**Hint:** Python sorting is stable.

**Difficulty:** Hard

