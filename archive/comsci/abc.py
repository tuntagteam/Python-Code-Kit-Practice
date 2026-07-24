letters = ["A","B","C"]
grid = [["","",""],
        ["","",""],
        ["","",""]]

def saidaimai(grid,r,c,test):
    if test in grid[r]:
        return False
    for i in range(3):
        if grid[i][c] == test:
            return False
    return True

for j in range(5):
    data = input().replace(",","").split()
    n = int(data[0])

    k = 1
    for i in range(n):

        pos = int(data[k])
        test = data[k+1]

        r = (pos-1)//3
        c = (pos-1)%3

        grid[r][c] = test

        k += 2
 
    for r in range(3):
        for c in range(3):
            if grid[r][c] == "":
                for test in letters:
                    if saidaimai(grid,r,c,test):
                        grid[r][c] = test
                        break

    ans = ""
    for r in range(3):
        for c in range(3):
            ans += grid[r][c]

    print(ans)