n = int(input())

productInput = input().split()

productId = []

for x in productInput:
    number = int(x)
    productId.append(number)

duplicateCount = 0
checked = []

for id in productId:
    if id not in checked:
        checked.append(id)
        count = 0
        for otherId in productId:
            if otherId == id:
                count += 1

        if count > 1:
            duplicateCount += 1

print(duplicateCount)