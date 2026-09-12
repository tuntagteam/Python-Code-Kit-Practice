import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

root = tk.Tk()
root.title("To Do List")
root.geometry("500x500")

task = []

def add(event=None):
    a = entry.get()
    task.append(a)
    entry.delete(0,tk.END)
    showTask()

def deleteTask():
    selected = listBox.curselection()
    if not selected:
        messagebox.showwarning("เลือก 1 อัน")
        return
    num = selected[0]
    task.pop(num)
    showTask()

def edit():
    selected = listBox.curselection()
    if not selected:
        messagebox.showwarning("เลือก 1 อัน")
        return
    index = selected[0]
    new_task = simpledialog.askstring(
        "Edit Task",
        "Edit the task:",
        initialvalue=task[index]
    )

    if new_task and new_task.strip():
        task[index] = new_task
        showTask()

def showTask():
    listBox.delete(0, tk.END)
    for index, item in enumerate(task):
        listBox.insert(tk.END, f"{index+1}: {item}")

def exit():
    sys.exit("Good Byeeee")

# Title
label = tk.Label(root, text="To Do List App", font=("Arial",30))
label.pack(pady=10)

# Input todolist
entry = tk.Entry(root, width=40, font=("Arial",12))
root.bind("<Return>",add)
entry.pack(pady=5)

# Add button
buttonAdd = tk.Button(root, text="Add Task", width=30, command=add)
buttonAdd.pack(pady=5)

# Task Lists
listBox = tk.Listbox(root, width=40, height=12,font=("Arial",12))
listBox.pack(pady=10)

# Edit Button
buttonEdit = tk.Button(root, text="Edit Task", width=20, command=edit)
buttonEdit.pack(pady=5)

# Delete Button
buttonDelete = tk.Button(root, text="Delete Task", width=20, command=deleteTask)
buttonDelete.pack(pady=5)

root.mainloop()