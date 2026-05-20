# word = input("Enter the words : ")

# word_reverse = word[::-1]

# if word == word_reverse:
#     print("VALID")
# else:
#     print("INVALID")

# Fibonacci
# 0 1 1 2 3 5 8 13 21 ... n

x = int(input())
palin = [0,1]
a = 0

for i in range(x):
    y = palin[-2] + palin[-1]
    palin.append(y)
    

print(palin[x])
