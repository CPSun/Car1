double tempOffset = 0;
float tempScale = 5.0/1024.0;

int tempPin = 3;
int voltagePins[] = { 10, 11, 12, 13, 14};

void setup() {
  Serial.begin(9600);
}

void loop() {
  printData();
}

void printData() {
  String printString = "";
  printString = printString + readTemperature() + ",";
  for(int ii = 0; ii < voltagePins.length; ii++) {
    printString = printString + 
  }

  Serial.println(printString);
  delay(200);
}

float readTemperature() {
  float temperature = analogRead(tempPin);
  temperature = (temperature * tempScale - .5) * 100.0;
  return (temperature * (9.0 / 5.0) + 32.0 - tempOffset);
}

float readVoltage(int pin, float calConst) {
  float voltage = analogRead(pin);
  return voltage - calConst;
}

float readAccel(int pin, float calConst) {
  float accel = analogRead(pin);
  
}

