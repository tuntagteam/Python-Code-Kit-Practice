n = int(input())

inside = set()

for _ in range(n):
    command = input().split()
    
    action = command[0]
    person_id = int(command[1])
    
    if action == "IN":
        inside.add(person_id)
    elif action == "OUT":
        inside.remove(person_id)

print(len(inside))