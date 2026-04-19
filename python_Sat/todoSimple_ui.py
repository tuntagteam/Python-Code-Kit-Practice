import tkinter as tk
from tkinter import messagebox, simpledialog

task = []

def refresh_tasks():
    listbox.delete(0, tk.END)
    for index, item in enumerate(task):
        listbox.insert(tk.END, f"{index + 1}: {item}")

def add():
    text = entry.get()
    if text.strip() == "":
        messagebox.showwarning("Warning", "Please enter a task")
        return
    task.append(text)
    entry.delete(0, tk.END)
    refresh_tasks()

def delete_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete")
        return
    index = selected[0]
    task.pop(index)
    refresh_tasks()

def edit_task():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to edit")
        return
    index = selected[0]
    new_text = simpledialog.askstring(
        "Edit Task",
        "Edit the task:",
        initialvalue=task[index]
    )
    if new_text and new_text.strip():
        task[index] = new_text
        refresh_tasks()

# Main window
root = tk.Tk()
root.title("To Do List")
root.geometry("400x450")

# Title
label = tk.Label(root, text="Welcome to ToDo List", font=("Arial", 16))
label.pack(pady=10)

# Input box
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=5)

# Add button
btn_add = tk.Button(root, text="Add Task", width=20, command=add)
btn_add.pack(pady=5)

# Task list
listbox = tk.Listbox(root, width=40, height=12, font=("Arial", 12))
listbox.pack(pady=10)

# Edit and delete buttons
btn_edit = tk.Button(root, text="Edit Selected Task", width=20, command=edit_task)
btn_edit.pack(pady=5)

btn_delete = tk.Button(root, text="Delete Selected Task", width=20, command=delete_task)
btn_delete.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", width=20, command=root.destroy)
btn_exit.pack(pady=10)

root.mainloop()