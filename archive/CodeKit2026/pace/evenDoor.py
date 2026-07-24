x=int(input())
y=list(map(int, input().split()))
a=0
for i in range(x-1):
    
    if y[i] % 2 == 0:
        a+=1
print(a)

# 6
# 10 20 25 26 27 
# Traceback (most recent call last):
#   File "c:\Users\TagTrueCodingJr\Documents\GitHub\Python-Code-Kit-Practice\CodeKit2026\pace\evenDoor.py", line 6, in <module>
#     if y[i] % 2 == 0:
#        ~^^^
# IndexError: list index out of range