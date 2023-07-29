import cv2
import numpy as np

img0 = cv2.imread('./test_images/maze_3.png')
red = (0,0,255)

maze_img = img0[94:694+12, 94:694+12]

cv2.line(img0,(0,94),(900,94),red,1)    #horizontal line
cv2.line(img0,(0,694+12),(900,694+12),red,1)    #horizontal line
cv2.line(img0,(94,0),(94,900),red,1)    #vertical line
cv2.line(img0,(694+12,0),(694+12,900),red,1) #vertical line

cv2.imshow('cropped image',maze_img)
cv2.waitKey(0)

horiz=['A','B','C','D','E','F','G']
traffic_signals=[]
start_node=''

for col in range(7):
    for r in range(7):
        #print(maze_img[r*100+2, col*100+2] )
        if all(maze_img[r*100+2, col*100+2] == [0,0,255]):
            #print('here')
            traffic_signals.append( horiz[col] + str(r+1) )
        elif all(maze_img[r*100+2, col*100+2] == [0,255,0]):
            start_node = horiz[col] + str(r+1)

print(traffic_signals, start_node)