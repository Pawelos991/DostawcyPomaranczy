import random
import math
import numpy as np
import matplotlib.pyplot as plt

# random.seed(1)

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
    return [point for point in generated_points if point.pickup]


def get_dropdown_points(generated_points):
    return [point for point in generated_points if not point.pickup]


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


def get_scalar(x1, y1, x2, y2, x3, y3):
    return ((x2 - x1) * (y3 - y1)) - ((x3 - x1) * (y2 - y1))


def is_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    s1 = get_scalar(x1, y1, x3, y3, x2, y2)
    s2 = get_scalar(x1, y1, x4, y4, x2, y2)
    s3 = get_scalar(x3, y3, x1, y1, x4, y4)
    s4 = get_scalar(x3, y3, x2, y2, x4, y4)
    if ((s1 > 0 > s2) or (s1 < 0 < s2)) and ((s3 > 0 > s4) or (s3 < 0 < s4)):
        return True
    else:
        return False


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


def can_go_to_point(point_to_go, temp_balance_par):
    if point_to_go.pickup and point_to_go.how_much + temp_balance_par <= maxLoad:
        return True
    if not point_to_go.pickup and temp_balance_par - point_to_go.how_much >= 0:
        return True
    return False


def get_route_length(route_points):
    temp_x = route_points[0].x
    temp_y = route_points[0].y
    route_length = 0
    for temp_point in route_points:
        route_length += get_distance(temp_x, temp_y, temp_point.x, temp_point.y)
        temp_x = temp_point.x
        temp_y = temp_point.y
    return route_length


def get_total_route_length(start_warehouse_point, generated_route):
    sub_routes = []
    start_warehouse_point_temp = Point()
    start_warehouse_point_temp.x = start_warehouse_point.x
    start_warehouse_point_temp.y = start_warehouse_point.y
    start_warehouse_point_temp.id = start_warehouse_point.id
    temp_sub_route = [start_warehouse_point_temp]
    for temp_point in generated_route:
        temp_sub_route.append(temp_point)
        if temp_point.id > 100:
            sub_routes.append(temp_sub_route)
            temp_sub_route = [temp_point]
    sub_routes_crosses = []
    for temp_route in sub_routes:
        crosses = 0
        for temp_point in temp_route:
            for i in range(temp_route.index(temp_point) + 1):
                if i >= 3:
                    p1 = temp_route[i]
                    p2 = temp_route[i - 1]
                    for j in range(i - 2):
                        p3 = temp_route[j]
                        p4 = temp_route[j + 1]
                        if is_intersection(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y, p4.x, p4.y):
                            crosses += 1
        sub_routes_crosses.append(crosses)
    temp_total_route_length = 0
    for sub_route in sub_routes:
        temp_length = get_route_length(sub_route)
        if sub_routes_crosses[sub_routes.index(sub_route)] == np.min(sub_routes_crosses) \
                and random.randint(0, 99) <= 4:
            temp_length = temp_length * 1.1
        temp_total_route_length += temp_length
    return temp_total_route_length


def add_arrow(line, position=None, direction='right', size=15, color=None):
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate('', xytext=(xdata[start_ind], ydata[start_ind]), xy=(xdata[end_ind], ydata[end_ind]), \
                       arrowprops=dict(arrowstyle="->", color=color), size=size)

def route_contains_point(temp_warehouse, temp_route):
    contains = False
    for temp_point in temp_route:
        if temp_point.x == temp_warehouse.x and temp_point.y == temp_warehouse.y:
            contains = True
    return contains

if __name__ == '__main__':
    points = generate_points(100)
    pickup_points = get_pickup_points(points)
    dropdown_points = get_dropdown_points(points)
    warehouses = generate_warehouses(5, points)
    start_warehouse = warehouses[random.randint(0, 4)]
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
    temp_nearest_warehouse = find_nearest_warehouse(warehouses, actual_x, actual_y)
    temp_nearest_warehouse_point = Point()
    temp_nearest_warehouse_point.id = temp_nearest_warehouse.id
    temp_nearest_warehouse_point.x = temp_nearest_warehouse.x
    temp_nearest_warehouse_point.y = temp_nearest_warehouse.y
    temp_nearest_warehouse_point.pickup = False
    temp_nearest_warehouse_point.how_much = balance
    route.append(temp_nearest_warehouse_point)
    i = 1
    balance = 0
    temp_start_warehouse_point = Point()
    temp_start_warehouse_point.id = start_warehouse.id
    temp_start_warehouse_point.x = start_warehouse.x
    temp_start_warehouse_point.y = start_warehouse.y
    temp_start_warehouse_point.pickup = True
    temp_start_warehouse_point.how_much = start_amount
    route.insert(0, temp_start_warehouse_point)
    total_route_length = get_total_route_length(start_warehouse, route)
    file = open("generated_route.txt", "w")
    file.write("Total route length: " + "{:.2f}".format(total_route_length) + ".\n")
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
    file = open("route.csv", "w")
    file.write("x,y\n")
    for point in route:
        file.write(str(point.x) + "," + str(point.y) + "\n")
    file.close()
    f, ax = plt.subplots(1)
    for i in range(1, route.__len__()):
        xvals = [route[i - 1].x, route[i].x]
        yvals = [route[i - 1].y, route[i].y]
        line = ax.plot(xvals, yvals, color='black')[0]
        add_arrow(line)
    for warehouse in warehouses:
        if not route_contains_point(warehouse, route):
            plt.plot(warehouse.x, warehouse.y, marker="o", markeredgecolor="blue", markerfacecolor="blue")
    for point in route:
        temp_color = "green"
        if route.index(point) == route.__len__() - 1:
            temp_color = "red"
        elif route.index(point) == 0:
            temp_color = "yellow"
        elif point.id > 100:
            temp_color = "blue"
        plt.plot(point.x, point.y, marker="o", markeredgecolor=temp_color, markerfacecolor=temp_color)
    plt.savefig('route.png', dpi=800)
