import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # Use the board's physical pin numbers

# Set the pins to output
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

GPIO.output(13, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(13, GPIO.LOW)

time.sleep(1)

GPIO.output(15, GPIO.HIGH)
time.sleep(0.5)
GPIO.output(15, GPIO.LOW)

GPIO.cleanup()