import numpy as np
import random

def score_similarity(img1: np.ndarray, img2: np.ndarray):
    diff_base = img1.astype(np.int32) - img2.astype(np.int32)
    score = np.sum(diff_base * diff_base, axis=2)
    score = np.mean(score)
    return score
def get_average_pixel_color(pixel1,pixel2):
    return np.array([int((pixel1[0] + pixel2[0])/2),
                     int((pixel1[1] + pixel2[1])/2),
                     int((pixel1[2] + pixel2[2])/2)], np.uint8)
def score_block(goal_pixel, block_name, block_colors):
    if "stained" in block_name:
        avg_color = get_average_pixel_color(goal_pixel, (block_colors[block_name][0],block_colors[block_name][1],block_colors[block_name][2]))
        return score_similarity(goal_pixel, np.array([[avg_color]], np.uint8))
    else:
        return score_similarity(goal_pixel, np.array([[[block_colors[block_name][0],block_colors[block_name][1],block_colors[block_name][2]]]], np.uint8))

# choose_block should maybe not be in here

def choose_block(use_glass : bool, goal_pixels : list, block_colors : dict):
    chosen_block = list(block_colors.keys())[0]
    best_scores = [100000000 for _ in range(len(goal_pixels))]
    for block_name in list(block_colors.keys()):
        # introduce randomness in the block choice:
        if random.randint(0, 5) < 1:
            continue
        if "glass" in block_name and not use_glass:
            continue
        scores = [100000000 for _ in range(len(goal_pixels))]
        for i,goal_pixel in enumerate(goal_pixels):
            scores[i] = score_block(goal_pixels, block_name, block_colors)
        use_block = True
        for i, score in enumerate(scores):
            if scores[i] > best_scores[i]:
                use_block = False
                break
        if use_block:
            chosen_block = block_name
            for i in range(len(best_scores)):
                best_scores[i] = scores[i]
    return chosen_block