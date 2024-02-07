#include "adxl372_withSPIlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

const uint8_t spi_mode = SPI_MODE;  // Declare a variable for SPI mode
const uint8_t bits_per_word = BITS_PER_WORD;  // Declare a variable for SPI mode
const uint32_t spi_speed = SPI_SPEED;  // Declare a variable for SPI mode

volatile int terminating = 0;

const uint8_t X_DATA_REG = 0x08;  // X-axis data register (12 bits)
const uint8_t Y_DATA_REG = 0x0A;  // Y-axis data register (12 bits)
const uint8_t Z_DATA_REG = 0x0C;  // Z-axis data register (12 bits)

int16_t readRegister(SPI_HANDLE spi, uint8_t reg) { 
    
	uint8_t buf[3] = { WRITE_CMD, reg, 0x00 };	// Example of LCD screen data you may want to send
	SpiWriteAndRead(spi, &buf[1], &buf[2], 3, false);   // Transfer buffer data to SPI call

    return buf[2];
}

int16_t readRegisterPair(SPI_HANDLE spi, uint8_t reg) { 
    
	uint8_t highRegister = readRegister(spi, reg);
	uint8_t lowRegister = readRegister(spi, reg+1);

    int16_t value = ((int16_t)highRegister << 8) | lowRegister;
    return value;
}

void terminate(int sign) {
  signal(SIGINT, SIG_DFL);
  terminating = 1;
}


int main() {
    // Initialize SPI 8 bits, 1Mhz, Mode 0, no semaphore locks
    SPI_HANDLE spi = SpiOpenPort(SPI_DEVICE, bits_per_word, SPI_SPEED, spi_mode, false);
    if (!spi) {
        perror("Error opening SPI device");
        return EXIT_FAILURE;
    }

    // Set ODR to 6.4 kHz and enable low-noise mode
    // set_register(POWER_CTL, 0b00101000); // ODR = 6.4 kHz, Low-Noise Mode

    // Set filter settings (if needed)
    // set_register(FILTER_CTL, ...);

    printf("X, Y, Z");

    while (1) {
        // Read accelerometer data
        uint8_t x_data = readRegisterPair(spi, X_DATA_REG);
        uint8_t y_data = readRegisterPair(spi, Y_DATA_REG);
        uint8_t z_data = readRegisterPair(spi, Z_DATA_REG);

        // Combine bytes to get signed 16-bit values
        int16_t x_value = (int16_t)x_data;
        int16_t y_value = (int16_t)y_data;
        int16_t z_value = (int16_t)z_data;

        // Print accelerometer data
        printf("%d, %d, %d\n", x_value, y_value, z_value);

        // Adjust the delay based on your desired effective sampling rate
        usleep(156); // Delay for approximately 6.4 kHz sampling rate
		
		if (terminating) {
		   SpiClosePort(spi);
		   break;
		}
    }
	
    return EXIT_SUCCESS;
}