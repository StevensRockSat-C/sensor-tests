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
#define X_DATA_REG 0x08
#define Y_DATA_REG 0x0A
#define Z_DATA_REG 0x0C

void set_register(uint8_t reg, uint8_t value);
int read_register(uint8_t reg);

#endif /* ADXL372_SPI_H */