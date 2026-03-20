int TRIG = 3;                 // Указываем вывод TRIG / PWM
 
void setup()
{
  pinMode(TRIG, OUTPUT);      // Устанавливаем вывод как выход
  digitalWrite(TRIG, LOW);    // Устанавливаем вывод в LOW

  // меняем частоту ШИМ с 490 Гц на 31250 Гц (31 кГц)
  TCCR2B = (TCCR2B & 0b11111000) | 0x01;
}
 
void loop()
{
  // digitalWrite(TRIG, HIGH);   // Включаем диод 
  // delay(2000);                // Пауза 2 с
  // digitalWrite(TRIG, LOW);    // Выключаем диод 
  // delay(2000);                // Пауза
 
// включить на x% и выключить
  analogWrite(TRIG, 64);
  delay(5000);
//  analogWrite(TRIG, 128);
//   delay(1000);
  analogWrite(TRIG, 255);
  delay(5000);
  //delay(1000);
}
