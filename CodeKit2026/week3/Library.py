L, R = map(int, input().split())

def odd_sum_to(x):
    count = (x + 1) // 2
    return count * count

print(odd_sum_to(R) - odd_sum_to(L - 1))