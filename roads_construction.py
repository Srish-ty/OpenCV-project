import cv2
import numpy as np

img0 = cv2.imread('./test_images/maze_0.png')
red = (0,0,255)

maze_img = img0[94:694+12, 94:694+12]

cv2.line(img0,(0,94),(900,94),red,1)    #horizontal line
cv2.line(img0,(0,694+12),(900,694+12),red,1)    #horizontal line
cv2.line(img0,(94,0),(94,900),red,1)    #vertical line
cv2.line(img0,(694+12,0),(694+12,900),red,1) #vertical line

horiz=['A','B','C','D','E','F','G']

hori_roads=[]
verti_roads=[]

for col in range(7):
    for r in range(7):
        if r!=6:
            if all(maze_img[100*r+60, 100*col+5 ] == [255,255,255]):
                verti_roads.append( horiz[col]+ str(r+1)+'-'+ horiz[col]+str(r+2) )
                maze_img= cv2.circle(maze_img,(100*col+5, 100*r+60 ),10,(200,0,255),4)
        if col!=6:
            if all(maze_img[100*r+5, 100*col+60] == [255,255,255]):
                hori_roads.append( horiz[col]+str(r+1)+'-'+ horiz[col+1]+str(r+1) )
                maze_img= cv2.circle(maze_img,(100*col+60, 100*r+5),10,(200,200,0),4)

print('Horizonatl_roads_under_constr :', hori_roads)
print('vertiacal_roads_under_constr :', verti_roads)

#cv2.imshow('cropped image',maze_img)
#cv2.waitKey(0)