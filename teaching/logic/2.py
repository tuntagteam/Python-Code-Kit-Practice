import tkinter as tk
import random

responses = {
    "love": ["💘 ความรักจะมาหาเร็ว ๆ นี้!", "💔 ตอนนี้ไม่ใช่เวลาแห่งรัก..."],
    "money": ["💸 เงินจะมาแบบไม่คาดฝัน!", "🪙 เก็บเหรียญที่พื้นไว้ดี ๆ"],
    "school": ["📚 ตั้งใจเรียนแล้วสิ่งดี ๆ จะตามมา", "💤 ห้ามหลับในห้องนะ!"],
    "magic": ["🪄 พลังเวทอยู่ในใจของเธอ", "🧙‍♂️ ต้องฝึกฝนทุกวันจึงจะเก่ง!"],
    "default": ["🤖 ข้าไม่เข้าใจ... ลองถามใหม่อีกทีสิ", "🌀 คำถามนี้ลึกลับเกินไป..."]
}

def ask_bot():
    msg = user_input.get().lower()
    found = False
    for key in responses:
        if key in msg:
            bot_response.set(random.choice(responses[key]))
            found = True
            break
    if not found:
        bot_response.set(random.choice(responses["default"]))
    chat_log.insert(tk.END, f"👦 คุณ: {msg}")
    chat_log.insert(tk.END, f"🤖 บอท: {bot_response.get()}")
    user_input.delete(0, tk.END)

# UI Setup
root = tk.Tk()
root.title("🤖 Magic ChatBot AI")
root.geometry("600x700")
root.config(bg="#1f0f3a")

font_k = ("Kanit", 14)
font_title = ("Kanit", 22, "bold")

tk.Label(root, text="🧙‍♂️ Magic ChatBot", font=font_title, bg="#1f0f3a", fg="gold").pack(pady=20)

# Chat log
chat_log = tk.Listbox(root, width=60, height=20, font=("Kanit", 12), bg="#fff8f0")
chat_log.pack(pady=10)

# ช่องพิมพ์
user_input = tk.Entry(root, font=font_k, width=40, justify="center")
user_input.pack(pady=10)

# ปุ่มถาม
tk.Button(root, text="❓ ถามคำถาม", font=font_k, bg="#8e44ad", fg="black", command=ask_bot).pack(pady=10)

# คำตอบบอท
bot_response = tk.StringVar()
tk.Label(root, textvariable=bot_response, font=("Kanit", 16), bg="#1f0f3a", fg="white", wraplength=500).pack(pady=10)

root.mainloop()