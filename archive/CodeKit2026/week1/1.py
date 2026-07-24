n = int(input())
parcels = []

for _ in range(n):
    name, priority, distance, deadline = input().split()

    priority = int(priority)
    distance = int(distance)
    deadline = int(deadline)

    parcels.append([name, priority, distance, deadline])

def sort_key(item):
    return (item[1], item[3], item[2], item[0])

parcels.sort(key=sort_key)

for item in parcels:
    print(item[0])