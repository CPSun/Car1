int tempPin = 0;
int tempMax = 83;
int tempMin = 77;
int relay = 7;

float increment = .5;
int tempScale = 1;

int tempCalibS = 1;

float tempOffset = 7;
void setup() {
  Serial.begin(9600);
  pinMode(relay, OUTPUT);
}

void loop() {
  while(readTemperature() < tempMax) {
    digitalWrite(relay, LOW);
    delay(increment*1000.0);
  }
  while(readTemperature() > tempMin) {
    digitalWrite(relay, HIGH);
    delay(increment*1000.0);
  }
  delay(500);
}

float readTemperature() {
  int reading = analogRead(tempPin);  
  float voltage = reading * 5.0;
  voltage /= 1024.0; 
  float temperatureC = (voltage - 0.5) * 100;
  float temperatureF = (temperatureC * 9.0 / 5.0) + 32.0 + tempOffset;
  Serial.println(temperatureF);
  return temperatureF;
}
