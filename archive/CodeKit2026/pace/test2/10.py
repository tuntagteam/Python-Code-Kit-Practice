x=input()

a =sum(1 for c in x if c.isupper())
b =sum(1 for c in x if c.isdigit())

if a > 0 and b > 0:
    print("STRONG")
else:
    print("weak")