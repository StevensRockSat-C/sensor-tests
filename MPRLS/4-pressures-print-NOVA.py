'''
Made to use the Multiplexer to run multiple MPRLS

sudo pip3 install adafruit-circuitpython-tca9548a
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_mprls

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.absolute()))

from AIR.pi.MPRLS import NovaPressureSensor

i2c = I2C(1) # Use i2c bus #1
time.sleep(2) # Needed to ensure i2c is properly initialized

multi = adafruit_tca9548a.TCA9548A(i2c)

# Use the Multiplexer to connect to the different MPRLS
mpr0 = NovaPressureSensor(channel=multi[1], psi_max=100)
mpr1 = NovaPressureSensor(channel=multi[2])
mpr2 = NovaPressureSensor(channel=multi[3])
mpr3 = adafruit_mprls.MPRLS(multi[0], psi_min=0, psi_max=25)

# Setup CSV headers
print("Time(ms),Pressure Manifold(hPa),Pressure 1(hpa),Pressure 2(hpa),Pressure Canister(hpa)")

while True:
    print(str(round(time.time()*1000)) + "," + str(mpr0.pressure) + "," + str(mpr1.pressure) + "," + str(mpr2.pressure) + "," + str(mpr3.pressure) + "," + str(mpr4.pressure))
    time.sleep(0.1)