# Python based License Plate Recognition
License plate recognition used for model vehicles

## Based on

After a first version of this project that was based on opencv, we decided to use OpenAlpr to recognize license plates even for our model vehicle. The installation is based on the following link:

https://www.flat-planet.net/?tag=projects-2

## Install instructions

### 1) Add virtual environment to Thonny

You need to add the under 1) created virtual environment to your favorite python IDE. When using the simple Thonny IDE, the following instructions apply:

* open thonny and show the toolbar (for displaying 'File', 'Edit', 'View', ...) when it is hidden
* Tools -> Options -> Interpreter -> Alternative Python 3 interpreter or virtual environment -> Locate another python executable ...
* Choose the installed python3 binary in your virtual environment folder (~/.virtualenv/cv/python3), you need to activate displaying hidden files with a secondary click inside the open dialog

### 2) Install other dependencies

Switch into virtual environment and install pip packets:

```
workon cv
pip install imutils
pip install pytesseract
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

### 3) Install OpenAlpr

```
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install liblog4cplus-dev
```

Build and install OpenAlpr and the python bindings:
```
git clone https://github.com/openalpr/openalpr.git
cd openalpr/src
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..
make
sudo make install
cd ../bindings/python
sudo python3 setup.py install
```

### 4) Install dependencies for LCD

Used library for display driver ST7036:

https://pypi.org/project/st7036/

It is available via github:

https://github.com/pimoroni/st7036

```
workon cv
pip install st7036
```

## Used ressources

https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md

https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/6

