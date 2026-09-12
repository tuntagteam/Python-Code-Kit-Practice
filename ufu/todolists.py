import tkinter as tk
from tkinter import messagebox

tasks = []

def refresh():
    listbox.delete(0, tk.END)

    for task in tasks:
        if task["done"]:
            listbox.insert(tk.END, "✅ " + task["title"])
        else:
            listbox.insert(tk.END, "⬜ " + task["title"])
        


def add_task():
    title = entry.get().strip()

    if title == "":
        messagebox.showwarning("เตือน", "กรุณาใส่งาน")
        return

    task = {
        "title": title,
        "done": False
    }

    tasks.append(task)
    entry.delete(0, tk.END)
    refresh()


def done_task():
    if not listbox.curselection():
        return

    index = listbox.curselection()[0]
    tasks[index]["done"] = True
    refresh()


def delete_task():
    if not listbox.curselection():
        return

    index = listbox.curselection()[0]
    tasks.pop(index)
    refresh()


window = tk.Tk()
window.title("To-Do List")
window.geometry("400x400")

entry = tk.Entry(window, font=("Arial", 14))
entry.pack(pady=10)

tk.Button(window, text="เพิ่มงาน", command=add_task).pack()
tk.Button(window, text="ทำเสร็จ", command=done_task).pack()
tk.Button(window, text="ลบ", command=delete_task).pack()

listbox = tk.Listbox(window, font=("Arial", 14))
listbox.pack(pady=20)

window.mainloop()