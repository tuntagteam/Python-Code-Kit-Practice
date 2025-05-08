import math

a, b = map(int, input().split())
# หาค่า GCD ด้วยฟังก์ชัน math.gcd
gcd = math.gcd(a, b)
# LCM = ผลคูณหารด้วย GCD
lcm = a * b // gcd
print(f"GCD = {gcd}")
print(f"LCM = {lcm}")