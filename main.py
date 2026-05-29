import cv2, numpy as np
from config import CANVAS_SIZE, GOAL_IMAGE_PATH
from utils.placement_funcs import get_overlayed_region
from utils.comparison_funcs import score_similarity

# temporary imports for testing:
import sys
rng = np.random.default_rng()
test_texture = cv2.imread("C:\\Users\\colin\\Downloads\\patrickdumb.jpg")

canvas = rng.integers(0,255,(CANVAS_SIZE[1], CANVAS_SIZE[0],3), dtype=np.uint8)
goal = cv2.imread(GOAL_IMAGE_PATH)
goal = cv2.resize(goal, CANVAS_SIZE)
cv2.imshow("g",goal)
for z in range(200,30,-1):
    for x in range(-40, 40, 5):
        for y in range(-40, 40, 5):
            results = get_overlayed_region(canvas, (x, y, z), test_texture, 0)
            if not results:
                continue
            bounds, new_region = results

            goal_region = goal[bounds[2]:bounds[3], bounds[0]:bounds[1]]
            canvas_region = canvas[bounds[2]:bounds[3], bounds[0]:bounds[1]]

            old_score = score_similarity(goal_region, canvas_region)
            new_score = score_similarity(goal_region, new_region)
            if new_score < old_score:
                #print("placed at " + str(x) + ", " + str(y))
                canvas[bounds[2]:bounds[3], bounds[0]:bounds[1]] = new_region

        cv2.imshow("c", canvas)
    cv2.waitKey(1)
cv2.waitKey(0)

