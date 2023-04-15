import serial

# Set the serial port and baud rate
port = "/dev/serial0"
baud_rate = 115200

# Open the serial port
PI_ser = serial.Serial(port, baud_rate)

# Wait until data is available to be read
while PI_ser.in_waiting == 0:
    pass

try:
    # Read the string sent by the sender
    rec = PI_ser.read_until()

    # Print the received string
    print(rec)
finally:
    # Close the serial port
    PI_ser.close()
