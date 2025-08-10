class Fixture:
    def __init__(self, name: str):
        self.name = name


class MovingHead(Fixture):
    def __init__(self, name: str, pan: int, tilt: int, speed: int):
        super().__init__(name)


class ParCan(Fixture):
    def __init__(self, name: str, red: int, green: int, blue: int):
        super().__init__(name)

