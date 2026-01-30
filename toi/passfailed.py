max_one = 10
max_two = 40
max_three = 50

one = int(input())
two = int(input())
three = int(input())

one_pass = max_one // 2
two_pass = max_two // 2
three_pass = max_three // 2

if one >= max_one and two > max_two and three > max_three:
    print("exceed limit")
else:
    if one >= one_pass or two >= two_pass or three >= three_pass:
        print("pass")
    else:
        print("failed")