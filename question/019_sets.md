# Sets

## Goal

Practice storing unique items and comparing groups.

## What students should know first

* Know lists.
* Know loops.
* Know unique values.

## Questions

### Question 1: Unique Stickers

**Problem description:** Read sticker names and print how many different stickers there are.

**Input format:** One line of words.

**Output format:** Unique count.

**Example input:**

```text
cat dog cat star
```

**Example output:**

```text
3
```

**Hint:** Convert the list to a set.

**Difficulty:** Easy

### Question 2: Club Members

**Problem description:** Read two club member lists. Print names that are in both clubs.

**Input format:** Two lines of names.

**Output format:** Common names sorted.

**Example input:**

```text
Ana Ben Cam
Ben Dan Ana
```

**Example output:**

```text
Ana Ben
```

**Hint:** Use set intersection.

**Difficulty:** Easy

### Question 3: All Friends

**Problem description:** Read two friend lists and print all unique names sorted.

**Input format:** Two lines of names.

**Output format:** Union names.

**Example input:**

```text
Mia Leo
Leo Zoe
```

**Example output:**

```text
Leo Mia Zoe
```

**Hint:** Use union or |.

**Difficulty:** Easy

### Question 4: Only Art Club

**Problem description:** Read art club and music club names. Print names only in art club sorted.

**Input format:** Two lines.

**Output format:** Names only in first set.

**Example input:**

```text
Ana Ben Cam
Ben
```

**Example output:**

```text
Ana Cam
```

**Hint:** Use set difference.

**Difficulty:** Medium

### Question 5: Duplicate Detector

**Problem description:** Read words. Print duplicate if any word appears twice, otherwise all unique.

**Input format:** One line words.

**Output format:** duplicate or all unique.

**Example input:**

```text
red blue red
```

**Example output:**

```text
duplicate
```

**Hint:** Compare list length and set length.

**Difficulty:** Medium

### Question 6: Treasure Types

**Problem description:** Read n treasure names and print each unique treasure sorted.

**Input format:** n, then n treasure names.

**Output format:** Unique treasures.

**Example input:**

```text
5
gem
coin
gem
map
coin
```

**Example output:**

```text
coin
gem
map
```

**Hint:** A set removes repeats.

**Difficulty:** Medium

### Question 7: Secret Guest

**Problem description:** Read invited names and arrived names. Print missing invited names sorted.

**Input format:** Two lines.

**Output format:** Missing names.

**Example input:**

```text
A B C
A C
```

**Example output:**

```text
B
```

**Hint:** invited - arrived.

**Difficulty:** Medium

### Question 8: Same Backpack

**Problem description:** Read two item lists. Print same if they contain the same unique items.

**Input format:** Two lines.

**Output format:** same or different.

**Example input:**

```text
pen pen map
map pen
```

**Example output:**

```text
same
```

**Hint:** Compare two sets.

**Difficulty:** Hard

### Question 9: New Cards

**Problem description:** Read old card names and new card names. Print cards that are new to the player sorted.

**Input format:** Two lines.

**Output format:** New cards.

**Example input:**

```text
sun moon
moon star
```

**Example output:**

```text
star
```

**Hint:** new_set - old_set.

**Difficulty:** Hard

### Question 10: Set Challenge

**Problem description:** Read three teams. Print names that appear in team 1 and team 2, but not team 3.

**Input format:** Three lines of names.

**Output format:** Sorted names.

**Example input:**

```text
A B C
B C D
C
```

**Example output:**

```text
B
```

**Hint:** Use intersection then difference.

**Difficulty:** Hard

