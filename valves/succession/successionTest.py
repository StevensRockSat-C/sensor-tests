import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) # Use BS made up numbers

main_valve = 27
dynamic_valve = 18
static_valve = 17
valve1 = 24
valve2 = 23

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
GPIO.setup(static_valve, GPIO.OUT)
GPIO.setup(valve1, GPIO.OUT)
GPIO.setup(valve2, GPIO.OUT)
GPIO.setup(dynamic_valve, GPIO.OUT)

# Set all to low
print("All low")
GPIO.output(main_valve, GPIO.LOW)
GPIO.output(static_valve, GPIO.LOW)
GPIO.output(valve1, GPIO.LOW)
GPIO.output(valve2, GPIO.LOW)
GPIO.output(dynamic_valve, GPIO.LOW)

time.sleep(1)

print("valve1 high")
GPIO.output(valve1, GPIO.HIGH)
time.sleep(1)
print("valve1 low\n")
GPIO.output(valve1, GPIO.LOW)

time.sleep(1)

print("valve2 high")
GPIO.output(valve2, GPIO.HIGH)
time.sleep(1)
print("valve2 low\n")
GPIO.output(valve2, GPIO.LOW)

time.sleep(1)

print("dynamic_valve high")
GPIO.output(dynamic_valve, GPIO.HIGH)
time.sleep(1)
print("dynamic_valve low\n")
GPIO.output(dynamic_valve, GPIO.LOW)

time.sleep(1)

print("static_valve high")
GPIO.output(static_valve, GPIO.HIGH)
time.sleep(1)
print("static_valve low\n")
GPIO.output(static_valve, GPIO.LOW)

time.sleep(1)

print("main_valve high")
GPIO.output(main_valve, GPIO.HIGH)
time.sleep(1)
print("main_valve low\n")
GPIO.output(main_valve, GPIO.LOW)

time.sleep(2)

print("main_valve high")
print("static_valve high")
GPIO.output(main_valve, GPIO.HIGH)
GPIO.output(static_valve, GPIO.HIGH)
time.sleep(2)
print("static_valve low")
print("valve1 high")
GPIO.output(static_valve, GPIO.LOW)
GPIO.output(valve1, GPIO.HIGH)
time.sleep(2)
print("main_valve low")
print("valve1 low\n")
GPIO.output(main_valve, GPIO.LOW)
GPIO.output(valve1, GPIO.LOW)

time.sleep(2)

print("main_valve high")
print("static_valve high")
GPIO.output(main_valve, GPIO.HIGH)
GPIO.output(static_valve, GPIO.HIGH)
time.sleep(2)
print("static_valve low")
print("valve2 high")
GPIO.output(static_valve, GPIO.LOW)
GPIO.output(valve2, GPIO.HIGH)
time.sleep(2)
print("main_valve low")
print("valve2 low\n")
GPIO.output(main_valve, GPIO.LOW)
GPIO.output(valve2, GPIO.LOW)

time.sleep(2)

print("main_valve high")
print("static_valve high")
GPIO.output(main_valve, GPIO.HIGH)
GPIO.output(static_valve, GPIO.HIGH)
time.sleep(2)
print("static_valve low")
print("dynamic_valve high")
GPIO.output(static_valve, GPIO.LOW)
GPIO.output(dynamic_valve, GPIO.HIGH)
time.sleep(2)
print("main_valve low")
print("dynamic_valve low")
GPIO.output(main_valve, GPIO.LOW)
GPIO.output(dynamic_valve, GPIO.LOW)

time.sleep(1)

GPIO.cleanup()