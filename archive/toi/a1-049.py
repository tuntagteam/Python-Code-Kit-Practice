# floor finding
# firstDigit > 5 = floor 9
# secondDigit > 5 = floor 10
# thirdDigit > 5 = floor 11
# fourthDigit > 5 = floor 12
# fifthDigit > 5 = floor 14
# not match any = floor 13

# room number finding
# if palindrome:
# firstDigit + fifthDigit > 5 = firstDigit Room Number = 1
# secondDigit * fourthDigit > 5 = firstDigit Room Number = 2
# not match any = firstDigit Room Number = 0

# if not palindrome:
# firstDigit // fifthDigit > 5 = firstDigit Room Number = 1
# secondDigit - fifthDigit > 5 = firstDigit Room Number = 2
# not match any = firstDigit Room Number = 0

# second room number finding
# sum of every digit > 25 = secondDigit Room Number = 1
# product of every digit > 55 = secondDigit Room Number = 2
# not match any = secondDigit Room Number = 0

s = input().strip()

d1 = int(s[0])  # firstDigit
d2 = int(s[1])  # secondDigit
d3 = int(s[2])  # thirdDigit
d4 = int(s[3])  # fourthDigit
d5 = int(s[4])  # fifthDigit

if d1 > 5:
    floor = 9
elif d2 > 5:
    floor = 10
elif d3 > 5:
    floor = 11
elif d4 > 5:
    floor = 12
elif d5 > 5:
    floor = 14
else:
    floor = 13

is_palindrome = (s == s[::-1])

if is_palindrome:
    if d1 + d5 > 5:
        room_digit_1 = 1
    elif d2 * d4 > 5:
        room_digit_1 = 2
    else:
        room_digit_1 = 0
else:
    if d5 != 0 and d1 // d5 > 5:
        room_digit_1 = 1
    elif d2 - d5 > 5:
        room_digit_1 = 2
    else:
        room_digit_1 = 0

total_sum = d1 + d2 + d3 + d4 + d5
total_product = d1 * d2 * d3 * d4 * d5

if total_sum > 25:
    room_digit_2 = 1
elif total_product > 55:
    room_digit_2 = 2
else:
    room_digit_2 = 0

answer = str(floor) + str(room_digit_1) + str(room_digit_2)
print(answer)