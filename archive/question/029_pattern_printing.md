# Pattern Printing

## Goal

Practice printing shapes and patterns with loops.

## What students should know first

* Know for loops.
* Know nested loops.
* Know string multiplication.

## Questions

### Question 1: Star Line

**Problem description:** Read n and print n stars.

**Input format:** One integer.

**Output format:** One star line.

**Example input:**

```text
5
```

**Example output:**

```text
*****
```

**Hint:** Use string multiplication.

**Difficulty:** Easy

### Question 2: Star Square

**Problem description:** Read n and print an n by n square.

**Input format:** One integer.

**Output format:** Square.

**Example input:**

```text
3
```

**Example output:**

```text
***
***
***
```

**Hint:** Loop for rows.

**Difficulty:** Easy

### Question 3: Growing Triangle

**Problem description:** Read n and print rows from 1 to n stars.

**Input format:** One integer.

**Output format:** Triangle.

**Example input:**

```text
4
```

**Example output:**

```text
*
**
***
****
```

**Hint:** Each row has row number of stars.

**Difficulty:** Easy

### Question 4: Shrinking Triangle

**Problem description:** Read n and print rows from n stars down to 1.

**Input format:** One integer.

**Output format:** Triangle.

**Example input:**

```text
4
```

**Example output:**

```text
****
***
**
*
```

**Hint:** Loop downward.

**Difficulty:** Medium

### Question 5: Number Stairs

**Problem description:** Read n and print 1, then 12, then 123 up to n.

**Input format:** One integer.

**Output format:** Number pattern.

**Example input:**

```text
4
```

**Example output:**

```text
1
12
123
1234
```

**Hint:** Inner loop prints numbers.

**Difficulty:** Medium

### Question 6: Right Triangle

**Problem description:** Read n and print a right-aligned triangle.

**Input format:** One integer.

**Output format:** Right triangle.

**Example input:**

```text
3
```

**Example output:**

```text
  *
 **
***
```

**Hint:** Use spaces before stars.

**Difficulty:** Medium

### Question 7: Hollow Square

**Problem description:** Read n and print a hollow square.

**Input format:** One integer.

**Output format:** Hollow square.

**Example input:**

```text
4
```

**Example output:**

```text
****
*  *
*  *
****
```

**Hint:** Edges are stars.

**Difficulty:** Medium

### Question 8: Diamond Mini

**Problem description:** Read n and print a diamond with widest row n for odd n.

**Input format:** Odd integer.

**Output format:** Diamond.

**Example input:**

```text
3
```

**Example output:**

```text
 *
***
 *
```

**Hint:** Build top then bottom.

**Difficulty:** Hard

### Question 9: Checker Pattern

**Problem description:** Read n and print X and O checker pattern.

**Input format:** One integer.

**Output format:** Checker board.

**Example input:**

```text
3
```

**Example output:**

```text
XOX
OXO
XOX
```

**Hint:** Use row plus column parity.

**Difficulty:** Hard

### Question 10: Alphabet Steps

**Problem description:** Read n and print A, then AB, then ABC up to n letters.

**Input format:** One integer 1 to 26.

**Output format:** Letter pattern.

**Example input:**

```text
3
```

**Example output:**

```text
A
AB
ABC
```

**Hint:** Use chr() or a string of letters.

**Difficulty:** Hard

