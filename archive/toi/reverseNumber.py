num = int(input())
if num < 1000 or num > 9999:
    print()
else:        
    flipped_num = int(str(num)[::-1])
    print(flipped_num)