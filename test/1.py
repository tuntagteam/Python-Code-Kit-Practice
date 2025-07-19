def list_sum(*nums):
    total = 0
    for num in nums:
        total += num
    return total

def wordlenght(words):
    return len(words)

def evenorodd(num):
    if num % 2 == 0:
        return "even"
    else:
        return "odd"

def list2string(*words):
    result = ""
    for word in words:
        result += word
    return result


def findlargest(*numbers):
    max = -999
    for i in numbers:
        if i > max:
            max = i
    return max

def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("fizzbuzz")
        elif i % 3 == 0:
            print("fizz")
        elif i % 5 == 0:
            print("buzz")
        else:
            print(i)

def countVowel(str):
    vowel = ["a" , "e" , "i" , "o" ,"u"]
    count = 0
    for i in str:
        if i in vowel:
            count += 1
    return count

    return str

def reverseString(str):
    reversed_string = str[::-1]
    return reversed_string

def positiveOnly(nums):
    pos = []
    for i in nums:
        if i > 0:
            pos.append(i)
    return pos

def greet(name):
    return "Hello" + name


print(list_sum(2, 4, 6)) 
print(wordlenght("elephant"))
print(evenorodd(4))
print(list2string("Hello" , "World"))
print(findlargest(2,4,5,6,7,8,9,1))
print(fizzbuzz(10))
print(reverseString("olleH"))
print(positiveOnly([10,-10,20,-20]))
print(greet("Tag"))
print(countVowel("Helloooooiiiii"))