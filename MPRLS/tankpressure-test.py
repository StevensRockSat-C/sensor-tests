import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_mprls

i2c = I2C(1)
time.sleep(2) # Needed to ensure i2c is properly initialized

# Simplest use, connect to default over I2C
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

while True:
    time.sleep(1)
    print((mpr.pressure,))