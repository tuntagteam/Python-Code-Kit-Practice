# Lists

## Goal

Practice storing many items in one Python list.

## What students should know first

* Know variables.
* Know strings and numbers.
* Know for loops.

## Questions

### Question 1: Pet Backpack

**Problem description:** Read n pet names into a list and print the first pet.

**Input format:** First line n, then n names.

**Output format:** First name.

**Example input:**

```text
3
cat
dog
fish
```

**Example output:**

```text
cat
```

**Hint:** Use list indexing.

**Difficulty:** Easy

### Question 2: Last Snack

**Problem description:** Read snacks on one line and print the last snack.

**Input format:** One line of words.

**Output format:** Last word.

**Example input:**

```text
chips apple cake
```

**Example output:**

```text
cake
```

**Hint:** Use split() and index -1.

**Difficulty:** Easy

### Question 3: List Length

**Problem description:** Read a line of toy names and print how many toys are in the list.

**Input format:** One line of words.

**Output format:** Count.

**Example input:**

```text
ball kite car
```

**Example output:**

```text
3
```

**Hint:** len(list_name) gives the size.

**Difficulty:** Easy

### Question 4: Second Score

**Problem description:** Read scores and print the second score.

**Input format:** One line of integers.

**Output format:** Second number.

**Example input:**

```text
5 9 2
```

**Example output:**

```text
9
```

**Hint:** Indexes start at 0.

**Difficulty:** Medium

### Question 5: Print All Items

**Problem description:** Read a list of colors and print each color on its own line.

**Input format:** One line of words.

**Output format:** Colors, one per line.

**Example input:**

```text
red blue green
```

**Example output:**

```text
red
blue
green
```

**Hint:** Loop over the list.

**Difficulty:** Medium

### Question 6: Bigger Than Ten

**Problem description:** Read numbers and print only the numbers greater than 10.

**Input format:** One line of integers.

**Output format:** Matching numbers.

**Example input:**

```text
4 12 8 15
```

**Example output:**

```text
12
15
```

**Hint:** Use an if inside a loop.

**Difficulty:** Medium

### Question 7: Reverse List

**Problem description:** Read words and print them in reverse order on one line.

**Input format:** One line of words.

**Output format:** Words reversed.

**Example input:**

```text
one two three
```

**Example output:**

```text
three two one
```

**Hint:** Use reversed() or slicing.

**Difficulty:** Medium

### Question 8: Index Finder

**Problem description:** Read words and a target. Print the first index of the target, or -1 if missing.

**Input format:** One line words, then target.

**Output format:** Index or -1.

**Example input:**

```text
red blue green
blue
```

**Example output:**

```text
1
```

**Hint:** Loop with indexes.

**Difficulty:** Hard

### Question 9: Every Other Toy

**Problem description:** Read toy names and print every other toy starting from the first.

**Input format:** One line of words.

**Output format:** Selected toys.

**Example input:**

```text
a b c d e
```

**Example output:**

```text
a c e
```

**Hint:** Use slicing with step 2.

**Difficulty:** Hard

### Question 10: List Copy Change

**Problem description:** Read numbers. Make a new list where each number is doubled. Print the new list values.

**Input format:** One line of integers.

**Output format:** Doubled numbers.

**Example input:**

```text
1 3 5
```

**Example output:**

```text
2 6 10
```

**Hint:** Append doubled values to a new list.

**Difficulty:** Hard

