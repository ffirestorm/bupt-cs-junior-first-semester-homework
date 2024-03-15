class Driveable:
    def start_engine(self):
        pass

    def stop_engine(self):
        pass

class Entertainment:
    def play_music(self):
        pass

    def operate_air_conditioner(self):
        pass

class Vehicle:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed

    def description(self):
        return f"This is a {self.name} and its maximum speed is {self.speed} km/h."

    @classmethod
    def create_vehicle(cls, name, speed):
        return cls(name, speed)

    @staticmethod
    def vehicle_type():
        return "Generic Vehicle"

class Car(Vehicle, Driveable, Entertainment):
    def start_engine(self):
        return "Starting the car's engine."

    def stop_engine(self):
        return "Stopping the car's engine."

    def play_music(self):
        return "Playing music in the car."

    def operate_air_conditioner(self):
        return "Operating the air conditioner in the car."

    def description(self):
        return f"This is a {self.name} car and its maximum speed is {self.speed} km/h."

    @staticmethod
    def vehicle_type():
        return "Car"

class Bicycle(Vehicle, Driveable):
    def start_engine(self):
        return "Pedaling the bicycle to start."

    def stop_engine(self):
        return "Stopping pedaling to stop the bicycle."

    def description(self):
        return f"This is a {self.name} bicycle and its maximum speed is {self.speed} km/h."

    @staticmethod
    def vehicle_type():
        return "Bicycle"

if __name__ == '__main__':
    car = Car.create_vehicle("Wenjie", 180)
    bicycle = Bicycle.create_vehicle("Mountain Bike", 30)

    vehicles = [car, bicycle]

    for vehicle in vehicles:
        print(f"{vehicle.description()} - Type: {vehicle.vehicle_type()}")
        if isinstance(vehicle, Driveable):
            print(f"Drive: {vehicle.start_engine()} / {vehicle.stop_engine()}")
        if isinstance(vehicle, Entertainment):
            print(f"Entertainment: {vehicle.play_music()} / {vehicle.operate_air_conditioner()}")