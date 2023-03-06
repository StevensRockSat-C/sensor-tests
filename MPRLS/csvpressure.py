import time
import board
import adafruit_mprls

i2c = board.I2C()

# Simplest use, connect to default over I2C
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

print("Time(ms),Pressure(hPa)")

while True:
    print(str(round(time.time()*1000)*1000) + "," + str(mpr.pressure))
    time.sleep(60)