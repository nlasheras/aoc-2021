class Point:
    """A point in 3D space with x,y,z coordinates"""
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash((self.x, self.y, self.z))
    def __eq__(self, __o: 'Point') -> bool:
        return self.x == __o.x and self.y == __o.y and self.z == __o.z

    def __add__(self, __o):
        return Point(self.x + __o.x, self.y + __o.y, self.z + __o.z)
    def __sub__(self, __o):
        return Point(self.x - __o.x, self.y - __o.y, self.z - __o.z)
    def __iadd__(self, __o):
        self.x += __o.x
        self.y += __o.y
        self.z += __o.z
        return self

    def length_squared(self):
        return self.x*self.x + self.y*self.y + self.z*self.z
    