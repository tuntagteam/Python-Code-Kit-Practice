# List Operations

## Goal

Practice adding, removing, changing, and checking items in lists.

## What students should know first

* Know list basics.
* Know indexes.
* Know loops.

## Questions

### Question 1: Add a Toy

**Problem description:** Read a list of toys and one new toy. Add it to the end and print the list.

**Input format:** One line toys, then one toy.

**Output format:** Updated list.

**Example input:**

```text
ball kite
car
```

**Example output:**

```text
ball kite car
```

**Hint:** Use append().

**Difficulty:** Easy

### Question 2: Remove Snack

**Problem description:** Read snacks and a snack to remove. Remove it once and print the list.

**Input format:** One line snacks, then target.

**Output format:** Updated list.

**Example input:**

```text
chips cake juice
cake
```

**Example output:**

```text
chips juice
```

**Hint:** Use remove() when the item exists.

**Difficulty:** Easy

### Question 3: Change First Color

**Problem description:** Read colors and a new color. Replace the first color and print the list.

**Input format:** One line colors, then new color.

**Output format:** Updated list.

**Example input:**

```text
red blue
green
```

**Example output:**

```text
green blue
```

**Hint:** Assign to index 0.

**Difficulty:** Medium

### Question 4: Insert Captain

**Problem description:** Read team names and one captain. Insert captain at the front.

**Input format:** One line names, then captain.

**Output format:** Updated team.

**Example input:**

```text
Mia Leo
Ava
```

**Example output:**

```text
Ava Mia Leo
```

**Hint:** Use insert(0, captain).

**Difficulty:** Medium

### Question 5: Pop Last Card

**Problem description:** Read card names. Remove the last card and print it.

**Input format:** One line cards.

**Output format:** Removed card.

**Example input:**

```text
sun moon star
```

**Example output:**

```text
star
```

**Hint:** pop() removes and returns the last item.

**Difficulty:** Medium

### Question 6: Sort Name List

**Problem description:** Read names and print them in alphabetical order.

**Input format:** One line names.

**Output format:** Sorted names.

**Example input:**

```text
Zoe Ana Ben
```

**Example output:**

```text
Ana Ben Zoe
```

**Hint:** Use sort() or sorted().

**Difficulty:** Medium

### Question 7: Count Same Stickers

**Problem description:** Read stickers and a target sticker. Print how many times it appears.

**Input format:** One line stickers, then target.

**Output format:** Count.

**Example input:**

```text
cat dog cat cat
dog
```

**Example output:**

```text
1
```

**Hint:** Use count() or loop.

**Difficulty:** Medium

### Question 8: Merge Teams

**Problem description:** Read two team lists and print one combined list.

**Input format:** Two lines of names.

**Output format:** Combined names.

**Example input:**

```text
A B
C D
```

**Example output:**

```text
A B C D
```

**Hint:** Use + for lists.

**Difficulty:** Hard

### Question 9: Remove All Mud

**Problem description:** Read item names. Remove every item named mud and print the clean list.

**Input format:** One line items.

**Output format:** Cleaned list.

**Example input:**

```text
mud ball mud kite
```

**Example output:**

```text
ball kite
```

**Hint:** Build a new list without mud.

**Difficulty:** Hard

### Question 10: Rotate Line

**Problem description:** Read a list of names. Move the first name to the end and print the list.

**Input format:** One line names.

**Output format:** Rotated names.

**Example input:**

```text
Ana Ben Cam
```

**Example output:**

```text
Ben Cam Ana
```

**Hint:** pop(0) then append().

**Difficulty:** Hard

