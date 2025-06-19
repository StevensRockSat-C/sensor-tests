from RPi import GPIO
import time

GSWITCH_PIN = 25            # G-switch input pin

def timeMS():
    """Get system time to MS."""
    return round(time.time()*1000)

# Setup the G-Switch listener
GPIO.setup(GSWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(GSWITCH_PIN, GPIO.FALLING,
                      callback=lambda channel: gswitch_callback(channel, GSWITCH_PIN), 
                      bouncetime=500)

def gswitch_callback(channel, pin):
    print("Pressed: " + str(timeMS()))