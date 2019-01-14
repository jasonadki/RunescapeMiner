import numpy as np
import pyautogui
import imutils
import cv2
import pandas as pd
import pythoncom, pyHook
"""
The purpose of this script is to be able to save images off of a screen quickly and painlessly.
Just open up the application that you are trying to grab images of so it displays on your screen,
move your mouse over the image you are trying to target (in the Runescape bot I put it over the rock) and press 'Enter'.
A png of your screen will then be saved in the images folder and the discription and location of the target will be recorded in the annotations.csv

"""



# Create function add list to dataframe as new row
def addRow(df,ls):
	"""
	Given a dataframe and a list,
	append the list as a new row to the dataframe.
	Should probably add error catches but I know what I am adding.
	
	:param df: <DataFrame> The original dataframe
	:param ls: <list> The new row to be added
	:return: <DataFrame> The dataframe with the newly appended row
	"""

	# Number of elements in the new row.
	numEl = len(ls)

	# Create a new dataframe with the same column names
	newRow = pd.DataFrame(np.array(ls).reshape(1,numEl), columns = list(df.columns))

	# Append the new dataframe
	df = df.append(newRow, ignore_index = True)
	return df


def saveImage():
	global i

	# Get screenshot and then convert to BGR color scheme
	image = pyautogui.screenshot()
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

	# Save image
	cv2.imwrite(f'./images/{i}.png', image)


def saveImageInfo():
	global df, i

	# Get screenshot and then convert to BGR color scheme
	image = pyautogui.screenshot()
	image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

	# Get position of mouse
	mousePos = pyautogui.position()
	mouseX = mousePos[0]
	mouseY = mousePos[1]

	# Define variables
	xMin = mouseX - 40
	xMax = mouseX + 40
	yMin = mouseY - 65
	yMax = mouseY + 15
	width = image.shape[1]
	height = image.shape[0]

	# Append image info to the dataframe
	newRow = [f'{i}.png', width, height, 'availRock', xMin, yMin, xMax, yMax]
	df = addRow(df, newRow)

def writeImageInfo():
	# Write annotations to csv
	df.to_csv("./annotation/annotations.csv", index = False)	


def OnKeyboardEvent(event):
	global i
	if event.KeyID == 13:	# "Enter"
		saveImage()
		saveImageInfo()
		i += 1
		
	elif event.KeyID == 81: # "q"
		writeImageInfo()

	return True



if __name__ == '__main__':
	i = 0

	# Create empty dataframe to hold annotations
	df = pd.DataFrame(columns = ['fileName', 'width', 'height', 'class',
									'xMin', 'yMin', 'xMax', 'yMax'])

	hm = pyHook.HookManager()
	# watch for all keyboard events
	hm.KeyDown = OnKeyboardEvent
	# set the hook
	hm.HookKeyboard()
	# wait forever
	pythoncom.PumpMessages()

