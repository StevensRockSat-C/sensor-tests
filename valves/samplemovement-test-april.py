'''
Tests moving sample between two tanks and a bleed repo
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_mprls
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # Use the board's physical pin numbers

# SETTINGS
"""
main_valve = 13 (BOARD) -> 27 (BCM)
bleed_valve = 15 (BOARD) -> 22 (BCM)
valve1 = 19 (BOARD) -> 10 (BCM)
valve2 = 21 (BOARD) -> 9 (BCM)
"""
main_valve = 27
bleed_valve = 22
valve1 = 10
valve2 = 9

i2c = I2C(1) # Use i2c bus #1
time.sleep(2) # Needed to ensure i2c is properly initialized

# Set GPIO outs
GPIO.setup(main_valve, GPIO.OUT)
GPIO.setup(bleed_valve, GPIO.OUT)
GPIO.setup(valve1, GPIO.OUT)
GPIO.setup(valve2, GPIO.OUT)

# Set all to low
GPIO.output(main_valve, GPIO.LOW)
GPIO.output(bleed_valve, GPIO.LOW)
GPIO.output(valve1, GPIO.LOW)
GPIO.output(valve2, GPIO.LOW)

multi = adafruit_tca9548a.TCA9548A(i2c)

# Use the Multiplexer to connect to the different MPRLS
mpr0 = adafruit_mprls.MPRLS(multi[0], psi_min=0, psi_max=25)
mpr1 = adafruit_mprls.MPRLS(multi[1], psi_min=0, psi_max=25)
mpr2 = adafruit_mprls.MPRLS(multi[2], psi_min=0, psi_max=25)

# Setup CSV headers
print("Time(ms),Pressure 0(hPa),Pressure 1(hpa),Pressure 2(hpa)")

def printInfo():
    print(str(round(time.time()*1000)) + "," + str(mpr0.pressure) + "," + str(mpr1.pressure) + "," + str(mpr2.pressure))
    time.sleep(0.1)
    
def sampleFrom(valve):

    printInfo()
    
    # Cycle bleed
    print(str(round(time.time()*1000)) + " - bleed open")
    GPIO.output(bleed_valve, GPIO.HIGH)
    for i in range(10):
        printInfo()
    print(str(round(time.time()*1000)) + " - bleed close")
    GPIO.output(bleed_valve, GPIO.LOW)
    
    for i in range(3):
        printInfo()
    
    print(str(round(time.time()*1000)) + " - main open")
    GPIO.output(main_valve, GPIO.HIGH)
    print(str(round(time.time()*1000)) + " - BCM " + valve + " open")
    GPIO.output(valve, GPIO.HIGH)
    for i in range(10):
        printInfo()
    print(str(round(time.time()*1000)) + " - main close")
    GPIO.output(main_valve, GPIO.LOW)
    print(str(round(time.time()*1000)) + " - BCM " + valve + " close")
    GPIO.output(valve, GPIO.LOW)
    
for i in range(100):
    printInfo()

sampleFrom(valve1)

for i in range(10):
    printInfo()

sampleFrom(valve2)

for i in range(100):
    printInfo()

GPIO.cleanup()