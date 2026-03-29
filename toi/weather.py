water_temp = int(input())
degree = input()

# 0 c 32 << f solid
# 0-100 c 32 - 212 f liquid
# 100 c 212 f >> gas

degree_lower = degree.lower()
if degree == "c":
    if water_temp <= 0:
        print("solid")
    elif water_temp > 1 and water_temp < 100:
        print("luqiud")
    elif water_temp >= 100:
        print("gas") 
elif degree == "f":
    if water_temp <= 32:
        print("solid")
    elif water_temp > 32 and water_temp < 212:
        print("luqiud")
    elif water_temp >= 212:
        print("gas") 

