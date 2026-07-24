# Graph Basics

## Goal

Practice working with connected places, paths, and friendships.

## What students should know first

* Know lists and dictionaries.
* Know queues or stacks.
* Know loops.

## Questions

### Question 1: Friend Count

**Problem description:** Read friendships and a name. Print how many friends the name has.

**Input format:** m, then m pairs, then target.

**Output format:** Friend count.

**Example input:**

```text
3
A B
A C
B D
A
```

**Example output:**

```text
2
```

**Hint:** Use an adjacency list.

**Difficulty:** Easy

### Question 2: Can Visit Directly

**Problem description:** Read edges and two names. Print yes if there is a direct edge.

**Input format:** m, pairs, then start end.

**Output format:** yes or no.

**Example input:**

```text
2
A B
B C
A B
```

**Example output:**

```text
yes
```

**Hint:** Store neighbors for each node.

**Difficulty:** Easy

### Question 3: BFS Order

**Problem description:** Read a graph and start node. Print BFS visit order.

**Input format:** n m, edges, start.

**Output format:** Visit order.

**Example input:**

```text
4 3
A B
A C
B D
A
```

**Example output:**

```text
A B C D
```

**Hint:** Use a queue.

**Difficulty:** Medium

### Question 4: DFS Order

**Problem description:** Read a graph and start node. Print DFS visit order.

**Input format:** n m, edges, start.

**Output format:** Visit order.

**Example input:**

```text
4 3
A B
A C
B D
A
```

**Example output:**

```text
A B D C
```

**Hint:** Use recursion or stack.

**Difficulty:** Medium

### Question 5: Connected Check

**Problem description:** Read a graph and two nodes. Print yes if a path connects them.

**Input format:** n m, edges, two nodes.

**Output format:** yes or no.

**Example input:**

```text
4 2
A B
C D
A D
```

**Example output:**

```text
no
```

**Hint:** Search from the first node.

**Difficulty:** Medium

### Question 6: Count Components

**Problem description:** Read a graph and print how many connected groups it has.

**Input format:** n m, nodes line, then edges.

**Output format:** Component count.

**Example input:**

```text
4 2
A B C D
A B
C D
```

**Example output:**

```text
2
```

**Hint:** Start a search from every unvisited node.

**Difficulty:** Medium

### Question 7: Shortest Unweighted Path

**Problem description:** Read a graph and two nodes. Print shortest number of edges, or -1.

**Input format:** n m, edges, start end.

**Output format:** Distance.

**Example input:**

```text
4 3
A B
B C
A D
A C
```

**Example output:**

```text
2
```

**Hint:** BFS finds shortest paths in unweighted graphs.

**Difficulty:** Medium

### Question 8: Grid Islands

**Problem description:** Read a grid of 1 and 0. Count groups of connected 1 cells up/down/left/right.

**Input format:** rows cols, grid rows.

**Output format:** Island count.

**Example input:**

```text
3 3
110
010
001
```

**Example output:**

```text
2
```

**Hint:** Use DFS or BFS on grid cells.

**Difficulty:** Hard

### Question 9: Tree Leaves

**Problem description:** Read a tree and root. Print all leaf nodes sorted.

**Input format:** n, edges, root.

**Output format:** Leaf nodes.

**Example input:**

```text
5
A B
A C
B D
B E
A
```

**Example output:**

```text
C D E
```

**Hint:** Leaves have no unvisited children from the root.

**Difficulty:** Hard

### Question 10: Topological Tasks

**Problem description:** Read task rules A before B. Print one valid task order.

**Input format:** n m, tasks, then rules.

**Output format:** Task order.

**Example input:**

```text
3 2
A B C
A B
B C
```

**Example output:**

```text
A B C
```

**Hint:** Use indegrees and a queue.

**Difficulty:** Hard

