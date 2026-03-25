void setup() {
  pinMode(3, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int gasValue = analogRead(A0);

  Serial.println(gasValue);

  if (gasValue > 500) {  // значения воздуха: 350-400
    digitalWrite(3, HIGH);
  } else {
    digitalWrite(3, LOW);
  }

  delay(200);
}