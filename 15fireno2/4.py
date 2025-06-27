numbers = [1, 4, 6, 9]
evens = [x for x in numbers if x % 2 == 0]
if evens:
    print("Average of even numbers:", sum(evens) / len(evens))
else:
    print("No even numbers.")
