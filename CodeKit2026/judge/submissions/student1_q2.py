s = input("Enter a string of brackets: ")

def valid(s):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for ch in s:
        if ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()

    return len(stack) == 0

if valid(s) == True:
    print("Valid")
else:
    print("Not Valid")