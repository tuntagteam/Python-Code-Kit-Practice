# Basic Problem Solving

## Goal

Practice turning small story problems into clear Python steps.

## What students should know first

* Know input and output.
* Know if statements.
* Know loops.

## Questions

### Question 1: Bus Seats

**Problem description:** Read seats and students. Print how many students cannot sit if there are too many, otherwise 0.

**Input format:** Two integers.

**Output format:** Students without seats.

**Example input:**

```text
10
13
```

**Example output:**

```text
3
```

**Hint:** Use max(0, students - seats).

**Difficulty:** Easy

### Question 2: Sticker Packs Needed

**Problem description:** Each pack has 5 stickers. Read needed stickers and print packs needed.

**Input format:** One integer.

**Output format:** Pack count.

**Example input:**

```text
12
```

**Example output:**

```text
3
```

**Hint:** Round up using integer math.

**Difficulty:** Easy

### Question 3: Pocket Money

**Problem description:** Read money and price. Print how many items can be bought.

**Input format:** Two integers.

**Output format:** Item count.

**Example input:**

```text
20
6
```

**Example output:**

```text
3
```

**Hint:** Use integer division.

**Difficulty:** Easy

### Question 4: Class Teams

**Problem description:** Read students and team size. Print full teams and leftover students.

**Input format:** Two integers.

**Output format:** Two numbers.

**Example input:**

```text
23
5
```

**Example output:**

```text
4 3
```

**Hint:** Use // and %.

**Difficulty:** Medium

### Question 5: Robot Distance

**Problem description:** Read forward and backward steps. Print final distance from start.

**Input format:** Two integers.

**Output format:** Absolute distance.

**Example input:**

```text
7
10
```

**Example output:**

```text
3
```

**Hint:** Use abs().

**Difficulty:** Medium

### Question 6: Game Coins

**Problem description:** Read small, medium, big coin counts worth 1, 5, and 10. Print total value.

**Input format:** Three integers.

**Output format:** Total.

**Example input:**

```text
3
2
1
```

**Example output:**

```text
23
```

**Hint:** Multiply each count by its value.

**Difficulty:** Medium

### Question 7: Clock Helper

**Problem description:** Read current hour and hours later. Print the new hour on a 24-hour clock.

**Input format:** Two integers.

**Output format:** New hour.

**Example input:**

```text
22
5
```

**Example output:**

```text
3
```

**Hint:** Use modulo 24.

**Difficulty:** Medium

### Question 8: Library Fine

**Problem description:** Read days late. First 3 days are free, then each day costs 2 coins. Print fine.

**Input format:** One integer.

**Output format:** Fine.

**Example input:**

```text
5
```

**Example output:**

```text
4
```

**Hint:** Only charge days after 3.

**Difficulty:** Hard

### Question 9: Water Bottles

**Problem description:** Read full bottles and exchange rate. Empty bottles can be traded for a new full bottle. Print total drinks.

**Input format:** Two integers.

**Output format:** Total drinks.

**Example input:**

```text
9
3
```

**Example output:**

```text
13
```

**Hint:** Simulate drinking and exchanging.

**Difficulty:** Hard

### Question 10: Best Deal

**Problem description:** Read two offers: price and pieces for each. Print A if offer A is cheaper per piece, otherwise B.

**Input format:** Four numbers.

**Output format:** A or B.

**Example input:**

```text
10
5
12
4
```

**Example output:**

```text
A
```

**Hint:** Compare price1 / pieces1 with price2 / pieces2.

**Difficulty:** Hard

