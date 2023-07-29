import cv2
import numpy as np

img0 = cv2.imread('./test_images/maze_0.png')

maze_img_cropped = img0[94:694+12, 94:694+12]  #crop out maze

red = (0,0,255)
cv2.line(img0,(0,94),(900,94),red,1)    #horizontal line
cv2.line(img0,(0,694+12),(900,694+12),red,1)    #horizontal line
cv2.line(img0,(94,0),(94,900),red,1)    #vertical line
cv2.line(img0,(694+12,0),(694+12,900),red,1) #vertical line

medics = maze_img_cropped[12:100,12:-12]  #upper medical blocks list

#new_list=medics[:,:100] #first block

centr_list=[]
#cv2.imwrite('C:/Users/srush/Documents/openCV/cyborg_task2/small_part.jpg',new_list)
#cv2.imwrite('C:/Users/srush/Documents/openCV/cyborg_task2/line_part.jpg',medics)

cv2.imshow('cropped image',maze_img_cropped)
cv2.waitKey(0)

mediclist=[]
j=1

def addshape(imgcont,j):
    list_s_names=[]
    img= imgcont
 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, threshold = cv2.threshold(gray, 227, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    # list for storing names of shapes
    for contour in contours:
        if i == 0:
            i = 1
            continue

        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        cv2.drawContours(img, [contour], 0, (0, 255, 0), 1)

        # finding centeroids
        M = cv2.moments(contour)
        #print(M)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        #print(len(approx))	
        
        if len(approx) in [5,11]:
            shape_nm= 'Triangle'
        elif len(approx) in [4,8]:
            shape_nm= 'Square'
        else:
            shape_nm= 'Circle'

        if all((img[y,x])==[0,255,0]) or all((img[y,x])==[255,255,255]):
            shape_clr = 'Green'
        elif all((img[y,x])==[0,127,255]):
            shape_clr = 'Orange'
        elif all((img[y,x])==[255,255,0]):
            shape_clr = 'Skyblue'
        elif all((img[y,x])==[180,0,255]):
            shape_clr = 'Pink'
        
        centr_list.append((106+100*(j-1)+x, 106+y))
        print(106+100*(j-1)+x, 106+y, shape_clr, img[x,y])
        img =cv2.putText(img, shape_clr , (x-20,y),cv2.FONT_HERSHEY_SIMPLEX, 0.5 ,(255,0,0), 1)  #put coolr name at its centroid
        list_s_names.append(['Shop_'+str(j), shape_clr , shape_nm ,[106+100*(j-1)+x, 106+y]])
        #print(img[x,y], shape_nm, shape_clr)
        cv2.imshow('edited image with label',img)
        cv2.waitKey(0)
    list_s_names.sort(key = lambda x: x[1]) # sorting by color-name
    
    if list_s_names!=[]:
        #print(list_s_names)
        for shop_shapes in list_s_names:
            mediclist.append(shop_shapes)
        

# for evry shop in shops-list
for i in range(6):
    img_part=  medics[:, 100*i:100*(i+1)-12]
    addshape(img_part, i+1)

for ctr in centr_list:
    img0 = cv2.circle(img0,ctr,2,(255,0,0),-1)

cv2.imshow('edited image with label',img0)
cv2.waitKey(0)

cv2.imwrite('C:/Users/srush/Documents/openCV/cyborg_task2/marked_centroids.jpg',img0)

print(mediclist)
    
