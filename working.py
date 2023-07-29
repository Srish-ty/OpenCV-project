import cv2
import numpy as np

img0 = cv2.imread('./test_images/maze_0.png')
red = (0,0,255)

imgwhole = img0[94:694+12, 94:694+12]

cv2.line(img0,(0,94),(900,94),red,1)
cv2.line(img0,(0,694+12),(900,694+12),red,1)
cv2.line(img0,(94,0),(94,900),red,1)
cv2.line(img0,(694+12,0),(694+12,900),red,1)

medics = imgwhole[12:100,12:-12]

new_list=medics[:,:100]

cv2.imwrite('C:/Users/srush/Documents/openCV/cyborg_task2/small_part.jpg',new_list)
cv2.imwrite('C:/Users/srush/Documents/openCV/cyborg_task2/line_part.jpg',medics)

#cv2.imshow('cropped image',medics)
#cv2.waitKey(0)

mediclist=[]
j=1

def addshape(imgcont,j):
    list_s_names=[]
    img= imgcont
    # converting image into grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # setting threshold of gray image
    _, threshold = cv2.threshold(gray, 227, 255, cv2.THRESH_BINARY)

    # using a findContours() function
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0
    # list for storing names of shapes
    for contour in contours:

        # here we are ignoring first counter because
        # findcontour function detects whole image as shape
        if i == 0:
            i = 1
            continue

        # cv2.approxPloyDP() function to approximate the shape
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        
        # using drawContours() function
        cv2.drawContours(img, [contour], 0, (0, 255, 0), 1)

        # finding center point of shape
        M = cv2.moments(contour)
        #print(M)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        #print(len(approx))	
        # putting shape name at center of each shape
        if len(approx) in [5,11]:
            cv2.putText(img, 'Triangle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
            list_s_names.append(['shop_'+str(j),'triangle',[112*(j-1)+x,y]])

        elif len(approx) in [4,8]:
            cv2.putText(img, 'Quadrilateral', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
            list_s_names.append(['shop_'+str(j),'quadrilateral',[[112*(j-1)+x,y]]])


        else:
            cv2.putText(img, 'circle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
            list_s_names.append(['shop_'+str(j),'circle',[112*(j-1)+x,y]])
    if list_s_names!=[]:
        mediclist.append(list_s_names)
    cv2.imshow('edited image with label',img)
    cv2.waitKey(0)


for i in range(6):
    img_part=  medics[:, 100*i:100*(i+1)-12]
    addshape(img_part,i+1)


#addshape((new_list))
print(mediclist)
cv2.imshow('shapes', new_list)
cv2.waitKey(0)
    
