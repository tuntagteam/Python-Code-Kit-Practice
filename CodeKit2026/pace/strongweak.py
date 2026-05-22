password = input().strip()

a = any(ch.isalpha() for ch in password)
d = any(ch.isdigit() for ch in password)

if a and d:
    print("STRONG")
else:
    print("WEAK")