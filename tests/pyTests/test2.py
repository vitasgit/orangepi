from RF24 import RF24, RF24_PA_LOW, RF24_1MBPS
import time

CE_PIN = 70      # pin3 229
CSN_PIN = 11       # Это должно дать spidev*.1

radio = RF24(CE_PIN, CSN_PIN)

print("Starting nRF24L01 test...")
if not radio.begin():
    print("ERROR: nRF24L01 not responding")
    exit(1)

radio.setPALevel(RF24_PA_LOW)
radio.setDataRate(RF24_1MBPS)
radio.setChannel(76)
radio.stopListening()

print("nRF24L01 initialized successfully")
radio.printDetails()

while True:
    time.sleep(2)
