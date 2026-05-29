# File Reading and Writing

## Goal

Practice reading information from files and writing results to files.

## What students should know first

* Know strings.
* Know lists.
* Know loops.

## Questions

### Question 1: Read One Line

**Problem description:** Read the first line from `message.txt` and print it without extra spaces.

**Input format:** File `message.txt` contains one line.

**Output format:** The line.

**Example input:**

```text
hello
```

**Example output:**

```text
hello
```

**Hint:** Use open() and read().

**Difficulty:** Easy

### Question 2: Count File Lines

**Problem description:** Read `notes.txt` and print how many lines it has.

**Input format:** File contents.

**Output format:** Line count.

**Example input:**

```text
red
blue
green
```

**Example output:**

```text
3
```

**Hint:** Loop over the file lines.

**Difficulty:** Easy

### Question 3: Write Greeting

**Problem description:** Read a name from input and write Hello name to `output.txt`.

**Input format:** One name.

**Output format:** File `output.txt` contains the greeting.

**Example input:**

```text
Mia
```

**Example output:**

```text
Hello Mia
```

**Hint:** Open the file in write mode.

**Difficulty:** Easy

### Question 4: Copy File

**Problem description:** Copy all text from `input.txt` to `copy.txt`.

**Input format:** File `input.txt`.

**Output format:** File `copy.txt` has the same text.

**Example input:**

```text
abc
```

**Example output:**

```text
abc
```

**Hint:** Read from one file and write to another.

**Difficulty:** Medium

### Question 5: Sum File Numbers

**Problem description:** Read integers from `numbers.txt`, one per line. Print their sum.

**Input format:** File contents.

**Output format:** Sum.

**Example input:**

```text
3
4
5
```

**Example output:**

```text
12
```

**Hint:** Convert each line to int.

**Difficulty:** Medium

### Question 6: Add Line Numbers

**Problem description:** Read `story.txt` and write numbered lines to `numbered.txt`.

**Input format:** File contents.

**Output format:** Numbered file contents.

**Example input:**

```text
cat
dog
```

**Example output:**

```text
1. cat
2. dog
```

**Hint:** Use enumerate starting at 1.

**Difficulty:** Medium

### Question 7: Find Word in File

**Problem description:** Read a target word from input and count how many lines in `book.txt` contain it.

**Input format:** Target word, plus file contents.

**Output format:** Matching line count.

**Example input:**

```text
star
star ship
moon
star map
```

**Example output:**

```text
2
```

**Hint:** Use in for each line.

**Difficulty:** Medium

### Question 8: Append Score

**Problem description:** Read a name and score. Append `name score` to `scores.txt`.

**Input format:** Two input lines.

**Output format:** The appended file line.

**Example input:**

```text
Ana
9
```

**Example output:**

```text
Ana 9
```

**Hint:** Open with append mode.

**Difficulty:** Hard

### Question 9: Highest File Score

**Problem description:** Read `scores.txt` where each line has name and score. Print the name with the highest score.

**Input format:** File contents.

**Output format:** Best name.

**Example input:**

```text
Ana 8
Ben 10
```

**Example output:**

```text
Ben
```

**Hint:** Split each line and compare scores.

**Difficulty:** Hard

### Question 10: Clean Blank Lines

**Problem description:** Read `messy.txt` and write only non-empty lines to `clean.txt`.

**Input format:** File contents.

**Output format:** Cleaned file contents.

**Example input:**

```text
cat

 dog
```

**Example output:**

```text
cat
 dog
```

**Hint:** Check if line.strip() is not empty.

**Difficulty:** Hard

