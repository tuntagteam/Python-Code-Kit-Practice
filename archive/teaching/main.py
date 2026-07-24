number = [1,2,3,4,5,56,6,7,8,8,9,10]

even = list(filter(lambda x: x % 2 != 0, number))

print("Even numbers:", even)

alphabet = [chr(i) for i in range(97, 123)]
print(alphabet)