import spidev

SPI_BUS = 1
SPI_DEVICE = 0   # /dev/spidev1.0

spi = spidev.SpiDev()
spi.open(SPI_BUS, SPI_DEVICE)
spi.max_speed_hz = 100_000
spi.mode = 0b00

R_REGISTER = 0x00
STATUS_REG = 0x07

def read_register(reg):
    resp = spi.xfer2([R_REGISTER | reg, 0xFF])
    return resp[1]

print("Testing nRF24L01 (SPI only)...")

status = read_register(STATUS_REG)
print(f"STATUS = 0x{status:02X}")

if status in (0x00, 0xFF):
    print("❌ No response from nRF24L01")
else:
    print("✅ nRF24L01 responds via SPI")

spi.close()
