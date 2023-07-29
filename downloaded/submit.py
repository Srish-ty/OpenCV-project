'''
*********************************************************************************
*
*        		===============================================
*           		        CYBORG OPENCV TASK 2
*        		===============================================
*
*
*********************************************************************************
'''

# Author Name:		[niazi]
# Roll No:			[121ID1081]
# Filename:			task_2_niazi.py
# Functions:		detect_arena_parameters
# 		        [ shops_array , show , imgviewer , get_shop , get_shape , get_shop_shape , get_limits_of_color , color_present , centroid , medicine_packages , 
# 		    	traffic_coordinates , get_vertical_track , get_vertical_road_coords , get_vertical_roads 
# 			    get_horizontal_track , get_horizontal_road_coords , get_horizontal_roads ]


####################### IMPORT MODULES #######################
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imutils
import math
from enum import Enum
import itertools
##############################################################
def shops_array(maze_image):
    global shops
    medical_shops = maze_image[100:200, 100:700]
    shops = [ medical_shops[0:100 , 0:100] , medical_shops[0:100 , 100 : 200] , medical_shops[0:100 , 200 : 300] , medical_shops[0:100 , 300 : 400] , medical_shops[0:100 , 400 : 500] , medical_shops[0:100 , 500 : 600] ] 
    return shops

def show(img):
    cv2.imshow('image' , img)
    cv2.waitKey()
    cv2.destroyAllWindows()

def imgviewer(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img ,mode = 'RGB' )
    img.show()
    
def get_shop(maze_no , shop_no):
    shop_no = shop_no - 1
    maze_no = str(maze_no)
    maze_image = cv2.imread('./test_images/maze_' + maze_no + '.png')
    shops = shops_array(maze_image)
    return shops[shop_no]

