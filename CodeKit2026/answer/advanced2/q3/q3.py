def merge_count(arr, temp, left, mid, right):
    i, j, k = left, mid + 1, left
    inv = 0
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            inv += mid - i + 1
            j += 1
        k += 1
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    for i in range(left, right + 1):
        arr[i] = temp[i]
    return inv


def sort_count(arr, temp, left, right):
    if left >= right:
        return 0
    mid = (left + right) // 2
    inv = sort_count(arr, temp, left, mid)
    inv += sort_count(arr, temp, mid + 1, right)
    inv += merge_count(arr, temp, left, mid, right)
    return inv


n = int(input())
arr = list(map(int, input().split()))
temp = [0] * n
print(sort_count(arr, temp, 0, n - 1))
