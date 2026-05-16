# Login System
# x = int(input())
# palin = [0,1]
# a = 0

# for i in range(x):
#     y = palin[-2] + palin[-1]
#     palin.append(y)
    

# print(palin[x])

username = "admin"
password = "1234"

# user inout ฝากแก้หน่อย
id = input("Enter Username :")
pass_word = input("Enter Password :")


# please refactor
if id == username:
    if pass_word == password:
        print("Login Successfully")
    else:
        print("Wrong Password!")
else:
    print("Get Back!")


