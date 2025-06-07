import tkinter as tk
import pandas as pd
import random
from datetime import datetime

# คำตอบแบบสุ่ม
responses = {
    "love": ["💘 ความรักจะมาหาเร็ว ๆ นี้!", "💔 ตอนนี้ไม่ใช่เวลาแห่งรัก..."],
    "money": ["💸 เงินจะมาแบบไม่คาดฝัน!", "🪙 เก็บเหรียญที่พื้นไว้ดี ๆ"],
    "school": ["📚 ตั้งใจเรียนแล้วสิ่งดี ๆ จะตามมา", "💤 ห้ามหลับในห้องนะ!"],
    "magic": ["🪄 พลังเวทอยู่ในใจของเธอ", "🧙‍♂️ ต้องฝึกฝนทุกวันจึงจะเก่ง!"],
    "default": ["🤖 ข้าไม่เข้าใจ... ลองถามใหม่อีกทีสิ", "🌀 คำถามนี้ลึกลับเกินไป..."]
}

# สร้าง DataFrame เก็บ log
chat_log_df = pd.DataFrame(columns=["Time", "User", "Bot"])

# หาคำตอบ
def get_response(msg):
    for key in responses:
        if key in msg:
            return random.choice(responses[key])
    return random.choice(responses["default"])

# ฟังก์ชันเมื่อผู้ใช้กดปุ่ม
def ask_bot():
    global chat_log_df
    msg = user_input.get().strip()
    if not msg:
        return
    response = get_response(msg.lower())

    # แสดงผลบนจอ
    chat_log.insert(tk.END, f"👦 คุณ: {msg}")
    chat_log.insert(tk.END, f"🤖 บอท: {response}")
    user_input.delete(0, tk.END)

    # บันทึกลง DataFrame
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[now, msg, response]], columns=chat_log_df.columns)
    chat_log_df = pd.concat([chat_log_df, new_row], ignore_index=True)

# export CSV ได้ถ้าต้องการ
def export_chat():
    chat_log_df.to_csv("chat_history.csv", index=False)
    chat_log.insert(tk.END, "💾 บันทึกบทสนทนาไว้ใน chat_history.csv แล้ว")

# สร้าง UI
root = tk.Tk()
root.title("🤖 Magic ChatBot AI (with pandas log)")
root.geometry("600x750")
root.config(bg="#1b1429")

font_k = ("Kanit", 14)
font_title = ("Kanit", 22, "bold")

tk.Label(root, text="🧙‍♂️ Magic ChatBot", font=font_title, fg="gold", bg="#1b1429").pack(pady=20)

chat_log = tk.Listbox(root, width=60, height=20, font=("Kanit", 12), bg="#fff8f0")
chat_log.pack(pady=10)

user_input = tk.Entry(root, font=font_k, width=40, justify="center")
user_input.pack(pady=10)

tk.Button(root, text="💬 ถาม", font=font_k, bg="#a29bfe", fg="black", command=ask_bot).pack(pady=10)
tk.Button(root, text="💾 บันทึกบทสนทนา", font=font_k, bg="#55efc4", fg="black", command=export_chat).pack(pady=5)

root.mainloop()