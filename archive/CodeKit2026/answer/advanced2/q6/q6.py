class SegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)

    def update(self, idx, val, node=1, start=1, end=None):
        if end is None:
            end = self.n
        if start == end:
            self.tree[node] += val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(idx, val, node * 2, start, mid)
        else:
            self.update(idx, val, node * 2 + 1, mid + 1, end)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, left, right, node=1, start=1, end=None):
        if end is None:
            end = self.n
        if right < start or end < left:
            return 0
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        return self.query(left, right, node * 2, start, mid) + self.query(
            left, right, node * 2 + 1, mid + 1, end
        )


n, q = map(int, input().split())
seg = SegTree(n)
for _ in range(q):
    parts = list(map(int, input().split()))
    if parts[0] == 1:
        _, idx, val = parts
        seg.update(idx, val)
    else:
        _, left, right = parts
        print(seg.query(left, right))
