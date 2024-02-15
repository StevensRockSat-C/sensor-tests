#ifndef ADXL372_WITHSPILIB_H
#define ADXL372_WITHSPILIB_H

#include <stdint.h>
#include <signal.h>
#include "accessLibs/spi.c"

#define SPI_DEVICE 0
#define SPI_SPEED 5000000
#define SPI_MODE 2
#define BITS_PER_WORD 8

#define BYTE_TO_BINARY_PATTERN "%c%c%c%c%c%c%c%c"
#define BYTE_TO_BINARY(byte)  \
  ((byte) & 0x80 ? '1' : '0'), \
  ((byte) & 0x40 ? '1' : '0'), \
  ((byte) & 0x20 ? '1' : '0'), \
  ((byte) & 0x10 ? '1' : '0'), \
  ((byte) & 0x08 ? '1' : '0'), \
  ((byte) & 0x04 ? '1' : '0'), \
  ((byte) & 0x02 ? '1' : '0'), \
  ((byte) & 0x01 ? '1' : '0') 


/*
#define POWER_CTL 0x2D
#define FILTER_CTL 0x2C
#define X_DATA_REG 0x08  // X-axis data register (12 bits)
#define Y_DATA_REG 0x0A  // Y-axis data register (12 bits)
const uint8_t Z_DATA_REG = 0x0C  // Z-axis data register (12 bits)
*/

uint16_t readRegister(SPI_HANDLE spi, uint8_t reg);
int16_t readRegisterPair(SPI_HANDLE spi, uint8_t reg);
void terminate(int sign);

#endif /* ADXL372_WITHSPILIB_H */
