int TRIG = 3;                 // Указываем вывод TRIG / PWM
 
void setup()
{
  pinMode(TRIG, OUTPUT);      // Устанавливаем вывод как выход
  digitalWrite(TRIG, LOW);    // Устанавливаем вывод в LOW
}
 
void loop()
{
  // digitalWrite(TRIG, HIGH);   // Включаем диод 
  // delay(1000);                // Пауза 2 с
  // digitalWrite(TRIG, LOW);    // Выключаем диод 
  // delay(1000);                // Пауза
 
// включить на x% и выключить
  analogWrite(TRIG, 64);
  delay(1000);
  digitalWrite(TRIG, LOW);
  delay(1000);
  analogWrite(TRIG, 128);
  delay(1000);
  digitalWrite(TRIG, LOW);
  delay(1000);
  analogWrite(TRIG, 255);
  delay(1000);
  digitalWrite(TRIG, LOW);
  delay(1000);
}