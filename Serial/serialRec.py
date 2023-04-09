import serial

# Set the serial port and baud rate
port = "/dev/serial0"
baud_rate = 115200

# Open the serial port
PI_ser = serial.Serial(port, baud_rate)

# Wait until data is available to be read
while PI_ser.in_waiting == 0:
    pass

# Read the string sent by the sender
PI_ser = PI_ser.read_until()

# Print the received string
print(PI_ser)

# Close the serial port
PI_ser.close()
