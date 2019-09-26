# Python based License Plate Recognition
License plate recognition used for model vehicles

## Based on

https://circuitdigest.com/microcontroller-projects/license-plate-recognition-using-raspberry-pi-and-opencv

## Install instructions

### 1) Install OpenCv

https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/

### 2) Add virtual environment to Thonny

You need to add the under 1) created virtual environment to your favorite python IDE. When using the simple Thonny IDE, the following instructions apply:

* open thonny and show the toolbar (for displaying 'File', 'Edit', 'View', ...) when it is hidden
* Tools -> Options -> Interpreter -> Alternative Python 3 interpreter or virtual environment -> Locate another python executable ...
* Choose the installed python3 binary in your virtual environment folder (~/.virtualenv/cv/python3), you need to activate displaying hidden files with a secondary click inside the open dialog

### 3) Install other dependencies

Switch into virtual environment and install pip packets:

'''
workon cv
pip install imutils
pip install pytesseract
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
'''

### 4) Install dependencies for LCD

Used library for display driver ST7036:

https://pypi.org/project/st7036/

It is available via github:

https://github.com/pimoroni/st7036

'''
workon cv
pip install st7036
'''

## Used ressources

https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md

https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/6

