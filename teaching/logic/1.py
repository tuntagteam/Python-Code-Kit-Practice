import tkinter as tk
import random

# ดวงหลากหลายแบบ
fortunes = [
    "🌈 พลังงานสดใสล้อมรอบตัวคุณ",
    "⚠️ ระวังการตัดสินใจที่เร่งรีบ",
    "💖 ความรักจะนำทางสิ่งดี ๆ มา",
    "🎉 วันนี้เหมาะกับการเริ่มต้นใหม่",
    "🧠 ความคิดของคุณคืออาวุธลับ",
    "💸 เงินจะมาแบบไม่คาดฝัน!",
    "🌪️ ความเปลี่ยนแปลงกำลังจะมา",
    "🛡️ คุณปลอดภัยในพลังแห่งเวท",
    "🔮 ทุกอย่างที่เกิด มีเหตุผลของมัน"
]

# ฟังก์ชันทำนาย
def tell_fortune():
    name = name_entry.get().strip()
    if not name:
        result_var.set("😅 ใส่ชื่อก่อนสิจ๊ะ!")
    else:
        fortune = random.choice(fortunes)
        result_var.set(f"{name} 🪄: {fortune}")
        log.insert(tk.END, f"✨ {name}: {fortune}")

# สร้างหน้าต่างหลัก
root = tk.Tk()
root.title("🧙‍♂️ Magic Fortune AI")
root.geometry("600x700")
root.config(bg="#1a103d")

font_k = ("Kanit", 16)
font_title = ("Kanit", 24, "bold")
font_fancy = ("Kanit", 18, "bold")

# หัวเรื่อง
tk.Label(root, text="🔮 Magic Fortune AI", font=font_title, fg="#ffd700", bg="#1a103d").pack(pady=25)

# กล่องป้อนชื่อ
tk.Label(root, text="Enter your name first", font=font_title, fg="#ffd700", bg="#1a103d").pack(pady=25)
name_entry = tk.Entry(root, font=font_k, width=25, justify="center", bg="#f2e9ff", fg="#2a003f")
name_entry.pack(pady=15)

# ปุ่มทำนาย
def on_enter(e): e.widget.config(bg="#ffb347")
def on_leave(e): e.widget.config(bg="#ff8c42")

btn = tk.Button(root, text="✨ ดูดวงตอนนี้!", font=font_fancy, bg="#ff8c42", fg="black", padx=20, pady=10, command=tell_fortune, relief=tk.RAISED)
btn.pack(pady=15)
btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

# กล่องผลลัพธ์
frame_result = tk.Frame(root, bg="#2e1f4f", bd=4, relief=tk.RIDGE)
frame_result.pack(pady=25, padx=20, fill="x")
result_var = tk.StringVar()
result_label = tk.Label(frame_result, textvariable=result_var, font=("Kanit", 20), fg="#ffffff", bg="#2e1f4f", wraplength=500, justify="center", pady=20)
result_label.pack()

# ประวัติ
tk.Label(root, text="📜 ประวัติการทำนาย", font=font_k, fg="white", bg="#1a103d").pack()
log = tk.Listbox(root, width=60, height=10, font=("Kanit", 12), bg="#fff0e1", fg="#4b2e83", bd=2)
log.pack(pady=10)

# เปิดใช้งาน
root.mainloop()