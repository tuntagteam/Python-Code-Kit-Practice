def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

year = int(input("Enter a year: "))
if is_leap_year(year):
    print(f"Bro {year} is a leap year Heehiww.")
else:
    print(f"Bro {year} is not a leap year Hiyaa.")