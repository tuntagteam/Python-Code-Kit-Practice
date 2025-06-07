# def sum (a , b, c):
#     return a + b + c


# a = int(input("Enter a mate :"))
# b = int(input("Enter a mate :"))
# c = int(input("Enter a mate :"))

# print(sum(a, b, c))

class Student:
    def __init__ (self, name, num):
        self.name = name
        self.num = num
        self.information(name, num)
    def information (self, name , num):
        print("Name :", name)
        print("Num :", num)
    def show(self):
        print(f"เลขที่ {self.num} ชื่อ {self.name}")

class Classroom:
    def __init__ (self):
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)
    
    def show_students(self):
        print("Students in the classroom:")
        for student in self.students:
            student.show()

student1 = Student("Finn", "568")
student2 = Student("Pace", "287")
student3 = Student("Jedi", "1234567890")

classroom = Classroom()
classroom.add_student(student1)
classroom.add_student(student2)
classroom.add_student(student3)

classroom.show_students()

# while True:
#     print("F")