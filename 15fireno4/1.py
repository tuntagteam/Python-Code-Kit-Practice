def is_balanced(s):
    stack = []
    pairs = {'(': ')', '{': '}', '[': ']'}
    for ch in s:
        if ch in pairs:
            stack.append(ch)
        else:
            if not stack:
                return False
            top = stack.pop()
            if pairs[top] != ch:
                return False
    
    return not stack

expr = input("Enter bracket string: ")
print(is_balanced(expr))