def get_shape(img):
    img = cv2.resize(img , None , fx = 5 , fy = 5 , interpolation = cv2.INTER_AREA)
    imgGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thrash = cv2.threshold(imgGrey, 240, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    shape_type = [] 
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02* cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [approx], 0, (0, 0, 0), 5)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            shape_type.append('Triangle')
            cv2.putText(img, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        elif len(approx) == 4:
            x1 ,y1, w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if aspectRatio >= 0.95 and aspectRatio <= 1.05:
                shape_type.append('Square')
                cv2.putText(img, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                shape_type.append('Rectangle')
                cv2.putText(img, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        else:
            shape_type.append('Circle')
            cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    return shape_type

def get_shop_shape(maze_no , shop_no):
    img = get_shop(maze_no , shop_no)
    shapes = get_shape(img)
    return shapes[1:]

def get_limits_of_colors(color):
    c = np.uint8([[color]])
    hsvC = cv2.cvtColor(c , cv2.COLOR_BGR2HSV)
    lowerlimit = hsvC[0][0][0] - 10 , 100 , 100
    upperlimit = hsvC[0][0][0] + 10 ,255 , 255
    
    lowerlimit = np.array(lowerlimit , dtype = np.uint8)
    upperlimit = np.array(upperlimit , dtype = np.uint8)
    
    return lowerlimit , upperlimit

def color_present(maze_no , shop_no , color):
    img = get_shop(maze_no , shop_no)
   #img = cv2.resize(img , None , fx = 5 , fy = 5 , interpolation = cv2.INTER_AREA)
    img = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    colors = {'Green' : [0 , 255 , 0] , 'Pink' : [180 , 0 , 255] , 'Orange' : [0,127,255] , 'Sky Blue' : [255 , 255 , 0]}
    color = colors.get(color)
    lowerlimit , upperlimit = get_limits_of_colors(color)
    mask = cv2.inRange(img , lowerlimit , upperlimit)
    mask_image = Image.fromarray(mask)
    if (mask_image.getbbox() is not None):
        x1 , y1 , x2 , y2 = mask_image.getbbox()
        cx , cy = centroid(mask)
        cx = cx + shop_no * 100
        cy = cy + 100
        cx = round(cx, -1)
        cy = round(cy , -1)
        return [x1,y1, x2,y2 , cx , cy] 
    else:
        return False
    
def centroid(mask):
    cnts = cv2.findContours(mask , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    return cx,cy

def medicine_packages(maze_no):
    ans = []
    colors_name = ['Green' , 'Orange' , 'Pink' , 'Sky Blue']
    for shop in range(1,7):
        i = 0
        while i <= 3:
            if(color_present(maze_no,shop,colors_name[i])):
                shape = get_shop_shape(maze_no , shop)
                lst = color_present(maze_no, shop , colors_name[i])
                ans.append(['shop_'+ str(shop) ,colors_name[i], shape[0] ,lst[4], lst[5]])
            i = i + 1
    return ans

def traffic_coordinates(maze_no):
    maze_no = str(maze_no)
    image = cv2.imread('./test_images/maze_' + maze_no + '.png')
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv_image, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_corners = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        if len(approx) == 4:
            red_corners.append(approx)
    ans = []
    col_name = {100 : 'A' , 200 : 'B' , 300 : 'C' , 400 : 'D' , 500 : 'E' , 600 : 'F' , 700 : 'G'}
    for corner in red_corners:
        x_sum = 0
        y_sum = 0
        for point in corner:
            x,y = point[0]
            x_sum = x + x_sum
            y_sum = y + y_sum
        ans.append(col_name.get(int(x_sum / 4)) + str(int(y_sum / 400)))
    ans.sort()
    return ans 

def get_vertical_track(maze_no , track_no):
    maze_no = str(maze_no)
    maze = cv2.imread('./test_images/maze_' + maze_no + '.png')
    grid = cv2.imread('./test_images/full_grid.png')
    y1 = 95 + 100 * (track_no - 1)
    y2 = 105 + 100 * (track_no - 1)
    maze = maze[95:705, y1 : y2]
    grid = grid[95:705, y1 : y2]
    bitwise_xor = cv2.bitwise_xor(maze,grid)
    return bitwise_xor

def get_vertical_road_coords(maze_no , track_no):
    img = get_vertical_track(maze_no , track_no)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    track_name = {1 : 'A' , 2 : 'B' , 3 : 'C' , 4 : 'D' , 5 : 'E' , 6 : 'F' , 7 : 'G'}
    cY_list = []
    roads = []
    mask = np.zeros_like(img)
    for contour in contours:
        cv2.drawContours(mask, [contour], 0, (255, 255, 255), -1)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cX = round(cX , -2)
            cY = round(cY , -2)
            cY = int(cY / 100)
            cY_list.append(cY)
#             print(cX , cY)
    cY_list.sort()
    for item in cY_list:
        ans = track_name.get(track_no) + str(item) + '-' + track_name.get(track_no) + str(item+1)
        roads.append(ans)
    result = cv2.bitwise_and(img, mask)
    if(len(roads) !=0):
        return roads
    else:
        return False

def get_vertical_roads(maze_no):
    all_roads = []
    for track_no in range(1,8):
        if get_vertical_road_coords(maze_no , track_no):
            all_roads.append(get_vertical_road_coords(maze_no , track_no))
    all_roads = list(itertools.chain.from_iterable(all_roads))
    return all_roads

def get_horizontal_track(maze_no , track_no):
    maze_no = str(maze_no)
    maze = cv2.imread('./test_images/maze_' + maze_no + '.png')
    grid = cv2.imread('./test_images/full_grid.png')
    x1 = 95 + 100 * (track_no - 1)
    x2 = 105 + 100 * (track_no - 1)
    maze = maze[x1:x2 , 95 : 705]
    grid = grid[x1:x2, 95 : 705]
    bitwise_xor = cv2.bitwise_xor(maze,grid)
    return bitwise_xor

def get_horizontal_road_coords(maze_no , track_no):
    img = get_horizontal_track(maze_no , track_no)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    track_name = {1 : 'A' , 2 : 'B' , 3 : 'C' , 4 : 'D' , 5 : 'E' , 6 : 'F' , 7 : 'G'}
    cX_list = []
    roads = []
    mask = np.zeros_like(img)
    for contour in contours:
        cv2.drawContours(mask, [contour], 0, (255, 255, 255), -1)
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cX = round(cX , -2)
            cX = int(cX / 100)
            cX_list.append(cX)
#             print(cX , cY)
        cX_list.sort()
        for item in cX_list:
            ans = track_name.get(item) + str(track_no) + '-' + track_name.get(item+1) + str(track_no)
            if ans not in roads:
                roads.append(ans)
    result = cv2.bitwise_and(img, mask)
    roads.sort()
    if(len(roads) !=0):
        return roads
    else:
        return False

def get_horizontal_roads(maze_no):
    all_roads = []
    for track_no in range(1,8):
        if get_horizontal_road_coords(maze_no , track_no):
            all_roads.append(get_horizontal_road_coords(maze_no , track_no))
    all_roads = list(itertools.chain.from_iterable(all_roads))
    all_roads.sort()
    return all_roads
##############################################################


	##################################################


