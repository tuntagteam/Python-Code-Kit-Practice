month = int(input("Enter Month : "))
date = int(input("Enter Date : "))

if month in (1,2,3):
    if date >= 21 & month % 3 == 0:
        print("Spring")
    else:
        print("Winter")
elif month in (4,5,6):
    if date >= 21 & month % 3 == 0:
        print("Summer")
    else:
        print("Spring")
elif month in (7,8,9):
    if date >= 21 & month % 3 == 0:
        print("Fall")
    else:
        print("Summer")
elif month in (10,11,12):
    if date >= 21 & month % 3 == 0:
        print("Winter")
    else:
        print("Fall")