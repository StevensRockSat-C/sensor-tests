'''
Made to log the time and pressure from the MPRLS in CSV format.
Call with -u to leave the output unbuffered for tee

python3.8 -u sample-collection-test.py |& tee output.csv
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_mprls

i2c = I2C(1)
time.sleep(2) # Needed to ensure i2c is properly initialized

# Simplest use, connect to default over I2C
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

# Setup CSV headers
print("Time(ms),Pressure(hPa)")

while True:
    print(str(round(time.time()*1000)) + "," + str(mpr.pressure))
    time.sleep(0.5)