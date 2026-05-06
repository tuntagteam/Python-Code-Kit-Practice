hero = 100
mons=[300, 170, 70, 200, 150]

bigguy = max(mons)

leftoverThing = []

for potato in mons:
    if potato != bigguy:
        leftoverThing.append(potato)

leftoverThing.sort()

bonk = 0

for tinyboi in leftoverThing:
    if hero > bigguy:
        break

    if hero > tinyboi:
        hero = hero + tinyboi
        bonk = bonk + 1
    else:
        break

if hero > bigguy:
    print(bonk + 1)
else:
    print("no")