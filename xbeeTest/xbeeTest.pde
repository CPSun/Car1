import processing.serial.*;

Serial xbee;
String potVal;

void setup() {
  try{
      printArray(Serial.list());
      // Open the port you are using at the rate you want:
      xbee = new Serial(this, Serial.list()[11], 9600);
      xbee.clear();
      xbee.bufferUntil(10);
    }catch(Exception e){
      println("Cannot open serial port.");
    }
}

void serialEvent(Serial xbee) {
  // See Tom Igoe's serial examples for more info
  potVal = xbee.readStringUntil(10); // read incoming data until line feed
  if (potVal != null) {
    println("Incoming data: " + potVal);
  }
}