import cv2, numpy as np
from utils.projection_funcs import *
from config import CANVAS_SIZE

texture_cache = {

}

def get_overlayed_region(canvas,position,texture,block_type = None):
    pts = get_polygons_for_cube(position)
    bounds = get_polygon_bounds(pts)
    base_y = min(bounds[2],bounds[3])
    base_x = min(bounds[0],bounds[1])
    if max(bounds[0],bounds[1]) > CANVAS_SIZE[0]:
        #print("a pixel is too far right")
        return None
    if base_x < 0:
        #print("a pixel is too far left")
        return None
    if max(bounds[2],bounds[3]) > CANVAS_SIZE[1]:
        #print("a pixel is too low")
        return None
    if base_y < 0:
        #print("a pixel is too high")
        return None
    region_pixels = canvas[bounds[2]:bounds[3],bounds[0]:bounds[1]].copy()
    x_higher_bound = pts[1][0][0] - base_x
    x_lower_bound = pts[1][2][0] - base_x
    y_lower_bound = pts[1][1][1] - base_y
    y_higher_bound = pts[1][0][1] - base_y
    size = (x_higher_bound-x_lower_bound,y_higher_bound-y_lower_bound)
    if size[0] < 0 or size[1] < 0:
        #print("X OR Y SIZE LESS THAN 0")
        return None
    if not size in texture_cache.keys():
        texture_cache[size]=cv2.resize(texture,size)
    #print(x_higher_bound,x_lower_bound,y_higher_bound,y_lower_bound)
    region_pixels[y_lower_bound:y_higher_bound,x_lower_bound:x_higher_bound] = temp_texture


    cv2.imshow("test",region_pixels)
    print(len(unique_texture_sizes))
    return bounds, region_pixels