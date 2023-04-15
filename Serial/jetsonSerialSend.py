import serial

# Set the serial port and baud rate
port = "/dev/ttyAMA1"
baud_rate = 115200

# Open the serial port
JETSON_ser = serial.Serial(port, baud_rate)

# Send the string "Hello world"
JETSON_ser.write(b"Hello world") # Write the message as bytes

# Close the serial port
JETSON_ser.close()