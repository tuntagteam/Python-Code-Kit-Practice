# For Loop

## Goal

Practice repeating actions a known number of times.

## What students should know first

* Know variables.
* Know lists or ranges.
* Know how to print inside a block.

## Questions

### Question 1: Rocket Countdown

**Problem description:** Read n and print numbers from n down to 1.

**Input format:** One integer n.

**Output format:** One number per line.

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

**Hint:** Use range with a negative step.

**Difficulty:** Easy

### Question 2: Cheer Squad

**Problem description:** Read a word and n. Print the word n times.

**Input format:** A word and an integer.

**Output format:** The word repeated on separate lines.

**Example input:**

```text
Go
3
```

**Example output:**

```text
Go
Go
Go
```

**Hint:** Loop n times.

**Difficulty:** Easy

### Question 3: Number Parade

**Problem description:** Read n and print numbers from 1 to n.

**Input format:** One integer.

**Output format:** One number per line.

**Example input:**

```text
4
```

**Example output:**

```text
1
2
3
4
```

**Hint:** range(1, n + 1) helps.

**Difficulty:** Easy

### Question 4: Even Steps

**Problem description:** Read n and print even numbers from 2 to n.

**Input format:** One integer.

**Output format:** Even numbers.

**Example input:**

```text
8
```

**Example output:**

```text
2
4
6
8
```

**Hint:** Use range(2, n + 1, 2).

**Difficulty:** Medium

### Question 5: Sticker Sum

**Problem description:** Read n sticker values and print their sum.

**Input format:** First line n, then n integers.

**Output format:** Total.

**Example input:**

```text
4
2
3
5
1
```

**Example output:**

```text
11
```

**Hint:** Add each value inside the loop.

**Difficulty:** Medium

### Question 6: Name Letters

**Problem description:** Read a name and print each letter on its own line.

**Input format:** One word.

**Output format:** One character per line.

**Example input:**

```text
Milo
```

**Example output:**

```text
M
i
l
o
```

**Hint:** A for loop can loop over a string.

**Difficulty:** Medium

### Question 7: Times Table

**Problem description:** Read n and print n times 1 through 5.

**Input format:** One integer.

**Output format:** Five multiplication lines.

**Example input:**

```text
3
```

**Example output:**

```text
3
6
9
12
15
```

**Hint:** Multiply n by the loop number.

**Difficulty:** Medium

### Question 8: Count Big Scores

**Problem description:** Read n scores and count how many are at least 10.

**Input format:** First line n, then n integers.

**Output format:** Count.

**Example input:**

```text
5
8
10
12
6
15
```

**Example output:**

```text
3
```

**Hint:** Use an if inside the loop.

**Difficulty:** Hard

### Question 9: Reverse Word Print

**Problem description:** Read a word and print its letters from last to first.

**Input format:** One word.

**Output format:** One reversed letter per line.

**Example input:**

```text
cat
```

**Example output:**

```text
t
a
c
```

**Hint:** Loop over indexes from len(word)-1 down to 0.

**Difficulty:** Hard

### Question 10: Factor Finder

**Problem description:** Read n and print all numbers from 1 to n that divide n evenly.

**Input format:** One integer.

**Output format:** One factor per line.

**Example input:**

```text
6
```

**Example output:**

```text
1
2
3
6
```

**Hint:** Use n % i == 0.

**Difficulty:** Hard

