'''
Simple license plate recognition used for model vehicles
Created 2019/09/18 for Hackfest @Schenck Process
'''

##### CONSTANTS

# global settings
CLEAR_DISPLAY_AFTER_NOPLATETRIES_CNT = 3

# picture settings
FRAME_RATE = 50
SLEEP_TIME_BETWEEN_CAPTURES_S = 0.5
RESOLUTION_X= 1280 # 640
RESOLUTION_Y = 1024 # 480
CROPPED_PERCENT_X = 25
CROPPED_PERCENT_Y = 15

# debug settings
ACTIVATE_IMAGE_SHOWS = 0

##### INCLUDES

import cv2
import imutils
import numpy as np
import pytesseract
import picamera
from picamera.array import PiRGBArray
from st7036lcd import printLicensePlate
import time
import re

##### GLOBAL VARIABLES

counterNoPlates = 0

##### FUNCTIONS

# check if given text is a plausible license plate
def getLicensePlateText(text):
    reg = re.findall(r".*\w\w[-]\w\w[-]\d\d.*", text)
    if len(reg) > 0:
        return reg[0]
    return ""

def parseLicensePlate(img):
    global counterNoPlates
    
    length_x = (RESOLUTION_X / 100 * CROPPED_PERCENT_X)
    length_y = (RESOLUTION_Y / 100 * CROPPED_PERCENT_Y)
    start_int_x = int((RESOLUTION_X / 2) - length_x / 2)
    start_int_y = int((RESOLUTION_Y / 2) - length_y / 2)
    length_int_x = int(length_x)
    length_int_y = int(length_y)
    imgCrop = img[start_int_y:start_int_y+length_int_y, start_int_x:start_int_x+length_int_x]
    
    if ACTIVATE_IMAGE_SHOWS:
        print("Showing normal image")
        cv2.imshow('image',img)
        cv2.waitKey(0)
        print("Showing cropped image!")
        cv2.imshow('image',imgCrop)
        cv2.waitKey(0)

    gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 50, 17, 217) #Blur to reduce noise
    edged = cv2.Canny(gray, 100, 20) #Perform Edge detection
    
    if ACTIVATE_IMAGE_SHOWS:
        print("Showing gray image!")
        cv2.imshow('image', gray)
        cv2.waitKey(0)
        print("Showing edged image!")
        cv2.imshow('image', edged)
        cv2.waitKey(0)

    # try to parse modified image to text
    text = pytesseract.image_to_string(imgCrop, config='--psm 11')
    print("Detected text: ", text)
    
    licensePlate = getLicensePlateText(text)
    if licensePlate != "":
        print("Detected License plate: ", licensePlate)
        printLicensePlate(licensePlate)
    else:
        counterNoPlates = counterNoPlates + 1
        if counterNoPlates >= CLEAR_DISPLAY_AFTER_NOPLATETRIES_CNT:
            print("Clearing display...")
            printLicensePlate("")
            counterNoPlates = 0
        
    cv2.destroyAllWindows()

##### MAIN ENTRY

print("Started license plate recognition script")

# initialize global variables
counterNoPlates = 0

with picamera.PiCamera() as camera:
    camera.resolution = (RESOLUTION_X, RESOLUTION_Y)
    camera.framerate = FRAME_RATE
    while True:
        camera.start_preview()
        time.sleep(SLEEP_TIME_BETWEEN_CAPTURES_S)
        
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            image = stream.array
            print("Trying to parse license plate...")
            parseLicensePlate(image)
        
    cv2.destroyAllWindows()
        
