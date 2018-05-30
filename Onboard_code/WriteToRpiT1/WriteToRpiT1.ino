
int currentPins[] = { 0, 1, 2, 3};
int voltagePins[] = { 4, 5, 6, 7};
byte bytes[8];
float maxSize = 1023;
int maxWrite = 255;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
//  Serial.write("STARTING");
}

void loop() {
  byte *ptr = bytes;
  for (int ii = 0; ii < sizeof(currentPins) / sizeof(int); ii++) {
    int n = analogRead(voltagePins[0]);
    *(ptr++) = lowByte(n);
    *(ptr++) = highByte(n);
  }
  for (int ii = 0; ii < sizeof(voltagePins) / sizeof(int); ii++) {
    int n = analogRead(voltagePins[ii]);
    *(ptr++) = lowByte(n);
    *(ptr++) = highByte(n);
  }
  Serial.write(bytes, 16);
  delay(500);
}

