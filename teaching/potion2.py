import tkinter as tk
from tkinter import messagebox

class Ingredient:
    def __init__(self, name, effect, power):
        self.name = name
        self.effect = effect
        self.power = power

    def describe(self):
        return f"{self.name} {self.effect} {self.power}"

# Spark , Explode , Color-Change , Poison , Fire , Meow
class Potion:
    def __init__(self):
        self.ingredients = []


    def add(self, ingredient):
        self.ingredients.append(ingredient)

    def mix(self):
        total_power = sum(ing.power for ing in self.ingredients)
        effects = {ing.effect for ing in self.ingredients}

        if "explode" in effects and total_power > 15:
            result = "BOOM! You're dead"
        elif "spark" in effects and "color-change" in effects:
            result = "You become Rainbow"
        elif "meow" in effects and total_power < 5:
            result = "You are a cute little cat"
        elif "poison" in effects and "spark" in effects:
            result = "Spark Poisoned. You're dead like a sparkle"
        elif "fire" in effects and "explode" in effects and total_power == 15:
            result = "Your house burns down"
        else:
            result = "Nothing happened. You just made the plain water"

        self.ingredients.clear()
        return result 

all_ingredients = [
    Ingredient("Spark Plug", "spark", 2),
    Ingredient("Gun Powder", "explode", 10),
    Ingredient("Nyan Cat", "color-change", 2),
    Ingredient("Acid", "poison", 8),
    Ingredient("Fire Cat", "fire", 5),
    Ingredient("Meow", "meow", 4),
]

potion = Potion()

root = tk.Tk()
root.title("JediPaceFinnPotion Hamburger Cookierun")
root.geometry("550x650")
root.config(bg="#00AF68")

font_title = ("Arial" ,18 , "bold")
font_p = ("Arial", 14)

tk.Label(root,font=font_title , text="JediPaceFinnPotion Hamburger Cookierun", fg="#FF9241", bg="#00AF68" ).pack(pady=15)

frame_ing = tk.LabelFrame(root, text="Ingredients", font=font_p, fg="#FF9241", bg="#00AF68", padx=10, pady=10, bd=3)
frame_ing.pack(pady=10)

def add_ingredient(index):
    ing = all_ingredients[index]
    potion.add(ing)
    log.insert(tk.END, f"Added: {ing.name}")

def on_enter(e): e.widget.config(bg="#d1aaff")
def on_leave(e): e.widget.config(bg="#a46bf5")

for i, ing in enumerate(all_ingredients):
    btn = tk.Button(frame_ing, text=ing.describe(), width=35, bg="#a46bf5", fg="black" ,font=font_p, relief=tk.RAISED, bd=2,
                    command=lambda i=i: add_ingredient(i))
    btn.grid(row=i, column=0, padx=4, pady=6)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

def mix_potion():
    result = potion.mix()
    messagebox.showinfo("Result :" ,result)
    log.insert(tk.END, f"{result}")
    log.insert(tk.END, "-" * 40)

mix_btn = tk.Button(root, text="Mix it all mate!", font=font_p, fg="#FF9241", bg="#00AF68", activebackground="red", padx=20 , pady=8 ,command=mix_potion)
mix_btn.pack(pady=20)

tk.Label(root, text="📜 Log", font=font_p, fg="white", bg="#2e003e").pack()
log = tk.Listbox(root, width=55, height=10, font=("Courier", 11), bg="#fff7e9", bd=2)
log.pack(pady=10)

root.mainloop()