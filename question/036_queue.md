# Queue

## Goal

Practice first-in, first-out problems using a queue.

## What students should know first

* Know lists or deque.
* Know first-in, first-out order.
* Know loops.

## Questions

### Question 1: Lunch Line

**Problem description:** Read commands join name and serve. Print served names.

**Input format:** n, then n commands.

**Output format:** Served names.

**Example input:**

```text
4
join Ana
join Ben
serve
serve
```

**Example output:**

```text
Ana
Ben
```

**Hint:** First joined is first served.

**Difficulty:** Easy

### Question 2: Ticket Counter

**Problem description:** Read people names in a line and print them in service order.

**Input format:** One line names.

**Output format:** Names one per line.

**Example input:**

```text
Mia Leo Zoe
```

**Example output:**

```text
Mia
Leo
Zoe
```

**Hint:** A queue keeps order.

**Difficulty:** Easy

### Question 3: Bus Stops

**Problem description:** Read starting passengers and stop changes. Print final passengers.

**Input format:** Start, n, then in out lines.

**Output format:** Final count.

**Example input:**

```text
5
2
3 1
0 2
```

**Example output:**

```text
5
```

**Hint:** Update in order.

**Difficulty:** Easy

### Question 4: Hot Potato

**Problem description:** Read names and k. Repeatedly move front to back k-1 times, then remove one. Print winner.

**Input format:** Names line, then k.

**Output format:** Winner.

**Example input:**

```text
A B C
2
```

**Example output:**

```text
C
```

**Hint:** Use a queue rotation.

**Difficulty:** Medium

### Question 5: Printer Queue

**Problem description:** Read print jobs and pages. Print job names in order with total pages so far.

**Input format:** n, then name pages.

**Output format:** Job and running pages.

**Example input:**

```text
2
art 3
code 5
```

**Example output:**

```text
art 3
code 8
```

**Hint:** Serve from front.

**Difficulty:** Medium

### Question 6: Recent Messages

**Problem description:** Read messages and keep only the latest 3. Print them oldest to newest.

**Input format:** n, then n messages.

**Output format:** Last three messages.

**Example input:**

```text
5
a
b
c
d
e
```

**Example output:**

```text
c
d
e
```

**Hint:** Pop from front when size is over 3.

**Difficulty:** Medium

### Question 7: Round Robin Chores

**Problem description:** Read names and chore count. Give chores one by one to front child, then move child to back. Print assignments.

**Input format:** Names line, then chore count.

**Output format:** Assigned names.

**Example input:**

```text
Ana Ben
5
```

**Example output:**

```text
Ana
Ben
Ana
Ben
Ana
```

**Hint:** Rotate after each assignment.

**Difficulty:** Medium

### Question 8: First Non-Repeating Stream

**Problem description:** Read letters one by one. After each letter, print the first letter seen once, or #.

**Input format:** One string.

**Output format:** One result per character.

**Example input:**

```text
aabc
```

**Example output:**

```text
a
#
b
b
```

**Hint:** Use counts plus a queue.

**Difficulty:** Hard

### Question 9: Maze Queue Step

**Problem description:** Read a line of positions and start index. Move right one step at a time until end. Print visited indexes.

**Input format:** n and start index.

**Output format:** Visited indexes.

**Example input:**

```text
5 2
```

**Example output:**

```text
2 3 4
```

**Hint:** Queue stores next positions.

**Difficulty:** Hard

### Question 10: Customer Patience

**Problem description:** Read arrivals and service time. One worker serves in queue order. Print finish time for each customer.

**Input format:** n, then arrival service lines.

**Output format:** Finish times.

**Example input:**

```text
3
0 3
1 2
5 1
```

**Example output:**

```text
3
5
6
```

**Hint:** Each customer starts when worker is free.

**Difficulty:** Hard

