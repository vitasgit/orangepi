import spidev

spi = spidev.SpiDev()
spi.open(1, 1) # Шина SPI1, CS0. Если CSN на другом пине, проверьте номер.
spi.max_speed_hz = 5000000

# Команда 0x00 - чтение регистра CONFIG
# Отправляем 0x00 и следом 0xFF, чтобы вытолкнуть данные из модуля
resp = spi.xfer2([0x00, 0xFF])

print(f"Статус модуля: {hex(resp[0])}")
print(f"Значение регистра CONFIG: {hex(resp[1])}")

if resp[1] in [0x00, 0xff]:
    print("Ошибка: Модуль вернул 0x00 или 0xFF. Проверьте MOSI/MISO и питание!")
else:
    print("Успех: Модуль отвечает!")

spi.close()
