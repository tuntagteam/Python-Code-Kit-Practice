password = input().strip()
has_upper = any(c.isupper() for c in password)
has_digit = any(c.isdigit() for c in password)
print("STRONG" if has_upper and has_digit else "WEAK")
