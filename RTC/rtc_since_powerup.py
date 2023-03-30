'''
Made to test the DS3231 RTC for T+ caculation
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ds3231
i2c = I2C(1)
time.sleep(2) # Needed to ensure i2c is properly initialized

ds3231 = adafruit_ds3231.DS3231(i2c)

class RTC:
    
    def __init__(self):
        
        try:
            self.rtcTime = ds3231.datetime
            self.now = round(time.time()*1000)
            self.t0 = self.now - (((self.rtcTime.tm_min * 60) + self.rtcTime.tm_sec + 2) * 1000) # The oscillator should take an average of 2s to start and calibrate, from the datasheet 
            self.ready = true
        except:
            print("No RTC is on the i2c line?!")
            self.ready = false
            
    def ready():
        return self.ready

    def getTPlus(): # Get the time since launch in seconds
        return round(time.time()) - round(self.t0 / 1000)

    def getTPlusMS(): # Get the time since launch in milliseconds
        return round(time.time()*1000) - self.t0
        
rtc = RTC()

while True:

    print("It's been " + rtc.getTPlusMS() + " ms since first power")
    time.sleep(1)