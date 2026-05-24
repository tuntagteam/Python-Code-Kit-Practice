class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


n, q = map(int, input().split())
dsu = DSU(n)
for _ in range(q):
    t, u, v = map(int, input().split())
    if t == 1:
        dsu.union(u, v)
    else:
        print("YES" if dsu.find(u) == dsu.find(v) else "NO")
