def text_to_binary(text: str) -> str:
    # แปลงแต่ละตัวอักษรเป็นเลขฐานสอง 8 บิต
    return ' '.join(format(ord(c), '08b') for c in text)

def binary_to_text(bstr: str) -> str:
    # แปกแต่ละ “คำ” (8 บิต) แล้วแปลงกลับเป็นตัวอักษร
    try:
        return ''.join(chr(int(b, 2)) for b in bstr.split())
    except ValueError:
        return "<Invalid binary input>"

# —— เริ่มโพรแกรม ——
print("Choose conversion:")
print("1) Text → Binary")
print("2) Binary → Text")
choice = input("Enter 1 or 2: ").strip()

if choice == '1':
    txt = input("Enter text: ")
    print("Binary:")
    print(text_to_binary(txt))

elif choice == '2':
    b = input("Enter binary (space-separated 8-bit blocks): ")
    print("Text:")
    print(binary_to_text(b))

else:
    print("Invalid choice. Please run again and enter 1 or 2.")