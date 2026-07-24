# String Basics

## Goal

Practice working with words, names, letters, and simple text actions.

## What students should know first

* Know variables.
* Know input and print.
* Know that strings are text inside quotes.

## Questions

### Question 1: Dragon Name Length

**Problem description:** Read a dragon name and print how many letters it has.

**Input format:** One word.

**Output format:** The length.

**Example input:**

```text
Sparkle
```

**Example output:**

```text
7
```

**Hint:** Use len(name).

**Difficulty:** Easy

### Question 2: First Letter Badge

**Problem description:** Read a camper name and print its first letter.

**Input format:** One word.

**Output format:** First character.

**Example input:**

```text
Mina
```

**Example output:**

```text
M
```

**Hint:** Index 0 gives the first character.

**Difficulty:** Easy

### Question 3: Last Letter Lantern

**Problem description:** Read a magic word and print its last letter.

**Input format:** One word.

**Output format:** Last character.

**Example input:**

```text
rainbow
```

**Example output:**

```text
w
```

**Hint:** Index -1 gives the last character.

**Difficulty:** Easy

### Question 4: Name Shout

**Problem description:** Read a name and print it in uppercase.

**Input format:** One word.

**Output format:** Uppercase name.

**Example input:**

```text
kiki
```

**Example output:**

```text
KIKI
```

**Hint:** Use upper().

**Difficulty:** Easy

### Question 5: Quiet Library

**Problem description:** Read a noisy word in uppercase and print it in lowercase.

**Input format:** One word.

**Output format:** Lowercase word.

**Example input:**

```text
BOOK
```

**Example output:**

```text
book
```

**Hint:** Use lower().

**Difficulty:** Medium

### Question 6: Join Two Words

**Problem description:** Read two words and join them with a hyphen.

**Input format:** Two words.

**Output format:** Hyphen joined text.

**Example input:**

```text
star
ship
```

**Example output:**

```text
star-ship
```

**Hint:** Use + or an f-string.

**Difficulty:** Medium

### Question 7: Double Word Spell

**Problem description:** Read a word and print it twice with no space.

**Input format:** One word.

**Output format:** Repeated word.

**Example input:**

```text
go
```

**Example output:**

```text
gogo
```

**Hint:** String multiplication works too.

**Difficulty:** Medium

### Question 8: Middle Slice Snack

**Problem description:** Read a word and print characters from index 1 up to but not including index 4.

**Input format:** One word with at least 4 letters.

**Output format:** The slice.

**Example input:**

```text
planet
```

**Example output:**

```text
lan
```

**Hint:** Use word[1:4].

**Difficulty:** Medium

### Question 9: Count the A's

**Problem description:** Read a word and count how many lowercase a letters it has.

**Input format:** One word.

**Output format:** Count of a.

**Example input:**

```text
banana
```

**Example output:**

```text
3
```

**Hint:** Use count('a') or a loop.

**Difficulty:** Hard

### Question 10: Palindrome Toy

**Problem description:** Read a word. Print yes if it reads the same forward and backward, otherwise no.

**Input format:** One word.

**Output format:** yes or no.

**Example input:**

```text
level
```

**Example output:**

```text
yes
```

**Hint:** Compare the word with word[::-1].

**Difficulty:** Hard

