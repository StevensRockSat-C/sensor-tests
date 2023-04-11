'''
Tests moving sample between two tanks and a bleed repo
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_mprls
import RPi.GPIO as GPIO

# SETTINGS
main_valve = 13
bleed_valve = 15
valve1 = 19
valve2 = 21

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
    GPIO.output(bleed_valve, GPIO.HIGH)
    for i in range(10):
        printInfo()
    GPIO.output(bleed_valve, GPIO.LOW)
    
    for i in range(3):
        printInfo()
    
    GPIO.output(main_valve, GPIO.HIGH)
    GPIO.output(valve, GPIO.HIGH)
    for i in range(10):
        printInfo()
    GPIO.output(main_valve, GPIO.LOW)
    GPIO.output(valve, GPIO.LOW)
    
for i in range(30):
    printInfo()

sampleFrom(valve1)

for i in range(10):
    printInfo()

sampleFrom(valve2)

while True:
    printInfo()