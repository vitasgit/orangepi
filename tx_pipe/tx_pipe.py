import time
import struct
from RF24 import RF24, RF24_PA_MAX, RF24_250KBPS, RF24_DRIVER
#from RF24 import *

CE_PIN = 73  # pin 7 на плате
CSN_PIN = 11  # для spidev1.1
radio = RF24(CE_PIN, CSN_PIN)

"""
    bool RF24::begin(void)
    возвращает true/false
    true - модуль инициализирован
    false - контроллер не смог инициализировать модуль
"""
if not radio.begin():
    print("радиомодуль не подключен")
    

# уровень мощности передатчика, чем выше мощность, тем дальше и лучше сигнал
radio.setPALevel(RF24_PA_MAX)

"""
    адрес трубы(pipe data).
    состоит из 5 байт, желательно задавать разные байты(стабильнее связь между модулями)
    pipe работает только в одну сторону, нельзя и отправлять данные и слушать. Только отправлять или  только слушать
"""
pipe1_addr = b"\x01\x02\x03\x04\x05"

radio.setAutoAck(1);        # режим подтверждения приёма, 1 вкл 0 выкл
radio.setRetries(0, 15);    # (время между попыткой достучаться, число попыток) 15 - максимальное
radio.setPayloadSize(1);   # пакет данных размером 1 байт (бубу передавать 1 или 0)
radio.setDataRate(RF24_250KBPS)  # Скорость передачи данных, чем меньше - тем дальше (скорость приема и передачи должна быть одинаковая)
radio.setChannel(76)  # выбираем канал передачи данных с самыми низкими помехами
radio.powerUp();        #  режим передачи (повышенного потребления), powerDown - режим ожидания
radio.openWritingPipe(pipe1_addr);   # открыть канал на отправку
radio.stopListening()  # режим передачи

print('Передача данных...')
while(1):
    cmd = input("(1 - включить светодиод/ 0 - выключить): ")
    if cmd == "1":
        data = b"\x01"
    elif cmd == "0":
        data = b"\x00"
    
    report = radio.write(data)
    if report:
        print(data, "OK")
    else:
        print("Ошибка")

    #print("Sent:", data, "OK" if report else "FAIL")
    time.sleep(1)
