import cv2
import numpy as np
from matplotlib import pyplot as plt

# reading image
img = cv2.imread('line_part.jpg')
cv2.imshow('shapes', img)
cv2.waitKey(0)

list_s_names=[]
# converting image into grayscale image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# setting threshold of gray image
_, threshold = cv2.threshold(gray, 227, 255, cv2.THRESH_BINARY)

# using a findContours() function
contours, _ = cv2.findContours(
	threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

i = 0
j=0
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
		list_s_names.append(['triangle',[x,y]])

	elif len(approx) in [4,8]:
		cv2.putText(img, 'Quadrilateral', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
		list_s_names.append(['quadrilateral',[x,y]])


	else:
		cv2.putText(img, 'circle', (x, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,0,0), 1)
		list_s_names.append(['circle',[x,y]])
	j+=1

# displaying the image after drawing contours
cv2.imshow('shapes', img)

cv2.waitKey(0)
print(list_s_names)
cv2.destroyAllWindows()
