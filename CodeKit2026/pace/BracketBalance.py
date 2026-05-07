# (() INVALID
# ()() VALID
# (()) VALID

x=input()
y=[]
good = True

for i in x:
    if i == "(":
        y.append(i)
    else:
        if len(y) == 0:
            good = False
            break
        
        y.pop()

if len(y) != 0:
    good = False

if good:
    print("VALID")
else:
    print("INVALID")