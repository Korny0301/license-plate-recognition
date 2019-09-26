'''
Display driver for ST7036 LCD. Based on:
https://github.com/pimoroni/st7036
Created 2019/09/26 for Hackfest @Schenck Process
'''

##### CONSTANTS


##### INCLUDES

import st7036
import time

##### FUNCTIONS

def printLicensePlate(plateStr):
    # TODO
    print("Dummy print for license plate:", plateStr)

##### MAIN ENTRY

lcd = st7036.st7036(register_select_pin=10, rows=2, columns=8, spi_chip_select=0)
lcd.set_display_mode()
lcd.set_contrast(40)
lcd.clear()
lcd.set_cursor_offset(0)
lcd.write("Hello World!")
time.sleep(3)

printLicensePlate("XX-YY-ZZZ")
