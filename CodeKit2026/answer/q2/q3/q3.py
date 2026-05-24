n = int(input())
temps = list(map(int, input().split()))
print("ALERT" if any(t < 0 for t in temps) else "SAFE")
