#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include "adxl372_spi.h"

int spi_fd;

uint8_t spi_mode = MODE;  // Declare a variable for SPI mode

void set_register(uint8_t reg, uint8_t value) {
    uint8_t data[2] = {reg, value};
    struct spi_ioc_transfer transfer = {
        .tx_buf = (unsigned long)data,
        .rx_buf = (unsigned long)NULL,
        .len = sizeof(data),
        .speed_hz = SPI_SPEED,
        .delay_usecs = 0,
        .bits_per_word = BITS_PER_WORD,
        .cs_change = 0,
    };

    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &transfer) < 0) {
        perror("SPI transfer failed");
        exit(EXIT_FAILURE);
    }
}

int read_register(uint8_t reg) {
    reg |= 0x80; // Set the READ bit to indicate a read operation
    uint8_t data[2] = {reg, 0};
    struct spi_ioc_transfer transfer = {
        .tx_buf = (unsigned long)data,
        .rx_buf = (unsigned long)data,
        .len = sizeof(data),
        .speed_hz = SPI_SPEED,
        .delay_usecs = 0,
        .bits_per_word = BITS_PER_WORD,
        .cs_change = 0,
    };

    if (ioctl(spi_fd, SPI_IOC_MESSAGE(1), &transfer) < 0) {
        perror("SPI transfer failed");
        exit(EXIT_FAILURE);
    }

    return data[1];
}

int main() {
    // Open SPI device
    spi_fd = open(SPI_DEVICE, O_RDWR);
    if (spi_fd < 0) {
        perror("Error opening SPI device");
        return EXIT_FAILURE;
    }

    // Configure SPI mode, speed, and bits per word
    if (ioctl(spi_fd, SPI_IOC_WR_MODE, &spi_mode) < 0) {
        perror("Error setting SPI mode");
        return EXIT_FAILURE;
    }

    if (ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &BITS_PER_WORD) < 0) {
        perror("Error setting SPI bits per word");
        return EXIT_FAILURE;
    }

    if (ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &SPI_SPEED) < 0) {
        perror("Error setting SPI speed");
        return EXIT_FAILURE;
    }

    // Set ODR to 6.4 kHz and enable low-noise mode
    set_register(POWER_CTL, 0b00101000); // ODR = 6.4 kHz, Low-Noise Mode

    // Set filter settings (if needed)
    // set_register(FILTER_CTL, ...);

    while (1) {
        // Read accelerometer data
        uint8_t x_data = read_register(X_DATA_REG);
        uint8_t y_data = read_register(Y_DATA_REG);
        uint8_t z_data = read_register(Z_DATA_REG);

        // Combine bytes to get signed 16-bit values
        int16_t x_value = (int16_t)x_data;
        int16_t y_value = (int16_t)y_data;
        int16_t z_value = (int16_t)z_data;

        // Print accelerometer data
        printf("X: %d, Y: %d, Z: %d\n", x_value, y_value, z_value);

        // Adjust the delay based on your desired effective sampling rate
        usleep(156); // Delay for approximately 6.4 kHz sampling rate
    }

    // Close SPI device
    close(spi_fd);

    return EXIT_SUCCESS;
}
