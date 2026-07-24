# n, p = map(int, input().split())
# times = list(map(int, input().split()))

# target = times[p - 1]

# rank = 1

# for t in times:
#     if t < target:
#         rank += 1

# print(rank)

def bubble_sort(list_given: list):
    lister = list_given
    for _ in lister[:-1]:
        for idx, e in enumerate(lister[:-1]):
            comparator = int(lister[idx + 1])
            comparee = int(lister[idx])
            if comparee > comparator:
                lister[idx + 1] = comparee
                lister[idx] = comparator
    return lister

n, p = map(int, input().split())
times = input().split()
times = bubble_sort(times)

time = times[p]
print(times.index(times[p]))
place = times.index(times[p])
print(place)