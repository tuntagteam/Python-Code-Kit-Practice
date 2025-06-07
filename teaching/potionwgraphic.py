import tkinter as tk
from tkinter import messagebox


class Ingredient:
    def __init__(self, name, effect, power):
        self.name = name
        self.effect = effect
        self.power = power

    def describe(self):
        return f"🔹 {self.name} ({self.effect}, {self.power})"


class Potion:
    def __init__(self):
        self.ingredients = []

    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def mix(self):
        total_power = sum(ing.power for ing in self.ingredients)
        effects = {ing.effect for ing in self.ingredients}

        if "explode" in effects and total_power > 15:
            result = "💥 BOOM! The potion exploded!"
        elif "spark" in effects and "color-change" in effects:
            result = "🌈 The potion sparkles and changes colors!"
        elif total_power < 5:
            result = "😴 Nothing interesting happens..."
        else:
            result = "✨ The potion bubbles mysteriously..."

        self.ingredients.clear()
        return result


# สร้างส่วนผสม
all_ingredients = [
    Ingredient("Fairy Dust", "spark", 4),
    Ingredient("Dragon Acid", "explode", 10),
    Ingredient("Rainbow Leaf", "color-change", 3),
    Ingredient("Mud", "none", 1),
    Ingredient("Phoenix Feather", "spark", 6),
]

potion = Potion()


# เริ่มต้น GUI
root = tk.Tk()
root.title("🧪 Potion Lab")
root.geometry("550x650")
root.config(bg="#2e003e")

font_k = ("Kanit", 13)
font_title = ("Kanit", 18, "bold")

# ส่วนหัว
tk.Label(root, text="🔮 Magic Potion Lab", font=font_title, fg="gold", bg="#2e003e").pack(pady=15)

# กล่องส่วนผสม
frame_ing = tk.LabelFrame(root, text="🧂 ส่วนผสม", font=font_k, fg="white", bg="#3b1e4e", padx=10, pady=10, bd=3)
frame_ing.pack(pady=10)

def add_ingredient(index):
    ing = all_ingredients[index]
    potion.add(ing)
    log.insert(tk.END, f"➕ Added: {ing.name}")

def on_enter(e): e.widget.config(bg="#d1aaff")
def on_leave(e): e.widget.config(bg="#a46bf5")

for i, ing in enumerate(all_ingredients):
    btn = tk.Button(frame_ing, text=ing.describe(), width=35, bg="#a46bf5", fg="black", font=font_k,
                    relief=tk.RAISED, bd=2,
                    command=lambda i=i: add_ingredient(i))
    btn.grid(row=i, column=0, padx=4, pady=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# ปุ่มผสม
def mix_potion():
    result = potion.mix()
    messagebox.showinfo("ผลลัพธ์", result)
    log.insert(tk.END, f"⚗️ {result}")
    log.insert(tk.END, "-" * 40)

mix_btn = tk.Button(root, text="🧪 ผสมน้ำยา", font=("Kanit", 14, "bold"), bg="#ff6f61", fg="black",
                    activebackground="#ff9478", padx=20, pady=8, command=mix_potion)
mix_btn.pack(pady=20)

# Log
tk.Label(root, text="📜 Log", font=font_k, fg="white", bg="#2e003e").pack()
log = tk.Listbox(root, width=55, height=10, font=("Courier", 11), bg="#fff7e9", bd=2)
log.pack(pady=10)

root.mainloop()