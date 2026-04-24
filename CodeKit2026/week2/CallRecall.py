times = int(input())

sequence = []

lastpatient = ""

for _ in range(times):
    command = input()
    if command.upper()[:4] == "CALL":
        patient = command.replace("CALL ", "")
        sequence.append(patient)
        last_patient = patient
    elif (command.upper() == "RECALL") and (last_patient != ""):
        sequence.append(last_patient)
    elif last_patient == "":
        sequence.append("EMPTY")

print(*sequence)