import random
import math

random.seed(1)

maxLoad = 2000


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


def point_occupied(points_to_check, x, y):
    for point in points_to_check:
        if point.x == x and point.y == y:
            return True
    return False


def generate_points(number_of_points):
    generated_points = []
    for i in range(number_of_points):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        pickup = random.randint(0, 2) == 2
        how_much = random.randint(100, 200)
        while point_occupied(generated_points, x, y):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
        new_point = Point()
        new_point.id = i + 1
        new_point.x = x
        new_point.y = y
        new_point.how_much = how_much
        new_point.pickup = pickup
        new_point.done = False
        generated_points.append(new_point)
    return generated_points


def get_pickup_points(generated_points):
    found_pickup_points = []
    for point in generated_points:
        if point.pickup:
            found_pickup_points.append(point)
    return found_pickup_points


def get_dropdown_points(generated_points):
    found_dropdown_points = []
    for point in generated_points:
        if not point.pickup:
            found_dropdown_points.append(point)
    return found_dropdown_points


def update_points(generated_points, found_pickup_points, found_dropdown_points):
    for point in generated_points:
        if point.done:
            for pickup_point in found_pickup_points:
                if pickup_point.id == point.id:
                    pickup_point.done = True
            for dropdown_point in found_dropdown_points:
                if dropdown_point.id == point.id:
                    dropdown_point.done = True
    for pickup_point in found_pickup_points:
        if pickup_point.done:
            for point in generated_points:
                if pickup_point.id == point.id:
                    point.done = True
    for dropdown_point in dropdown_points:
        if dropdown_point.done:
            for point in generated_points:
                if dropdown_point.id == point.id:
                    point.done = True


def generate_warehouses(number_of_warehouses, generated_points):
    generated_warehouses = []
    for i in range(number_of_warehouses):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        while point_occupied(generated_points, x, y) or point_occupied(generated_warehouses, x, y):
            x = random.randint(0, 100)
            y = random.randint(0, 100)
        new_warehouse = Warehouse()
        new_warehouse.id = i + 101
        new_warehouse.x = x
        new_warehouse.y = y
        generated_warehouses.append(new_warehouse)
    return generated_warehouses


def get_distance(x1, y1, x2, y2):
    return math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def is_any_point_undone(generated_points):
    for point in generated_points:
        if not point.done:
            return True
    return False


def find_first_undone_point(generated_points):
    for point in generated_points:
        if not point.done:
            return point
    return None


def find_nearest_undone_point(generated_points, x, y):
    if is_any_point_undone(generated_points):
        nearest_point_found = find_first_undone_point(generated_points)
        for point in generated_points:
            if get_distance(point.x, point.y, x, y) != 0 and get_distance(point.x, point.y, x, y) \
                    < get_distance(nearest_point_found.x, nearest_point_found.y, x, y) and not point.done:
                nearest_point_found = point
        return nearest_point_found
    return None


def find_nearest_warehouse(generated_warehouses, x, y):
    nearest_found_warehouse = generated_warehouses[0]
    for warehouse in generated_warehouses:
        if get_distance(warehouse.x, warehouse.y, x, y) < \
                get_distance(nearest_found_warehouse.x, nearest_found_warehouse.y, x, y):
            nearest_found_warehouse = warehouse
    return nearest_found_warehouse


def can_go_to_point(point_to_go, temp_balance):
    if point_to_go.pickup and point_to_go.how_much + temp_balance <= maxLoad:
        return True
    if not point_to_go.pickup and temp_balance - point_to_go.how_much >= 0:
        return True
    return False


