class Ingredient:
    def __init__(self, name, effect, power):
        self.name = name
        self.effect = effect  # เช่น "spark", "explode", "color-change"
        self.power = power  # ค่าพลังของปฏิกิริยา

    def describe(self):
        return f"{self.name} (Effect: {self.effect}, Power: {self.power})"


class Potion:
    def __init__(self):
        self.ingredients = []

    def add(self, ingredient):
        self.ingredients.append(ingredient)
        print(f"🔹 Added {ingredient.name}")

    def mix(self):
        print("\n🔬 Mixing Potion...")

        total_power = sum(ing.power for ing in self.ingredients)
        effects = {ing.effect for ing in self.ingredients}

        if "explode" in effects and total_power > 15:
            print("💥 BOOM! The potion exploded!")
        elif "spark" in effects and "color-change" in effects:
            print("🌈 The potion sparkles and changes colors!")
        elif total_power < 5:
            print("😴 Nothing interesting happens...")
        else:
            print("✨ The potion bubbles mysteriously...")

        self.ingredients.clear()

# ส่วนผสมต่าง ๆ
dust = Ingredient("Fairy Dust", "spark", 4)
acid = Ingredient("Dragon Acid", "explode", 10)
color_leaf = Ingredient("Rainbow Leaf", "color-change", 3)

# เริ่มสร้าง potion
my_potion = Potion()

# เพิ่มส่วนผสม
my_potion.add(dust)
my_potion.add(color_leaf)
my_potion.add(acid)
my_potion.mix()
