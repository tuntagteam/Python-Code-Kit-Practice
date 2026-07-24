first_line = input().split()
machine = int(first_line[0])
robotAmout = int(first_line[1])

machineTimes = []

for i in range(machine):
    time = int(input())
    machineTimes.append(time)

minute = 1

while True:
    totalRobot = 0

    for t in machineTimes:
        totalRobot += minute // t

    if totalRobot >= robotAmout:
        print(minute)
        break

    minute += 1