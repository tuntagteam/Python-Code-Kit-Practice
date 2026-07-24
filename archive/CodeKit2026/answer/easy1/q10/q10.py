password = input().strip()
has_letter = any(c.isalpha() for c in password)
has_digit = any(c.isdigit() for c in password)
print("STRONG" if has_letter and has_digit else "WEAK")
