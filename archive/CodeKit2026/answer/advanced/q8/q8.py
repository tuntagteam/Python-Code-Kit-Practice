s = input().strip()
pairs = {")": "(", "]": "[", "}": "{"}
stack = []
valid = True
for ch in s:
    if ch in "([{":
        stack.append(ch)
    elif ch in ")]}":
        if not stack or stack[-1] != pairs[ch]:
            valid = False
            break
        stack.pop()
print("VALID" if valid and not stack else "INVALID")
