'''
Simple license plate recognition used for model vehicles
Created 2019/09/18 for Hackfest @Schenck Process
'''

##### CONSTANTS

# TODO need to guess this factor (or use machine learning to train system)
CONTOUR_FACTOR = 0.018

SLEEP_TIME_BETWEEN_PICS = 5

TMP_PICTURE_PATH = '/home/pi/Desktop/tmp_img.jpg'

##### INCLUDES

import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from picamera import PiCamera
from picamera import PiRGBArray
from time import sleep

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
	 approx = cv2.approxPolyDP(c, 0.018 * peri, True)

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

	#Read the number plate
	text = pytesseract.image_to_string(Cropped, config='--psm 11')
	print("Detected Number is:",text)

	cv2.imshow('image',img)
	cv2.imshow('Cropped',Cropped)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

##### MAIN ENTRY

# loop from https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
rawCapture = PiRGCArray(camera, size=(640, 480))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
 
	# show the frame
	cv2.imshow("Frame", image)
	
	# wait for user key
	key = cv2.waitKey(1) & 0xFF
	
	# ggf. img = cv2.imread(TMP_PICTURE_PATH,cv2.IMREAD_COLOR)
	parseLicensePlate(image)
	
	# wait for user key
	key = cv2.waitKey(1) & 0xFF
 
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
