class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(self.name, "says Woof!")


dog = Dog("Buddy", 3)
dog.bark()
