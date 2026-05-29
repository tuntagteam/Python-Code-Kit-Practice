# Stack

## Goal

Practice last-in, first-out problems using a stack.

## What students should know first

* Know lists.
* Know append and pop.
* Know loops.

## Questions

### Question 1: Plate Stack

**Problem description:** Read commands push name and pop. Print the popped plates.

**Input format:** n, then n commands.

**Output format:** Popped names.

**Example input:**

```text
4
push red
push blue
pop
pop
```

**Example output:**

```text
blue
red
```

**Hint:** Last pushed is first popped.

**Difficulty:** Easy

### Question 2: Undo Text

**Problem description:** Read letters and UNDO commands. Build text with stack behavior and print final text.

**Input format:** n, then commands add x or undo.

**Output format:** Final text.

**Example input:**

```text
5
add c
add a
undo
add t
add s
```

**Example output:**

```text
cts
```

**Hint:** Pop the last letter on undo.

**Difficulty:** Easy

### Question 3: Balanced Parentheses

**Problem description:** Read a string of parentheses and print balanced or not balanced.

**Input format:** One string.

**Output format:** balanced or not balanced.

**Example input:**

```text
(()())
```

**Example output:**

```text
balanced
```

**Hint:** Push ( and pop for ).

**Difficulty:** Easy

### Question 4: Browser Back

**Problem description:** Read page visits and back commands. Print the final page.

**Input format:** n, then visit page or back.

**Output format:** Current page.

**Example input:**

```text
4
visit home
visit games
back
visit code
```

**Example output:**

```text
code
```

**Hint:** A stack can remember page history.

**Difficulty:** Medium

### Question 5: Reverse Words Stack

**Problem description:** Read words, push them, then pop to print reversed order.

**Input format:** One line words.

**Output format:** Reversed words.

**Example input:**

```text
red blue green
```

**Example output:**

```text
green blue red
```

**Hint:** Use append and pop.

**Difficulty:** Medium

### Question 6: Remove Stars

**Problem description:** Read a string where * deletes the previous character. Print the final string.

**Input format:** One string.

**Output format:** Clean string.

**Example input:**

```text
ab*c
```

**Example output:**

```text
ac
```

**Hint:** Use stack for kept characters.

**Difficulty:** Medium

### Question 7: Bracket Mix

**Problem description:** Read brackets using (), [], {}. Print balanced or not balanced.

**Input format:** One string.

**Output format:** balanced or not balanced.

**Example input:**

```text
([]{})
```

**Example output:**

```text
balanced
```

**Hint:** Match closing brackets to the stack top.

**Difficulty:** Medium

### Question 8: Next Greater Number

**Problem description:** Read numbers and print the next greater number to the right for each, or -1.

**Input format:** n then n integers.

**Output format:** Next greater list.

**Example input:**

```text
4
2 1 3 2
```

**Example output:**

```text
3 3 -1 -1
```

**Hint:** Use a stack of indexes.

**Difficulty:** Hard

### Question 9: Stack Min

**Problem description:** Process push, pop, and min commands. Print answers for min commands.

**Input format:** n, then commands.

**Output format:** Minimum values.

**Example input:**

```text
5
push 3
push 1
min
pop
min
```

**Example output:**

```text
1
3
```

**Hint:** Keep another stack of minimums.

**Difficulty:** Hard

### Question 10: Postfix Calculator

**Problem description:** Read a postfix expression with single-digit numbers and +. Print the result.

**Input format:** One line tokens.

**Output format:** Result.

**Example input:**

```text
2 3 + 4 +
```

**Example output:**

```text
9
```

**Hint:** Push numbers, pop two for an operator.

**Difficulty:** Hard

