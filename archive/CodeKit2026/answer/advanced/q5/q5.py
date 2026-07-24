q = int(input())
stack = []
for _ in range(q):
    parts = input().split()
    cmd = parts[0]
    if cmd == "PUSH":
        stack.append(int(parts[1]))
    elif cmd == "POP":
        print("EMPTY" if not stack else stack.pop())
    elif cmd == "TOP":
        print("EMPTY" if not stack else stack[-1])
    elif cmd == "SIZE":
        print(len(stack))
