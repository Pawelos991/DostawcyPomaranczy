import numpy as np
import matplotlib.pyplot as plt
from route_generator import generate_points, generate_routes, generate_warehouses, plot_route


generator = np.random.default_rng(1)

points = generate_points(generator, 100)
warehouses = generate_warehouses(generator, 5, points)

routes = generate_routes(
    generator,
    points,
    warehouses,
    routes=5,
    write_generated_route_txt=False,
    write_route_csv=False
)

for route in routes:
    plot_route(
        route.points,
        route.length,
        warehouses,
        save_to_png=False
    )
    plt.show()
