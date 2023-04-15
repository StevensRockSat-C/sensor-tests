'''
Made to use the Multiplexer to run multiple MPRLS

sudo pip3 install adafruit-circuitpython-tca9548a
'''

import time
from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_tca9548a
import adafruit_mprls
import adafruit_ssd1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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


# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = oled.height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()


# Setup CSV headers
print("Time(ms),Pressure 0(hPa),Pressure 1(hpa),Pressure 2(hpa),Pressure 3(hpa),Pressure 4(hpa)")

while True:
    
    oled.fill(0)

    draw.text((x, top),       "1: " + str(mpr0.pressure) + "  2: " + str(mpr1.pressure),  font=font, fill=255)
    draw.text((x, top+8),     "3: " + str(mpr2.pressure) + "  4: " + str(mpr3.pressure), font=font, fill=255)
    draw.text((x, top+16),    "5: " + str(mpr4.pressure),  font=font, fill=255)
    draw.text((x, top+16),    "t: " + str(round(time.time()*1000)) + " s",  font=font, fill=255)

    # Display image.
    oled.image(image)
    oled.show()
    
    print(str(round(time.time()*1000)) + "," + str(mpr0.pressure) + "," + str(mpr1.pressure) + "," + str(mpr2.pressure) + "," + str(mpr3.pressure) + "," + str(mpr4.pressure))
    time.sleep(0.25)