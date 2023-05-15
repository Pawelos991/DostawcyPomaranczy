class Point:
    id = 0
    x = 0
    y = 0
    pickup = False
    how_much = 100
    done = False


class Warehouse:
    id = 0
    x = 0
    y = 0


class Route:
    def __init__(self, points=[], length=0):
        self.points = points
        self.length = length
