import serial

xb = serial.Serial("/dev/cu.usbserial-A5056WMY")

while(True):
   xb.write(b'255')