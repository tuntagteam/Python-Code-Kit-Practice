def merge_intervals(intervals):
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            last[1] = max(last[1], current[1])
        else:
            merged.append(current)

    return merged

n = int(input("กรุณาใส่จำนวน intervals: "))
intervals = []
for _ in range(n):
    start, end = map(int, input("ใส่ Start End: ").split())
    intervals.append([start, end])

result = merge_intervals(intervals)

for interval in result:
    print(interval[0], interval[1])