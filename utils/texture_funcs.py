import cv2
import numpy as np

# add the functions that load the texture files

def get_blocks_data(image=None, ignore_color = None):
    block_colors = {}
    block_textures = {}
    block_textures_80 = {}
    with open('block_colors.txt', 'r') as f:
        for line in f:
            line = line.strip()
            '''if not ("glass" in line or "blue" in line or "black" in line or "white" in line or "grey" in line or "gray" in line):
                continue'''
            '''if not ("dirt"  in line or "grass" in line or "cobble" in line):
                continue'''
            block_colors["minecraft:" + line.split("@")[0]] = (
                int(line.split("@")[1].split(",")[0]),
                int(line.split("@")[1].split(",")[1]),
                int(line.split("@")[1].split(",")[2]),
            )
            texture = cv2.imread(line.split("@")[2].strip())
            block_textures["minecraft:" + line.split("@")[0]] = texture
            darker = np.clip(texture.astype(np.float32) * 0.8, 0, 255).astype(np.uint8)
            block_textures_80["minecraft:" + line.split("@")[0]] = darker
    # sort keys for faster block choosing
    '''change this to turn on block choosing'''
    if 2**4==16:
        return block_colors, block_textures, block_textures_80
    if np.any(image):
        resized = cv2.resize(image,(100,100))
        # get best palett for that image
        blocks_in_palett = []
        shape = resized.shape
        for x in range(shape[0]):
            for y in range(shape[1]):
                top_for_pixel = []
                keys = list(block_colors.keys())
                best = keys[0]
                goal_pixel = resized[x,y]
                if np.any(goal_pixel == ignore_color):
                    continue
                best_score = score_similarity(np.array([[goal_pixel]]), np.array([[block_colors[keys[0]]]]))
                for b in range(1,len(keys)):
                    if keys[b] in top_for_pixel:
                        continue
                    score = score_similarity(np.array([[goal_pixel]]), np.array([[block_colors[keys[b]]]]))

                    if score < best_score and score < 100883:
                        best = keys[b]
                        best_score = score
                top_for_pixel.insert(0,best)
                for i in range(0,min(10,len(top_for_pixel))):
                    if not top_for_pixel[i] in blocks_in_palett:
                        blocks_in_palett.insert(0,top_for_pixel[i])
        filtered_block_colors = {}
        filtered_block_textures = {}
        filtered_block_textures_80 = {}
        for key in list(block_colors.keys()):
            if (key in blocks_in_palett and not ("emerald" in key or  "green" in key or "lime" in key or "cyan" in key)) or "glass" in key :
                filtered_block_colors[key] = block_colors[key]
                print(key,block_colors[key])
                filtered_block_textures[key] = block_textures[key]
                filtered_block_textures_80[key] = block_textures_80[key]
        return filtered_block_colors, filtered_block_textures, filtered_block_textures_80