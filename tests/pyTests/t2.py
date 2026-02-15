from RF24 import RF24, RF24_PA_LOW, RF24_1MBPS
import time

# Настройки пинов согласно вашему gpio readall
# CE_PIN: Физический пин 3 (GPIO 229)
# CSN: Используем 0 (так как мы сделали симлинк spidev1.0 -> spidev0.0)
CE_PIN = 229
CSN_PIN = 0

# Инициализируем радио
radio = RF24(CE_PIN, CSN_PIN)

def setup():
    print("Инициализация модуля NRF24L01...")

    if not radio.begin():
        print("ОШИБКА: Модуль не отвечает! Проверьте подключение и питание.")
        return False

    radio.setPALevel(RF24_PA_LOW)      # Низкое усиление (безопасно для тестов рядом)
    radio.setDataRate(RF24_1MBPS)      # Скорость 1 Мбит/с
    radio.setChannel(76)               # Канал (0-125)

    # Открываем трубу для чтения/записи (адрес 5 байт)
    address = b"1Node"
    radio.openWritingPipe(address)
    radio.openReadingPipe(1, address)

    radio.stopListening()              # Режим передачи

    print("--- Детали конфигурации ---")
    radio.printDetails()               # Если здесь будут нули или FF — связи нет
    print("---------------------------")
    return True

def loop():
    count = 0
    while True:
        message = f"Hello NRF {count}"
        print(f"Отправка: {message}")

        # Преобразуем строку в массив байтов (до 32 байт)
        payload = bytes(message, 'utf-8')
        result = radio.write(payload)

        if result:
            print("Доставлено!")
        else:
            print("Ошибка доставки (Ack не получен)")

        count += 1
        time.sleep(1)

if __name__ == "__main__":
    if setup():
        try:
            loop()
        except KeyboardInterrupt:
            print("\nОстановка программы")
