#include <iostream>
#include <RF24/RF24.h>
#include <unistd.h> // Для функции sleep/usleep

// На Orange Pi:
// Первый параметр — пин CE (GPIO номер)
// Второй параметр — индекс CSN (0 для /dev/spidev0.0 или 1 для /dev/spidev0.1)
RF24 radio(229, 1);

int main() {
    // Вместо Serial.begin
    std::cout << "Starting..." << std::endl;

    if (!radio.begin()) {
        std::cout << "Radio hardware not responding!" << std::endl;
        return 1;
    }

    std::cout << "Connected ";

    // Аналог radio.isPVariant()
    if (radio.isPVariant()) {
        std::cout << "nRF24L01+ - OK";
    } else {
        std::cout << "nRF24L01 (non-plus) or err";
    }

    std::cout << std::endl;

    // Эмуляция loop()
    while (true) {
        // Здесь будет ваш основной код
        usleep(100000); // Пауза 100мс, чтобы не перегружать процессор
    }

    return 0;
}
