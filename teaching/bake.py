def bake_bread(flour, yeast, sugar):

    print(f"1. ใส่แป้ง {flour} g")
    print(f"2. ใส่ยีสต์ {yeast} g")
    print(f"3. ใส่น้ำตาล {sugar} g")
    print("4. ผสมส่วนผสมให้เข้ากัน")
    print("5. นวดแป้งให้เนียน")
    print("6. หมักให้แป้งขึ้นเป็นสองเท่า")
    print("7. อบที่อุณหภูมิ 180°C นาน 30 นาที")
    return "🍞 ขนมปังสุกกรอบพร้อมทาน! 🍞"

flour = int(input("flour(g) :"))
yeast = int(input("yeast(g) :"))
sugar = int(input("sugar(g) :"))
bread = bake_bread(flour=flour, yeast=yeast, sugar=sugar)
print("ผลลัพธ์:", bread)