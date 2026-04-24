from collections import deque

n = int(input())

queue = deque()
answers = []

for _ in range(n):
    command = input().split()

    if command[0] == "ADD":
        queue.append(command[1])

    elif command[0] == "SEND":
        if queue:
            queue.popleft()

    elif command[0] == "CHECK":
        if queue:
            answers.append(queue[0])
        else:
            answers.append("EMPTY")

for ans in answers:
    print(ans)