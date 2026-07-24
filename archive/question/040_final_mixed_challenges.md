# Final Mixed Challenges

## Goal

Practice mixing many Python skills to solve bigger challenges.

## What students should know first

* Know all earlier topics.
* Know how to plan a solution.
* Know how to test examples.

## Questions

### Question 1: Classroom Report

**Problem description:** Read names and scores. Print average score and the highest scoring name.

**Input format:** n, then name score lines.

**Output format:** Average and best name.

**Example input:**

```text
3
Ana 8
Ben 10
Cam 6
```

**Example output:**

```text
8.0
Ben
```

**Hint:** Use sum, max, and a loop.

**Difficulty:** Easy

### Question 2: Treasure Map Steps

**Problem description:** Read move commands N S E W. Print final x y position.

**Input format:** One line of commands.

**Output format:** Final coordinates.

**Example input:**

```text
N E E S W
```

**Example output:**

```text
1 0
```

**Hint:** Track x and y variables.

**Difficulty:** Easy

### Question 3: Shop Basket

**Problem description:** Read item prices, apply discount if total is at least 100, and print final total.

**Input format:** n then n prices.

**Output format:** Final total.

**Example input:**

```text
3
40 35 30
```

**Example output:**

```text
95
```

**Hint:** Subtract 10 when total >= 100.

**Difficulty:** Easy

### Question 4: Word Lab

**Problem description:** Read a sentence. Print the longest word and number of unique words.

**Input format:** One line sentence.

**Output format:** Longest word and unique count.

**Example input:**

```text
red blue red yellow
```

**Example output:**

```text
yellow
3
```

**Hint:** Use split, set, and max by length.

**Difficulty:** Medium

### Question 5: Game Inventory

**Problem description:** Read add/remove item commands. Print final inventory sorted.

**Input format:** n, then commands.

**Output format:** Sorted items.

**Example input:**

```text
4
add map
add key
remove map
add gem
```

**Example output:**

```text
gem key
```

**Hint:** Use a set or list carefully.

**Difficulty:** Medium

### Question 6: Robot Energy Route

**Problem description:** Read energy changes. Print first step when energy becomes negative, or safe.

**Input format:** Start energy, n, changes.

**Output format:** Step number or safe.

**Example input:**

```text
5
4
-2 -2 -3 4
```

**Example output:**

```text
3
```

**Hint:** Simulate and stop when needed.

**Difficulty:** Medium

### Question 7: Mini Leaderboard

**Problem description:** Read scores for players, possibly repeated. Print players sorted by total score high to low.

**Input format:** n, then name score lines.

**Output format:** Leaderboard.

**Example input:**

```text
4
A 5
B 7
A 4
C 6
```

**Example output:**

```text
A 9
B 7
C 6
```

**Hint:** Use a dictionary, then sort.

**Difficulty:** Medium

### Question 8: Path Finder

**Problem description:** Read a graph of rooms and print shortest steps from start to goal.

**Input format:** n m, edges, start goal.

**Output format:** Step count or -1.

**Example input:**

```text
4 3
A B
B C
C D
A D
```

**Example output:**

```text
3
```

**Hint:** Use BFS.

**Difficulty:** Hard

### Question 9: Best Study Streak

**Problem description:** Read daily minutes. Print the longest streak of days with at least 30 minutes.

**Input format:** n then n integers.

**Output format:** Longest streak.

**Example input:**

```text
7
20 30 40 10 35 36 37
```

**Example output:**

```text
3
```

**Hint:** Reset streak when a day is too small.

**Difficulty:** Hard

### Question 10: Challenge Tournament

**Problem description:** Read player scores. Print the second highest unique score, or none if it does not exist.

**Input format:** n then n integers.

**Output format:** Second highest or none.

**Example input:**

```text
6
10 8 10 6 8 5
```

**Example output:**

```text
8
```

**Hint:** Use set to remove duplicates, then sort.

**Difficulty:** Hard

