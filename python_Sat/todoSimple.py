
import sys

task = []

def add(text):
    task.append(text)

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
    while True:
        a = input("Enter Task Name : ")
        if a == "Delete":
            which = int(input("Enter task number : "))
            deleteTask(which)
        elif a == "Edit":
            which = int(input("Enter task number : "))
            edit(which)
        elif a == "Exit":
            exit()
        else:
            add(a)
        showTask()





            
if __name__ == "__main__":
    __main__()