#include <SPI.h>
#include <RF24.h>

#define LED 7
RF24 radio(9, 10);
uint8_t pipe1_addr[5] = {0x01, 0x02, 0x03, 0x04, 0x05};

void setup() {
  Serial.begin(9600);
  Serial.println("RX start");

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);

  if (!radio.begin()) {
    Serial.println("радио не подключен");
    while(1);
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_250KBPS);
  radio.setChannel(76);
  radio.setPayloadSize(1);  // размер пакета (полезной нагрузки) - 1 байт (1 или 0)

  radio.openReadingPipe(1, pipe1_addr);
  radio.startListening();

  Serial.println("Listening...");
}

void loop() {
  if (radio.available()) {
    uint8_t data;
    radio.read(&data, 1);  // Читать 1 байт

    Serial.print("Received: ");
    Serial.println(data, HEX);

    if (data == 0x01) {
      digitalWrite(LED, HIGH);
      Serial.println("LED ON");
    }
    else if (data == 0x00) {
      digitalWrite(LED, LOW);
      Serial.println("LED OFF");
    }
  }
}