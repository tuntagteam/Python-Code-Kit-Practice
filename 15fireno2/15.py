s = ".O.##."

kitchen_index = s.index('O')
customer_indices = [i for i, c in enumerate(s) if c == '#']

leftmost = min(customer_indices)
rightmost = max(customer_indices)

time_go_left_first = abs(kitchen_index - leftmost) + (rightmost - leftmost)
time_go_right_first = abs(kitchen_index - rightmost) + (rightmost - leftmost)

print(min(time_go_left_first, time_go_right_first))