import serial

ser = serial.Serial('/dev/ttyTHS1', 9600) # Replace '/dev/ttyUSB0' with the correct serial port on the Jetson

while True:
    if ser.in_waiting > 0: # check if there's data available to be read
        data = ser.readline().decode().rstrip()
        print(data)
