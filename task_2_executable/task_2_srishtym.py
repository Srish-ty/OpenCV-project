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

# Author Name:		srishtym
# Roll No:			122CR0544
# Filename:			task_2_srishtym.py
# Functions:		[detect_arena_parameters, addshape]
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
   ## You are free to make any changes in this section. ##
##############################################################
import cv2
import numpy as np
#img_given =cv2.imread('./test_images/maze_0.png')
##############################################################

def detect_arena_parameters(maze_image):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a dictionary
	containing the details of the different arena parameters in that image

	The arena parameters are of four categories:
	i) traffic_signals : list of nodes having a traffic signal
	ii) horizontal_roads_under_construction : list of missing horizontal links
	iii) vertical_roads_under_construction : list of missing vertical links
	iv) medicine_packages : list containing details of medicine packages
	v)start_node : list containing the start node

	These four categories constitute the four keys of the dictionary

	Input Arguments:
	---
	`maze_image` :	[ numpy array ]
			numpy array of image returned by cv2 library
	Returns:
	---
	`arena_parameters` : { dictionary }
			dictionary containing details of the arena parameters
	
	Example call:
	---
	arena_parameters = detect_arena_parameters(maze_image)
	"""    
	arena_parameters = {'traffic_signals':[], 'start_node':[], 'horizontal_roads_under_construction':[], 'vertical_roads_under_construction':[], 'medicine_packages_present':[]}

	##############	ADD YOUR CODE HERE	##############
	img0= maze_image
	maze_img = img0[94:694+12, 94:694+12]  #crop out maze

	red = (0,0,255)
	cv2.line(img0,(0,94),(900,94),red,1)    #horizontal line
	cv2.line(img0,(0,694+12),(900,694+12),red,1)    #horizontal line
	cv2.line(img0,(94,0),(94,900),red,1)    #vertical line
	cv2.line(img0,(694+12,0),(694+12,900),red,1) #vertical line

	medics = maze_img[12:100,12:-12]  #upper medical blocks list

	#new_list=medics[:,:100] #first block

	#cv2.imshow('cropped image',maze_img)  #see cropped maze
	#cv2.waitKey(0)

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

			if all((img[y,x])==[0,255,0]):
				shape_clr = 'Green'
			elif all((img[y,x])==[0,127,255]):
				shape_clr = 'Orange'
			elif all((img[y,x])==[255,255,0]):
				shape_clr = 'Skyblue'
			elif all((img[y,x])==[180,0,255]):
				shape_clr = 'Pink'
			
			list_s_names.append(['Shop_'+str(j), shape_clr , shape_nm ,[106+100*(j-1)+x, 106+y]])
			#print(img[x,y], shape_nm, shape_clr)
			
		list_s_names.sort(key = lambda x: x[1]) # sorting by color-name
		
		if list_s_names!=[]:
			#print(list_s_names)
			for shop_shapes in list_s_names:
				mediclist.append(shop_shapes)
		#cv2.imshow('edited image with label',img)
		#cv2.waitKey(0)

	# for evry shop in shops-list
	for i in range(6):
		img_part=  medics[:, 100*i:100*(i+1)-12]
		addshape(img_part, i+1)

	arena_parameters['medicine_packages_present'] = mediclist

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

	#print(traffic_signals, start_node)
	arena_parameters['traffic_signals'] = traffic_signals
	arena_parameters['start_node'].append(start_node)


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

	#print('Horizonatl_roads_under_constr :', hori_roads)
	#print('vertiacal_roads_under_constr :', verti_roads)

	arena_parameters['horizontal_roads_under_construction']= hori_roads
	arena_parameters['vertical_roads_under_construction'] = verti_roads


	##################################################
	
	return arena_parameters




#print(detect_arena_parameters(img_given))