from RF24 import RF24

radio = RF24(229, 0)

if not radio.begin():
    print("NRF24 NOT responding")
else:
    print("NRF24 OK")
    radio.printDetails()
