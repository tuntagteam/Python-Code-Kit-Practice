# Error Handling

## Goal

Practice handling mistakes in input or code without crashing.

## What students should know first

* Know input.
* Know if statements.
* Know that programs can receive unexpected data.

## Questions

### Question 1: Number Guard

**Problem description:** Read one value. Try to convert it to an integer. Print ok if it works, otherwise print not a number.

**Input format:** One value.

**Output format:** ok or not a number.

**Example input:**

```text
12
```

**Example output:**

```text
ok
```

**Hint:** Use try and except ValueError.

**Difficulty:** Easy

### Question 2: Safe Age

**Problem description:** Read an age. If it is not a number, print invalid. Otherwise print age next year.

**Input format:** One value.

**Output format:** Next age or invalid.

**Example input:**

```text
ten
```

**Example output:**

```text
invalid
```

**Hint:** Put int() inside try.

**Difficulty:** Easy

### Question 3: Divide Helper

**Problem description:** Read a and b. Print a / b, but print cannot divide if b is 0.

**Input format:** Two integers.

**Output format:** Result or message.

**Example input:**

```text
8
0
```

**Example output:**

```text
cannot divide
```

**Hint:** Catch ZeroDivisionError or check first.

**Difficulty:** Easy

### Question 4: Score Input

**Problem description:** Read a score. Print valid if it is an integer from 0 to 100, otherwise invalid.

**Input format:** One value.

**Output format:** valid or invalid.

**Example input:**

```text
105
```

**Example output:**

```text
invalid
```

**Hint:** Handle bad conversion and bad range.

**Difficulty:** Medium

### Question 5: List Index Guard

**Problem description:** Read a list and an index. Print the item, or print missing if the index is not valid.

**Input format:** One line words, then index.

**Output format:** Item or missing.

**Example input:**

```text
red blue
5
```

**Example output:**

```text
missing
```

**Hint:** Catch IndexError.

**Difficulty:** Medium

### Question 6: Dictionary Guard

**Problem description:** Read name-score pairs and a target name. Print the score or unknown.

**Input format:** n, pairs, then target.

**Output format:** Score or unknown.

**Example input:**

```text
1
Ana 9
Ben
```

**Example output:**

```text
unknown
```

**Hint:** Use get() or catch KeyError.

**Difficulty:** Medium

### Question 7: Retry Until Number

**Problem description:** Read values until one can be converted to an integer. Print that integer.

**Input format:** Several lines.

**Output format:** First valid integer.

**Example input:**

```text
cat
4
```

**Example output:**

```text
4
```

**Hint:** Use a loop with try except.

**Difficulty:** Medium

### Question 8: Safe Average

**Problem description:** Read numbers from one line. If the line is empty, print no numbers. Otherwise print the average.

**Input format:** One line, maybe empty.

**Output format:** Average or message.

**Example input:**

```text
```

**Example output:**

```text
no numbers
```

**Hint:** Check length before dividing.

**Difficulty:** Hard

### Question 9: Clean Number List

**Problem description:** Read words and add only the ones that are valid integers. Print their sum.

**Input format:** One line of values.

**Output format:** Sum of valid integers.

**Example input:**

```text
3 cat 4 sun
```

**Example output:**

```text
7
```

**Hint:** Try converting each word.

**Difficulty:** Hard

### Question 10: Final Always

**Problem description:** Read a filename. Try to print open file. Always print done after that.

**Input format:** One filename.

**Output format:** Two lines if no error, or error then done.

**Example input:**

```text
notes.txt
```

**Example output:**

```text
open file
done
```

**Hint:** Use finally to run cleanup-style code.

**Difficulty:** Hard

