'''
Made to test the DS3231 RTC for T+ caculation
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_ds3231
i2c = I2C(1)
time.sleep(2) # Needed to ensure i2c is properly initialized

print("i2c up, connecting to DS3231")
ds3231 = adafruit_ds3231.DS3231(i2c)
print("Connected")

class RTC:
    
    def __init__(self):
        self.ready = False
        
        try:
            self.rtcTime = ds3231.datetime
            print('The self.rtcTime time is: {}/{}/{} {:02}:{:02}:{:02}'.format(self.rtcTime.tm_mon, self.rtcTime.tm_mday, self.rtcTime.tm_year, self.rtcTime.tm_hour, self.rtcTime.tm_min, self.rtcTime.tm_sec))
            self.now = round(time.time()*1000)
            self.t0 = self.now - (((self.rtcTime.tm_min * 60) + self.rtcTime.tm_sec) * 1000) # The oscillator should take an average of 2s to start and calibrate, from the datasheet 
            self.ready = True
        except:
            print("No RTC is on the i2c line?!")
            self.ready = False
            
    def ready(self):
        return self.ready

    def getTPlus(self): # Get the time since launch in seconds
        return round(time.time()) - round(self.t0 / 1000)

    def getTPlusMS(self): # Get the time since launch in milliseconds
        return round(time.time()*1000) - self.t0
        
rtc = RTC()

while True:

    print("It's been " + str(rtc.getTPlusMS()) + " ms since first power")
    time.sleep(1)