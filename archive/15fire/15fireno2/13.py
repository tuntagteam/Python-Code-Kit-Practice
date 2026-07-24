cipher = "PB QDPH LV FKDZDGRO VXZDQVDQLW"
shift = 3
result = ''
for c in cipher:
    if c.isalpha():
        start = ord('a') if c.islower() else ord('A')
        result += chr((ord(c) - start - shift) % 26 + start)
    else:
        result += c
print("Decoded text:", result)