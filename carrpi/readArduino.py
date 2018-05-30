import serial
import struct
ser = serial.Serial('/dev/cu.usbmodem141241', 9600)
while 1:
   print(struct.unpack("hhhhhhhh",ser.read(16)))