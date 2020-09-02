'''
Simple license plate recognition used for model vehicles
Created 2019/09/18 for Hackfest @Schenck Process
'''

##### CONSTANTS

# webserver settings
PORT = 8080

# global settings
CLEAR_DISPLAY_AFTER_NOPLATETRIES_CNT = 5
IMG_PATH_ORIGINAL = "/home/pi/license-plate-recognition/plate_orig.jpg"
IMG_PATH_PLATE = "/home/pi/license-plate-recognition/plate_crop.jpg"
PLATE_TXT_FILE = "/home/pi/license-plate-recognition/plate.txt"

# picture settings
FRAME_RATE = 50
SLEEP_TIME_BETWEEN_CAPTURES_S = 0.3
RESOLUTION_X= 1280 # 640
RESOLUTION_Y = 1024 # 480
#CROPPED_PERCENT_X = 25
#CROPPED_PERCENT_Y = 15

# debug settings
ACTIVATE_IMAGE_SHOWS = 0

##### INCLUDES

import cv2
import imutils
import numpy as np
import pytesseract
import picamera
from picamera.array import PiRGBArray
import st7036
import time
import re
import _thread
import http.server
import socketserver
import locale
from openalpr import Alpr
import json
import locale

locale.setlocale(locale.LC_ALL, 'C')

##### GLOBAL VARIABLES

counterNoPlates = 0
alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data")
Handler = http.server.SimpleHTTPRequestHandler
# license plate can look like: "DASP123", "AURKS688", "DA SP 123", "DA SP123", "DA SP 1", " DA SP 12  ", ...
RegexPlate = re.compile(r"^\s*([A-Z]{1,3})\s*([A-Z]{2})\s*(\d{1,4})\s*")

##### FUNCTIONS

def printLicensePlateOnLCD(plateStr):
    lcd.clear()
    lcd.write(plateStr)
    
def printLicensePlateInFile(plateStr):
    with open(PLATE_TXT_FILE, "w") as f:
        f.write(plateStr)
        
def printLicensePlate(plateStr):
    printLicensePlateInFile(plateStr)
    printLicensePlateOnLCD(plateStr)

# check if given text is a plausible license plate
def getLicensePlateText(text):
    m = RegexPlate.match(text)
    if len(m.groups()) >= 2:
        return m.group(0) + "-" + m.group(1) + "-" + m.group(2)
    return ""

def parseLicensePlate(img):
    global counterNoPlates
    global alpr
    
    # store original image on filesystem for webserver
    #cv2.imwrite(IMG_PATH_ORIGINAL, img) 
    
    #length_x = (RESOLUTION_X / 100 * CROPPED_PERCENT_X)
    #length_y = (RESOLUTION_Y / 100 * CROPPED_PERCENT_Y)
    #start_int_x = int((RESOLUTION_X / 2) - length_x / 2)
    #start_int_y = int((RESOLUTION_Y / 2) - length_y / 2)
    #length_int_x = int(length_x)
    #length_int_y = int(length_y)
    #imgCrop = img[start_int_y:start_int_y+length_int_y, start_int_x:start_int_x+length_int_x]
    
    #if ACTIVATE_IMAGE_SHOWS:
    #    print("Showing normal image")
    #    cv2.imshow('image',img)
    #    cv2.waitKey(0)
    #    print("Showing cropped image!")
    #    cv2.imshow('image',imgCrop)
    #    cv2.waitKey(0)

    #gray = cv2.cvtColor(imgCrop, cv2.COLOR_BGR2GRAY) #convert to grey scale
    #gray = cv2.bilateralFilter(gray, 50, 17, 217) #Blur to reduce noise
    #edged = cv2.Canny(gray, 100, 20) #Perform Edge detection
    
    #if ACTIVATE_IMAGE_SHOWS:
    #    print("Showing gray image!")
    #    cv2.imshow('image', gray)
    #    cv2.waitKey(0)
    #    print("Showing edged image!")
    #    cv2.imshow('image', edged)
    #    cv2.waitKey(0)

    # try to parse modified image to text
    #text = pytesseract.image_to_string(imgCrop, config='--psm 11')
    results = alpr.recognize_file(img)
    #print(json.dumps(results, indent=4))
    text = ""

    if len(results['results']) == 0:
        print('No number plate detected in recognize_file()')
    else:
        text = results['results'][0]['plate']
        print("Detected text: ", text)
    
    licensePlate = getLicensePlateText(text)
    if licensePlate != "":
        counterNoPlates = 0
        print("Detected License plate: ", licensePlate)
        printLicensePlate(licensePlate)
        coord = results['results'][0]['coordinates']
        imgCrop = img[coord[0]['y']:coord[2]['y'], coord[0]['x']:coord[2]['x']]
        cv2.imwrite(IMG_PATH_PLATE, imgCrop)
        if ACTIVATE_IMAGE_SHOWS:
            print("Showing cropped image!")
            cv2.imshow('image', imgCrop)
            cv2.waitKey(0)
    else:
        counterNoPlates = counterNoPlates + 1
        if counterNoPlates >= CLEAR_DISPLAY_AFTER_NOPLATETRIES_CNT:
            print("Clearing display...")
            printLicensePlate("")
            counterNoPlates = 0
        
    cv2.destroyAllWindows()
    
def start_webserver():
    print("Starting webserver...")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
            
def start_license_plate():
    # initialize global variables
    counterNoPlates = 0

    with picamera.PiCamera() as camera:
        camera.resolution = (RESOLUTION_X, RESOLUTION_Y)
        camera.framerate = FRAME_RATE
        while True:
            #camera.start_preview()
            time.sleep(SLEEP_TIME_BETWEEN_CAPTURES_S)
        
            #with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(IMG_PATH_ORIGINAL)
            #image = stream.array
            print("Trying to parse license plate...")
            parseLicensePlate(IMG_PATH_ORIGINAL)
        
        cv2.destroyAllWindows()
        alpr.unload()

##### MAIN ENTRY

print("Started license plate recognition script")

lcd = st7036.st7036(register_select_pin=22, rows=1, columns=8, spi_chip_select=0)
lcd.set_display_mode()
lcd.set_contrast(40)
lcd.clear()
time.sleep(1)

try:
    _thread.start_new_thread(start_license_plate, ())
    _thread.start_new_thread(start_webserver, ())
except:
    print("Error: Could not start threads!")

while True:
    time.sleep(50)
    pass
