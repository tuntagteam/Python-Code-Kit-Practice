# Dictionaries

## Goal

Practice storing pairs of keys and values, like names and scores.

## What students should know first

* Know lists.
* Know loops.
* Know strings as keys.

## Questions

### Question 1: Pet Ages

**Problem description:** Read n pet names and ages into a dictionary. Then read one pet name and print its age.

**Input format:** First line n, then n name age lines, then target name.

**Output format:** Age.

**Example input:**

```text
3
Milo 4
Luna 2
Pip 5
Luna
```

**Example output:**

```text
2
```

**Hint:** Names are keys and ages are values.

**Difficulty:** Easy

### Question 2: Score Lookup

**Problem description:** Store player scores from input and print the score for one player.

**Input format:** First line n, then n name score lines, then target.

**Output format:** Target score.

**Example input:**

```text
2
Ana 10
Ben 7
Ana
```

**Example output:**

```text
10
```

**Hint:** Use dictionary[target].

**Difficulty:** Easy

### Question 3: Add New Word

**Problem description:** Read a tiny dictionary of word meanings, add one new word, and print the number of words.

**Input format:** n, then n word meaning lines, then new word and meaning.

**Output format:** Dictionary size.

**Example input:**

```text
1
cat animal
dog animal
```

**Example output:**

```text
2
```

**Hint:** Assign dict[new_word] = meaning.

**Difficulty:** Medium

### Question 4: Favorite Color

**Problem description:** Read names and colors. Print yes if a target name is in the dictionary.

**Input format:** n, then n name color lines, then target.

**Output format:** yes or no.

**Example input:**

```text
2
Mia red
Leo blue
Mia
```

**Example output:**

```text
yes
```

**Hint:** Use in to check keys.

**Difficulty:** Medium

### Question 5: Update Score

**Problem description:** Read player scores, then a player and bonus. Add the bonus to that player's score.

**Input format:** n, score lines, then name bonus.

**Output format:** Updated score.

**Example input:**

```text
2
Ari 5
Kai 9
Ari 3
```

**Example output:**

```text
8
```

**Hint:** Read, update, then print.

**Difficulty:** Medium

### Question 6: Print Keys

**Problem description:** Read n name score pairs and print all names in input order.

**Input format:** n, then pairs.

**Output format:** Names.

**Example input:**

```text
3
A 1
B 2
C 3
```

**Example output:**

```text
A
B
C
```

**Hint:** Modern Python keeps insertion order.

**Difficulty:** Medium

### Question 7: Total Coins

**Problem description:** Read item coin values in a dictionary and print the total of all values.

**Input format:** n, then item coins lines.

**Output format:** Total coins.

**Example input:**

```text
3
map 5
key 2
gem 10
```

**Example output:**

```text
17
```

**Hint:** Loop over values.

**Difficulty:** Medium

### Question 8: Highest Score Name

**Problem description:** Read names and scores. Print the name with the highest score.

**Input format:** n, then name score lines.

**Output format:** Best name.

**Example input:**

```text
3
Ana 8
Ben 12
Cam 9
```

**Example output:**

```text
Ben
```

**Hint:** Track best name and score.

**Difficulty:** Hard

### Question 9: Word Counter

**Problem description:** Read words and build a dictionary counting each word. Print the count for a target word.

**Input format:** One line words, then target.

**Output format:** Count.

**Example input:**

```text
red blue red green
red
```

**Example output:**

```text
2
```

**Hint:** Use get(word, 0) + 1.

**Difficulty:** Hard

### Question 10: Class Points

**Problem description:** Read score changes as name points. Sum points by name and print each final score in input name order.

**Input format:** n, then n name points lines.

**Output format:** Name and total lines.

**Example input:**

```text
4
A 3
B 5
A 2
C 1
```

**Example output:**

```text
A 5
B 5
C 1
```

**Hint:** Create new keys when first seen.

**Difficulty:** Hard

