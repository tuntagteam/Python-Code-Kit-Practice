tasks = []

def show_tasks():
    if not tasks:
        print("\nNo tasks yet.\n")
        return

    print("\nTo-Do List:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "⬜"
        print(f"{i}. {status} {task['title']}")
    print()


def add():
    title = input("Enter task title: ").strip()

    if title == "":
        print("Task title cannot be empty.\n")
        return

    task = {
        "title": title,
        "done": False
    }

    tasks.append(task)
    print("Task added.\n")


def mark_done():
    show_tasks()
    if not tasks:
        return

    try:
        index = int(input("Enter task number to mark done: ")) - 1
        if 0 <= index < len(tasks):
            tasks[index]["done"] = True
            print("Task marked as done.\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")


def delete_task():
    show_tasks()
    if not tasks:
        return

    try:
        index = int(input("Enter task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            deleted = tasks.pop(index)
            print(f"Deleted: {deleted['title']}\n")
        else:
            print("Invalid task number.\n")
    except ValueError:
        print("Please enter a valid number.\n")


def main():
    while True:
        print("=== TO-DO LIST ===")
        print("1. Show tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Exit")

        choice = input("Choose an option: ").strip()
        print()

        if choice == "1":
            show_tasks()
        elif choice == "2":
            add()
        elif choice == "3":
            mark_done()
        elif choice == "4":
            delete_task()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")


main()