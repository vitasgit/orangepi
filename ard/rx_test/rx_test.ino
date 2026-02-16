#include <SPI.h>
#include <RF24.h>

#define LED 7
RF24 radio(9, 10); // CE, CSN
const byte address[6] = "NODE1";
char buffer[32];

void setup() {
  Serial.begin(9600);
  Serial.println("Arduino RX starting...");

  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);
  delay(500);
  digitalWrite(LED, LOW);

  if (!radio.begin()) {
    Serial.println("NRF24 init failed");
    while (1);
  }

  radio.setPALevel(RF24_PA_LOW);
  radio.setDataRate(RF24_1MBPS);
  radio.setChannel(76);

  radio.openReadingPipe(0, address);
  radio.startListening();

  Serial.println("Listening...");
}

void loop() {
  if (radio.available()) {
    memset(buffer, 0, sizeof(buffer));
    radio.read(&buffer, sizeof(buffer));

    String msg = String(buffer);
    Serial.print("Received: ");
    Serial.println(msg);

    if (msg == "LED_ON") {
      digitalWrite(LED, HIGH);
      Serial.println("LED ON");
    }
    else if (msg == "LED_OFF") {
      digitalWrite(LED, LOW);
      Serial.println("LED OFF");
    }
  }
}
