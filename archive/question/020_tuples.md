# Tuples

## Goal

Practice using fixed groups of values that stay together.

## What students should know first

* Know lists.
* Know indexes.
* Know that some data should not change.

## Questions

### Question 1: Point Printer

**Problem description:** Read x and y and store them as a tuple. Print x,y with a comma.

**Input format:** Two integers.

**Output format:** Coordinate.

**Example input:**

```text
3
5
```

**Example output:**

```text
3,5
```

**Hint:** Tuple values can be read by index.

**Difficulty:** Easy

### Question 2: Color Pair

**Problem description:** Read two colors and print them as first - second.

**Input format:** Two words.

**Output format:** Pair text.

**Example input:**

```text
red
blue
```

**Example output:**

```text
red - blue
```

**Hint:** Store both in one tuple.

**Difficulty:** Easy

### Question 3: Student Record

**Problem description:** Read name and age as a tuple. Print name is age.

**Input format:** Name and integer age.

**Output format:** Record sentence.

**Example input:**

```text
Nia
10
```

**Example output:**

```text
Nia is 10
```

**Hint:** Unpack the tuple.

**Difficulty:** Easy

### Question 4: Swap Tuple

**Problem description:** Read two numbers, store as a tuple, then print them swapped.

**Input format:** Two integers.

**Output format:** Swapped values.

**Example input:**

```text
4
9
```

**Example output:**

```text
9 4
```

**Hint:** Tuple unpacking can swap values.

**Difficulty:** Medium

### Question 5: First and Last

**Problem description:** Read three words as a tuple and print the first and last.

**Input format:** Three words.

**Output format:** First and last.

**Example input:**

```text
cat dog fish
```

**Example output:**

```text
cat fish
```

**Hint:** Use indexes 0 and -1.

**Difficulty:** Medium

### Question 6: Point Distance Simple

**Problem description:** Read x and y. Print x*x + y*y.

**Input format:** Two integers.

**Output format:** Squared distance from zero.

**Example input:**

```text
3
4
```

**Example output:**

```text
25
```

**Hint:** Unpack x and y from the tuple.

**Difficulty:** Medium

### Question 7: Tuple List

**Problem description:** Read n name score pairs into tuples. Print the first tuple's score.

**Input format:** n, then name score lines.

**Output format:** First score.

**Example input:**

```text
2
Ana 8
Ben 9
```

**Example output:**

```text
8
```

**Hint:** Store each pair as (name, score).

**Difficulty:** Medium

### Question 8: Best Pair

**Problem description:** Read n item price pairs. Print the item with the lowest price.

**Input format:** n, then item price lines.

**Output format:** Cheapest item.

**Example input:**

```text
3
pen 4
bag 20
eraser 2
```

**Example output:**

```text
eraser
```

**Hint:** Compare the second value in each tuple.

**Difficulty:** Hard

### Question 9: Coordinate Match

**Problem description:** Read two points. Print same if both coordinates match.

**Input format:** Four integers: x1 y1 x2 y2.

**Output format:** same or different.

**Example input:**

```text
2 3 2 3
```

**Example output:**

```text
same
```

**Hint:** Compare two tuples directly.

**Difficulty:** Hard

### Question 10: Sort Pairs

**Problem description:** Read n name score pairs and print them sorted by score from low to high.

**Input format:** n, then name score lines.

**Output format:** Sorted pairs.

**Example input:**

```text
3
A 9
B 5
C 7
```

**Example output:**

```text
B 5
C 7
A 9
```

**Hint:** Sort using the score part.

**Difficulty:** Hard

