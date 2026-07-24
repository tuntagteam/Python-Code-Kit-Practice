# Simulation Problems

## Goal

Practice copying a real or imaginary process step by step in code.

## What students should know first

* Know loops.
* Know if statements.
* Know changing variables over time.

## Questions

### Question 1: Robot Walk

**Problem description:** Read moves like F and B. F adds 1, B subtracts 1. Print final position.

**Input format:** One line of move letters.

**Output format:** Position.

**Example input:**

```text
F F B F
```

**Example output:**

```text
2
```

**Hint:** Simulate each move.

**Difficulty:** Easy

### Question 2: Coin Jar Days

**Problem description:** Read starting coins and daily changes. Print final coins.

**Input format:** Start, n, then n changes.

**Output format:** Final coins.

**Example input:**

```text
10
3
2 -1 5
```

**Example output:**

```text
16
```

**Hint:** Update the coins each day.

**Difficulty:** Easy

### Question 3: Health Potion

**Problem description:** Read health and actions. heal adds 5, hit subtracts 3. Print final health.

**Input format:** Health, n, then n action words.

**Output format:** Final health.

**Example input:**

```text
10
3
heal hit heal
```

**Example output:**

```text
17
```

**Hint:** Use if for each action.

**Difficulty:** Medium

### Question 4: Queue Tickets

**Problem description:** Read people count and served count. Print people left.

**Input format:** Two integers.

**Output format:** Remaining people.

**Example input:**

```text
12
5
```

**Example output:**

```text
7
```

**Hint:** Subtract served from count.

**Difficulty:** Easy

### Question 5: Traffic Light

**Problem description:** A light starts green. Each command next changes green to yellow to red to green. Print final light.

**Input format:** n, then n commands all next.

**Output format:** Final light.

**Example input:**

```text
4
next next next next
```

**Example output:**

```text
yellow
```

**Hint:** Keep the current state.

**Difficulty:** Medium

### Question 6: Board Game

**Problem description:** Read starting square and dice rolls. Print final square.

**Input format:** Start, n, then n rolls.

**Output format:** Final square.

**Example input:**

```text
0
4
3 2 6 1
```

**Example output:**

```text
12
```

**Hint:** Add each roll.

**Difficulty:** Medium

### Question 7: Shop Stock

**Problem description:** Read starting stock and events buy/sell amount. buy adds, sell subtracts. Print final stock.

**Input format:** Stock, n, then event amount lines.

**Output format:** Final stock.

**Example input:**

```text
10
2
sell 3
buy 5
```

**Example output:**

```text
12
```

**Hint:** Parse each event.

**Difficulty:** Medium

### Question 8: Battery Drain

**Problem description:** Read battery and actions. game drains 10, charge adds 15 but battery cannot go above 100. Print final battery.

**Input format:** Battery, n, then actions.

**Output format:** Battery.

**Example input:**

```text
90
2
charge game
```

**Example output:**

```text
90
```

**Hint:** Use min(100, battery + 15).

**Difficulty:** Hard

### Question 9: Elevator Ride

**Problem description:** Read starting floor and commands up/down. Print final floor, never below 0.

**Input format:** Start, n, commands.

**Output format:** Final floor.

**Example input:**

```text
1
4
down down up up
```

**Example output:**

```text
2
```

**Hint:** Use max(0, floor - 1).

**Difficulty:** Hard

### Question 10: Growing Plant

**Problem description:** Read days. Plant starts height 1. Each day it doubles, but if height is over 20 it grows only 3. Print final height.

**Input format:** One integer days.

**Output format:** Final height.

**Example input:**

```text
6
```

**Example output:**

```text
35
```

**Hint:** Simulate day by day.

**Difficulty:** Hard
