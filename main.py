import cv2, cProfile, numpy as np
from config import CANVAS_SIZE, GOAL_IMAGE_PATH
from utils.placement_funcs import get_overlayed_region
from utils.comparison_funcs import score_similarity

# temporary imports for testing:
import sys
rng = np.random.default_rng()

# the biggest optimization to be made is to store each image as an int32
# the reason is that one of the most expensive functions is score_similarity
# because it has to convert each image to int32. if i just keep the image as
# an int32 all the time i dont have to keep doing this. i'd only have to make
# it a uint8 when im displaying it. however, this comes with challenges that
# i can probably solve, but i dont want to get distracted right now. the main
# challenge being resizing int32 images. id have to make a custom resizing
# function. i think itd use np.reduce

# i think it could be incredibly efficient to cache resized textures since
# their sizes (most likely, but i havent looked to closely into it) come in
# multiples of 3, reducing the needed number of caches significantly. im already
# caching the 16x16+ texture so it wouldnt hurt to have 4-5 more sizes cached,
# especially if they are smaller. however, i need to actually finish this code
# right now.

test_texture = cv2.imread("C:\\Users\\colin\\Downloads\\patrickdumb.jpg")
canvas = rng.integers(0,255,(CANVAS_SIZE[1], CANVAS_SIZE[0],3), dtype=np.uint8)
goal = cv2.imread(GOAL_IMAGE_PATH)
goal = cv2.resize(goal, CANVAS_SIZE)
cv2.imshow("g",goal)
def main():
    for z in range(200, 30, -1):
        for x in range(-40, 40, 1):
            for y in range(-40, 40, 1):
                results = get_overlayed_region(canvas, (x, y, z), test_texture, 0)
                if not results:
                    continue
                bounds, new_region = results

                goal_region = goal[bounds[2]:bounds[3], bounds[0]:bounds[1]]
                canvas_region = canvas[bounds[2]:bounds[3], bounds[0]:bounds[1]]

                old_score = score_similarity(goal_region, canvas_region)
                new_score = score_similarity(goal_region, new_region)
                if new_score < old_score:
                    # print("placed at " + str(x) + ", " + str(y))
                    canvas[bounds[2]:bounds[3], bounds[0]:bounds[1]] = new_region

        cv2.imshow("c", canvas)
        cv2.waitKey(1)
    cv2.waitKey(0)

cProfile.run('main()')