import numpy as np
from config import FOCAL_LENGTH, CANVAS_SIZE

def project_point(pos : tuple[float,float,float]):
    x,y,z = pos[0],pos[1],pos[2]
    if z == 0:
        z = 0.01
    fov = CANVAS_SIZE[0]/FOCAL_LENGTH # CANVAS_SIZE[0]/CANVAS_SIZE[1]
    projected_x = (x * fov / z) + CANVAS_SIZE[0] / 2
    projected_y = (y * fov / z) + CANVAS_SIZE[1] / 2
    return [projected_x,projected_y] # may 29 i made this into ints
                                                # because it should never return
                                                # float pixel positions.
def get_polygons_for_cube(pos : tuple[int, int, int]):
    x,y,z = pos[0],pos[1],pos[2]
    return np.array([
        [ # right face
            project_point((x + 0.5 , y + 0.5, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [ # front face
            project_point((x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH))
        ],
        [ # left face
            project_point((x - 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [ # bottom face
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [  # top face
            project_point((x + 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y + 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y + 0.5, z + 0.5/FOCAL_LENGTH))
        ]
    ], dtype=np.int32)
def get_polygons_for_slab(pos):
    x,y,z = pos[0],pos[1],pos[2]
    return np.array([
        [  # right face
            project_point((x + 0.5, y, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [  # front face
            project_point((x + 0.5, y, z - 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5,y, z - 0.5/FOCAL_LENGTH))
        ],
        [  # left face
            project_point((x - 0.5,y, z + 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5,y, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [  # bottom face
            project_point((x + 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5, y - 0.5, z + 0.5/FOCAL_LENGTH))
        ],
        [  # top face
            project_point((x + 0.5,y, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5,y, z - 0.5/FOCAL_LENGTH)),
            project_point((x - 0.5,y, z + 0.5/FOCAL_LENGTH)),
            project_point((x + 0.5,y, z + 0.5/FOCAL_LENGTH))
        ]
    ],dtype=np.int32)
def get_polygon_bounds(pts) -> tuple[int,int,int,int]:
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
    return (most_left_pixel,most_right_pixel,most_top_pixel,most_bottom_pixel)
def get_face_bounds(face) -> tuple[int,int,int,int]:
    most_left_pixel = 10000
    most_right_pixel = 0
    most_top_pixel = 100000
    most_bottom_pixel = 0
    for point in face:
        if point[0] < most_left_pixel:
            most_left_pixel = point[0]
        elif point[0] > most_right_pixel:
            most_right_pixel = point[0]
        if point[1] < most_top_pixel:
            most_top_pixel = point[1]
        elif point[1] > most_bottom_pixel:
            most_bottom_pixel = point[1]
    return (most_left_pixel,most_right_pixel,most_top_pixel,most_bottom_pixel)
