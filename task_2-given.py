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

# Author Name:		[]
# Roll No:			[]
# Filename:			task_2_{your name}.py
# Functions:		detect_arena_parameters
# 					[ Comma separated list of functions in this file ]


####################### IMPORT MODULES #######################
   ## You are free to make any changes in this section. ##
##############################################################
import cv2
import numpy as np
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
	arena_parameters = {}

	##############	ADD YOUR CODE HERE	##############

	##################################################
	
	return arena_parameters
