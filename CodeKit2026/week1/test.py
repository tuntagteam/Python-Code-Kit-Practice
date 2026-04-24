times = int(input())

students = []

for _ in range(times):
    action = input()
    if "IN" in action.upper():
        students.append(action.replace("IN ", ""))
    elif "OUT" in action.upper() and (action.replace("OUT ", "") in students):
        students.remove(action.replace("OUT ", ""))

print(len(students))