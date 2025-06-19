import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM) # Use BS made up numbers

GSWITCH_PIN = 25            # G-switch input pin
main_valve = 27

def timeMS():
    """Get system time to MS."""
    return round(time.time()*1000)

"""

      +-------------------------------------------------------+
      |  3V3  (1) (2)  5V                                    |
      |  GPIO2 (3) (4)  5V                                    |
      |  GPIO3 (5) (6)  GND                                   |
      |  GPIO4 (7) (8)  GPIO14                                |
      |    GND (9) (10) GPIO15                                |
      | GPIO17 (11) (12) GPIO18                               |
  --> | GPIO27 (13) (14) GND                                  |
  --> | GPIO22 (15) (16) GPIO23                               |
      |  3V3  (17) (18) GPIO24                                |
  --> | GPIO10 (19) (20) GND                                  |
  --> |  GPIO9 (21) (22) GPIO25                               |
  --> | GPIO11 (23) (24) GPIO8                                |
      |    GND (25) (26) GPIO7                                |
      |  GPIO0 (27) (28) GPIO1                                |
      |  GPIO5 (29) (30) GND                                  |
      |  GPIO6 (31) (32) GPIO12                               |
      | GPIO13 (33) (34) GND                                  |
      | GPIO19 (35) (36) GPIO16                               |
      | GPIO26 (37) (38) GPIO20                               |
      |    GND (39) (40) GPIO21                               |
      +-------------------------------------------------------+

"""

# Set the pins to output
GPIO.setup(main_valve, GPIO.OUT)

# Set all to low
print("All low")
GPIO.output(main_valve, GPIO.LOW)

# Setup the G-Switch listener
GPIO.setup(GSWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(GSWITCH_PIN, GPIO.FALLING,
                      callback=lambda channel: gswitch_callback(channel, GSWITCH_PIN), 
                      bouncetime=500)

def gswitch_callback(channel, pin):
    print("Pressed: " + str(timeMS()))

timestart = timeMS()
while (timeMS() < timestart + 1000):
    pass

print("main_valve high")
GPIO.output(main_valve, GPIO.HIGH)

timestart = timeMS()
while (timeMS() < timestart + 2000):
    pass

print("main_valve low\n")
GPIO.output(main_valve, GPIO.LOW)

timestart = timeMS()
while (timeMS() < timestart + 2000):
    pass

GPIO.cleanup()