import random


class Point:
    x = 0
    y = 0
    odbior = False
    ile = 100


def point_occupied(points, x, y):
    for point in points:
        if point.x == x and point.y == y:
            return True
    return False


def generate_points(number_of_points):
    points = []
    for i in range(number_of_points):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        odbior = random.randint(0, 2) == 2
        ile = random.randint(100, 200)
        while point_occupied(points, x, y):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
        new_point = Point()
        new_point.x = x
        new_point.y = y
        new_point.ile = ile
        new_point.odbior = odbior
        points.append(new_point)
    file = open("points.csv", "w")
    for point in points:
        file.write(str(point.x) + "," + str(point.y) + "," + str(point.ile) + "," + str(point.odbior) + "\n")
    file.close()


if __name__ == '__main__':
    generate_points(100)

    # Struktura pliku - W kazdym rzedzie 1 punkt
    # Dla kazdego punktu kolejno X, Y, ILE (kg), CZY_ODBIOR (jak false, to dostawa do tego punktu)
