# While Loop

## Goal

Practice repeating actions while a condition is still true.

## What students should know first

* Know if conditions.
* Know variables that can change.
* Know comparison operators.

## Questions

### Question 1: Rocket Fuel

**Problem description:** Read fuel. While fuel is above 0, print fuel and subtract 1.

**Input format:** One integer.

**Output format:** Fuel values.

**Example input:**

```text
3
```

**Example output:**

```text
3
2
1
```

**Hint:** Change the variable inside the loop.

**Difficulty:** Easy

### Question 2: Cookie Jar

**Problem description:** Read cookies. Keep removing 2 until no full pair remains. Print cookies left.

**Input format:** One integer.

**Output format:** Remaining cookies.

**Example input:**

```text
7
```

**Example output:**

```text
1
```

**Hint:** while cookies >= 2.

**Difficulty:** Easy

### Question 3: Password Repeat

**Problem description:** Read words until the word open appears. Print unlocked.

**Input format:** Several words, one per line, ending with open.

**Output format:** unlocked.

**Example input:**

```text
try
hello
open
```

**Example output:**

```text
unlocked
```

**Hint:** Loop while the word is not open.

**Difficulty:** Medium

### Question 4: Double Until Big

**Problem description:** Read n. Keep doubling it until it is at least 100, then print it.

**Input format:** One integer.

**Output format:** Final number.

**Example input:**

```text
13
```

**Example output:**

```text
104
```

**Hint:** Use n = n * 2.

**Difficulty:** Medium

### Question 5: Digit Counter

**Problem description:** Read a positive number and count its digits using a while loop.

**Input format:** One integer.

**Output format:** Digit count.

**Example input:**

```text
12345
```

**Example output:**

```text
5
```

**Hint:** Repeatedly use integer division by 10.

**Difficulty:** Medium

### Question 6: Savings Goal

**Problem description:** Read goal and weekly savings. Print how many weeks are needed to reach the goal.

**Input format:** Two integers.

**Output format:** Number of weeks.

**Example input:**

```text
25
6
```

**Example output:**

```text
5
```

**Hint:** Keep adding savings until total >= goal.

**Difficulty:** Medium

### Question 7: Guess Limit

**Problem description:** Read secret and then guesses until the guess matches. Print how many guesses were used.

**Input format:** First line secret, then guesses.

**Output format:** Guess count.

**Example input:**

```text
7
3
5
7
```

**Example output:**

```text
3
```

**Hint:** Count each guess.

**Difficulty:** Hard

### Question 8: Subtract Race

**Problem description:** Read a and b. Repeatedly subtract b from a while possible. Print the remainder.

**Input format:** Two integers.

**Output format:** Remainder.

**Example input:**

```text
17
5
```

**Example output:**

```text
2
```

**Hint:** This copies the idea of modulo.

**Difficulty:** Hard

### Question 9: Climb the Tower

**Problem description:** A player climbs up and slides down each turn. Read height, up, down. Print turns to reach or pass height.

**Input format:** Three integers.

**Output format:** Turns.

**Example input:**

```text
10
4
1
```

**Example output:**

```text
3
```

**Hint:** After climbing, check if the top is reached.

**Difficulty:** Hard

### Question 10: Collatz Junior

**Problem description:** Read n. While n is not 1, if n is even divide by 2, otherwise multiply by 3 and add 1. Print step count.

**Input format:** One integer.

**Output format:** Number of steps.

**Example input:**

```text
6
```

**Example output:**

```text
8
```

**Hint:** Update n each step and count.

**Difficulty:** Hard

