def solve(s):
    kitchen_index = s.index('O')
    customer_indices = [i for i, c in enumerate(s) if c == '#']

    left_customers = [i for i in customer_indices if i < kitchen_index]
    right_customers = [i for i in customer_indices if i > kitchen_index]

    if left_customers and right_customers:
        result = (kitchen_index - min(left_customers)) + (max(right_customers) - kitchen_index)
    elif left_customers:
        result = kitchen_index - min(left_customers)
    else:
        result = max(right_customers) - kitchen_index

    print(result)

s1 = ".O.##."
solve(s1)

s2 = ".#..O.#"
solve(s2)

s3 = "#O....#"
solve(s3)