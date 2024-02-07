#ifndef ADXL372_SPI_H
#define ADXL372_SPI_H

#include <stdint.h>
#include <signal.h>
#include "accessLibs/spi.h"

#define SPI_DEVICE "/dev/spidev0.0"
#define SPI_SPEED 1000000
#define SPI_MODE 3
#define BITS_PER_WORD 8

#define POWER_CTL 0x2D
#define FILTER_CTL 0x2C
#define X_DATA_REG 0x08  // X-axis data register (12 bits)
#define Y_DATA_REG 0x0A  // Y-axis data register (12 bits)
#define Z_DATA_REG 0x0C  // Z-axis data register (12 bits)

int readRegister(SPI_HANDLE spi, uint8_t reg);
int readRegisterPair(SPI_HANDLE spi, uint8_t reg);
void terminate(int sign);

#endif /* ADXL372_SPI_H */