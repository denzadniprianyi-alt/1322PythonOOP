
class Human():
    def __init__ (self, name:str):
        pass

class Car:
    def __init__ (self, name, space):
        self.name = name
        self.space = space
        self.passengers = 0

    def add_passenger(self, passenger:Human):

        if  <= self.passengers:
            self.passengers += 1

    def info(self):
        print(f"Name: {self.name}")
        print(f"Space: {self.space}")
        print(f"Passengers: {self.passengers}")

audi = Car("Audi", 5)
audi.info()
audi.add_passenger()
audi.info()