import numpy as np
from config import FOCAL_LENGTH


def project_point(x,y,z,canvas_size):
    if z == 0:
        z = 0.01
    fov = canvas_size[0]/FOCAL_LENGTH # canvas_size[0]/canvas_size[1]
    projected_x = (x * fov / z) + canvas_size[0] / 2
    projected_y = (y * fov / z) + canvas_size[1] / 2
    return [projected_x,projected_y]
def get_polygons_for_cube(x,y,z,canvas_size):
    return np.array([
        [ # right face
            project_point(x + 0.5 , y + 0.5, z + 0.5/FOCAL_LENGTH,canvas_size),
            project_point(x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH,canvas_size),
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH,canvas_size),
            project_point(x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH,canvas_size)
        ],
        [ # front face
            project_point(x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [ # left face
            project_point(x - 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [ # bottom face
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [  # top face
            project_point(x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ]
    ],np.int32)
def get_polygons_for_slab(x,y,z,canvas_size):
    return np.array([
        [  # right face
            project_point(x + 0.5, y, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [  # front face
            project_point(x + 0.5, y, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5,y, z - 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [  # left face
            project_point(x - 0.5,y, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5,y, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [  # bottom face
            project_point(x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH, canvas_size)
        ],
        [  # top face
            project_point(x + 0.5,y, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5,y, z - 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x - 0.5,y, z + 0.5/FOCAL_LENGTH, canvas_size),
            project_point(x + 0.5,y, z + 0.5/FOCAL_LENGTH, canvas_size)
        ]
    ], np.int32)
def get_polygon_bounds(pts):
    most_left_pixel = 10000
    most_right_pixel = 0
    most_top_pixel = 100000
    most_bottom_pixel = 0
    for point_set in pts:
        for point in point_set:
            if point[0] < most_left_pixel:
                most_left_pixel = point[0]
            elif point[0] > most_right_pixel:
                most_right_pixel = point[0]
            if point[1] < most_top_pixel:
                most_top_pixel = point[1]
            elif point[1] > most_bottom_pixel:
                most_bottom_pixel = point[1]
    return most_left_pixel,most_right_pixel,most_top_pixel,most_bottom_pixel