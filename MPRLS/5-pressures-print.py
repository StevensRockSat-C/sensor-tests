'''
Made to use the Multiplexer to run multiple MPRLS

sudo pip3 install adafruit-circuitpython-tca9548a
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_mprls

i2c = I2C(1) # Use i2c bus #1
time.sleep(2) # Needed to ensure i2c is properly initialized

multi = adafruit_tca9548a.TCA9548A(i2c)

# Use the Multiplexer to connect to the different MPRLS
mpr0 = adafruit_mprls.MPRLS(multi[0], psi_min=0, psi_max=25)
mpr1 = adafruit_mprls.MPRLS(multi[1], psi_min=0, psi_max=25)
mpr2 = adafruit_mprls.MPRLS(multi[2], psi_min=0, psi_max=25)
mpr3 = adafruit_mprls.MPRLS(multi[3], psi_min=0, psi_max=25)
mpr4 = adafruit_mprls.MPRLS(multi[4], psi_min=0, psi_max=25)

oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Setup CSV headers
print("Time(ms),Pressure 0(hPa),Pressure 1(hpa),Pressure 2(hpa),Pressure 3(hpa),Pressure 4(hpa)")

while True:
    print(str(round(time.time()*1000)) + "," + str(mpr0.pressure) + "," + str(mpr1.pressure) + "," + str(mpr2.pressure) + "," + str(mpr3.pressure) + "," + str(mpr4.pressure))
    time.sleep(0.1)