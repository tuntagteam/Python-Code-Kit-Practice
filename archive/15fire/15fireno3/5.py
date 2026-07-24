s = input().strip()
filtered = ''.join(ch.lower() for ch in s if ch.isalnum())
if filtered == filtered[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")