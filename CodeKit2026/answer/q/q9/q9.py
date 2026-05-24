n = int(input())
temps = list(map(int, input().split()))
print("ALERT" if any(t > 8 for t in temps) else "SAFE")
