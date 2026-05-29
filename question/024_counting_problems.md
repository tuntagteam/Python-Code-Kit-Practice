# Counting Problems

## Goal

Practice counting items that match a rule.

## What students should know first

* Know loops.
* Know if statements.
* Know variables used as counters.

## Questions

### Question 1: Count Red Balloons

**Problem description:** Read n balloon colors and count how many are red.

**Input format:** First line n, second line n colors.

**Output format:** Number of red balloons.

**Example input:**

```text
5
red blue red green red
```

**Example output:**

```text
3
```

**Hint:** Start a counter at 0.

**Difficulty:** Easy

### Question 2: Even Counter

**Problem description:** Read numbers and count how many are even.

**Input format:** First line n, second line n integers.

**Output format:** Even count.

**Example input:**

```text
6
1 2 4 5 7 8
```

**Example output:**

```text
3
```

**Hint:** Use num % 2 == 0.

**Difficulty:** Easy

### Question 3: Long Word Count

**Problem description:** Read words and count words with more than 4 letters.

**Input format:** One line of words.

**Output format:** Count.

**Example input:**

```text
cat robot school
```

**Example output:**

```text
2
```

**Hint:** Use len(word).

**Difficulty:** Easy

### Question 4: Passing Scores

**Problem description:** Read scores and count scores at least 50.

**Input format:** First line n, second line n scores.

**Output format:** Pass count.

**Example input:**

```text
5
40 55 70 49 90
```

**Example output:**

```text
3
```

**Hint:** Compare each score.

**Difficulty:** Medium

### Question 5: Vowel Counter

**Problem description:** Read a word and count vowels a e i o u.

**Input format:** One word.

**Output format:** Vowel count.

**Example input:**

```text
planet
```

**Example output:**

```text
2
```

**Hint:** Check if each letter is in a vowel string.

**Difficulty:** Medium

### Question 6: Between Numbers

**Problem description:** Read numbers and count how many are between 10 and 20 inclusive.

**Input format:** n then n integers.

**Output format:** Count.

**Example input:**

```text
5
9 10 15 21 20
```

**Example output:**

```text
3
```

**Hint:** Use two comparisons.

**Difficulty:** Medium

### Question 7: Pair Count

**Problem description:** Read n numbers and count neighboring pairs that are equal.

**Input format:** n then n integers.

**Output format:** Equal neighbor count.

**Example input:**

```text
5
1 1 2 3 3
```

**Example output:**

```text
2
```

**Hint:** Compare item i with item i - 1.

**Difficulty:** Medium

### Question 8: Word Starts

**Problem description:** Read words and a letter. Count words that start with that letter.

**Input format:** One line words, then one letter.

**Output format:** Count.

**Example input:**

```text
sun star moon
s
```

**Example output:**

```text
2
```

**Hint:** Use word[0].

**Difficulty:** Hard

### Question 9: Mountain Days

**Problem description:** Read temperatures and count days warmer than the previous day.

**Input format:** n then n integers.

**Output format:** Warmer day count.

**Example input:**

```text
5
20 21 19 22 23
```

**Example output:**

```text
3
```

**Hint:** Start from the second value.

**Difficulty:** Hard

### Question 10: Special Count

**Problem description:** Read numbers and count numbers divisible by 3 but not by 2.

**Input format:** n then n integers.

**Output format:** Count.

**Example input:**

```text
6
3 6 9 12 15 18
```

**Example output:**

```text
3
```

**Hint:** Combine conditions with and.

**Difficulty:** Hard

