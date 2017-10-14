int tempPin = 0;
int tempMax = 84;
int tempMin = 76;
int relay = 1;

int tempScale = 1;

int tempCalibS = 1;

int tempOffset = 0;
void setup() {
  // put your setup code here, to run once:
}

void loop() {
  while(readTemperature() < tempMax) {
    digitalWrite(relay, HIGH);
    delay(1000);
  }
  while(readTemperature() > tempMin) {
    digitalWrite(relay, LOW);
    delay(1000);
  }
}

float readTemperature() {
  float temperature = analogRead(tempPin);
  temperature = (temperature * tempScale - .5) * 100.0;
  return (tempCalibS * (temperature * (9.0 / 5.0) + 32.0) - tempOffset);
}
