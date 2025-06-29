'''
    Script to read from an ADXL372 on the SPI bus.
'''

import spidev
import time

READ_HZ = 6400.0
READ_SLEEP = 1.0/READ_HZ

# SPI configuration
spi = spidev.SpiDev()
spi.open(0, 0)  # Specify SPI bus and device (0, 0 for default SPI bus on Raspberry Pi)

# ADXL372 command codes
READ_REG = 0x0B
WRITE_REG = 0x0A

# ADXL372 register addresses
X_DATA_REG = 0x08  # X-axis data register (14 bits)
Y_DATA_REG = 0x0A  # Y-axis data register (14 bits)
Z_DATA_REG = 0x0C  # Z-axis data register (14 bits)

def read_register(register):
    command = [READ_REG, register, 0x00]
    response = spi.xfer2(command)
    return response[2]

def read_acceleration(axis_reg):
    low_byte = read_register(axis_reg + 1)
    high_byte = read_register(axis_reg)
    raw_value = (high_byte << 8) | low_byte

    # Convert 14-bit signed value to signed integer
    #if raw_value & 0x2000:
    #   raw_value -= 0x4000

    return raw_value

print(f"Status Register,X-Axis,Y-Axis,Z-Axis,")
try:
    while True:
        x_accel = read_acceleration(X_DATA_REG)
        y_accel = read_acceleration(Y_DATA_REG)
        z_accel = read_acceleration(Z_DATA_REG)
        status = read_register(0x04)
        
        print(format(status, 'b'), end = ",")
        print(f"{x_accel},{y_accel},{z_accel},")

        time.sleep(READ_SLEEP)  # Adjust sleep time based on your desired sampling rate

except KeyboardInterrupt:
    spi.close()
    print("SPI closed. Exiting.")
