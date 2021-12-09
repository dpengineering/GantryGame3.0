from cv2 import cv2
import numpy as np


"""
How it works:
spirals out, finds all the pixels one away
if there are not two it deletes the original pixel
then it takes the ajacent pixels, and makes sure that there are more pixels outside that are not the other pixels it found
checks to see if the ones one away have another one one away
"""
'''
Key:
white: unprocessed edge
2: one away
4: 
'''


def denoise_edges(input_img):
    input_img = input_img.deepcopy() #todo not using .copy might be impacting performance
    img = input_img.deepcopy()
    mask = cv2.inRange(img, (0,0,0), (255,255,255))
    img[mask>0] = (255,255,255)

    for x in range(len(img)):
        for y in range(len(img[0])):
            if input_img[x][y] == 255:
                fun_zone = input_img.deepcopy()
                fun_zone[x][y] = 10
                potential_points = check_close(x,y)
                if len(potential_points) >= 2:
                    for point in potential_points:
                        print(point)





def spiral_out(x,y, spiral_radius):
    for j in range(1,spiral_radius+1):
        for i in range(x-j,x+j+1):
            yield (i,y+j)
            yield (i,y-j)
        for i in range(y-j+1, y+j):
            yield (x+j,i)
            yield (x-j,i)

def check_close(xP,yP):

    # for y in range(yP-20,yP+20):
    #     for x in range(xP-20, xP+20):
    #         if (x,y) == (xP, yP):
    #             continue
    #         if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
    #             if edges[y][x] == 255:
    #                 return(x,y)

    for x,y in spiral_out(xP,yP, 50):
        if 0 <= x < edges.shape[1] and 0 <= y < edges.shape[0]:
            if edges[y][x] == 255:
                    return(x,y)


