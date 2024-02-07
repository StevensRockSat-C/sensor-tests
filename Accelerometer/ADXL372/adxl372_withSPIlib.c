#include "spi.h"


SPI_HANDLE spi = SpiOpenPort(0,8,614400, SPI_MODE_0, false);
if (spi) {
    uint_t buf[3] = {WRITE_CMD, addr, byte };
    SpiWriteAndRead(spi, &buf[0], 3, false);
    SpiClosePort(spi);
}
    