if __name__ == '__main__':
    points = generate_points(100)
    pickup_points = get_pickup_points(points)
    dropdown_points = get_dropdown_points(points)
    warehouses = generate_warehouses(5, points)
    start_warehouse = warehouses[random.randint(0, 5)]
    actual_x = start_warehouse.x
    actual_y = start_warehouse.y
    route = []
    start_amount = 0
    balance = 0
    while True:
        nearest_point = find_nearest_undone_point(points, actual_x, actual_y)
        temp_delivery_amount = nearest_point.how_much
        if nearest_point.pickup:
            temp_delivery_amount = -temp_delivery_amount
        if start_amount + temp_delivery_amount <= maxLoad and \
                (balance - temp_delivery_amount >= 0 or
                 start_amount - (balance - temp_delivery_amount) <= maxLoad) and \
                balance - temp_delivery_amount <= maxLoad:
            potential_balance = start_amount
            if temp_delivery_amount > 0:
                potential_balance = start_amount + temp_delivery_amount
            for point in route:
                if point.pickup:
                    potential_balance += point.how_much
                else:
                    potential_balance -= point.how_much
            if potential_balance < 0 or potential_balance > maxLoad:
                break
            for point in points:
                if point.id == nearest_point.id:
                    point.done = True
                    break
            actual_x = nearest_point.x
            actual_y = nearest_point.y
            route.append(nearest_point)
            if temp_delivery_amount > 0:
                start_amount += temp_delivery_amount
            balance = start_amount
            for point in route:
                if point.pickup:
                    balance += point.how_much
                else:
                    balance -= point.how_much
        else:
            break
    balance = start_amount
    for point in route:
        actual_x = point.x
        actual_y = point.y
        if point.pickup:
            balance += point.how_much
        else:
            balance -= point.how_much
    while is_any_point_undone(points):
        temp_nearest_point = find_nearest_undone_point(points, actual_x, actual_y)
        if can_go_to_point(temp_nearest_point, balance):
            for point in points:
                if temp_nearest_point.id == point.id:
                    point.done = True
            route.append(temp_nearest_point)
            actual_x = temp_nearest_point.x
            actual_y = temp_nearest_point.y
            if temp_nearest_point.pickup:
                balance += temp_nearest_point.how_much
            else:
                balance -= temp_nearest_point.how_much
        else:
            if temp_nearest_point.pickup:
                temp_nearest_dropdown_point = find_nearest_undone_point(dropdown_points, actual_x, actual_y)
                if temp_nearest_dropdown_point is None:
                    temp_nearest_warehouse = find_nearest_warehouse(warehouses, actual_x, actual_y)
                    temp_nearest_warehouse_point = Point()
                    temp_nearest_warehouse_point.id = temp_nearest_warehouse.id
                    temp_nearest_warehouse_point.x = temp_nearest_warehouse.x
                    temp_nearest_warehouse_point.y = temp_nearest_warehouse.y
                    temp_nearest_warehouse_point.pickup = False
                    temp_nearest_warehouse_point.how_much = balance
                    route.append(temp_nearest_warehouse_point)
                    actual_x = temp_nearest_warehouse_point.x
                    actual_y = temp_nearest_warehouse_point.y
                    balance = 0
                else:
                    route.append(temp_nearest_dropdown_point)
                    actual_x = temp_nearest_dropdown_point.x
                    actual_y = temp_nearest_dropdown_point.y
                    balance -= temp_nearest_dropdown_point.how_much
                    for point in points:
                        if point.id == temp_nearest_dropdown_point.id:
                            point.done = True
            else:
                temp_nearest_warehouse = find_nearest_warehouse(warehouses, actual_x, actual_y)
                temp_nearest_pickup_point = find_nearest_undone_point(pickup_points, actual_x, actual_y)
                if temp_nearest_pickup_point is None:
                    temp_nearest_warehouse_point = Point()
                    temp_nearest_warehouse_point.id = temp_nearest_warehouse.id
                    temp_nearest_warehouse_point.x = temp_nearest_warehouse.x
                    temp_nearest_warehouse_point.y = temp_nearest_warehouse.y
                    temp_nearest_warehouse_point.pickup = True
                    temp_nearest_warehouse_point.how_much = maxLoad - balance
                    route.append(temp_nearest_warehouse_point)
                    actual_x = temp_nearest_warehouse_point.x
                    actual_y = temp_nearest_warehouse_point.y
                    balance = maxLoad
                else:
                    if get_distance(temp_nearest_pickup_point.x, temp_nearest_pickup_point.y, actual_x, actual_y) <= \
                            get_distance(temp_nearest_warehouse.x, temp_nearest_warehouse.y, actual_x, actual_y):
                        route.append(temp_nearest_pickup_point)
                        actual_x = temp_nearest_pickup_point.x
                        actual_y = temp_nearest_pickup_point.y
                        balance += temp_nearest_pickup_point.how_much
                        for point in points:
                            if point.id == temp_nearest_pickup_point.id:
                                point.done = True
                    else:
                        temp_dropdown_line = []
                        temp_balance = balance
                        temp_x = temp_nearest_warehouse.x
                        temp_y = temp_nearest_warehouse.y
                        while True:
                            temp_temp_nearest_dropdown_point = \
                                find_nearest_undone_point(dropdown_points, temp_x, temp_y)
                            if temp_temp_nearest_dropdown_point is None:
                                break
                            else:
                                if temp_balance + temp_temp_nearest_dropdown_point.how_much <= maxLoad:
                                    temp_balance += temp_temp_nearest_dropdown_point.how_much
                                    temp_x = temp_temp_nearest_dropdown_point.x
                                    temp_y = temp_temp_nearest_dropdown_point.y
                                    temp_dropdown_line.append(temp_temp_nearest_dropdown_point)
                                    for dropdown_point in dropdown_points:
                                        if temp_temp_nearest_dropdown_point.id == dropdown_point.id:
                                            dropdown_point.done = True
                                else:
                                    break
                        temp_nearest_warehouse_point = Point()
                        temp_nearest_warehouse_point.id = temp_nearest_warehouse.id
                        temp_nearest_warehouse_point.x = temp_nearest_warehouse.x
                        temp_nearest_warehouse_point.y = temp_nearest_warehouse.y
                        temp_nearest_warehouse_point.pickup = True
                        temp_nearest_warehouse_point.how_much = temp_balance - balance
                        route.append(temp_nearest_warehouse_point)
                        balance = temp_balance
                        for temp_dropdown_point in temp_dropdown_line:
                            route.append(temp_dropdown_point)
                            balance -= temp_dropdown_point.how_much
                            actual_x = temp_dropdown_point.x
                            actual_y = temp_dropdown_point.y
        update_points(points, pickup_points, dropdown_points)
    temp_start_warehouse_point = Point()
    temp_start_warehouse_point.id = start_warehouse.id
    temp_start_warehouse_point.x = start_warehouse.x
    temp_start_warehouse_point.y = start_warehouse.y
    temp_start_warehouse_point.pickup = False
    temp_start_warehouse_point.how_much = balance
    i = 1
    balance = start_amount
    total_route = 0
    temp_x = start_warehouse.x
    temp_y = start_warehouse.y
    for point in route:
        total_route += get_distance(temp_x, temp_y, point.x, point.y)
        temp_x = point.x
        temp_y = point.y
    file = open("generated_route.txt", "w")
    file.write("Total route length: " + "{:.2f}".format(total_route) + ".\n")
    for point in route:
        temp_amount = -point.how_much
        if point.pickup:
            temp_amount = point.how_much
        additional_space = " "
        if i < 100:
            additional_space += " "
        if i < 10:
            additional_space += " "
        file.write(str(i) + "." + additional_space + "Point ID: " + str(point.id) + ".\n")
        if point.id > 100:
            file.write("     This point is a warehouse.\n")
        if point.pickup:
            file.write("     Amount to pick up:   " + str(point.how_much) + ".\n")
            file.write("     Amount before point: " + str(balance) + ".\n")
            balance += point.how_much
            file.write("     Amount after point:  " + str(balance) + ".\n")
        else:
            file.write("     Amount to drop down: " + str(point.how_much) + ".\n")
            file.write("     Amount before point: " + str(balance) + ".\n")
            balance -= point.how_much
            file.write("     Amount after point:  " + str(balance) + ".\n")
        i += 1
    file.close()
