
float arduinoVoltage = 5.04;

float tempScale = arduinoVoltage/1024.0;

int tempPin = 1;
float tempOffset = 0;
float tempCalibS = 1;
float tempCalibR = 1;

int voltagePins[] = { 10, 11, 12, 13, 14};
float voltageOffsets[] = { 0, 0, 0, 0, 0 };
float voltageCalibS[] = { 1, 1, 1, 1, 1 }; //Resistor calibration
float voltageCalibR[] = { 1, 1, 1, 1, 1 }; //Resistor calibration

int accelPins[] = { 2, 3, 4, 5 };
float accelOffsets[] = { 0, 0, 0, 0};
float accelCalibS[] = { 1, 1, 1, 1}; //Sensor calibration
float accelCalibR[] = { 1, 1, 1, 1}; //Resistor calibration

int currentPins[] = { 6, 7, 8, 9 };
float currentOffsets[] = { 0, 0, 0, 0, 0 };
float currentCalibS[] = { 1, 1, 1, 1, 1 }; //Sensor calibration
float currentCalibR[] = { 1, 1, 1, 1, 1 }; //Resistor calibration

void setup() {
  Serial.begin(9600);
}

void loop() {
  printData();
  delay(1000);
}

void printData() {
  String printString = "Current: ";
  for(int ii = 0; ii < sizeof(voltagePins)/sizeof(int); ii++) {
    printString = printString + readCurrent(ii) + " ";
  }
  printString = printString + " Voltage: ";
  for(int ii = 0; ii < sizeof(voltagePins)/sizeof(int); ii++) {
    printString = printString + readVoltage(ii) + ", ";
  }
  printString = printString + "  Accelerometers: ";
  for(int ii = 0; ii < sizeof(accelPins)/sizeof(int); ii++) {
    printString = printString + readAccel(ii) + ", ";
  }
  printString = printString + "  Temperature: ";
  printString = printString + readTemperature() + ", ";

  Serial.println(printString.substring(0, printString.length() - 2));
  delay(200);
}

float readTemperature() {
  float temperature = analogRead(tempPin);
  temperature = (temperature * tempScale - .5) * 100.0;
  return (tempCalibR * tempCalibS * (temperature * (9.0 / 5.0) + 32.0));
}

float readVoltage(int index) {
  float voltage = analogRead(voltagePins[index]);
  return voltageCalibR[index] * voltageCalibS[index] * voltage;
}

float readCurrent(int index) {
  float voltage = analogRead(voltagePins[index]);
  return voltageCalibR[index] * voltageCalibS[index] * voltage;
}

float readAccel(int index) {
  float accel = analogRead(accelPins[index]);
  return accelCalibR[index] * accelCalibS[index] * accel;
}

