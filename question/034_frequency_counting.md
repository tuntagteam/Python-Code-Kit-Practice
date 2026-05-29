# Frequency Counting

## Goal

Practice counting how many times each item appears.

## What students should know first

* Know dictionaries.
* Know loops.
* Know counting problems.

## Questions

### Question 1: Most Common Color

**Problem description:** Read colors and print the color that appears most often.

**Input format:** One line colors.

**Output format:** Most common color.

**Example input:**

```text
red blue red green
```

**Example output:**

```text
red
```

**Hint:** Use a dictionary of counts.

**Difficulty:** Easy

### Question 2: Letter Counts

**Problem description:** Read a word and print each different letter with its count in alphabetical order.

**Input format:** One word.

**Output format:** Letter counts.

**Example input:**

```text
banana
```

**Example output:**

```text
a 3
b 1
n 2
```

**Hint:** Count characters, then sort keys.

**Difficulty:** Easy

### Question 3: Number Frequency

**Problem description:** Read numbers and a target. Print target frequency.

**Input format:** n, numbers, target.

**Output format:** Count.

**Example input:**

```text
5
1 2 2 3 2
2
```

**Example output:**

```text
3
```

**Hint:** Dictionary counts work for numbers too.

**Difficulty:** Easy

### Question 4: Unique Count

**Problem description:** Read words and print how many appear exactly once.

**Input format:** One line words.

**Output format:** Unique-once count.

**Example input:**

```text
cat dog cat bird
```

**Example output:**

```text
2
```

**Hint:** Count, then count values equal to 1.

**Difficulty:** Medium

### Question 5: Can Make Word

**Problem description:** Read letters and a target word. Print yes if the letters can build the word.

**Input format:** Letters string, then target.

**Output format:** yes or no.

**Example input:**

```text
aabbcc
abc
```

**Example output:**

```text
yes
```

**Hint:** Compare needed counts to available counts.

**Difficulty:** Medium

### Question 6: Anagram Groups

**Problem description:** Read words and print how many pairs are anagrams.

**Input format:** n then n words.

**Output format:** Pair count.

**Example input:**

```text
4
cat
act
dog
tac
```

**Example output:**

```text
3
```

**Hint:** Sorted letters can be a frequency key.

**Difficulty:** Medium

### Question 7: First Non-Repeating

**Problem description:** Read a word and print the first character that appears once, or none.

**Input format:** One word.

**Output format:** Character or none.

**Example input:**

```text
swiss
```

**Example output:**

```text
w
```

**Hint:** Count first, then scan original order.

**Difficulty:** Medium

### Question 8: Inventory Merge

**Problem description:** Read two inventories item count. Print total count for each item alphabetically.

**Input format:** n pairs, then m pairs.

**Output format:** Merged inventory.

**Example input:**

```text
2
pen 3
bag 1
2
pen 2
map 4
```

**Example output:**

```text
bag 1
map 4
pen 5
```

**Hint:** Add counts for matching keys.

**Difficulty:** Hard

### Question 9: Mode With Tie

**Problem description:** Read numbers and print the most frequent number. If tied, print the smallest.

**Input format:** n then n integers.

**Output format:** Mode.

**Example input:**

```text
6
4 2 4 2 3 2
```

**Example output:**

```text
2
```

**Hint:** Sort keys when checking ties.

**Difficulty:** Hard

### Question 10: Frequency Sort

**Problem description:** Read words and print them sorted by frequency high to low, then alphabetically.

**Input format:** One line words.

**Output format:** Sorted unique words.

**Example input:**

```text
red blue red apple blue red
```

**Example output:**

```text
red blue apple
```

**Hint:** Sort by (-count, word).

**Difficulty:** Hard

