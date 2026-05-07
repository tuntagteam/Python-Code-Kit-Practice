# 6. Competitor Ranking System
# The robot competition has scores for each competitor.
# The judges want to know what the “second highest score” is.
# If scores are the same, they are counted as the same rank.
# Input
# First line: n numbers
# Second line: n scores

# Output
# Second highest score

# Example
# Input
# 6
# 100 80 100 70 60 80

# Output
# 80

# Let's break it down:

# input() gets user input and returns a string, e.g. "1 2 3 4 5"

# input().split() splits that input on whitespaces, e.g. ["1", "2", "3", ...]

# int() converts a string to a integer, e.g. "1" -> 1

# map(fn, sequence) applies the function fn to each element in the sequence, e.g. fn(sequence[0]), fn(sequence[1]), ...

# map(int, input().split()) applies int to each string element in the input, e.g. ["1", "2", "3", ...] -> int("1"), int("2"), ...

# list() turns any iterator/generator to a list, e.g. int("1"), int("2"), ... => [1, 2, 3, ...]

# Example:

# In []:
# list(map(int, input().split()))

# Input:
# 1 2 3 4 5

# Out[]:
# [1, 2, 3, 4, 5]
# Note: this is the same as, which may be easier to read:

# In []:
# [int(n) for n in input().split()]

# Input:
# 1 2 3 4 5

# Out[]:
# [1, 2, 3, 4, 5]

#  A set in Python is a built-in data structure used to store a collection of items.
#  Think of it like a bag of unique marbles—you don't care which one you grab first,
#  but you know you won't have two of the exact same marble.

x=int(input())
y = list(map(int, input().split()))
z = set(y)
rank = sorted(z, reverse=True)

print(rank[1])

# [100, 70, 60, 50]
