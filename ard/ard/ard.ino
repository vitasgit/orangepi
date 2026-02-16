#include <SPI.h>
#include <RF24.h>

// CE, CSN
RF24 radio(9, 10);

void setup() {
  Serial.begin(9600);
  while (!Serial) {}

  Serial.println(F("=== nRF24L01 Diagnostic Test ==="));

  if (!radio.begin()) {
    Serial.println(F("ERROR: nRF24L01 not responding"));
    while (1);
  }

  // Базовая настройка
  radio.setAutoAck(false);
  radio.setRetries(0, 0);
  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.setChannel(76);
  radio.disableCRC();

  // Переходим в приём, чтобы тестировать эфир
  radio.startListening();

  // Печать всех регистров (аналог printDetails)
  radio.printDetails();

  Serial.println(F("\n--- Parsed configuration ---"));

  Serial.print(F("Data rate: "));
  rf24_datarate_e dr = radio.getDataRate();
  if (dr == RF24_250KBPS) Serial.println(F("250 kbps"));
  else if (dr == RF24_1MBPS) Serial.println(F("1 Mbps"));
  else if (dr == RF24_2MBPS) Serial.println(F("2 Mbps"));

  Serial.print(F("PA level: "));
  rf24_pa_dbm_e pa = radio.getPALevel();
  if (pa == RF24_PA_MIN) Serial.println(F("MIN"));
  else if (pa == RF24_PA_LOW) Serial.println(F("LOW"));
  else if (pa == RF24_PA_HIGH) Serial.println(F("HIGH"));
  else if (pa == RF24_PA_MAX) Serial.println(F("MAX"));

  Serial.print(F("Channel: "));
  Serial.println(radio.getChannel());

  Serial.println(F("\nListening for carrier noise..."));
}

void loop() {
  uint8_t noise = 0;

  for (uint8_t ch = 0; ch < 128; ch++) {
    radio.setChannel(ch);
    radio.startListening();
    delayMicroseconds(140);
    radio.stopListening();

    if (radio.testCarrier()) {
      noise++;
    }
  }

  Serial.print(F("Active channels detected: "));
  Serial.println(noise);

  delay(2000);
}
