class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def is_pass(self):
        if self.score >= 50:
            return True
        else:
            return False

    def display_info(self):
        print("Name :", self.name)
        print("Score :", self.score)

        if self.is_pass():
            print("Status : Pass")
        else:
            print("Status : Fail")


student = Student("Alice", 78)
student.display_info()
