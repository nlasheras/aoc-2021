class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __add__(self, o):
        return Point(self.x + o.x, self.y + o.y, self.z + o.z)
    def __sub__(self, o):
        return Point(self.x - o.x, self.y - o.y, self.z - o.z)

    def length_squared(self):
        return self.x*self.x + self.y*self.y + self.z*self.z
