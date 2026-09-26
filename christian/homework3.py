# Create todolists using Def While Lists to store the data
# Functionality
# 1. Add new to do list
# 2. Edit the existing todo list
# 3. List/Show all to do list
# 4. Delete the existing todo list
# 5. Quit the program
# 6. No AI
# 7. Google is allow

import sys

task = []

def add():
    text2 = input("Enter your task : ")
    task.append(text2)

def deleteTask(num):
    task.pop(num)

def edit(num):
    edit = input(f"Edit the task (Current: {task[num]}): ")
    task[num] = edit

def showTask():
    for index, item in enumerate(task):
        print(f"{index+1}: {item}")

def exit():
    sys.exit("Good Byeeee")

def __main__():
    print("================")
    print("Welcome to todolist")
    print("1) Show all tasks")
    print("2) Add new task")
    print("3) Edit task")
    print("4) Delete task")
    print("================")
    print("0) Exit Program")
    print("================")
    a = int(input("Enter your choices : "))
    while True:
        if a == 1:
            showTask()
        elif a == 2:
            add()
        elif a == 3:
            showTask()
            which = int(input("Enter task number : "))
            edit(which-1)
        elif a == 4:
            showTask()
            which = int(input("Enter task number : "))
            deleteTask(which-1)
        elif a == 0:
            exit()
        else:
            print("================")
            print("Please enter valid number")
        print("================")
        print("Welcome to todolist")
        print("1) Show all tasks")
        print("2) Add new task")
        print("3) Edit task")
        print("4) Delete task")
        print("================")
        print("0) Exit Program")
        print("================")
        a = int(input("Enter your choices : "))

            
if __name__ == "__main__":
    __main__()