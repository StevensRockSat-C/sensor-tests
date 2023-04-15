import serial

# Set the serial port and baud rate
port = "/dev/serial0"
baud_rate = 115200

# Open the serial port
PI_ser = serial.Serial(port, baud_rate)

# Send the string "Hello world"
try:
    PI_ser.write(b"Hello world")

finally:
    # Close the serial port
    PI_ser.close()
