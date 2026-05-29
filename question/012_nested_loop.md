# Nested Loop

## Goal

Practice using loops inside other loops to work with grids and repeated patterns.

## What students should know first

* Know for loops.
* Know print output.
* Know how indentation works.

## Questions

### Question 1: Star Square

**Problem description:** Read n and print an n by n square of stars.

**Input format:** One integer.

**Output format:** Square pattern.

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

**Hint:** Use one loop for rows and one for columns.

**Difficulty:** Easy

### Question 2: Number Grid

**Problem description:** Read rows and columns. Print each row as 1 to columns.

**Input format:** Two integers.

**Output format:** Grid of numbers.

**Example input:**

```text
2
4
```

**Example output:**

```text
1 2 3 4
1 2 3 4
```

**Hint:** Build each row before printing.

**Difficulty:** Easy

### Question 3: Multiplication Mini Table

**Problem description:** Read n and print a table from 1x1 to nxn.

**Input format:** One integer.

**Output format:** Rows of products.

**Example input:**

```text
3
```

**Example output:**

```text
1 2 3
2 4 6
3 6 9
```

**Hint:** Multiply row number by column number.

**Difficulty:** Medium

### Question 4: Triangle Stars

**Problem description:** Read n and print a growing triangle.

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

**Hint:** The row number tells how many stars.

**Difficulty:** Medium

### Question 5: Seat Labels

**Problem description:** Read rows and seats. Print labels like R1S1.

**Input format:** Two integers.

**Output format:** Seat labels.

**Example input:**

```text
2
3
```

**Example output:**

```text
R1S1 R1S2 R1S3
R2S1 R2S2 R2S3
```

**Hint:** Nested loops can make row and seat numbers.

**Difficulty:** Medium

### Question 6: Checker Board

**Problem description:** Read n and print an n by n board using X and O alternating.

**Input format:** One integer.

**Output format:** Checker pattern.

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

**Hint:** Use (row + col) % 2.

**Difficulty:** Medium

### Question 7: Pair Maker

**Problem description:** Read two lists of letters and print every pair.

**Input format:** Two lines of space-separated letters.

**Output format:** One pair per line.

**Example input:**

```text
A B
1 2
```

**Example output:**

```text
A1
A2
B1
B2
```

**Hint:** Loop through the first list, then the second list.

**Difficulty:** Hard

### Question 8: Treasure Coordinates

**Problem description:** Read rows and columns. Print all coordinates as (r,c).

**Input format:** Two integers.

**Output format:** Coordinates.

**Example input:**

```text
2
2
```

**Example output:**

```text
(1,1) (1,2)
(2,1) (2,2)
```

**Hint:** Rows outside, columns inside.

**Difficulty:** Hard

### Question 9: Hollow Box

**Problem description:** Read n and print a hollow square border of stars.

**Input format:** One integer at least 2.

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

**Hint:** Print stars on edges and spaces inside.

**Difficulty:** Hard

### Question 10: Word Ladder Grid

**Problem description:** Read a word. Print prefixes from length 1 to full length.

**Input format:** One word.

**Output format:** One prefix per line.

**Example input:**

```text
code
```

**Example output:**

```text
c
co
cod
code
```

**Hint:** The inner loop prints characters up to the current length.

**Difficulty:** Hard

