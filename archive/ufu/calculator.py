import tkinter as tk

# สร้างหน้าต่างโปรแกรม
window = tk.Tk()
window.title("Calculator")
window.geometry("300x300")


# ฟังก์ชันเมื่อกดปุ่มตัวเลข
def click(num):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(num))


# ฟังก์ชันล้างค่า
def clear():
    entry.delete(0, tk.END)


# ฟังก์ชันคำนวณ
def calculate():
    expression = entry.get()
    result = eval(expression)

    entry.delete(0, tk.END)
    entry.insert(0, result)


# ช่องแสดงผล
entry = tk.Entry(window, font=("Arial", 20))
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


# ปุ่มตัวเลข
num = 1
for j in range(1, 4):
    for i in range(3):
        btn = tk.Button(window, text=str(num), width=5, height=2, command=lambda x=num: click(x))
        btn.grid(row=j , column = i)
        num += 1


# ปุ่ม +
btn_plus = tk.Button(window, text="+", width=5, height=2,command=lambda: click("+"))
btn_plus.grid(row=5, column=0)

btn_minus = tk.Button(window, text="-", width=5, height=2,command=lambda: click("-"))
btn_minus.grid(row=5, column=1)

btn_multiply = tk.Button(window, text="*", width=5, height=2,command=lambda: click("*"))
btn_multiply.grid(row=5, column=2)

btn_divide = tk.Button(window, text="/", width=5, height=2,command=lambda: click("/"))
btn_divide.grid(row=5, column=3)


# ปุ่ม =
btn_equal = tk.Button(window, text="=", width=5, height=2,
                      command=calculate)
btn_equal.grid(row=5, column=1)


# ปุ่ม Clear
btn_clear = tk.Button(window, text="Clear", width=5, height=2,
                      command=clear)
btn_clear.grid(row=4, column=2)


window.mainloop()