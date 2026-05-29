# Logical Operators

## Goal

Practice combining choices with and, or, and not.

## What students should know first

* Know if statements.
* Know comparison operators.
* Know True and False values.

## Questions

### Question 1: Park Day Check

**Problem description:** Read weather and homework. Print go if weather is sunny and homework is done, otherwise stay.

**Input format:** Two words: weather and homework.

**Output format:** go or stay.

**Example input:**

```text
sunny
done
```

**Example output:**

```text
go
```

**Hint:** Use and because both things must be true.

**Difficulty:** Easy

### Question 2: Snack Choice

**Problem description:** Read a snack. Print yes if it is apple or banana.

**Input format:** One word.

**Output format:** yes or no.

**Example input:**

```text
banana
```

**Example output:**

```text
yes
```

**Hint:** Use or for two accepted snacks.

**Difficulty:** Easy

### Question 3: Quiet Mode

**Problem description:** Read a word. Print loud if the word is not quiet.

**Input format:** One word.

**Output format:** loud or quiet.

**Example input:**

```text
music
```

**Example output:**

```text
loud
```

**Hint:** Use not or compare with !=.

**Difficulty:** Easy

### Question 4: Game Login

**Problem description:** Read username and password. Print welcome only if both match kid and python.

**Input format:** Two words.

**Output format:** welcome or denied.

**Example input:**

```text
kid
python
```

**Example output:**

```text
welcome
```

**Hint:** Both comparisons must be true.

**Difficulty:** Medium

### Question 5: Library Pass

**Problem description:** Read age and has_card. Print enter if age is at least 8 or has_card is yes.

**Input format:** One integer and one word.

**Output format:** enter or wait.

**Example input:**

```text
7
yes
```

**Example output:**

```text
enter
```

**Hint:** Either condition can allow entry.

**Difficulty:** Medium

### Question 6: Robot Safety

**Problem description:** Read battery and door. Print start if battery is at least 50 and door is closed.

**Input format:** One integer and one word.

**Output format:** start or stop.

**Example input:**

```text
60
closed
```

**Example output:**

```text
start
```

**Hint:** Use and with a number comparison.

**Difficulty:** Medium

### Question 7: Treasure Rule

**Problem description:** Read coins and key. Print open if coins are at least 10 or key is gold.

**Input format:** One integer and one word.

**Output format:** open or closed.

**Example input:**

```text
4
gold
```

**Example output:**

```text
open
```

**Hint:** One successful condition is enough.

**Difficulty:** Medium

### Question 8: No Rain No Wind

**Problem description:** Read rain and wind as yes or no. Print picnic if both are no.

**Input format:** Two words.

**Output format:** picnic or home.

**Example input:**

```text
no
no
```

**Example output:**

```text
picnic
```

**Hint:** You can use rain == 'no' and wind == 'no'.

**Difficulty:** Medium

### Question 9: Club Member

**Problem description:** Read grade and badge. Print join if grade is 5, 6, or badge is special.

**Input format:** One integer and one word.

**Output format:** join or wait.

**Example input:**

```text
4
special
```

**Example output:**

```text
join
```

**Hint:** Group the grade checks with or.

**Difficulty:** Hard

### Question 10: Smart Door

**Problem description:** Read code, card, and time. Print open if code is 1234 and either card is yes or time is day.

**Input format:** Three lines.

**Output format:** open or locked.

**Example input:**

```text
1234
no
day
```

**Example output:**

```text
open
```

**Hint:** Use parentheses to keep the logic clear.

**Difficulty:** Hard

