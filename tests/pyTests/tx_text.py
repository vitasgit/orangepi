from RF24 import RF24, RF24_PA_LOW, RF24_1MBPS
import time

CE_PIN = 73     # 7pin
CSN = 1          # spidev1.1
SPI_BUS = 1      # SPI1

radio = RF24(CE_PIN, CSN, SPI_BUS)

print("Orange Pi TX starting...")

if not radio.begin():
    print("ERROR: nRF24L01 not responding")
    exit(1)

radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(RF24_1MBPS)
radio.setChannel(76)

address = b"NODE1"
radio.openWritingPipe(address)
radio.stopListening()

print("TX ready, sending commands...")

while True:
    cmd = input("(on - включить/ off - выключить): ")
    if cmd == "on":
        msg = b"LED_ON"
    elif cmd == "off":
        msg = b"LED_OFF"

    ok = radio.write(msg)

    print("Sent:", msg, "OK" if ok else "FAIL")
    #time.sleep(1)

