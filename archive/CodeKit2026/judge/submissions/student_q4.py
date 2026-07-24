done = []
q = []
for i in range(int(input())):
   data = input().split()
   if data[0] == "JOIN":
      data[1] = int(data[1])
      q.append(data[1])
   else:
      if not q:
         pass
      elif q:
         done.append(q[0])
         q.pop(0)
print(*done)