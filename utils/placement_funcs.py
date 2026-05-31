from socket import has_dualstack_ipv6

import cv2, numpy as np
from utils.projection_funcs import *
from config import CANVAS_SIZE

def get_overlayed_region(canvas,position,texture,block_type = None):
    pts = get_polygons_for_cube(position)
    bounds = get_polygon_bounds(pts)
    base_y = min(bounds[2],bounds[3])
    base_x = min(bounds[0],bounds[1])

    if max(bounds[0],bounds[1]) > CANVAS_SIZE[0]:
        return None
    if base_x < 0:
        return None
    if max(bounds[2],bounds[3]) > CANVAS_SIZE[1]:
        return None
    if base_y < 0:
        return None
    region_pixels = canvas[bounds[2]:bounds[3],bounds[0]:bounds[1]].copy()

    x_higher_bound = pts[1][0][0] - base_x
    x_lower_bound = pts[1][2][0] - base_x
    y_lower_bound = pts[1][1][1] - base_y
    y_higher_bound = pts[1][0][1] - base_y
    size = (x_higher_bound-x_lower_bound,y_higher_bound-y_lower_bound)
    if size[0] < 0 or size[1] < 0:
        return None
    # add left/right/top/bottom block face depending on relative position:
    if position[0] < 0: # block is left (draw right face)
        face_bounds = get_face_bounds(pts[0])
        if not (face_bounds[0] == face_bounds[1] or face_bounds[2] == face_bounds[3]):
            cv2.fillPoly(region_pixels, np.array([[[pts[0][0][0] - base_x, pts[0][0][1] - base_y],
                                             [pts[0][1][0] - base_x, pts[0][1][1] - base_y],
                                             [pts[0][2][0] - base_x, pts[0][2][1] - base_y],
                                             [pts[0][3][0] - base_x, pts[0][3][1] - base_y]
                                             ]]), color=(200,0,200))
    elif position[0] > 0:
        face_bounds = get_face_bounds(pts[2])
        if not (face_bounds[0] == face_bounds[1] or face_bounds[2] == face_bounds[3]):
            cv2.fillPoly(region_pixels, np.array([[[pts[2][0][0] - base_x, pts[2][0][1] - base_y],
                                                   [pts[2][1][0] - base_x, pts[2][1][1] - base_y],
                                                   [pts[2][2][0] - base_x, pts[2][2][1] - base_y],
                                                   [pts[2][3][0] - base_x, pts[2][3][1] - base_y]
                                                   ]]), color=(200, 0, 200))
    if position[1] < 0:
        face_bounds = get_face_bounds(pts[4])
        if not (face_bounds[0] == face_bounds[1] or face_bounds[2] == face_bounds[3]):
            cv2.fillPoly(region_pixels, np.array([[[pts[4][0][0] - base_x, pts[4][0][1] - base_y],
                                                   [pts[4][1][0] - base_x, pts[4][1][1] - base_y],
                                                   [pts[4][2][0] - base_x, pts[4][2][1] - base_y],
                                                   [pts[4][3][0] - base_x, pts[4][3][1] - base_y]
                                                   ]]), color=(200, 0, 200))
    elif position[1] > 0:
        face_bounds = get_face_bounds(pts[3])
        if not (face_bounds[0] == face_bounds[1] or face_bounds[2] == face_bounds[3]):
            cv2.fillPoly(region_pixels, np.array([[[pts[3][0][0] - base_x, pts[3][0][1] - base_y],
                                                   [pts[3][1][0] - base_x, pts[3][1][1] - base_y],
                                                   [pts[3][2][0] - base_x, pts[3][2][1] - base_y],
                                                   [pts[3][3][0] - base_x, pts[3][3][1] - base_y]
                                                   ]]), color=(200, 0, 200))
    # add front texture:
    region_pixels[y_lower_bound:y_higher_bound,x_lower_bound:x_higher_bound] = cv2.resize(texture,size)
    return bounds, region_pixels