'''
Simple license plate recognition used for model vehicles
Created 2019/09/18 for Hackfest @Schenck Process
'''

##### CONSTANTS

# TODO need to guess this factor (or use machine learning to train system)
CONTOUR_FACTOR = 0.018

SLEEP_TIME_BETWEEN_CAPTURES_S = 0.5

TMP_PICTURE_PATH = '/home/pi/Desktop/tmp_img.jpg'

##### INCLUDES

import cv2
import imutils
import numpy as np
import pytesseract
import picamera
from picamera.array import PiRGBArray
import time
from st7036-lcd import printLicensePlate

##### FUNCTIONS

def parseLicensePlate(img):
    img = cv2.resize(img, (620,480) )

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection

    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
    screenCnt = None

    # loop over our contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, CONTOUR_FACTOR * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print("No contour detected")
    else:
        detected = 1
        print("Contour detected")

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        # Masking the part other than the number plate
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        # Now crop
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Read the number plate
        text = pytesseract.image_to_string(Cropped, config='--psm 11')
        print("Detected Number is:",text)
        
        # now print found license plate on LCD
        # TODO
        #printLicensePlate(text)

        cv2.imshow('image',img)
        cv2.imshow('Cropped',Cropped)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

##### MAIN ENTRY

running = True
print("Started license plate recognition script,", time.ctime())
last_iteration_time = time.time()

with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 5
    while running:
        camera.start_preview()
        time.sleep(SLEEP_TIME_BETWEEN_CAPTURES_S)
        
        with picamera.array.PiRGBArray(camera) as stream:
            camera.capture(stream, format='bgr')
            image = stream.array
            #cv2.imwrite('tmp_image.jpg', image)
            #cv2.imshow("image", image)
            #if cv2.waitKey(0) & 0xFF == ord('q'):
            #    running = False
            #    break
            print("Trying to parse license plate...")
            parseLicensePlate(image)
            
        new_iteration_time = time.time()
        iteration_diff = new_iteration_time - last_iteration_time
        last_iteration_time = new_iteration_time
        
        print("New iteration after", iteration_diff)
        
    cv2.destroyAllWindows()
        
